[![Publishing Status](https://github.com/Reithan/MINT/actions/workflows/publish.yml/badge.svg?branch=main)](https://github.com/Reithan/MINT/actions/workflows/publish.yml)
[![CI Status](https://github.com/Reithan/MINT/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Reithan/MINT/actions/workflows/ci.yml)
# MINT
Meaning-Informed Next-token Transformation

## Project Goals
MINT adds a transformation layer that redistributes next\-token probabilities
according to semantic token similarity based on the model's embedding space. The
aim is to produce more varied, human\-like text without sacrificing coherence.

## Installation
Create a virtual environment and install the package in editable mode:

```bash
pip install -e .
```

This installs the `mint` package and provides the `mint` command-line interface.

To use the published release from PyPI (when available), run:

```bash
pip install mint-llm
```

## CLI Usage
Run the CLI with:

```bash
mint --help
```

The `mint` command exposes several subcommands. The typical workflow is shown
below.

## Using MINT

The recommended workflow progresses through four commands:

1. **Extract** token embeddings from a checkpoint.

   ```bash
   mint extract <model.safetensors> embeddings.safetensors
   ```

2. **Blend** the embeddings into a sparse similarity matrix. The command tries
   to use GPU 0 via CUDA, then Vulkan, before falling back to the CPU. Use
   `--cpu` to disable GPU usage or `--gpu <index>` to choose a device. The
   `--sdk` option selects the acceleration backend and values below `--tau`
   (default: `1e-4`) are pruned before saving the matrix as a PyTorch sparse
   tensor:

   ```bash
   mint blend embeddings.safetensors similarity.pt --cpu --tau 0.00001
   ```

3. **Infuse** a HuggingFace model with the similarity data. The model can be a
   Hub identifier or a local folder path.

   ```bash
   mint infuse model_id similarity.pt --alpha 0.1
   mint infuse ./local_model similarity.pt
   ```

4. **Brew** new text from the wrapped model.

   ```bash
   mint brew --model <model_id_or_path> --similarity similarity.pt --prompt "Hello"
   ```
  Omit `--prompt` or pass `--interactive` to read prompts line by line from
  stdin.

You can also explore the generator interactively using the CLI.

## Quickstart Script
Run [`examples/quickstart.py`](examples/quickstart.py) for an end-to-end
demonstration. The script mirrors the `mint` CLI commands:
`extract`, `blend` and `brew`.

Required argument:

- `--prompt` – input text to generate from.

Optional arguments default to values defined in
[`tests/utils/model_config.json`](tests/utils/model_config.json):

- `--checkpoint` – checkpoint path; if omitted `model_url` is downloaded.
- `--model` – model identifier or path; defaults to `model_id` or one derived
  from `model_url`.
- `--embeddings` – output file for embeddings (default
  `embeddings.safetensors`).
- `--similarity` – output file for the similarity matrix (default
  `similarity.pt`).
- `--tau` – sparsity threshold (default `1e-4`).

```bash
python examples/quickstart.py --prompt "Hello"
```

The script extracts embeddings, builds the similarity matrix and generates text
using the wrapped model.

## Examples
Practical examples are provided in the [notebooks](notebooks/) directory.
They demonstrate embedding extraction, building a similarity matrix and
brewing text from a short prompt.

## Development
Install development dependencies with:

```bash
pip install -e '.[dev]'
```

Use the provided Makefile to run common tasks:

```bash
make lint   # run ruff and mypy (if configured)
make format # check black formatting
make test   # run the pytest suite
make all    # runs all checks
```


`make` commands `format`, `lint`, and `all` can also be suffixed with `-fix` (e.g. `make format-fix`)
to attempt to automatically fix issues.

## Contributing
Development tasks are tracked in `todos.json`. See
[`project_proposal-MINT.md`](project_proposal-MINT.md) for the full technical
plan. Release notes are available in
[`CHANGELOG.md`](CHANGELOG.md). Feel free to open issues or pull requests to
contribute.


## Citation
If you use MINT in your research, please cite the project using the metadata in [CITATION.cff](CITATION.cff).
