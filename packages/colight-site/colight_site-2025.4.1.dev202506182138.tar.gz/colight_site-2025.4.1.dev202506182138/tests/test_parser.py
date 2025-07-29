"""Test the parser module."""

import pathlib
import tempfile
from colight_site.parser import (
    parse_colight_file,
    is_colight_file,
    parse_file_metadata,
    FileMetadata,
)


def test_is_colight_file():
    """Test colight file detection."""
    assert is_colight_file(pathlib.Path("example.colight.py"))
    assert is_colight_file(pathlib.Path("test.colight.py"))
    assert not is_colight_file(pathlib.Path("regular.py"))
    assert not is_colight_file(pathlib.Path("test.txt"))


def test_parse_simple_colight_file():
    """Test parsing a simple colight file."""
    content = """# This is a title
# Some description

import numpy as np

# Create data
x = np.linspace(0, 10, 100)

# This creates a visualization
np.sin(x)
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".colight.py", delete=False) as f:
        f.write(content)
        f.flush()

        forms, metadata = parse_colight_file(pathlib.Path(f.name))

        # Should have 5 forms (improved separation of markdown and code)
        assert len(forms) == 5

        # First form: import (should have the title comments)
        assert "import numpy as np" in forms[0].code
        assert len(forms[0].markdown) > 0
        assert "This is a title" in forms[0].markdown[0]

        # Second form: dummy markdown form for "Create data"
        assert "Create data" in forms[1].markdown[0]
        assert forms[1].code.strip() == "pass"

        # Third form: assignment
        assert "x = np.linspace" in forms[2].code
        assert len(forms[2].markdown) == 0

        # Fourth form: dummy markdown form for "This creates a visualization"
        assert "This creates a visualization" in forms[3].markdown[0]
        assert forms[3].code.strip() == "pass"

        # Fifth form: expression
        assert "np.sin(x)" in forms[4].code
        assert forms[4].is_expression

        # Clean up
        pathlib.Path(f.name).unlink()


def test_parse_empty_file():
    """Test parsing an empty file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".colight.py", delete=False) as f:
        f.write("")
        f.flush()

        forms, metadata = parse_colight_file(pathlib.Path(f.name))
        assert len(forms) == 0


def test_consecutive_code_grouping():
    """Test that consecutive code statements are grouped into single forms."""
    content = """# Title
# Description

import numpy as np

# Some comment
x = np.linspace(0, 10, 100)
y = np.sin(x)
z = np.cos(x)

# Another comment
result = x, y, z
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".colight.py", delete=False) as f:
        f.write(content)
        f.flush()

        forms, metadata = parse_colight_file(pathlib.Path(f.name))

        # Should have 6 forms total (improved separation of markdown and code)
        assert len(forms) == 6

        # Form 0: import with title markdown
        assert "Title" in forms[0].markdown[0]
        assert "import numpy as np" in forms[0].code

        # Form 1: dummy markdown form for "Some comment"
        assert "Some comment" in forms[1].markdown[0]
        assert forms[1].code.strip() == "pass"

        # Form 2: first assignment
        assert "x = np.linspace" in forms[2].code
        assert len(forms[2].markdown) == 0

        # Form 3: grouped assignments (consecutive code)
        assert "y = np.sin" in forms[3].code
        assert "z = np.cos" in forms[3].code
        assert len(forms[3].markdown) == 0

        # Form 4: dummy markdown form for "Another comment"
        assert "Another comment" in forms[4].markdown[0]
        assert forms[4].code.strip() == "pass"

        # Form 5: final assignment
        assert "result = x, y, z" in forms[5].code
        assert len(forms[5].markdown) == 0

        pathlib.Path(f.name).unlink()


def test_parse_file_metadata_basic():
    """Test parsing basic file metadata."""
    source = """#| colight: hide-statements
#| colight: format-html

