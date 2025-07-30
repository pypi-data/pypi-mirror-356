"""ParaCuda: Parallel Grid Search Execution Framework
=================================================

A poor man's parallel grid search execution framework for machine learning experiments.

ParaCuda is a tool designed to distribute grid search experiments across multiple GPUs.
It manages parameter combinations, tracks progress, and handles execution of individual
training runs in parallel to maximize resource utilization.

It also brings colorful logs.

Usage
-----
From the command line:

```
Required arguments:
  --config PATH         Path to JSON configuration file
  --gpus N              Number of GPUs to use for parallel execution

Optional arguments:
  --control_dir PATH    Directory to store control files (default: "control_dir")
  --log-level LEVEL     Set logging verbosity (choices: TRACE, DEBUG, INFO, SUCCESS,
                        WARNING, ERROR, CRITICAL; default: INFO)
  --dry-run            Only print commands without executing them

Configuration File Format
------------------------
The configuration file should be a JSON document with the following structure:

```json
{
  "base_command": "python script_to_run.py",
  "output_dir": "results_directory",
  "param_grid": {
    "param1": ["value1", "value2"],
    "param2": [1, 2, 3],
    ...
  }
}

This will then run all grid combinations of the parameters specified in `param_grid` by calling a subprocess.

"""

import argparse
import json
import subprocess
import time
from multiprocessing import Manager, Pool
from pathlib import Path

import torch
from loguru import logger
from sklearn.model_selection import ParameterGrid
from tqdm.auto import tqdm

from paracuda import utils


def parse_args():
	"""Parse command-line arguments for configuring the grid search runner.

	Returns:
	    argparse.Namespace: Parsed arguments containing:
	        --config (str): Path to the JSON configuration file.
	        --gpus (int): Number of GPUs to use.
	"""
	parser = argparse.ArgumentParser(
		description="Run parallel grid search across multiple GPUs",
		formatter_class=argparse.ArgumentDefaultsHelpFormatter,
	)
	parser.add_argument("--config", type=str, required=True, help="Path to JSON configuration file")
	parser.add_argument("--gpus", type=int, required=True, help="Number of GPUs to use")
	parser.add_argument(
		"--control_dir",
		type=str,
		default="control_dir",
		help="Directory to store control files",
	)
	parser.add_argument(
		"--log-level",
		type=str,
		default="INFO",
		choices=["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"],
		help="Set the logging level",
	)
	parser.add_argument(
		"--dry-run",
		action="store_true",
		help="Only print commands without executing them",
	)
	return parser.parse_args()


def run_task(task_info):
	"""Run a single grid search task on a specified GPU.

	Args:
	    task_info (tuple): Contains:
	        idx (int): Task index.
	        params (dict): Parameter combination for this run.
	        gpu_id (int): GPU device ID to use.
	        base_command (str): Base command to execute.
	        output_dir (str or Path): Directory to store logs and done files.
	        progress_dict: Shared progress dictionary for tracking
	        dry_run (bool): If True, only print commands without executing them
	"""
	idx, params, gpu_id, base_command, output_dir, progress_dict, dry_run = task_info

	# Create parameter string for command
	param_str = " ".join([f"--{key} {value}" for key, value in params.items()])

	# Create unique identifier for this run
	param_id = "_".join([f"{key}-{value}" for key, value in params.items()])
	param_id_hash = utils.hash_string_md5(param_id)

	# Create output paths
	output_dir = Path(output_dir)
	output_dir.mkdir(parents=True, exist_ok=True)
	log_file = output_dir / f"{param_id_hash}.log"
	done_file = output_dir / f"{param_id_hash}.done"

	# Update progress dict to show current task details
	progress_dict["current_task"] = f"Task {idx + 1} on GPU {gpu_id}: {param_id_hash[:8]}"

	# Skip if already done and not in dry-run mode
	if done_file.exists() and not dry_run:
		logger.info(f"⏩ Skipping completed task ({idx + 1}): {param_id_hash[:8]} [GPU {gpu_id}]")
		# logger.info(f"📝 {param_id}")
		progress_dict["completed"] += 1
		return

	# Construct the full command
	command = f"CUDA_VISIBLE_DEVICES={gpu_id} {base_command} {param_str} > {log_file} 2>&1"

	if dry_run:
		# In dry-run mode, just print the command
		logger.info(f"🔍 [DRY RUN] Task {idx + 1} on GPU {gpu_id}: {param_id_hash[:8]}")
		logger.info(f"📝 Command: {command}")
		progress_dict["completed"] += 1
		return

	logger.info(f"🚀 Running task {idx + 1} on GPU {gpu_id}: {param_id_hash[:8]}")
	logger.debug(f"📝 Full command: {command}")

	start_time = time.time()
	try:
		subprocess.run(command, shell=True, check=True)
		# Mark as done if successful
		done_file.write_text("done")
		elapsed = time.time() - start_time
		logger.success(f"✅ Task {idx + 1} completed successfully in {elapsed:.2f}s")
		progress_dict["completed"] += 1
	except subprocess.CalledProcessError as e:
		logger.error(f"❌ Task {idx + 1} failed with error: {e}")
		progress_dict["failed"] += 1


