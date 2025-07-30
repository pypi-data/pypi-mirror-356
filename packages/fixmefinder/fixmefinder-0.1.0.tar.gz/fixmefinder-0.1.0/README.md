# fixmefinder

fixmefinder is a command-line tool that scans Python files for `# TODO:` and `# FIXME:` comments, creates issues for them in Linear, and updates the comments with the issue ID.

## Features

- Detects `TODO` / `FIXME` comments in `.py` files
- Respects `.gitignore`
- Creates issues in Linear using its API
- Updates comments with the Linear issue ID

## Installation

1. install `uv`
2. run `uv tool install fixmefinder`

## Usage

3. run `fixmefinder` from the repo root

## License

This project is licensed under the MIT License.
