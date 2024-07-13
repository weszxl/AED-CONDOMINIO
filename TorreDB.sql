SHOW DATABASES;

CREATE DATABASE torreDB;
USE torreDB;

SELECT * FROM apartamentos;

CREATE TABLE apartamentos (
    id INT PRIMARY KEY,
    numero VARCHAR(10),
    vaga INT
);

INSERT INTO apartamentos (id, numero, vaga) VALUES
(1, '101', 1),
(2, '102', 2),
(3, '103', 3),
(4, '104', 4),
(5, '105', 5),
(6, '106', 6),
(7, '107', 7),
(8, '108', 8),
(9, '109', 9),
(10, '110', 10);

