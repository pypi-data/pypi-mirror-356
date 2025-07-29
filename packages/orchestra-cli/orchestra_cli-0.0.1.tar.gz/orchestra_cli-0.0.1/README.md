# orchestra-cli

A Python-based CLI tool for running Orchestra actions.

## Usage

```bash
orchestra-cli validate example.yaml
```

## Development

- Make sure [uv](https://github.com/astral-sh/uv) is installed
- Use `uv pip install -e ".[dev]"` to install the CLI in editable mode for development

## Building and Releasing

- Run `uv build` to build the CLI
- Run `uv publish` to publish the CLI

## Troubleshooting

- If `orchestra-cli` is not found, make sure you have run `uv pip install -e .` and your venv is activated.
- If you get 'No such command', check you are using the correct subcommand (e.g., `validate`).
