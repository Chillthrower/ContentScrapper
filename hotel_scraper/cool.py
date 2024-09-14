from bs4 import BeautifulSoup

def read_html_file(file_path):
    """Read the content of an HTML file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def extract_body_content(html_content):
    """Extract the body content from HTML."""
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    """Remove script and style tags, and clean the body content."""
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    """Split the cleaned content into chunks of max_length."""
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]

def process_html_file(file_path, output_txt_path):
    """Process the HTML file to extract, clean, and split the body content, then save it to a text file."""
    html_content = read_html_file(file_path)
    body_content = extract_body_content(html_content)
    cleaned_content = clean_body_content(body_content)
    content_chunks = split_dom_content(cleaned_content)

    # Save the chunks to a text file
    with open(output_txt_path, "w", encoding="utf-8") as txt_file:
        for i, chunk in enumerate(content_chunks):
            txt_file.write(f"--- Chunk {i + 1} ---\n")
            txt_file.write(chunk)
            txt_file.write("\n\n")

# Example usage
if __name__ == "__main__":
    input_file_path = "page.html"  # Replace with your HTML file path
    output_file_path = "processed_content.md"  # Desired output text file path
    process_html_file(input_file_path, output_file_path)
    print(f"Processed content saved to {output_file_path}")
