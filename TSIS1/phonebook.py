# =============================================================
# phonebook.py  —  PhoneBook Extended (TSIS 1)
#
# Builds on Practice 7 (CRUD, CSV import, console entry,
# query / update / delete) and Practice 8 (pattern-search
# function, upsert procedure, bulk-insert, pagination function,
# delete procedure).
#
# NEW in TSIS 1:
#   3.1  Extended data model  (groups, phones, email, birthday)
#   3.2  Filter by group, search by email, sort, page navigation
#   3.3  Export/import JSON, extended CSV import
#   3.4  Calls add_phone, move_to_group, search_contacts
# =============================================================

import csv
import json
from connect import get_connection


# ─────────────────────────────────────────────────────────────
# INTERNAL HELPERS
# ─────────────────────────────────────────────────────────────

# Reusable SELECT fragment that joins contacts ↔ groups ↔ phones
# and returns one row per contact (phones aggregated into a string).
_CONTACT_SELECT = """
    SELECT
        c.id,
        c.name,
        c.email,
        c.birthday,
        g.name          AS group_name,
        STRING_AGG(
            p.phone || ' (' || COALESCE(p.type, '?') || ')',
            ', '
        )               AS phones,
        c.created_at
    FROM contacts c
    LEFT JOIN groups g  ON c.group_id = g.id
    LEFT JOIN phones p  ON c.id = p.contact_id
"""

_CONTACT_GROUP = """
    GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
"""


def _print_contact(row):
    """Pretty-print one contact row returned by _CONTACT_SELECT."""
    cid, name, email, birthday, group, phones, created = row
    sep = "─" * 42
    print(f"  {sep}")
    print(f"  ID       : {cid}")
    print(f"  Name     : {name}")
    print(f"  Email    : {email    or '—'}")
    print(f"  Birthday : {birthday or '—'}")
    print(f"  Group    : {group    or '—'}")
    print(f"  Phones   : {phones   or '—'}")
    print(f"  Added    : {created}")


