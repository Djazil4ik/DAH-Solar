#!/usr/bin/env python3
"""
DAH Solar Product Scraper
Scrapes product data from en.dahsolar.com and outputs JSON + CSV.
Images are downloaded to ./images/<model_slug>/ folder.

Usage:
    python3 dahsolar_scraper.py --urls urls.txt
    python3 dahsolar_scraper.py --url "https://en.dahsolar.com/prodetails/..."
    python3 dahsolar_scraper.py --url "..." --no-images   # skip image download
    python3 dahsolar_scraper.py --url "..." --images-dir /var/www/media/products
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import argparse
import sys
import re
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

DELAY_BETWEEN_REQUESTS = 2    # seconds between product pages
DELAY_BETWEEN_IMAGES = 0.3  # seconds between image downloads


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fetch_page(url: str) -> BeautifulSoup | None:
    """Fetch a page and return BeautifulSoup object."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except requests.RequestException as e:
        print(f"  [ERROR] Failed to fetch {url}: {e}")
        return None


def model_to_slug(model: str) -> str:
    """Convert model name to filesystem-safe folder name, e.g. DHN-66Z20 -> DHN_66Z20"""
    return re.sub(r"[^\w\-]", "_", model).strip("_")


# ---------------------------------------------------------------------------
# Image downloader
# ---------------------------------------------------------------------------

def download_images(image_urls: list[str], model: str, images_root: Path) -> list[dict]:
    """
    Download images into images_root/<model_slug>/
    Returns list of:
        {
            "original_url": "https://...",
            "local_path":   "images/DHN_66Z20/image_001.png",   # relative path
            "filename":     "image_001.png"
        }
    """
    if not image_urls:
        return []

    folder = images_root / model_to_slug(model)
    folder.mkdir(parents=True, exist_ok=True)

    results = []
    for i, url in enumerate(image_urls, 1):
        # Detect extension (strip CDN query params like ?vf=B7gH3s)
        clean_url = url.split("?")[0]
        ext = Path(urlparse(clean_url).path).suffix.lower()
        if ext not in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}:
            ext = ".jpg"

        filename = f"image_{i:03d}{ext}"
        local_path = folder / filename
        rel_path = str(local_path)  # e.g. "images/DHN_66Z20/image_001.png"

        # Skip if already downloaded (re-run safe)
        if local_path.exists():
            print(f"    [skip] {filename} (already exists)")
            results.append(
                {"original_url": url, "local_path": rel_path, "filename": filename})
            continue

        try:
            resp = requests.get(url, headers=HEADERS, timeout=20, stream=True)
            resp.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            size_kb = local_path.stat().st_size // 1024
            print(f"    ✓ {filename}  ({size_kb} KB)")
            results.append(
                {"original_url": url, "local_path": rel_path, "filename": filename})

        except requests.RequestException as e:
            print(f"    ✗ {filename} — {e}")
            results.append(
                {"original_url": url, "local_path": None, "filename": filename})

        time.sleep(DELAY_BETWEEN_IMAGES)

    return results


# ---------------------------------------------------------------------------
# Page extractors
# ---------------------------------------------------------------------------

def extract_product_name(soup: BeautifulSoup) -> dict:
    result = {"category": "", "model": ""}

    cat_el = soup.select_one(".e_text-4")
    if cat_el:
        result["category"] = cat_el.get_text(strip=True)

    model_el = soup.select_one(".con_tit.fnt_40, h1.e_text-5")
    if model_el:
        result["model"] = model_el.get_text(strip=True)

    if not result["model"]:
        title = soup.find("title")
        if title:
            raw = title.get_text(strip=True)
            result["model"] = raw.split("-DAH Solar")[0].split("|")[0].strip()

    return result


def extract_key_specs(soup: BeautifulSoup) -> list[dict]:
    """Highlighted key specs (efficiency, warranties, etc.)."""
    specs = []
    for item in soup.select(".e_loop_sub-6 .p_loopItem"):
        key_el = item.select_one(".e_text-8")
        val_el = item.select_one(".e_text-9")
        if key_el and val_el:
            key = key_el.get_text(strip=True)
            val = val_el.get_text(strip=True)
            if key:
                specs.append({"label": key, "value": val})
    return specs


