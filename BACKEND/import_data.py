import json
import re
from datetime import datetime
from pathlib import Path

import pandas as pd
from db import get_db_connection

# This is the exact filename currently in your DATA folder.
EXCEL_FILE = Path(__file__).resolve().parent.parent / "DATA" / "Smart_Campus_Complete_Systematic_Dataset (5) (2).xlsx"
BACKUP_DIR = Path(__file__).resolve().parent / "db_backups"

# Table names, column mappings, primary keys, and matching rules reflect the
# existing database schema. This script does not create, delete, or alter tables.
TABLE_CONFIG = [
    {
        "sheet": "FACULTY_ALL",
        "table": "faculty",
        "id": "faculty_id",
        "mapping": {
            "FACULTY NAME": "faculty_name",
            "DEPARTMENT": "department",
            "BUILDING": "building",
            "FLOOR": "floor",
            "ROOM NO.": "room_no",
            "E-MAIL": "email",
        },
        "match": ("faculty",),
    },
    {
        "sheet": "CLASSROOMS_ALL",
        "table": "classrooms",
        "id": "classroom_id",
        "mapping": {
            "ROOM NO.": "room_no",
            "BUILDING": "building",
            "FLOOR": "floor",
            "SOURCE": "source",
        },
        "match": ("classroom",),
    },
    {
        "sheet": "LABS_ALL",
        "table": "labs",
        "id": "lab_id",
        "mapping": {
            "LAB ROOM NO.": "lab_room_no",
            "BUILDING": "building",
            "FLOOR": "floor",
            "SOURCE": "source",
        },
        "match": ("lab",),
    },
    {
        "sheet": "OFFICES_ALL",
        "table": "offices",
        "id": "office_id",
        "mapping": {
            "OFFICE": "office",
            "BUILDING": "building",
            "FLOOR": "floor",
            "TIMING": "timing",
            "SERVICES": "services",
            "SOURCE": "source",
        },
        "match": ("office",),
    },
    {
        "sheet": "DEPARTMENTS_ALL",
        "table": "departments",
        "id": "department_id",
        "mapping": {
            "DEPARTMENT": "department",
            "HOD": "hod",
            "ROOM NO.": "room_no",
            "E-MAIL": "email",
            "SOURCE": "source",
        },
        "match": ("department",),
    },
    {
        "sheet": "ADMIN_SERVICES",
        "table": "admin_services",
        "id": "service_id",
        "mapping": {
            "BLOCK NAME": "block_name",
            "DEPARTMENT / ROOM": "department_room",
            "SERVICES PROVIDED": "services_provided",
            "SOURCE": "source",
        },
        "match": ("admin_service",),
    },
    {
        "sheet": "DT_SEATING_PLAN",
        "table": "dt_seating_plan",
        "id": "seating_id",
        "mapping": {
            "FLOOR": "floor",
            "FACULTY NAME": "faculty_name",
            "ROOM / CABIN NO.": "room_cabin_no",
            "SOURCE SHEET": "source_sheet",
            "SOURCE ROW": "source_row",
        },
        "match": ("seating",),
    },
]


def clean(value):
    """Convert Excel values to safe Python/MySQL values without turning NaN into text."""
    if pd.isna(value):
        return None
    if isinstance(value, str):
        value = value.strip()
        return value if value else None
    # Preserve integer values for integer columns such as SOURCE ROW.
    if hasattr(value, "item"):
        value = value.item()
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def norm(value):
    """Normalize text for matching without changing the stored value."""
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value).strip()).casefold()


def make_keys(kind, row):
    """Return one or more possible natural keys for matching a row."""
    if kind == "faculty":
        keys = []
        email = norm(row.get("email"))
        name, dept = norm(row.get("faculty_name")), norm(row.get("department"))
        if email:
            keys.append(("email", email))
        if name and dept:
            keys.append(("name_dept", name, dept))
        return keys

    if kind == "classroom":
        parts = tuple(norm(row.get(c)) for c in ("room_no", "building", "floor"))
    elif kind == "lab":
        parts = tuple(norm(row.get(c)) for c in ("lab_room_no", "building", "floor"))
    elif kind == "office":
        parts = tuple(norm(row.get(c)) for c in ("office", "building", "floor"))
    elif kind == "department":
        name = norm(row.get("department"))
        return [("department", name)] if name else []
    elif kind == "admin_service":
        parts = tuple(norm(row.get(c)) for c in
                      ("block_name", "department_room", "services_provided"))
    elif kind == "seating":
        source_sheet = norm(row.get("source_sheet"))
        source_row = norm(row.get("source_row"))
        if source_sheet and source_row:
            return [("source", source_sheet, source_row)]
        parts = tuple(norm(row.get(c)) for c in
                      ("floor", "faculty_name", "room_cabin_no"))
    else:
        return []

    return [parts] if all(parts) else []


