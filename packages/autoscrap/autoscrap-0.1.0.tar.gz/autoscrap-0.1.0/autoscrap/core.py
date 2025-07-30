import requests
from bs4 import BeautifulSoup
from typing import List, Optional


def get_text(url: str, tag: str) -> List[str]:
    """
    Fetches all text within a given HTML tag from the specified URL.
    Returns a list of strings (text content of each tag found).
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[AutoScrap] Error fetching URL: {e}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all(tag)
    if not elements:
        print(f"[AutoScrap] No elements found for tag '<{tag}>' on the page.")
    return [el.get_text(strip=True) for el in elements]


def extract_table(url: str, as_dataframe: bool = False) -> Optional[object]:
    """
    Extracts the first HTML table from the URL.
    Returns a list of lists (rows), or a pandas DataFrame if as_dataframe=True and pandas is installed.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[AutoScrap] Error fetching URL: {e}")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    if not table:
        print("[AutoScrap] No table found on the page.")
        return None
    rows = []
    for tr in table.find_all('tr'):
        cells = tr.find_all(['td', 'th'])
        rows.append([cell.get_text(strip=True) for cell in cells])
    if as_dataframe:
        try:
            import pandas as pd
            return pd.DataFrame(rows[1:], columns=rows[0]) if len(rows) > 1 else pd.DataFrame(rows)
        except ImportError:
            print("[AutoScrap] pandas is not installed. Install it or set as_dataframe=False.")
            return None
    return rows 