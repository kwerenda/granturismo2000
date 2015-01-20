



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
var gameBorder = 700;
var mapTileSize = 128;
var game, gameWidth, gameHeight;
var r=0, g= 56, b=50;
var r_line = 255, g_line= 80, b_line= 0;
var r_start = 72, g_start= 204, b_start= 20;
var r_end= 255, g_end= 7, b_end= 0;
var r_rect = 97, g_rect =  31, b_rect = 0;

function preload() {
    game.load.image('BlackFrame', 'assets/BlackFrame.png');
    game.load.image('WhiteFrame', 'assets/WhiteFrame.png');
    game.load.image('WhiteRectangle', 'assets/WhiteRectangle.png');

    game.scale.maxWidth = gameWidth;
    game.scale.maxHeight = gameHeight;

    game.scale.scaleMode = Phaser.ScaleManager.SHOW_ALL;
    game.scale.refresh();
}

function prepareStaticMap() {

    //game.stage.backgroundColor = Phaser.Color.createColor(255,255,255);

    for(var x=0; x<map.length; x++) {
        for(var y=0; y<map[x].length; y++) {
            var obs = game.add.sprite(x * scaledMapGrid, y * scaledMapGrid, 'WhiteRectangle');
            obs.scale.x = mapScale;
            obs.scale.y = mapScale;
            obs.tint = Phaser.Color.getColor(r, g, b);
            obs.alpha = map[x][y];
        }
    }
    var graphics = game.add.graphics(0, 0);
    var circleRadius = mapScale >= 0.1 ? 15: 10;
    graphics.lineStyle(0, 0xFFFFFF);
    graphics.beginFill(Phaser.Color.getColor(r_start, g_start, b_start), 1);
    graphics.drawCircle(start.x*scaledMapGrid + scaledMapGrid/2, start.y*scaledMapGrid + scaledMapGrid/2, circleRadius);
    graphics.endFill();
    graphics.beginFill(Phaser.Color.getColor(r_end, g_end, b_end), 1);
    graphics.drawCircle(end.x*scaledMapGrid + scaledMapGrid/2, end.y*scaledMapGrid + scaledMapGrid/2, circleRadius);
    graphics.endFill();
    //obs = game.add.sprite(start.x * scaledMapGrid, start.y * scaledMapGrid, 'WhiteFrame');
    //obs.scale.x = mapScale;
    //obs.scale.y = mapScale;
    //
    //obs = game.add.sprite(end.x * scaledMapGrid, end.y * scaledMapGrid, 'WhiteFrame');
    //obs.scale.x = mapScale;
    //obs.scale.y = mapScale;


    for (var vert = 0; vert < discrete_route.length; vert++) {
        obs = game.add.sprite(discrete_route[vert].x * scaledMapGrid, discrete_route[vert].y * scaledMapGrid, 'BlackFrame');
        obs.scale.x = mapScale;
        obs.scale.y = mapScale;
    }

    drawRoute()
}

function drawRoute() {
    if(route.length>0) {
        var graphics = game.add.graphics(0, 0);
        var line_graphics = game.add.graphics(0,0);
        var lineWidth = mapScale >= 0.1 ? 8 : 4;
        var circleRadius = mapScale >= 0.1 ? 15: 10;
        line_graphics.lineStyle(lineWidth, Phaser.Color.getColor(r_line, g_line, b_line), 1);
        line_graphics.moveTo(start.x*scaledMapGrid + scaledMapGrid/2, start.y*scaledMapGrid + scaledMapGrid/2);
        for (var vert = 0; vert < route.length; vert++) {
            line_graphics.lineTo(route[vert].x*scaledMapGrid + scaledMapGrid/2, route[vert].y*scaledMapGrid + scaledMapGrid/2);
            graphics.lineStyle(0, 0xFFFFFF);
            graphics.beginFill(Phaser.Color.getColor(r_line, g_line, b_line), 1);
            graphics.drawCircle(route[vert].x*scaledMapGrid + scaledMapGrid/2, route[vert].y*scaledMapGrid + scaledMapGrid/2, circleRadius);
            graphics.endFill();
        }
        line_graphics.lineTo(end.x*scaledMapGrid + scaledMapGrid/2, end.y*scaledMapGrid + scaledMapGrid/2);
    }
}

function create() {
    prepareStaticMap();
}

function loadGame() {
//    scale = (gameBorder / $scope.map["border"]) / tileSize;

    var gridWidth = map.length;
    var gridHeight = map[0].length;
    var ratio =  gridWidth / gridHeight;
    if(gridWidth >= gridHeight) {
        gameWidth = gameBorder;
        gameHeight = gameBorder/ratio;
        leadGrid = map.length;
    } else {
        gameWidth = gameBorder * ratio;
        gameHeight = gameBorder;
        leadGrid = map[0].length;
    }
    mapScale = (gameBorder / leadGrid) / mapTileSize;
//    scaledGrid = tileSize * scale;
    scaledMapGrid = mapScale * mapTileSize;

    game = new Phaser.Game(gameWidth, gameHeight, Phaser.CANVAS, 'visualization', {}, true);

    game.state.add('animation', {
        preload: preload,
        create: create
    });
    game.state.start('animation');
}

loadGame();