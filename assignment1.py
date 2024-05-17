from __future__ import print_function
import time
from sr.robot import *

# Initialize the list of picked markers
picked_up_markers = []

# The token the robot is programmed to gather the rest of the tokens at
reference_token = None
ref_token_code = 0  # Alternative to using reference_token.info.code

# Threshold distance and angle for token grabbing
a_th = 2.0
d_th = 0.4

R = Robot()

def drive(speed, seconds):
    """Drive the robot forward at a given speed for a specified duration"""
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """Turn the robot at a given speed for a specified duration"""
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_token():
    """Look for tokens and return the nearest one's distance, angle, and marker"""
    global picked_up_markers, ref_token_code
    dist = 100
    markers = R.see()

    while not markers:
        turn(20, 0.2)
        print("I turned right to look for markers!")
        markers = R.see()

    print("I can see", len(markers), "markers:")
    marker = None

    for token in markers:
        if token.dist < dist and (token.info.code not in picked_up_markers) and (token.info.code != ref_token_code):
            dist = token.dist
            rot_y = token.rot_y
            marker = token
        elif (token.info.code in picked_up_markers) or (token.info.code == ref_token_code):
            print("I already picked up this token or it's the reference code")
            marker = token

    if (dist == 100) or (marker.info.code in picked_up_markers) or (marker.info.code == ref_token_code):
        return None, -1, -1
    else:
        return marker, dist, rot_y

def save_reference_token():
    """Save one of the tokens as the reference token for later calculations"""
    global reference_token, ref_token_code
    marker, _, _ = find_token()
    if marker:
        reference_token = marker
        ref_token_code = reference_token.info.code
        print("Reference token saved:", ref_token_code)
    else:
        print("No token found to save as reference.")

def displace_token():
    """Displace the grabbed token to the reference token"""
    global reference_token
    markers = R.see()
    found_it = False

    for marker in markers:
        if reference_token.info.code == marker.info.code:
            reference_token = marker
            found_it = True
            break

    if found_it:
        while found_it:
            dist = reference_token.dist
            rot_y = reference_token.rot_y

            if dist < d_th + 0.3:
                print("Arrived at reference!")
                R.release()
                print("Released the token")
                found_it = False
                break
            else:
                print("Aww, I'm not close enough.")

            if -a_th <= rot_y <= a_th:
                print("Ah, that'll do.")
                drive(55, 0.5)
            elif rot_y < -a_th:
                print("Turning left...")
                turn(-2, 0.5)
            elif rot_y > a_th:
                print("Turning right...")
                turn(2, 0.5)
            displace_token()
    else:
        print("I don't see the reference token")
        drive(20, 0.5)
        turn(20, 0.5)
        displace_token()

# Main code

save_reference_token()

print("The reference token is:", reference_token)

while True:
    token, dist, rot_y = find_token()

    if dist == -1:
        print("I don't see any token!")
        turn(+15, 1)
    elif dist < d_th:
        print("I found it!")
        if R.grab():
            print("Gotcha!")
            displace_token()
            drive(-45, 1)
            turn(-40, 1)
            picked_up_markers.append(token.info.code)
            print("Picked up markers:", picked_up_markers)
    else:
        print("Aww, I'm not close enough.")

    if -a_th <= rot_y <= a_th:
        print("Ah, that'll do.")
        drive(45, 0.5)
    elif rot_y < -a_th:
        print("Turning left...")
        turn(-2, 0.5)
    elif rot_y > a_th:
        print("Turning right...")
        turn(2, 0.5)

    if len(picked_up_markers) == 5:
        print("Done!")
        break

