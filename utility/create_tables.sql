CREATE TABLE PA (
	stud_id integer PRIMARY KEY,
	nome text NOT NULL,
	cognome text NOT NULL
);

CREATE TABLE PA_INTERROGAZIONI (
	interr_id text PRIMARY KEY,
	stud_id integer,
	data text NOT NULL,
	voto text NOT NULL,
	FOREIGN KEY (stud_id) REFERENCES PA (stud_id)
	ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE PA_GIUSTIFICAZIONI (
	giust_id text PRIMARY KEY,
	stud_id integer NOT NULL,
	data text NOT NULL,
	FOREIGN KEY (stud_id) REFERENCES PA (stdu_id)
);

CREATE TABLE PM (
	stud_id integer PRIMARY KEY,
	nome text NOT NULL,
	cognome text NOT NULL
);

CREATE TABLE PM_INTERROGAZIONI (
	interr_id text PRIMARY KEY,
	stud_id integer NOT NULL,
	data text NOT NULL,
	voto text NOT NULL,
	FOREIGN KEY (stud_id) REFERENCES PM (stud_id)
);

CREATE TABLE PM_GIUSTIFICAZIONI (
	giust_id text PRIMARY KEY,
	stud_id integer NOT NULL,
	data text NOT NULL,
	FOREIGN KEY (stud_id) REFERENCES PM (stud_id)
);