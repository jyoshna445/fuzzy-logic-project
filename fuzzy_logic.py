import tkinter as tk
from tkinter import ttk
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Patch
import random

# ===== FUZZY =====
density_range = np.arange(0, 101, 1)
time_range = np.arange(10, 61, 1)

def create_fuzzy_system(roads):
    rules = []
    for r in roads:
        d = ctrl.Antecedent(density_range, f'density_{r}')
        d['low'] = fuzz.trimf(density_range, [0, 0, 50])
        d['medium'] = fuzz.trimf(density_range, [25, 50, 75])
        d['high'] = fuzz.trimf(density_range, [50, 100, 100])

        g = ctrl.Consequent(time_range, f'green_time_{r}')
        g['short'] = fuzz.trimf(time_range, [10, 10, 25])
        g['medium'] = fuzz.trimf(time_range, [20, 35, 50])
        g['long'] = fuzz.trimf(time_range, [40, 60, 60])

        rules += [
            ctrl.Rule(d['low'], g['short']),
            ctrl.Rule(d['medium'], g['medium']),
            ctrl.Rule(d['high'], g['long'])
        ]

    return ctrl.ControlSystem(rules)

# ===== GUI =====
class TrafficGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Smart Traffic Control System")
        self.root.geometry("1000x750")
        self.root.configure(bg="#1e272e")

        self.roads = []
        self.entries = {}
        self.lights = {}
        self.times = {}
        self.current_index = 0
        self.after_id = None

        # TITLE
        tk.Label(root, text="AI SMART TRAFFIC CONTROL SYSTEM",
                 fg="#00cec9", bg="#1e272e",
                 font=("Segoe UI", 18, "bold")).pack(pady=10)

        # MODE
        top = tk.Frame(root, bg="#1e272e")
        top.pack()

        tk.Label(top, text="Junction:", fg="white", bg="#1e272e").pack(side=tk.LEFT)

        self.mode = ttk.Combobox(top,
            values=["2-Way","4-Way","6-Way"], width=10)
        self.mode.current(1)
        self.mode.pack(side=tk.LEFT, padx=10)

        ttk.Button(top, text="Apply", command=self.setup_inputs).pack(side=tk.LEFT)

        # EMERGENCY
        self.emergency = tk.BooleanVar()
        tk.Checkbutton(root, text="🚑 Emergency Mode",
                       variable=self.emergency,
                       bg="#1e272e", fg="#00cec9",
                       selectcolor="#2d3436").pack()

        # INPUT
        self.input_frame = tk.Frame(root, bg="#1e272e")
        self.input_frame.pack(pady=10)

        # BUTTONS
        btn = tk.Frame(root, bg="#1e272e")
        btn.pack()

        tk.Button(btn, text="Start Simulation",
                  bg="#00b894", fg="white",
                  command=self.calculate).pack(side=tk.LEFT, padx=5)

        tk.Button(btn, text="🎲 Random Traffic",
                  bg="#0984e3", fg="white",
                  command=self.generate_random).pack(side=tk.LEFT, padx=5)

        tk.Button(btn, text="Clear",
                  bg="#d63031", fg="white",
                  command=self.clear).pack(side=tk.LEFT)

        # STATUS
        self.status = tk.StringVar()
        tk.Label(root, textvariable=self.status,
                 fg="#fdcb6e", bg="#1e272e",
                 font=("Segoe UI", 11, "bold")).pack(pady=5)

        # TRAFFIC CONDITION
        self.condition = tk.StringVar()
        tk.Label(root, textvariable=self.condition,
                 fg="#55efc4", bg="#1e272e",
                 font=("Segoe UI", 11, "bold")).pack(pady=5)

        # SIGNAL FRAME
        self.signal_frame = tk.Frame(root, bg="#2d3436")
        self.signal_frame.pack(pady=10)

        # GRAPH
        self.fig, self.ax = plt.subplots(figsize=(8,3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.setup_inputs()

    def setup_inputs(self):
        for w in self.input_frame.winfo_children():
            w.destroy()

        mode = self.mode.get()

        if mode == "2-Way":
            self.roads = ['A','B']
        elif mode == "4-Way":
            self.roads = ['A','B','C','D']
        else:
            self.roads = ['A','B','C','D','E','F']

        self.entries = {}

        for i,r in enumerate(self.roads):
            tk.Label(self.input_frame, text=f"Road {r}",
                     bg="#1e272e", fg="white").grid(row=i,column=0)

            e = tk.Entry(self.input_frame)
            e.grid(row=i,column=1)
            e.insert(0,"0")
            self.entries[r] = e

        self.system = create_fuzzy_system(self.roads)

    def generate_random(self):
        for r in self.roads:
            val = random.randint(0,100)
            self.entries[r].delete(0, tk.END)
            self.entries[r].insert(0, str(val))

    def create_signals(self):
        for w in self.signal_frame.winfo_children():
            w.destroy()

        self.lights = {}
        container = tk.Frame(self.signal_frame, bg="#2d3436")
        container.pack()

        for r in self.roads:
            f = tk.Frame(container, bg="#2d3436", bd=2, relief="solid")
            f.pack(side=tk.LEFT, padx=15)

            tk.Label(f, text=r, fg="white", bg="#2d3436").pack()

            c = tk.Canvas(f, width=120, height=140, bg="black")
            c.pack()

            red = c.create_oval(40,10,80,40, fill="red")
            yellow = c.create_oval(40,50,80,80, fill="gray")
            green = c.create_oval(40,90,80,120, fill="gray")

            self.lights[r] = (c, red, yellow, green)

    def run_cycle(self):
        r = self.roads[self.current_index]

        for road in self.roads:
            c, red, _, green = self.lights[road]

            if road == r:
                c.itemconfig(red, fill="gray")
                c.itemconfig(green, fill="green")
            else:
                c.itemconfig(red, fill="red")
                c.itemconfig(green, fill="gray")

        delay = int(self.times[r] * 1000)
        self.current_index = (self.current_index + 1) % len(self.roads)

        if self.after_id:
            self.root.after_cancel(self.after_id)

        self.after_id = self.root.after(delay, self.run_cycle)

    def get_condition(self, values):
        avg = sum(values.values()) / len(values)
        if avg > 70:
            return "🚨 Heavy Traffic"
        elif avg > 30:
            return "⚖ Moderate Traffic"
        return "🟢 Low Traffic"

    def calculate(self):
        values = {r:int(self.entries[r].get()) for r in self.roads}

        sim = ctrl.ControlSystemSimulation(self.system)
        for r in self.roads:
            sim.input[f'density_{r}'] = values[r]
        sim.compute()

        self.times = {r:sim.output[f'green_time_{r}'] for r in self.roads}

        if self.emergency.get():
            self.times[self.roads[0]] = 60

        best = max(self.times, key=self.times.get)

        self.status.set(f"Priority Road: {best}")
        self.condition.set(self.get_condition(values))

        self.create_signals()
        self.current_index = 0
        self.run_cycle()

        # ===== GRAPH WITH LEGEND =====
        self.ax.clear()
        roads_list = self.roads
        times_list = [self.times[r] for r in roads_list]

        bars = self.ax.bar(roads_list, times_list)

        for bar, r in zip(bars, roads_list):
            if r == best:
                bar.set_color('#00b894')
            else:
                bar.set_color('#b2bec3')

        self.ax.set_title("Green Time Allocation (Fuzzy Logic Output)")
        self.ax.set_ylim(0,65)

        # Values
        for bar, t in zip(bars, times_list):
            self.ax.text(bar.get_x()+bar.get_width()/2,
                         t+1, f"{t:.1f}s",
                         ha='center')

        # Legend
        legend_elements = [
            Patch(facecolor='#00b894', label='Priority Road'),
            Patch(facecolor='#b2bec3', label='Other Roads')
        ]
        self.ax.legend(handles=legend_elements)

        self.ax.grid(axis='y', linestyle='--', alpha=0.5)
        self.canvas.draw()

    def clear(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)

        for w in self.signal_frame.winfo_children():
            w.destroy()

        self.ax.clear()
        self.canvas.draw()

# RUN
root = tk.Tk()
app = TrafficGUI(root)
root.mainloop()