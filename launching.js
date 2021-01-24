// module aliases
var Engine = Matter.Engine,
    Render = Matter.Render,
    World = Matter.World,
    Bodies = Matter.Bodies,
    Body = Matter.Body,
    Vertices = Matter.Vertices,
    Composites = Matter.Composites,
    // Runner = Matter.Runner,
    MouseConstraint = Matter.MouseConstraint,
    Mouse = Matter.Mouse,
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
        showCollisions: false,
        background: 'black'
    }
});
Render.run(render);
// var runner = Runner.create({fps:60});
// Runner.run(runner, engine);


// static parameters
var temporal_delay = 2; // time between collision and when patient starts to move, set to 2 to have frame_t A stops B stops
var duration = 1200; // the duration of capturing png images
var startMillis; // subtract the initial millis before first draw to begin at t_ratio=0
var xvelocity = 1; // 1 slow vs 2.4 fast
var blink_position = render.options.width / (4*2); // time to blink in patient object, 4 early vs 1.5 late

// ---------------------------------------------------------------------------------------------------------------------
// stimulus parameters
var distance_idx = 9;
var capturer = new CCapture({ format: 'png', framerate: 60 , name: 'H_concave_'+distance_idx});
var spatial_gap = 96 + [0, 4, 8, 12, 16, 20, 25, 32, 45, 64][distance_idx]; // collision spatial gap between two convex shapes
// ---------------------------------------------------------------------------------------------------------------------

// objects
var ground = Bodies.rectangle(500, 350, 1000, 5, {label: 'ground', isStatic: true, friction: 0, render:{ fillStyle: 'black'}});
// Vertices.fromPath('104 20 42 80 25 125 127 117 85 107 104 98'); // A front concave
// Vertices.fromPath('41 23 46 102 66 110 23 119 127 125 105 81'); // A back convex
// Vertices.fromPath('59 14 95 24 106 79 45 136 44 82 52 94 56 70 48 43'); // B front convex
// Vertices.fromPath('96 12 59 18 43 75 101 137 105 82 96 94 93 72 105 40'); // B back concave
// Vertices.fromPath('42 20 45 114 105 130 71 97 83 82 107 78 83 40 66 24'); // C front concave
// Vertices.fromPath('105 19 80 23 68 36 43 77 65 81 79 96 47 130 106 112'); // C back convex
// Vertices.fromPath('108 25 35 54 38 123 49 106 81 119 110 119 105 109 113 109 99 96 66 86 115 91 54 63'); // D front convex
// Vertices.fromPath('40 28 113 55 113 122 102 106 70 119 41 119 45 110 38 109 49 98 81 85 35 89 92 64'); // D back concave
// Vertices.fromPath('0 0 0 80 80 80 80 0'); // regular box
// Vertices.fromPath('34 33 105 25 98 82 116 47 91 122 63 42 44 109 72 96 47 123 35 119'); // E front concave
// Vertices.fromPath('43 27 113 32 117 117 105 123 80 98 108 109 84 42 61 123 33 51 51 82'); // E back convex
// Vertices.fromPath('54 22 112 37 111 14 119 20 119 80 100 122 53 135 41 120 91 51 80 54 38 99 30 91 60 60 33 60 36 39'); // F front concave
// Vertices.fromPath('30 20 39 14 39 38 94 21 115 39 117 59 91 59 121 90 113 97 71 56 59 50 110 120 98 134 51 122 31 81'); // F back convex
// Vertices.fromPath('15 104 38 82 57 31 69 56 66 23 92 28 87 58 117 38 127 54 34 99 126 106 135 117 45 114 35 128'); // G front convex
// Vertices.fromPath('25 52 36 36 66 56 63 26 86 22 83 56 96 30 114 83 135 105 115 128 105 113 14 114 25 104 114 98'); // G back concave
// Vertices.fromPath('28 26 33 44 101 27 69 51 49 56 57 67 45 74 51 80 24 82 30 118 52 93 75 114 77 104 82 137 90 97 127 112 119 48 104 48 127 18 84 14'); // H front convex
// Vertices.fromPath('27 15 75 15 127 29 119 47 55 26 78 49 102 58 95 67 107 77 101 82 126 88 119 122 99 95 74 114 72 104 64 136 59 95 24 111 34 44 47 44'); // H back concave

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
color = randomColor();
var boxA = makeBox(0, 250, pointsA, 'boxA', color);
Body.setAngle(boxA, -Math.PI/1.7);

// ----------------------------------------------------- box B to be changed
color = randomColor();
// var pointsB = Vertices.fromPath('0 0 0 80 80 80 80 0'); // regular box
var pointsB = Vertices.fromPath('27 15 75 15 127 29 119 47 55 26 78 49 102 58 95 67 107 77 101 82 126 88 119 122 99 95 74 114 72 104 64 136 59 95 24 111 34 44 47 44'); // H back concave
var boxB = makeBox(render.options.width/2, 215, pointsB, 'boxB', color);
Body.setAngle(boxB, -Math.PI*1);
// ----------------------------------------------------- end of change


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

// collision detection for type 4 (two convex)
function type4COllision(){
    if (Astarted==true && boxA.position.x + spatial_gap >= boxB.position.x){ 
        // console.log('center of mass x distance', boxB.position.x - boxA.position.x);
        // console.log('Euclidean A tip to B COM', Math.sqrt(Math.pow(boxA.position.x + (473.87-411.35) - boxB.position.x, 2) + Math.pow(boxA.position.y + (208.31-250) - boxB.position.y, 2)));
        console.log('collision t', t);
        stopA();
    }
}

// generate random color with same brightness
function randomColor(){ // hue, saturation, brightness, alpha
    return "hsla(" + ~~(360 * Math.random()) + "," +
                    "70%,"+
                    "70%, 1)"
}


// ---------------------------------------------------------------------------------------------------------------------
// main loop

// helper variables
var Astarted = false; // if A started to move
var Bstarted = false; // if B started to move
var Bshown = false; // if B has blinked into the screen
var t = 0; // current timestamp
var collision_time = Infinity; // collision timestamp record

// update frame
(function run() {
    
    // regular updates
    window.requestAnimationFrame(run); // fps fixed to 60
    Engine.update(engine, 1);
    render.mouse = mouse;


    // time stamp for capturer
    if (t >= duration){
        console.log('finished recording');
        capturer.stop();
        capturer.save();
        return;
    }

    // start boxA
    if (t==1){
        // Body.setVelocity( boxA, {x: xvelocity, y: 0});
        Astarted = true;
        capturer.start();
    }

    // blink in boxB
    if (Bshown==false && boxA.position.x >= blink_position) {
        Bshown = true;
        World.add(engine.world, boxB);
    }

    // collision detection
    type4COllision(); 

    // start boxB if there was a collision
    if (Astarted==false && t==collision_time+temporal_delay){
        Bstarted = true;
    }
    
    // maintain constant velocity
    if (Astarted){
        // Body.setVelocity(boxA, {x: xvelocity, y: 0});
        Body.setPosition(boxA, {x:boxA.position.x+xvelocity, y:boxA.position.y});
    }
    if (Bstarted){
        // Body.setVelocity(boxB, {x:xvelocity, y: 0})
        Body.setPosition(boxB, {x:boxB.position.x+xvelocity, y:boxB.position.y});
    }

    // capturer saving
    capturer.capture(render.canvas);

    // update time
    t = t + 1;
})();