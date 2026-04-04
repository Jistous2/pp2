CREATE OR REPLACE PROCEDURE upsert_user(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE name = p_name;
    ELSE
        INSERT INTO phonebook (name, surname, phone)
        VALUES (p_name, NULL, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE upsert_many_users(
    IN p_names TEXT[],
    IN p_phones TEXT[],
    INOUT p_incorrect_data TEXT[] DEFAULT ARRAY[]::TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
    v_name TEXT;
    v_phone TEXT;
BEGIN
    IF COALESCE(array_length(p_names, 1), 0) <> COALESCE(array_length(p_phones, 1), 0) THEN
        RAISE EXCEPTION 'p_names and p_phones must have the same length';
    END IF;

    p_incorrect_data := ARRAY[]::TEXT[];

    FOR i IN 1..COALESCE(array_length(p_names, 1), 0) LOOP
        v_name := btrim(p_names[i]);
        v_phone := btrim(p_phones[i]);

        IF v_name = '' OR v_phone !~ '^\+?[0-9]{10,15}$' THEN
            p_incorrect_data := array_append(
                p_incorrect_data,
                format('name="%s", phone="%s"', COALESCE(v_name, 'NULL'), COALESCE(v_phone, 'NULL'))
            );
        ELSE
            IF EXISTS (SELECT 1 FROM phonebook WHERE name = v_name) THEN
                UPDATE phonebook
                SET phone = v_phone
                WHERE name = v_name;
            ELSE
                INSERT INTO phonebook (name, surname, phone)
                VALUES (v_name, NULL, v_phone);
            END IF;
        END IF;
    END LOOP;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_from_phonebook(
    IN p_username VARCHAR DEFAULT NULL,
    IN p_phone VARCHAR DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_username IS NULL AND p_phone IS NULL THEN
        RAISE EXCEPTION 'Pass username or phone for deletion';
    END IF;

    DELETE FROM phonebook
    WHERE (p_username IS NOT NULL AND name = p_username)
       OR (p_phone IS NOT NULL AND phone = p_phone);
END;
$$;
