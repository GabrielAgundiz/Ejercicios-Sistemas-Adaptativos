import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import Label, Entry, Button

class PSOVisualizer:
    def __init__(self, master):
        self.master = master
        master.title("PSO Visualizer")

        self.label_particles = Label(master, text="Número de Partículas:")
        self.label_particles.grid(row=0, column=0)
        self.entry_particles = Entry(master)
        self.entry_particles.grid(row=0, column=1)

        self.label_dimensions = Label(master, text="Número de Dimensiones:")
        self.label_dimensions.grid(row=1, column=0)
        self.entry_dimensions = Entry(master)
        self.entry_dimensions.grid(row=1, column=1)

        self.label_iterations = Label(master, text="Número de Iteraciones:")
        self.label_iterations.grid(row=2, column=0)
        self.entry_iterations = Entry(master)
        self.entry_iterations.grid(row=2, column=1)

        self.run_button = Button(master, text="Ejecutar PSO", command=self.run_pso)
        self.run_button.grid(row=3, column=0, columnspan=2)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=2)

        self.label_best_position = Label(master, text="Mejor Posición:")
        self.label_best_position.grid(row=5, column=0, columnspan=2)

        self.label_best_value = Label(master, text="Mejor Valor:")
        self.label_best_value.grid(row=6, column=0, columnspan=2)

    def objective_function(self, x):
        return x[0]**2 + x[1]**2

    def pso(self, n_particles, n_dimensions, n_iterations):
        w = 0.5
        c1 = 2.0
        c2 = 2.0

        particles = np.random.rand(n_particles, n_dimensions)
        velocities = np.random.rand(n_particles, n_dimensions)
        personal_best_positions = particles.copy()
        personal_best_values = np.zeros(n_particles)

        global_best_position = np.zeros(n_dimensions)
        global_best_value = float('inf')

        best_scores = []

        for iteration in range(n_iterations):
            for i in range(n_particles):
                fitness = self.objective_function(particles[i])

                if fitness < personal_best_values[i]:
                    personal_best_values[i] = fitness
                    personal_best_positions[i] = particles[i]

                if fitness < global_best_value:
                    global_best_value = fitness
                    global_best_position = particles[i]

            best_scores.append(global_best_value)

            for i in range(n_particles):
                r1, r2 = np.random.rand(), np.random.rand()
                velocities[i] = w * velocities[i] + c1 * r1 * (personal_best_positions[i] - particles[i]) + c2 * r2 * (global_best_position - particles[i])
                particles[i] = particles[i] + velocities[i]

        return global_best_position, global_best_value, best_scores

    def run_pso(self):
        num_particles = int(self.entry_particles.get())
        num_dimensions = int(self.entry_dimensions.get())
        num_iterations = int(self.entry_iterations.get())

        best_position, best_value, best_scores = self.pso(num_particles, num_dimensions, num_iterations)

        print("Mejor posición encontrada:", best_position)
        print("Mejor valor encontrado:", best_value)

        # Limpiar el gráfico anterior
        self.ax.clear()

        # Visualización de la convergencia
        self.ax.plot(best_scores, label='Convergencia del PSO')
        self.ax.axhline(y=best_value, color='r', linestyle='--', label='Mejor Valor Final')
        self.ax.legend()
        self.ax.set_ylabel('Mejor Valor')

        # Actualizar el gráfico en la interfaz
        self.canvas.draw()

        # Mostrar la mejor posición y el mejor valor en la interfaz
        self.label_best_position.config(text=f"Mejor Posición: {best_position}")
        self.label_best_value.config(text=f"Mejor Valor: {best_value}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PSOVisualizer(root)
    root.mainloop()
