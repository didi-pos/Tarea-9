import tkinter as tk
import math
import random

class PistaCarreras:
    def __init__(self, root):
        self.root = root
        self.root.title("🏁 Pista de Carreras - 4 Curvas")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # Canvas principal
        self.canvas = tk.Canvas(root, width=900, height=650, bg="#2d5016")
        self.canvas.pack()
        
        # Panel de información
        self.info_frame = tk.Frame(root, bg="#1a1a1a", height=50)
        self.info_frame.pack(fill=tk.X)
        
        self.lap_label = tk.Label(
            self.info_frame, 
            text="Vuelta: 0/3", 
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#1a1a1a"
        )
        self.lap_label.pack(side=tk.LEFT, padx=20)
        
        self.speed_label = tk.Label(
            self.info_frame,
            text="Velocidad: 0 km/h",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#1a1a1a"
        )
        self.speed_label.pack(side=tk.LEFT, padx=20)
        
        self.time_label = tk.Label(
            self.info_frame,
            text="Tiempo: 0.0s",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#1a1a1a"
        )
        self.time_label.pack(side=tk.LEFT, padx=20)
        
        self.control_label = tk.Label(
            self.info_frame,
            text="⬆️ Acelerar  ⬇️ Frenar  ⬅️➡️ Girar",
            font=("Arial", 12),
            fg="#00ff00",
            bg="#1a1a1a"
        )
        self.control_label.pack(side=tk.RIGHT, padx=20)
        
        # Variables del carro
        self.car_x = 450
        self.car_y = 300
        self.car_angle = 0
        self.car_speed = 0
        self.max_speed = 8
        self.acceleration = 0.3
        self.friction = 0.95
        self.turn_speed = 4
        
        # Variables de juego
        self.laps = 0
        self.max_laps = 3
        self.checkpoints_passed = [False] * 4
        self.game_time = 0
        self.game_started = False
        self.game_over = False
        
        # Controles
        self.keys = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }
        
        # Crear pista
        self.crear_pista()
        self.crear_checkpoints()
        
        # Crear carro
        self.car = self.canvas.create_polygon(
            0, 0, 0, 0, 0, 0,
            fill="#ff0000",
            outline="white",
            width=2
        )
        
        # Eventos de teclado
        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)
        
        # Mensaje inicial
        self.start_text = self.canvas.create_text(
            450, 325,
            text="Presiona ⬆️ para comenzar",
            font=("Arial", 24, "bold"),
            fill="white",
            tags="start_message"
        )
        
        # Iniciar loop del juego
        self.update_game()
    
    def crear_pista(self):
        """Crea una pista con 4 curvas pronunciadas"""
        # Pista exterior (borde externo)
        puntos_exterior = []
        # Pista interior (borde interno)
        puntos_interior = []
        
        num_puntos = 100
        center_x, center_y = 450, 325
        
        for i in range(num_puntos):
            angle = (i / num_puntos) * 2 * math.pi
            
            # Crear forma con 4 curvas pronunciadas usando función paramétrica
            # Radio base + variación que crea 4 lóbulos
            radio_base = 200
            variacion = 50 * math.cos(2 * angle)  # 2 * angle crea 4 curvas
            
            radio_exterior = radio_base + variacion + 40
            radio_interior = radio_base + variacion - 40
            
            # Puntos del borde exterior
            x_ext = center_x + radio_exterior * math.cos(angle)
            y_ext = center_y + radio_exterior * math.sin(angle)
            puntos_exterior.append((x_ext, y_ext))
            
            # Puntos del borde interior
            x_int = center_x + radio_interior * math.cos(angle)
            y_int = center_y + radio_interior * math.sin(angle)
            puntos_interior.append((x_int, y_int))
        
        # Dibujar césped exterior
        self.canvas.create_oval(50, 25, 850, 625, fill="#2d5016", outline="")
        
        # Dibujar pista (asfalto)
        self.canvas.create_polygon(puntos_exterior, fill="#3a3a3a", outline="")
        self.canvas.create_polygon(puntos_interior, fill="#2d5016", outline="")
        
        # Dibujar líneas de borde blancas
        for i in range(len(puntos_exterior)):
            x1, y1 = puntos_exterior[i]
            x2, y2 = puntos_exterior[(i + 1) % len(puntos_exterior)]
            self.canvas.create_line(x1, y1, x2, y2, fill="white", width=3)
        
        for i in range(len(puntos_interior)):
            x1, y1 = puntos_interior[i]
            x2, y2 = puntos_interior[(i + 1) % len(puntos_interior)]
            self.canvas.create_line(x1, y1, x2, y2, fill="white", width=3)
        
        # Dibujar línea discontinua central
        for i in range(0, num_puntos, 4):
            angle = (i / num_puntos) * 2 * math.pi
            radio_base = 200
            variacion = 50 * math.cos(2 * angle)
            radio_medio = radio_base + variacion
            
            x1 = center_x + radio_medio * math.cos(angle)
            y1 = center_y + radio_medio * math.sin(angle)
            
            angle2 = ((i + 2) / num_puntos) * 2 * math.pi
            variacion2 = 50 * math.cos(2 * angle2)
            radio_medio2 = radio_base + variacion2
            
            x2 = center_x + radio_medio2 * math.cos(angle2)
            y2 = center_y + radio_medio2 * math.sin(angle2)
            
            self.canvas.create_line(x1, y1, x2, y2, fill="yellow", width=2, dash=(10, 10))
        
        # Línea de salida/meta
        self.canvas.create_rectangle(
            center_x + 200 - 5, center_y - 40,
            center_x + 200 + 5, center_y + 40,
            fill="white",
            outline=""
        )
        
        # Texto de meta
        self.canvas.create_text(
            center_x + 250, center_y,
            text="META",
            font=("Arial", 20, "bold"),
            fill="white"
        )
        
        self.puntos_pista_exterior = puntos_exterior
        self.puntos_pista_interior = puntos_interior
    
    def crear_checkpoints(self):
        """Crea 4 checkpoints invisibles para detectar vueltas"""
        self.checkpoints = [
            {'x': 450, 'y': 100, 'radius': 80},   # Checkpoint 1 (arriba)
            {'x': 700, 'y': 325, 'radius': 80},   # Checkpoint 2 (derecha)
            {'x': 450, 'y': 550, 'radius': 80},   # Checkpoint 3 (abajo)
            {'x': 200, 'y': 325, 'radius': 80},   # Checkpoint 4 (izquierda)
        ]
    
    def check_checkpoint(self):
        """Verifica si el carro pasó por un checkpoint"""
        for i, cp in enumerate(self.checkpoints):
            dist = math.sqrt((self.car_x - cp['x'])**2 + (self.car_y - cp['y'])**2)
            if dist < cp['radius'] and not self.checkpoints_passed[i]:
                self.checkpoints_passed[i] = True
                
                # Si pasó por todos los checkpoints en orden
                if all(self.checkpoints_passed):
                    self.laps += 1
                    self.checkpoints_passed = [False] * 4
                    self.lap_label.config(text=f"Vuelta: {self.laps}/{self.max_laps}")
                    
                    if self.laps >= self.max_laps:
                        self.game_over = True
                        self.mostrar_victoria()
    
    def mostrar_victoria(self):
        """Muestra mensaje de victoria"""
        self.canvas.create_rectangle(250, 250, 650, 400, fill="black", outline="white", width=3)
        self.canvas.create_text(
            450, 300,
            text="🏆 ¡GANASTE! 🏆",
            font=("Arial", 32, "bold"),
            fill="gold"
        )
        self.canvas.create_text(
            450, 350,
            text=f"Tiempo: {self.game_time:.1f}s",
            font=("Arial", 20),
            fill="white"
        )
    
    def key_press(self, event):
        """Maneja teclas presionadas"""
        if not self.game_started and event.keysym == 'Up':
            self.game_started = True
            self.canvas.delete("start_message")
        
        if event.keysym == 'Up':
            self.keys['up'] = True
        elif event.keysym == 'Down':
            self.keys['down'] = True
        elif event.keysym == 'Left':
            self.keys['left'] = True
        elif event.keysym == 'Right':
            self.keys['right'] = True
    
    def key_release(self, event):
        """Maneja teclas liberadas"""
        if event.keysym == 'Up':
            self.keys['up'] = False
        elif event.keysym == 'Down':
            self.keys['down'] = False
        elif event.keysym == 'Left':
            self.keys['left'] = False
        elif event.keysym == 'Right':
            self.keys['right'] = False
    
    def update_car_physics(self):
        """Actualiza la física del carro"""
        if self.game_over:
            return
        
        # Aceleración
        if self.keys['up']:
            self.car_speed = min(self.car_speed + self.acceleration, self.max_speed)
        elif self.keys['down']:
            self.car_speed = max(self.car_speed - self.acceleration * 1.5, -self.max_speed * 0.5)
        else:
            # Fricción
            self.car_speed *= self.friction
            if abs(self.car_speed) < 0.1:
                self.car_speed = 0
        
        # Giro (solo si hay velocidad)
        if abs(self.car_speed) > 0.5:
            if self.keys['left']:
                self.car_angle -= self.turn_speed * (abs(self.car_speed) / self.max_speed)
            if self.keys['right']:
                self.car_angle += self.turn_speed * (abs(self.car_speed) / self.max_speed)
        
        # Movimiento
        rad = math.radians(self.car_angle)
        self.car_x += self.car_speed * math.cos(rad)
        self.car_y += self.car_speed * math.sin(rad)
        
        # Mantener en canvas
        self.car_x = max(50, min(850, self.car_x))
        self.car_y = max(50, min(600, self.car_y))
    
    def draw_car(self):
        """Dibuja el carro en su posición actual"""
        # Forma del carro (rectángulo)
        car_width = 20
        car_height = 35
        
        # Calcular esquinas del carro rotado
        rad = math.radians(self.car_angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        # Puntos del carro (forma de flecha)
        points = [
            (-car_width/2, -car_height/2),
            (car_width/2, -car_height/2),
            (car_width/2, car_height/3),
            (0, car_height/2),
            (-car_width/2, car_height/3),
        ]
        
        # Rotar y trasladar puntos
        rotated_points = []
        for px, py in points:
            rx = px * cos_a - py * sin_a + self.car_x
            ry = px * sin_a + py * cos_a + self.car_y
            rotated_points.extend([rx, ry])
        
        self.canvas.coords(self.car, *rotated_points)
    
    def update_game(self):
        """Loop principal del juego"""
        if self.game_started and not self.game_over:
            self.game_time += 0.02
            self.update_car_physics()
            self.check_checkpoint()
            
            # Actualizar labels
            speed_kmh = abs(self.car_speed) * 20
            self.speed_label.config(text=f"Velocidad: {speed_kmh:.0f} km/h")
            self.time_label.config(text=f"Tiempo: {self.game_time:.1f}s")
        
        self.draw_car()
        self.root.after(20, self.update_game)

# Crear ventana y ejecutar juego
if __name__ == "__main__":
    root = tk.Tk()
    game = PistaCarreras(root)
    root.mainloop()
