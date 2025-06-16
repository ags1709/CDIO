def determineAuxiliaryActions(robotDistance, robotAngle, robotState):
    if robotState == "TO_GOAL":
        if robotDistance <= 100:
            return True
    return False