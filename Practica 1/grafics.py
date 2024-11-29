import tkinter as tk
import threading
import time
import random

class Street:
    def __init__(self, name, x1, y1, x2, y2, direction):
        self.name = name
        self.queue = []
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.direction = direction

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
    def __init__(self, name, direction):
        self.name = name
        self.direction = direction

def simulate_traffic(intersection):
    while True:
        time.sleep(random.uniform(0.1, 2.0))
        direction = random.choice(["↓←", "→↓", "↑→", "←↑"])
        vehicle = Vehicle(f"Car_{random.randint(1, 100)}", direction)
        street = random.choice(intersection.streets)
        street.queue.append(vehicle)
        update_ui(intersection)  # Actualiza la interfaz gráfica

def control_traffic_lights(intersection):
    while True:
        horizontal_streets = [0, 2]
        vertical_streets = [1, 3]
        
        random.shuffle(horizontal_streets)
        random.shuffle(vertical_streets)

        # Verificar conflictos y encender semáforos en consecuencia
        if horizontal_streets[0] in [0, 2]:
            intersection.semaphores[0].turn_on()
            intersection.semaphores[2].turn_on()
            intersection.semaphores[1].turn_off()
            intersection.semaphores[3].turn_off()
        else:
            intersection.semaphores[1].turn_on()
            intersection.semaphores[3].turn_on()
            intersection.semaphores[0].turn_off()
            intersection.semaphores[2].turn_off()
            
        for i, (street, semaphore) in enumerate(zip(intersection.streets, intersection.semaphores)):
            if street.queue and not semaphore.green_light:
                semaphore.turn_on()
            elif not street.queue and semaphore.green_light:
                semaphore.turn_off()
                
        update_ui(intersection)

        time.sleep(2)

def run_traffic_lights(intersection):
    while True:
        for street, semaphore in zip(intersection.streets, intersection.semaphores):
            if semaphore.green_light and len(street.queue) > 0:
                street.queue.pop(0)
        update_ui(intersection)
        time.sleep(1)

def update_ui(intersection):
    canvas.delete("all")
    
    for i, street in enumerate(intersection.streets):
        canvas.create_rectangle(street.x1, street.y1, street.x2, street.y2, fill="gray")
        
        # Calcular las coordenadas del texto descriptivo
        if street.direction == "↓←":
            text_x = street.x2 - 80
            text_y = (street.y1 + street.y2) / 2
        elif street.direction == "→↓":
            text_x = (street.x1 + street.x2) / 2
            text_y = street.y2 - 50
        elif street.direction == "↑→":
            text_x = street.x1 + 90
            text_y = (street.y1 + street.y2) / 2
        elif street.direction == "←↑":
            text_x = (street.x1 + street.x2) / 2
            text_y = street.y1 + 50
        
        canvas.create_text(text_x, text_y, text=f"{street.name}\nQueue: {len(street.queue)}")
        
        # Agregar lógica para representar semáforos según el estado de Semaphore.green_light
        semaphore_color = "green" if street.semaphore.green_light else "red"
        
        if street.direction == "↓←":
            semaphore_x1 = (street.x1 + street.x2) / 2 - 20
            semaphore_y1 = (street.y1 + street.y2) / 2 - 10
            semaphore_x2 = (street.x1 + street.x2) / 2 + 20
            semaphore_y2 = (street.y1 + street.y2) / 2 + 10
        elif street.direction == "→↓":
            semaphore_x1 = (street.x1 + street.x2) / 2 - 10
            semaphore_y1 = (street.y1 + street.y2) / 2 - 20
            semaphore_x2 = (street.x1 + street.x2) / 2 + 10
            semaphore_y2 = (street.y1 + street.y2) / 2 + 20
        elif street.direction == "↑→":
            semaphore_x1 = (street.x1 + street.x2) / 2 - 20
            semaphore_y1 = (street.y1 + street.y2) / 2 - 10
            semaphore_x2 = (street.x1 + street.x2) / 2 + 20
            semaphore_y2 = (street.y1 + street.y2) / 2 + 10
        elif street.direction == "←↑":
            semaphore_x1 = (street.x1 + street.x2) / 2 - 10
            semaphore_y1 = (street.y1 + street.y2) / 2 - 20
            semaphore_x2 = (street.x1 + street.x2) / 2 + 10
            semaphore_y2 = (street.y1 + street.y2) / 2 + 20
        
        canvas.create_rectangle(semaphore_x1, semaphore_y1, semaphore_x2, semaphore_y2, fill=semaphore_color)
        
        for j in range(len(street.queue)):
            if street.direction == "↓←":
                canvas.create_oval((street.x1 + street.x2) / 2 - 10, street.y1 + 20 + j * 30, (street.x1 + street.x2) / 2 + 10, street.y1 + 30 + j * 30, fill="blue")
            elif street.direction == "→↓":
                canvas.create_oval(street.x1 + 20 + j * 30, (street.y1 + street.y2) / 2 - 10, street.x1 + 30 + j * 30, (street.y1 + street.y2) / 2 + 10, fill="blue")
            elif street.direction == "↑→":
                canvas.create_oval((street.x1 + street.x2) / 2 - 10, street.y2 - 30 - j * 30, (street.x1 + street.x2) / 2 + 10, street.y2 - 20 - j * 30, fill="blue")
            elif street.direction == "←↑":
                canvas.create_oval(street.x2 - 30 - j * 30, (street.y1 + street.y2) / 2 - 10, street.x2 - 20 - j * 30, (street.y1 + street.y2) / 2 + 10, fill="blue")

if __name__ == "__main__":
    horizontal1 = Street("Street Up-Down", 150, 0, 170, 400, "↓←")
    horizontal2 = Street("Street Down-Up", 250, 0, 270, 400, "↑→")
    vertical1 = Street("Street Left-Right", 0, 150, 400, 170, "→↓")
    vertical2 = Street("Street Right-Left", 0, 250, 400, 270, "←↑")
    
    intersection = Intersection([horizontal1, horizontal2, vertical1, vertical2])

    root = tk.Tk()
    root.title("Traffic Simulation")

    canvas = tk.Canvas(root, width=500, height=500)
    canvas.pack()

    horizontal1.semaphore = intersection.semaphores[0]
    horizontal2.semaphore = intersection.semaphores[1]
    vertical1.semaphore = intersection.semaphores[2]
    vertical2.semaphore = intersection.semaphores[3]

    traffic_simulation_thread = threading.Thread(target=simulate_traffic, args=(intersection,))
    traffic_light_control_thread = threading.Thread(target=control_traffic_lights, args=(intersection,))
    traffic_light_run_thread = threading.Thread(target=run_traffic_lights, args=(intersection,))

    traffic_simulation_thread.start()
    traffic_light_control_thread.start()
    traffic_light_run_thread.start()

    root.mainloop()
