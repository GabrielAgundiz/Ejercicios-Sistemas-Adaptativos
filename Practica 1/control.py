import threading
import time
import random

class Street:
    def __init__(self, name):
        self.name = name
        self.queue = []

class Intersection:
    def __init__(self, streets):
        self.streets = streets
        self.semaphores = [Semaphore() for _ in streets]

class Semaphore:
    def __init__(self):
        self.green_light = False

    def turn_on(self):
        self.green_light = True

    def turn_off(self):
        self.green_light = False

class Vehicle:
    def __init__(self, name):
        self.name = name

def simulate_traffic(intersection):
    while True:
        # Randommente, algunos vehículos llegan a la intersección y eligen una calle
        time.sleep(random.uniform(0.1, 2.0))
        vehicle = Vehicle(f"Car_{random.randint(1, 100)}")
        street = random.choice(intersection.streets)
        street.queue.append(vehicle)
        print(f"{vehicle.name} arrived at {street.name}")

def control_traffic_lights(intersection):
    while True:
        # Elegir aleatoriamente una calle perpendicular para tener el semáforo verde
        perpendicular_streets = [0, 2]  # Índices de calles perpendiculares
        random.shuffle(perpendicular_streets)
        intersection.semaphores[perpendicular_streets[0]].turn_on()
        intersection.semaphores[perpendicular_streets[1]].turn_off()

        # Calcula la congestión en cada calle y ajusta las luces en consecuencia
        for street, semaphore in zip(intersection.streets, intersection.semaphores):
            if street.queue and not semaphore.green_light:
                semaphore.turn_on()
                print(f"{street.name} is congested. Turning on the green light.")
            elif not street.queue and semaphore.green_light:
                semaphore.turn_off()
                print(f"{street.name} is not congested. Turning off the green light.")

        # Espera antes de realizar el siguiente ajuste de semáforos
        time.sleep(5)

def run_traffic_lights(intersection):
    while True:
        for street, semaphore in zip(intersection.streets, intersection.semaphores):
            if semaphore.green_light:
                print(f"{street.name}'s green light is on. Vehicles passing...")
                if len(street.queue) > 0:
                    street.queue.pop(0)  # Vehicle passes
                time.sleep(1)  # Time for vehicles to pass

def main():
    street1 = Street("Street Up-Down")
    street2 = Street("Street Left-Right")
    street3 = Street("Street Down-Up")
    street4 = Street("Street Right-Left")
    intersection = Intersection([street1, street2, street3, street4])

    # Iniciar hilos para simulación de tráfico y regulación de semáforos
    traffic_simulation_thread = threading.Thread(target=simulate_traffic, args=(intersection,))
    traffic_light_control_thread = threading.Thread(target=control_traffic_lights, args=(intersection,))
    traffic_light_run_thread = threading.Thread(target=run_traffic_lights, args=(intersection,))

    traffic_simulation_thread.start()
    traffic_light_control_thread.start()
    traffic_light_run_thread.start()

    traffic_simulation_thread.join()
    traffic_light_control_thread.join()
    traffic_light_run_thread.join()

if __name__ == "__main__":
    main()