import numpy as np
"""
    metadata = parse_file_metadata(source)
    assert metadata.hide_statements is True
    assert metadata.hide_visuals is False
    assert metadata.hide_code is False
    assert metadata.format == "html"


def test_parse_file_metadata_multiple_options():
    """Test parsing multiple options in one line."""
    source = """#| colight: hide-statements, hide-visuals, format-markdown

import numpy as np
"""
    metadata = parse_file_metadata(source)
    assert metadata.hide_statements is True
    assert metadata.hide_visuals is True
    assert metadata.hide_code is False
    assert metadata.format == "markdown"


def test_parse_file_metadata_mostly_prose():
    """Test the mostly-prose shorthand."""
    source = """#| colight: mostly-prose

import numpy as np
"""
    metadata = parse_file_metadata(source)
    assert metadata.hide_statements is True
    assert metadata.hide_visuals is False
    assert metadata.hide_code is True
    assert metadata.format is None


def test_parse_file_metadata_no_pragmas():
    """Test parsing a file without any pragmas."""
    source = """# This is just a regular comment
import numpy as np
"""
    metadata = parse_file_metadata(source)
    assert metadata.hide_statements is False
    assert metadata.hide_visuals is False
    assert metadata.hide_code is False
    assert metadata.format is None


def test_parse_file_metadata_unknown_options():
    """Test that unknown options are silently ignored."""
    source = """#| colight: hide-statements, unknown-option, format-html

import numpy as np
"""
    metadata = parse_file_metadata(source)
    assert metadata.hide_statements is True
    assert metadata.format == "html"


def test_file_metadata_merge_with_cli():
    """Test merging file metadata with CLI options."""
    metadata = FileMetadata(hide_statements=True, format="html")

    # CLI options should override file metadata
    result = metadata.merge_with_cli_options(hide_visuals=True, format="markdown")

    assert result["hide_statements"] is True  # from file
    assert result["hide_visuals"] is True  # from CLI
    assert result["hide_code"] is False  # default
    assert result["format"] == "markdown"  # CLI override


def test_file_metadata_mostly_prose_cli():
    """Test that CLI mostly-prose flag works correctly."""
    metadata = FileMetadata(hide_visuals=True)

    result = metadata.merge_with_cli_options(mostly_prose=True)

    assert result["hide_statements"] is True  # from mostly_prose
    assert result["hide_code"] is True  # from mostly_prose
    assert result["hide_visuals"] is True  # preserved from file


def test_parse_colight_file_with_metadata():
    """Test parsing a colight file with metadata."""
    content = """#| colight: hide-statements, format-html
# This is a title
# Some description

import numpy as np

# Create data
x = np.linspace(0, 10, 100)
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".colight.py", delete=False) as f:
        f.write(content)
        f.flush()

        forms, metadata = parse_colight_file(pathlib.Path(f.name))

        # Check that metadata was parsed correctly
        assert metadata.hide_statements is True
        assert metadata.format == "html"

        # Check that forms were still parsed correctly
        assert len(forms) >= 1
        assert "import numpy as np" in forms[0].code

        pathlib.Path(f.name).unlink()


def test_pragma_comments_filtered():
    """Test that pragma comments are not included in markdown output."""
    content = """#| colight: hide-statements
# This is a regular comment
# This should appear in output

import numpy as np

#| colight: format-html
# Another regular comment
x = np.linspace(0, 10, 100)
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".colight.py", delete=False) as f:
        f.write(content)
        f.flush()

        forms, metadata = parse_colight_file(pathlib.Path(f.name))

        # Check that metadata was parsed correctly
        assert metadata.hide_statements is True
        assert metadata.format == "html"

        # Check that pragma comments are not in any form's markdown
        all_markdown = []
        for form in forms:
            all_markdown.extend(form.markdown)

        # Regular comments should be present
        assert any("This is a regular comment" in line for line in all_markdown)
        assert any("Another regular comment" in line for line in all_markdown)

        # Pragma comments should NOT be present
        assert not any("colight:" in line for line in all_markdown)
        assert not any("hide-statements" in line for line in all_markdown)
        assert not any("format-html" in line for line in all_markdown)

        pathlib.Path(f.name).unlink()
