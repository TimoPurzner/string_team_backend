
CREATE TABLE user(
	id int PRIMARY KEY,
	name char(50),
	psid int,
	group_name char(50)
);


INSERT INTO user (id, name, psid, group_name) VALUES (0, "Fabian", 1337, "default");


SELECT * FROM user;

CREATE TABLE groupname(
	id int PRIMARY KEY,
	group_name char(50),
	valid_psid char(256)
);


INSERT INTO groupname (id, group_name, valid_psid) VALUES (0, "default", "{'psids':[56308]}");


SELECT * FROM groupname;


CREATE TABLE calendar(
	reservation_id int PRIMARY KEY,
	workspace_id int,
	user_id int,
	effective_from int,
	effective_to int
);


INSERT INTO calendar (reservation_id, workspace_id, user_id, effective_from, effective_to) VALUES (2, 0, 0, 0, 1);


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
