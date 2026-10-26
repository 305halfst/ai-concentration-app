"""Rebuild the three files the app reads (data/processed/) from the two raw files in data/sources/.

Run from the repository root:   python data/build_processed.py
Needs: pandas, openpyxl.  Deterministic: the same sources give byte-identical outputs.
The script stops if either raw file's MD5 differs from the snapshot the app was built on.
"""
from pathlib import Path
import hashlib
import re

import pandas as pd

DATA = Path(__file__).resolve().parent
SRC, OUT = DATA / "sources", DATA / "processed"
OUT.mkdir(exist_ok=True)
MANIFEST = []

EXPECTED_MD5 = {
    "top500/TOP500_202606.xlsx": "26d72ecb9eb8fcdcefb0df3a1b215f79",   # TOP500 June 2026, downloaded 11/10/2026
    "epoch/data_centers.csv": "ea246ddea0bf7f561f99c1639662be23",      # Epoch AI data centres, downloaded 11/10/2026
}


def md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def check_sources() -> None:
    for rel, expected in EXPECTED_MD5.items():
        got = md5(SRC / rel)
        if got != expected:
            raise SystemExit(f"MD5 mismatch for {rel}: {got} != {expected} (source changed?)")
    print(f"OK  {len(EXPECTED_MD5)} source files match the recorded MD5s")


def save(df: pd.DataFrame, name: str, source: str, transform: str) -> None:
    df.to_csv(OUT / name, index=False, float_format="%.6g", lineterminator="\n")
    MANIFEST.append((name, len(df), source, transform))
    print(f"wrote {name:36s} {len(df):>4} rows")


def split_tokens(cell) -> list[str]:
    """'A, B, A' -> ['A', 'B'] (trimmed, de-duplicated, order kept)."""
    if pd.isna(cell):
        return []
    return list(dict.fromkeys(t.strip() for t in str(cell).split(",") if t.strip()))


def build_top500() -> None:
    raw = pd.read_excel(SRC / "top500/TOP500_202606.xlsx")
    assert raw["Rank"].is_unique and len(raw) == 500
    keep = {"Rank": "rank", "Name": "name", "Site": "site", "Manufacturer": "manufacturer", "Country": "country",
            "Year": "install_year", "Segment": "segment", "Rmax [TFlop/s]": "rmax_tflops",
            "Rpeak [TFlop/s]": "rpeak_tflops", "Power (kW)": "power_kw", "Total Cores": "total_cores"}
    systems = raw[list(keep)].rename(columns=keep)
    systems["sector_group"] = systems["segment"].map({"Research": "Public", "Academic": "Public", "Government": "Public",
                                                      "Industry": "Private", "Vendor": "Private", "Others": "Other"})
    assert systems["sector_group"].notna().all()
    save(systems, "top500_systems_clean.csv", "top500/TOP500_202606.xlsx",
         "Kept 11 of 38 columns, snake_case names. sector_group: Research/Academic/Government = Public; "
         "Industry/Vendor = Private; Others = Other. Power (kW) left blank where the source is blank.")
    seg = (systems.groupby(["sector_group", "segment"])
           .agg(n_systems=("rank", "size"), rmax_tflops=("rmax_tflops", "sum")).reset_index())
    seg["system_share_pct"] = (100 * seg["n_systems"] / seg["n_systems"].sum()).round(2)
    seg["rmax_share_pct"] = (100 * seg["rmax_tflops"] / seg["rmax_tflops"].sum()).round(2)
    save(seg.sort_values("rmax_share_pct", ascending=False), "fig4_top500_by_segment.csv", "top500/TOP500_202606.xlsx",
         "top500_systems_clean grouped by segment: count and sum of Rmax; shares of the 500 systems and of total Rmax.")


def build_datacenters() -> None:
    raw = pd.read_csv(SRC / "epoch/data_centers.csv")
    assert raw["Name"].is_unique

    def strip_tags(cell) -> str:
        return "|".join(re.sub(r"\s*#\w+", "", t).strip() for t in split_tokens(cell)) if pd.notna(cell) else ""

    sites = pd.DataFrame({
        "name": raw["Name"].str.strip(),
        "owner": raw["Owner"].map(strip_tags).replace("", "Unknown"),
        "country": raw["Country"],
        "h100_equivalents": raw["Current H100 equivalents"].round(0),
        "power_mw": raw["Current power (MW)"].round(1),
        "capital_cost_2025usd_bn": raw["Current total capital cost (2025 USD billions)"].round(3),
    }).sort_values("capital_cost_2025usd_bn", ascending=False)
    owners = (sites.groupby("owner")
              .agg(country=("country", lambda cs: "|".join(dict.fromkeys(c for cell in cs for c in split_tokens(cell)))),
                   n_datacenters=("name", "size"), capital_cost_2025usd_bn=("capital_cost_2025usd_bn", "sum"),
                   power_mw=("power_mw", "sum"), h100_equivalents=("h100_equivalents", "sum"))
              .reset_index())
    owners.insert(2, "n_countries", owners["country"].str.split("|").map(len))
    owners = owners.sort_values("capital_cost_2025usd_bn", ascending=False)
    owners["capex_share_pct"] = (100 * owners["capital_cost_2025usd_bn"] / owners["capital_cost_2025usd_bn"].sum()).round(2)
    save(owners, "datacenters_by_owner_country.csv", "epoch/data_centers.csv",
         "Removed '#confident/#likely/#speculative' tags from Owner; missing owner -> 'Unknown'. Grouped site rows by "
         "owner (operator, not model developer): listed site countries (de-duplicated, joined with '|'), country count, "
         "site count, sums of capital cost, power and H100 equivalents, and each owner's share of total capital cost.")


def write_manifest() -> None:
    man = pd.DataFrame(MANIFEST, columns=["processed_file", "rows", "source_files", "transform"])
    man["md5"] = man["processed_file"].map(lambda f: md5(OUT / f))
    man.to_csv(OUT / "MANIFEST.csv", index=False, lineterminator="\n")
    print(f"wrote MANIFEST.csv ({len(man)} files)")


if __name__ == "__main__":
    check_sources()
    build_top500()
    build_datacenters()
    write_manifest()
