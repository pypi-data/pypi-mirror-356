import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"--gpu", type=str, default="0", help="GPU to use for the script"
	)
	parser.add_argument("--number", type=int, default=100, help="Number to square.")

	args = parser.parse_args()

	print(f"Using GPU: {args.gpu}")
	print(f"Number to square: {args.number}")
