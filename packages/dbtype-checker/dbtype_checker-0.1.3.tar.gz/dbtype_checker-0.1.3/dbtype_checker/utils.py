MAX_INFER_ROWS = 10_000  # Set global max sample size

def infer_type(column_name, sample_values):
    """
    Infers the data type of a column based on heuristics and sample inspection.
    Limits sample inspection to MAX_INFER_ROWS for performance.
    """

    name = column_name.lower()

    # Step 1: Heuristic based on column name
    if "id" in name or name.endswith("_no") or name == "roll_no":
        return int
    elif "date" in name:
        return str  # or datetime if needed
    elif "is_" in name or name.startswith("has_"):
        return bool
    elif any(kw in name for kw in ["age", "count", "num", "marks", "salary", "average"]):
        return int

    # Step 2: Limit values to MAX_INFER_ROWS
    values_to_check = sample_values[:MAX_INFER_ROWS]

    # Step 3: Value inspection
    int_count = float_count = bool_count = str_count = 0

    for value in values_to_check:
        if value is None:
            continue
        try:
            int(value)
            int_count += 1
            continue
        except (ValueError, TypeError):
            pass
        try:
            float(value)
            float_count += 1
            continue
        except (ValueError, TypeError):
            pass
        if str(value).strip().lower() in ['true', 'false', 'yes', 'no', '1', '0']:
            bool_count += 1
        else:
            str_count += 1

    type_counts = {
        int: int_count,
        float: float_count,
        bool: bool_count,
        str: str_count,
    }

    # Step 4: Choose type with the highest match count
    inferred_type = max(type_counts, key=type_counts.get)
    return inferred_type
