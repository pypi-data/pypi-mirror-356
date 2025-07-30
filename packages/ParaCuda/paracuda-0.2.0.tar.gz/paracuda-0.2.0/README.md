# ParaCuda

![release](https://flat-badgen.vercel.app/github/release/gieses/paracuda)
![tag](https://flat-badgen.vercel.app/github/tag/gieses/ParaCuda)
![PyPI version](https://flat-badgen.vercel.app/pypi/v/ParaCuda)

<img src="assets/paracuda.png" width="400" height="200" alt="paracuda">

## Overview

**ParaCuda** is a **para**llel **cuda** execution framework for arbitrary tools. Consider it a (very) poor man's version of workflow
management systems. ParaCuda uses a config file that describes the script that needs to be run and the parameters
that we want to pass down to the script. ParaCuda then logs the execution and distributes it over all specified GPUs.

## Motivation

In machine learning, or modern bioinformatics we often require GPUs for execution of processes or predictions. Sometimes,
this is extremely trivial and a simple solution is desired that can run a script parameterized in different ways across
all available GPUs. ParaCuda addresses this challenge by easy set-up and execution of experiments concurrently.

## Installation

For the moment, clone the repository and create the environment using mamba.

```bash
git clone https://github.com/gieses/paracuda.git
mamba env create -f environment.yml
```


## Usage

Usage is very simple, use the `paracuda` command together with a configuration file (see below).

```bash
usage: paracuda [-h] --config CONFIG --gpus GPUS [--control_dir CONTROL_DIR] [--log-level {TRACE,DEBUG,INFO,SUCCESS,WARNING,ERROR,CRITICAL}] [--dry-run]

Run parallel grid search across multiple GPUs

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to JSON configuration file (default: None)
  --gpus GPUS           Number of GPUs to use (default: None)
  --control_dir CONTROL_DIR
                        Directory to store control files (default: control_dir)
  --log-level {TRACE,DEBUG,INFO,SUCCESS,WARNING,ERROR,CRITICAL}
                        Set the logging level (default: INFO)
  --dry-run             Only print commands without executing them (default: False)

```

Example

Please check the example directory for a simple demonstration of how to write the config and the python script. Note, 
that per default we generate all possible hyperparameter combinations from the config file to run the defined script.

```json
{
  "base_command": "python example/example_script.py",
  "output_dir": "results_directory",
  "param_grid": {
    "number": [1, 2, 3]
  }
}
```

```
paracuda --config example/example_config.json --gpus 2 --dry-run
```

Returns:

```bash
2025-06-18 23:48:35 | INFO     | 🔍 DRY RUN MODE: Commands will be printed but not executed
2025-06-18 23:48:35 | INFO     | 🔍 Starting grid search with 2 GPUs
2025-06-18 23:48:35 | SUCCESS  | 📂 Successfully loaded configuration from example/example_config.json
2025-06-18 23:48:35 | INFO     | 🧮 Generated 3 parameter combinations
2025-06-18 23:48:35 | INFO     | Storing results in: control_dir
2025-06-18 23:48:37 | INFO     | ⚙️ Starting parallel execution                                                                                                                                             
⏳ Starting... | ✅ 0 | ❌ 0:   0%|                                                                                                                                                          | 0/3 [00:02<?]
2025-06-18 23:48:40.455 | INFO     | paracuda.paracuda_run:run_task:148 - 🔍 [DRY RUN] Task 1 on GPU 0: c5b39f71
2025-06-18 23:48:40.455 | INFO     | paracuda.paracuda_run:run_task:149 - 📝 Command: CUDA_VISIBLE_DEVICES=0 python example/example_script.py --number 1 > control_dir/c5b39f7159270a92961b45aaf8ea44fa.log 2>&1
2025-06-18 23:48:40.455 | INFO     | paracuda.paracuda_run:run_task:148 - 🔍 [DRY RUN] Task 2 on GPU 1: e360de0c
2025-06-18 23:48:40.455 | INFO     | paracuda.paracuda_run:run_task:149 - 📝 Command: CUDA_VISIBLE_DEVICES=1 python example/example_script.py --number 2 > control_dir/e360de0cffb59c8b5711943068cee5e2.log 2>&1
2025-06-18 23:48:40.456 | INFO     | paracuda.paracuda_run:run_task:148 - 🔍 [DRY RUN] Task 3 on GPU 0: ba21f795
2025-06-18 23:48:40.456 | INFO     | paracuda.paracuda_run:run_task:149 - 📝 Command: CUDA_VISIBLE_DEVICES=0 python example/example_script.py --number 3 > control_dir/ba21f7957fd020b1c4473607144bf4ac.log 2>&1
⏳ Task 3 on GPU 0: ba21f795 | ✅ 3 | ❌ 0: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 3/3 [00:02<00:00]
2025-06-18 23:48:40 | SUCCESS  | ✨ Dry run completed! Printed 3 commands

```
