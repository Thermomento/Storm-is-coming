# /// script
# requires-python = ">=3.10"
# dependencies = ["pandas"]
# ///
from pathlib import Path
import pandas as pd

HERE = Path(__file__).parent
df = pd.read_csv(HERE / "data" / "ibtracs-west-pacific.csv", skiprows=[1], low_memory=False)

print(df.columns.tolist())       # 列名，应该看到 SID, LAT, LON, WMO_WIND ...
print(df.iloc[0][["SID", "NAME", "LAT", "LON"]])   # 第一行
print(type(df["LAT"].iloc[0]))   # LAT 的类型