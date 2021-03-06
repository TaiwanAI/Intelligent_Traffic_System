# This simulator will generate a model
# to simulate the real traffic in a city


import turtle
import random
import time
import pygame
import math
from qlearningAgents import QLearningAgent
import sys

# Default to be 1000
sys.setrecursionlimit(1500)

# Initialization
SOUTH = 0
NORTH = 1
EAST = 2
WEST = 3
pygame.init()


window_height = 600
window_width = 600
times = [5,2,1,0,-1,-2,-5]
#all actions (red, green)

actionFn = lambda x: actions
learner = QLearningAgent(actionFn=actionFn)

lastAction = None
update_interval = 1
# The direction is to be...not the current situation
traffic_direction_north_south = True
#traffic_time_scale_to_update = 50  # How much we should wait for a light change
traffic_time = 0
traffic_time_red_update = 50    # How long is the red light
traffic_time_green_update = 50  # How long is the green light
state = None
oldState = None
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
min_dist_between_car_horizontal = 80
collision_factor_for_speed = 2.5

# Cars
car_max_num = 10
car_start_num = 1
cars = []

car_start_position_x = [45,-45,-1000,1000]
car_start_position_y = [1000,-1000,45,-45]

CAR_SPEED = 30
time_to_create_car = 10


# Cool Initialization
rate_of_car_on_NS = 0.5
interface_cache = [0,0,0,0,0,[0,0]]    # total, north, south, west, east, [NS,WE]
time_pin = 0    # To count the time of simulation
congest_rate_array = []
average_congest_rate = 0


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

def tune_traffic_time_green_red_north_south(greenUpdateTime, redUpdateTime):
    global traffic_time_green_update
    global traffic_time_red_update
    if((greenUpdateTime > redUpdateTime) and (traffic_time_green_update / float(traffic_time_red_update) < 3.0)) or\
        ((greenUpdateTime < redUpdateTime) and (traffic_time_red_update / float(traffic_time_green_update) < 3.0)):                            
        traffic_time_green_update += greenUpdateTime
        traffic_time_red_update += redUpdateTime

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

# Get the total number of cars on NS & WE directions:
def get_car_num_NS_WE():
    NS_num = 0
    WE_num = 0
    for car in cars:
        if (car.heading() % 180 == 90):     # NS
            NS_num += 1
        else:
            WE_num += 1
            
    return [NS_num, WE_num]


##### End of APIs for external usage #####


# Implementation

def getRandDir0to3():
    rate = random.uniform(0, 2)     # Generate a float between 0 and 2
    if(rate > 1):
        rate -= 1
        if(rate > rate_of_car_on_NS):
            return EAST
        else:
            return SOUTH
    else:
        if(rate > rate_of_car_on_NS):
            return WEST
        else:
            return NORTH

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
    if(_direction == SOUTH):    # go south
        car.setheading(270)
        car.shape("car_toSouth.gif")
    elif(_direction == NORTH):  # go north
        car.setheading(90)
        car.shape("car_toNorth.gif")
    elif(_direction == EAST):  # go east
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

    car.setWaiting(False)   # Waiting for none
    car.hideturtle()       # Hide the image

    #_direction = random.randint(0,3)   # Generate random direction
    _direction = getRandDir0to3()
    
    # Set the car direction
    if(_direction == SOUTH):    # go south
        car.setheading(270)
        
        car.shape("car_toSouth.gif")
    elif(_direction == NORTH):  # go north
        car.setheading(90)
        car.shape("car_toNorth.gif")
    elif(_direction == EAST):  # go east
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

# Simulate as the real traffic pattern
# Each traffic switch takes around 55 time_pin
def realMode():
    global time_pin
    global rate_of_car_on_NS

    # Traffic Pattern Control
    if(time_pin < 300):
        rate_of_car_on_NS = 0.5
    elif(time_pin < 600):
        rate_of_car_on_NS = 0.9
    elif(time_pin < 900):
        rate_of_car_on_NS = 0.1
    else:
        rate_of_car_on_NS = 0.5

    # Light Time Control
    # 1/6 chance to update
    toRandChange = random.randint(0,5)
    if(toRandChange == 0):
        if(time_pin < 320):
            tune_traffic_time_green_red_north_south(0, 0)
        elif(time_pin < 620):
            tune_traffic_time_green_red_north_south(1, -1)
        elif(time_pin < 920):
            tune_traffic_time_green_red_north_south(-2, 2)
        else:
            tune_traffic_time_green_red_north_south(1, -1)
    