def _resolve_group(cur, group_name: str) -> int:
    """Return group.id for name; INSERT the group first if absent."""
    cur.execute("SELECT id FROM groups WHERE name ILIKE %s", (group_name,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        "INSERT INTO groups (name) VALUES (%s) RETURNING id",
        (group_name,)
    )
    return cur.fetchone()[0]


def _pick_group(cur):
    """Interactive prompt: list groups, return chosen group_id or None."""
    cur.execute("SELECT id, name FROM groups ORDER BY name")
    groups = cur.fetchall()
    print("  Available groups:")
    for gid, gname in groups:
        print(f"    • {gname}")
    choice = input("  Group (blank = none): ").strip()
    if not choice:
        return None
    return _resolve_group(cur, choice)


# ─────────────────────────────────────────────────────────────
# SCHEMA INITIALISATION
# ─────────────────────────────────────────────────────────────

def init_schema():
    """Execute schema.sql to create tables (safe to re-run)."""
    with open("schema.sql", encoding="utf-8") as f:
        sql = f.read()
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    print("  ✓ Schema initialised.")


def apply_procedures():
    """Execute procedures.sql to create/replace all stored objects."""
    with open("procedures.sql", encoding="utf-8") as f:
        sql = f.read()
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    print("  ✓ Procedures/functions applied.")


# ─────────────────────────────────────────────────────────────
# 3.1  EXTENDED CONTACT CRUD
# ─────────────────────────────────────────────────────────────

def add_contact_console():
    """
    Add a contact with full extended fields via interactive input.
    Allows adding multiple phone numbers in one session.
    """
    conn = get_connection()
    cur  = conn.cursor()

    name     = input("  Name            : ").strip()
    email    = input("  Email  (opt.)   : ").strip() or None
    birthday = input("  Birthday YYYY-MM-DD (opt.): ").strip() or None
    group_id = _pick_group(cur)

    cur.execute(
        """
        INSERT INTO contacts (name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """,
        (name, email, birthday, group_id)
    )
    contact_id = cur.fetchone()[0]
    conn.commit()

    # Add one or more phone numbers
    print("  Add phone numbers (press Enter with no number to stop):")
    while True:
        phone = input("    Number : ").strip()
        if not phone:
            break
        ptype = input("    Type   (home / work / mobile) : ").strip().lower()
        if ptype not in ("home", "work", "mobile"):
            print("    ⚠  Invalid type — defaulting to 'mobile'.")
            ptype = "mobile"
        cur.execute(
            "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
            (contact_id, phone, ptype)
        )
        conn.commit()
        print("    ✓ Phone added.")

    cur.close()
    conn.close()
    print(f"  ✓ Contact '{name}' saved (id={contact_id}).")


# ─────────────────────────────────────────────────────────────
# 3.2  ADVANCED SEARCH & FILTER
# ─────────────────────────────────────────────────────────────

def filter_by_group():
    """Show all contacts that belong to a chosen group."""
    conn = get_connection()
    cur  = conn.cursor()

    # List available groups first
    cur.execute("SELECT name FROM groups ORDER BY name")
    print("  Groups:", ", ".join(r[0] for r in cur.fetchall()))
    group_name = input("  Filter by group: ").strip()

    cur.execute(
        _CONTACT_SELECT +
        " WHERE g.name ILIKE %s " +
        _CONTACT_GROUP +
        " ORDER BY c.name",
        (group_name,)
    )
    rows = cur.fetchall()
    print(f"\n  ── {len(rows)} contact(s) in '{group_name}' ──")
    for row in rows:
        _print_contact(row)

    cur.close()
    conn.close()


def search_by_email():
    """Partial-match search on the email field."""
    conn = get_connection()
    cur  = conn.cursor()

    query = input("  Email search (e.g. 'gmail'): ").strip()
    cur.execute(
        _CONTACT_SELECT +
        " WHERE c.email ILIKE %s " +
        _CONTACT_GROUP +
        " ORDER BY c.name",
        ("%" + query + "%",)
    )
    rows = cur.fetchall()
    print(f"\n  ── {len(rows)} result(s) for email '{query}' ──")
    for row in rows:
        _print_contact(row)

    cur.close()
    conn.close()


def list_contacts_sorted():
    """List all contacts; user chooses the sort column."""
    SORT_OPTIONS = {
        "1": ("name",       "c.name"),
        "2": ("birthday",   "c.birthday NULLS LAST"),
        "3": ("date added", "c.created_at"),
    }
    print("  Sort by:  1) Name   2) Birthday   3) Date added")
    choice     = input("  Choice [1]: ").strip() or "1"
    label, col = SORT_OPTIONS.get(choice, SORT_OPTIONS["1"])

    conn = get_connection()
    cur  = conn.cursor()
    cur.execute(
        _CONTACT_SELECT +
        _CONTACT_GROUP +
        f" ORDER BY {col}"
    )
    rows = cur.fetchall()
    print(f"\n  ── {len(rows)} contact(s) sorted by {label} ──")
    for row in rows:
        _print_contact(row)

    cur.close()
    conn.close()


def paginated_navigation(page_size: int = 3):
    """
    Browse contacts page by page.
    Commands at the prompt:  next | prev | quit
    Internally calls the DB-side get_phonebook_paginated() from
    Practice 8, but the display uses the richer _CONTACT_SELECT view.
    """
    conn = get_connection()
    cur  = conn.cursor()
    page = 0

    while True:
        offset = page * page_size
        cur.execute(
            _CONTACT_SELECT +
            _CONTACT_GROUP +
            " ORDER BY c.name LIMIT %s OFFSET %s",
            (page_size, offset)
        )
        rows = cur.fetchall()

        if not rows:
            if page == 0:
                print("  (no contacts found)")
                break
            print("  ← Past the last page.")
            page -= 1
            continue

        print(f"\n  ══════════════  Page {page + 1}  ══════════════")
        for row in rows:
            _print_contact(row)

        cmd = input("\n  [next / prev / quit] → ").strip().lower()
        if cmd == "next":
            if len(rows) < page_size:
                print("  ← Already on the last page.")
            else:
                page += 1
        elif cmd == "prev":
            if page == 0:
                print("  ← Already on the first page.")
            else:
                page -= 1
        elif cmd == "quit":
            break
        else:
            print("  Unknown command — type  next / prev / quit.")

    cur.close()
    conn.close()


# ─────────────────────────────────────────────────────────────
# 3.3  IMPORT / EXPORT
# ─────────────────────────────────────────────────────────────

def export_to_json(file_path: str = "contacts_export.json"):
    """
    Write all contacts (name, email, birthday, group, phones list)
    to a JSON file.
    """
    conn = get_connection()
    cur  = conn.cursor()

    cur.execute("""
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday::TEXT,
            g.name      AS group_name,
            c.created_at::TEXT
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.name
    """)
    contacts = cur.fetchall()

    output = []
    for cid, name, email, birthday, group, created in contacts:
        cur.execute(
            "SELECT phone, type FROM phones WHERE contact_id = %s ORDER BY id",
            (cid,)
        )
        phones = [{"phone": ph, "type": tp} for ph, tp in cur.fetchall()]
        output.append({
            "name":       name,
            "email":      email,
            "birthday":   birthday,
            "group":      group,
            "phones":     phones,
            "created_at": created,
        })

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    cur.close()
    conn.close()
    print(f"  ✓ {len(output)} contact(s) exported → '{file_path}'.")


def import_from_json(file_path: str = "contacts_export.json"):
    """
    Read contacts from a JSON file and insert into the DB.
    On duplicate name the user chooses: [s]kip or [o]verwrite.
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            records = json.load(f)
    except FileNotFoundError:
        print(f"  ✗ File '{file_path}' not found.")
        return

    conn = get_connection()
    cur  = conn.cursor()
    inserted = overwritten = skipped = 0

    for rec in records:
        name = (rec.get("name") or "").strip()
        if not name:
            continue

        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        existing = cur.fetchone()

        if existing:
            ans = input(
                f"  Duplicate '{name}' — [s]kip / [o]verwrite? "
            ).strip().lower()
            if ans != "o":
                skipped += 1
                continue
            cid = existing[0]
            # Remove old phones before re-inserting
            cur.execute("DELETE FROM phones WHERE contact_id = %s", (cid,))
            group_id = _resolve_group(cur, rec["group"]) if rec.get("group") else None
            cur.execute(
                """
                UPDATE contacts
                SET    email=%s, birthday=%s, group_id=%s
                WHERE  id=%s
                """,
                (rec.get("email"), rec.get("birthday"), group_id, cid)
            )
            overwritten += 1
        else:
            group_id = _resolve_group(cur, rec["group"]) if rec.get("group") else None
            cur.execute(
                """
                INSERT INTO contacts (name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (name, rec.get("email"), rec.get("birthday"), group_id)
            )
            cid = cur.fetchone()[0]
            inserted += 1

        for ph in rec.get("phones", []):
            cur.execute(
                "INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s)",
                (cid, ph.get("phone"), ph.get("type"))
            )

    conn.commit()
    cur.close()
    conn.close()
    print(
        f"  ✓ Import done — "
        f"inserted: {inserted}, overwritten: {overwritten}, skipped: {skipped}."
    )


def import_from_csv_extended(file_path: str = "contacts.csv"):
    """
    Extended CSV importer (extends the Practice 7 version).

    Expected columns:
        name, phone, phone_type, email, birthday, group

    • name       – required
    • phone      – optional; phone_type defaults to 'mobile'
    • email      – optional
    • birthday   – optional, format YYYY-MM-DD
    • group      – optional; auto-created if it doesn't exist
    """
    conn = get_connection()
    cur  = conn.cursor()
    processed = 0

    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("name") or "").strip()
            if not name:
                continue

            email     = row.get("email",    "").strip() or None
            birthday  = row.get("birthday", "").strip() or None
            group_raw = row.get("group",    "").strip()
            group_id  = _resolve_group(cur, group_raw) if group_raw else None

            # Upsert contact record (mirrors Practice 8 upsert logic)
            cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
            existing = cur.fetchone()
            if existing:
                cid = existing[0]
                cur.execute(
                    """
                    UPDATE contacts
                    SET email=%s, birthday=%s, group_id=%s
                    WHERE id=%s
                    """,
                    (email, birthday, group_id, cid)
                )
            else:
                cur.execute(
                    """
                    INSERT INTO contacts (name, email, birthday, group_id)
                    VALUES (%s,%s,%s,%s)
                    RETURNING id
                    """,
                    (name, email, birthday, group_id)
                )
                cid = cur.fetchone()[0]

            # Handle phone + phone_type columns
            phone = row.get("phone", "").strip()
            ptype = row.get("phone_type", "mobile").strip().lower()
            if ptype not in ("home", "work", "mobile"):
                ptype = "mobile"
            if phone:
                cur.execute(
                    "INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s)",
                    (cid, phone, ptype)
                )

            processed += 1

    conn.commit()
    cur.close()
    conn.close()
    print(f"  ✓ CSV import done — {processed} row(s) processed.")


