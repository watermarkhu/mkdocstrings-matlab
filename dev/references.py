

import json
from pathlib import Path

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

REFERENCE_LIST_URL = "https://mathworks.com/help/matlab/referencelist.html"

def scrape_references() -> None:
    """
    Scrapes the MATLAB reference list from the MathWorks website and saves it as a JSON file.

    Returns:
        None
    """
    opts = Options()
    opts.add_argument("-headless")
    driver = Firefox(options=opts)
    driver.get(REFERENCE_LIST_URL)

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//table[@class='table tablecondensed has_limited_support']")) 
        )
        elements = driver.find_elements(By.XPATH, "//td[@class='term add_font_monospace']/a[2]")
        reference_dict = {item.get_attribute('innerHTML'): item.get_attribute('href') for item in elements}

        file = Path(__file__).parents[1] / "src" / "matlab_path" / "matlab" / "data" / "references.json"
        with open(file, "w") as outfile:
            json.dump(reference_dict, outfile, indent=2)

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_references()