import requests
from bs4 import BeautifulSoup

def get_wikipedia_summary(query, sentences=2):
    search_url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    print('Search Url:',search_url)
    
    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        return "Could not retrieve Wikipedia page."

    soup = BeautifulSoup(response.text, "lxml")
    
    paragraphs = soup.find_all("p")
    summary = ""

    for para in paragraphs:
        text = para.get_text().strip()
        if text:
            summary += " " + text
            if summary.count(".") >= sentences:
                break

    return summary if summary else "No relevant summary found."
