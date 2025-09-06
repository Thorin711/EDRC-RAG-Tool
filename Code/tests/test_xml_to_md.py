import os
import tempfile
import pytest
import sys
# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from xml_to_md import xml_to_markdown

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test outputs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

def test_xml_to_markdown_conversion(temp_dir):
    """
    Tests the complete conversion of a sample GROBID TEI XML file to Markdown.
    """
    # --- Arrange ---
    # Path to the sample XML file
    xml_file_path = os.path.join(os.path.dirname(__file__), 'test_data', 'sample_grobid_tei.xml')
    output_dir = temp_dir

    # Expected output file path
    expected_md_filename = "sample_grobid_tei.md"
    expected_md_filepath = os.path.join(output_dir, expected_md_filename)

    # --- Act ---
    # Run the conversion function
    xml_to_markdown(xml_file_path, output_dir)

    # --- Assert ---
    # 1. Check if the output file was created
    assert os.path.exists(expected_md_filepath), "Markdown file was not created."

    # 2. Read the content of the generated Markdown file
    with open(expected_md_filepath, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 3. Verify the YAML front matter
    expected_yaml = """\
---
title: "This is a Test Title"
authors:
  - "John Doe"
  - "Jane Smith"
doi: "10.1234/test.doi"
---
"""
    assert md_content.startswith(expected_yaml), "YAML front matter is incorrect."

    # 4. Verify the Markdown body
    assert "## Abstract" in md_content, "Abstract heading is missing."
    assert "This is the abstract of the test paper." in md_content, "Abstract content is missing."
    assert "## Introduction" in md_content, "Introduction heading is missing."
    assert "This is the first paragraph of the introduction." in md_content, "First intro paragraph is missing."
    assert "## Methods" in md_content, "Methods heading is correct."
    assert "This is the first paragraph of the methods section." in md_content, "Methods paragraph is missing."

    # 5. Verify that the "References" section was removed
    assert "References" not in md_content, "The 'References' section was not removed."
    assert "This section should be removed." not in md_content, "Content of the 'References' section is still present."

def test_xml_to_markdown_no_doi(temp_dir):
    """
    Tests handling of an XML file with a missing DOI.
    """
    # --- Arrange ---
    # Create a dummy XML file without a DOI
    xml_content = """
    <TEI xmlns="http://www.tei-c.org/ns/1.0">
        <teiHeader>
            <fileDesc><titleStmt><title>No DOI Test</title></titleStmt></fileDesc>
            <profileDesc><abstract><p>Abstract content.</p></abstract></profileDesc>
        </teiHeader>
        <text>
            <front>
                <div type="analytic">
                    <author><persName><forename>Test</forename><surname>Author</surname></persName></author>
                </div>
            </front>
            <body><div><head>Body</head><p>Some text.</p></div></body>
        </text>
    </TEI>
    """
    xml_file_path = os.path.join(temp_dir, "no_doi.xml")
    with open(xml_file_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)

    output_dir = temp_dir
    expected_md_filepath = os.path.join(output_dir, "no_doi.md")

    # --- Act ---
    xml_to_markdown(xml_file_path, output_dir)

    # --- Assert ---
    assert os.path.exists(expected_md_filepath)
    with open(expected_md_filepath, 'r', encoding='utf-8') as f:
        md_content = f.read()

    assert 'doi: ""' in md_content, "DOI should be an empty string in the YAML front matter."

def test_xml_to_markdown_no_abstract(temp_dir):
    """
    Tests handling of an XML file with a missing abstract.
    """
    # --- Arrange ---
    xml_content = """
    <TEI xmlns="http://www.tei-c.org/ns/1.0">
        <teiHeader>
            <fileDesc><titleStmt><title>No Abstract Test</title></titleStmt></fileDesc>
        </teiHeader>
        <text>
            <body><div><head>Body</head><p>Some text.</p></div></body>
        </text>
    </TEI>
    """
    xml_file_path = os.path.join(temp_dir, "no_abstract.xml")
    with open(xml_file_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)

    output_dir = temp_dir
    expected_md_filepath = os.path.join(output_dir, "no_abstract.md")

    # --- Act ---
    xml_to_markdown(xml_file_path, output_dir)

    # --- Assert ---
    assert os.path.exists(expected_md_filepath)
    with open(expected_md_filepath, 'r', encoding='utf-8') as f:
        md_content = f.read()

    assert "## Abstract" not in md_content, "Abstract section should not be present if missing in the XML."
