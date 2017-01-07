DROP DATABASE IF EXISTS db_status;
DROP USER IF EXISTS 's_user';

CREATE USER 's_user' IDENTIFIED BY 'ThePasswordOfSUser';

CREATE DATABASE db_status;
USE db_status;
CREATE TABLE player_status (
  id INT PRIMARY KEY
);


GRANT SELECT, INSERT ON player_status TO s_user;