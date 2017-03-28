# This simulator will generate a model
# to simulate the real traffic in a city


import turtle
import random
import time
import pygame
import math


# Initialization
pygame.init()

window_height = 600
window_width = 600

update_interval = 30
# The direction is to be...not the current situation
traffic_direction_north_south = True
#traffic_time_scale_to_update = 50  # How much we should wait for a light change
traffic_time = 0
traffic_time_red_update = 50    # How long is the red light
traffic_time_green_update = 50  # How long is the green light

# Traffic Lights [up, down, left, right]
light_pair_number = 4

red_lights = []
red_light_position_x = [70, -70, -100, 100]
red_light_position_y = [100,-100, 70, -70]

green_lights = []
green_light_position_x = [20, -20, -100, 100]
green_light_position_y = [100,-100, 20, -20]

# Minimum Allow Distance between cars
min_dist_between_car_vertical = 100
min_dist_between_car_horizontal = 50
collision_factor_for_speed = 2.5

# Cars
car_max_num = 20
car_start_num = 1
cars = []

car_start_position_x = [45,-45,-1000,1000]
car_start_position_y = [1000,-1000,45,-45]

CAR_SPEED = 35
time_to_create_car = 20

# Get the number of cars waiting for the red lights on different direction
#car_num_waiting_north = 0
#car_num_waiting_south = 0
#car_num_waiting_west = 0
#car_num_waiting_east = 0

# Car Class
class Car(turtle.Turtle):
    def __init__(self, _isWaiting = False, _waitingFor = -1):
        super(Car, self).__init__()
        self.isWaiting = _isWaiting
        self.waitingFor = _waitingFor

    # True if is waiting; False if not
    def setWaiting(self, _isWaiting):
        self.isWaiting = _isWaiting
        if(not _isWaiting):
            self.waitingFor = -1
        
    def getWaiting(self):
        return self.isWaiting

    # -1 if not waiting/horizontal waiting; 0,1,2,3 for N,S,W,E
    def setWaitingFor(self, _waitingFor):
        self.waitingFor = _waitingFor
        
    def getWaitingFor(self):
        return self.waitingFor


turtle.addshape("car_toNorth.gif")
turtle.addshape("car_toSouth.gif")
turtle.addshape("car_toEast.gif")
turtle.addshape("car_toWest.gif")


##### APIs for external usage #####

# Set the time for green light and red light on North-South direction
# @param greenTime (Integer) The time lasted for green lights on North-South direction
# @param redTime (Integer) The time lasted for red lights on North-South direction
def set_traffic_time_green_red_north_south(greenTime, redTime):
    global traffic_time_green_update
    global traffic_time_red_update
    traffic_time_green_update = greenTime
    traffic_time_red_update = redTime


# Get the total number of cars waiting behind the red lights on each direction
# @return [num_north, num_south, num_west, num_east] (List of Integer)
def get_car_num_waiting():
    # Initialization
    car_num_waiting_north = 0
    car_num_waiting_south = 0
    car_num_waiting_west = 0
    car_num_waiting_east = 0
    
    for i in range(len(cars)):
        curCar = cars[i]
        if(curCar.getWaitingFor() == 0):
            car_num_waiting_north += 1
        elif(curCar.getWaitingFor() == 1):
            car_num_waiting_south += 1
        elif(curCar.getWaitingFor() == 2):
            car_num_waiting_west += 1
        elif(curCar.getWaitingFor() == 3):
            car_num_waiting_east += 1
            
    return [car_num_waiting_north, car_num_waiting_south, car_num_waiting_west, car_num_waiting_east]


# Get the total number of cars
# @return num_of_cars (Integer)
def get_car_num_total():
    return len(cars)

##### End of APIs for external usage #####


# Implementation

def exec_traffic_direction():
    global traffic_direction_north_south
    #global car_num_waiting_north
    #global car_num_waiting_south
    #global car_num_waiting_west
    #global car_num_waiting_east

    # Set the car waiting number to 0
    #car_num_waiting_north = 0
    #car_num_waiting_south = 0
    #car_num_waiting_west = 0
    #car_num_waiting_east = 0
    
    if traffic_direction_north_south:
        red_lights[0].hideturtle()
        red_lights[1].hideturtle()
        green_lights[2].hideturtle()
        green_lights[3].hideturtle()
        
        red_lights[2].showturtle()
        red_lights[3].showturtle()
        green_lights[0].showturtle()
        green_lights[1].showturtle()
        
        # Set to opposite direction
        traffic_direction_north_south = False  
        
    else:
        red_lights[2].hideturtle()
        red_lights[3].hideturtle()
        green_lights[0].hideturtle()
        green_lights[1].hideturtle()
        
        red_lights[0].showturtle()
        red_lights[1].showturtle()
        green_lights[2].showturtle()
        green_lights[3].showturtle()
        
        # Set to opposite direction
        traffic_direction_north_south = True  


