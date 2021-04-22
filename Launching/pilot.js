// module aliases
var Engine = Matter.Engine,
    Render = Matter.Render,
    World = Matter.World,
    Bodies = Matter.Bodies,
    Body = Matter.Body,
    Vertices = Matter.Vertices,
    Composites = Matter.Composites,
    Runner = Matter.Runner,
    MouseConstraint = Matter.MouseConstraint,
    Mouse = Matter.Mouse,
    Runner = Matter.Runner,
    Events = Matter.Events;

// initialize engine, render, runner
var engine = Engine.create();
var render = Render.create({
    element: document.body,
    engine: engine,
    options: {
        width: 1000,
        height: 400,
        wireframes: false,
        showAngleIndicator: false,
        showConvexHulls: false,
        showCollisions: true,
        background: 'black'
    }
});

Render.run(render);
var runner = Runner.create();
Runner.run(runner, engine);


// ---------------------------------------------------------------------------------------------------------------------
// stimulus parameters
var temporal_delay = 2; // time between collision and when patient starts to move, set to 2 to have frame_t A stops B stops
var type2_margin = 23 / 2; // type 2 use only: margin for the semi-coarse bounding box (between coarse and precise boxes)

var xvelocity = 1; // 1 slow vs 2.4 fast
var blink_position = render.options.width / (1.5*2); // time to blink in patient object, 4 early vs 1.5 late
var bounding_box_type = 4; // 1 for coarse box, 2 for semi-coarse, 3 for precise box, 4 for collision with exact position
var spatial_gap = 84 + ((420.8-387.7)/2)*3; // collision spatial gap between two convex shapes


// ---------------------------------------------------------------------------------------------------------------------
// objects

var ground = Bodies.rectangle(500, 350, 1000, 5, {label: 'ground', isStatic: true, friction: 0, render:{ fillStyle: 'black'}});
// Vertices.fromPath('104 20 42 80 25 125 127 117 85 107 104 98'); // A front
// Vertices.fromPath('41 23 46 102 66 110 23 119 127 125 105 81'); // A back
// Vertices.fromPath('59 14 95 24 106 79 45 136 44 82 52 94 56 70 48 43'); // B front
// Vertices.fromPath('96 12 59 18 43 75 101 137 105 82 96 94 93 72 105 40'); // B back
// Vertices.fromPath('42 20 45 114 105 130 71 97 83 82 107 78 83 40 66 24'); // C front
// Vertices.fromPath('105 19 80 23 68 36 43 77 65 81 79 96 47 130 106 112'); // C back
// Vertices.fromPath('108 25 35 54 38 123 49 106 81 119 110 119 105 109 113 109 99 96 66 86 115 91 54 63'); // D front
// Vertices.fromPath('40 28 113 55 113 122 102 106 70 119 41 119 45 110 38 109 49 98 81 85 35 89 92 64'); // D back
// Vertices.fromPath('0 0 0 80 80 80 80 0'); // regular box

function makeBox(x, y, points, label, color, xvelocity) {
    return(Bodies.fromVertices(x, y, points,
            {
                label: label,
                render: {
                    fillStyle: color,
                    strokeStyle: color,
                    lineWidth: 1,
                    visible: true
                },
                friction: 0,
                velocity: {x: xvelocity, y:0}
            }, true)
    )
}

// var pointsA = Vertices.fromPath('0 0 0 80 80 80 80 0'); // regular box
var pointsA = Vertices.fromPath('96 12 59 18 43 75 101 137 105 82 96 94 93 72 105 40'); // B back
color = '#'+Math.floor(Math.random()*16777215).toString(16);

var boxA = makeBox(0, 250, pointsA, 'boxA', color, 0);
Body.setAngle(boxA, -Math.PI/1.7);

// -------------------------------- box B to be changed
// var pointsB = Vertices.fromPath('0 0 0 80 80 80 80 0'); // regular box
var pointsB = Vertices.fromPath('40 28 113 55 113 122 102 106 70 119 41 119 45 110 38 109 49 98 81 85 35 89 92 64'); // D back
color = '#'+Math.floor(Math.random()*16777215).toString(16);

