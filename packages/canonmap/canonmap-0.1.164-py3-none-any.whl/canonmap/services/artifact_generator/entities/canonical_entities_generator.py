# canonmap/services/artifact_generator/entities/canonical_entities_generator.py

import logging
import pandas as pd
import re
from typing import List, Dict, Any, Optional, Set, Tuple
from canonmap.utils.logger import get_logger
from canonmap.services.artifact_generator.ingestion.clean_columns import _clean_column_name

logger = get_logger("canonical_entities_generator")

def _analyze_field_values(values: List[str], split: bool = False) -> Tuple[int, int, float, float]:
    """
    Analyze field values to compute statistics both with and without comma splitting.
    
    Args:
        values: List of string values to analyze
        split: Whether to analyze after splitting on commas
        
    Returns:
        Tuple of (total_count, unique_count, uniqueness_ratio, avg_length)
    """
    if split:
        # Split on commas and analyze individual tokens
        tokens = [token.strip() for v in values for token in v.split(",") if token.strip()]
        total = len(tokens)
        unique = len(set(tokens))
        avg_length = sum(len(token) for token in tokens) / total if total > 0 else 0
    else:
        # Analyze whole values
        total = len(values)
        unique = len(set(values))
        avg_length = sum(len(v) for v in values) / total if total > 0 else 0
    
    uniqueness_ratio = unique / total if total > 0 else 0
    return total, unique, uniqueness_ratio, avg_length

def _should_split_on_commas(series: pd.Series) -> bool:
    """
    Determine if a field should be split on commas based on statistical analysis.
    
    Args:
        series: The pandas Series to analyze
        
    Returns:
        bool: Whether the field should be split on commas
    """
    # Skip if empty
    if series.empty:
        return False
    
    # Get non-empty values
    values = [str(v).strip() for v in series.dropna() if str(v).strip()]
    if not values:
        return False
    
    # Analyze both unsplit and split variants
    tot_unsplit, uniq_unsplit, ratio_unsplit, avg_unsplit = _analyze_field_values(values, split=False)
    tot_split, uniq_split, ratio_split, avg_split = _analyze_field_values(values, split=True)
    
    # Log statistics for debugging
    logger.info(f"Field value analysis:")
    logger.info(f"  Unsplit -> Count: {tot_unsplit}, Unique: {uniq_unsplit}, Ratio: {ratio_unsplit:.2f}, Avg Length: {avg_unsplit:.2f}")
    logger.info(f"  Split   -> Count: {tot_split}, Unique: {uniq_split}, Ratio: {ratio_split:.2f}, Avg Length: {avg_split:.2f}")
    
    # Decision criteria:
    
    # 1. Must have some comma-containing values
    if tot_split <= tot_unsplit:
        logger.info("  -> No increase in values after splitting")
        return False
    
    # 2. Split values should be reasonably sized
    if avg_split < 2 or avg_split > 50:
        logger.info("  -> Split values outside reasonable length range")
        return False
    
    # 3. Splitting should not create too many unique values
    # We want the split ratio to be lower than the unsplit ratio
    # This indicates that splitting reveals repeated elements
    if ratio_split >= ratio_unsplit:
        logger.info("  -> Splitting increases uniqueness ratio")
        return False
    
    # 4. Check consistency of comma usage
    comma_values = [v for v in values if "," in v]
    comma_ratio = len(comma_values) / len(values)
    if comma_ratio < 0.3:  # At least 30% of values should contain commas
        logger.info("  -> Too few values contain commas")
        return False
    
    # 5. Check for consistent structure in comma-separated values
    comma_counts = [v.count(",") for v in comma_values]
    if max(comma_counts) - min(comma_counts) > 2:  # Allow some variance but not too much
        logger.info("  -> Too much variance in comma counts")
        return False
    
    logger.info("  -> Field qualifies for comma splitting")
    return True

