#Laboratorio 2 - Motoman MH6
#Equipo 5B - Ariel Cárdenas, Kennet Cruz

from robodk.robolink import *    # API para comunicarte con RoboDK
from robodk.robomath import *    # Funciones matemáticas
import math


# 1) Conexión a RoboDK e inicialización

RDK = Robolink()

#Elegir un robot
robot = RDK.ItemUserPick("Selecciona un robot", ITEM_TYPE_ROBOT)
if not robot.Valid():
    raise Exception("No se ha seleccionado un robot válido.")

# Conectar al robot físico 
'''
if not robot.Connect():
    raise Exception("No se pudo conectar al robot. Verifique que esté en modo remoto y que la configuración sea correcta.")

# Confirmar conexión
if not robot.ConnectedState():
    raise Exception("El robot no está conectado correctamente. Revisa la conexión.")

print("Robot conectado correctamente.")
'''


# 2) Cargar el Frame donde se va a dibujar

# Ajusta el nombre

frame_name = "Frame_from_Target1"
target_home = "Target Home"
frame = RDK.Item(frame_name, ITEM_TYPE_FRAME)
t_h = RDK.Item(target_home, ITEM_TYPE_TARGET)
if not frame.Valid():
    raise Exception(f'No se encontró el Frame "{frame_name}" en la estación.')

# Asignamos este frame al robot
robot.setPoseFrame(frame)
# Usamos la herramienta activa
robot.setPoseTool(robot.PoseTool())


# Ajustes de velocidad y blending
robot.setSpeed(300)   # mm/s 
robot.setRounding(3)  # blending (radio de curvatura), se reduce a 3 para dibujar las secciones de la figura mas pequeñas


# 3) Parámetros de la figura 

num_points = 100       # Cuántos puntos se muestrean 
A = 240                # Amplitud 
k = 5                  # Parámetros de la figura
z_surface = 0          # Z=0 en el plano del frame
z_safe = 50            # Altura segura para aproximarse y salir 


# 4) Movimiento al centro en altura segura

#Target Home

robot.MoveJ(t_h)

# El centro de la rosa (r=0) corresponde a x=0, y=0
robot.MoveJ(transl(0, 0, z_surface - z_safe))

# Bajamos a la "superficie" (Z=0)
robot.MoveL(transl(0, 0, z_surface))


# 5) Dibujar la figura

# Recorremos theta de 0 a 2*pi (una vuelta completa)
full_turn = math.pi

for i in range(num_points+1):
    # Fracción entre 0 y 1
    t = i / num_points
    # Ángulo actual
    theta = full_turn * t

    # Calculamos r
    r = A * math.sin(k * theta) * math.sin(k * theta) * math.cos(theta)

    # Convertimos a coordenadas Cartesianas X, Y
    x = r * math.cos(theta)
    y = r * math.sin(theta)

    # Movemos linealmente (MoveL) en el plano del Frame
    robot.MoveL(transl(x, y, z_surface))

# Al terminar, subimos de nuevo para no chocar
robot.MoveL(transl(x, y, z_surface - z_safe))


# 6) Dibujar los nombres: Ariel y Kennet

robot.setRounding(1) # Menor radio de curvatura para que las letras salgan mas nítidas
# Usando la librería de matplotlib (textpath) se extraen las coordenadas para los nombres 

