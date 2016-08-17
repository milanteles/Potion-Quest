DROP TABLE 	IF EXISTS  Player 	CASCADE	;
DROP TABLE 	IF EXISTS  Items 	CASCADE	;
DROP TABLE 	IF EXISTS  Effect 	CASCADE	;
DROP TABLE 	IF EXISTS  Cell 	CASCADE	;
DROP TABLE 	IF EXISTS  Games 	CASCADE	;
DROP TABLE      IF EXISTS  Type_cell   CASCADE	;
DROP TABLE 	IF EXISTS  Turn 	CASCADE	;
DROP TABLE 	IF EXISTS  Type_item    CASCADE	;
DROP TABLE 	IF EXISTS  Users        CASCADE	;


CREATE TABLE Player(
        player_id     SERIAL PRIMARY KEY ,
        player_pseudo Varchar (255) ,
        player_pos_x  Int ,
        player_pos_y  Int ,
        player_pa     Int ,
        player_pv     Int ,
        game_id       Int ,
        user_id       Int 
);

CREATE TABLE Items(
        item_id   SERIAL PRIMARY KEY ,
        item_name  Varchar (255) ,
        player_id Int ,
        effect_id  Int ,
        cell_id   Int ,
        turn_id   Int ,
        typeI_id     Int ,
        item_id_1 Int ,
        game_id   Int 
);

CREATE TABLE Effect(
        effect_id        SERIAL PRIMARY KEY,
        effect_name       Varchar (255) ,
        effect_activable Bool
);

CREATE TABLE Cell(
        cell_id    SERIAL PRIMARY KEY ,
        cell_pos_x Int ,
        cell_pos_y Int ,
        game_id    Int ,
        typeI_id   Int ,
        item_id    Int
);

CREATE TABLE Games(
        game_id            SERIAL PRIMARY KEY ,
        game_height        Int ,
        game_width         Int ,
        game_turn          Int ,
        game_timeout       Int ,
        game_name          Varchar (255),
        game_file_bin      Varchar (255),
        game_max_player	   Int,
        game_pv_default    Int,
        game_status	   VarChar (50),
        game_victoryCond   Varchar (50),
        game_victory_value Int
);


CREATE TABLE Type_cell(
        typeC_id   SERIAL PRIMARY KEY ,
        typeC_name Varchar (255)  
);

CREATE TABLE Turn(
        turn_id    SERIAL PRIMARY KEY ,
        turn_pos_x Int ,
        turn_pos_y Int ,
        player_id  Int ,
        game_id    Int ,
        item_id    Int
);


CREATE TABLE Type_item(
        typeI_id      SERIAL PRIMARY KEY ,
        typeI_name     Varchar (25) ,
        typeI_url_img Varchar (255) 
);

CREATE TABLE Users(
        user_id       SERIAL PRIMARY KEY ,
        user_name     Varchar (25) ,
        user_password Varchar (255)
);


ALTER TABLE Player ADD CONSTRAINT FK_Player_game_id FOREIGN KEY (game_id) REFERENCES Games(game_id);
ALTER TABLE Items ADD CONSTRAINT FK_Items_player_id FOREIGN KEY (player_id) REFERENCES Player(player_id);
ALTER TABLE Items ADD CONSTRAINT FK_Items_effect_id FOREIGN KEY (effect_id) REFERENCES Effect(effect_id);
ALTER TABLE Items ADD CONSTRAINT FK_Items_cell_id FOREIGN KEY (cell_id) REFERENCES Cell(cell_id);
ALTER TABLE Items ADD CONSTRAINT FK_Items_turn_id FOREIGN KEY (turn_id) REFERENCES Turn(turn_id);
ALTER TABLE Items ADD CONSTRAINT FK_Items_typeI_id FOREIGN KEY (typeI_id) REFERENCES Type_item(typeI_id);
ALTER TABLE Items ADD CONSTRAINT FK_Items_item_id_1 FOREIGN KEY (item_id_1) REFERENCES Items(item_id);
ALTER TABLE Items ADD CONSTRAINT FK_Items_game_id FOREIGN KEY (game_id) REFERENCES Games(game_id);
ALTER TABLE Cell ADD CONSTRAINT FK_Cell_game_id FOREIGN KEY (game_id) REFERENCES Games(game_id);
ALTER TABLE Cell ADD CONSTRAINT FK_Cell_item_id FOREIGN KEY (item_id) REFERENCES Items(item_id);
ALTER TABLE Turn ADD CONSTRAINT FK_Turn_player_id FOREIGN KEY (player_id) REFERENCES Player(player_id);
ALTER TABLE Turn ADD CONSTRAINT FK_Turn_game_id FOREIGN KEY (game_id) REFERENCES Games(game_id);
ALTER TABLE Turn ADD CONSTRAINT FK_Turn_item_id FOREIGN KEY (item_id) REFERENCES Items(item_id);


INSERT INTO Games (game_height, game_width,game_turn,game_timeout,game_file_bin, game_name, game_max_player, game_pv_default, game_status, game_victoryCond, game_victory_value) VALUES (13,13,0,50,'/carte/1','The one',10,1, 'OPENED','coins', 10);

INSERT INTO Player (player_pseudo,player_pos_x, player_pos_y, player_pa, player_pv,game_id) VALUES ('Toto',0,0,1,1,1);
INSERT INTO Player (player_pseudo, player_pos_x, player_pos_y, player_pa, player_pv,game_id) VALUES ('Tata',5,5,1,1,1);

INSERT INTO Type_item (typeI_name, typeI_url_img) VALUES ('coin','/coins');
INSERT INTO Type_item (typeI_name, typeI_url_img) VALUES ('chest','/chest');
INSERT INTO Type_item (typeI_name, typeI_url_img) VALUES ('potion','/potions');

INSERT INTO Items (item_name,typeI_id,game_id) VALUES ('fov-increase',3,1);
INSERT INTO Items (item_name,typeI_id,game_id) VALUES ('coin',1,1);
INSERT INTO Items (item_name,typeI_id,game_id) VALUES ('coin',1,1);

INSERT INTO Users (user_name, user_password) VALUES ('Valentin', 'valentin');
INSERT INTO Users (user_name, user_password) VALUES ('user', 'password');



