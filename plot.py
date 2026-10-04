# /// script
# requires-python = ">=3.10"
# dependencies = ["pandas", "numpy", "matplotlib", "cartopy"]
# ///

"""
Interactive storm-track map of the western North Pacific, 1980–2026.

- Every track is drawn with color mapped to wind speed (WMO_WIND),
  light blue (weak) → dark red (violent).
- A slider at the bottom picks a season. That season is drawn in colour,
  all other years fade to light grey.
- Saves out/storm-corridor.png before opening the interactive window.

    uv run plot.py
"""

from pathlib import Path

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
from matplotlib.widgets import Slider

HERE = Path(__file__).parent
DATA = HERE / "data"
OUT = HERE / "out"

# ---------------------------------------------------------------- load data
df = pd.read_csv(
    DATA / "ibtracs-wp-2000-2026.csv",
    skiprows=[1],
    usecols=["SID", "SEASON", "ISO_TIME", "LAT", "LON", "WMO_WIND"],
    low_memory=False,
)
df = df.dropna(subset=["LAT", "LON", "ISO_TIME"])
df["SEASON"] = pd.to_numeric(df["SEASON"], errors="coerce")
df["WMO_WIND"] = pd.to_numeric(df["WMO_WIND"], errors="coerce")
df = df[df["SEASON"] >= 1980]
df = df.sort_values(["SID", "ISO_TIME"])   # ISO 时间戳按字符串排序就是按时间排序

# -------------------------------------------- build per-storm line segments
segments = []   # 每场风暴一个 (N-1, 2, 2) 数组：段起点、段终点
winds = []      # 每场风暴一个 (N-1,) 数组：该段的参考风速
seasons = []    # 每场风暴一个 int：该风暴所属年份

for sid, g in df.groupby("SID"):
    if len(g) < 2:
        continue
    pts = g[["LON", "LAT"]].to_numpy()            # (N, 2)
    seg = np.stack([pts[:-1], pts[1:]], axis=1)   # (N-1, 2, 2)
    w = g["WMO_WIND"].to_numpy()[:-1]             # 段起点对应风速
    segments.append(seg)
    winds.append(w)
    seasons.append(int(g["SEASON"].iloc[0]))

seasons = np.array(seasons)

# ---------------------------------------------------------------- figure
OUT.mkdir(exist_ok=True)

fig = plt.figure(figsize=(12, 9))
ax = fig.add_axes([0.07, 0.18, 0.86, 0.76], projection=ccrs.PlateCarree())
ax.set_extent([100, 180, 0, 50], crs=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND, facecolor="#f2f0e6", edgecolor="none", zorder=0)
ax.add_feature(cfeature.COASTLINE, linewidth=0.5, edgecolor="#888", zorder=1)
ax.gridlines(draw_labels=True, linewidth=0.3, color="grey", alpha=0.4)
ax.set_title("Western North Pacific storm tracks by wind speed")

# 颜色映射：风速 0–120 kts，从浅蓝到深红
norm = Normalize(vmin=0, vmax=120)
cmap = plt.get_cmap("RdYlBu_r")

# ---- 底层：所有年份，灰色
all_segs = np.concatenate(segments)
grey = LineCollection(
    all_segs, colors="lightgrey", linewidths=0.4,
    transform=ccrs.PlateCarree(), zorder=2,
)
ax.add_collection(grey)

# ---- 高亮层：初始为空，滑块一变就换内容
highlight = LineCollection(
    [], linewidths=1.2, cmap=cmap, norm=norm,
    transform=ccrs.PlateCarree(), zorder=3,
)
ax.add_collection(highlight)

# ---- 色标
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
cbar = fig.colorbar(sm, ax=ax, orientation="vertical", pad=0.02, fraction=0.03)
cbar.set_label("Max wind (knots)")

# ---- 年份滑块
ax_year = fig.add_axes([0.15, 0.06, 0.7, 0.03])
year_min, year_max = int(seasons.min()), int(seasons.max())
slider = Slider(ax_year, "Season", year_min, year_max, valinit=year_max, valstep=1)

current = {"year": year_max}

def refresh(year):
    idx = np.where(seasons == year)[0]
    if len(idx) == 0:
        highlight.set_segments([])
        highlight.set_array(np.array([]))
    else:
        highlight.set_segments(np.concatenate([segments[i] for i in idx]))
        highlight.set_array(np.concatenate([winds[i] for i in idx]))
    ax.set_title(f"Western North Pacific storm tracks — {year}")
    fig.canvas.draw_idle()

def on_slider(val):
    year = int(slider.val)
    if year == current["year"]:
        return
    current["year"] = year
    refresh(year)

slider.on_changed(on_slider)

# 初始视图 = 最近一年
refresh(year_max)

fig.savefig(OUT / "storm-corridor.png", dpi=150)
plt.show()