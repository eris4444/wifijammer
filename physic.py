import tkinter as tk
from tkinter import ttk
import math
import numpy as np
from PIL import Image, ImageTk
import time
import random

class CircuitSimulation:
    def __init__(self, canvas):
        self.canvas = canvas
        self.voltage = 12
        self.resistance = 100
        self.current = self.voltage / self.resistance
        self.electrons = []
        self.electron_positions = []
        
    def create_circuit(self):
        # Draw battery
        self.canvas.create_rectangle(50, 150, 80, 250, fill='gray')
        self.canvas.create_text(65, 130, text=f"{self.voltage}V")
        
        # Draw resistor
        self.canvas.create_rectangle(200, 150, 300, 170, fill='brown')
        self.canvas.create_text(250, 190, text=f"{self.resistance}Ω")
        
        # Draw wires
        self.canvas.create_line(80, 200, 200, 200, fill='black', width=2)
        self.canvas.create_line(300, 160, 400, 160, fill='black', width=2)
        self.canvas.create_line(400, 160, 400, 250, fill='black', width=2)
        self.canvas.create_line(400, 250, 50, 250, fill='black', width=2)
        
        # Create electrons
        for _ in range(10):
            x = random.randint(80, 380)
            if x <= 200:
                y = 200
            elif x <= 300:
                y = 160
            else:
                if random.random() < 0.5:
                    y = 160
                else:
                    y = random.randint(160, 250)
            
            electron = self.canvas.create_oval(x-3, y-3, x+3, y+3, fill='blue')
            self.electrons.append(electron)
            self.electron_positions.append([x, y])
    
    def update(self):
        speed = self.current * 0.5
        for i, electron in enumerate(self.electrons):
            x, y = self.electron_positions[i]
            
            # Update position based on current path
            if y == 200 and x < 200:  # Top horizontal wire
                x += speed
                if x >= 200:
                    x = 200
                    y = 160
            elif x == 200 and y > 160:  # Vertical at resistor start
                y -= speed
            elif y == 160 and x < 400:  # Through resistor and top right
                x += speed * 0.5  # Slower through resistor
            elif x >= 400 and y < 250:  # Right vertical wire
                y += speed
            elif y >= 250:  # Bottom wire
                x -= speed
                if x <= 50:
                    x = 80
                    y = 200
            
            # Update position
            self.electron_positions[i] = [x, y]
            self.canvas.coords(electron, x-3, y-3, x+3, y+3)

class PendulumSimulation:
    def __init__(self, canvas):
        self.canvas = canvas
        self.length = 150
        self.angle = math.pi/4
        self.angular_velocity = 0
        self.gravity = 9.81
        self.damping = 0.999
        self.pivot_x = 250
        self.pivot_y = 50
        
    def create_pendulum(self):
        # Draw pivot point
        self.pivot = self.canvas.create_oval(
            self.pivot_x-5, self.pivot_y-5,
            self.pivot_x+5, self.pivot_y+5,
            fill='black'
        )
        
        # Calculate bob position
        bob_x = self.pivot_x + self.length * math.sin(self.angle)
        bob_y = self.pivot_y + self.length * math.cos(self.angle)
        
        # Draw string
        self.string = self.canvas.create_line(
            self.pivot_x, self.pivot_y,
            bob_x, bob_y,
            fill='black'
        )
        
        # Draw bob
        self.bob = self.canvas.create_oval(
            bob_x-15, bob_y-15,
            bob_x+15, bob_y+15,
            fill='red'
        )
    
    def update(self):
        # Update angular acceleration, velocity and position
        angular_acceleration = -self.gravity/self.length * math.sin(self.angle)
        self.angular_velocity += angular_acceleration * 0.1
        self.angular_velocity *= self.damping
        self.angle += self.angular_velocity * 0.1
        
        # Calculate new bob position
        bob_x = self.pivot_x + self.length * math.sin(self.angle)
        bob_y = self.pivot_y + self.length * math.cos(self.angle)
        
        # Update graphics
        self.canvas.coords(
            self.string,
            self.pivot_x, self.pivot_y,
            bob_x, bob_y
        )
        self.canvas.coords(
            self.bob,
            bob_x-15, bob_y-15,
            bob_x+15, bob_y+15
        )

class WaveSimulation:
    def __init__(self, canvas):
        self.canvas = canvas
        self.amplitude = 50
        self.frequency = 2
        self.wave_points = []
        self.time = 0
        
    def create_wave(self):
        # Create initial wave points
        for x in range(0, 500, 5):
            y = 200 + self.amplitude * math.sin(x/50)
            point = self.canvas.create_oval(x-2, y-2, x+2, y+2, fill='blue')
            self.wave_points.append(point)
    
    def update(self):
        self.time += 0.1
        for i, point in enumerate(self.wave_points):
            x = i * 5
            y = 200 + self.amplitude * math.sin(x/50 - self.time * self.frequency)
            self.canvas.coords(point, x-2, y-2, x+2, y+2)

