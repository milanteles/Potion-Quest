# -*- coding: utf-8 -*-
from flask import Flask, request, make_response
import json, os, psycopg2, urlparse
from db import Db 

app = Flask(__name__)
app.debug = True

##################################################################

@app.route('/debug/db/reset')
def route_dbinit():
  	"""Cette route sert à initialiser (ou nettoyer) la base de données."""
  	db = Db()
  	db.executeFile("database_resetb.sql")
  	db.close()
  	return "Done."

#-----------------------------------------------------------------

@app.route('/games')
def games_fetchall():
  	db = Db()
	game = db.select('SELECT * FROM Games')
	returned=[]
	for data in game :
		playerOnGame = []
		
		playersList = db.select('SELECT player_pseudo AS name FROM Player WHERE game_id = %(id)s',{
			'id' : data['game_id']
		})
		nbCoin = db.select('SELECT COUNT(*) FROM Items WHERE typeI_id = 1 AND game_id = %(id)s',{
			'id' : data['game_id']
		})
		nbChest = db.select('SELECT COUNT(*) FROM Items WHERE typeI_id = 2 AND game_id = %(id)s',{
			'id' : data['game_id']
		})
		nbPotion = db.select('SELECT COUNT(*) FROM Items WHERE typeI_id = 3 AND game_id = %(id)s',{
			'id' : data['game_id']
		})
		
		print playersList
		
		for player in playersList :
			playerOnGame.append(player['name'])
			print playerOnGame
		
		current = data['game_turn'] % len(playerOnGame)
		
		if (current == 0) :
			current = len(playerOnGame)
		
		result = {'id' : data['game_id'],'name' : data['game_name'], 'width' : data['game_width'], 'height' : data['game_height'], 'players' : playerOnGame, 'maxPlayers' : data['game_max_player'], 'fovDefault' : data['game_pv_default'], 'turn' : data['game_turn'], 'status' : data['game_status'] ,'nbItems' : { 'coins' : nbCoin[0]['count'], 'potions' : nbPotion[0]['count'], 'chest' : nbChest[0]['count']}, 'victoryOn' : {'rule' : data['game_victorycond'], 'value' : data['game_victory_value']}, 'currentPlayer' : playersList[current-1]['name']}
		returned.append(result)
	
	resp = make_response(json.dumps(returned), 200)
	resp.mimetype = 'application/json'
	return resp

#-----------------------------------------------------------------

@app.route('/games', methods=['POST'])
def games_create():
	db=Db()
	data = request.get_json()
	
	new = db.select('''INSERT INTO Games (game_height, game_width, game_turn,game_timeout,game_file_bin,game_name,game_max_player, game_victorycond, game_victory_value, game_pv_default, game_status) 
			   VALUES (%(height)s, %(width)s, %(turn)s, %(timeout)s, %(bin)s,%(name)s,%(max_playeur)s,%(victoryCond)s,%(victoryValue)s, %(pvDefault)s, %(status)s) RETURNING game_id''',{
			   'height' : data['height'],
			   'width' : data['width'],
			   'turn' : 0,
			   'timeout' : data['timeout'],
			   'bin' : '0101010111011011011011011010000100100010010110110100',
			   'name' : data['name'],
			   'max_playeur' : data['maxPlayers'],
			   'victoryCond' : data['victoryOn']['rule'],
			   'victoryValue' : data['victoryOn']['value'],
			   'pvDefault' : data['fovDefault'],
			   'status' : 'OPENED'
			   })
	
	db.execute('INSERT INTO Player (player_pseudo,game_id) VALUES (%(name)s, %(game_id)s)',{
		'name' : 'toto',
		'game_id' : new[0]['game_id']
	})
	
	for i in range(0,data['nbItems']['coins']) :
		db.execute('INSERT INTO Items (item_name, game_id, typeI_id) VALUES (%(name)s,%(game_id)s,1 )',{
			'name' : 'coin',
			'game_id' : new[0]['game_id']
		})
	for i in range(0,data['nbItems']['chest']) :
		db.execute('INSERT INTO Items (item_name, game_id, typeI_id) VALUES (%(name)s,%(game_id)s,2 )',{
			'name' : 'chest',
			'game_id' : new[0]['game_id']
		})
	for i in range(0,data['nbItems']['potions']) :
		db.execute('INSERT INTO Items (item_name, game_id, typeI_id) VALUES (%(name)s,%(game_id)s,3 )',{
			'name' : 'potion',
			'game_id' : new[0]['game_id']
		})		
	db.close()
	resp = make_response('OK', 201)
	resp.mimetype = 'application/json'
	return resp

