drop TABLE player_status;
drop DATABASE db_status;

create DATABASE db_status;
CREATE TABLE player_status (
  id INT UNIQUE NOT NULL
);