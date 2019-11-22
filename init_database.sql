
CREATE TABLE user(
	id int PRIMARY KEY,
	name char(50),
	psid int,
	group_name char(50)
);


INSERT INTO user (id, name, psid, group_name) VALUES (0, "Fabian", 1337, "default");


SELECT * FROM user;
