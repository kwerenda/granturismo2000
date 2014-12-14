var gameBorder = 400;
var mapTileSize = 128;

map  = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [1, 1, 1, 0, 1],
    [1, 1, 0, 0, 1],
    [1, 1, 0, 0, 0]
];

start = {x: 3, y:4 };
end = {x: 0, y:1 };

route = [{x:3, y:4}, {x:3, y:1}, {x:2, y:0}, {x:1, y:0}, {x:0, y:1}];

game = new Phaser.Game(gameBorder, gameBorder, Phaser.CANVAS, 'visualization', {}, true);

game.state.add('animation', {
    preload: preload,
    create: create,
    render: render
});

function preload() {
    //load image which will be used as ground texture
    game.load.image('road', 'assets/road.png');
    game.load.image('dirt', 'assets/dirt.png');

    //  This sets a limit on the up-scale
    game.scale.maxWidth = 500;
    game.scale.maxHeight = 500;

    //  Then we tell Phaser that we want it to scale up to whatever the browser can handle, but to do it proportionally
    game.scale.scaleMode = Phaser.ScaleManager.SHOW_ALL;
    game.scale.setScreenSize();
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
//        var shape = game.add.graphics(0, 0);
        game.context.strokeStyle = 'rgb(30,90,30)';
        game.context.lineWidth = 8;
        game.context.beginPath();
        game.context.moveTo(route[0].x*scaledMapGrid + scaledMapGrid/2, route[0].y*scaledMapGrid + scaledMapGrid/2);
//        shape.moveTo(route[0].x*scaledMapGrid + scaledMapGrid/2, route[0].y*scaledMapGrid + scaledMapGrid/2);
//        shape.lineStyle(2, 0x0000FF, 1); // width, color (0x0000FF), alpha (0 -> 1) // required settings
//        shape.beginFill(0xFFFF0B, 1); // color (0xFFFF0B), alpha (0 -> 1) // required settings
        for (var vert = 1; vert < route.length; vert++) {
            game.context.lineTo(route[vert].x*scaledMapGrid + scaledMapGrid/2, route[vert].y*scaledMapGrid + scaledMapGrid/2)
        }
//        shape.endFill();
        game.context.stroke();
        game.context.closePath();

//            new Phaser.Line(route[vert].x, route[vert].y, route[vert + 1].x, route[vert + 1].y);
    }
}

function create() {
    prepareStaticMap();
//    drawRoute();
}

function render() {
    drawRoute();
}

function loadGame() {
//    scale = (gameBorder / $scope.map["border"]) / tileSize;
    mapScale = (gameBorder / map.length) / mapTileSize;
//    scaledGrid = tileSize * scale;
    scaledMapGrid = mapScale * mapTileSize;
    game.state.start('animation');
}

loadGame();