#-----------------------------------------------------------------

@app.route('/user')
def get_user():
	db=Db()
	
	result = db.select('SELECT user_name AS username, user_password AS password FROM users')
	
	db.close()
	resp = make_response(json.dumps(result),200)
	return resp
	
#-----------------------------------------------------------------

@app.route('/user', methods=['POST'])
def create_user():
	db=Db()
	data = request.get_json()
	
	
	db.execute('INSERT INTO Users (user_name, user_password) VALUES (%(username)s , %(password)s)',{
		'username' : data['username'],
		'password' : data['password']
	
	})
	db.close()
	resp = make_response('Compte créé avec succès',200)
	return resp
#-----------------------------------------------------------------

@app.route('/games/<int:id>/players', methods=['GET'])
def get_playeur_by_games(id):
	db = Db()
	
	result =db.select('SELECT player_id, player_pseudo as player FROM Player WHERE game_id = %(id)s',{
		'id' : id
	})
	db.close()
	resp = make_response(json.dumps(result),200)
	return resp

#-----------------------------------------------------------------

@app.route('/game/<int:gameid>')
def games_fetchallbyid(gameid):
  	db = Db()
	game = db.select('SELECT * FROM Games WHERE game_id = %(gameid)s',{
  			"gameid":gameid
  		})
	
	for data in game :
		playerOnGame = []
		
		playersList = db.select('SELECT player_pseudo AS name FROM Player WHERE game_id = %(gameid)s',{
			'gameid' : data['game_id']
		})
		nbCoin = db.select('SELECT COUNT(*) FROM Items WHERE typeI_id = 1 AND game_id = %(gameid)s',{
			'gameid' : data['game_id']
		})
		nbChest = db.select('SELECT COUNT(*) FROM Items WHERE typeI_id = 2 AND game_id = %(gameid)s',{
			'gameid' : data['game_id']
		})
		nbPotion = db.select('SELECT COUNT(*) FROM Items WHERE typeI_id = 3 AND game_id = %(gameid)s',{
			'gameid' : data['game_id']
		})
		
		print playersList
		
		for player in playersList :
			playerOnGame.append(player['name'])
			print playerOnGame
		
		current = data['game_turn'] % len(playerOnGame)
		
		if (current == 0) :
			current = len(playerOnGame)
		
		result = {'id' : data['game_id'],'name' : data['game_name'], 'width' : data['game_width'], 'height' : data['game_height'], 'players' : playerOnGame, 'maxPlayers' : data['game_max_player'], 'fovDefault' : data['game_pv_default'], 'turn' : data['game_turn'], 'status' : data['game_status'] ,'nbItems' : { 'coins' : nbCoin[0]['count'], 'potions' : nbPotion[0]['count'], 'chest' : nbChest[0]['count']}, 'victoryOn' : {'rule' : data['game_victorycond'], 'value' : data['game_victory_value']}, 'currentPlayer' : playersList[current-1]['name']}
		
	
	resp = make_response(json.dumps(result), 200)
	resp.mimetype = 'application/json'
	return resp
#-----------------------------------------------------------------


@app.route('/games/<int:id>/players', methods=['POST'])
def connect_to_game(id):
	db = Db()
	data = request.get_json()
	
	db.execute('''INSERT INTO Player (player_pseudo, player_pv, game_id, user_id) 
			VALUES (%(pseudo)s, %(pv)s, %(game_id)s, %(user_id)s) ''',{
			'pseudo' : data['username'],
			'pv' : 1,
			'user_id' : 1,
			'game_id': id
			})
	db.close()
	resp = make_response('OK',200)
	return resp

#-----------------------------------------------------------------
@app.route('/users-auth', methods=['GET'])
def authentification():	
	db = Db()
	if not(request.authorization):
		resp = make_response("Credentials required", 401)
		resp.headers['WWW-Authenticate'] = 'Basic realm="Credentials required"'
		return resp
	result = db.select('SELECT user_id FROM Users WHERE user_name = %(e)s AND user_password = %(p)s', {
		'e': request.authorization.username,
		'p': request.authorization.password
	})
	if len(result) != 1:
		resp = make_response("Authentification FAIL", 401)
		resp.headers['WWW-Authenticate'] = 'Basic realm="Credentials required"'
		return 1
	else :
		resp = make_reponse("Authentification OK", 200)
		resp.headers['WWW-Authenticate'] = 'Basic realm="Credentials valid"'
		return 0

