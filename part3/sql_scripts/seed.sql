INSERT INTO "user" (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$kqKDYkZJ9G8AJF5U6/c0UOIo4VnyOJY6pU6TjAYXeU8kWcQoYHLzq', -- bcrypt hash de 'admin1234'
    TRUE
);

INSERT INTO amenity (id, name) VALUES
    ('e1a7b313-f9e4-4cb3-b982-5e638a6b91a1', 'WiFi'),
    ('f9db6a9c-cf77-4ac2-9029-4de2fffb0552', 'Swimming Pool'),
    ('b3a9a8dc-89e3-4128-a3be-2c8a9f1ecb90', 'Air Conditioning');
