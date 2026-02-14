import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def crawl_website(start_url: str, max_pages: int = 2) -> dict:
    """Crawl 1–2 pages only. Returns structured data for AI analysis."""
    if not start_url.startswith(("http://", "https://")):
        start_url = "https://" + start_url

    visited = set()
    to_visit = [start_url]
    data = {
        "url": start_url,
        "title": "",
        "meta_description": "",
        "headings": [],
        "images": [],
        "text_content": "",
        "page_count": 0,
        "load_time_seconds": 0.0,
        "num_images": 0,
        "text_length": 0,
    }

    total_load_time = 0.0
    pages_crawled = 0

    while to_visit and pages_crawled < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)

        try:
            start = time.time()
            resp = requests.get(
                url,
                timeout=10,
                headers={"User-Agent": "ArvixAI-Website-Auditor/1.0"}
            )
            resp.raise_for_status()
            load_time = time.time() - start
            total_load_time += load_time

            soup = BeautifulSoup(resp.text, "html.parser")

            if not data["title"]:
                data["title"] = soup.title.string.strip() if soup.title else ""
            if not data["meta_description"]:
                meta = soup.find("meta", attrs={"name": "description"})
                data["meta_description"] = meta["content"].strip() if meta and meta.get("content") else ""

            # Headings
            for lvl in range(1, 7):
                for h in soup.find_all(f"h{lvl}"):
                    text = h.get_text(strip=True)
                    if text:
                        data["headings"].append({"level": lvl, "text": text})

            # Images
            for img in soup.find_all("img"):
                src = img.get("src")
                if src:
                    data["images"].append({
                        "src": urljoin(url, src),
                        "alt": img.get("alt", "").strip()
                    })

            data["text_content"] += " " + soup.get_text(separator=" ", strip=True)[:12000]

            # Queue internal links
            domain = urlparse(start_url).netloc
            for a in soup.find_all("a", href=True):
                link = urljoin(url, a["href"])
                parsed = urlparse(link)
                if (parsed.netloc == domain and
                    link not in visited and
                    "#" not in link and
                    not link.endswith((".pdf", ".jpg", ".png", ".gif"))):
                    to_visit.append(link)

            pages_crawled += 1

        except Exception as e:
            print(f"Warning: Could not crawl {url} → {e}")

    data["page_count"] = pages_crawled
    data["load_time_seconds"] = round(total_load_time / max(1, pages_crawled), 2)
    data["num_images"] = len(data["images"])
    data["text_length"] = len(data["text_content"])
    data["headings"] = data["headings"][:40]   # limit prompt size
    data["images"] = data["images"][:30]

    return data