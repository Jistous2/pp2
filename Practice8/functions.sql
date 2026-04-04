CREATE OR REPLACE FUNCTION search_phonebook(p_pattern TEXT)
RETURNS TABLE (
    id INT,
    name VARCHAR,
    surname VARCHAR,
    phone VARCHAR
)
LANGUAGE SQL
AS $$
    SELECT pb.id, pb.name, pb.surname, pb.phone
    FROM phonebook AS pb
    WHERE pb.name ILIKE '%' || COALESCE(p_pattern, '') || '%'
       OR COALESCE(pb.surname, '') ILIKE '%' || COALESCE(p_pattern, '') || '%'
       OR pb.phone ILIKE '%' || COALESCE(p_pattern, '') || '%'
    ORDER BY pb.id;
$$;


CREATE OR REPLACE FUNCTION get_phonebook_page(p_limit INT, p_offset INT)
RETURNS TABLE (
    id INT,
    name VARCHAR,
    surname VARCHAR,
    phone VARCHAR
)
LANGUAGE SQL
AS $$
    SELECT pb.id, pb.name, pb.surname, pb.phone
    FROM phonebook AS pb
    ORDER BY pb.id
    LIMIT GREATEST(COALESCE(p_limit, 0), 0)
    OFFSET GREATEST(COALESCE(p_offset, 0), 0);
$$;
