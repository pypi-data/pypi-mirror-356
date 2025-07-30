from paracuda.utils import hash_string_md5, sanitize_filename


def test_already_safe_string():
	"""Test strings with only allowed characters remain unchanged."""
	input_str = "safe_file-name123"
	assert sanitize_filename(input_str) == input_str


def test_spaces():
	"""Test spaces are replaced with underscores."""
	assert sanitize_filename("file name") == "file_name"


def test_special_characters():
	"""Test special characters are replaced with underscores."""
	assert sanitize_filename("file!@#$%^&*()name.txt") == "file__________name_txt"


def test_known_hash():
	"""Test a known string produces the expected MD5 hash."""
	# MD5 hash for "test"
	assert hash_string_md5("test") == "098f6bcd4621d373cade4e832627b4f6"