def createCar(_direction, _speed = 30, isNew = True):

    global car_start_position_x
    global car_start_position_y
       
     # Create a new car
    car = Car()
    car.hideturtle()       # Hide the image
    
    # Set the car direction
    if(_direction == 0):    # go south
        car.setheading(270)
        car.shape("car_toSouth.gif")
    elif(_direction == 1):  # go north
        car.setheading(90)
        car.shape("car_toNorth.gif")
    elif(_direction == 2):  # go east
        car.setheading(0)
        car.shape("car_toEast.gif")
    else:                   # go west
        car.setheading(180)
        car.shape("car_toWest.gif")
        
    # Move the car to the starting position
    car.speed(0)
    car.up()              # Hide moving trace
    car.goto(car_start_position_x[_direction], car_start_position_y[_direction])  # Set position

    car.showturtle()       # Show the image

    car.speed(_speed)
    
    if(isNew):
        cars.append(car)     # Collect control back

    if(willCollide(car, car.xcor(), car.ycor())):
        restartCar(car)

def restartCar(car):

    global car_start_position_x
    global car_start_position_y
    
    car.hideturtle()       # Hide the image

    _direction = random.randint(0,3)   # Generate random direction
    
    # Set the car direction
    if(_direction == 0):    # go south
        car.setheading(270)
        
        car.shape("car_toSouth.gif")
    elif(_direction == 1):  # go north
        car.setheading(90)
        car.shape("car_toNorth.gif")
    elif(_direction == 2):  # go east
        car.setheading(0)
        car.shape("car_toEast.gif")
    else:                   # go west
        car.setheading(180)
        car.shape("car_toWest.gif")

    # Move the car to the starting position
    car.speed(0)
    car.up()              # Hide moving trace
    car.goto(car_start_position_x[_direction], car_start_position_y[_direction])  # Set position
           
    car.showturtle()       # Show the image

    _speed = random.randint(20,30)
    car.speed(_speed)

    if(willCollide(car, car.xcor(), car.ycor())):
        restartCar(car)

# Check if a collision will happen
# call by willCollide(curCar, curCar.xcor() + 10, curCar.ycor())
def willCollide(curCar, nextX, nextY):
    for i in range(len(cars)):
        neiCar = cars[i]
        
        if not (curCar == neiCar):
            dist = math.hypot(nextX - neiCar.xcor(), nextY - neiCar.ycor())
            # Check Neighbor Car
            # Same direction or opposite
            if (curCar.heading() % 180 == neiCar.heading() % 180):
                # Same direction and collide
                if ((curCar.heading() == neiCar.heading()) and (dist <= min_dist_between_car_vertical)):
                    #print("might vertical collide")
                    # It waits for the same light its front car waiting for
                    curCar.setWaitingFor(neiCar.getWaitingFor())
                    return True
            elif (dist <= min_dist_between_car_horizontal):
                curCar.setWaitingFor(-1)
                #print("might horizontal collide")
                return True
    # No Collision
    return False

