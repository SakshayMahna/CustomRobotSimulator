%% Use Python Virtual Environment
% https://in.mathworks.com/support/search.html/answers/1750425-python-virtual-environments-with-python-interface.html?fq%5B%5D=asset_type_name:answer&page=1
pythonPath = "C:\\Personal\\Robot\\Mobile Robots\\LocalizationExperiment\\CustomRobotSimulator\\rsim\\Scripts\\python.exe";
pyenv('Version', pythonPath, 'ExecutionMode', 'OutOfProcess');

%% Import Modules
components = py.importlib.import_module('components');
components = py.importlib.reload(components);
pygame_components = py.importlib.import_module('components.pygame_components');
pygame_components = py.importlib.reload(pygame_components);

physics_engine = py.importlib.import_module('physics_engine.physics_engine');
physics_engine = py.importlib.reload(physics_engine);
physics_actors = py.importlib.import_module('physics_engine.actors');
physics_actors = py.importlib.reload(physics_actors);

visual_engine = py.importlib.import_module('visual_engine.visual_engine');
visual_engine = py.importlib.reload(visual_engine);
visual_actors = py.importlib.import_module('visual_engine.actors');
visual_actors = py.importlib.reload(visual_actors);

%% Script
ve = visual_engine.PygameVisualEngine();
pe = physics_engine.PygamePhysicsEngine(0.01);

grid = createGrid(pygame_components);
ve.add_actor(visual_actors.VEGridActor(grid));
pe.add_actor(physics_actors.PEGridActor(grid));

robot = createRobot(components, pygame_components);
ve.add_actor(visual_actors.VERobotActor(robot));
pe.add_actor(physics_actors.PERobotActor(robot));

sensor = createLaserSensor(pygame_components, grid);
robot.add_sensor(sensor);
ve.add_actor(visual_actors.VELaserSensorActor(sensor));
pe.add_actor(physics_actors.PELaserSensorActor(sensor));

RobotNode(robot);

running = ve.initialize();

while running
    running = ve.render();
    pe.step();
end

ve.terminate();

%% Creation functions
function grid = createGrid(pygame_components)
    grid = pygame_components.PygameGrid();
    
    obstacle = pygame_components.PygameRectangleObstacle(440, 160, 300, 300);
    grid.add_obstacle(obstacle);
end

function robot = createRobot(components, pygame_components)
    initialPose = components.motion.Pose(340, 60, -pi/6);
    motionModel = components.motion.UnicycleModel(initialPose);
    robot = pygame_components.PygameRobot(motionModel);
end

function sensor = createLaserSensor(pygame_components, grid)
    resolution = 0.005;
    startAngle = -0.3; 
    endAngle = 0.3;
    sensorOffsets = startAngle:resolution:endAngle;

    sensor = pygame_components.PygameLaserSensor(grid, sensorOffsets);
end