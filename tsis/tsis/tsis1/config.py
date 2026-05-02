db_config = {
    "host": "localhost",
    "database": "phonebook_db",
    "user": "postgres",
    "password": "supercool"
}

#docker run --name pb_database -e POSTGRES_PASSWORD=supercool -e POSTGRES_DB=phonebook_db -p 5432:5432 -d postgres
#docker exec -i pb_database psql -U postgres -d phonebook_db < schema.sql
#docker exec -i pb_database psql -U postgres -d phonebook_db < procedures.sql

