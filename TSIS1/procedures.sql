-- =============================================================
-- procedures.sql  —  PhoneBook Extended (TSIS 1)
--
-- Section A  ►  Practice 8 procedures/functions adapted to the
--               new schema (contacts + phones tables).
--               Logic is unchanged; table names updated.
--
-- Section B  ►  TSIS 1 new server-side objects:
--               • add_phone
--               • move_to_group
--               • search_contacts  (extended)
-- =============================================================


-- ─────────────────────────────────────────────────────────────
-- SECTION A  —  Practice 8 (adapted, not re-implemented)
-- ─────────────────────────────────────────────────────────────

-- Upsert: insert new contact or update its first phone number
CREATE OR REPLACE PROCEDURE upsert_user(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql AS $$
DECLARE
    v_id INTEGER;
BEGIN
    SELECT id INTO v_id FROM contacts WHERE name = p_name;

    IF v_id IS NOT NULL THEN
        -- update the earliest phone entry for this contact
        UPDATE phones
        SET    phone = p_phone
        WHERE  contact_id = v_id
          AND  id = (SELECT MIN(id) FROM phones WHERE contact_id = v_id);
    ELSE
        INSERT INTO contacts (name) VALUES (p_name) RETURNING id INTO v_id;
        INSERT INTO phones   (contact_id, phone, type)
        VALUES (v_id, p_phone, 'mobile');
    END IF;
END;
$$;


-- Bulk insert with phone-format validation
CREATE OR REPLACE PROCEDURE bulk_insert_users(
    names      TEXT[],
    phones_arr TEXT[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP
        IF phones_arr[i] ~ '^\+?[0-9]{10,15}$' THEN
            CALL upsert_user(names[i], phones_arr[i]);
        ELSE
            RAISE NOTICE 'Skipped — invalid phone: % (user: %)',
                          phones_arr[i], names[i];
        END IF;
    END LOOP;
END;
$$;


-- Delete contact by name OR phone number
CREATE OR REPLACE PROCEDURE delete_user(p_value TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts
    WHERE  name = p_value
       OR  id IN (
               SELECT contact_id FROM phones WHERE phone = p_value
           );
END;
$$;


-- Pattern-search across name and phone (Practice 8 signature kept)
CREATE OR REPLACE FUNCTION search_phonebook(pattern TEXT)
RETURNS TABLE(contact_name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT c.name::TEXT, p.phone::TEXT
    FROM   contacts c
    JOIN   phones   p ON c.id = p.contact_id
    WHERE  c.name  ILIKE '%' || pattern || '%'
       OR  p.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;


-- Paginated listing (Practice 8 signature kept)
CREATE OR REPLACE FUNCTION get_phonebook_paginated(
    limit_val  INT,
    offset_val INT
)
RETURNS TABLE(contact_name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.name::TEXT,
        STRING_AGG(p.phone, ', ')::TEXT
    FROM   contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    GROUP  BY c.name
    ORDER  BY c.name
    LIMIT  limit_val
    OFFSET offset_val;
END;
$$ LANGUAGE plpgsql;


-- ─────────────────────────────────────────────────────────────
-- SECTION B  —  TSIS 1  new server-side objects
-- ─────────────────────────────────────────────────────────────

-- 1. Add a phone number to an existing contact
--    Raises an exception if the contact is not found.
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    SELECT id INTO v_contact_id
    FROM   contacts
    WHERE  name = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found.', p_contact_name;
    END IF;

    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Invalid type "%". Use: home | work | mobile.', p_type;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;


-- 2. Move a contact to a group; create the group if it doesn't exist.
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id   INTEGER;
    v_contact_id INTEGER;
BEGIN
    -- Resolve or create group
    SELECT id INTO v_group_id
    FROM   groups
    WHERE  name = p_group_name;

    IF v_group_id IS NULL THEN
        INSERT INTO groups (name) VALUES (p_group_name)
        RETURNING id INTO v_group_id;
        RAISE NOTICE 'Created new group "%".', p_group_name;
    END IF;

    -- Resolve contact
    SELECT id INTO v_contact_id
    FROM   contacts
    WHERE  name = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found.', p_contact_name;
    END IF;

    UPDATE contacts
    SET    group_id = v_group_id
    WHERE  id = v_contact_id;
END;
$$;


-- 3. Extended full-text search: name + email + ALL phone numbers
--    Returns the same row shape as the Python CONTACTS_VIEW query
--    so results can be printed with print_contact_row().
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    id         INTEGER,
    name       TEXT,
    email      TEXT,
    birthday   DATE,
    group_name TEXT,
    phones     TEXT,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.name::TEXT,
        c.email::TEXT,
        c.birthday,
        g.name::TEXT                                              AS group_name,
        STRING_AGG(
            ph.phone || ' (' || COALESCE(ph.type, '?') || ')',
            ', '
        )::TEXT                                                   AS phones,
        c.created_at
    FROM   contacts c
    LEFT JOIN groups  g  ON c.group_id = g.id
    LEFT JOIN phones  ph ON c.id = ph.contact_id
    WHERE
           c.name  ILIKE '%' || p_query || '%'
        OR c.email ILIKE '%' || p_query || '%'
        OR ph.phone ILIKE '%' || p_query || '%'
    GROUP  BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
    ORDER  BY c.name;
END;
$$ LANGUAGE plpgsql;
