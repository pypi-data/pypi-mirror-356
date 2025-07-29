import requests
import time
import os
import json
from typing import Optional, Dict, Any, List
from optimas.utils.logging import setup_logger

logger = setup_logger(__name__)


def _api(host: str, port: int, path: str) -> str:
    return f"http://{host}:{port}{path}"


def list_models(host="localhost", port=8001) -> list[str]:
    """Return the names served by the vLLM daemon (base + LoRAs)."""
    r = requests.get(_api(host, port, "/v1/models"), timeout=30)
    r.raise_for_status()
    data = r.json()
    return [m["id"] for m in data.get("data", [])]


def unload_lora_adapter(
    lora_name: str, host="localhost", port=8001, silent: bool = False
) -> None:
    """POST /v1/unload_lora_adapter (ignore 404)."""
    r = requests.post(
        _api(host, port, "/v1/unload_lora_adapter"),
        json={"lora_name": lora_name},
        timeout=120,
    )
    if r.ok:
        if not silent:
            print(f"[vLLM] unloaded «{lora_name}»")
    else:
        # 404 means not loaded – fine
        if r.status_code != 404:
            raise RuntimeError(f"Could not unload {lora_name}: {r.text}")


def load_lora_adapter(
    lora_name: str, lora_path: str, host="localhost", port=8001, retries: int = 3
) -> None:
    """Ensure *exactly one* copy of <lora_name> is served, then load it."""
    if lora_name in list_models(host, port):
        unload_lora_adapter(lora_name, host, port, silent=True)

    payload = {"lora_name": lora_name, "lora_path": lora_path}
    for i in range(retries):
        r = requests.post(
            _api(host, port, "/v1/load_lora_adapter"), json=payload, timeout=300
        )
        if r.ok:
            print(f"[vLLM] loaded «{lora_name}» from {lora_path}")
            return
        print(f"[vLLM] load failed ({i+1}/{retries}): {r.text}")
        time.sleep(2)

    raise RuntimeError(f"Could not load LoRA {lora_name}")


def update_pipeline_with_ppo_results(pipeline, ppo_output_base_dir, module_names=None):
    """
    Update pipeline modules to use the results from PPO training.

    Args:
        pipeline: The CompoundAgentPipeline instance
        ppo_output_base_dir: Base directory containing PPO outputs
        module_names: List of module names to update, or None for all optimizable modules
    """
    from optimas.utils.lora import get_adapter_from_ppo_output, load_lora_adapter

    if module_names is None:
        module_names = [
            name
            for name, module in pipeline.modules.items()
            if hasattr(module, "variable") and module.variable == "local_lm"
        ]

    host = os.getenv("VLLM_HOST", "localhost")
    port = int(os.getenv("VLLM_PORT", "8001"))

    for module_name in module_names:
        if module_name not in pipeline.modules:
            logger.warning(f"Module {module_name} not found in pipeline")
            continue

        module = pipeline.modules[module_name]

        # Check if this is a local LLM module
        if not (hasattr(module, "variable") and module.variable == "local_lm"):
            logger.info(f"Skipping non-local LLM module: {module_name}")
            continue

        # Look for PPO results
        best_adapter_path = get_adapter_from_ppo_output(
            ppo_output_base_dir, module_name
        )

        if best_adapter_path:
            adapter_id = f"{module_name}_ppo_optimized"

            success = load_lora_adapter(adapter_id, best_adapter_path, host, port)

            if success:
                if hasattr(module, "set_adapter_path"):
                    module.set_adapter_path(best_adapter_path, adapter_id)
                else:
                    module.model_id = adapter_id
                    module._current_adapter_path = best_adapter_path

                logger.info(
                    f"Updated module {module_name} with PPO adapter from {best_adapter_path}"
                )
            else:
                logger.error(f"Failed to load PPO adapter for module {module_name}")
        else:
            logger.info(f"No PPO adapter found for module {module_name}")


# ============ NEW FUNCTIONS FOR ON-POLICY OPTIMIZATION ============


def check_vllm_server_status(
    host: str = "localhost", port: int = 8001, timeout: float = 5.0
) -> bool:
    """
    Check if vLLM server is running and responsive.

    Args:
        host: vLLM server host
        port: vLLM server port
        timeout: Request timeout in seconds

    Returns:
        bool: True if server is responsive, False otherwise
    """
    try:
        # Try to list models as a health check
        list_models(host, port)
        return True
    except Exception:
        return False


