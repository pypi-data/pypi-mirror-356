from pathlib import Path
from textwrap import dedent

import pytest

from decatenator._core import extract_files, write_files


SAMPLE = (
    dedent(
        """
    ### a.py
    ```python
    print("A")
    ```

    ### dir/b.txt
    ```
    hello
    ```
    """
    )
    .lstrip()
    .splitlines(keepends=True)
)

SAMPLE_TWO_HASH = (
    dedent(
        """
    ## main.py
    ```python
    def main():
        pass
    ```

    ## config.json
    ```json
    {"key": "value"}
    ```
    """
    )
    .lstrip()
    .splitlines(keepends=True)
)

SAMPLE_NO_FENCES = (
    dedent(
        """
    ## script.py
    print("Hello World")
    x = 42

    ## data.txt
    line1
    line2
    line3
    """
    )
    .lstrip()
    .splitlines(keepends=True)
)

SAMPLE_MIXED = (
    dedent(
        """
    ## fenced.py
    ```python
    print("fenced")
    ```

    ## unfenced.py
    print("unfenced")
    x = 1

    ## another.txt
    ```
    some text
    ```
    """
    )
    .lstrip()
    .splitlines(keepends=True)
)


def test_extract_files_simple():
    files = list(extract_files(SAMPLE))
    assert files == [
        ("a.py", 'print("A")\n'),
        ("dir/b.txt", "hello\n"),
    ]


def test_write_files(tmp_path: Path):
    write_files(extract_files(SAMPLE), tmp_path)
    assert (tmp_path / "a.py").read_text() == 'print("A")\n'
    assert (tmp_path / "dir" / "b.txt").read_text() == "hello\n"


def test_two_hash_headings():
    files = list(extract_files(SAMPLE_TWO_HASH))
    assert files == [
        ("main.py", "def main():\n    pass\n"),
        ("config.json", '{"key": "value"}\n'),
    ]


def test_no_fences():
    files = list(extract_files(SAMPLE_NO_FENCES))
    assert files == [
        ("script.py", 'print("Hello World")\nx = 42\n\n'),
        ("data.txt", "line1\nline2\nline3\n"),
    ]


def test_mixed_fenced_and_unfenced():
    files = list(extract_files(SAMPLE_MIXED))
    assert files == [
        ("fenced.py", 'print("fenced")\n'),
        ("unfenced.py", 'print("unfenced")\nx = 1\n\n'),
        ("another.txt", "some text\n"),
    ]


def test_python_comments_ignored():
    # Test that Python comments with multiple words are not treated as headings
    sample_with_comments = [
        "## valid_file.py\n",
        "# This is a comment\n",
        "## another comment with spaces\n",
        "print('code')\n",
        "### multiple words here\n",
        "more code\n",
        "## single_word\n",
        "final content\n",
    ]
    files = list(extract_files(sample_with_comments))
    assert files == [
        (
            "valid_file.py",
            (
                "# This is a comment\n"
                "## another comment with spaces\n"
                "print('code')\n"
                "### multiple words here\n"
                "more code\n"
            ),
        ),
        ("single_word", "final content\n"),
    ]


def test_confusing_comments():
    """Test with comments that look like headings but have multiple words."""
    sample_with_confusing = (
        dedent(
            """
        ## real_file.py
        # This is a normal comment
        ## This is also a comment with spaces
        ### Another comment that looks like heading
        #### Even more hashes with text
        print("actual code")

        # ## This comment starts with hash-space-hash-space
        # ### More confusing patterns

        ## actual_file2.py
        ```python
        # ## Comments inside code blocks
        # ### Should not be treated as headings
        def func():
            pass
        ```

        ## file3.txt
        Some content here
        ## Not a heading because it's content
        ### Also not a heading
        More content
        """
        )
        .lstrip()
        .splitlines(keepends=True)
    )

    files = list(extract_files(sample_with_confusing))
    assert len(files) == 3
    assert files[0][0] == "real_file.py"
    assert "# This is a normal comment" in files[0][1]
    assert "## This is also a comment with spaces" in files[0][1]
    assert 'print("actual code")' in files[0][1]

    assert files[1][0] == "actual_file2.py"
    assert "# ## Comments inside code blocks" in files[1][1]
    assert "def func():" in files[1][1]

    assert files[2][0] == "file3.txt"
    assert "Some content here" in files[2][1]
    assert "## Not a heading because it's content" in files[2][1]


