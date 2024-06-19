from djitellopy import Tello

# Initialize the Tello drone
tello = Tello()

# Connecting to the drone
print("Connecting")
tello.connect(False)

# 1  2  3  4  5
#[X][ ][ ][ ][X] 5
#[ ][ ][ ][ ][ ] 4
#[ ][ ][X][ ][ ] 3
#[ ][ ][ ][ ][ ] 2
#[D][ ][ ][ ][X] 1

# Taking off
print("Taking off")
tello.takeoff()


droneX = 0
droneY = 0

def goToX(cordX):
    global droneX
    print("-----------x------------")
    print("Target X cord: " + str(cordX))
    print ("Drone X cord: " + str(droneX))
    target = (droneX - cordX)* (-1)
    print ("Target cord difference: " + str(target))

    if target != 0:
        if target > 0:
            tello.move_right(target*100)
        if target < 0:
            tello.move_left(target*100*-1)
            
    print("Drone moving by: " + str(target*100))
    droneX += target
    
    if droneX == cordX:
        print ("drone is on target cord X: " + str(droneX))


def goToY(cordY):
    global droneY
    global droneX
    print("-----------y------------")
    print ("Target Y cord: " + str(cordY))
    print ("Drone Y cord: " + str(droneY))
    target = (droneY - cordY)* (-1)
    print ("Target cord difference: " + str(target))

    if target != 0:
        if target > 0:
            tello.move_forward(target*100)
        if target < 0:
            tello.move_back(target*100*-1)
    print("Drone moving by: " + str(target*100))        
    droneY += target

    if droneY == cordY:
        print ("drone is on target cord Y: " + str(droneY))
        #tello.flip_forward()
        #droneX += 1
        #print ("flip")

def distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def get_NearestPoint(current_pos, points):
    nearest_point = None
    nearest_distance = float('inf')
    for point in points:
        dist = distance(current_pos, point)
        if dist < nearest_distance:
            nearest_distance = dist
            nearest_point = point
    return nearest_point


while True:
    cmd = input("Enter coordinates (x,y;x,y) (x,y in range of 1;5) or Q to quit, first coordinate is where the drone starts: ")

    if cmd.upper() == "Q":
        break

    input_coords = []
    input_pairs = cmd.split(";")
    for pair in input_pairs:
        x, y = map(int, pair.split(","))
        input_coords.append((x, y))
        if (droneX == 0) and (droneY == 0):
            droneX = x
            droneY = y

    if (droneX, droneY) not in input_coords:
        input_coords.append((droneX, droneY))

    start_pos = (droneX, droneY)

    path = []

    while input_coords:
        current_pos = (droneX, droneY)
        nearest_point = get_NearestPoint(current_pos, input_coords)
        input_coords.remove(nearest_point)
        path.append(nearest_point)
        goToX(nearest_point[0])
        goToY(nearest_point[1])


    goToX(start_pos[0])
    goToY(start_pos[1])
    path.append(start_pos)
    print("----------end-----------")
    print("Visited path:", path)

print("Landing")
tello.land()