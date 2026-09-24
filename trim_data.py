# /// script
# requires-python = ">=3.10"
# dependencies = ["pandas", "requests"]
# ///
from pathlib import Path
import pandas as pd
import requests

HERE = Path(__file__).parent
RAW = HERE / "data" / "raw_ibtracs.csv"
SMALL = HERE / "data" / "ibtracs-wp-2000-2026.csv"


if not RAW.exists():
    url = "https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/ibtracs.WP.list.v04r01.csv"
    print("Downloading (approx 110MB, may take a while)...")
    r = requests.get(url, headers={"User-Agent": "SD5913 PolyU student"}, timeout=120)
    r.raise_for_status()
    RAW.write_bytes(r.content)

# 裁剪：只保留 2000 年以后
print("Trimming...")
df = pd.read_csv(RAW, skiprows=[1], low_memory=False)
df = df[df["SEASON"] >= 2000]
df.to_csv(SMALL, index=False)
print(f"Saved {SMALL.name}, size: {SMALL.stat().st_size // 1024 // 1024} MB")