def updateScreen():

    global traffic_direction_north_south
    global traffic_time_scale_to_update
    global traffic_time
    global time_to_create_car
    #global car_num_waiting_north
    #global car_num_waiting_south
    #global car_num_waiting_west
    #global car_num_waiting_east


    # Control the traffic time
    traffic_time += 1
    
    # When North-South is green(to be red), and the traffic time reach green's limit
    # OR when North-South is red(to be green), and the traffic time reach red's limit
    if ((traffic_time >= traffic_time_green_update) and not traffic_direction_north_south) or ((traffic_time >= traffic_time_red_update) and traffic_direction_north_south):
        traffic_time = 0
        # Control the traffic lights
        exec_traffic_direction()

    # Create random car
    if ((traffic_time % time_to_create_car == 0) and (len(cars) < car_max_num)):
        print("Create new car!")
        rand_dir = random.randint(0,3)
        createCar(rand_dir,30)  # given direction


    # Move the cars
    for i in range(len(cars)):
        curCar = cars[i]

        if (curCar.heading() == 270.0):  # Head South
            if ((curCar.ycor() < 200) and (curCar.ycor() > 100) and (red_lights[0].isvisible())):
                #if(not curCar.getWaiting()):
                    #car_num_waiting_north += 1    # Wait at north
                # Stop the car
                curCar.setWaiting(True)
                curCar.setWaitingFor(0)
            elif (curCar.ycor() < -350):  # Cancel car when out of sight
                restartCar(curCar)
            else:
                if(not willCollide(curCar, curCar.xcor(), curCar.ycor() - CAR_SPEED * collision_factor_for_speed)):
                    curCar.forward(CAR_SPEED)
                    curCar.setWaiting(False)

        elif (curCar.heading() == 90.0):  # Head North
            if ((curCar.ycor() < -100) and (curCar.ycor() > -200) and (red_lights[1].isvisible())):
                #if(not curCar.getWaiting()):
                    #car_num_waiting_south += 1    # Wait at south
                # Stop the car
                curCar.setWaiting(True)
                curCar.setWaitingFor(1)
            elif (curCar.ycor() > 350):  # Cancel car when out of sight
                restartCar(curCar)
            else:
                if(not willCollide(curCar, curCar.xcor(), curCar.ycor() + CAR_SPEED * collision_factor_for_speed)):
                    curCar.forward(CAR_SPEED)
                    curCar.setWaiting(False)
                
        elif (curCar.heading() == 0.0):  # Head East
            if ((curCar.xcor() < -100) and (curCar.xcor() > -200) and (red_lights[2].isvisible())):
                #if(not curCar.getWaiting()):
                    #car_num_waiting_west += 1    # Wait at west
                # Stop the car
                curCar.setWaiting(True)
                curCar.setWaitingFor(2)
            elif (curCar.xcor() > 350):  # Cancel car when out of sight
                restartCar(curCar)
            else:
                if(not willCollide(curCar, curCar.xcor() + CAR_SPEED * collision_factor_for_speed, curCar.ycor())):
                    curCar.forward(CAR_SPEED)
                    curCar.setWaiting(False)
                
        elif (curCar.heading() == 180.0):  # Head West 
            if ((curCar.xcor() < 200) and (curCar.xcor() > 100) and (red_lights[3].isvisible())):
                #if(not curCar.getWaiting()):
                    #car_num_waiting_east += 1    # Wait at east
                # Stop the car
                curCar.setWaiting(True)
                curCar.setWaitingFor(3)
            elif (curCar.xcor() < -350):  # Cancel car when out of sight
                restartCar(curCar)
            else:
                if(not willCollide(curCar, curCar.xcor() - CAR_SPEED * collision_factor_for_speed, curCar.ycor())):
                    curCar.forward(CAR_SPEED)
                    curCar.setWaiting(False)
                  
        else:
            curCar.forward(CAR_SPEED)


    # Update Interface
    score_text.clear()
    wait_list = get_car_num_waiting()
    wait_list_str = str(wait_list[0]) + " " + str(wait_list[1]) + " " + str(wait_list[2]) + " " + str(wait_list[3]) + "\n"
    score_text.write(wait_list_str, font=("Arial", 20, "bold"), align="center")
    score_text.write("\nTotal: " + str(get_car_num_total()), font=("Arial", 20, "bold"), align="center")
        

    # Update the screen for every time interval
    turtle.update()
    turtle.ontimer(updateScreen, update_interval)


def startSimulation():

    traffic_direction_north_south = True
    exec_traffic_direction()
    
    updateScreen()

    # Create cars
    rand_dir = random.randint(0,3)
    createCar(rand_dir, 30)

    

# Entry
turtle.setup(window_width, window_height) # Set the window size
turtle.bgpic(picname="intersection2.gif") # Set the background picture

# Create traffic lights
turtle.addshape("redLight.gif")
turtle.addshape("greenLight.gif")

# Red Lights
for ind in range(light_pair_number):
    redLit = turtle.Turtle()  # Create a new red light
    redLit.hideturtle()       # Hide the image
    redLit.speed(0)
    redLit.shape("redLight.gif")  # Provide image source
    redLit.up()               # Hide moving trace
    redLit.goto(red_light_position_x[ind], red_light_position_y[ind])  # Set position
    #redLit.showturtle()       # Show the image [Don't Show the lights at begin]
    
    red_lights.append(redLit)     # Collect control back

# Green Lights
for ind in range(light_pair_number):
    greenLit = turtle.Turtle()  # Create a new red light
    greenLit.hideturtle()       # Hide the image
    greenLit.speed(0)
    greenLit.shape("greenLight.gif")  # Provide image source
    greenLit.up()               # Hide moving trace
    greenLit.goto(green_light_position_x[ind], green_light_position_y[ind])  # Set position
    #greenLit.showturtle()       # Show the image [Don't Show the lights at begin]
    
    green_lights.append(greenLit)     # Collect control back


# Interface
score_text=turtle.Turtle()
score_text.up()
score_text.hideturtle()
score_text.goto(250, 250)


# Start!!!
startSimulation()


turtle.update()


turtle.done()
    