def wait_for_vllm_server(
    host: str = "localhost",
    port: int = 8001,
    max_wait_time: float = 300.0,
    check_interval: float = 5.0,
) -> bool:
    """
    Wait for vLLM server to become available.

    Args:
        host: vLLM server host
        port: vLLM server port
        max_wait_time: Maximum time to wait in seconds
        check_interval: Time between status checks in seconds

    Returns:
        bool: True if server becomes available, False if timeout
    """
    logger.info(f"Waiting for vLLM server at {host}:{port}...")

    start_time = time.time()
    while time.time() - start_time < max_wait_time:
        if check_vllm_server_status(host, port):
            logger.info("vLLM server is ready!")
            return True

        elapsed = time.time() - start_time
        logger.info(f"Waiting for server... ({elapsed:.1f}s elapsed)")
        time.sleep(check_interval)

    logger.error(f"Timeout waiting for vLLM server after {max_wait_time}s")
    return False


def cleanup_all_adapters(
    host: str = "localhost", port: int = 8001, exclude_base: bool = True
) -> bool:
    """
    Unload all currently loaded LoRA adapters.

    Args:
        host: vLLM server host
        port: vLLM server port
        exclude_base: Whether to exclude base model from cleanup

    Returns:
        bool: True if all adapters were unloaded successfully
    """
    try:
        models = list_models(host, port)
        base_model = os.getenv("VLLM_BASE_MODEL", "")
        base_model_name = os.path.basename(base_model) if base_model else ""

        adapters_to_unload = []
        for model in models:
            # Skip base model if exclude_base is True
            if exclude_base and (model == base_model or model == base_model_name):
                continue
            # Skip if it looks like a base model path
            if exclude_base and (
                "/" in model or model.startswith("meta-") or model.startswith("Qwen")
            ):
                continue
            adapters_to_unload.append(model)

        if not adapters_to_unload:
            logger.info("No adapters to cleanup")
            return True

        success = True
        for adapter_name in adapters_to_unload:
            try:
                unload_lora_adapter(adapter_name, host, port, silent=True)
            except Exception as e:
                logger.warning(f"Failed to unload adapter {adapter_name}: {e}")
                success = False

        logger.info(f"Cleaned up {len(adapters_to_unload)} adapters")
        return success

    except Exception as e:
        logger.error(f"Failed to cleanup adapters: {e}")
        return False


def get_adapter_from_ppo_output(ppo_output_dir: str, module_name: str) -> Optional[str]:
    """
    Find the best adapter from PPO output directory.

    Args:
        ppo_output_dir: PPO output directory (should contain ppo/module_name subdirectory)
        module_name: Name of the module

    Returns:
        Path to the best adapter, or None if not found
    """
    # Handle both cases: ppo_output_dir is the module dir or contains ppo/module_name
    if os.path.basename(ppo_output_dir) == module_name:
        module_ppo_dir = ppo_output_dir
    else:
        module_ppo_dir = os.path.join(ppo_output_dir, "ppo", module_name)

    if not os.path.exists(module_ppo_dir):
        logger.warning(f"PPO output directory not found: {module_ppo_dir}")
        return None

    # Look for final directory first
    final_dir = os.path.join(module_ppo_dir, "final")
    if os.path.exists(final_dir) and os.path.isdir(final_dir):
        # Check if it contains necessary files (adapter_config.json, adapter_model.bin/safetensors)
        required_files = ["adapter_config.json"]
        has_model_file = any(
            os.path.exists(os.path.join(final_dir, f))
            for f in ["adapter_model.bin", "adapter_model.safetensors"]
        )

        if has_model_file and all(
            os.path.exists(os.path.join(final_dir, f)) for f in required_files
        ):
            logger.info(f"Found final adapter: {final_dir}")
            return final_dir

    # Look for step directories
    step_dirs = []
    try:
        for item in os.listdir(module_ppo_dir):
            if item.startswith("step_"):
                step_dir = os.path.join(module_ppo_dir, item)
                if os.path.isdir(step_dir):
                    try:
                        step_num = int(item.split("step_")[-1])
                        # Check if this step directory has the required files
                        required_files = ["adapter_config.json"]
                        has_model_file = any(
                            os.path.exists(os.path.join(step_dir, f))
                            for f in ["adapter_model.bin", "adapter_model.safetensors"]
                        )

                        if has_model_file and all(
                            os.path.exists(os.path.join(step_dir, f))
                            for f in required_files
                        ):
                            step_dirs.append((step_num, step_dir))
                    except ValueError:
                        continue
    except OSError as e:
        logger.error(f"Error reading directory {module_ppo_dir}: {e}")
        return None

    if step_dirs:
        # Sort by step number and return the latest
        step_dirs.sort(key=lambda x: x[0])
        latest_step_dir = step_dirs[-1][1]
        logger.info(f"Found latest step adapter: {latest_step_dir}")
        return latest_step_dir

    logger.warning(f"No valid adapter found in {module_ppo_dir}")
    return None


