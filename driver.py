import math
import random
import csv

engine_file = "engines.txt"
tire_file = "tires.txt"
transmission_file = "transmissions.txt"
valid_cars_file = "valid_book.csv"

valid_cars = set()
class Car:
    def __init__(self, engine, tire, transmission, roof):
        self.transmission = transmission
        self.engine = engine
        self.tire = tire
        self.roof = roof

    def __eq__(self, car):
        return car.engine == self.engine and car.tire == self.tire and car.transmission == self.transmission and car.roof == self.roof

    def __hash__(self):
        return hash((self.engine, self.tire, self.transmission, self.roof))

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

def get_probability(delta_e, level):
    return math.e ** (delta_e / level)

def hill_climbing_with_simulated_annealing(start_car, goal_car, engines,transmissions,tires, roofs, valid_cars):
    current_car = start_car
    level = 0
    states = []
    while current_car != goal_car:
        delta_values = []

        if current_car.engine != goal_car.engine:
            level +=1
            for engine in engines:
                candidate_car = Car(engine, current_car.tire, current_car.transmission, current_car.roof)
                if candidate_car in valid_cars:
                    delta = delta_e(current_car, candidate_car, goal_car)
                    delta_values.append((candidate_car, delta))

        if current_car.transmission != goal_car.transmission:
            level += 1
            for transmission in transmissions:
                candidate_car = Car(transmission,current_car.engine,current_car.tire,current_car.roof)
                if candidate_car in valid_cars:
                    delta = delta_e(current_car,candidate_car,goal_car)
                    delta_values.append((candidate_car,delta))

        if current_car.tire != goal_car.tire:
            level += 1
            for tire in tires:
                candidate_car = Car(tire,current_car.engine,current_car.transmission,current_car.roof)
                if candidate_car in valid_cars:
                    delta = delta_e(current_car,candidate_car,goal_car)
                    delta_values.append((candidate_car,delta))

        if current_car.roof != goal_car.roof:
            level += 1
            for roof in roofs:
                candidate_car = Car(roof,current_car.engine, current_car.tire, current_car.transmission)
                if candidate_car in valid_cars:
                    delta = delta_e(current_car,candidate_car,goal_car)
                    delta_values.append((candidate_car,delta))

        if not delta_values:
            print("No valid candidates at level:", level)
            break

        delta_values.sort(key=lambda x: x[1], reverse=True)


        if delta_values[0][1] <= 0:
            probability = get_probability(delta_values[0][1], 1 / level)
            if random.uniform(0, 1) > probability:
                break
        
        current_car = goal_car

    return goal_car, level



engines = content_reader(engine_file)
transmissions = content_reader(transmission_file)
tires = content_reader(tire_file)
roofs = ["Sunroof", "Moonroof", "Noroof"]

start_car = Car("EFI", "Danlop", "AT", "Noroof")
goal_car = Car("V12", "Pirelli", "CVT", "Noroof")

load_cars(valid_cars_file)

best_state, years = hill_climbing_with_simulated_annealing(start_car, goal_car, engines, transmissions, tires, roofs, valid_cars)
print("Best state:", best_state.engine,",",best_state.tire,",",best_state.transmission,",",best_state.roof)
print("Minimum number of years:", years)
