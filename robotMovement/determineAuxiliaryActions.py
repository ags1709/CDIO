def determineAuxiliaryActions(robotDistance, robotAngle, robotState):
    if robotState == "TO_GOAL":
        if robotDistance <= 140:
            return True
    return False