#-----------------------------------------------------------------
@app.route('/games/<int:g_id>/moves', methods=['POST'])
def display_games_id_moves(game_id):
  
  db = Db()


  #Récupération de la requête json#
  
  data = request.get_json()


  if not(request.authorization):
    resp = make_response("Credentials required", 401)
    resp.headers['WWW-Authenticate'] = 'Basic realm="Credentials required"'
    return resp


  result1 = db.select("SELECT user_id FROM Users WHERE user_name = %(e)s AND user_password = %(p)s", {
  'e': request.authorization.username,
  'p': request.authorization.password
  })


  result2 = db.select("SELECT player_id FROM Player WHERE game_id= %(game_id)s AND user_id = %(user_id)s", {
  'game_id': game_id,
  'user_id': result1[0]["user_id"]
  })

  
  #Récuperation des positions actuelles du joueur#
  
  result3 = db.select("SELECT player_pos_y, player_pos_x FROM Player WHERE player_id = %(player_id)s" , {
  'player_id': result2[0]["player_id"]
  })  

  
#vérification joueur actuel

  #En fonction de l'action modification des positions #


  
  if data["action"] == "move" :
  
    if data["value"] == "up":
      dx =  0
      dy = -1
  
    elif data["value"] == "down":
      dx = 0
      dy = 1
  
    elif data["value"] == "left":
      dx = -1
      dy =  0
  
    elif data["value"] == "right":
      dx =  1
      dy =  0
  
  else:
    db.close()
    resp = make_response('Bad Request', 403)
    return resp
  
  
  #Message d'erreur si requêtes incompatible ou incomplête
   #Modification de la table joueur avec ajout des nouvelles positions après mouvement#

  player_pos_x = result3[0]["player_pos_x"] + dx
  player_pos_y = result3[0]["player_pos_y"] + dy

  
  db.execute("UPDATE Player SET player_pos_x = %(player_pos_x)s , player_pos_y = %(player_pos_y)s  WHERE  game_id = %(game_id)s", {
  'player_pos_x': player_pos_x,
  'player_pos_y': player_pos_y,
  'game_id' : game_id
  })

  #Envoie des nouvelles données
  
  response = {"id": game_id, "player_id": result2[0]["player_id"], "pos_x": result3[0]["player_pos_x"], "pos_y": result3[0]["player_pos_y"]}


  
  db.close()
  resp = make_response(json.dumps(result3))
  resp.mimetype = 'application/json'
  



  return resp
#-----------------------------------------------------------------
'''
@app.route('/games/<int:gameId>', methods=['GET'])
def get_IHM_game(gameId):
	db = Db()
	
	return '{"name":"Testcarte","id":1,"width":3,"height":3,"status":"OPENED","turn":5,"currentPlayer":"tata","players":["tata","toto","titi"],"maxPlayers":5,"timeout":30,"nbItems":{"coins":10,"chest":10,"potion":10},"nbItemsLeft":{"coins":5,"potion":7},"fovDefault":1,"victoryOn":{"rule":"coins","value":5},"ranking":["titi"],"inventory":{"coins":5,"potions":[{"kind":"immunity"},{"kind":"lottery-win"}]},"activePotion":null,"mapView":[[{"x":0,"y":0,"isObstacle":false,"skin":"00000000","players":[],"contains":{"kind":"","skin":""}}],[{"x":0,"y":1,"isObstacle":false,"skin":"00000000","players":["toto"],"contains":{"kind":"","skin":""}}],[{"x":0,"y":2,"isObstacle":true,"skin":"01000000","players":[],"contains":{"kind":"","skin":""}}],[{"x":1,"y":0,"isObstacle":false,"skin":"00000000","players":[],"contains":{"kind":"","skin":""}}],[{"x":1,"y":1,"isObstacle":true,"skin":"01000000","players":[],"contains":{"kind":"","skin":""}}],[{"x":1,"y":2,"isObstacle":false,"skin":"00000000","players":[],"contains":{"kind":"potion","skin":""}}],[{"x":2,"y":0,"isObstacle":false,"skin":"00000000","players":["tata"],"contains":{"kind":"","skin":""}}],[{"x":2,"y":1,"isObstacle":false,"skin":"00000000","players":[],"contains":{"kind":"chest","skin":""}}],[{"x":2,"y":2,"isObstacle":false,"skin":"00000000","players":["titi"],"contains":{"kind":"","skin":""}}]]}'
'''
#-----------------------------------------------------------------
	
if __name__ == "__main__":
	app.run()