def updateScreen():
    

    global traffic_direction_north_south
    global traffic_time_scale_to_update
    global traffic_time
    global time_to_create_car
    global timeCounter
    global oldState
    global state
    global lastAction
    global lightswitch
    global time_pin
    global rate_of_car_on_NS
    global average_congest_rate
    
    #global car_num_waiting_north
    #global car_num_waiting_south
    #global car_num_waiting_west
    #global car_num_waiting_east
    
    
   
        
    # Control the traffic time
    traffic_time += 1
    
    # When North-South is green(to be red), and the traffic time reach green's limit
    # OR when North-South is red(to be green), and the traffic time reach red's limit
    if ((traffic_time >= traffic_time_green_update) and not traffic_direction_north_south) or ((traffic_time >= traffic_time_red_update) and traffic_direction_north_south):
        

        
        # Control the traffic lights
        if((traffic_time >= traffic_time_green_update) and not traffic_direction_north_south):
            currentState = tuple(get_car_num_waiting() + [traffic_time_red_update, traffic_time_green_update])
            if(oldState == None):
                oldState = currentState
            else:
                oldStateSum = sum(oldState[:4])
                currentStateSum = sum(currentState[:4])
                reward = (oldStateSum - currentStateSum)
                learner.observeTransition(oldState, lastAction, currentState, reward)
            lastAction = learner.getAction(currentState)
            redLightTune, greenLightTune = lastAction
            tune_traffic_time_green_red_north_south(greenLightTune, redLightTune)
            #print (redLightTune, greenLightTune)
        
        traffic_time = 0
        exec_traffic_direction()


    # Create random car
    if ((traffic_time % time_to_create_car == 0) and (len(cars) < car_max_num)):
        #print("Create new car!")
        #rand_dir = random.randint(0,3)
        createCar(getRandDir0to3(),30)  # given direction

    # Move the cars
    for i in range(len(cars)):
        curCar = cars[i]

        if (curCar.heading() == 270.0):  # Head South
            if ((curCar.ycor() < 200) and (curCar.ycor() > 150) and (red_lights[0].isvisible())):
                #if(not curCar.getWaiting()):
                    #car_num_waiting_north += 1    # Wait at north
                # Stop the car
                #curCar.setWaiting(True)
                curCar.setWaitingFor(0)
            elif (curCar.ycor() < -350):  # Cancel car when out of sight
                restartCar(curCar)
            else:
                if(not willCollide(curCar, curCar.xcor(), curCar.ycor() - CAR_SPEED * collision_factor_for_speed)):
                    curCar.forward(CAR_SPEED)
                    #curCar.setWaiting(False)

        elif (curCar.heading() == 90.0):  # Head North
            if ((curCar.ycor() < -150) and (curCar.ycor() > -200) and (red_lights[1].isvisible())):
                #if(not curCar.getWaiting()):
                    #car_num_waiting_south += 1    # Wait at south
                # Stop the car
                #curCar.setWaiting(True)
                curCar.setWaitingFor(1)
            elif (curCar.ycor() > 350):  # Cancel car when out of sight
                restartCar(curCar)
            else:
                if(not willCollide(curCar, curCar.xcor(), curCar.ycor() + CAR_SPEED * collision_factor_for_speed)):
                    curCar.forward(CAR_SPEED)
                    #curCar.setWaiting(False)
                
        elif (curCar.heading() == 0.0):  # Head East
            if ((curCar.xcor() < -150) and (curCar.xcor() > -200) and (red_lights[2].isvisible())):
                #if(not curCar.getWaiting()):
                    #car_num_waiting_west += 1    # Wait at west
                # Stop the car
                #curCar.setWaiting(True)
                curCar.setWaitingFor(2)
            elif (curCar.xcor() > 350):  # Cancel car when out of sight
                restartCar(curCar)
            else:
                if(not willCollide(curCar, curCar.xcor() + CAR_SPEED * collision_factor_for_speed, curCar.ycor())):
                    curCar.forward(CAR_SPEED)
                    #curCar.setWaiting(False)
                
        elif (curCar.heading() == 180.0):  # Head West 
            if ((curCar.xcor() < 200) and (curCar.xcor() > 150) and (red_lights[3].isvisible())):
                #if(not curCar.getWaiting()):
                    #car_num_waiting_east += 1    # Wait at east
                # Stop the car
                #curCar.setWaiting(True)
                curCar.setWaitingFor(3)
            elif (curCar.xcor() < -350):  # Cancel car when out of sight
                restartCar(curCar)
            else:
                if(not willCollide(curCar, curCar.xcor() - CAR_SPEED * collision_factor_for_speed, curCar.ycor())):
                    curCar.forward(CAR_SPEED)
                    #curCar.setWaiting(False)
                  
        #else:
            #curCar.forward(CAR_SPEED)


    # Update Interface
    congest_list = get_car_num_waiting()
    car_num_total = get_car_num_total()
    car_num_NS_WE = get_car_num_NS_WE()
    
    congest_num_total = 0
    for i in range(len(congest_list)):
        congest_num_total += congest_list[i]
    
    if (car_num_total != 0):
        congest_rate = congest_num_total / float(car_num_total)
    else:
        congest_rate = 0.00
    # Add to the history (not too frequent)
    if(time_pin % 10 == 0):
        if len(congest_rate_array) > 10:
            congest_rate_array.pop(0)   # avoid exceeding
        congest_rate_array.append(congest_rate)

    if(interface_cache[0] != car_num_total):
        interface_cache[0] = car_num_total
        total_car_num.clear()
        total_car_num.write("\nTotal Cars: " + str(interface_cache[0]), font=("Arial", 16, "bold"), align="left")

    if(interface_cache[1] != congest_list[0]):
        interface_cache[1] = congest_list[0]
        north_congest_num.clear()
        if(interface_cache[1] != 0):
            north_congest_num.write(str(congest_list[0]), font=("Arial", 20, "bold"), align="center")

    if(interface_cache[2] != congest_list[1]):
        interface_cache[2] = congest_list[1]
        south_congest_num.clear()
        if(interface_cache[2] != 0):
            south_congest_num.write(str(congest_list[1]), font=("Arial", 20, "bold"), align="center")

    if(interface_cache[3] != congest_list[2]):
        interface_cache[3] = congest_list[2]
        west_congest_num.clear()
        if(interface_cache[3] != 0):
            west_congest_num.write(str(congest_list[2]), font=("Arial", 20, "bold"), align="center")

    if(interface_cache[4] != congest_list[3]):
        interface_cache[4] = congest_list[3]
        east_congest_num.clear()
        if(interface_cache[4] != 0):
            east_congest_num.write(str(congest_list[3]), font=("Arial", 20, "bold"), align="center")

    if(interface_cache[5] != car_num_NS_WE):
        interface_cache[5] = car_num_NS_WE
        NS_WE_car_num.clear()
        NS_WE_car_num.write("North - South Cars: " + str(interface_cache[5][0]) +\
                            "\nWest - East Cars: " + str(interface_cache[5][1]) +\
                            "\nCongest Rate: " + "%.1f" % (average_congest_rate * 100) + "%",\
                            font=("Arial", 16, "bold"), align="left")
                            # "\nCongest Rate: " + "%.1f" % (congest_rate * 100) + "%" +\
        

    # Update the screen for every time interval
    time_pin += 1
    if(time_pin % 50 == 0):
        
        average_congest_rate = sum(congest_rate_array) / float(len(congest_rate_array))
        
        print "time_pin: " + str(time_pin)
        print "Rate of car (NS): " + str(rate_of_car_on_NS)
        print "Red Light Time (NS): " + str(traffic_time_red_update)
        print "Green Light Time (NS):" + str(traffic_time_green_update)
        print "Average Congest Rate:" + "%.1f" % (average_congest_rate * 100) + "%"
        print "---------------------------------------------------\n"
    realMode()
    
    turtle.update()
    turtle.ontimer(updateScreen, update_interval)


