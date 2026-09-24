# /// script
# requires-python = ">=3.10"
# dependencies = ["pandas", "matplotlib"]
# ///

"""
Draw every storm track in the western North Pacific as one picture.

    uv run plot.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).parent
DATA = HERE / "data"
OUT = HERE / "out"

df = pd.read_csv(
    DATA / "ibtracs-wp-2000-2026.csv",
    skiprows=[1],
    usecols=["SID", "SEASON", "LAT", "LON", "WMO_WIND"],  
    low_memory=False,
)

df = df.dropna(subset=["LAT", "LON", "WMO_WIND"])           
df = df[df["SEASON"] >= 2000]                               

OUT.mkdir(exist_ok=True)

fig, ax = plt.subplots(figsize=(10, 8))

for sid, track in df.groupby("SID"):
    ax.plot(track["LON"], track["LAT"], linewidth=0.5, alpha=0.4, color="steelblue")

ax.set_title("Western North Pacific storm tracks (IBTrACS, 2000–2026)")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_xlim(100, 180)
ax.set_ylim(0, 50)
ax.grid(True, linewidth=0.3, alpha=0.5)

fig.tight_layout()
fig.savefig(OUT / "storm-corridor.png", dpi=150)
plt.show()