from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
import os


REFERENCE_LIST_URL = "https://mathworks.com/help/matlab/referencelist.html"


def extract_function_names_with_playwright(url):
    # Start Playwright
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        # Wait for the page to fully load (adjust timeout if needed)
        page.wait_for_timeout(10000)
        html_content = page.content()
        browser.close()

    # Parse the rendered HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all <td> elements with the specified class
    td_elements = soup.find_all("td", class_="term add_font_monospace")

    # Extract the text from the <a> element, skipping those with 'data-toggle' and 'title' attributes
    links = {}
    for td in td_elements:
        a_elements = td.find_all("a")
        for a in a_elements:
            if not (a.has_attr("data-toggle") and a.has_attr("title")) and a.has_attr("href"):
                name = a.text.strip()
                if name.isalnum():  # Check if name is alphanumeric
                    links[name] = a["href"]
                    break  # Only consider the first valid <a> element in the <td>

    return links


if __name__ == "__main__":
    links = extract_function_names_with_playwright(REFERENCE_LIST_URL)

    if links:
        sorted_links = {k: links[k] for k in sorted(links.keys())}

        output_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "src",
            "mkdocstrings_handlers",
            "matlab",
        )
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "matlab_builtins.json")
        with open(output_file, "w") as f:
            json.dump(sorted_links, f, indent=4)

        print(f"Saved {len(links)} function names to matlab_builtins.json")
    else:
        print("No function names found or failed to retrieve the page.")
