DROP TABLE IF EXISTS Game CASCADE;
DROP TABLE IF EXISTS Login CASCADE;
DROP TABLE IF EXISTS Player CASCADE;
DROP TABLE IF EXISTS Item CASCADE;
DROP TABLE IF EXISTS Type_Item CASCADE;
DROP TABLE IF EXISTS Subtype_Item CASCADE;
DROP TABLE IF EXISTS Turn CASCADE;
DROP TABLE IF EXISTS Used CASCADE;

CREATE TABLE Game (
  game_id            SERIAL,
  game_width		INT,
  game_height		INT,
  game_time_max      INT,
  game_url_file		  BYTEA,
  game_name          VARCHAR,
  game_max_players    INT,
  game_status			VARCHAR,
  game_victory_rule    VARCHAR,
  game_fov_default		INT,
  game_victory_value INT,
  game_turn			INT,
  PRIMARY KEY (game_id)
);

CREATE TABLE Login (
  login_id       SERIAL,
  login_name    VARCHAR,
  login_password VARCHAR,
  login_isadmin    BOOLEAN NOT NULL,
  PRIMARY KEY (login_id)
);

CREATE TABLE Player (
  player_id      SERIAL,
  player_name  VARCHAR,
  player_join_game DATE,
  player_posx    INT,
  player_posy    INT,
  player_fov	INT,
  game_id        INT,
  login_id      INT,
  PRIMARY KEY (player_id)
);

CREATE TABLE Item (
  Item_id       SERIAL,
  game_id		INT,
  player_id     INT,
  type_Item_id    INT,
  subtype_Item_id INT,
  PRIMARY KEY (Item_id)
);

CREATE TABLE Type_Item (
  type_Item_id    SERIAL,
  type_Item_name VARCHAR,
  PRIMARY KEY (type_Item_id)
);

CREATE TABLE Subtype_Item (
  subtype_Item_id    SERIAL,
  subtype_Item_name VARCHAR(32) NOT NULL,
  PRIMARY KEY (subtype_Item_id)
);

CREATE TABLE Turn (
  turn_id          SERIAL,
  turn_move VARCHAR,
  game_id          INT,
  player_id        INT,
  PRIMARY KEY (turn_id)
);

CREATE TABLE Used (
  turn_id INT,
  Item_id INT,
  PRIMARY KEY (turn_id, Item_id)
);

ALTER TABLE Player ADD CONSTRAINT FK_Player_game_id FOREIGN KEY (game_id) REFERENCES Game(game_id);
ALTER TABLE Player ADD CONSTRAINT FK_Player_login_id FOREIGN KEY (login_id) REFERENCES Login(login_id);
ALTER TABLE Turn ADD CONSTRAINT FK_Turn_game_id FOREIGN KEY (game_id) REFERENCES Game(game_id);
ALTER TABLE Turn ADD CONSTRAINT FK_Turn_player_id FOREIGN KEY (player_id) REFERENCES Player(player_id);
ALTER TABLE Item ADD CONSTRAINT FK_Item_player_id FOREIGN KEY (player_id) REFERENCES Player(player_id);
ALTER TABLE Item ADD CONSTRAINT FK_Item_type_item_id FOREIGN KEY (type_item_id) REFERENCES Type_item(type_item_id);
ALTER TABLE Item ADD CONSTRAINT FK_Item_subtype_item_id FOREIGN KEY (subtype_item_id) REFERENCES Subtype_item(subtype_item_id);
ALTER TABLE Used ADD CONSTRAINT FK_Used_turn_id FOREIGN KEY (turn_id) REFERENCES Turn(turn_id);
ALTER TABLE Used ADD CONSTRAINT FK_Used_item_id FOREIGN KEY (item_id) REFERENCES Item(item_id);

INSERT INTO Login (login_name, login_password, login_isadmin) VALUES ('admin', md5('admin'), TRUE);
INSERT INTO Type_Item (type_Item_name) VALUES ('coin');
INSERT INTO Type_Item (type_Item_name) VALUES ('chest');
INSERT INTO Type_Item (type_Item_name) VALUES ('potion');