def update_progress_bar(pbar, progress_dict):
	"""Update the progress bar with the latest information."""
	pbar.n = progress_dict["completed"] + progress_dict["failed"]
	pbar.set_description(
		f"⏳ {progress_dict['current_task']} | ✅ {progress_dict['completed']} | ❌ {progress_dict['failed']}"
	)
	pbar.refresh()


def main():
	"""Main function to coordinate parallel grid search across multiple GPUs.

	- Parses arguments.
	- Loads configuration from JSON.
	- Generates parameter combinations.
	- Assigns tasks to GPUs.
	- Runs tasks in parallel using multiprocessing.
	"""
	args = parse_args()

	# Configure logger
	logger.remove()
	logger.add(
		sink=lambda msg: tqdm.write(msg, end=""),
		level=args.log_level,
		format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
		colorize=True,
	)

	if args.dry_run:
		logger.info("🔍 DRY RUN MODE: Commands will be printed but not executed")

	logger.info(f"🔍 Starting grid search with {args.gpus} GPUs")

	# Check available GPUs if not in dry-run mode
	if not args.dry_run:
		available_gpus = torch.cuda.device_count()
		if args.gpus > available_gpus:
			logger.warning(
				f"⚠️ Requested <yellow>{args.gpus}</yellow> GPUs but only <yellow>{available_gpus}</yellow> are available"
			)
			args.gpus = available_gpus

		if args.gpus <= 0:
			logger.error("❌ Error: Need at least 1 GPU")
			return

	# Load configuration
	config_path = Path(args.config)
	try:
		with config_path.open("r") as f:
			config = json.load(f)
		logger.success(f"📂 Successfully loaded configuration from {config_path}")
	except Exception as e:
		logger.error(f"❌ Failed to load configuration: {e}")
		return

	# Extract configuration parameters
	base_command = config.get("base_command", "python script.py")
	output_dir = config.get("control_dir", args.control_dir)
	param_grid = config.get("param_grid", {})

	# Generate all parameter combinations
	combinations = list(ParameterGrid(param_grid))
	total_combinations = len(combinations)
	logger.info(f"🧮 Generated {total_combinations} parameter combinations")
	logger.info(f"Storing results in: {output_dir}")

	# Create a shared dictionary to track progress
	manager = Manager()
	progress_dict = manager.dict()
	progress_dict["completed"] = 0
	progress_dict["failed"] = 0
	progress_dict["current_task"] = "Starting..."

	# Prepare tasks with GPU assignments
	tasks = []
	for idx, params in enumerate(combinations):
		gpu_id = idx % args.gpus
		tasks.append((idx, params, gpu_id, base_command, output_dir, progress_dict, args.dry_run))

	# Create persistent progress bar
	pbar = tqdm(
		total=total_combinations,
		desc="Processing grid search tasks",
		unit="task",
		position=0,
		leave=True,
		dynamic_ncols=True,
		bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
	)

	# Run tasks in parallel with progress updates
	logger.info("⚙️ Starting parallel execution")

	# Create a pool for parallel processing
	with Pool(args.gpus) as pool:
		# Start asynchronously processing tasks
		results = pool.map_async(run_task, tasks)

		# Update progress bar until all tasks complete
		while not results.ready():
			update_progress_bar(pbar, progress_dict)
			time.sleep(0.1)

		# Final update to ensure we show 100% when done
		update_progress_bar(pbar, progress_dict)

	pbar.close()

	# Print final stats
	if args.dry_run:
		logger.success(f"✨ Dry run completed! Printed {progress_dict['completed']} commands")
	else:
		logger.success(
			f"✨ All tasks completed! ✅ Success: {progress_dict['completed']} | ❌ Failed: {progress_dict['failed']}"
		)


if __name__ == "__main__":
	main()
