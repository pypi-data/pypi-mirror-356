import hashlib
import re


def sanitize_filename(value: str) -> str:
	"""Sanitize a string to be safe for filenames.

	Args:
	        value (str): Input string to sanitize
	Returns:
	        str: Sanitized filename-safe string
	"""
	return re.sub(r"[^a-zA-Z0-9_-]", "_", str(value))


def hash_string_md5(param_str):
	"""Generate an MD5 hash for a given string.

	Args:
	        param_str (str): The string to hash.

	Returns:
	        str: The MD5 hash of the input string.
	"""
	return hashlib.md5(param_str.encode()).hexdigest()
