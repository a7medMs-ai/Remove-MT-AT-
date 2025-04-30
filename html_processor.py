# analyzer/html_processor.py

import os
from concurrent.futures import ThreadPoolExecutor
from analyzer.content_analyzer import extract_page_data

def process_all_pages_parallel(html_folder: str, max_workers: int = 5) -> list:
    """
    Process all HTML files in the given folder using parallel threads.

    Parameters:
    - html_folder (str): Path to the folder containing HTML files.
    - max_workers (int): Number of parallel threads to use.

    Returns:
    - list: List of dictionaries containing page analysis results.
    """
    html_files = [f for f in os.listdir(html_folder) if f.endswith(".html")]
    results = []

    def process_file(index, file):
        with open(os.path.join(html_folder, file), encoding="utf-8") as f:
            html_content = f.read()
        return extract_page_data(
            html_content,
            page_url=f"http://example.com/{file}",
            page_name=file,
            counter=index + 1
        )

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_file, idx, file) for idx, file in enumerate(html_files)]
        for future in futures:
            results.append(future.result())

    return results
