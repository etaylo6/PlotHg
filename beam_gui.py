import tkinter as tk
from tkinter import ttk, messagebox
from beam_model import create_beam_model
from plothg import plot_simulation, PlotSettings
from constrainthg.hypergraph import Node

class ToggleSwitch(tk.Canvas):
    """Custom toggle switch widget."""

    def __init__(self, parent, width=60, height=30, command=None, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.command = command
        self.width = width
        self.height = height
        self.state = False

        # Draw the switch
        self.draw_switch()

        # Bind click events
        self.bind("<Button-1>", self.toggle)

    def draw_switch(self):
        """Draw the toggle switch."""
        self.delete("all")

        # Background track
        track_color = "#4CAF50" if self.state else "#cccccc"
        self.create_rounded_rect(2, 2, self.width-2, self.height-2,
                               radius=13, fill=track_color, outline="")

        # Toggle circle
        circle_x = self.width - 15 if self.state else 15
        self.create_oval(circle_x - 11, 4, circle_x + 11, self.height - 4,
                        fill="white", outline="")

    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        """Create a rounded rectangle."""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, **kwargs, smooth=True)

    def toggle(self, event=None):
        """Toggle the switch state."""
        self.state = not self.state
        self.draw_switch()
        if self.command:
            self.command(self.state)

    def set_state(self, state):
        """Set the switch state programmatically."""
        self.state = state
        self.draw_switch()

    def get_state(self):
        """Get the current switch state."""
        return self.state

class BeamSimulationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Beam Model Simulation")
        self.root.geometry("900x600")
        self.root.configure(bg="#f5f5f5")

        # Beam model variables
        self.variables = {
            "point load": {"default": 1000, "unit": "N", "description": "Applied Point Load"},
            "kappa": {"default": 5/6, "unit": "", "description": "Timoshenko Shear Coefficient"},
            "youngs modulus": {"default": 200e9, "unit": "Pa", "description": "Young's Modulus"},
            "moment of inertia": {"default": 1e-6, "unit": "m⁴", "description": "Moment of Inertia"},
            "shear modulus": {"default": 80e9, "unit": "Pa", "description": "Shear Modulus"},
            "area": {"default": 1e-4, "unit": "m²", "description": "Cross-sectional Area"},
            "length": {"default": 2.0, "unit": "m", "description": "Beam Length"},
            "theta": {"default": "", "unit": "m", "description": "Deflection"}
        }

        self.setup_gui()

    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="Beam Model Simulation",
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Create input fields
        self.input_vars = {}

        # Beam parameters frame
        param_frame = ttk.LabelFrame(main_frame, text="Beam Parameters", padding="15")
        param_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        param_frame.columnconfigure(1, weight=1)

        row = 0
        for var_name, info in self.variables.items():
            # Variable name label
            var_label = ttk.Label(param_frame, text=f"{var_name.title()}:")
            var_label.grid(row=row, column=0, sticky=tk.W, pady=5)

            # Input entry
            self.input_vars[var_name] = tk.StringVar(value=str(info["default"]))
            entry = ttk.Entry(param_frame, textvariable=self.input_vars[var_name], width=15)
            entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)

            # Unit label
            unit_label = ttk.Label(param_frame, text=info["unit"])
            unit_label.grid(row=row, column=2, sticky=tk.W, padx=(10, 0))

            row += 1

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0))

        run_btn = ttk.Button(button_frame, text="Run Beam Simulation", command=self.run_simulation)
        run_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Status
        self.status_label = ttk.Label(main_frame, text="Ready to run beam simulation")
        self.status_label.grid(row=3, column=0, columnspan=2, pady=(10, 0))

    def run_simulation(self):
        """Run the beam model simulation."""
        try:
            # Get inputs
            inputs = {}
            for var_name, var_info in self.variables.items():
                if var_name != "theta":  # Don't include target in inputs
                    try:
                        value = float(self.input_vars[var_name].get())
                        inputs[var_name] = value
                    except ValueError:
                        messagebox.showerror("Error", f"Invalid number for {var_name}")
                        return

            self.status_label.config(text="Creating beam model...")
            self.root.update()

            # Create the beam model
            hg = create_beam_model()

            self.status_label.config(text="Running simulation...")
            self.root.update()

            # Create target node (theta - deflection)
            target_node = Node("theta")

            # Run the simulation
            plot_simulation(hg, PlotSettings(), inputs, target_node, search_depth=1000)

            self.status_label.config(text="Beam simulation completed!")

        except Exception as e:
            messagebox.showerror("Error", f"Simulation failed: {str(e)}")
            self.status_label.config(text="Simulation failed")

def main():
    root = tk.Tk()
    app = BeamSimulationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
