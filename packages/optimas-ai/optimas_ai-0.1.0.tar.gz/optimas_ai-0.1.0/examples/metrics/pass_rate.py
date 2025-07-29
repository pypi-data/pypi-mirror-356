# from __future__ import annotations

# import atexit
# import itertools
# import multiprocessing as mp
# import os
# import shutil
# import sqlite3
# import tempfile
# import traceback
# from typing import Dict, List, Tuple, Union

# import numpy as np

# # -----------------------------------------------------------------------------
# # BigCodeBench import – keep the string import here so you only need to fix one
# # line if the path differs on your system.
# # -----------------------------------------------------------------------------
# try:
#     # Most installations expose it right here:
#     from bigcodebench.eval import untrusted_check  # type: ignore
# except ImportError as _e:  # pragma: no cover – adjust to your layout once
#     raise ImportError(
#         "Cannot import `untrusted_check` – please edit the import in metrics.py "
#         "to match your local BigCodeBench installation"
#     ) from _e

# # -----------------------------------------------------------------------------
# # Constants mirroring what `untrusted_check` returns
# # -----------------------------------------------------------------------------
# PASS: str = "pass"
# FAIL: str = "fail"
# TIMEOUT: str = "timeout"

# # -----------------------------------------------------------------------------
# # One‑time environment hardening
# # -----------------------------------------------------------------------------
# _DSPY_CACHE_DIR = tempfile.mkdtemp(prefix="dspy_cache_")
# os.environ.setdefault("DSPY_CACHEDIR", _DSPY_CACHE_DIR)
# os.environ.setdefault("LITELLM_CACHE_DIR", _DSPY_CACHE_DIR)

# # On Unix/macOS prefer `fork` so that child processes do not re‑import heavy
# # modules (which is where the cache corruption was triggered).
# if os.name == "posix":
#     try:
#         mp.set_start_method("fork")
#     except RuntimeError:
#         # Start‑method already set – nothing to do.
#         pass


# def _cleanup_cache() -> None:  # registered via `atexit` below
#     """Remove the temp cache directory created for this run."""
#     shutil.rmtree(_DSPY_CACHE_DIR, ignore_errors=True)


# aexit_id = atexit.register(_cleanup_cache)

# # -----------------------------------------------------------------------------
# # Compatibility helpers replicated from BigCodeBench
# # -----------------------------------------------------------------------------


# def compatible_eval_result(results: Dict) -> Dict:  # noqa: D401
#     """Make sure `results["eval"][task]["nfiles"]` is present for old logs."""
#     for task_results in results.get("eval", {}).values():
#         if "files" in task_results and "nfiles" not in task_results:
#             task_results["nfiles"] = len(task_results.pop("files"))
#     return results


# def estimate_pass_at_k(
#     num_samples: Union[int, List[int], np.ndarray],
#     num_correct: Union[List[int], np.ndarray],
#     k: int,
# ) -> np.ndarray:
#     """Unbiased pass@k estimator from OpenAI/human‑eval."""

#     def _estimator(n: int, c: int, k_: int) -> float:
#         if n - c < k_:
#             return 1.0
#         return 1.0 - np.prod(1.0 - k_ / np.arange(n - c + 1, n + 1))

#     if isinstance(num_samples, int):
#         num_samples_it = itertools.repeat(num_samples, len(num_correct))
#     else:
#         assert len(num_samples) == len(num_correct)
#         num_samples_it = iter(num_samples)

#     return np.array(
#         [_estimator(int(n), int(c), k) for n, c in zip(num_samples_it, num_correct)]
#     )


# # -----------------------------------------------------------------------------
# # Robust pass_rate wrapper
# # -----------------------------------------------------------------------------


# def pass_rate(
#     code: str,
#     unit_tests: str,
#     entry_point: str = "task_func",
#     *,
#     max_retries: int = 2,
#     verbose: bool = False,
#     resource_limits: Tuple[int, int, int] = (300 * 1024, 300 * 1024, 300 * 1024),
#     min_time_limit: float = 2.0,
#     gt_time_limit: float = 5.0,
# ) -> float:
#     """Return *1.0* if *all* tests pass, else *0.0*.

#     Retries `untrusted_check` when **framework‑level** exceptions occur (e.g.
#     corrupted SQLite cache files triggered during module import in the child
#     process).
#     """

#     max_as_limit, max_data_limit, max_stack_limit = resource_limits

#     for attempt in range(1, max_retries + 2):  # first try + `max_retries` more
#         try:
#             stat, details = untrusted_check(
#                 code,
#                 unit_tests,
#                 entry_point,
#                 max_as_limit=max_as_limit,
#                 max_data_limit=max_data_limit,
#                 max_stack_limit=max_stack_limit,
#                 min_time_limit=min_time_limit,
#                 gt_time_limit=gt_time_limit,
#             )

#             if verbose:
#                 print(f"[metrics.pass_rate] attempt={attempt} stat={stat}")
#                 if stat != PASS:
#                     print(f"details: {details}")

#             return 1.0 if stat == PASS else 0.0

#         # ----------------------------- cache corruption ----------------------
#         except sqlite3.DatabaseError as db_err:
#             if verbose:
#                 print(
#                     f"[metrics.pass_rate] SQLite error on attempt {attempt}: {db_err}\n"
#                     "Resetting temporary cache directory and retrying…"
#                 )
#             shutil.rmtree(
#                 os.environ.get("DSPY_CACHEDIR", _DSPY_CACHE_DIR), ignore_errors=True
#             )
#             new_dir = tempfile.mkdtemp(prefix="dspy_cache_")
#             os.environ["DSPY_CACHEDIR"] = new_dir
#             os.environ["LITELLM_CACHE_DIR"] = new_dir
#             continue  # retry

#         # --------------------------- any other exception ---------------------
#         except Exception as exc:  # pylint: disable=broad-except
#             if verbose:
#                 print(
#                     f"[metrics.pass_rate] untrusted_check crash on attempt {attempt}: {exc}"
#                 )
#                 traceback.print_exc()
#             continue  # retry

#     if verbose:
#         print("[metrics.pass_rate] All retries exhausted – treating as failure.")
#     return 0.0


# __all__ = [
#     "pass_rate",
#     "compatible_eval_result",
#     "estimate_pass_at_k",
# ]

from bigcodebench.eval import untrusted_check


def pass_rate(code, unit_tests, entry_point='task_func'):
    # try:
    result = untrusted_check(code,
                            unit_tests,
                            entry_point,
                            max_as_limit=300*1024,
                            max_data_limit=300*1024,
                            max_stack_limit=300*1024,
                            min_time_limit=2,
                            gt_time_limit=5)
    print(result)
    return float(result[0] == 'pass')
