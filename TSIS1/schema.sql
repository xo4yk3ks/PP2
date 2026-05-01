-- =============================================================
-- schema.sql  —  PhoneBook Extended (TSIS 1)
-- Run once on phonebook_db AFTER the original Practice 7 table
-- exists (or on a fresh database).
-- =============================================================

-- ── 1. Groups lookup ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Seed the four default categories
INSERT INTO groups (name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT DO NOTHING;

-- ── 2. Contacts  (replaces the flat Practice-7 phonebook) ────
--   If you are migrating an existing phonebook table, run:
--     INSERT INTO contacts (name) SELECT name FROM phonebook;
--   first, then drop the old table.
CREATE TABLE IF NOT EXISTS contacts (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(100),
    birthday   DATE,
    group_id   INTEGER REFERENCES groups(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- ── 3. Multiple phones per contact ───────────────────────────
CREATE TABLE IF NOT EXISTS phones (
    id         SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone      VARCHAR(20) NOT NULL,
    type       VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
);
