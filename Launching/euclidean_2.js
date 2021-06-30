// module aliases
var Engine = Matter.Engine,
    Render = Matter.Render,
    World = Matter.World,
    Bodies = Matter.Bodies,
    Body = Matter.Body,
    Vertices = Matter.Vertices,
    Composites = Matter.Composites,
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
        showCollisions: false, // need to be true to show collision point coordinate
        background: 'black'
    }
});
Render.run(render);



// static parameters
var temporal_delay = 2; // time between collision and when patient starts to move, set to 2 to have frame_t A stops B stops
var duration = 1200; // the duration of capturing png images, generating stimulus video
// var duration = 600; // the max duration used for capturing collision frames, also have to keep Bstarted = false all the time.
var startMillis; // subtract the initial millis before first draw to begin at t_ratio=0
var xvelocity = 1; // 1 slow vs 2.4 fast
var blink_position = render.options.width / (4*2); // time to blink in patient object, 4 early vs 1.5 late

// ---------------------------------------------------------------------------------------------------------------------
// stimulus parameters
var distance_idx = 9; // [0, 3, 5, 6, 7, 8, 9]
var capturer = new CCapture({ format: 'png', framerate: 60 , name: 'Euclidean_warmup_'+distance_idx});
var spatial_gap = 80 + [0, 8, 16, 32, 48, 64, 80, 96, 112, 128][distance_idx]; // collision spatial gap between two convex shapes
// ---------------------------------------------------------------------------------------------------------------------

// objects

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


color = randomColor();
// var pointsA = Vertices.fromPath('0 200 90 200 0 260'); // B back
var pointsA = Vertices.fromPath('0 0 0 80 80 80 80 0'); // regular box
var boxA = makeBox(0, 230, pointsA, 'boxA', color);

// ----------------------------------------------------- box B to be changed
color = randomColor();

var pointsB = Vertices.fromPath('0 0 0 80 80 80 80 0'); // regular box
var boxB = makeBox(render.options.width/2, 230, pointsB, 'boxB', color);
// spatial gap = 80

// var pointsB = Vertices.fromPath('104 20 23 80 23 127 104 127 200 127 245 120 104 120 85 100 104 80'); // shape 1 concave
// var boxB = makeBox(render.options.width/2, 220, pointsB, 'boxB', color);
// Body.setAngle(boxB, -Math.PI); 
// // spatial gap = 69

// var pointsB = Vertices.fromPath('-104 20 -23 80 -23 127 -104 127 -200 127 -245 120 -104 120 -85 100 -104 80'); // shape 1 concave
// var boxB = makeBox(render.options.width/2, 225, pointsB, 'boxB', color);
// Body.setAngle(boxB, -Math.PI); 
// // spatial gap = 118

// var pointsB = Vertices.fromPath('84 30 84 104 73 96 75 115 60 82 73 70 50 50 -130 50 -130 58 -145 30'); // shape 2 concave
// var boxB = makeBox(render.options.width/2, 187, pointsB, 'boxB', color);
// // spatial gap = -19

// var pointsB = Vertices.fromPath('-84 30 -84 104 -73 96 -75 115 -60 82 -73 70 -50 50 130 50 130 58 145 30'); // shape 2 convex
// var boxB = makeBox(render.options.width/2, 187, pointsB, 'boxB', color);
// // spatial gap = 153

// var pointsB = Vertices.fromPath('70 140 109 140 109 67 40 15 33 50 -80 50 -92 38 -80 60 58 60 85 87 62 122'); // shape 3 concave
// var boxB = makeBox(render.options.width/2, 200, pointsB, 'boxB', color);
// // spatial gap = 33

// var pointsB = Vertices.fromPath('-70 140 -109 140 -109 67 -40 15 -33 50 80 50 92 38 80 60 -58 60 -85 87 -62 122'); // shape 3 convex
// var boxB = makeBox(render.options.width/2, 190, pointsB, 'boxB', color);
// // spatial gap = 113

// var pointsB = Vertices.fromPath('50 65 30 48 -130 48 -115 40 77 40 120 61 120 108 110 115 66 69 66 80 97 115 87 124 66 100 66 127 45 127 30 90'); // shape 4 concave
// var boxB = makeBox(render.options.width/2, 218, pointsB, 'boxB', color);
// // spatial gap = 64

// var pointsB = Vertices.fromPath('-50 65 -30 48 130 48 115 40 -77 40 -120 61 -120 108 -110 115 -66 69 -66 80 -97 115 -87 124 -66 100 -66 127 -45 127 -30 90'); // shape 4 convex
// var boxB = makeBox(render.options.width/2, 200, pointsB, 'boxB', color);
// // spatial gap = 128

// ----------------------------------------------------- end of change


// disable gravity
engine.world.gravity.y = 0;
World.add(engine.world, [boxA]);
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
        // Bstarted = false; // for collision frame screenshot, B does not have to start
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