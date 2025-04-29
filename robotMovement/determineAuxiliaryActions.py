def determineAuxiliaryActions(robotDistance, robotAngle, robotState):
    if robotState == "TO_GOAL":
        if robotDistance <= 100 and robotAngle < 0.2 and robotAngle > -0.2:
            return True
    return False