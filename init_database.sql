
CREATE TABLE user(
	id int PRIMARY KEY,
	name char(50),
	psid int,
	group_name char(50)
);


INSERT INTO user (id, name, psid, group_name) VALUES (0, "Fred", 56308, "all");
INSERT INTO user (id, name, psid, group_name) VALUES (1, "Timo", 61671, "all");
INSERT INTO user (id, name, psid, group_name) VALUES (2, "Anne", 61720, "all");
INSERT INTO user (id, name, psid, group_name) VALUES (3, "Fabian", 61718, "all");
INSERT INTO user (id, name, psid, group_name) VALUES (4, "Pascal", 61719, "all");

SELECT * FROM user;

CREATE TABLE groupname(
	id int PRIMARY KEY,
	group_name char(50),
	valid_psid char(256)
);


INSERT INTO groupname (id, group_name, valid_psid) VALUES (0, "default", "{'psids':[56308]}");
INSERT INTO groupname (id, group_name, valid_psid) VALUES (1, "all", "{'psids':[56308]}");


SELECT * FROM groupname;


CREATE TABLE calendar(
	reservation_id int PRIMARY KEY,
	workspace_id int,
	user_id int,
	effective_from int,
	effective_to int
);


INSERT INTO calendar (reservation_id, workspace_id, user_id, effective_from, effective_to) VALUES (0, 56308, 0, 1574502110, 1574502710);


SELECT * FROM calendar;

CREATE TABLE workspace (
            id,
            xml_id,
            occupied,
            occupied_preliminary,
            latitude,
            longitude,
            level,
            ignored,
            last_change,
            last_contact,
            reserved,
            has_display,
            parking_lot_id,
            workspace_name
);
