import os
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Encoding of the HTML files
html_encoding = "windows-1251"

directory_to_search = "."
search_index_output = "search_index.js"

class HTMLFileHandler(FileSystemEventHandler):
    def __init__(self, index_callback):
        self.index_callback = index_callback

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".html"):
            self.index_callback(event.src_path)

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".html"):
            self.index_callback(event.src_path)

def list_html_files(directory="."):
    """
    Recursively list all .html file paths relative to the given directory.

    :param directory: The root directory to start the search (default is current directory).
    :return: A list of relative file paths for .html files.
    """
    html_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                # Construct the relative path
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                html_files.append(relative_path)

    return html_files

def extract_content_for_index(file_path):
    """
    Extract content from an HTML file for search indexing.

    :param file_path: Path to the HTML file.
    :return: A dictionary with extracted content or None in case of an error.
    """
    try:
        with open(file_path, "r", encoding=html_encoding) as file:
            soup = BeautifulSoup(file, "html.parser")

            # Extract various components
            title = soup.title.string if soup.title else ""
            headings = " ".join(
                [h.get_text() for h in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])]
            )
            meta_tags = " ".join(
                [
                    meta.attrs.get("content", "")
                    for meta in soup.find_all("meta")
                    if meta.get("content")
                ]
            )
            body = soup.body.get_text(separator=" ") if soup.body else ""

            return {
                "title": title.strip(),
                "headings": headings.strip(),
                "meta_tags": meta_tags.strip(),
                "body": body.strip(),
                "path": file_path
            }
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return None

def create_search_index(directory=".", output_file="search_index.js"):
    """
    Find all HTML files in a directory, extract content, and create a search index.

    :param directory: Directory to search for HTML files.
    :param output_file: Path to save the JS search index.
    """
    try:
        # List all HTML files
        html_files = list_html_files(directory)

        # Dictionary to store all indexed content
        search_index = []

        # Process each HTML file with a progress bar
        for html_file in tqdm(html_files, desc="Indexing files"):
            content = extract_content_for_index(html_file)
            if content:
                search_index.append(content)

        # Save to JS file
        with open(output_file, "w", encoding="utf-8") as js_file:
            js_file.write(f"const searchIndex = {json.dumps(search_index, ensure_ascii=False, indent=2)};\n")

        print(f"\nIndex created successfully and saved to {output_file}")
        print(f"Total files indexed: {len(search_index)}")

    except Exception as e:
        print(f"An error occurred: {e}")

def update_search_index(file_path, output_file="search_index.js"):
    """
    Update the search index for a single file.

    :param file_path: Path to the HTML file to update.
    :param output_file: Path to the JS search index.
    """
    try:
        # Load existing index
        if os.path.exists(output_file):
            with open(output_file, "r", encoding="utf-8") as js_file:
                content = js_file.read()
                search_index = json.loads(content.replace("const searchIndex = ", "").rstrip(";\n"))
        else:
            search_index = []

        # Extract content for the file
        content = extract_content_for_index(file_path)
        if content:
            # Remove existing entry for the file
            search_index = [entry for entry in search_index if entry["path"] != file_path]
            # Add updated entry
            search_index.append(content)

            # Save updated index to JS file
            with open(output_file, "w", encoding="utf-8") as js_file:
                js_file.write(f"const searchIndex = {json.dumps(search_index, ensure_ascii=False, indent=2)};\n")

    except Exception as e:
        print(f"Error updating index for {file_path}: {e}")

def monitor_directory(directory=".", output_file="search_index.js"):
    """
    Monitor a directory for changes to HTML files and update the search index dynamically.

    :param directory: Directory to monitor.
    :param output_file: Path to the JS search index.
    """
    event_handler = HTMLFileHandler(lambda file_path: update_search_index(file_path, output_file))
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)

    try:
        print("Monitoring directory for changes...")
        observer.start()
        while True:
            pass
    except KeyboardInterrupt:
        print("\nStopping monitoring...")
        observer.stop()
    observer.join()

if __name__ == "__main__":
    # Create the initial search index
    create_search_index(directory=directory_to_search, output_file=search_index_output)

    # Start monitoring the directory
    monitor_directory(directory=directory_to_search, output_file=search_index_output)
