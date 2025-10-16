import numpy as np
from constrainthg.hypergraph import Hypergraph, Node

def create_beam_model():
    """Creates a simplified beam model hypergraph focused on Timoshenko beam theory."""
    hg = Hypergraph()

    P = Node("point load")
    k = Node("kappa")
    E = Node("youngs modulus")
    I = Node("moment of inertia")
    G = Node("shear modulus")
    A = Node("area")
    L = Node("length")
    theta = Node("theta")

    ### E,V,G Relations ###
    def shear_modulus_from_elastic_poisson(E, V):
        return E / (2 * (1 + V))

    def elastic_modulus_from_shear_poisson(G, V):
        return 2 * G * (1 + V)

    def poisson_from_elastic_shear(E, G):
        return (E / (2 * G)) - 1
    
    ### R,I,A Relations ###
    def area_from_radius(radius):
        return np.pi * radius**2
        
    def radius_from_area(A):
        return np.sqrt(A / np.pi)

    def moment_of_inertia_from_radius(radius):
        return (np.pi / 4) * radius**4

    def radius_from_moment_of_inertia(I):
        return (4 * I / np.pi)**(1/4)
        
    def moment_of_inertia_from_area(A):
        return A**2 / (4 * np.pi)
        
    def area_from_moment_of_inertia(I):
        return np.sqrt(4 * np.pi * I)

    ### Timoshenko Relations ###
    def timoshenko_beam_deflection(P, E, I, L, k, G, A):
        delta_bending = P * L**3 / (3 * E * I)
        delta_shear = P * L / (k * G * A)
        return delta_bending + delta_shear

    def solve_for_P_from_timoshenko(theta, E, I, L, k, G, A):
        return theta / (L**3/(3*E*I) + L/(k*G*A))

    def solve_for_E_from_timoshenko(theta, P, I, L, k, G, A):
        return P * L**3 / (3 * I * (theta - P*L/(k*G*A)))

    def solve_for_I_from_timoshenko(theta, P, E, L, k, G, A):
        return P * L**3 / (3 * E * (theta - P*L/(k*G*A)))

    def solve_for_L_from_timoshenko(theta, P, E, I, k, G, A):
        coeffs = [P/(3*E*I), 0, P/(k*G*A), -theta]
        roots = np.roots(coeffs)
        real_positive_roots = roots[np.isreal(roots) & (roots > 0)]
        if len(real_positive_roots) > 0:
            return real_positive_roots[0]
        else:
            return 0 

    def solve_for_k_from_timoshenko(theta, P, E, I, L, G, A):
        return P * L / (G * A * (theta - P*L**3/(3*E*I)))

    def solve_for_G_from_timoshenko(theta, P, E, I, L, k, A):
        return P * L / (k * A * (theta - P*L**3/(3*E*I)))

    def solve_for_A_from_timoshenko(theta, P, E, I, L, k, G):
        return P * L / (k * G * (theta - P*L**3/(3*E*I)))

    # Add all nodes to the hypergraph
    hg.add_node(P)
    hg.add_node(k)
    hg.add_node(E)
    hg.add_node(I)
    hg.add_node(G)
    hg.add_node(A)
    hg.add_node(L)
    hg.add_node(theta)

    # Core Timoshenko Beam Relations - Direct relationships for beam deflection
    # These represent the fundamental Timoshenko beam equation: θ = f(P, E, I, L, k, G, A)
    hg.add_edge([P, E, I, L, k, G, A], theta, timoshenko_beam_deflection, label='Timoshenko')

    # Inverse relationships for solving for other variables
    # Each equation solves for one variable given the others
    hg.add_edge([theta, E, I, L, k, G, A], P, solve_for_P_from_timoshenko, label='Timoshenko->P')
    hg.add_edge([theta, P, I, L, k, G, A], E, solve_for_E_from_timoshenko, label='Timoshenko->E')
    hg.add_edge([theta, P, E, L, k, G, A], I, solve_for_I_from_timoshenko, label='Timoshenko->I')
    hg.add_edge([theta, P, E, I, k, G, A], L, solve_for_L_from_timoshenko, label='Timoshenko->L')
    hg.add_edge([theta, P, E, I, L, G, A], k, solve_for_k_from_timoshenko, label='Timoshenko->k')
    hg.add_edge([theta, P, E, I, L, k, A], G, solve_for_G_from_timoshenko, label='Timoshenko->G')
    hg.add_edge([theta, P, E, I, L, k, G], A, solve_for_A_from_timoshenko, label='Timoshenko->A')

    return hg