import threading
from typing import Any, Dict, List, Optional, Union
import random
from contextlib import contextmanager
from types import SimpleNamespace
import time
import traceback
from optimas.utils.logging import setup_logger
from optimas.utils.prediction import Prediction

logger = setup_logger()


class BaseModule:
    """
    A base module class for defining reusable components in a multiagent pipeline.

    This class provides thread-safe configuration and variable management, error handling,
    and execution tracking. It serves as a foundation for implementing specialized
    processing modules within a pipeline architecture.

    Attributes:
        description (str): Description of the module's functionality
        input_fields (List[str]): List of expected input field names
        output_fields (List[str]): List of output field names this module produces
    """

    def __init__(
        self,
        description: str,
        input_fields: Optional[List[str]] = None,
        output_fields: Optional[List[str]] = None,
        variable: Optional[Any] = None,
        variable_search_space: Optional[Dict[str, List[Any]]] = None,
        # output_space: Optional[Dict[str, List[Any]]] = None,
        config: Optional[Dict[str, Any]] = None,
        num_retry: int = 100
    ):
        """
        Initialize the BaseModule.

        Args:
            description: Description of the module's functionality
            input_fields: List of expected input field names
            output_fields: List of output field names this module produces
            variable: Module variable for optimization (can be string, neural network, or dictionary)
            variable_search_space: Search space for variable optimization
            config: Configuration parameters
            num_retry: Number of retry attempts for forward execution
        """
        # Core attributes
        self.description = description
        self.num_retry = num_retry
        self.input_fields = input_fields or []
        self.output_fields = output_fields or []
        # self.output_space = output_space or []
        self.variable_search_space = variable_search_space
        self.traj = {}  # Store inputs and outputs for the module

        # Convert config into a dot-accessible object
        self.default_config = SimpleNamespace(**(config or {}))

        # Initialize default variable from search space or directly
        if self.variable_search_space and variable is None:
            self._default_variable = {
                key: random.choice(value)
                for key, value in self.variable_search_space.items()
            }
        else:
            self._default_variable = variable

        self.default_config = SimpleNamespace(**{**vars(self.default_config), "randomize_search_variable": False})
        self.config_keys = list(vars(self.default_config).keys())

        # Thread-local storage for configuration and variables
        self._thread_local = threading.local()
        # Lock for thread safety
        self._lock = threading.Lock()

    @property
    def optimizable(self) -> bool:
        """Check if this module has optimizable variables."""
        return self._default_variable is not None

    def update(self, new_variable: Any) -> None:
        """
        Replace the variable used in the module's forward process.

        Args:
            new_variable: The new variable to replace the existing variable
        """
        with self._lock:
            self._default_variable = new_variable
            # Update thread-local storage if it exists
            if hasattr(self._thread_local, "variable"):
                self._thread_local.variable = new_variable

    @property
    def variable(self):
        """
        Thread-safe access to the module's variable.

        Returns:
            The module's variable specific to the current thread
        """
        if not hasattr(self._thread_local, "variable"):
            with self._lock:
                self._thread_local.variable = self._default_variable
        return self._thread_local.variable

    @property
    def config(self) -> SimpleNamespace:
        """
        Thread-safe access to the module's config.

        Returns:
            SimpleNamespace: The module's configuration specific to the current thread
        """
        if not hasattr(self._thread_local, "config"):
            with self._lock:
                self._thread_local.config = SimpleNamespace(**vars(self.default_config))
        return self._thread_local.config

    def update_config(self, **kwargs) -> None:
        """
        Update configuration safely within a thread.

        Args:
            **kwargs: Configuration parameters to update

        Raises:
            ValueError: If an invalid configuration key is provided
        """
        with self._lock:
            config_dict = vars(self.config).copy()
            for key, value in kwargs.items():
                if key in self.config_keys:
                    config_dict[key] = value
                else:
                    raise ValueError(f"Invalid config key: {key}")
            self._thread_local.config = SimpleNamespace(**config_dict)

    @contextmanager
    def context(self, variable=None, **kwargs):
        """
        Context manager for temporary configuration and variable changes.
        Restores the original config and variable after exiting the context.

        Args:
            variable: Dictionary with variable changes or replacement variable
            **kwargs: Configuration parameters to change temporarily

        Yields:
            The module itself for method chaining

        Example:
            >>> with module.context(variable={"param": value}, config_option=value) as m:
            >>>     result = m.forward(input_data)
        """

        # Save original states
        original_config = vars(self.config).copy()
        original_variable = None
        original_default_config = vars(self.default_config).copy()

        # Update variable if needed
        if variable is not None and self._default_variable is not None:
            with self._lock:
                # Initialize and save original thread-local variable
                if not hasattr(self._thread_local, "variable"):
                    self._thread_local.variable = self._default_variable
                original_variable = self._thread_local.variable

                # Handle different variable types
                if isinstance(variable, dict) and isinstance(self._default_variable, dict):
                    # For dictionaries, create a new dict with updated values
                    if isinstance(original_variable, dict):
                        var_dict = original_variable.copy()
                        var_dict.update(variable)
                    else:
                        var_dict = variable.copy()

                    self._thread_local.variable = var_dict
                    # Temporarily override the default variable for all threads
                    self._default_variable = var_dict
                else:
                    # For strings, neural networks, or other types, replace directly
                    self._thread_local.variable = variable
                    # Temporarily override the default variable for all threads
                    self._default_variable = variable

        # Update config
        self.update_config(**kwargs)

        # Also update default_config for new threads
        if kwargs:
            with self._lock:
                config_dict = vars(self.default_config).copy()
                for key, value in kwargs.items():
                    if key in self.config_keys:
                        config_dict[key] = value
                self.default_config = SimpleNamespace(**config_dict)

        try:
            yield self  # Return self to allow method chaining
        finally:
            # Restore original states
            with self._lock:
                # Restore thread-local values
                self._thread_local.config = SimpleNamespace(**original_config)
                if original_variable is not None:
                    self._thread_local.variable = original_variable

                # Restore default values for new threads
                self._default_variable = original_variable or self._default_variable
                self.default_config = SimpleNamespace(**original_default_config)

    def __call__(self, **inputs: Any) -> Dict[str, Any]:
        """
        Executes the module and updates the trajectory.
        Uses the thread-safe configuration and variable.

        Args:
            **inputs: Input parameters for the module

        Returns:
            Dict[str, Any]: Output from the module

        Raises:
            Exception: If execution fails after max retries
        """
        # Get the current configuration explicitly to ensure it's thread-local
        current_config = self.config
        current_variable = self.variable

        # Always randomize fresh for each call if enabled
        temp_variable = None
        random_variable = None

        # Check if randomization is enabled and we have a search space
        if (hasattr(current_config, 'randomize_search_variable') and
            current_config.randomize_search_variable and
            self.variable_search_space):

            # Generate a completely fresh random variable
            random_variable = {
                key: random.choice(value)
                for key, value in self.variable_search_space.items()
            }

            temp_variable = current_variable

            # Set the random variable for just this call
            with self._lock:
                self._thread_local.variable = random_variable

            # For debugging - print what's happening
            print(f"[RANDOM] {self.__class__.__name__}: Generated random variable {random_variable}")

        # Prepare inputs
        if not isinstance(inputs, dict):
            raise ValueError("Inputs must be a dictionary.")

        # Try execution with retries
        outputs = None
        exception = None

        # print(f"[CALL] {self.__class__.__name__}: Current variable: {self.variable} Current config: {self.config}")
        # try:
        # for retry_count in range(self.num_retry):
        #     try:
        #         outputs = self.forward(**inputs)
        #         break
        #     except Exception as e:
        #         time.sleep(1)
        #         logger.warning(f"[Retry={retry_count}] Error executing module: {e}")
        #         logger.debug(traceback.format_exc())
        #         exception = e

        #         if retry_count == self.num_retry - 1:
        #             logger.error(f"Max retries reached. Unable to execute module.")
        outputs = self.forward(**inputs)
        # finally:
        #     # Always restore the original variable if we randomized
        #     if random_variable is not None and temp_variable is not None:
        #         with self._lock:
        #             self._thread_local.variable = temp_variable

        # If all retries failed, raise the last exception
        if outputs is None and exception is not None:
            raise exception

        # Handle Prediction objects
        if hasattr(outputs, 'items'):
            outputs = {key: item for key, item in outputs.items()}

        # Get the used variable BEFORE entering the lock
        used_variable = random_variable if random_variable is not None else current_variable

        with self._lock:
            self.traj = {
                "input": inputs,
                "output": outputs,
                "variable": used_variable if isinstance(used_variable, dict) else None,
            }

        return outputs

    def set_adapter_path(self, adapter_path: str, adapter_id: str = None):
        """
        Set the adapter path for a local LLM module.

        Args:
            adapter_path: Path to the LoRA adapter
            adapter_id: Unique identifier for the adapter in vLLM
        """
        if hasattr(self, "variable") and self.variable == "local_lm":
            self._current_adapter_path = adapter_path
            if adapter_id:
                self.model_id = adapter_id
            else:
                # Generate a unique adapter ID based on module name and timestamp
                import time

                self.model_id = f"{self.__class__.__name__.lower()}_{int(time.time())}"
        else:
            logger.warning(f"set_adapter_path called on non-local LLM module")


    def get_adapter_info(self):
        """
        Get current adapter information for this module.

        Returns:
            Dict containing adapter_id and adapter_path, or None if no adapter
        """
        if hasattr(self, "variable") and self.variable == "local_lm":
            adapter_id = getattr(self, "model_id", None)
            adapter_path = getattr(self, "_current_adapter_path", None)

            if adapter_id and adapter_path:
                return {"adapter_id": adapter_id, "adapter_path": adapter_path}
        return None
