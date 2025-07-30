# Easy Dataset Share

A Python package and CLI tool to help you responsibly share datasets by gzipping files (such as `.jsonl`, `.csv`, etc.) in your repository and restoring them as needed.

## Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/Responsible-Dataset-Sharing/easy-dataset-share.git
```

Or, if you have cloned the repo locally:

```bash
pip install -e .
```

The dependency management is handled through `poetry` (https://python-poetry.org/).

## Quick start
To protect your dataset from nosy LLMs!:
  `easy-dataset-share magic-protect-dir <path to data directory> -p <password for encryption>`
To remove the protections from the dataset:
  `easy-dataset-share magic-unprotect-dir <path to data directory> -p <password for encryption>`


## Usage
You can call the CLI directly with `python easy_dataset_share/cli.py` or, if you already ran `pip install -e .`, it should put this command on your path and you can call `easy-dataset-share`.

`easy-dataset-share` is a CLI tool which has several subcommands, which you can explore using:

```
easy-dataset-share --help
```

Example output:
```
Commands:
  add-canary           Add canary files to a dataset for LLM training...
  add-robots           Generate and save a robots.txt file to prevent LLM...
  get-canary-string    Get the canary string for a directory.
  magic-protect-dir    Zip a directory and password protect it in one step.
  magic-unprotect-dir  Decrypt and extract a protected directory in one...
  remove-canary        Remove canary files from a dataset.
```

The workflow of the general tools is simple:
0. Add a robots.txt so that good actors don't train on this data!
1. add canaries to the data so that if people were training on it, we could tell! We add canaries in 2 ways; 1- adding canary files, and 2- adding canaries to the data itself
2. zip the data, so that the text (or whatever the data is) is not in plaintext! (This also makes hosting the data easier as it is now smaller)
3. password protect the zips, so that agents can't trivially unzip the data

The main command is `magic-protect-dir` and `magic-unprotect-dir`, which runs all 3 of these commands either forwards, or in reverse.


## Todos:
1. better documentation
2. Failure mode -
  one failure mode is that the canary string is not the same as the one that was used to protect the directory in this case, the canary files will not be removed - some checking here needs to be done.
4. tests to make sure you don't add canaries to a file twice, or not-remove data from the file.
5. the same try/excepts that exist for .json files should exist for .jsonl files. Add a dummy jsonl dataset that has a malformed line to make sure those edge cases are covered.

## Contributing

To set up git hooks properly, please run
`git config core.hooksPath .githooks`
(once). This will enable hooks such as running `yapf` on all python files

