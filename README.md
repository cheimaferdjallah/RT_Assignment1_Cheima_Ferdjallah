# RT_Assignment1_Cheima_Ferdjallah
This solution showcases a basic robotic behavior – using markers and a reference point to navigate, pick up objects, and place them at a specific location.
## Pseudo code
----------------------
```python
Initialize picked_up_markers list
Initialize reference_token as None
Initialize ref_token_code as 0
Initialize threshold distances a_th and d_th

Define drive function(speed, seconds):
    Set robot motors power to speed
    Sleep for seconds duration
    Stop robot motors
Define turn function(speed, seconds):
    Set left motor power to speed
    Set right motor power to -speed
    Sleep for seconds duration
    Stop robot motors

Define find_token function():
    While no markers seen:
        Turn robot right slightly
        If no markers seen:
            Continue loop
    Print number of markers seen
    Initialize marker as None
    Initialize dist to a high value
    Iterate over markers seen:
        If marker is closer than dist and not picked or reference code:
            Update dist, rot_y, and marker
        If marker already picked or reference code:
            Print "Already picked or reference"
            Update marker
    If no marker found or all markers picked:
        Return None, -1, -1
    Else:
        Return marker, its distance, and angle

Define save_reference_token function():
    Find a token using find_token
    If a token is found:
        Set it as reference_token
        Update ref_token_code
        Print "Reference token saved"
    Else:
        Print "No token found"

Define displace_token function():
    Find markers in sight
    Set found_it as False
    Iterate over markers:
        If marker code matches reference code:
            Update reference_token and found_it
            Break loop
    If reference token found:
        While token not displaced:
            Get distance and angle to reference token
            If distance is within threshold:
                Release token and print "Released the token"
                Set found_it to False
                Break loop
            Else:
                Print "Not close enough"
                Adjust robot's position towards reference token
                Recursively call displace_token
    Else:
        Print "Reference token not found"
        Adjust robot's position and call displace_token recursively
        
Main code
Call save_reference_token

Print reference_token code
While true:
    Get token, distance, and angle using find_token
    If no token seen:
        Print "No token found"
        Turn right slightly
    Else, if token within grabbing distance:
        Print "Found it"
        If able to grab token:
            Print "Gotcha!"
            Displace token
            Drive backward
            Turn left
            Append token code to picked_up_markers
            Print picked_up_markers
    Else:
        Print "Not close enough"
        Adjust robot's position towards token
    Adjust robot's position based on angle to token
    If all markers picked:
        Print "Done!"
        Break loop
## How to RUN the code
-----------------------------

After cloning the repositoriy on your machine, you need to navigate to the folder "robot-sim". then you are able to run the code.
To run the script in the simulator, use `run.py`, passing it the file names. 

you can run the program with:

```bash
$ python run.py assignment1.py
```

If you want to check the code you can use `gedit` to see the code structure.

Use the following line :

```bash
$ gedit assignment1.py
```

## Future improvements
-----------------------------

The code can be optimized by making the robot first retrieving the reference token (Box) and relocating it to the center before beginning its search for other tokens. This strategy reduces the time spent searching for the remaining tokens, as positioning the robot in the middle guarantees that all tokens are within its sight.
```
