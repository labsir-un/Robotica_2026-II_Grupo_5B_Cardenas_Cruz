# Laboratorio 1 — Robótica Industrial: Trayectorias, Entradas y Salidas Digitales
### ABB IRB 140 · RobotStudio · RAPID · IRC5

<div align="center">

[![ABB IRB140](https://img.shields.io/badge/Robot-ABB%20IRB%20140-orange.svg)](#)
[![Controlador](https://img.shields.io/badge/Controlador-IRC5%20%28DSQC%20652%29-blue.svg)](#)
[![Software](https://img.shields.io/badge/Software-RobotStudio-red.svg)](#)
[![Lenguaje](https://img.shields.io/badge/Lenguaje-RAPID-lightgrey.svg)](#)

**Universidad Nacional de Colombia — Sede Bogotá**  
**Facultad de Ingeniería · Departamento de Ingeniería Mecánica y Mecatrónica**  
**Asignatura:** Robótica (2026-II)  
**Grupo 5B:** Ariel Giovanni Cárdenas Santisteban · Jared Cruz

</div>

---

## Índice
1. [Descripción de la solución](#1-descripción-de-la-solución)
2. [Objetivos alcanzados](#2-objetivos-alcanzados)
3. [Estructura del directorio](#3-estructura-del-directorio)
4. [Diseño del portamarcador](#4-diseño-del-portamarcador)
5. [Calibración de TCP y WorkObject](#5-calibración-de-tcp-y-workobject)
6. [Lógica de control y programa RAPID](#6-lógica-de-control-y-programa-rapid)
7. [Resultados y video demostrativo](#7-resultados-y-video-demostrativo)
8. [Aprendizajes y dificultades](#8-aprendizajes-y-dificultades)
9. [Instrucciones de reproducción](#9-instrucciones-de-reproducción)

---

## 1. Descripción de la solución

En esta práctica se automatizó la rutina de decoración de un pastel (representado físicamente mediante una superficie de pizarra redonda en la celda robótica), utilizando el manipulador industrial **ABB IRB 140** controlado por la unidad **IRC5** y sincronizado con una **banda transportadora**.

La tarea de decoración se diseñó de forma conjunta por el equipo y comprende:
- **Trazado perimetral:** Escritura continua de los nombres de los integrantes (**Ariel** y **Jared**) distribuidos a lo largo del borde circular de la pizarra.
- **Trazado central:** Ilustración del rostro de **Naruto** en el centro de la superficie circular.
- **Modos de operación:** Implementación de tres rutinas independientes seleccionadas mediante las entradas digitales del módulo DSQC 652:
  1. **`DI_01` — Ciclo automático de decoración:** Ingreso del pastel sobre la banda transportadora, detención en la estación de trabajo, ejecución de las trayectorias de dibujo por parte del robot y evacuación del producto terminado hacia el final de la banda.
  2. **`DI_02` — Pose de mantenimiento:** Desplazamiento seguro del robot a una posición accesible para inspección, ajuste o cambio del marcador.
  3. **`DI_03` — Rutina *Farmear Aura*:** Coreografía de movimiento libre desarrollada por el equipo como componente creativo y de verificación cinemática.

---

## 2. Objetivos alcanzados

- Diseñar y acoplar mecánicamente un portamarcador funcional al flange del manipulador ABB IRB 140.
- Calibrar la herramienta tanto en el entorno virtual de **RobotStudio** como en el robot real mediante el método de 4 puntos en el FlexPendant.
- Definir y calibrar el sistema de coordenadas de trabajo (**WorkObject**) sobre la superficie circular de trabajo.
- Programar la secuencia modular en lenguaje **RAPID**, implementando trayectorias lineales (`MoveL`), articulares (`MoveJ`, `MoveAbsJ`) y control de aproximación/zona (`fine`, `z10`).
- Integrar las señales de entrada y salida digitales (módulo **DSQC 652**) para coordinar el movimiento bidireccional de la banda transportadora (`FWD_Conveyor`, `BWD_Conveyor`) y la señalización de estado del robot (`DO_01`, `DO_02`, `DO_03`).
- Validar la seguridad y prevención de colisiones mediante enclavamientos lógicos en RAPID antes de la ejecución en la celda física.

---

## 3. Estructura del directorio

La organización de los archivos asociados a este laboratorio es la siguiente:

```text
Laboratorio No. 01 - Robótica Industrial ABB IRB140 y RobotStudio/
├── README.MD               # Documentación principal de la práctica
├── CAD/                    # Modelos geométricos de la herramienta (formato .SAT)
├── RAPID/                  # Código fuente del programa (.mod)
├── RobotStudio/            # Estación y paquete de simulación (.rspag)
└── Resultados/             # Fotografías, evidencias de planta y ejecuciones
```

---

## 4. Diseño del portamarcador

Para ejecutar el trazado sobre la pizarra redonda sin dañar el marcador ni comprometer la precisión de la trayectoria, se diseñó un soporte portaherramienta acoplable al plato portaherramientas (flange) del ABB IRB 140.

- **Archivo CAD:** El modelo en formato de intercambio se encuentra alojado en [`CAD/`](./CAD/).
- **Características de la herramienta:**

| Parámetro | Detalle / Valor |
|---|---|
| Tipo de acople | Flange estándar ABB IRB 140 |
| Mecanismo de sujeción | Prisionero / Ajuste mecánico para marcador |
| Formato disponible | `.SAT` |
| Masa aproximada | *[Completar: ej. 0.15 kg]* |
| Material de fabricación | *[Completar: ej. PLA / Impresión 3D]* |

> [!NOTE]
> *(Una vez cargada la imagen o render del diseño en `Resultados/portamarcador.png`, se enlazará en este apartado).*

---

## 5. Calibración de TCP y WorkObject

### 5.1 Tool Center Point (TCP)
La calibración física del TCP se llevó a cabo en el laboratorio mediante el FlexPendant utilizando el método de aproximación por 4 puntos a una referencia fija cónica. En RobotStudio, el TCP virtual se obtuvo a partir de las coordenadas del modelo CAD acoplado al flange.

| Parámetro | Simulación (RobotStudio) | Robot real (FlexPendant) | Error / Diferencia |
|---|---|---|---|
| **X [mm]** | *[Completar]* | *[Completar]* | *[Completar]* |
| **Y [mm]** | *[Completar]* | *[Completar]* | *[Completar]* |
| **Z [mm]** | *[Completar]* | *[Completar]* | *[Completar]* |
| **Orientación (q1, q2, q3, q4)** | *[Completar]* | *[Completar]* | — |

### 5.2 WorkObject (Superficie de trabajo)
Se definió un objeto de trabajo correspondiente a la superficie plana circular. Este objeto permite desacoplar las trayectorias de la posición absoluta de la base del robot, facilitando su reubicación o reutilización en otros cuadrantes sin modificar las trayectorias geométricas programadas.

---

## 6. Lógica de control y programa RAPID

### 6.1 Mapeo de Entradas y Salidas Digitales (Módulo DSQC 652)

| Señal | Tipo | Descripción |
|---|---|---|
| `DI_01` | Entrada Digital | Inicia el ciclo automático de transporte y decoración |
| `DI_02` | Entrada Digital | Solicita el desplazamiento a pose de mantenimiento |
| `DI_03` | Entrada Digital | Inicia la rutina coreográfica *Farmear Aura* |
| `DO_01` | Salida Digital | Activa (1) mientras el robot ejecuta la rutina de decoración |
| `DO_02` | Salida Digital | Activa (1) mientras el robot permanece en pose de mantenimiento |
| `DO_03` | Salida Digital | Activa (1) durante la ejecución de la rutina *Farmear Aura* |
| `FWD_Conveyor` | Salida Digital | Activa el avance de la banda transportadora hacia la estación |
| `BWD_Conveyor` | Salida Digital | Activa el retroceso de la banda transportadora hacia la salida |

> [!WARNING]
> **Enclavamiento de seguridad:** Para proteger el motor y el variador de frecuencia, el programa prohíbe y previene en todo momento la activación simultánea de `FWD_Conveyor = 1` y `BWD_Conveyor = 1`.

### 6.2 Arquitectura modular del programa

El código RAPID está estructurado en procedimientos especializados:

- **`main()`**: Ciclo principal de supervisión que consulta el estado de las entradas digitales y deriva la ejecución a la subrutina correspondiente.
- **`CicloDecoracion()`**: Secuencia que coordina el avance de la banda, detención, llamado al trazado, retorno a HOME y evacuación del pastel.
- **`RutinaDecoracion()`**: Trazado continuo que ejecuta los nombres perimetrales (**Ariel** y **Jared**) y el rostro central de **Naruto** sobre el WorkObject.
- **`PoseMantenimiento()`**: Desplazamiento articular a una posición elevada y accesible.
- **`FarmearAura()`**: Secuencia coreográfica libre de movimientos coordinados del manipulador.
- **`HomeRobot()`**: Retorno seguro mediante `MoveAbsJ` a la pose de reposo.
- **`ConveyorForward()`, `ConveyorBackward()`, `ConveyorStop()`**: Rutinas de control de la banda con tiempos de espera (`WaitTime`) para evitar transiciones bruscas.

> [!TIP]
> **Diagrama de flujo:** El diagrama detallado de la secuencia completa se integrará formalmente una vez se incorpore el archivo fuente final en `RAPID/`.

---

## 7. Resultados y video demostrativo

La implementación física fue validada de forma completa en el laboratorio del LabSIR, ejecutando tanto el ciclo de transporte como el trazado real sobre la pizarra circular con el marcador.

### Video oficial de la práctica (Canal LabSIR - YouTube)

A continuación se presenta el registro audiovisual oficial de la práctica en el robot real:

<div align="center">

[![Video Demostrativo Lab 1 - Robotica UNAL](https://img.youtube.com/vi/vdbJv02MnJA/maxresdefault.jpg)](https://www.youtube.com/watch?v=vdbJv02MnJA)

*Haz clic en la imagen superior para reproducir el video en YouTube*  
**Enlace directo:** [https://www.youtube.com/watch?v=vdbJv02MnJA](https://www.youtube.com/watch?v=vdbJv02MnJA)

</div>

---

## 8. Aprendizajes y dificultades

### Aprendizajes clave
- *[Completar con los aprendizajes técnicos específicos del equipo]*
- *[Por ejemplo: efecto del filtrado de zonas z10 vs fine en la fluidez del trazado de Naruto, repetibilidad del robot al trabajar con WorkObjects]*

### Dificultades encontradas y soluciones implementadas
- *[Completar con las dificultades reales experimentadas]*
- *[Por ejemplo: ajuste de la presión del marcador para trazo uniforme, calibración del tiempo exacto de detención de la banda transportadora con la inercia del variador]*

---

## 9. Instrucciones de reproducción

1. **Simulación en RobotStudio:**
   - Clonar o descargar el repositorio.
   - Abrir RobotStudio (versión 2020 o superior).
   - Restaurar el paquete de estación ubicado en [`RobotStudio/`](./RobotStudio/).
2. **Carga del código RAPID:**
   - En el controlador virtual o real, cargar el módulo contenido en [`RAPID/`](./RAPID/).
   - Verificar la configuración de señales I/O del módulo DSQC 652 en la pestaña de configuración del controlador.
3. **Puesta en marcha y seguridad:**
   - Verificar en modo manual y con velocidad reducida (25%) el primer ciclo completo.
   - Constatar que la parada de emergencia se encuentre despejada y operativa antes de pasar a modo automático.
