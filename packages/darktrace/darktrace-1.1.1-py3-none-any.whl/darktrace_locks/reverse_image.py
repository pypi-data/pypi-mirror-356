# darktrace_locks/reverse_image.py

import os
import requests
from bs4 import BeautifulSoup

def reverse_image_search(image_path):
    print("🔍 Performing reverse image search...")

    try:
        # Bing reverse image search URL
        search_url = "https://www.bing.com/images/searchbyimage?cbir=sbi&imgurl=file://" + os.path.abspath(image_path)
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(search_url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            results = []

            # Extract titles and snippets
            for tag in soup.find_all("a", {"class": "iusc"}):
                title = tag.get("m", "")
                if title:
                    results.append(title)

            if results:
                print("✅ Results found:")
                for res in results[:5]:
                    print("•", res)
            else:
                print("❌ No results found.")

        else:
            print("❌ Bing search failed:", response.status_code)

    except Exception as e:
        print("⚠️ Reverse search error:", str(e))
