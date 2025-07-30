# Flatten CLI

A fast, smart command-line tool to recursively flatten directory structures by copying all files into a single output directory. Perfect for preparing repository files for LLM context, code analysis, or file consolidation.

## Features

- **Fast recursive flattening** - Process entire directory trees in seconds
- **Smart filtering** - Built-in exclusions for common unwanted files/directories
- **Flexible file selection** - Include only specific file types or use preset filters
- **Conflict resolution** - Automatically handles duplicate filenames
- **Structure preservation** - Optionally preserve directory paths in filenames
- **LLM-ready** - Optimized for preparing codebases for AI context
- **Clean output** - Beautiful progress indicators and summary reports
- **Global configuration** - Customize default behavior with persistent settings

## Installation

### With pipx (recommended)

```bash
pipx install flatten-cli
```

### With pip

```bash
pip install flatten-cli
```

### From source

```bash
git clone https://github.com/yourusername/flatten-cli.git
cd flatten-cli
pipx install .
```

## Quick Start

```bash
# Basic usage - flatten a directory
flatten ./my-project ./flattened-output

# Flatten current directory
flatten . ./output

# Code files only (perfect for LLMs)
flatten ./repository ./context --code

# Current directory with code files and structure preservation
flatten . ./context --code --preserve

# Specific file types
flatten ./docs ./output -e .md .txt .rst

# Preserve directory structure in filenames
flatten ./src ./dest --preserve
```

## Configuration

Flatten CLI supports global configuration to customize default behavior. Your settings are stored in:

- **Linux/macOS**: `~/.config/flatten-cli/config.json`
- **Windows**: `%APPDATA%/flatten-cli/config.json`

### View Current Configuration

```bash
flatten config show
```

### Manage Exclude Patterns

```bash
# Add patterns to always exclude
flatten config add exclude .log .tmp "*.cache"

# Remove patterns from exclude list
flatten config remove exclude .DS_Store

# See what's currently excluded
flatten config show
```

### Manage Code Extensions

```bash
# Add file extensions to the --code preset
flatten config add extensions .svelte .astro .nim

# Remove extensions from code preset
flatten config remove extensions .bat .ps1

# Check current code extensions
flatten config show
```

### Set Default Behaviors

```bash
# Always preserve directory structure by default
flatten config set preserve_structure true

# Enable quiet mode by default
flatten config set quiet true

# Turn off defaults
flatten config set preserve_structure false
```

### Reset Configuration

```bash
# Reset everything to factory defaults
flatten config reset
```

## Usage

```
flatten [OPTIONS] SOURCE_DIR OUTPUT_DIR
```

### Arguments

- `SOURCE_DIR` - Directory to flatten (use `.` for current directory)
- `OUTPUT_DIR` - Where to place flattened files

### Options

| Flag             | Description                                      | Example                    |
| ---------------- | ------------------------------------------------ | -------------------------- |
| `-e, --ext`      | Include only specific extensions                 | `-e .py .js .md`           |
| `--code`         | Include all configured code file types           | `--code`                   |
| `-p, --preserve` | Keep directory structure in filenames            | `--preserve`               |
| `-x, --exclude`  | Additional patterns to exclude (adds to config)  | `-x test docs`             |
| `--exclude-only` | Use only these exclude patterns (ignores config) | `--exclude-only .git logs` |
| `-q, --quiet`    | Minimal output                                   | `--quiet`                  |
| `-v, --verbose`  | Show all skipped files                           | `--verbose`                |
| `-h, --help`     | Show help message                                | `--help`                   |

### Configuration Commands

| Command                                        | Description                   | Example                                      |
| ---------------------------------------------- | ----------------------------- | -------------------------------------------- |
| `flatten config show`                          | Display current configuration |                                              |
| `flatten config add exclude <patterns>`        | Add exclude patterns          | `flatten config add exclude .log .cache`     |
| `flatten config add extensions <exts>`         | Add code extensions           | `flatten config add extensions .svelte .vue` |
| `flatten config remove exclude <patterns>`     | Remove exclude patterns       | `flatten config remove exclude .DS_Store`    |
| `flatten config remove extensions <exts>`      | Remove code extensions        | `flatten config remove extensions .bat`      |
| `flatten config set preserve_structure <bool>` | Set default preserve behavior | `flatten config set preserve_structure true` |
| `flatten config set quiet <bool>`              | Set default quiet mode        | `flatten config set quiet false`             |
| `flatten config reset`                         | Reset to factory defaults     |                                              |

## Use Cases

### Preparing Code for LLMs

Perfect for giving AI assistants context about your entire codebase:

```bash
# Include all common code files from current directory
flatten . ./llm-context --code --preserve

# Include all common code files from a specific project
flatten ./my-app ./llm-context --code --preserve

# Custom selection for a Python project
flatten ./django-project ./context -e .py .html .css .js .md .yml .json --preserve

# Quick context from current directory
flatten . ./context --code
```

**The `--code` flag includes your configured extensions. Default includes:** `.py`, `.js`, `.ts`, `.jsx`, `.tsx`, `.vue`, `.go`, `.rs`, `.java`, `.cpp`, `.c`, `.h`, `.cs`, `.php`, `.rb`, `.swift`, `.kt`, `.scala`, `.sh`, `.bat`, `.ps1`, `.sql`, `.html`, `.css`, `.scss`, `.less`, `.json`, `.yaml`, `.yml`, `.toml`, `.xml`, `.md`, `.txt`, `.cfg`, `.ini`, `.env`, and more!

