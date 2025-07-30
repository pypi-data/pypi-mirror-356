import os
from unittest.mock import patch

from paracuda.decorators import set_cuda_visible_devices


def environment_variable_is_set_during_context():
	with patch.dict(os.environ, {}, clear=True):
		with set_cuda_visible_devices("0,1"):
			assert os.environ.get("CUDA_VISIBLE_DEVICES") == "0,1"


def original_value_is_restored_after_context(self):
	with patch.dict(os.environ, {"CUDA_VISIBLE_DEVICES": "2,3"}, clear=True):
		with set_cuda_visible_devices("0,1"):
			pass
		assert os.environ.get("CUDA_VISIBLE_DEVICES") == "2,3"
