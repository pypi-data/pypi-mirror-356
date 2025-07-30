import click
import json
import csv
import importlib.metadata
import fnmatch
import os
import subprocess
import json
from pathlib import Path
from .core import get_installed_packages_info

def is_valid_venv(venv_path_str):
    """Checks if the given path is a Python virtual environment."""
    if not venv_path_str:
        return False
    venv_path = Path(venv_path_str)
    if not venv_path.is_dir():
        return False

    pyvenv_cfg_path = venv_path / 'pyvenv.cfg'
    if not pyvenv_cfg_path.is_file():
        return False

    if os.name == 'nt':
        python_exe_path = venv_path / 'Scripts' / 'python.exe'
    else:
        python_exe_path = venv_path / 'bin' / 'python'
    
    if not python_exe_path.is_file():
        return False
    
    return True

def parse_size_to_bytes(size_str):
    """
    Parses a size string (e.g., "10MB", "500KB", "1GB") and returns size in bytes.
    Returns None if parsing fails.
    """
    if not size_str:
        return None
    
    size_str = size_str.upper().strip()
    units = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3}
    
    num_part = ""
    unit_part = ""
    
    for char in reversed(size_str):
        if char.isalpha():
            unit_part = char + unit_part
        else:
            num_part = char + num_part
            
    if not num_part:
        return None

    try:
        size = float(num_part)
    except ValueError:
        return None

    if unit_part == "K": unit_part = "KB"
    if unit_part == "M": unit_part = "MB"
    if unit_part == "G": unit_part = "GB"
    
    if unit_part in units:
        return int(size * units[unit_part])
    elif not unit_part and size_str == num_part:
        return int(size)
    else:
        click.echo(f"Error: Unknown size unit '{unit_part}' in threshold '{size_str}'. Use B, KB, MB, or GB.", err=True)
        return None

