import os
from bs4 import BeautifulSoup

def xml_to_markdown(xml_file_path, output_dir):
    """
    Converts a GROBID TEI XML file to a structured Markdown file
    with YAML front matter for use in a vector database.

    Args:
        xml_file_path (str): The full path to the input XML file.
        output_dir (str): The directory where the Markdown file will be saved.
    """
    try:
        with open(xml_file_path, 'r', encoding='utf-8') as f:
            # Use the 'lxml-xml' parser for proper XML handling
            soup = BeautifulSoup(f, 'lxml-xml')

        # --- Pre-process to remove unwanted sections ---
        unwanted_section_headings = [
            "references",
            "bibliography",
            "credit authorship contribution statement",
            "declaration of competing interest"
        ]
        for div in soup.find_all('div'):
            head = div.find('head')
            if head and head.get_text(strip=True).lower() in unwanted_section_headings:
                div.decompose()

        # --- 1. Extract Metadata for YAML Front Matter ---

        # Title
        title_tag = soup.find('titleStmt').find('title')
        title = title_tag.get_text(strip=True) if title_tag else "No Title Found"
        title = title.replace('"', '\\"')

        # Authors and DOI are often in the <front> section
        authors = []
        doi = ""
        front_section = soup.find('front')
        if front_section:
            analytic_div = front_section.find('div', type='analytic')
            if analytic_div:
                # Authors
                for author in analytic_div.find_all('author'):
                    pers_name = author.find('persName')
                    if pers_name:
                        forenames = " ".join([fn.get_text(strip=True) for fn in pers_name.find_all('forename')])
                        surname = pers_name.find('surname').get_text(strip=True) if pers_name.find('surname') else ""
                        authors.append(f"{forenames} {surname}".strip())

                # DOI (Digital Object Identifier)
                doi_tag = analytic_div.find('idno', type='DOI')
                if doi_tag:
                    doi = doi_tag.get_text(strip=True)

        # Abstract
        abstract_tag = soup.find('abstract')
        abstract_text = "\n".join([p.get_text(strip=True) for p in abstract_tag.find_all('p')]) if abstract_tag else ""


        # --- 2. Create YAML Front Matter ---

        yaml_front_matter = "---\n"
        yaml_front_matter += f'title: "{title}"\n'
        yaml_front_matter += "authors:\n"
        for author in authors:
            yaml_front_matter += f'  - "{author}"\n'
        yaml_front_matter += f'doi: "{doi}"\n'
        yaml_front_matter += "---\n\n"

        # --- 3. Process the Body Content ---

        markdown_body = []

        if abstract_text:
            markdown_body.append("## Abstract")
            markdown_body.append(abstract_text)

        body_tag = soup.find('body')
        if body_tag:
            for section in body_tag.find_all('div', recursive=False):
                heading_tag = section.find('head')
                if heading_tag:
                    heading_text = heading_tag.get_text(strip=True)

                    heading_level = len(heading_tag.get('n', '').split('.')) + 1
                    heading_prefix = '#' * heading_level
                    markdown_body.append(f"\n{heading_prefix} {heading_text}")

                    paragraphs = section.find_all('p', recursive=False)
                    for p in paragraphs:
                        markdown_body.append(p.get_text(strip=True))

        # --- 4. Assemble and Save the Markdown File ---

        final_markdown = yaml_front_matter + "\n\n".join(markdown_body)

        os.makedirs(output_dir, exist_ok=True)

        # --- MODIFIED: Clean up the output filename ---
        base_name = os.path.basename(xml_file_path)
        # Remove the '.grobid.tei' part from the string
        clean_base_name = base_name.replace('.grobid.tei', '')
        # Now get the name without the final extension (e.g., .xml)
        file_name_without_ext = os.path.splitext(clean_base_name)[0]
        output_path = os.path.join(output_dir, f"{file_name_without_ext}.md")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_markdown)

        print(f"Successfully converted '{xml_file_path}' to '{output_path}'")

    except Exception as e:
        print(f"Error processing '{xml_file_path}': {e}")


# --- Example Usage ---
if __name__ == '__main__':
    # Your input and output directories
    input_dir = r"C:\Users\td00654\OneDrive - University of Surrey\Documents\EDRC LLM Project\Papers\EDRC - XML"
    output_dir = r'C:\Users\td00654\OneDrive - University of Surrey\Documents\EDRC LLM Project\Papers\EDRC - Text'

    # The script now looks for files ending in '.xml' as before,
    # but the output name will be cleaner.
    for filename in os.listdir(input_dir):
        if filename.endswith('.xml'):
            xml_to_markdown(os.path.join(input_dir, filename), output_dir)
