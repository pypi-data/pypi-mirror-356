import pandas as pd
from typing import List, Dict, Any

def augment_schema_with_examples(
    cleaned_df: pd.DataFrame,
    raw_schema_map: Dict[str, Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    """
    Enhance each column in the schema with up to 10 example values.
    Properly formats values for MariaDB insertion.
    """
    if not isinstance(cleaned_df, pd.DataFrame):
        raise TypeError("Expected `cleaned_df` to be a pandas DataFrame.")

    augmented_schema = {}

    for col, col_info in raw_schema_map.items():
        if col not in cleaned_df.columns:
            raise KeyError(f"Column '{col}' not found in provided DataFrame.")

        entry = dict(col_info)

        series = cleaned_df[col]
        if not isinstance(series, pd.Series):
            raise TypeError(f"Expected column '{col}' to be a pandas Series.")

        series = series.dropna()
        example_list: List[Any] = []

        if len(series) > 0:
            unique_vals = series.drop_duplicates().head(10).tolist()
            for v in unique_vals:
                if isinstance(v, pd.Timestamp):
                    if col_info["data_type"] == "DATE":
                        fmt = col_info.get("date_format_in_database") or "%Y-%m-%d"
                        example_list.append(v.strftime(fmt))
                    elif col_info["data_type"] == "DATETIME":
                        fmt = col_info.get("date_format_in_database") or "%Y-%m-%d %H:%M:%S"
                        example_list.append(v.strftime(fmt))
                    else:
                        example_list.append(str(v))
                elif isinstance(v, pd.Timedelta):
                    example_list.append(str(v))
                else:
                    example_list.append(v)

        entry["example_data"] = example_list
        augmented_schema[col] = entry

    return augmented_schema