### File Organization

```bash
# Consolidate documentation from current directory
flatten . ./all-docs -e .md .txt .rst

# Gather configuration files
flatten ./project ./configs -e .json .yaml .yml .toml .ini .cfg

# Extract scripts from complex structure
flatten ./automation ./scripts -e .sh .bat .ps1 .py
```

### Code Analysis

```bash
# Prepare current directory for static analysis tools
flatten . ./analysis --code --quiet

# Extract specific language files from current directory
flatten . ./python-only -e .py

# Get all frontend assets
flatten ./webapp ./frontend -e .js .ts .jsx .tsx .vue .html .css .scss
```

## Smart Exclusions

Flatten CLI maintains a configurable list of patterns to automatically exclude. The default exclusions include:

**Directories:**

- `.git` - Git repository data
- `__pycache__` - Python cache files
- `.venv`, `venv` - Python virtual environments
- `node_modules` - Node.js dependencies
- `.pytest_cache`, `.mypy_cache` - Python tool caches
- `dist`, `build` - Build artifacts
- `.idea`, `.vscode` - IDE directories
- `.next`, `.nuxt` - Framework build directories
- `target` - Rust/Java build directories

**Files:**

- `.DS_Store` - macOS system files
- `*.pyc`, `*.pyo` - Python compiled files
- `*.class`, `*.jar` - Java compiled files
- `*.egg-info` - Python package info
- `.coverage`, `.nyc_output` - Coverage reports

### Customizing Exclusions

View current exclusions:

```bash
flatten config show
```

Add your own patterns:

```bash
flatten config add exclude logs temp "*.log" .env.local
```

Remove unwanted exclusions:

```bash
flatten config remove exclude .vscode .idea
```

Override config for a single command:

```bash
# Use only these exclusions, ignoring config
flatten ./project ./output --exclude-only .git node_modules

# Add to config exclusions for this run
flatten ./project ./output -x additional_temp_dir
```

## Examples

### First Time Setup

```bash
# Check default configuration
$ flatten config show
Config file: /home/user/.config/flatten-cli/config.json
Current configuration:
--------------------------------------------------
Exclude patterns:
   • .git
   • __pycache__
   • .venv
   • node_modules
   • .DS_Store
   [... more patterns]

# Customize for your needs
$ flatten config add exclude .env.local .terraform
Added '.env.local' to exclude
Added '.terraform' to exclude

$ flatten config add extensions .svelte .astro
Added '.svelte' to extensions
Added '.astro' to extensions
```

### Basic Flattening

```bash
$ flatten ./my-project ./flattened
Flattening: /home/user/my-project
Output: /home/user/flattened
Excluding: .git, __pycache__, .venv, node_modules, .DS_Store
────────────────────────────────────────────────────────
Copied: src/main.py → main.py
Copied: src/utils/helpers.py → helpers.py
Copied: docs/README.md → README.md
Copied: tests/test_main.py → test_main.py
────────────────────────────────────────────────────────
Complete! Copied 15 files, skipped 8
```

### Code Files with Structure Preservation

```bash
$ flatten ./webapp ./context --code --preserve
Flattening: /home/user/webapp
Output: /home/user/context
Excluding: .git, __pycache__, .venv, node_modules, .DS_Store
Including: .py, .js, .ts, .jsx, .tsx, .vue, .go, .rs, .java, .cpp, .c, .h, .cs, .php, .rb, .swift, .kt, .scala, .sh, .bat, .ps1, .sql, .html, .css, .scss, .less, .json, .yaml, .yml, .toml, .xml, .md, .txt, .cfg, .ini, .env, .dockerfile, .gitignore, .gitattributes
────────────────────────────────────────────────────────
Copied: src/components/Header.jsx → src__components__Header.jsx
Copied: src/utils/api.js → src__utils__api.js
Copied: styles/main.css → styles__main.css
Copied: package.json → package.json
────────────────────────────────────────────────────────
Complete! Copied 42 files, skipped 156
```

### Quiet Mode for Scripts

```bash
$ flatten ./docs ./output -e .md --quiet
# No output, just processing...
$ echo $?
0  # Success!
```

## Advanced Usage

### Filename Conflict Resolution

When files have the same name, flatten automatically resolves conflicts:

```
src/utils.py     → utils.py
lib/utils.py     → utils__1.py
helpers/utils.py → utils__2.py
```

### Structure Preservation

With `--preserve`, directory paths become part of the filename:

```
src/components/Button.jsx → src__components__Button.jsx
tests/unit/helpers.py     → tests__unit__helpers.py
```

### Combining Options

```bash
# Complex filtering example
flatten ./monorepo ./extracted \
  --code \
  --preserve \
  --exclude node_modules dist .next .cache \
  --verbose
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests if applicable
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

## Development

```bash
# Clone and setup
git clone https://github.com/yourusername/flatten-cli.git
cd flatten-cli

# Install in development mode
pipx install -e .

# Run tests (if you add them)
python -m pytest

# Format code
black flatten/
```

## Issues & Feature Requests

Found a bug or have a feature idea? [Open an issue](https://github.com/yourusername/flatten-cli/issues) on GitHub!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
