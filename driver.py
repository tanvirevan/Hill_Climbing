import math

engine_file = "engines.txt"
tire_file = "tires.txt"
transmission_file = "transmissions.txt"
valid_cars_file = "valid_book.csv"
import random
import csv
valid_cars = set()
class Car:
    def __init__(self, engine, tire, transmission, roof):
        self.transmission = transmission
        self.engine = engine
        self.tire = tire
        self.roof = roof

    def __eq__(self, car):
        return car.engine == self.engine and car.tire == self.tire and car.transmission == self.transmission and car.roof == self.roof



def load_cars(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for engine, tire, transmission, roof in reader:
            valid_cars.add(Car(engine, tire, transmission, roof))




def content_reader(filename):
    with open(filename) as file:
        container = [line.rstrip() for line in file]
        return container

# compare with the target
# car2 -> target
def compare_with_target(car1, car2):
    num_mismatched = 0
    if car1.transmission != car2.transmission:
        num_mismatched += 1
    if car1.engine != car2.engine:
        num_mismatched += 1
    if car1.tire != car2.tire:
        num_mismatched += 1
    if car1.roof != car2.roof:
        num_mismatched += 1
    return num_mismatched

def delta_e(parent_car, child_car, target):
    return compare_with_target(parent_car, target) - compare_with_target(child_car, target)

def get_e(delta_e, level):
    return math.e ** (delta_e / level)


engines = content_reader(engine_file)
transmission = content_reader(transmission_file)
tires = content_reader(tire_file)
roofs = ["Sunroof", "Moonroof", "Noroof"]

start_car = Car("EFI","Danlop", "AT", "Noroof")

goal_car = Car("V12", "Pirelli", "CVT", "Sunroof")

from collections import deque
frontier = deque()
level = -1
seen = set()
seen.add(start_car)
frontier.append(start_car)
goal_reached = False
while frontier:
    level += 1
    # explore the current level
    while frontier:
        current_car = frontier.popleft()
        current_engine = current_car.engine
        current_tire = current_car.tire
        current_transmission = current_car.transmission
        current_roof = current_car.roof
        children = deque()
        for engine in engines:
            candidate_car = Car(engine, current_tire, current_transmission, current_roof)
            if candidate_car not in seen and candidate_car in valid_cars:
                if candidate_car == goal_car:
                    print(level + 1)
                    goal_reached = True
                    break
                # check if this candidate_car is worthy: calculate delta E
                # if delta E > 0 just pick the child
                # if delta E <= 0 pick the child with some probability
                # random.uniform(0, 1) <=  get_e(delta_e, 1 / level)
                children.append(candidate_car)
                seen.add(candidate_car)
        # one for transmission
        # one for tire
        # one for roof
        if goal_reached:
            break
        
    if goal_reached:
        break

print(level + 1)
