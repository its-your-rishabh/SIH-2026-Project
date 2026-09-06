import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class ThermoShelterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ThermoShelter AI - Prototype Dashboard")
        self.root.geometry("1100x650")
        self.root.configure(bg="#0f172a")

        # Variables
        self.target_temp = tk.DoubleVar(value=21.0)
        self.thickness = tk.DoubleVar(value=0.15)
        self.ambient_temp = tk.DoubleVar(value=-10.0)

        self.setup_ui()
        self.update_simulation()

    def setup_ui(self):
        # Header Frame (Fixed padding using padx and pady)
        header = tk.Frame(self.root, bg="#1e293b")
        header.pack(fill="x", padx=10, pady=10)

        title = tk.Label(header, text="ThermoShelter AI", font=("Arial", 18, "bold"), fg="#10b981", bg="#1e293b")
        title.pack(anchor="w", padx=10, pady=(10, 2))

        subtitle = tk.Label(
            header, 
            text="SIH26051 | Team Agnit (Team45) | Leader: Mantosh Kumar Chaudhary", 
            font=("Arial", 10), fg="#94a3b8", bg="#1e293b"
        )
        subtitle.pack(anchor="w", padx=10, pady=(0, 10))

        # Main Layout Grid
        main_frame = tk.Frame(self.root, bg="#0f172a")
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Left Column: Inputs
        controls_frame = tk.LabelFrame(main_frame, text=" Control Parameters ", font=("Arial", 11, "bold"), fg="#e2e8f0", bg="#1e293b", bd=1)
        controls_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        tk.Label(controls_frame, text="Target Indoor Temp (°C):", fg="#94a3b8", bg="#1e293b").pack(anchor="w", padx=10, pady=(10, 0))
        temp_spin = tk.Spinbox(controls_frame, from_=10, to=30, increment=0.5, textvariable=self.target_temp, command=self.update_simulation, bg="#0f172a", fg="white")
        temp_spin.pack(fill="x", padx=10, pady=5)

        tk.Label(controls_frame, text="Wall Insulation Thickness (m):", fg="#94a3b8", bg="#1e293b").pack(anchor="w", padx=10, pady=(10, 0))
        thick_slider = tk.Scale(controls_frame, from_=0.05, to=0.40, resolution=0.01, orient="horizontal", variable=self.thickness, command=lambda x: self.update_simulation(), bg="#1e293b", fg="white", highlightthickness=0)
        thick_slider.pack(fill="x", padx=10, pady=5)

        tk.Label(controls_frame, text="Ambient External Temp (°C):", fg="#94a3b8", bg="#1e293b").pack(anchor="w", padx=10, pady=(10, 0))
        amb_spin = tk.Spinbox(controls_frame, from_=-40, to=10, increment=1.0, textvariable=self.ambient_temp, command=self.update_simulation, bg="#0f172a", fg="white")
        amb_spin.pack(fill="x", padx=10, pady=5)

        # Team Details
        team_frame = tk.Frame(controls_frame, bg="#0f172a")
        team_frame.pack(fill="x", padx=10, pady=20)
        tk.Label(team_frame, text="Team Agnit Members:", font=("Arial", 9, "bold"), fg="#10b981", bg="#0f172a").pack(anchor="w", padx=5, pady=2)
        members = ["• Mohd Tokeer Raza", "• Meenakshi Pandey", "• Neha", "• Krishna Gupta", "• Rishabh Upadhyay"]
        for m in members:
            tk.Label(team_frame, text=m, font=("Arial", 8), fg="#94a3b8", bg="#0f172a").pack(anchor="w", padx=5)

        # Center Column: 3D Visualization
        viz_frame = tk.LabelFrame(main_frame, text=" Interactive 3D Thermal Model ", font=("Arial", 11, "bold"), fg="#e2e8f0", bg="#1e293b", bd=1)
        viz_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.fig = plt.Figure(figsize=(5, 4), facecolor="#1e293b")
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_facecolor("#1e293b")
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Right Column: Solver Results
        results_frame = tk.LabelFrame(main_frame, text=" Thermodynamic Solver Output ", font=("Arial", 11, "bold"), fg="#e2e8f0", bg="#1e293b", bd=1)
        results_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        self.lbl_uvalue = tk.Label(results_frame, text="U-Value: -", font=("Arial", 11, "bold"), fg="#e2e8f0", bg="#1e293b")
        self.lbl_uvalue.pack(anchor="w", padx=15, pady=15)

        self.lbl_heatloss = tk.Label(results_frame, text="Total Heat Loss (Q): -", font=("Arial", 11, "bold"), fg="#10b981", bg="#1e293b")
        self.lbl_heatloss.pack(anchor="w", padx=15, pady=15)

        self.lbl_status = tk.Label(results_frame, text="PMV Comfort Zone: -", font=("Arial", 10, "bold"), fg="#38bdf8", bg="#1e293b")
        self.lbl_status.pack(anchor="w", padx=15, pady=15)

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)
        main_frame.columnconfigure(2, weight=1)

    def update_simulation(self):
        t_in = self.target_temp.get()
        t_out = self.ambient_temp.get()
        d = self.thickness.get()

        # Thermodynamic Math: Q = U * A * Delta_T
        k_eps = 0.04 # EPS thermal conductivity W/mK
        u_value = k_eps / d
        area = 48.0 # Total wall surface area (m²)
        delta_t = t_in - t_out
        heat_loss = u_value * area * delta_t

        # Update Labels
        self.lbl_uvalue.config(text=f"Calculated U-Value:\n{u_value:.3f} W/m²K")
        self.lbl_heatloss.config(text=f"Total Heat Loss (Q):\n{heat_loss:.1f} Watts")

        status = "Optimal Comfort" if 18 <= t_in <= 24 else ("Under-heated" if t_in < 18 else "Over-heated")
        color = "#10b981" if status == "Optimal Comfort" else ("#3b82f6" if t_in < 18 else "#ef4444")
        self.lbl_status.config(text=f"Thermal Status:\n{status}", fg=color)

        # Render 3D Box Wireframe
        self.ax.clear()
        self.ax.set_facecolor("#1e293b")

        # Box dimensions
        l, w, h = 4, 3, 2
        vertices = np.array([
            [0,0,0], [l,0,0], [l,w,0], [0,w,0],
            [0,0,h], [l,0,h], [l,w,h], [0,w,h]
        ])
        
        edges = [
            (0,1), (1,2), (2,3), (3,0),
            (4,5), (5,6), (6,7), (7,4),
            (0,4), (1,5), (2,6), (3,7)
        ]

        for e in edges:
            self.ax.plot3D(*zip(*vertices[list(e)]), color=color, linewidth=2)

        self.ax.set_title(f"3D Shelter Heat Map ({t_in}°C)", color="white")
        self.ax.axis('off')
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = ThermoShelterApp(root)
    root.mainloop()
