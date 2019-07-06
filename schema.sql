BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `profiles` (
	`username`	TEXT,
	`password`	TEXT,
	`client_id`	TEXT,
	`client_secret`	TEXT,
	`proxy`	TEXT,
  `pid`	INTEGER ,
	`running`	INTEGER
);
COMMIT;
