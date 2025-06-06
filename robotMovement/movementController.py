import numpy as np
import time


errorForward = 0.1
errorAngleToTarget = 0.1
kd = 0.1
previous_error_forward = 0
previous_error_angle_to_target = 0
previous_time = time.time()

def getTurnSpeed(angleToTarget: float):
    return max(-100, min(100, angleToTarget**3*40+angleToTarget*50)) # x^(3)*40+x*50

# PID controller
def calculateSpeedAndRotation(distanceFromTarget, angleToTarget, state):
    global previous_error_forward, previous_error_angle_to_target, previous_time
    if distanceFromTarget == None or angleToTarget == None:
        return (0, 0)
    # Robot should drive differently depending on state.


    if state == "SEARCH_BALLS":
        # Proportionality constants. Tune to change how fast speed changes
        kp_speed = 0.2

        errorForward = distanceFromTarget - goalDistanceFromBall
        errorAngleToTarget = angleToTarget
        dt = time.time() - previous_time

        DForward = kd * (errorForward - previous_error_forward)  / dt
        DTurn = kd * (errorAngleToTarget - previous_error_angle_to_target) / dt

        goalDistanceFromBall = 20
        # Assuming that we use MoveSteering().on(steering, speed), the values range from -100 to 100, adjust below values accordingly
        forwardSpeed = max(5, min(100, kp_speed * (distanceFromTarget - goalDistanceFromBall)) + DForward)
        turnSpeed = getTurnSpeed(angleToTarget) + DTurn

        previous_error_angle_to_target = errorAngleToTarget
        previous_time = time.time()
        previous_error_forward = errorForward

    elif state == "TO_INTERMEDIARY":
        kp_speed = 0.2

        goalDistanceFromBall = 10

        errorForward = distanceFromTarget - goalDistanceFromBall
        errorAngleToTarget = angleToTarget
        dt = time.time() - previous_time

        DForward = kd * (errorForward - previous_error_forward)  / dt
        DTurn = kd * (errorAngleToTarget - previous_error_angle_to_target) / dt

        forwardSpeed = max(40, min(100, kp_speed * (distanceFromTarget - goalDistanceFromBall)) + DForward)
        turnSpeed = getTurnSpeed(angleToTarget) + DTurn

        previous_error_angle_to_target = errorAngleToTarget
        previous_time = time.time()
        previous_error_forward = errorForward

    elif state == "TO_GOAL":
        kp_speed = 0.2

        errorForward = distanceFromTarget - goalDistanceFromBall
        errorAngleToTarget = angleToTarget

        dt = time.time() - previous_time
        previous_time = time.time()

        DForward = kd * (errorForward - previous_error_forward)  / dt
        DTurn = kd * (errorAngleToTarget - previous_error_angle_to_target) / dt

        goalDistanceFromBall = 100
        forwardSpeed = max(0, min(100, kp_speed * (distanceFromTarget - goalDistanceFromBall)) + DForward)
        turnSpeed = getTurnSpeed(angleToTarget) + DTurn

        previous_error_forward = errorForward 
        previous_error_angle_to_target = errorAngleToTarget


    return (turnSpeed, forwardSpeed)
