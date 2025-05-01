# CDIO
CDIO project for DTU course 62410

Notes to remember:
ball image recognition using colors is fairly vulnerable to changes in lighting and distance of camera from balls.



TODO software-wise: 
- [X] Obstacle Avoidance (Anders working on this)
- [ ] Ball Selection Optimization(Smartly select what ball the robot should currently pursue)(Maybe?)
- [ ] When and how to switch from normal ball pursuing behavior to "ball close to corner" behavior (Using grabber helper etc.) (Probably good to use the state machine
    to change into specific state altering robot behavior specifically to get ball from corner)(Christian working on this)
- [ ] Interpolation (Simon working on this)
- [ ] Optimization of the basic robot movement that takes robot from A to B, aka the PID (Try optimizing how fast/slow it turns and drives etc.) 
- [ ] Testing of robot missing corner calculations (Possibly by visualization).
- [ ] Error handling(Prevent program from crashing). Program crashes in several different scenarios, known ones are:
    1) robot corners blocked from camera. Calculation of robotPos (in robotMovement/selectRobotTarget.py) crashes
    2) if field is not detected the calculation of intermediary point (in robotMovement/selectRobotTarget.py) crashes
    3)
- [ ] Test whether robot can do hand-in of many balls (6-8+) or if it stops the grabber early. (If it does, 
    it might be due to balls reappearing and the robot switching back to collection mode) fix by only considering balls for collection when inside play field
- [ ] Save ball positions such that if target ball dissapears for a second robot moves to its old location (Some type 
    of persistance of target when balls things dissapear)
- [ ] Figure out when it makes sense for robot to drive instead of just turning (For example if ball is 180 degrees behind it). Calculate optimal point.


TODO Imagerecognition-wise:
- [ ] Take more pictures to make model better. OBS: include pictures with balls very close to cross.
- [ ] Include pictures with balls partially covered. Include pictures in different light(sunlight vs darkness)
- [ ] Test accuracy and speed of different models, f.eks. large vs medium model, or model trained on 200 epochs vs model trained on 100. 


TODO Hardware-wise:
Group discussion about whether we should try the overhead belt collection method - If yes, build it
