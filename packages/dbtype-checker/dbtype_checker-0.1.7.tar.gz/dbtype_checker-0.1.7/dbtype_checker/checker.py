from .db import connect, get_table_names, fetch_table_data, close_connection
from .utils import infer_type


def check_column_types(db_url):
    engine, session = connect(db_url)
    tables = get_table_names(engine)

    mismatches = []

    for table in tables:
        records = fetch_table_data(session, table)
        if not records:
            continue

        # Collect sample values for each column
        column_samples = {}
        for record in records:
            for key, val in record.items():
                if key not in column_samples:
                    column_samples[key] = []
                if val is not None:
                    column_samples[key].append(val)

        for column_name, values in column_samples.items():
            # Infer type using pandas-based logic
            result = infer_type(column_name, values[:20])
            expected_type = result["final_inferred_type"]

            for row in records:
                val = row.get(column_name)
                if val is not None:
                    # Runtime-safe type check
                    if not is_type(val, expected_type):
                        mismatches.append((
                            table,
                            column_name,
                            type(val).__name__,
                            expected_type.__name__ if isinstance(expected_type, type) else str(expected_type)
                        ))
                        break  

    close_connection(session)
    return mismatches


def print_mismatches(db_url):
    mismatches = check_column_types(db_url)

    if mismatches:
        print("\nMismatched column types found:")
        for table, column, found, expected in mismatches:
            print(f" - {table}.{column}: found {found}, expected {expected}")
    else:
        print("No mismatches found.")


# Safe type check for str, int, float, bool, datetime
def is_type(value, expected_type):
    try:
        if expected_type == "datetime":
            import pandas as pd
            return pd.to_datetime(value, errors="coerce") is not pd.NaT
        return isinstance(value, expected_type)
    except:
        return False
