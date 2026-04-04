
-- functions.sql

-- 1. Pattern search function
CREATE OR REPLACE FUNCTION search_phonebook(pattern TEXT)
RETURNS TABLE(name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT p.name, p.phone
    FROM phonebook p
    WHERE p.name ILIKE '%' || pattern || '%'
       OR p.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- 2. Pagination function
CREATE OR REPLACE FUNCTION get_phonebook_paginated(limit_val INT, offset_val INT)
RETURNS TABLE(name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT p.name, p.phone
    FROM phonebook p
    LIMIT limit_val OFFSET offset_val;
END;
$$ LANGUAGE plpgsql;
