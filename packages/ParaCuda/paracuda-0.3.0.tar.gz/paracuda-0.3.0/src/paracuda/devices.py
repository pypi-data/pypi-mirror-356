import os
from typing import List, Optional

import torch


def is_cuda_available() -> bool:
	"""Check if CUDA is available."""
	return torch.cuda.is_available()


def get_device_count() -> int:
	"""Get the number of available CUDA devices."""
	return torch.cuda.device_count() if is_cuda_available() else 0


def get_device(device_index: Optional[int] = None) -> torch.device:
	"""
	Get the appropriate device (CUDA or CPU) based on availability and index.

	Args:
	    device_index: CUDA device index to use. If None, uses the current device.
	                 If negative, counts backward from the end.

	Returns:
	    torch.device: The selected device
	"""
	if not is_cuda_available():
		return torch.device("cpu")

	device_count = get_device_count()

	if device_index is None:
		return torch.device("cuda")

	# Handle negative indexing
	if device_index < 0:
		device_index = device_count + device_index

	# Ensure the index is within bounds
	if device_index < 0 or device_index >= device_count:
		print(f"Warning: Requested device {device_index} out of range (0-{device_count - 1}). Using CPU.")
		return torch.device("cpu")

	return torch.device(f"cuda:{device_index}")


def get_visible_devices() -> List[int]:
	"""Parse CUDA_VISIBLE_DEVICES environment variable into a list of indices."""
	if "CUDA_VISIBLE_DEVICES" not in os.environ:
		return list(range(get_device_count()))

	cuda_visible_devices = os.environ.get("CUDA_VISIBLE_DEVICES", "")
	if cuda_visible_devices == "":
		return []

	return [int(idx) for idx in cuda_visible_devices.split(",") if idx.strip()]
