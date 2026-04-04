
-- procedures.sql

-- 1. Upsert procedure
CREATE OR REPLACE PROCEDURE upsert_user(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO phonebook(name, phone) VALUES (p_name, p_phone);
    END IF;
END;
$$;

-- 2. Bulk insert with validation
CREATE OR REPLACE PROCEDURE bulk_insert_users(names TEXT[], phones TEXT[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP
        IF phones[i] ~ '^\+?[0-9]{10,15}$' THEN
            CALL upsert_user(names[i], phones[i]);
        ELSE
            RAISE NOTICE 'Invalid phone: % for user %', phones[i], names[i];
        END IF;
    END LOOP;
END;
$$;

-- 3. Delete procedure
CREATE OR REPLACE PROCEDURE delete_user(p_value TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = p_value OR phone = p_value;
END;
$$;
