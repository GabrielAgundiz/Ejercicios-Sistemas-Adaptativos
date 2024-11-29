import numpy as np
import matplotlib.pyplot as plt

def objective_function(x):
    return x[0]**2 + x[1]**2

def pso(n_particles, n_dimensions, n_iterations):
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
            fitness = objective_function(particles[i])
 
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

if __name__ == "__main__":
    num_particles = 30
    num_dimensions = 2
    num_iterations = 100

    best_position, best_value, best_scores = pso(num_particles, num_dimensions, num_iterations)

    print("Mejor posición encontrada:", best_position)
    print("Mejor valor encontrado:", best_value)

    # Visualización de la convergencia
    plt.plot(best_scores)
    plt.title('Convergencia del PSO')
    plt.xlabel('Iteración')
    plt.ylabel('Mejor Valor')
    plt.show()