# ─────────────────────────────────────────────────────────────
# 3.4  STORED-PROCEDURE / FUNCTION CALLERS
# ─────────────────────────────────────────────────────────────

def call_add_phone():
    """
    Console wrapper for the add_phone(name, phone, type) procedure.
    Adds a new number to an already-existing contact.
    """
    conn = get_connection()
    cur  = conn.cursor()
    name  = input("  Contact name         : ").strip()
    phone = input("  Phone number         : ").strip()
    ptype = input("  Type (home/work/mobile): ").strip().lower()
    try:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
        conn.commit()
        print("  ✓ Phone added.")
    except Exception as e:
        conn.rollback()
        print(f"  ✗ {e}")
    finally:
        cur.close()
        conn.close()


def call_move_to_group():
    """
    Console wrapper for the move_to_group(name, group) procedure.
    Creates the group if it doesn't exist yet.
    """
    conn = get_connection()
    cur  = conn.cursor()
    name  = input("  Contact name : ").strip()
    group = input("  Target group : ").strip()
    try:
        cur.execute("CALL move_to_group(%s, %s)", (name, group))
        conn.commit()
        print(f"  ✓ '{name}' moved to group '{group}'.")
    except Exception as e:
        conn.rollback()
        print(f"  ✗ {e}")
    finally:
        cur.close()
        conn.close()


