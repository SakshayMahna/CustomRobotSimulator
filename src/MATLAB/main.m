scenario = createScenario();
robot = createRobot(scenario);

[ax,plotFrames] = show3D(scenario);
lightangle(-45,30)
view(60,50)

setup(scenario)
r = rateControl(20);

while advance(scenario)
    motion = read(robot);
    move(robot, "base", [motion(1:3) 1 0 0 0 0 0 1 0 0 0 0 0 0]);
    show3D(scenario,Parent=ax,FastUpdate=true);
    waitfor(r);
    drawnow update
end
