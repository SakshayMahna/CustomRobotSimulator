function scenario = createScenario()
    scenario = robotScenario(UpdateRate=5);
    
    floorColor = [0.5882 0.2941 0];
    addMesh(scenario,"Plane",Position=[5 5 0],Size=[10 10],Color=floorColor);
    
    wallHeight = 1;
    wallWidth = 0.25;
    wallLength = 10;
    wallColor = [1 1 0.8157];
    
    addMesh(scenario,"Box",Position=[wallWidth/2, wallLength/2, wallHeight/2],...
        Size=[wallWidth, wallLength, wallHeight],Color=wallColor,IsBinaryOccupied=true);
    addMesh(scenario,"Box",Position=[wallLength-wallWidth/2, wallLength/2, wallHeight/2],...
        Size=[wallWidth, wallLength, wallHeight],Color=wallColor,IsBinaryOccupied=true);
    addMesh(scenario,"Box",Position=[wallLength/2, wallLength-wallWidth/2, wallHeight/2],...
        Size=[wallLength, wallWidth, wallHeight],Color=wallColor,IsBinaryOccupied=true);
    addMesh(scenario,"Box",Position=[wallLength/2, wallWidth/2, wallHeight/2],...
        Size=[wallLength, wallWidth, wallHeight],Color=wallColor,IsBinaryOccupied=true);
    
    addMesh(scenario,"Box",Position=[wallLength/8, wallLength/3, wallHeight/2],...
        Size=[wallLength/4, wallWidth, wallHeight],Color=wallColor,IsBinaryOccupied=true);
    addMesh(scenario,"Box",Position=[wallLength/4, wallLength/3, wallHeight/2],...
        Size=[wallWidth, wallLength/6,  wallHeight],Color=wallColor,IsBinaryOccupied=true);
    addMesh(scenario,"Box",Position=[(wallLength-wallLength/4), wallLength/2, wallHeight/2],...
       Size=[wallLength/2, wallWidth, wallHeight],Color=wallColor,IsBinaryOccupied=true);
    addMesh(scenario,"Box",Position=[wallLength/2, wallLength/2, wallHeight/2],...
        Size=[wallWidth, wallLength/3, wallHeight],Color=wallColor,IsBinaryOccupied=true);
end
