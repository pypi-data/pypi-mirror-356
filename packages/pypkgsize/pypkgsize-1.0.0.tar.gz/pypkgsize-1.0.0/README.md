# 📦 PkgSize - Python Package Size Analyzer

PkgSize is a CLI tool and Python library for analyzing the disk space usage of installed Python packages, helping you manage your environments efficiently.

## Core Features

*   **Comprehensive Size Analysis**: Displays installed Python packages with their disk usage in human-readable formats (KB, MB, GB).
*   **Flexible Sorting**: Sort packages by size (default), name, or installation date (feature to be confirmed/added if not present).
*   **Targeted Analysis**:
    *   Analyze packages in the current environment or specify a target virtual environment using `--path <venv_path>`.
    *   Filter by package name (`--name`), size threshold (`--threshold`), or focus on packages imported in your project (`--project-only <path_to_project>`).
*   **In-depth Dependency Insights**: 
    *   Use `--include-deps` to view a breakdown of package sizes including their unique dependencies.
    *   The console output shows an indented tree of dependencies with individual sizes.
    *   JSON exports include a detailed `dependencies_breakdown` structure.
*   **Detailed File Structure View**: Use `--tree` to explore the internal directory tree and file sizes of each package.
*   **Versatile Export Options**:
    *   Export reports in JSON, CSV, or Markdown formats.
    *   Specify an output directory with `--output <directory>` and format with `--format <format>`.
    *   Console output is automatically suppressed when exporting to a file (unless overridden).
*   **Customizable Output**:
    *   Show only the top N largest packages (`--top N`).
    *   Disable colorized CLI output with `--no-color`.
    *   Minimize output for scripting with `--quiet`.
*   **Environment Comparison**: Compare package sizes between two different Python environments (feature to be confirmed/added, e.g., `--compare <path_to_other_venv>`).


## Key CLI Options

The `pkgsize analyze` command supports various options to customize the analysis:

*   `--name <package_name>`: Filter results to show only specific packages (can be used multiple times).
*   `--top N`: Display only the top N largest packages.
*   `--threshold SIZE`: Filter out packages smaller than a specified size (e.g., `10MB`, `1GB`).
*   `--include-deps`: Include the size of dependencies and show a breakdown.
*   `--path <venv_path>`: Specify the path to a Python virtual environment to analyze its packages instead of the current environment.
*   `--project-only <project_path>`: (To be implemented/confirmed) Only show packages used in a given .py file or directory.
*   `--tree`: (To be implemented/confirmed) Show directory tree of package internals and file sizes.
*   `--output <directory_path>`: Specify a directory to export the report.
*   `--format <json|csv|md>`: Specify the output format for reports when using `--output`.
*   `--sort <size|name>`: Sort packages by size (default) or name. (Add 'date' if implemented)
*   `--no-color`: Disable CLI coloring.
*   `--quiet`: Suppress informational messages and console output, useful when only exporting.
*   `--version`: Display the version of PkgSize.
*   `--help`: Show the help message and exit.

## Installation

*(Placeholder for installation instructions, e.g., `pip install pypkgsize` if published, or steps for local editable install.)*
To install the package locally for development:
```bash
pip install -e .
```

## Basic Usage

Analyze packages in the current environment:
```bash
pkgsize analyze
```

Show the top 5 largest packages, including dependencies:
```bash
pkgsize analyze --top 5 --include-deps
```

Analyze packages in a specific virtual environment and export a CSV report:
```bash
pkgsize analyze --path /path/to/your/venv --output ./reports --format csv
```

Export a JSON report of packages larger than 50MB to the `my_reports` directory:
```bash
pkgsize analyze --threshold 50MB --output ./my_reports --format json
```

Analyze specific packages (e.g., `requests` and `numpy`):
```bash
pkgsize analyze --name requests --name numpy
```

Show the top 3 packages sorted by name:
```bash
pkgsize analyze --top 3 --sort name
```

Export a Markdown report of all packages, including dependencies, to the `docs` directory quietly (no console output):
```bash
pkgsize analyze --include-deps --output ./docs --format md --quiet
```