def call_search_contacts():
    """
    Console wrapper for search_contacts(query).
    Searches name, email, and every phone number in the phones table.
    """
    conn = get_connection()
    cur  = conn.cursor()
    query = input("  Search (name / email / phone): ").strip()
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()
    print(f"\n  ── {len(rows)} result(s) ──")
    for row in rows:
        _print_contact(row)
    cur.close()
    conn.close()


# ─────────────────────────────────────────────────────────────
# MAIN MENU
# ─────────────────────────────────────────────────────────────

_MENU = [
    # (key, label, function)
    ("1",  "Add contact (extended)",           add_contact_console),
    ("2",  "Filter contacts by group",         filter_by_group),
    ("3",  "Search contacts by email",         search_by_email),
    ("4",  "List contacts (sorted)",           list_contacts_sorted),
    ("5",  "Browse pages  [next/prev/quit]",   paginated_navigation),
    ("6",  "Export contacts → JSON",           export_to_json),
    ("7",  "Import contacts ← JSON",           import_from_json),
    ("8",  "Import contacts ← CSV (extended)", import_from_csv_extended),
    ("9",  "Add phone to existing contact",    call_add_phone),
    ("10", "Move contact to group",            call_move_to_group),
    ("11", "Search contacts (all fields)",     call_search_contacts),
    ("0",  "Exit",                             None),
]


def main():
    print()
    print("  ╔══════════════════════════════════════════╗")
    print("  ║   PhoneBook — Extended  (TSIS 1)         ║")
    print("  ╚══════════════════════════════════════════╝")

    while True:
        print()
        print("  ┌─ Menu ──────────────────────────────────┐")
        for key, label, _ in _MENU:
            print(f"  │  {key:>2}.  {label}")
        print("  └─────────────────────────────────────────┘")

        choice = input("  → ").strip()
        match  = next((fn for k, _, fn in _MENU if k == choice), "NOT_FOUND")

        if match == "NOT_FOUND":
            print("  ⚠  Invalid choice — try again.")
            continue
        if match is None:          # Exit
            print("  Goodbye!")
            break

        print()
        try:
            match()
        except KeyboardInterrupt:
            print("\n  (cancelled)")
        except Exception as exc:
            print(f"  ✗ Unexpected error: {exc}")


if __name__ == "__main__":
    main()
