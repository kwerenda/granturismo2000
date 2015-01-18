



route1 = [{x:3, y:4}, {x:3, y:1}, {x:2, y:0}, {x:1, y:0}, {x:0, y:1}];

route3 = [
{x:0,y:0},
{x:2,y:1},
{x:0,y:0},
{x:3,y:0}]; //443
route2 = [
{x:2,y:3},
{x:0,y:0},
{x:2,y:0},
{x:4,y:0}];


var leadGrid, scaledMapGrid, mapScale;
var gameBorder = 500;
var mapTileSize = 128;
var game, gameWidth, gameHeight;

function preload() {
    game.load.image('road', 'assets/road.png');
    game.load.image('dirt', 'assets/dirt.png');

    game.scale.maxWidth = gameWidth;
    game.scale.maxHeight = gameHeight;

    game.scale.scaleMode = Phaser.ScaleManager.SHOW_ALL;
    game.scale.refresh();
}

function prepareStaticMap() {
    var road = game.add.tileSprite(0, 0, game.width, game.height, 'road');
    for(var y=0; y<map.length; y++) {
        for(var x=0; x<=map[y].length; x++) {
            if(map[y][x]==1) {
                var obs = game.add.sprite(x * scaledMapGrid, y * scaledMapGrid, 'dirt');
                obs.scale.x = mapScale;
                obs.scale.y = mapScale;
            }
        }
    }
}

function drawRoute() {
    if(route.length>0) {
        game.context.strokeStyle = 'rgb(30,90,30)';
        game.context.lineWidth = 8;
        game.context.beginPath();
        game.context.moveTo(start.x*scaledMapGrid + scaledMapGrid/2, start.y*scaledMapGrid + scaledMapGrid/2);
        for (var vert = 1; vert < route.length; vert++) {
            game.context.lineTo(route[vert].x*scaledMapGrid + scaledMapGrid/2, route[vert].y*scaledMapGrid + scaledMapGrid/2)
        }
        game.context.lineTo(end.x*scaledMapGrid + scaledMapGrid/2, end.y*scaledMapGrid + scaledMapGrid/2);
        game.context.stroke();
        game.context.closePath();
    }
}

function create() {
    prepareStaticMap();
}

function render() {
    drawRoute();
}

function loadGame() {
//    scale = (gameBorder / $scope.map["border"]) / tileSize;

    var gridWidth = map[0].length;
    var gridHeight = map.length;
    var ratio =  gridWidth / gridHeight;
    if(gridWidth >= gridHeight) {
        gameWidth = gameBorder;
        gameHeight = gameBorder/ratio;
        leadGrid = map[0].length;
    } else {
        gameWidth = gameBorder * ratio;
        gameHeight = gameBorder;
        leadGrid = map.length;
    }
    mapScale = (gameBorder / leadGrid) / mapTileSize;
//    scaledGrid = tileSize * scale;
    scaledMapGrid = mapScale * mapTileSize;

    game = new Phaser.Game(gameWidth, gameHeight, Phaser.CANVAS, 'visualization', {}, true);

    game.state.add('animation', {
        preload: preload,
        create: create,
        render: render,
        update: function(){}
    });
    game.state.start('animation');
}

loadGame();