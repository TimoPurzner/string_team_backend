
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
INSERT INTO groupname (id, group_name, valid_psid) VALUES (1, "all", "{'psids':[56308, 61671, 56309, 61719, 61718, 61717, 61716, 61715, 61714, 61720]}");


SELECT * FROM groupname;


CREATE TABLE calendar(
	reservation_id int PRIMARY KEY,
	workspace_id int,
	user_id int,
	effective_from int,
	effective_to int,
    valid int
);


INSERT INTO calendar (reservation_id, workspace_id, user_id, effective_from, effective_to, valid) 
VALUES 
(0, 56308, 0, 1574502110, 1574502140, 1),
(1, 56308, 0, 1574518546, 1574593391, 1);


SELECT * FROM calendar;

CREATE TABLE workspace (
            id int PRIMARY KEY,
            xml_id int,
            occupied bool,
            occupied_preliminary bool,
            latitude int,
            longitude int,
            level int,
            ignored bool,
            last_change int,
            last_contact int,
            reserved bool,
            has_display bool,
            parking_lot_id int,
            workspace_name char(50)
);

INSERT INTO workspace(id,xml_id,occupied,occupied_preliminary,latitude,longitude,level,ignored,last_change,last_contact,reserved,has_display,parking_lot_id,workspace_name) VALUES 
(56308, 0, false, false, 0, 0, 0, false, 0, 0, false, false, 0, "Pikochu"),
(61671, 0, false, false, 0, 0, 0, false, 0, 0, false, false, 0, "Bisasom"),
(56309, 0, false, false, 0, 0, 0, false, 0, 0, false, false, 0, "Schiggo"),
(61719, 0, false, false, 0, 0, 0, false, 0, 0, false, false, 0, "Glumonda"),
(61718, 0, false, false, 0, 0, 0, false, 0, 0, false, false, 0, "Zeptos"),
(61717, 0, false, false, 0, 0, 0, false, 0, 0, false, false, 0, "Arktus"),
(61716, 0, false, false, 0, 0, 0, false, 0, 0, false, false, 0, "Moew"),
(61715, 0, false, false, 0, 0, 0, false, 0, 0, false, false, 0, "MoewThree"),
(61714, 0, false, false, 0, 0, 0, false, 0, 0, false, false, 0, "Lovados"),
(61720, 0, false, false, 0, 0, 0, false, 0, 0, false, false, 0, "Evali");


SELECT * FROM workspace;