def extract_parameter_tables(soup: BeautifulSoup) -> dict:
    """All parameter tables keyed by tab name."""
    tab_names = [
        h.get_text(strip=True)
        for h in soup.select(".e_container-13 .p_item h3")
        if h.get_text(strip=True)
    ]

    tables_data = {}
    for i, rt in enumerate(soup.select(".e_container-19 .p_item > .s_title")):
        table = rt.find("table")
        if not table:
            continue
        tab_name = tab_names[i] if i < len(tab_names) else f"Table_{i+1}"
        rows_data = []
        for row in table.find_all("tr"): #type: ignore
            cells = [td.get_text(strip=True) for td in row.find_all("td")] #type: ignore
            if any(c for c in cells):
                rows_data.append(cells)
        if rows_data:
            tables_data[tab_name] = rows_data

    return tables_data


def extract_advantages(soup: BeautifulSoup) -> list[dict]:
    """
    Product advantages — each slide may have:
      h3.e_text-9  → title   (e.g. "Higher load capacity")
      p.e_text-10  → description
    """
    advantages = []
    for slide in soup.select(".e_loop_sub-4 .p_loopItem"):
        title_el = slide.select_one(".e_text-9")
        desc_el = slide.select_one(".e_text-10")
        title = title_el.get_text(strip=True) if title_el else ""
        desc = desc_el.get_text(strip=True) if desc_el else ""
        if title or desc:
            advantages.append({"title": title, "description": desc})
    return advantages


def extract_images(soup: BeautifulSoup) -> list[str]:
    """Product image URLs (lazy-loaded src attributes)."""
    images, seen = [], set()
    for img in soup.select(".swpt1 img, .e_subImg-15 img"):
        src = img.get("lazy") or img.get("src", "")
        if src and not src.endswith("s.png") and src not in seen: # type: ignore
            seen.add(src)
            images.append(src)
    return images


def extract_pdf_link(soup: BeautifulSoup) -> str:
    for a in soup.find_all("a", href=True):
        if a["href"].lower().endswith(".pdf"): # type: ignore
            return a["href"] # type: ignore
    return ""


# ---------------------------------------------------------------------------
# Main scrape function
# ---------------------------------------------------------------------------

def scrape_product(url: str, images_root: Path | None = None) -> dict | None:
    """
    Scrape one product page.
    images_root=None  → URLs recorded but nothing downloaded.
    images_root=Path  → images saved to images_root/<model>/
    """
    print(f"  Scraping: {url}")
    soup = fetch_page(url)
    if not soup:
        return None

    name_data = extract_product_name(soup)
    key_specs = extract_key_specs(soup)
    param_tables = extract_parameter_tables(soup)
    advantages = extract_advantages(soup)
    image_urls = extract_images(soup)
    pdf_link = extract_pdf_link(soup)

    if images_root is not None and image_urls:
        model = name_data["model"] or "unknown"
        print(
            f"  Downloading {len(image_urls)} image(s) → {images_root}/{model_to_slug(model)}/")
        images = download_images(image_urls, model, images_root)
    else:
        images = [
            {"original_url": u, "local_path": None, "filename": None}
            for u in image_urls
        ]

    return {
        "url":              url,
        "scraped_at":       datetime.utcnow().isoformat() + "Z",
        "category":         name_data["category"],
        "model":            name_data["model"],
        "key_specs":        key_specs,
        "parameter_tables": param_tables,
        "advantages":       advantages,
        # each entry: {"original_url": "...", "local_path": "images/.../image_001.png", "filename": "..."}
        "images":           images,
        "pdf_datasheet":    pdf_link,
    }


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def flatten_for_csv(product: dict) -> dict:
    adv_parts = []
    for adv in product["advantages"]:
        if adv["title"] and adv["description"]:
            adv_parts.append(f"{adv['title']}: {adv['description']}")
        elif adv["title"]:
            adv_parts.append(adv["title"])
        elif adv["description"]:
            adv_parts.append(adv["description"])

    orig_urls = [img["original_url"] for img in product["images"]]
    local_paths = [img["local_path"] or "" for img in product["images"]]

    row = {
        "url":           product["url"],
        "scraped_at":    product["scraped_at"],
        "category":      product["category"],
        "model":         product["model"],
        "pdf_datasheet": product["pdf_datasheet"],
        # original CDN URLs  (pipe-separated)
        "image_urls":    " | ".join(orig_urls),
        # local file paths after download  (pipe-separated, empty if --no-images)
        "image_local":   " | ".join(p for p in local_paths if p),
        "advantages":    " | ".join(adv_parts),
    }

    for spec in product["key_specs"]:
        col = "spec_" + re.sub(r"[^\w]", "_", spec["label"].lower()).strip("_")
        row[col] = spec["value"]

    for table_name, rows in product["parameter_tables"].items():
        col = "params_" + re.sub(r"[^\w]", "_", table_name.lower()).strip("_")
        flat = "; ".join([" | ".join(r) for r in rows])
        row[col] = flat

    return row


