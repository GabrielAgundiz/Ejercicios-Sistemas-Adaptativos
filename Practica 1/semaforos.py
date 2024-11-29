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

def control_traffic_lights(intersection, conflict_matrix):
    while True:
        # Calcula la congestión en cada calle
        congestion = [len(street.queue) for street in intersection.streets]

        for i, semaphore in enumerate(intersection.semaphores):
            if not semaphore.green_light and any(conflict_matrix[i][j] and intersection.semaphores[j].green_light for j in range(len(intersection.semaphores))):
                # No se puede encender este semáforo debido a conflictos con otros semáforos verdes
                continue
            if congestion[i] > 0:
                semaphore.turn_on()
                print(f"{intersection.streets[i].name} is congested. Turning on the green light.")
            else:
                semaphore.turn_off()
                print(f"{intersection.streets[i].name} is not congested. Turning off the green light.")

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

    # Definir la matriz de conflictos
    conflict_matrix = [
        [False, True, False, True],  # Street Up-Down
        [True, False, True, False],  # Street Left-Right
        [False, True, False, True],  # Street Down-Up
        [True, False, True, False],  # Street Right-Left
    ]

    # Iniciar hilos para simulación de tráfico y regulación de semáforos
    traffic_simulation_thread = threading.Thread(target=simulate_traffic, args=(intersection,))
    traffic_light_control_thread = threading.Thread(target=control_traffic_lights, args=(intersection, conflict_matrix))
    traffic_light_run_thread = threading.Thread(target=run_traffic_lights, args=(intersection,))

    traffic_simulation_thread.start()
    traffic_light_control_thread.start()
    traffic_light_run_thread.start()

    traffic_simulation_thread.join()
    traffic_light_control_thread.join()
    traffic_light_run_thread.join()

if __name__ == "__main__":
    main()