def test_html_comments_and_markdown():
    """Test with HTML comments and other markdown that might confuse parser."""
    sample_html = (
        dedent(
            """
        ## style.css
        /* ## This is a CSS comment that looks like heading */
        /* ### Another CSS comment */
        body { margin: 0; }

        ## script.js
        ```javascript
        // ## JavaScript comment that looks like heading
        // ### More JS comments
        console.log("hello");
        ```

        ## readme_fragment.md
        <!-- ## HTML comment that looks like heading -->
        <!-- ### More HTML comments -->

        This is regular markdown content.

        ## Not a real heading because multiple words
        ### Also not real because multiple words

        Real content continues here.
        """
        )
        .lstrip()
        .splitlines(keepends=True)
    )

    files = list(extract_files(sample_html))
    assert len(files) == 3

    # CSS file should contain the CSS comments
    css_content = files[0][1]
    assert "/* ## This is a CSS comment" in css_content
    assert "body { margin: 0; }" in css_content

    # JS file should contain JS comments
    js_content = files[1][1]
    assert "// ## JavaScript comment" in js_content
    assert 'console.log("hello");' in js_content

    # Markdown fragment should contain HTML comments and content
    md_content = files[2][1]
    assert "<!-- ## HTML comment" in md_content
    assert "This is regular markdown content." in md_content
    assert "## Not a real heading because multiple words" in md_content


def test_edge_cases_whitespace_and_formatting():
    """Test edge cases with whitespace, tabs, and formatting."""
    sample_edge = (
        dedent(
            """
        ##	tab_separated.py
        ```python
        print("tab after hashes")
        ```

        ## trailing_space.txt
        Content with trailing space in heading

        ##   multiple_spaces.py
        Content with multiple spaces

        ## $pecial-chars_123.py
        Special characters in filename

        ## file.name.with.dots
        ```
        Content for dotted filename
        ```

        ##
        Empty heading should be ignored

        ##nospace
        This should be ignored (no space after hashes)

        ##123invalid
        This should also be ignored (no space after hashes)

        ## multiple words here
        This should be ignored (multiple words)
        """
        )
        .lstrip()
        .splitlines(keepends=True)
    )

    files = list(extract_files(sample_edge))

    # Should extract valid files
    file_names = [f[0] for f in files]
    assert "tab_separated.py" in file_names
    assert "trailing_space.txt" in file_names
    assert "multiple_spaces.py" in file_names
    assert "$pecial-chars_123.py" in file_names
    assert "file.name.with.dots" in file_names

    # Should not extract invalid ones
    assert "" not in file_names  # Empty heading
    assert "nospace" not in file_names  # No space after hashes
    assert "123invalid" not in file_names  # No space after hashes


def test_nested_markdown_structures():
    """Test with nested markdown structures that might confuse parser."""
    sample_nested = (
        dedent(
            """
        ## main.py
        ```python
        def generate_markdown():
            return '''
        ## This looks like a heading but it's inside a string
        ### Another fake heading in string
            '''
        ```

        ## config.yaml
        # YAML comment
        ## Also a YAML comment, not a heading
        key: |
          ## Multi-line string that contains
          ### What looks like headings
          But are actually content

        ## test_data.txt
        Here's some test data:

        ## Section 1 - not a real heading
        ### Subsection - also not real

        Some actual content here.
        """
        )
        .lstrip()
        .splitlines(keepends=True)
    )

    files = list(extract_files(sample_nested))
    assert len(files) == 3

    # Python file should contain the triple-quoted string with fake headings
    py_content = files[0][1]
    assert "## This looks like a heading but it's inside a string" in py_content
    assert "### Another fake heading in string" in py_content

    # YAML file should contain comments that look like headings
    yaml_content = files[1][1]
    assert "## Also a YAML comment, not a heading" in yaml_content
    assert "## Multi-line string that contains" in yaml_content

    # Text file should contain fake headings as content
    txt_content = files[2][1]
    assert "## Section 1 - not a real heading" in txt_content
    assert "### Subsection - also not real" in txt_content


def test_error_on_missing_fence():
    bad = ["### foo.py\n", "```python\n", "code here\n"]  # Missing closing fence
    with pytest.raises(SyntaxError):
        list(extract_files(bad))