class OpticsSimulation:
    def __init__(self, canvas):
        self.canvas = canvas
        self.mirror_angle = 45
        self.light_rays = []
        
    def create_optics(self):
        # Draw mirror
        self.mirror = self.canvas.create_line(
            200, 100, 300, 200,
            fill='silver', width=3
        )
        
        # Create incident light ray
        self.create_light_ray(150, 50, 250, 150, 'yellow')
        
    def create_light_ray(self, x1, y1, x2, y2, color):
        ray = self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
        self.light_rays.append(ray)
        
        # Calculate reflection
        angle = math.atan2(y2-y1, x2-x1)
        reflection_angle = 2 * math.radians(self.mirror_angle) - angle
        
        # Draw reflected ray
        length = 100
        x3 = x2 + length * math.cos(reflection_angle)
        y3 = y2 + length * math.sin(reflection_angle)
        
        reflected_ray = self.canvas.create_line(x2, y2, x3, y3, fill=color, width=2)
        self.light_rays.append(reflected_ray)
    
    def update(self):
        # Update mirror angle if needed
        pass

class VirtualPhysicsLab:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Physics Laboratory")
        self.root.geometry("800x600")
        
        # Setup styles
        self.setup_styles()
        
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(expand=True, fill='both')
        
        # Create tabs
        self.setup_circuit_tab()
        self.setup_pendulum_tab()
        self.setup_wave_tab()
        self.setup_optics_tab()
        
        # Start animation
        self.animate()
        
    def setup_styles(self):
        style = ttk.Style()
        
        # Configure colors
        self.colors = {
            'primary': '#2563eb',
            'secondary': '#f1f5f9',
            'accent': '#0284c7',
            'background': '#ffffff',
            'text': '#0f172a'
        }
        
        # Configure styles
        style.configure('TNotebook',
            background=self.colors['background']
        )
        
        style.configure('TNotebook.Tab',
            padding=[15, 5],
            background=self.colors['secondary'],
            foreground=self.colors['text']
        )
        
        style.map('TNotebook.Tab',
            background=[('selected', self.colors['background'])],
            foreground=[('selected', self.colors['primary'])]
        )
        
        style.configure('TFrame',
            background=self.colors['background']
        )
        
        style.configure('TButton',
            padding=[10, 5],
            background=self.colors['primary'],
            foreground=self.colors['background']
        )
        
    def setup_circuit_tab(self):
        circuit_frame = ttk.Frame(self.notebook)
        self.notebook.add(circuit_frame, text='Electricity')
        
        # Create canvas
        canvas = tk.Canvas(circuit_frame, width=500, height=400, bg='white')
        canvas.pack(pady=10)
        
        # Create controls
        controls_frame = ttk.Frame(circuit_frame)
        controls_frame.pack(fill='x', padx=10)
        
        # Create circuit simulation
        self.circuit_sim = CircuitSimulation(canvas)
        self.circuit_sim.create_circuit()
        
    def setup_pendulum_tab(self):
        pendulum_frame = ttk.Frame(self.notebook)
        self.notebook.add(pendulum_frame, text='Pendulum')
        
        # Create canvas
        canvas = tk.Canvas(pendulum_frame, width=500, height=400, bg='white')
        canvas.pack(pady=10)
        
        # Create controls
        controls_frame = ttk.Frame(pendulum_frame)
        controls_frame.pack(fill='x', padx=10)
        
        # Create pendulum simulation
        self.pendulum_sim = PendulumSimulation(canvas)
        self.pendulum_sim.create_pendulum()
        
    def setup_wave_tab(self):
        wave_frame = ttk.Frame(self.notebook)
        self.notebook.add(wave_frame, text='Waves')
        
        # Create canvas
        canvas = tk.Canvas(wave_frame, width=500, height=400, bg='white')
        canvas.pack(pady=10)
        
        # Create controls
        controls_frame = ttk.Frame(wave_frame)
        controls_frame.pack(fill='x', padx=10)
        
        # Create wave simulation
        self.wave_sim = WaveSimulation(canvas)
        self.wave_sim.create_wave()
        
    def setup_optics_tab(self):
        optics_frame = ttk.Frame(self.notebook)
        self.notebook.add(optics_frame, text='Optics')
        
        # Create canvas
        canvas = tk.Canvas(optics_frame, width=500, height=400, bg='white')
        canvas.pack(pady=10)
        
        # Create controls
        controls_frame = ttk.Frame(optics_frame)
        controls_frame.pack(fill='x', padx=10)
        
        # Create optics simulation
        self.optics_sim = OpticsSimulation(canvas)
        self.optics_sim.create_optics()
        
    def animate(self):
        # Update all simulations
        self.circuit_sim.update()
        self.pendulum_sim.update()
        self.wave_sim.update()
        self.optics_sim.update()
        
        # Schedule next update
        self.root.after(50, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualPhysicsLab(root)
    root.mainloop()