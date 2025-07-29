"""Test the generator module."""

import pathlib
from typing import List, Optional
from colight_site.generator import MarkdownGenerator
from colight_site.parser import Form
import libcst as cst

# Get paths
test_dir = pathlib.Path(__file__).parent
examples_dir = test_dir / "examples"
project_root = test_dir.parent.parent.parent  # Go up 3 levels to project root
artifacts_dir = project_root / "test-artifacts" / "colight-site-hide"

# Create test-artifacts directory
artifacts_dir.mkdir(parents=True, exist_ok=True)


def test_markdown_generation():
    """Test basic markdown generation."""
    output_dir = artifacts_dir
    generator = MarkdownGenerator(output_dir)

    # Create mock forms
    import_stmt = cst.parse_statement("import numpy as np")
    expr_stmt = cst.parse_statement("np.sin(x)")

    forms = [
        Form(markdown=["This is a test"], node=import_stmt, start_line=1),
        Form(markdown=["Create visualization"], node=expr_stmt, start_line=3),
    ]

    colight_files = [None, pathlib.Path("test.colight")]

    markdown = generator.generate_markdown(forms, colight_files, "Test Document")

    assert "# Test Document" in markdown
    assert "This is a test" in markdown
    assert "Create visualization" in markdown
    assert "```python" in markdown
    assert "import numpy as np" in markdown
    assert "np.sin(x)" in markdown
    assert "data-src=" in markdown and 'test.colight"' in markdown


def test_html_generation():
    """Test HTML generation."""
    output_dir = artifacts_dir
    generator = MarkdownGenerator(output_dir)

    # Create mock forms
    import_stmt = cst.parse_statement("import numpy as np")
    expr_stmt = cst.parse_statement("np.sin(x)")

    forms = [
        Form(markdown=["This is a test"], node=import_stmt, start_line=1),
        Form(markdown=["Create visualization"], node=expr_stmt, start_line=3),
    ]

    colight_files = [None, pathlib.Path("test.colight")]

    html = generator.generate_html(forms, colight_files, "Test Document")

    assert "<!DOCTYPE html>" in html
    assert "<title>Test Document</title>" in html
    assert "colight-embed" in html
    assert "embed.js" in html
    assert "<h1>Test Document</h1>" in html
    assert "<p>This is a test</p>" in html


def test_hide_statements_flag():
    """Test the hide_statements flag."""
    output_dir = artifacts_dir
    generator = MarkdownGenerator(output_dir)

    # Create forms with both statements and expressions
    import_stmt = cst.parse_statement("import numpy as np")
    assign_stmt = cst.parse_statement("x = np.linspace(0, 10, 100)")
    expr_stmt = cst.parse_statement("np.sin(x)")

    forms = [
        Form(markdown=["Import libraries"], node=import_stmt, start_line=1),
        Form(markdown=["Create data"], node=assign_stmt, start_line=2),
        Form(markdown=["Visualize"], node=expr_stmt, start_line=3),
    ]

    colight_files = [None, None, pathlib.Path("test.colight")]

    # Generate without hiding statements
    markdown = generator.generate_markdown(forms, colight_files)
    assert "import numpy as np" in markdown
    assert "x = np.linspace(0, 10, 100)" in markdown
    assert "np.sin(x)" in markdown

    # Generate with hide_statements=True
    markdown_hidden = generator.generate_markdown(
        forms, colight_files, hide_statements=True
    )
    assert "import numpy as np" not in markdown_hidden  # statement
    assert "x = np.linspace(0, 10, 100)" not in markdown_hidden  # statement
    assert "np.sin(x)" in markdown_hidden  # expression

    # Importantly, markdown content should still be present
    assert "Import libraries" in markdown_hidden
    assert "Create data" in markdown_hidden
    assert "Visualize" in markdown_hidden


def test_hide_code_flag():
    """Test the hide_code flag."""
    output_dir = artifacts_dir
    generator = MarkdownGenerator(output_dir)

    # Create forms
    import_stmt = cst.parse_statement("import numpy as np")
    expr_stmt = cst.parse_statement("np.sin(x)")

    forms = [
        Form(markdown=["Import libraries"], node=import_stmt, start_line=1),
        Form(markdown=["Visualize"], node=expr_stmt, start_line=2),
    ]

    colight_files = [None, pathlib.Path("test.colight")]

    # Generate without hiding code
    markdown = generator.generate_markdown(forms, colight_files)
    assert "```python" in markdown
    assert "import numpy as np" in markdown
    assert "np.sin(x)" in markdown

    # Generate with hide_code=True
    markdown_hidden = generator.generate_markdown(forms, colight_files, hide_code=True)
    assert "```python" not in markdown_hidden
    assert "import numpy as np" not in markdown_hidden
    assert "np.sin(x)" not in markdown_hidden
    # But markdown content should still be there
    assert "Import libraries" in markdown_hidden
    assert "Visualize" in markdown_hidden
    # And visualizations should still be there
    assert "colight-embed" in markdown_hidden


def test_hide_visuals_flag():
    """Test the hide_visuals flag."""
    output_dir = artifacts_dir
    generator = MarkdownGenerator(output_dir)

    # Create forms
    expr_stmt = cst.parse_statement("np.sin(x)")

    forms = [
        Form(markdown=["Visualize"], node=expr_stmt, start_line=1),
    ]

    colight_files: List[Optional[pathlib.Path]] = [pathlib.Path("test.colight")]

    # Generate without hiding visuals
    markdown = generator.generate_markdown(forms, colight_files)
    assert "colight-embed" in markdown
    assert "data-src=" in markdown and "test.colight" in markdown

    # Generate with hide_visuals=True
    markdown_hidden = generator.generate_markdown(
        forms, colight_files, hide_visuals=True
    )
    assert "colight-embed" not in markdown_hidden
    assert "data-src=" not in markdown_hidden
    # But code and markdown should still be there
    assert "Visualize" in markdown_hidden
    assert "np.sin(x)" in markdown_hidden