def format_size(size_bytes):
    """Converts size in bytes to a human-readable string (KB, MB, GB)."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes/1024:.2f} KB"
    elif size_bytes < 1024**3:
        return f"{size_bytes/1024**2:.2f} MB"
    else:
        return f"{size_bytes/1024**3:.2f} GB"

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    try:
        version = importlib.metadata.version('pkgsize')
        click.echo(f'pkgsize version {version}')
    except importlib.metadata.PackageNotFoundError:
        click.echo('pkgsize version: unknown (package not found or not installed correctly)')
    ctx.exit()

@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True, help="Show the version and exit.")
@click.option('--no-color', is_flag=True, help="Disable colored output.")
@click.pass_context
def main(ctx, no_color):
    """
    PkgSize: A tool to analyze the disk usage of installed Python packages.
    """
    if no_color:
        ctx.color = False
    pass

@main.command()
@click.option('--sort-by', default='size', type=click.Choice(['name', 'size', 'location'], case_sensitive=False), help='Sort packages by name, size, or location.')
@click.option('--top', default=None, type=int, help='Show only the top N packages by size.')
@click.option('--threshold', default=None, type=str, help='Only show packages larger than this size (e.g., 10MB, 500KB, 1GB).')
@click.option('--json', 'output_format_json', is_flag=True, help='Output the report in JSON format.')
@click.option('--csv', 'output_format_csv', is_flag=True, help='Output the report in CSV format.')
@click.option('--md', 'output_format_md', is_flag=True, help='Output the report in Markdown format.')
@click.option('--quiet', '-q', is_flag=True, help='Suppress informational output. Export output is still shown if an export format is selected.')
@click.option('--name', 'name_filter', type=str, default=None, help='Filter packages by name (case-insensitive, supports glob patterns like *name*).')
@click.option('--output', 'output_path', type=click.Path(file_okay=False, dir_okay=True, writable=True, resolve_path=True, allow_dash=False), default=None, help='Directory to save export files. Defaults to current working directory if not specified and an export format is chosen.')
@click.option('--include-deps', is_flag=True, help='Include sizes of dependencies recursively.')
@click.option('--path', 'venv_path_str', type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True, resolve_path=True), default=None, help='Path to a Python virtual environment to analyze. If not provided, analyzes the current environment.')
@click.pass_context
def analyze(ctx, sort_by, top, threshold, output_format_json, output_format_csv, output_format_md, quiet, name_filter, output_path, include_deps, venv_path_str):
    """
    Analyzes and lists installed Python packages and their disk usage.
    Can output in JSON, CSV, or Markdown format.
    """
    raw_packages_data_from_venv = None
    target_env_description = "current environment"

    if venv_path_str:
        if not is_valid_venv(venv_path_str):
            click.echo(f"Error: The path '{venv_path_str}' is not a valid Python virtual environment or is not accessible.", err=True)
            ctx.exit(1)
        
        target_env_description = venv_path_str
        venv_path = Path(venv_path_str)
        inspector_script_path = Path(__file__).parent / '_venv_inspector.py'

        if os.name == 'nt':
            python_exe_in_venv = venv_path / 'Scripts' / 'python.exe'
        else:
            python_exe_in_venv = venv_path / 'bin' / 'python'

        if not python_exe_in_venv.is_file():
            click.echo(f"Error: Python interpreter not found in '{venv_path_str}'.", err=True)
            ctx.exit(1)
        if not inspector_script_path.is_file():
            click.echo(f"Error: Internal helper script _venv_inspector.py not found at {inspector_script_path}.", err=True)
            ctx.exit(1)

        if not quiet:
            click.echo(f"Inspecting packages in virtual environment: {venv_path_str}...")
        try:
            cmd = [str(python_exe_in_venv), str(inspector_script_path)]
            process_result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
            raw_packages_data_from_venv = json.loads(process_result.stdout)
            if not quiet:
                click.echo(f"Successfully retrieved package data from {venv_path_str}.")
        except subprocess.CalledProcessError as e:
            click.echo(f"Error running inspector script in '{venv_path_str}': {e}", err=True)
            click.echo(f"Stderr: {e.stderr}", err=True)
            ctx.exit(1)
        except json.JSONDecodeError as e:
            click.echo(f"Error parsing package data from '{venv_path_str}': {e}", err=True)
            click.echo(f"Raw output: {process_result.stdout[:500]}...", err=True)
            ctx.exit(1)
        except Exception as e:
            click.echo(f"An unexpected error occurred while inspecting '{venv_path_str}': {e}", err=True)
            ctx.exit(1)
    else:
        if not quiet:
            click.echo("Analyzing packages in the current environment...")

    packages_data = get_installed_packages_info(
        include_deps=include_deps, 
        external_package_data=raw_packages_data_from_venv,
        target_env_description=target_env_description
    )

    if not packages_data:
        if not (output_format_json or output_format_csv or output_format_md):
            if not quiet:
                click.echo("No packages found or error retrieving package information.")
            return

    # Parse threshold
    min_size_bytes = None
    if threshold:
        min_size_bytes = parse_size_to_bytes(threshold)
        if min_size_bytes is None:
            return

    if min_size_bytes is not None:
        packages_data = [p for p in packages_data if p['size_bytes'] >= min_size_bytes]
        if not packages_data and not (output_format_json or output_format_csv or output_format_md) and not quiet:
            click.echo(f"No packages found larger than {threshold}.")

    if name_filter:
        packages_data = [p for p in packages_data if fnmatch.fnmatch(p['name'].lower(), name_filter.lower())]
        if not packages_data and not (output_format_json or output_format_csv or output_format_md) and not quiet:
            click.echo(f"No packages found matching name pattern '{name_filter}'.")
            
    if sort_by == 'name':
        packages_data.sort(key=lambda p: p['name'].lower())
    elif sort_by == 'location':
        packages_data.sort(key=lambda p: (p['location'] == "N/A" or "Error" in p['location'], p['location'].lower()))
    else: 
        packages_data.sort(key=lambda p: p['size_bytes'], reverse=True)
    
    if top is not None and top > 0:
        packages_data = packages_data[:top]
        if not packages_data and not (output_format_json or output_format_csv or output_format_md) and not quiet:
            click.echo(f"No packages match the criteria to display top {top}.")

    export_packages = []
    for pkg in packages_data:
        pkg_export_entry = {
            "name": pkg["name"],
            "version": pkg["version"],
            "size_bytes": pkg["size_bytes"],
            "size_human": format_size(pkg["size_bytes"]),
            "location": pkg["location"]
        }
        if include_deps and "dependencies_breakdown" in pkg:
            detailed_deps = []
            for dep_detail in pkg["dependencies_breakdown"]:
                detailed_deps.append({
                    **dep_detail,
                    "size_human": format_size(dep_detail["size_bytes"])
                })
            pkg_export_entry["dependencies_breakdown"] = detailed_deps
        export_packages.append(pkg_export_entry)
    
    if output_format_json or output_format_csv or output_format_md:
        base_dir = Path(output_path) if output_path else Path(os.getcwd())
        try:
            base_dir.mkdir(parents=True, exist_ok=True)
            
            if output_format_json:
                file_path = base_dir / "pkgsize_report.json"
                with open(file_path, 'w') as f:
                    json.dump(export_packages, f, indent=2)
                if not quiet:
                    click.echo(f"Report saved to {file_path}")
            elif output_format_csv:
                file_path = base_dir / "pkgsize_report.csv"
                with open(file_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Package Name", "Version", "Size (Bytes)", "Size (Human)", "Location"])
                    for pkg in export_packages:
                        writer.writerow([pkg['name'], pkg['version'], pkg['size_bytes'], pkg['size_human'], pkg['location']])
                if not quiet:
                    click.echo(f"Report saved to {file_path}")
            elif output_format_md:
                file_path = base_dir / "pkgsize_report.md"
                with open(file_path, 'w') as f:
                    f.write("| Package Name | Version | Size (Bytes) | Size (Human) | Location |\n")
                    f.write("|---|---|---|---|---|\n")
                    for pkg in export_packages:
                        f.write(f"| {pkg['name']} | {pkg['version']} | {pkg['size_bytes']} | {pkg['size_human']} | {pkg['location']} |\n")
                if not quiet:
                    click.echo(f"Report saved to {file_path}")
        except IOError as e:
            click.echo(f"Error: Could not write to directory {base_dir}. {e}", err=True)
        return
    else:
        if not quiet:
            if not packages_data:
                click.echo("No packages match the specified criteria.")
            else:
                header_name_width = 40 if include_deps else 30
                header_line = f"{'Package Name':<{header_name_width}} | {'Version':<15} | {'Size':<12} | {'Location'}"
                click.echo(header_line)
                click.echo("-" * (header_name_width + 15 + 12 + len('Location') + 9))

                for pkg in packages_data:
                    name = pkg.get('name', 'N/A')
                    version = pkg.get('version', 'N/A')
                    size_str = format_size(pkg.get('size_bytes', 0))
                    location = pkg.get('location', 'N/A')
                    click.echo(f"{name:<{header_name_width}} | {version:<15} | {size_str:<12} | {location}")

                    if include_deps and "dependencies_breakdown" in pkg and pkg["dependencies_breakdown"]:
                        click.echo(f"  {'|- Dependencies:':<{header_name_width-2}}")
                        for i, dep in enumerate(pkg["dependencies_breakdown"]):
                            is_last = i == len(pkg["dependencies_breakdown"]) - 1
                            prefix = "  |- " if not is_last else "  \- "
                            dep_name = dep.get('name', 'N/A')
                            dep_version = dep.get('version', 'N/A')
                            dep_size_str = format_size(dep.get('size_bytes', 0))
                            dep_location_str = dep.get('location', 'N/A')
                            if len(dep_location_str) > 30:
                                dep_location_str = dep_location_str[:27] + "..."
                            click.echo(f"  {prefix}{dep_name:<{header_name_width-len(prefix)-2}} | {dep_version:<15} | {dep_size_str:<12} | {dep_location_str}")

if __name__ == '__main__':
    main()
