CREATE TABLE IF NOT EXISTS todo (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            item VARCHAR(255) NOT NULL
        ) ;

INSERT INTO todo (item)
VALUES ('Learn SQL'), ('Build a REST API'), ('Write Unit Tests.');

SELECT id, item
FROM todo;

UPDATE todo
SET item = 'Learn Advanced SQL'
WHERE id = '55bd7aee-a340-47fc-8bc2-76417648a3e6';

DELETE FROM todo
WHERE id = '55bd7aee-a340-47fc-8bc2-76417648a3e6';