def startSimulation():

    traffic_direction_north_south = True
    exec_traffic_direction()
    
    updateScreen()

    # Create cars
    #rand_dir = random.randint(0,3)
    createCar(getRandDir0to3(), 30)

    

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
total_car_num=turtle.Turtle()
total_car_num.up()
total_car_num.hideturtle()
total_car_num.goto(120, 270)

NS_WE_car_num=turtle.Turtle()
NS_WE_car_num.up()
NS_WE_car_num.hideturtle()
NS_WE_car_num.goto(120, 210)

north_congest_num=turtle.Turtle()
north_congest_num.up()
north_congest_num.hideturtle()
north_congest_num.goto(70, 90)
#north_congest_num.write("0", font=("Arial", 20, "bold"), align="center")

south_congest_num=turtle.Turtle()
south_congest_num.up()
south_congest_num.hideturtle()
south_congest_num.goto(-70, -110)
#south_congest_num.write("0", font=("Arial", 20, "bold"), align="center")

west_congest_num=turtle.Turtle()
west_congest_num.up()
west_congest_num.hideturtle()
west_congest_num.goto(-100, 60)
#west_congest_num.write("0", font=("Arial", 20, "bold"), align="center")

east_congest_num=turtle.Turtle()
east_congest_num.up()
east_congest_num.hideturtle()
east_congest_num.goto(100, -80)
#east_congest_num.write("0", font=("Arial", 20, "bold"), align="center")

slider_bar=turtle.Turtle()
slider_bar.up()
slider_bar.hideturtle()
slider_bar.goto(-120, 270)

# Start!!!
startSimulation()


turtle.update()


turtle.done()
    
