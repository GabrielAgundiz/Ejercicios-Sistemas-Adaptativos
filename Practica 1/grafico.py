import tkinter as tk
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
        time.sleep(random.uniform(0.1, 2.0))
        vehicle = Vehicle(f"Car_{random.randint(1, 100)}")
        street = random.choice(intersection.streets)
        street.queue.append(vehicle)
        update_ui()  # Actualiza la interfaz gráfica

def control_traffic_lights(intersection):
    while True:
        perpendicular_streets = [0, 2]
        random.shuffle(perpendicular_streets)
        intersection.semaphores[perpendicular_streets[0]].turn_on()
        intersection.semaphores[perpendicular_streets[1]].turn_off()

        for street, semaphore in zip(intersection.streets, intersection.semaphores):
            if street.queue and not semaphore.green_light:
                semaphore.turn_on()
            elif not street.queue and semaphore.green_light:
                semaphore.turn_off()
                
        update_ui()

        time.sleep(5)

def run_traffic_lights(intersection):
    while True:
        for street, semaphore in zip(intersection.streets, intersection.semaphores):
            if semaphore.green_light and len(street.queue) > 0:
                street.queue.pop(0)
                update_ui()
        time.sleep(1)

def update_ui():
    canvas.delete("all")
    for i, street in enumerate(intersection.streets):
        x1, y1, x2, y2 = 50, 100 * (i + 1), 250, 100 * (i + 1)
        canvas.create_rectangle(x1, y1, x2, y2)
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f"{street.name}\nQueue: {len(street.queue)}")
        
        for j in range(len(street.queue)):
            canvas.create_oval(30 + j * 30, (y1 + y2) / 2 - 10, 40 + j * 30, (y1 + y2) / 2 + 10, fill="blue")

if __name__ == "__main__":
    street1 = Street("Street Up-Down")
    street2 = Street("Street Left-Right")
    street3 = Street("Street Down-Up")
    street4 = Street("Street Right-Left")
    intersection = Intersection([street1, street2, street3, street4])

    root = tk.Tk()
    root.title("Traffic Simulation")

    canvas = tk.Canvas(root, width=400, height=600)
    canvas.pack()

    traffic_simulation_thread = threading.Thread(target=simulate_traffic, args=(intersection,))
    traffic_light_control_thread = threading.Thread(target=control_traffic_lights, args=(intersection,))
    traffic_light_run_thread = threading.Thread(target=run_traffic_lights, args=(intersection,))

    traffic_simulation_thread.start()
    traffic_light_control_thread.start()
    traffic_light_run_thread.start()

    root.mainloop()
