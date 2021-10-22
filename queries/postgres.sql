CREATE DATABASE networks_project;

CREATE TABLE arp(
 interface VARCHAR (50) NOT NULL,
 mac VARCHAR (50) NOT NULL,
 ip VARCHAR (100) NOT NULL,
 age VARCHAR (200) NOT NULL
);

INSERT INTO arp(interface, mac, ip, age) VALUES("X", "X", "X", "X");

SELECT * FROM arp;

UPDATE arp SET interface = "X", ip = "X", age="X" WHERE mac = "X";

DELETE FROM arp WHERE mac = "X";