def load_adapter_safe(
    lora_name: str,
    lora_path: str,
    host: str = "localhost",
    port: int = 8001,
    retries: int = 3,
    verify_load: bool = True,
) -> bool:
    """
    Safely load a LoRA adapter with verification and return success status.

    Args:
        lora_name: Name for the adapter
        lora_path: Path to the adapter
        host: vLLM server host
        port: vLLM server port
        retries: Number of retry attempts
        verify_load: Whether to verify the adapter was loaded successfully

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Check if path exists and contains required files
        if not os.path.exists(lora_path):
            logger.error(f"Adapter path does not exist: {lora_path}")
            return False

        required_files = ["adapter_config.json"]
        has_model_file = any(
            os.path.exists(os.path.join(lora_path, f))
            for f in ["adapter_model.bin", "adapter_model.safetensors"]
        )

        if not has_model_file or not all(
            os.path.exists(os.path.join(lora_path, f)) for f in required_files
        ):
            logger.error(f"Adapter directory missing required files: {lora_path}")
            return False

        # Use the existing robust load function
        load_lora_adapter(lora_name, lora_path, host, port, retries)

        # Verify the adapter was loaded if requested
        if verify_load:
            models = list_models(host, port)
            if lora_name not in models:
                logger.error(
                    f"Adapter {lora_name} not found in model list after loading"
                )
                return False

        logger.info(f"Successfully loaded adapter {lora_name}")
        return True

    except Exception as e:
        logger.error(f"Failed to load adapter {lora_name}: {e}")
        return False


def unload_adapter_safe(
    lora_name: str, host: str = "localhost", port: int = 8001
) -> bool:
    """
    Safely unload a LoRA adapter and return success status.

    Args:
        lora_name: Name of the adapter to unload
        host: vLLM server host
        port: vLLM server port

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        unload_lora_adapter(lora_name, host, port, silent=True)
        logger.info(f"Successfully unloaded adapter {lora_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to unload adapter {lora_name}: {e}")
        return False


class LoRAAdapterManager:
    """
    Context manager for LoRA adapters that ensures cleanup.
    """

    def __init__(
        self,
        adapter_name: str,
        adapter_path: str,
        host: str = "localhost",
        port: int = 8001,
        auto_cleanup: bool = True,
    ):
        self.adapter_name = adapter_name
        self.adapter_path = adapter_path
        self.host = host
        self.port = port
        self.auto_cleanup = auto_cleanup
        self.loaded = False

    def __enter__(self):
        """Load the adapter when entering the context."""
        self.loaded = load_adapter_safe(
            self.adapter_name, self.adapter_path, self.host, self.port
        )

        if not self.loaded:
            raise RuntimeError(f"Failed to load LoRA adapter {self.adapter_name}")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Unload the adapter when exiting the context."""
        if self.loaded and self.auto_cleanup:
            unload_adapter_safe(self.adapter_name, self.host, self.port)


def get_adapter_info(adapter_path: str) -> Optional[Dict[str, Any]]:
    """
    Get information about a LoRA adapter from its config file.

    Args:
        adapter_path: Path to the adapter directory

    Returns:
        Dict containing adapter configuration, or None if not found
    """
    config_path = os.path.join(adapter_path, "adapter_config.json")

    if not os.path.exists(config_path):
        return None

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        return config
    except Exception as e:
        logger.warning(f"Failed to read adapter config from {config_path}: {e}")
        return None


def list_available_adapters(search_dirs: List[str]) -> Dict[str, str]:
    """
    Search for available LoRA adapters in the given directories.

    Args:
        search_dirs: List of directories to search for adapters

    Returns:
        Dict mapping adapter names to their paths
    """
    adapters = {}

    for search_dir in search_dirs:
        if not os.path.exists(search_dir):
            continue

        try:
            for item in os.listdir(search_dir):
                item_path = os.path.join(search_dir, item)
                if os.path.isdir(item_path):
                    # Check if this directory contains an adapter
                    if get_adapter_info(item_path) is not None:
                        adapters[item] = item_path
        except OSError as e:
            logger.warning(f"Error searching directory {search_dir}: {e}")

    return adapters
