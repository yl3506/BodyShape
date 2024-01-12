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
var distance_idx = 9; // [0, 4, 5, 6, 7, 8, 9]
var capturer = new CCapture({ format: 'png', framerate: 60 , name: 'Euclidean_H_convex_'+distance_idx});
var spatial_gap = 116 + [0, 4, 8, 12, 16, 20, 25, 32, 45, 64][distance_idx]; // collision spatial gap between two convex shapes
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


var pointsA = Vertices.fromPath('96 12 59 18 43 75 101 137 105 82 96 94 93 72 105 40'); // B back
color = randomColor();
var boxA = makeBox(0, 250, pointsA, 'boxA', color);
Body.setAngle(boxA, -Math.PI/1.7);

// ----------------------------------------------------- box B to be changed
color = randomColor();

// var pointsB = Vertices.fromPath('104 20 42 80 25 125 80 120 118 139 165 125 120 130 100 119 127 117 85 107 104 98'); // A concave
// var boxB = makeBox(render.options.width/2, 230, pointsB, 'boxB', color);
// Body.setAngle(boxB, -Math.PI); // spatial gap = 97

// var pointsB = Vertices.fromPath('-60 299 -123 239 -140 194 -85 199 -47 180 0 194 -45 189 -65 200 -38 202 -80 212 -61 221'); // A convex
// var boxB = makeBox(render.options.width/2, 225, pointsB, 'boxB', color);
// // spatial gap = 111

// var pointsB = Vertices.fromPath('34 33 105 25 98 82 116 47 91 122 63 42 44 109 72 96 52 118 35 180 28 180 47 123 35 119'); // E concave
// var boxB = makeBox(render.options.width/2, 215, pointsB, 'boxB', color);
// Body.setAngle(boxB, -Math.PI*1.51);// spatial gap = 104

// var pointsB = Vertices.fromPath('-143 180 -154 251 -96 246 -132 263 -56 240 -135 210 -68 193 -82 220 -59 201 2 186 3 179 -54 196 -58 184'); // E convex
// var boxB = makeBox(render.options.width/2, 230, pointsB, 'boxB', color);
// // spatial gap = 105

// var pointsB = Vertices.fromPath('54 22 112 37 111 14 119 20 119 80 100 122 70 130 50 185 -45 185 -45 175 45 175 59 133 53 135 41 120 91 51 80 54 38 99 30 91 60 60 33 60 36 39'); // F concave
// var boxB = makeBox(render.options.width/2, 225, pointsB, 'boxB', color);
// // spatial gap = 94

// var pointsB = Vertices.fromPath('-125 156 -183 171 -182 148 -190 154 -190 214 -171 256 -141 264 -121 319 -26 319 -26 309 -116 309 -130 267 -124 269 -112 254 -162 185 -151 188 -109 233 -101 225 -131 194 -104 194 -107 173'); // F convex
// var boxB = makeBox(render.options.width/2, 250, pointsB, 'boxB', color);
// // spatial gap = 116

// var pointsB = Vertices.fromPath('27 15 65 15 80 -40 200 -40 200 -33 88 -33 75 15 127 29 119 47 55 26 78 49 102 58 95 67 107 77 101 82 126 88 119 122 99 95 74 114 72 104 64 136 59 95 24 111 34 44 47 44'); // H concave
// var boxB = makeBox(render.options.width/2, 224, pointsB, 'boxB', color);
// Body.setAngle(boxB, -Math.PI);// spatial gap = 94

var pointsB = Vertices.fromPath('-152 250 -114 250 -98 305 21 305 21 298 -90 298 -104 250 -52 236 -60 218 -124 239 -101 216 -77 207 -84 198 -72 188 -78 183 -53 177 -60 143 -80 170 -105 151 -107 161 -115 129 -120 170 -155 154 -145 221 -132 221'); // H convex
var boxB = makeBox(render.options.width/2, 240, pointsB, 'boxB', color);
// spatial gap = 116
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