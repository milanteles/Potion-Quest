var pNum = 2;
var gridNum = 3;
var nameInput="";
var heightInput="";
var widthInput="";
var maxPlayerInput="";
var fovInput ="";
var timeoutInput="";
var coinInput="";
var chestInput="";
var potionInput="";
var valueInput="";
var victoryOnInput="";

function updateInputName() {
  nameInput=document.getElementById('inputName').value;
  console.log(nameInput);
  $("#mapName").val(nameInput);
}

function updateInputHeight() {
  heightInput=document.getElementById('inputHeight').value;
  heightInput=Number(heightInput);
  console.log(heightInput);
  $("#mapHeight").val(heightInput);
}

function updateInputWidth() {
  widthInput=document.getElementById('inputWidth').value;
  widthInput=Number(widthInput);
  console.log(widthInput);
  $("#mapWidth").val(widthInput);
}

function updateInputMaxPlayer() {
  maxPlayerInput=document.getElementById('inputMaxPlayer').value;
  maxPlayerInput=Number(maxPlayerInput);
  console.log(maxPlayerInput);
  $("#numberOfPlayer").val(maxPlayerInput);
}

function updateInputFov() {
  fovInput=document.getElementById('inputFov').value;
  fovInput=Number(fovInput);
  console.log(fovInput);
  $("#mapName").val(fovInput);
}

function updateInputTimeout() {
  timeoutInput=document.getElementById('inputTimeout').value;
  timeoutInput=Number(timeoutInput);
  console.log(timeoutInput);
  $("#turnLeft").val(timeoutInput);
}

function updateInputCoins() {
  coinInput=document.getElementById('inputCoins').value;
  coinInput=Number(coinInput);
  console.log(coinInput);
  $("#coinLeft").val(coinInput);
}

function updateInputChest() {
  chestInput=document.getElementById('inputChest').value;
  chestInput=Number(chestInput);
  console.log(chestInput);
  $("#chestLeft").val(chestInput);
}

function updateInputPotion() {
  potionInput=document.getElementById('inputPotion').value;
  potionInput=Number(potionInput);
  console.log(potionInput);
  $("#potionLeft").val(potionInput);
}

function updateInputValues() {
  valueInput=document.getElementById('inputValues').value;
  console.log(valueInput);
}

function chooseVictory(){
  if (document.getElementById('victoryCoinsCheck').checked) {
    victoryOnInput = document.getElementById('victoryCoinsCheck').value;
  }
  else if (document.getElementById('victoryItemCheck').checked) {
    victoryOnInput = document.getElementById('victoryItemCheck').value;
  }
  else if (document.getElementById('victoryTurnsCheck').checked) {
    victoryOnInput = document.getElementById('victoryTurnsCheck').value;
  }
  console.log(victoryOnInput);
  $("#victoryOn").val(victoryOnInput);
}

function appendPlayer() {
  for (var i = 0; i < maxPlayerInput - 1 ; i++) {
    var table = document.getElementById("myTable");
    var row = table.insertRow(pNum-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    cell1.innerHTML = `<td><input type="text" placeholder="Player ${pNum} - X" id="player${pNum}X"></td>`;
    cell2.innerHTML = `<td><input type="text" placeholder="Player ${pNum} - Y" id="player${pNum}Y"></td>`;
    pNum++;
  }

}

function deletePlayer() {
  for (var i = 0; i < maxPlayerInput; i++) {
    if ( pNum > 2 ){
      pNum--;
      document.getElementById("myTable").deleteRow(pNum-1);
    }
  }
}

function addGame() {
  $.ajax('/games', {
    method: "POST",
    contentType: 'application/json',
    data: JSON.stringify({ height: heightInput, width: widthInput, timeout: timeoutInput, name: nameInput, maxPlayers: maxPlayerInput, victoryOn:{rule: victoryOnInput, value: valueInput}, fovDefault: fovInput, nbItems:{coins: coinInput, chest: chestInput, potions: potionInput}}),
    success: listGames
  });
}

function listGames() {
  $('#listGame').empty();
  $.ajax('/games', {
    success: function(Games){
      for(var i in Games) {
        var game = Games[i];
        $('#listGame').append(`<option value="${game.id}"> ${game.name} ${game.status}</option>`);
      }
    }
  });
}


function getAGame(gameid) {          
  $.ajax('/game/'+gameid, {
    success: function(game){
      $('#mapHeight').val(game.height);
      heightInput=game.height
      $('#mapName').val(game.name);
      $('#mapWidth').val(game.width);
      widthInput=game.width
      $('#currentPlayer').val(game.currentPlayer);
      $('#numberOfPlayer').val(game.maxPlayers);
      $('#turnLeft').val(game.turn);
      $('#chestLeft').val(game.nbItems.coins);
      $('#coinLeft').val(game.nbItems.chest);
      $('#potionLeft').val(game.nbItems.potions);
      $('#victoryOn').val(game.victoryOn.rule);
      $('#valueVictory').val(game.victoryOn.value);
      appendGrid()
    }
  });
}

function listPlayers(id){
  $('#listPlayer').empty();
  $.ajax('/games/'+id+'/players', {
    success: function(Player){
      Players= jQuery.parseJSON(Player)
      for(var i in Players) {
        var player = Players[i];
        $('#listPlayer').append(`<option value="${player.player_id}">${player.player}</option>`);
      }
    }
  });
}

function appendGrid() {

  $('#testGrille').empty();

  for ( var i = 0; i < heightInput; i++){
    var row = $('<tr></tr>');
    for ( var j = 0; j < widthInput; j++){
      row.append(`<td>${i}${j}</td>`);
    }
    $('#testGrille').append(row);
  }
}


listGames();

$(function(){ // on DOM Ready
                
  $('#listGame').on('click', function(){
    var $this = $(this);
    var gid = $this.val();
    getAGame(gid);
  }); 

  $('#listGame').on('click', function(){
    var $this = $(this);
    var id = $this.val();
    listPlayers(id);
  });

  $('#btnNouvPartie').on('click', addGame);
      
})


