# This simulator will generate a model
# to simulate the real traffic in a city


import turtle
import random
import time
import pygame


# Initialization
pygame.init()

window_height = 600
window_width = 600

update_interval = 30

traffic_direction_north_south = True
traffic_time_scale_to_update = 50  # How much we should wait for a light change
traffic_time = 0

# Traffic Lights [up, down, left, right]
light_pair_number = 4

red_lights = []
red_light_position_x = [70, -70, -100, 100]
red_light_position_y = [100,-100, 70, -70]

green_lights = []
green_light_position_x = [20, -20, -100, 100]
green_light_position_y = [100,-100, 20, -20]


# Cars
car_max_num = 5
car_start_num = 1
cars = []

car_start_position_x = [45,-45,-300,300]
car_start_position_y = [300,-300,45,-45]

CAR_SPEED = 25
time_to_create_car = 20


# Car Class
class Car(turtle.Turtle):
    def __init__(self):
        super(Car, self).__init__()


turtle.addshape("car_toNorth.gif")
turtle.addshape("car_toSouth.gif")
turtle.addshape("car_toEast.gif")
turtle.addshape("car_toWest.gif")

# Implementation

def exec_traffic_direction():
    global traffic_direction_north_south
    
    if traffic_direction_north_south:
        red_lights[0].hideturtle()
        red_lights[1].hideturtle()
        green_lights[2].hideturtle()
        green_lights[3].hideturtle()
        
        red_lights[2].showturtle()
        red_lights[3].showturtle()
        green_lights[0].showturtle()
        green_lights[1].showturtle()
        
        traffic_direction_north_south = False  # Set to opposite direction
        
    else:
        red_lights[2].hideturtle()
        red_lights[3].hideturtle()
        green_lights[0].hideturtle()
        green_lights[1].hideturtle()
        
        red_lights[0].showturtle()
        red_lights[1].showturtle()
        green_lights[2].showturtle()
        green_lights[3].showturtle()
        
        traffic_direction_north_south = True  # Set to opposite direction


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
    

def updateScreen():

    global traffic_direction_north_south
    global traffic_time_scale_to_update
    global traffic_time
    global time_to_create_car

    # Control the traffic time
    traffic_time += 1
    if traffic_time >= traffic_time_scale_to_update:
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

        #if ((curCar.heading() == 0.0) and (curCar.xcor() < )):  # Head East

        if (curCar.heading() == 270.0):  # Head South
            if ((curCar.ycor() < 200) and (curCar.ycor() > 100) and (red_lights[0].isvisible())):        
                curCar.forward(0)
            elif (curCar.ycor() < -350):
                rand_dir = random.randint(0,3)
                restartCar(curCar)
            else:
                curCar.forward(CAR_SPEED)

        elif (curCar.heading() == 90.0):  # Head North
            if ((curCar.ycor() < -100) and (curCar.ycor() > -200) and (red_lights[1].isvisible())):
                curCar.forward(0)
            elif (curCar.ycor() > 350):
                rand_dir = random.randint(0,3)
                restartCar(curCar)
            else:
                curCar.forward(CAR_SPEED)
                
        elif (curCar.heading() == 0.0):  # Head East
            if ((curCar.xcor() < -100) and (curCar.xcor() > -200) and (red_lights[2].isvisible())):  
                curCar.forward(0)
            elif (curCar.xcor() > 350):
                rand_dir = random.randint(0,3)
                restartCar(curCar)
            else:
                curCar.forward(CAR_SPEED)
                
        elif (curCar.heading() == 180.0):  # Head West 
            if ((curCar.xcor() < 200) and (curCar.xcor() > 100) and (red_lights[3].isvisible())):         
                curCar.forward(0)
            elif (curCar.xcor() < -350):
                rand_dir = random.randint(0,3)
                restartCar(curCar)
            else:
                curCar.forward(CAR_SPEED)
                  
        else:
            curCar.forward(CAR_SPEED)
        

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
    redLit.showturtle()       # Show the image
    
    red_lights.append(redLit)     # Collect control back

# Green Lights
for ind in range(light_pair_number):
    greenLit = turtle.Turtle()  # Create a new red light
    greenLit.hideturtle()       # Hide the image
    greenLit.speed(0)
    greenLit.shape("greenLight.gif")  # Provide image source
    greenLit.up()               # Hide moving trace
    greenLit.goto(green_light_position_x[ind], green_light_position_y[ind])  # Set position
    greenLit.showturtle()       # Show the image
    
    green_lights.append(greenLit)     # Collect control back


# Start!!!
startSimulation()


turtle.update()


turtle.done()
    