trazos_nombres = [[[-96.57, -304.48], [-93.11, -304.48], [-93.11, -315.27], [-81.66, -304.48], [-77.22, -304.48], [-89.88, -316.38], [-76.31, -330.0], [-80.86, -330.0], [-93.11, -317.71], [-93.11, -330.0], [-96.57, -330.0], [-96.57, -304.48]], [[-73.61, -304.48], [-57.48, -304.48], [-57.48, -307.39], [-70.16, -307.39], [-70.16, -314.94], [-58.01, -314.94], [-58.01, -317.85], [-70.16, -317.85], [-70.16, -327.1], [-57.17, -327.1], [-57.17, -330.0], [-73.61, -330.0], [-73.61, -304.48]], [[-51.5, -304.48], [-46.85, -304.48], [-35.54, -325.83], [-35.54, -304.48], [-32.19, -304.48], [-32.19, -330.0], [-36.84, -330.0], [-48.15, -308.66], [-48.15, -330.0], [-51.5, -330.0], [-51.5, -304.48]], [[-25.32, -304.48], [-20.67, -304.48], [-9.35, -325.83], [-9.35, -304.48], [-6.01, -304.48], [-6.01, -330.0], [-10.66, -330.0], [-21.97, -308.66], [-21.97, -330.0], [-25.32, -330.0], [-25.32, -304.48]], [[0.86, -304.48], [17.0, -304.48], [17.0, -307.39], [4.31, -307.39], [4.31, -314.94], [16.47, -314.94], [16.47, -317.85], [4.31, -317.85], [4.31, -327.1], [17.3, -327.1], [17.3, -330.0], [0.86, -330.0], [0.86, -304.48]], [[19.44, -304.48], [41.02, -304.48], [41.02, -307.39], [31.97, -307.39], [31.97, -330.0], [28.5, -330.0], [28.5, -307.39], [19.44, -307.39], [19.44, -304.48]], [[-68.03, -357.88], [-72.72, -370.58], [-63.34, -370.58], [-68.03, -357.88]], [[-69.99, -354.48], [-66.07, -354.48], [-56.35, -380.0], [-59.94, -380.0], [-62.26, -373.45], [-73.76, -373.45], [-76.08, -380.0], [-79.73, -380.0], [-69.99, -354.48]], [[-40.52, -368.03], [-39.43, -368.62], [-38.36, -369.64], [-37.31, -371.1], [-36.25, -373.03], [-32.74, -380.0], [-36.46, -380.0], [-39.72, -373.45], [-40.96, -371.32], [-42.17, -370.05], [-42.82, -369.69], [-44.44, -369.27], [-45.41, -369.22], [-49.17, -369.22], [-49.17, -380.0], [-52.62, -380.0], [-52.62, -354.48], [-44.83, -354.48], [-42.78, -354.6], [-39.52, -355.51], [-38.3, -356.31], [-37.36, -357.34], [-36.28, -360.1], [-36.15, -361.83], [-36.22, -362.99], [-36.78, -364.99], [-37.27, -365.84], [-37.89, -366.57], [-39.52, -367.67], [-40.52, -368.03]], [[-49.17, -357.32], [-49.17, -366.38], [-44.83, -366.38], [-43.66, -366.31], [-41.78, -365.73], [-41.06, -365.22], [-40.5, -364.58], [-39.87, -362.88], [-39.79, -361.83], [-39.87, -360.78], [-40.5, -359.1], [-41.06, -358.46], [-41.78, -357.96], [-43.66, -357.39], [-44.83, -357.32], [-49.17, -357.32]], [[-28.3, -354.48], [-24.85, -354.48], [-24.85, -380.0], [-28.3, -380.0], [-28.3, -354.48]], [[-17.98, -354.48], [-1.85, -354.48], [-1.85, -357.39], [-14.53, -357.39], [-14.53, -364.94], [-2.38, -364.94], [-2.38, -367.85], [-14.53, -367.85], [-14.53, -377.1], [-1.54, -377.1], [-1.54, -380.0], [-17.98, -380.0], [-17.98, -354.48]], [[4.13, -354.48], [7.58, -354.48], [7.58, -377.1], [20.01, -377.1], [20.01, -380.0], [4.13, -380.0], [4.13, -354.48]]]

# Luego se ajusta en la posición deseada en el área de trabajo, en este caso debajo de la figura

POS_X = -90   # Mueve el texto hacia arriba/abajo respecto a la figura
POS_Y = -10   # Mueve el texto hacia izquierda/derecha para centrarlo
ANGULO = math.radians(90) 

cos_a = math.cos(ANGULO)
sin_a = math.sin(ANGULO)

# Transformaciones para ubicar bien los nombres
def transformar_punto(px, py):
    
    # 1. Quitar el efecto espejo de Y y centrar cerca del origen
    x_temp = px + 30
    y_temp = -py - 340
    
    # 2. Rotar 90 grados
    x_rot = x_temp * cos_a - y_temp * sin_a
    y_rot = x_temp * sin_a + y_temp * cos_a
    
    # 3. Mover a la posición final debajo de la figura
    return x_rot + POS_X, y_rot + POS_Y

for trazo in trazos_nombres:
    if len(trazo) == 0:
        continue
        
    x0, y0 = transformar_punto(trazo[0][0], trazo[0][1])
    
    # 1. Ir al inicio del trazo por arriba 
    robot.MoveL(transl(x0, y0, z_surface - z_safe))
    
    # 2. Bajar y recorrer todos los puntos del trazo
    for px, py in trazo:
        nx, ny = transformar_punto(px, py)
        robot.MoveL(transl(nx, ny, z_surface))
        
    # 3. Subir al terminar el trazo
    xf, yf = transformar_punto(trazo[-1][0], trazo[-1][1])
    robot.MoveL(transl(xf, yf, z_surface - z_safe))

robot.setRounding(3) 


# Regreso a Home

robot.MoveJ(t_h)

print(f"¡Figura completada en el frame '{frame_name}'!")