var boxB = makeBox(render.options.width/2, 240, pointsB, 'boxB', color, xvelocity);
Body.setAngle(boxB, -Math.PI*0.07);
// --------------------------------- end change


// disable gravity
engine.world.gravity.y = 0;
// add all objects to world, ready to run
World.add(engine.world, [boxA, ground]);
// add mouse control
var mouse = Mouse.create(render.canvas),
    mouseConstraint = MouseConstraint.create(engine, {
        mouse: mouse,
        constraint: {
            stiffness: 0.2,
            render: {
                visible: false
            }
        }
    });
World.add(engine.world, mouseConstraint);


// ---------------------------------------------------------------------------------------------------------------------
// collision detection

// stop A moving when it hits B
function stopA () {
    Astarted = false;
    Body.setVelocity(boxA, {x: 0, y: 0});
    collision_time = t;
}

function type1Collision () {
    if (Astarted==true){
        stopA();
        console.log('type 1 x position', boxA.position.x);
    }
}

function type2Collision () {
    // touches the coarse box
    if (temp_touch==false){
        temp_touch = true;
        temp_x = boxA.position.x;
    }
    // half way passes the coarse box
    if (Astarted==true && temp_touch && (boxA.position.x >= temp_x + type2_margin)){
        stopA();
        console.log('type 2 x position', boxA.position.x);
    }
}

// collision detection for type 3 (precise)
if (bounding_box_type == 3) {
    Matter.Events.on(engine, 'collisionStart', function (event) {
        let pairs = event.pairs;
        pairs.forEach(function (pair) {
            if ((pair.bodyA.label == "boxA" && pair.bodyB.label == "boxB") || (pair.bodyA.label == "boxB" && pair.bodyB.label == "boxA")) {
                stopA();
                console.log('type 3 x position', boxA.position.x);
                console.log(pair.collision)
            }
        });
    });
}

// collision detection for type 4 (two convex)
function type4COllision(){
    if (Astarted==true && boxA.position.x + spatial_gap >= boxB.position.x){ 
        console.log('center of mass x distance', boxB.position.x - boxA.position.x);
        console.log('Euclidean A tip to B com', Math.sqrt(Math.pow(boxA.position.x + (473.87-411.35) - boxB.position.x, 2) + Math.pow(boxA.position.y + (208.31-250) - boxB.position.y, 2)));
        stopA();
    }
}


// ---------------------------------------------------------------------------------------------------------------------
// main loop

// helper variables
var Astarted = false; // if A started to move
var Bstarted = false; // if B started to move
var Bshown = false; // if B has blinked into the screen
var t = 0; // current timestamp
var collision_time = Infinity; // collision timestamp record
var temp_touch = false; // for type2 use only: record whether boxA touches boxB's coarse box
var temp_x = Infinity;  // for type2 use only: record collision position of boxA when touching coarse box


// update frame
(function run() {
    
    // regular updates
    window.requestAnimationFrame(run);
    Engine.update(engine, 1);
    render.mouse = mouse;

    // start boxA
    if (t==1){
        Body.setVelocity( boxA, {x: xvelocity, y: 0});
        Astarted = true;
        // console.log(boxA);
    }
    // blink in boxB
    if (Bshown==false && boxA.position.x >= blink_position) {
        Bshown = true;
        World.add(engine.world, boxB);
    }

    // collision for coarse bounding box
    if (Matter.SAT.collides(boxA, boxB).collided){
        if (bounding_box_type==1){
            type1Collision();
        }
        if (bounding_box_type==2){
            type2Collision();
        }
    }
    if (bounding_box_type==4){
        type4COllision();
    }

    // start boxB if there was a collision
    if (Astarted==false && t==collision_time+temporal_delay){
        Bstarted = true;
    }
    
    // maintain constant velocity
    if (Astarted){
        Body.setVelocity(boxA, {x: xvelocity, y: 0});
    }
    if (Bstarted){
        Body.setVelocity(boxB, {x:xvelocity, y: 0})
    }

    t = t + 1;
})();