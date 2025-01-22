# Generic Search Template for Static Applications

This project provides a simple and efficient way to add search functionality to static web applications. It automatically creates and maintains a search index for HTML files and provides a clean, modern search interface that can be easily integrated into any static website.

## Features

- Dynamic indexing of HTML files
- Real-time file monitoring and index updates
- Clean and responsive search interface
- No backend server required - works entirely client-side
- Support for Windows-1251 encoded HTML files
- Easy integration with existing static websites

## Project Structure

- `dynamic_html_indexer.py` - Python script for creating and maintaining the search index
- `index.html` - Main search interface
- `search.js` - Client-side search implementation
- `search_index.js` - Generated search index
- `styles.css` - Styling for the search interface

## Getting Started

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the indexer:
   ```bash
   python dynamic_html_indexer.py
   ```

3. Open `index.html` in your web browser to use the search functionality.

## Configuration

The main configuration options are in `dynamic_html_indexer.py`:

- `html_encoding`: Set the encoding for HTML files (default: "windows-1251")
- `directory_to_search`: Directory to search for HTML files (default: ".")
- `search_index_output`: Output file for the search index (default: "search_index.js")

## Integration

To add search to your static website:

1. Copy the following files to your project:
   - `search.js`
   - `styles.css`
   - `index.html`
   - Generated `search_index.js`

2. Modify the `CONFIG` object in `index.html` to match your application's configuration.

3. Open `index.html` in your web browser to test the search functionality.



## License

This project is licensed under the MIT License.

