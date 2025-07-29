"""Main builder module that coordinates parsing, execution, and generation."""

import pathlib

from .parser import parse_colight_file, is_colight_file
from .executor import SafeFormExecutor
from .generator import MarkdownGenerator


def _get_output_path(input_path: pathlib.Path, format: str) -> pathlib.Path:
    """Convert .colight.py input path to output path with correct extension."""
    if input_path.name.endswith(".colight.py"):
        # Remove .colight.py and add the new extension
        base_name = input_path.name[:-11]  # Remove ".colight.py"
        suffix = ".html" if format == "html" else ".md"
        return input_path.parent / (base_name + suffix)
    else:
        # Fallback for non-.colight.py files
        suffix = ".html" if format == "html" else ".md"
        return input_path.with_suffix(suffix)


def build_file(
    input_path: pathlib.Path,
    output_path: pathlib.Path,
    verbose: bool = False,
    format: str = "markdown",
    hide_statements: bool = False,
    hide_visuals: bool = False,
    hide_code: bool = False,
):
    """Build a single .colight.py file."""
    if not is_colight_file(input_path):
        raise ValueError(f"Not a .colight.py file: {input_path}")

    if verbose:
        print(f"Building {input_path} -> {output_path}")

    try:
        # Parse the file
        forms, file_metadata = parse_colight_file(input_path)
        if verbose:
            print(f"Found {len(forms)} forms")
            if any(
                [
                    file_metadata.hide_statements,
                    file_metadata.hide_visuals,
                    file_metadata.hide_code,
                    file_metadata.format,
                ]
            ):
                print(f"File metadata: {file_metadata}")
    except Exception as e:
        if verbose:
            print(f"Parse error: {e}")
        # Create a minimal output file with error message
        output_path.parent.mkdir(parents=True, exist_ok=True)
        error_content = f"# Parse Error\n\nCould not parse {input_path.name}: {e}\n"
        output_path.write_text(error_content)
        return

    # Setup execution environment
    colight_dir = output_path.parent / (output_path.stem + "_colight")
    executor = SafeFormExecutor(colight_dir)

    # Execute forms and collect visualizations
    colight_files = []
    for i, form in enumerate(forms):
        try:
            result = executor.execute_form(form, str(input_path))
            colight_file = executor.save_colight_visualization(result, i)
            colight_files.append(colight_file)

            if verbose and colight_file:
                print(f"  Form {i}: saved visualization to {colight_file.name}")
        except Exception as e:
            if verbose:
                print(f"  Form {i}: execution failed: {e}")
            colight_files.append(None)

    # Generate output
    generator = MarkdownGenerator(colight_dir)
    title = input_path.stem.replace(".colight", "").replace("_", " ").title()

    # Merge file metadata with CLI options (CLI takes precedence)
    merged_options = file_metadata.merge_with_cli_options(
        hide_statements=hide_statements,
        hide_visuals=hide_visuals,
        hide_code=hide_code,
        format=format,
    )

    # Extract the actual format to use
    final_format = merged_options.pop("format") or format

    if final_format == "html":
        html_content = generator.generate_html(
            forms, colight_files, title, output_path, **merged_options
        )
        generator.write_html_file(html_content, output_path)
    else:
        markdown_content = generator.generate_markdown(
            forms, colight_files, title, output_path, **merged_options
        )
        generator.write_markdown_file(markdown_content, output_path)

    if verbose:
        print(f"Generated {output_path}")


def build_directory(
    input_dir: pathlib.Path,
    output_dir: pathlib.Path,
    verbose: bool = False,
    format: str = "markdown",
    hide_statements: bool = False,
    hide_visuals: bool = False,
    hide_code: bool = False,
):
    """Build all .colight.py files in a directory."""
    if verbose:
        print(f"Building directory {input_dir} -> {output_dir}")

    # Find all .colight.py files
    colight_files = []
    for path in input_dir.rglob("*.py"):
        if is_colight_file(path):
            colight_files.append(path)

    if verbose:
        print(f"Found {len(colight_files)} .colight.py files")

    # Build each file
    for colight_file in colight_files:
        try:
            # Calculate relative output path
            rel_path = colight_file.relative_to(input_dir)
            output_file_rel = _get_output_path(rel_path, format)
            output_file = output_dir / output_file_rel

            build_file(
                colight_file,
                output_file,
                verbose=verbose,
                format=format,
                hide_statements=hide_statements,
                hide_visuals=hide_visuals,
                hide_code=hide_code,
            )
        except Exception as e:
            print(f"Error building {colight_file}: {e}")
            if verbose:
                import traceback

                traceback.print_exc()


def init_project(project_dir: pathlib.Path):
    """Initialize a new colight-site project."""
    project_dir.mkdir(parents=True, exist_ok=True)

    # Create directory structure
    (project_dir / "src").mkdir(exist_ok=True)
    (project_dir / "build").mkdir(exist_ok=True)

    # Create example .colight.py file
    example_file = project_dir / "src" / "example.colight.py"
    example_content = """# My First Colight Document
# This is a simple example of mixing narrative text with executable code.

import numpy as np

# Let's create some data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# This will create a visualization
x, y  # Return the data for visualization

# You can add more narrative here
# And more code blocks...

print("Hello from colight-site!")
"""

    example_file.write_text(example_content)

    # Create README
    readme_content = """# Colight Site Project

This project uses `colight-site` to generate static documentation with embedded visualizations.

## Usage

Build the site:
```bash
colight-site build src --output build
```

Watch for changes:
```bash
colight-site watch src --output build
```

## Files

- `src/` - Source .colight.py files
- `build/` - Generated markdown and HTML files
"""

    (project_dir / "README.md").write_text(readme_content)
