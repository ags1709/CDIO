def determineAuxiliaryActions(robotDistance, robotAngle, robotState):
    if robotState == "TO_GOAL":
        if robotDistance <= 110:
            return True
    return False