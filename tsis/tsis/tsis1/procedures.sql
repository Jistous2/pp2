-- 1. Добавление телефона
CREATE OR REPLACE PROCEDURE add_phone(p_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
AS $$
BEGIN
    INSERT INTO phones (contact_id, phone, type)
    SELECT id, p_phone, p_type FROM contacts WHERE first_name = p_name LIMIT 1;
END;
$$ LANGUAGE plpgsql;

-- 2. Смена группы (с созданием группы, если её нет)
CREATE OR REPLACE PROCEDURE move_to_group(p_name VARCHAR, p_group VARCHAR)
AS $$
DECLARE
    v_group_id INTEGER;
BEGIN
    INSERT INTO groups (name) VALUES (p_group) ON CONFLICT (name) DO NOTHING;
    SELECT id INTO v_group_id FROM groups WHERE name = p_group;
    UPDATE contacts SET group_id = v_group_id WHERE first_name = p_name;
END;
$$ LANGUAGE plpgsql;

-- 3. Расширенный поиск по всем полям
CREATE OR REPLACE FUNCTION search_contacts_full(p_query TEXT)
RETURNS TABLE(first_name VARCHAR, last_name VARCHAR, email VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT c.first_name, c.last_name, c.email, p.phone
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.first_name ILIKE '%' || p_query || '%'
       OR c.last_name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%';
END;
$$ LANGUAGE plpgsql;