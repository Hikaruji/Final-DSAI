"""Quick local check for image_url quality.

This does not require internet. It reports obviously corrupted URLs and
values replaced by local fallbacks after the backend loader sanitises them.
"""

from collections import Counter
from urllib.parse import urlparse

import pandas as pd

from app.data_loader import PLACES
from app.image_utils import is_suspicious_image_url


def main() -> None:
    df = pd.read_excel("Full_Translated_DataSet_V2.xlsx")
    raw_urls = df["Image_URL"].fillna("").astype(str).str.strip().tolist()

    suspicious = []
    for i, raw in enumerate(raw_urls, start=1):
        if is_suspicious_image_url(raw):
            suspicious.append((i, raw))

    loaded_hosts = Counter(
        urlparse(p.image_url).netloc or "local-fallback"
        for p in PLACES
    )

    print(f"Total rows: {len(raw_urls)}")
    print(f"Suspicious raw URLs replaced by fallback: {len(suspicious)}")
    print("\nMost common loaded image hosts:")
    for host, count in loaded_hosts.most_common(15):
        print(f"  {host:40s} {count}")

    if suspicious:
        print("\nExamples of suspicious raw URLs:")
        for row, raw in suspicious[:20]:
            print(f"  row {row:03d}: {raw[:100]!r}")

    print("\nSample loaded image URLs:")
    for p in PLACES[:10]:
        print(f"  {p.id} | {p.name:35s} -> {p.image_url}")


if __name__ == "__main__":
    main()
