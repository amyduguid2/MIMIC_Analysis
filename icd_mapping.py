import pandas as pd
from pathlib import Path

def _read_icd9_to10_gem(path: str | Path) -> pd.DataFrame:
    """
    Read the ICD-9-CM → ICD-10-CM GEM file (e.g., "2018_I9gem.txt").
    Returns a DataFrame with two columns: src_code (ICD9) and tgt_code (ICD10).
    """
    # Read the GEM text file; it's whitespace-delimited, no headers
    gem = pd.read_csv(path, sep=r"\s+", header=None, comment="#", dtype=str, engine="python")
    
    # Keep only the first two columns (ICD9 code, ICD10 code)
    gem = gem.iloc[:, :2].copy()
    
    # Rename them for clarity
    gem.columns = ["src_code", "tgt_code"]
    
    # Drop rows where the ICD10 code is missing
    gem = gem[gem["tgt_code"].notna() & (gem["tgt_code"] != "")]
    
    # Remove duplicates if any
    return gem.drop_duplicates()


def convert_to_icd10(
    df: pd.DataFrame,
    code_col: str,
    icd_version_col: str = "icd_version",
    icd9_to10_gem_path: str | Path = "2018_I9gem.txt",
    keep_unmapped: bool = True,
) -> pd.DataFrame:
    """
    Convert a mixed ICD-9/ICD-10 dataset to ICD-10 using the ICD-9→ICD-10 GEM file.
    - df: input DataFrame
    - code_col: name of the column with ICD codes
    - icd_version_col: column with version (9 or 10)
    - icd9_to10_gem_path: path to GEM file (e.g. 2018_I9gem.txt)
    - keep_unmapped: whether to keep ICD9 rows that don’t map
    """

    # Make a copy so we don’t modify the original DataFrame
    dt = df.copy()

    # Function to normalize icd_version values into strings "ICD9"/"ICD10"
    def _norm_ver(v):
        s = str(v).strip()  # convert to string and trim spaces
        if s == "9": return "ICD9"
        if s == "10": return "ICD10"
        return None  # invalid values become None

    # Apply normalization to the icd_version column
    dt["_src_system"] = dt[icd_version_col].map(_norm_ver)

    # Safety check: throw error if there are unexpected values (not 9/10)
    if dt["_src_system"].isna().any():
        bad = dt.loc[dt["_src_system"].isna(), icd_version_col].unique()
        raise ValueError(f"Found non-9/10 values in '{icd_version_col}': {bad}")

    # Load the ICD9 → ICD10 mapping table from GEM file
    gem_9to10 = _read_icd9_to10_gem(icd9_to10_gem_path)

    # Identify rows that need mapping (ICD9) and those already ICD10
    need_map = dt["_src_system"] == "ICD9"
    to_map = dt[need_map].copy()        # ICD9 rows → need conversion
    pass_through = dt[~need_map].copy() # ICD10 rows → keep as-is

    # Merge ICD9 rows with GEM mapping (left join keeps all ICD9 rows)
    # → if one ICD9 maps to multiple ICD10s, you get multiple rows
    mapped = to_map.merge(
        gem_9to10, left_on=code_col, right_on="src_code", how="left"
    )

    # Add output columns: we’re converting everything to ICD10
    mapped["target_system"] = "ICD10"
    mapped["target_code"] = mapped["tgt_code"]  # mapped ICD10 code

    # For ICD10 rows, just carry them forward
    pass_through["target_system"] = "ICD10"
    pass_through["target_code"] = pass_through[code_col]

    # Combine mapped ICD9 rows and pass-through ICD10 rows
    out = pd.concat([mapped, pass_through], ignore_index=True)

    # Optionally drop ICD9 rows that failed to map (target_code is null)
    if not keep_unmapped:
        out = out[~((out["_src_system"] == "ICD9") & out["target_code"].isna())]

    # Keep original columns plus the new standardized target columns
    keep_cols = list(df.columns) + ["target_system", "target_code"]

    # Return clean DataFrame
    return out[keep_cols].reset_index(drop=True)


# -------------------------
# Example usage
# -------------------------
# df = pd.DataFrame({
#     "pt": [1,2,3,4],
#     "code": ["25000","E119","41401","S72001A"],
#     "icd_version": [9,10,9,10]
# })
#
# out = convert_to_icd10(df, code_col="code", icd_version_col="icd_version",
#                        icd9_to10_gem_path="2018_I9gem.txt")
# print(out)
