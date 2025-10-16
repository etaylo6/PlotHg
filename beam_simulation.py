from beam_model import create_beam_model
from plothg import plot_simulation, PlotSettings
from constrainthg.hypergraph import Node

def run_beam_simulation():
    """Creates a beam model and runs a simulation with plotting."""
    
    # Create the beam model hypergraph
    hg = create_beam_model()
    
    # Define input values for the beam simulation
    # These represent known values in a beam problem
    inputs = {
        "youngs modulus": 200e9,      # 200 GPa (steel)
        "moment of inertia": 1e-6,    # 1e-6 m^4
        "length": 2.0,                # 2 meters
        "kappa": 5/6,                 # Timoshenko shear coefficient
        "shear modulus": 80e9,        # 80 GPa
        "area": 1e-4,                 # 1e-4 m^2 (10 cm^2)
        "point load": 1000            # 1000 N
    }
    
    # Define the target node to solve for (deflection)
    target_node = Node("theta")
    
    # Create plot settings
    ps = PlotSettings()
    
    # Run the simulation with plotting
    print("Running beam simulation...")
    print("Input values:")
    for key, value in inputs.items():
        print(f"  {key}: {value}")
    print(f"Target: {target_node.label}")
    
    plot_simulation(hg, ps, inputs, target_node, search_depth=1000)

if __name__ == "__main__":
    run_beam_simulation()
