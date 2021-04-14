# Installation and execution

Updated code can be found in the [gitlab repo](https://github.com/majstenmark/stereo2).

The program can be simulated in ABB RobotStudio on Windows:

* Install [ABB RobotStudio 2019.5](https://new.abb.com/products/robotics/robotstudio/downloads) or later.
* Open one of the Pack and Go files TableMounted.rspag or Inverted.rspag
* Open the virtual Flexpendant and the menu button, select the Stereo2 app. 
* Press 'Raise' to go to the initial position. 
* Press 'Run Experiment' to execute the test.

## Installation on physical robot system.
* Tested with RobotWare 6.10.01.
* Load the Data.mod and MainModule.mod for both T_ROB_R and T_ROB_L from the virtual controller (TableMounted or Inverted) to the physical system.
* Use File Transfer to copy TpsViewStereo2.dll, TpsViewStereo2.gtpu.dll, TpsViewStereo2.pdb from the FPApp folder of the virtual robot system. The GUI will be loaded when the Flexpendant is restarted using the reset button on the back of the FlexPendant, or when the entire system is warmstarted. 
* If the robot is inverted, change the gravitation parameters: Go to Configuration -> Motion -> Robot and change the __Gravity Alpha__ and __Gravity Beta__ for ROB_L to 0.629233 and -2.19094 and for ROB_R -0.629233 and -2.19094. Warmstart the system.
* Test the app by press __Raise__ and wait until the robot has raised its arms. 

## Calibrate cameras
* Attach the cameras to the adaptor plates and attach the plates to the robot.
* Connect cameras to a computer and place calibration grid in view. 
* Press the gear icon to open the settings menu, select __1.Go to start__.
* Adjust the calibration the calibration grid position to where the crosshairs should align.
* In the jogging menu, select tCamL/tCamR as tool and *rotate* the cameras until the crosshairs align. 
* Update the left and the right tool with the buttons in the app. This will update the tooldata.


## The application
Each of the buttons in the code will execute RAPID routines on both arms. 

* The robot has a *store* position with tighly crossed arms, move in and out of the position by pressing __To store pos__ and __From store pos__ (RAPID routines __gotobatpos__ and __gofrombatpos__). 
* For each experiment, __Go to start__ will move the robot into the start position and the __1100 mm__ and __1400 mm__ buttons will run the 1100 and the 1400 measurements respectively. Note that the focus point is moved down and the radius is increased, so the height is not changed (RAPID routines __goto1100__, __goto1400__, __run1100__ and __run1400__). 
* __Run Experiment__ will execute both series in sequence (RAPID routines __runall__).
* The __Play/Pause__ button will continue or stop the robot at the current position.  
* Open the settings menu by pressing the gear icon.
* Adjust the height and the x distance from the robot using the plus and minus symbols, each adjustment with step 1 mm, __++__ and __--__ changes the distance with steps of size 5 mm (RAPID routines __inc__, __incinc__, __dec__ and __decdec__ will adjust the z position of the __wobjHeart__, __incX__, __incincX__, __decX__, __decdecX__ adjusts the x position of the __wobjHeart__). 
* The X1 moves the robot into the first position with 50 mm separation, X2 moves the robot into position 15, 190 mm (routines __gotoX1__ and __gotoX2__). 

## The code
* The T_ROB_R/Data.mod has the data for the variables used in the program, here you can edit __wobjHeart__, the __distances__, the radius (__nRadius__) and the waittime (__nWaittime__) and convergence positions (__convergencePos__).


## Debugging
* If the robot position cannot be reached, jog the robot in the wobjHeart workobject to make sure that the robot can reach the desired position with the desired orientation.