def save_json(products: list[dict], path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    print(f"\n✅ JSON saved: {path}")


def save_csv(products: list[dict], path: str):
    if not products:
        return
    rows = [flatten_for_csv(p) for p in products]

    all_keys: list[str] = []
    seen_keys: set[str] = set()
    for row in rows:
        for k in row:
            if k not in seen_keys:
                seen_keys.add(k)
                all_keys.append(k)

    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=all_keys, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f"✅ CSV saved: {path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="DAH Solar product scraper — exports JSON + CSV, downloads images")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url",  help="Single product URL")
    group.add_argument("--urls", help="Text file with one URL per line")
    parser.add_argument("--output",     default="dahsolar_products",
                        help="Output filename prefix (default: dahsolar_products)")
    parser.add_argument("--images-dir", default="images",
                        help="Folder to save images (default: ./images)")
    parser.add_argument("--no-images",  action="store_true",
                        help="Skip image downloading (only store URLs)")
    parser.add_argument("--delay", type=float, default=DELAY_BETWEEN_REQUESTS,
                        help=f"Delay between pages in seconds (default: {DELAY_BETWEEN_REQUESTS})")
    args = parser.parse_args()

    if args.url:
        urls = [args.url.strip()]
    else:
        p = Path(args.urls)
        if not p.exists():
            print(f"[ERROR] File not found: {args.urls}")
            sys.exit(1)
        urls = [
            line.strip() for line in p.read_text().splitlines()
            if line.strip() and not line.startswith("#")
        ]

    images_root = None if args.no_images else Path(args.images_dir)
    if images_root:
        images_root.mkdir(parents=True, exist_ok=True)

    print(f"\n🔆 DAH Solar Scraper")
    print(f"   URLs to process : {len(urls)}")
    print(
        f"   Images folder   : {'disabled (--no-images)' if args.no_images else args.images_dir}")
    print(f"   Delay           : {args.delay}s between pages\n")

    products, failed = [], []

    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}]", end=" ")
        product = scrape_product(url, images_root=images_root)
        if product:
            products.append(product)
            n = len(product["images"])
            print(f"  ✓ {product['model'] or 'Unknown'} — {n} image(s)")
        else:
            failed.append(url)
            print("  ✗ Failed")

        if i < len(urls):
            time.sleep(args.delay)

    print(f"\n📊 Results: {len(products)} succeeded, {len(failed)} failed")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    if products:
        save_json(products, f"{args.output}_{ts}.json")
        save_csv(products,  f"{args.output}_{ts}.csv")

    if failed:
        fp = f"{args.output}_failed_{ts}.txt"
        Path(fp).write_text("\n".join(failed))
        print(f"⚠️  Failed URLs: {fp}")

    print("\nDone!")


if __name__ == "__main__":
    main()