def generate_canonical_entities(
    df: pd.DataFrame,
    full_schema: Dict[str, Dict[str, Any]],
    schema_database_type: str,
    entity_fields: List[Dict[str, str]],
    source_name: str,
    table_name: str,
    use_other_fields_as_metadata: bool = True,
    clean_field_names: bool = False,
    table_relationships: Optional[Dict[str, List[str]]] = None
) -> List[Dict[str, Any]]:
    """
    Generates canonical entity objects from the provided DataFrame and optional schema.
    Validates entity fields using database schema types if available, otherwise falls back to pandas dtype checks.
    
    Args:
        df: DataFrame to generate entities from
        full_schema: Schema dictionary
        schema_database_type: Type of database for schema validation
        entity_fields: List of entity fields with table and field names
        source_name: Name of the data source
        table_name: Name of the table
        use_other_fields_as_metadata: Whether to include non-entity fields as metadata
        clean_field_names: Whether to clean field names
        table_relationships: Optional dict mapping table names to their related tables
    """

    STRING_TYPE_MAP = {
        "mariadb": {"TEXT", "VARCHAR", "VARCHAR(255)"},
        "postgres": {"TEXT", "VARCHAR", "CHAR"},
        "sqlite": {"TEXT"},
        "bigquery": {"STRING"},
        "mysql": {"TEXT", "VARCHAR"},
    }

    def _canonical_entities_objects_equal(obj1: Dict[str, Any], obj2: Dict[str, Any]) -> bool:
        """Check if two canonical_entities objects are exactly equal in all their attributes."""
        if set(obj1.keys()) != set(obj2.keys()):
            return False
        return all(obj1[k] == obj2[k] for k in obj1.keys())

    canonical_entities_list: List[Dict[str, Any]] = []
    valid_entity_fields: List[tuple] = []

    if entity_fields:
        logger.info(f"Using provided entity_fields: {entity_fields}")
        string_types = STRING_TYPE_MAP.get(schema_database_type.lower(), set())

        # Create case-insensitive column mapping
        column_map = {col.lower(): col for col in df.columns}
        # logger.info(f"Column mapping (lowercase -> original): {column_map}")

        for entry in entity_fields:
            # Skip if table_name doesn't match
            if entry.get("table_name") != table_name:
                logger.info(f"Skipping field from table '{entry.get('table_name')}' (not matching current table '{table_name}').")
                continue

            fld = entry["field_name"]
            cleaned_field = _clean_column_name(fld)
            field_to_check = cleaned_field if clean_field_names else fld

            # Log all possible field names we're checking
            logger.info(f"Checking field '{fld}' with possible variations: original='{fld}', cleaned='{cleaned_field}', preferred='{field_to_check}'")
            logger.info(f"Available columns: {list(df.columns)}")

            # Try all versions (case-insensitive)
            field_lower = fld.lower()
            cleaned_lower = cleaned_field.lower()
            field_to_check_lower = field_to_check.lower()

            if (
                field_to_check_lower not in column_map and
                field_lower not in column_map and
                cleaned_lower not in column_map
            ):
                logger.info(f"Skipping '{fld}' (column not found in original or cleaned form).")
                continue

            # Find which version exists in the DataFrame (case-insensitive)
            if field_to_check_lower in column_map:
                actual_field = column_map[field_to_check_lower]
                logger.info(f"Found field using preferred name: '{field_to_check}' -> '{actual_field}'")
            elif field_lower in column_map:
                actual_field = column_map[field_lower]
                logger.info(f"Found field using original name: '{fld}' -> '{actual_field}'")
            else:
                actual_field = column_map[cleaned_lower]
                logger.info(f"Found field using cleaned name: '{cleaned_field}' -> '{actual_field}'")

            try:
                actual_type = full_schema[source_name][table_name][actual_field]["data_type"]
                if actual_type.upper() in string_types:
                    # Use the field name from the schema to ensure consistency
                    output_field = actual_field
                    valid_entity_fields.append((actual_field, output_field))
                    logger.info(f"Added field '{fld}' as '{output_field}' (using '{actual_field}' for data access)")
                else:
                    logger.info(
                        f"Skipping '{actual_field}' (data_type={actual_type} is not string-compatible for {schema_database_type})."
                    )
            except (KeyError, TypeError):
                if pd.api.types.is_string_dtype(df[actual_field]):
                    logger.warning(f"No schema for '{actual_field}' — using pandas dtype to allow it.")
                    # Use the field name from the schema to ensure consistency
                    output_field = actual_field
                    valid_entity_fields.append((actual_field, output_field))
                    logger.info(f"Added field '{fld}' as '{output_field}' (using '{actual_field}' for data access)")
                else:
                    logger.info(f"Skipping '{actual_field}' (pandas dtype not string-compatible).")

        if not valid_entity_fields:
            logger.info(
                "No valid entity_fields remain after filtering to string-compatible columns. "
                "Falling back to auto-extraction."
            )

        logger.info(f"Entity fields that will actually be used: {[f[1] for f in valid_entity_fields]}")

    if valid_entity_fields:
        # for each declared entity field, extract uniques + first metadata row
        for actual_field, output_field in valid_entity_fields:
            # Check if field should be split on commas using statistical analysis
            should_split = _should_split_on_commas(df[actual_field])
            logger.info(f"Field '{actual_field}' comma-split analysis complete: {should_split}")

            # 1) select just the entity column + any metadata columns
            cols = [actual_field]
            if use_other_fields_as_metadata:
                # keep all other columns so we can pull metadata later
                cols += [c for c in df.columns if c != actual_field]
            df_slice = df[cols]

            # 2) drop rows where the entity is null
            df_slice = df_slice.dropna(subset=[actual_field])

            # 3) normalize to strings, strip whitespace
            df_slice["_val_str"] = (
                df_slice[actual_field]
                .astype(str)
                .str.strip()
            )

            # 4) filter out blank/"nan"/"none"/"null"
            bad = {"", "nan", "none", "null"}
            df_slice = df_slice[~df_slice["_val_str"].str.lower().isin(bad)]

            # 5) handle comma-separated values if detected
            if should_split:
                # Split values and create a row for each part
                split_rows = []
                for _, row in df_slice.iterrows():
                    parts = [p.strip() for p in row["_val_str"].split(",")]
                    # Filter out empty parts or parts that are in the bad set
                    valid_parts = [p for p in parts if p and p.lower() not in bad]
                    for part in valid_parts:
                        new_row = row.copy()
                        new_row["_val_str"] = part
                        split_rows.append(new_row)
                if split_rows:
                    df_slice = pd.DataFrame(split_rows)

            # 6) drop duplicates on normalized value, keep the first row
            df_unique = df_slice.drop_duplicates(subset=["_val_str"], keep="first")

            # 7) build your entity objects from that tiny deduped slice
            for _, row in df_unique.iterrows():
                entity_obj: Dict[str, Any] = {
                    "_canonical_entity_": row[actual_field] if not should_split else row["_val_str"],
                    "_field_name_": output_field,
                    "_source_name_": source_name,
                    "_table_name_": table_name,
                    "_comma_separated_": should_split,  # New field indicating if this was split from a comma-separated value
                }

                if use_other_fields_as_metadata:
                    for other_col in cols:
                        if other_col in (actual_field, "_val_str"):
                            continue
                        val = row[other_col]
                        # skip null/empty, same checks as above
                        if pd.isna(val):
                            continue
                        s = str(val).strip()
                        if not s or s.lower() in bad:
                            continue
                        entity_obj[other_col] = val

                canonical_entities_list.append(entity_obj)

    return canonical_entities_list