def json_safe(value):
    return str(value) if value is not None else None


def create_backup(connection):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"campus_db_before_merge_{stamp}.json"
    backup = {}

    cursor = connection.cursor(dictionary=True)
    for config in TABLE_CONFIG:
        table = config["table"]
        cursor.execute(f"SELECT * FROM `{table}`")
        backup[table] = cursor.fetchall()
    cursor.close()
    connection.commit()

    with backup_path.open("w", encoding="utf-8") as file:
        json.dump(backup, file, ensure_ascii=False, indent=2, default=json_safe)

    return backup_path


def merge_sheet(connection, config):
    df = pd.read_excel(EXCEL_FILE, sheet_name=config["sheet"])
    df.columns = [str(col).strip() for col in df.columns]

    missing = [col for col in config["mapping"] if col not in df.columns]
    if missing:
        raise ValueError(
            f"{config['sheet']} is missing expected Excel columns: {missing}"
        )

    table = config["table"]
    id_column = config["id"]
    mapping = config["mapping"]
    kind = config["match"][0]

    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM `{table}`")
    existing_rows = cursor.fetchall()
    cursor.close()

    by_key = {}
    for existing in existing_rows:
        for key in make_keys(kind, existing):
            if key not in by_key:
                by_key[key] = existing

    inserted = updated = unchanged = skipped = 0
    cursor = connection.cursor()

    target_columns = list(mapping.values())
    placeholders = ", ".join(["%s"] * len(target_columns))
    column_sql = ", ".join(f"`{c}`" for c in target_columns)
    insert_sql = f"INSERT INTO `{table}` ({column_sql}) VALUES ({placeholders})"

    for _, excel_row in df.iterrows():
        incoming = {
            mysql_col: clean(excel_row[excel_col])
            for excel_col, mysql_col in mapping.items()
        }

        # Don't create records with no usable identity.
        keys = make_keys(kind, incoming)
        if not keys:
            skipped += 1
            continue

        existing = next((by_key[key] for key in keys if key in by_key), None)
        key = keys[0]
        if existing is None:
            cursor.execute(
                insert_sql,
                tuple(incoming[col] for col in target_columns)
            )
            inserted += 1
            # Record inserted ID so duplicate rows in the same workbook don't insert again.
            new_id = cursor.lastrowid
            saved = dict(incoming)
            saved[id_column] = new_id
            for saved_key in make_keys(kind, saved):
                by_key[saved_key] = saved
            continue

        # Update only fields with non-empty incoming values.
        # Empty Excel cells never erase useful values already in MySQL.
        changes = {
            col: value for col, value in incoming.items()
            if value is not None and str(value).strip() != ""
            and norm(existing.get(col)) != norm(value)
        }

        if not changes:
            unchanged += 1
            continue

        assignments = ", ".join(f"`{col}` = %s" for col in changes)
        values = list(changes.values()) + [existing[id_column]]
        cursor.execute(
            f"UPDATE `{table}` SET {assignments} WHERE `{id_column}` = %s",
            tuple(values)
        )
        existing.update(changes)
        updated += 1

    cursor.close()
    print(
        f"{config['sheet']} -> {table}: "
        f"{inserted} inserted, {updated} updated, "
        f"{unchanged} unchanged, {skipped} skipped"
    )


def main():
    print("=" * 55)
    print("SMART CAMPUS SAFE DATA MERGE")
    print("=" * 55)

    if not EXCEL_FILE.exists():
        raise FileNotFoundError(
            f"Excel file not found:\n{EXCEL_FILE}\n"
            "Check the filename inside your project's DATA folder."
        )

    # Validate workbook sheets before opening a database connection.
    workbook = pd.ExcelFile(EXCEL_FILE)
    required_sheets = [item["sheet"] for item in TABLE_CONFIG]
    missing_sheets = [sheet for sheet in required_sheets if sheet not in workbook.sheet_names]
    if missing_sheets:
        raise ValueError(f"Workbook is missing required sheets: {missing_sheets}")

    connection = get_db_connection()
    print("MySQL connection successful.")

    try:
        backup_path = create_backup(connection)
        print(f"Backup created: {backup_path}")

        connection.start_transaction()
        try:
            for config in TABLE_CONFIG:
                merge_sheet(connection, config)
            connection.commit()
            print("\nMerge completed successfully. Existing rows were not deleted.")
        except Exception:
            connection.rollback()
            raise
    finally:
        connection.close()

    print("=" * 55)


if __name__ == "__main__":
    main()