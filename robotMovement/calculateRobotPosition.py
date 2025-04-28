

def calculateRobotPosition(frontLeftCorner, frontRightCorner, backLeftCorner, backRightCorner):
    if (frontLeftCorner and frontRightCorner and backLeftCorner and backRightCorner):
        forwardsPoint = ( (frontLeftCorner[0] + frontRightCorner[0]) / 2, (frontLeftCorner[1] + frontRightCorner[1]) / 2 )
        backwardsPoint = ( (backLeftCorner[0] + backRightCorner[0]) / 2, (backLeftCorner[1] + backRightCorner[1]) / 2 )
        return (forwardsPoint, backwardsPoint)

    
# Done with chatGPT
# NOTE: Insert default width and height. Should be the pixel distences between corners
def calculateRobotPositionFlexible(frontLeftCorner, frontRightCorner, backLeftCorner, backRightCorner, width=None, height=None):
    # Fill missing corners if possible
    if not frontLeftCorner:
        if frontRightCorner and backLeftCorner:
            frontLeftCorner = (backLeftCorner[0], frontRightCorner[1])
        elif frontRightCorner and backRightCorner:
            frontLeftCorner = (frontRightCorner[0] - width, frontRightCorner[1])
        elif backLeftCorner and backRightCorner:
            frontLeftCorner = (backLeftCorner[0], backLeftCorner[1] + height)
    
    if not frontRightCorner:
        if frontLeftCorner and backRightCorner:
            frontRightCorner = (backRightCorner[0], frontLeftCorner[1])
        elif frontLeftCorner and backLeftCorner:
            frontRightCorner = (frontLeftCorner[0] + width, frontLeftCorner[1])
        elif backLeftCorner and backRightCorner:
            frontRightCorner = (backRightCorner[0], backRightCorner[1] + height)

    if not backLeftCorner:
        if backRightCorner and frontLeftCorner:
            backLeftCorner = (frontLeftCorner[0], backRightCorner[1])
        elif frontLeftCorner and frontRightCorner:
            backLeftCorner = (frontLeftCorner[0], frontLeftCorner[1] - height)
        elif frontRightCorner and backRightCorner:
            backLeftCorner = (backRightCorner[0] - width, backRightCorner[1])

    if not backRightCorner:
        if backLeftCorner and frontRightCorner:
            backRightCorner = (frontRightCorner[0], backLeftCorner[1])
        elif frontLeftCorner and frontRightCorner:
            backRightCorner = (frontRightCorner[0], frontRightCorner[1] - height)
        elif frontLeftCorner and backLeftCorner:
            backRightCorner = (backLeftCorner[0] + width, backLeftCorner[1])

    # Now calculate points
    if (frontLeftCorner and frontRightCorner and backLeftCorner and backRightCorner):
        forwardsPoint = ( (frontLeftCorner[0] + frontRightCorner[0]) / 2, (frontLeftCorner[1] + frontRightCorner[1]) / 2 )
        backwardsPoint = ( (backLeftCorner[0] + backRightCorner[0]) / 2, (backLeftCorner[1] + backRightCorner[1]) / 2 )
        return (forwardsPoint, backwardsPoint)
    else:
        raise ValueError("Not enough information to calculate corners.")