import pybullet as p
import pybullet_data
import time
import math

# Conectar a PyBullet en modo GUI
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -10)

# Configurar cámara para mejor vista
p.resetDebugVisualizerCamera(
    cameraDistance=2.5,
    cameraYaw=45,
    cameraPitch=-30,
    cameraTargetPosition=[0, 0, 0.5]
)

# Cargar plano
planeId = p.loadURDF("plane.urdf")

# Cargar brazo robótico Kuka (viene incluido con PyBullet)
startPos = [0, 0, 0]
startOrientation = p.getQuaternionFromEuler([0, 0, 0])
robotId = p.loadURDF("kuka_iiwa/model.urdf", startPos, startOrientation, useFixedBase=True)

# Obtener información del robot
numJoints = p.getNumJoints(robotId)
print(f"\n{'='*60}")
print(f"BRAZO ROBÓTICO KUKA IIWA - CONTROL MANUAL")
print(f"{'='*60}")
print(f"Número de articulaciones: {numJoints}")

# Información de las articulaciones
joint_info = []
for i in range(numJoints):
    info = p.getJointInfo(robotId, i)
    joint_name = info[1].decode('utf-8')
    joint_type = info[2]
    
    if joint_type == p.JOINT_REVOLUTE:
        joint_info.append({
            'index': i,
            'name': joint_name,
            'lower': info[8],
            'upper': info[9],
            'max_force': info[10],
            'max_velocity': info[11]
        })
        print(f"  Articulación {i}: {joint_name}")
        print(f"    Rango: [{info[8]:.2f}, {info[9]:.2f}] rad")

print(f"\n{'='*60}")
print("CONTROLES:")
print("  - Usa los sliders para controlar cada articulación")
print("  - Presiona 'R' para resetear a posición inicial")
print("  - Presiona 'D' para demostración automática")
print(f"{'='*60}\n")

# Crear sliders para control manual de cada articulación
sliders = []
for joint in joint_info:
    slider = p.addUserDebugParameter(
        paramName=f"Joint {joint['index']}: {joint['name']}",
        rangeMin=joint['lower'],
        rangeMax=joint['upper'],
        startValue=0
    )
    sliders.append(slider)

# Botones de control
reset_button = p.addUserDebugParameter("Reset Position", 1, 0, 0)
demo_button = p.addUserDebugParameter("Demo Mode", 1, 0, 0)

# Variables de demostración
demo_mode = False
demo_time = 0
last_demo_state = 0

# Posiciones predefinidas para demostración
demo_positions = [
    [0, 0, 0, 0, 0, 0, 0],  # Posición inicial
    [0.5, -0.5, 0.5, -1.0, 0.5, 0.5, 0],  # Posición 1
    [-0.5, 0.5, -0.5, -1.5, -0.5, 0.8, 0],  # Posición 2
    [0.8, 0.3, 0.8, -0.8, 0.3, -0.3, 0],  # Posición 3
    [0, 0, 0, 0, 0, 0, 0],  # Volver a inicio
]
current_demo_pos = 0

# Función para mover el brazo a una posición
def move_to_position(target_positions, duration=2.0):
    """Mueve el brazo suavemente a la posición objetivo"""
    steps = int(duration * 240)  # 240 Hz
    
    # Obtener posiciones actuales
    current_positions = []
    for joint in joint_info:
        state = p.getJointState(robotId, joint['index'])
        current_positions.append(state[0])
    
    # Interpolar entre posición actual y objetivo
    for step in range(steps):
        t = step / steps
        for i, joint in enumerate(joint_info):
            interpolated = current_positions[i] + t * (target_positions[i] - current_positions[i])
            p.setJointMotorControl2(
                robotId,
                joint['index'],
                p.POSITION_CONTROL,
                targetPosition=interpolated,
                force=joint['max_force']
            )
        p.stepSimulation()
        time.sleep(1./240.)

print("✓ Sistema iniciado. Usa los sliders para controlar el brazo.\n")

# Loop principal de simulación
try:
    while True:
        # Leer estado de botones
        demo_state = p.readUserDebugParameter(demo_button)
        reset_state = p.readUserDebugParameter(reset_button)
        
        # Activar/desactivar modo demo
        if demo_state != last_demo_state:
            demo_mode = not demo_mode
            if demo_mode:
                print("\n🎬 Modo Demostración ACTIVADO")
                current_demo_pos = 0
                demo_time = time.time()
            else:
                print("\n⏸️  Modo Demostración DESACTIVADO")
            last_demo_state = demo_state
        
        # Reset a posición inicial
        if reset_state > 0.5:
            print("\n🔄 Reseteando a posición inicial...")
            move_to_position([0] * len(joint_info), duration=1.5)
            demo_mode = False
        
        if demo_mode:
            # Modo demostración automática
            if time.time() - demo_time > 3.0:  # Cambiar posición cada 3 segundos
                print(f"  → Moviendo a posición demo {current_demo_pos + 1}/{len(demo_positions)}")
                move_to_position(demo_positions[current_demo_pos], duration=2.5)
                current_demo_pos = (current_demo_pos + 1) % len(demo_positions)
                demo_time = time.time()
        else:
            # Control manual con sliders
            for i, slider in enumerate(sliders):
                target_pos = p.readUserDebugParameter(slider)
                p.setJointMotorControl2(
                    robotId,
                    joint_info[i]['index'],
                    p.POSITION_CONTROL,
                    targetPosition=target_pos,
                    force=joint_info[i]['max_force']
                )
        
        # Avanzar simulación
        p.stepSimulation()
        time.sleep(1./240.)

except KeyboardInterrupt:
    print("\n\n⏹️  Simulación detenida por el usuario")
    p.disconnect()
except Exception as e:
    print(f"\n❌ Error: {e}")
    p.disconnect()
