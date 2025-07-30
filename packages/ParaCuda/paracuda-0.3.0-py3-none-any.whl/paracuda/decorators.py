import os
from contextlib import contextmanager


@contextmanager
def set_cuda_visible_devices(gpu_ids):
	"""
	Context manager to set the CUDA_VISIBLE_DEVICES environment variable.

	Parameters:
	- gpu_ids (str): A comma-separated string of GPU IDs to be made visible to CUDA.

	Usage:
	        ```python
	                with set_cuda_visible_devices("0,1"):
	        # The following code can now use the specified GPUs
	        pass
	    ```

	The specified GPUs will be set as visible for the duration of the context.
	"""
	# Save the original CUDA_VISIBLE_DEVICES value
	original_cuda_visible_devices = os.environ.get("CUDA_VISIBLE_DEVICES", "")
	os.environ["CUDA_VISIBLE_DEVICES"] = gpu_ids

	try:
		# Yield control to the block of code within the 'with' statement
		yield
	finally:
		# Restore the original CUDA_VISIBLE_DEVICES value
		os.environ["CUDA_VISIBLE_DEVICES"] = original_cuda_visible_devices
