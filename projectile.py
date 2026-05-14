from ursina import *
from ursina.prefabs.slider import Slider
from ursina.prefabs.editor_camera import EditorCamera
from ursina.shaders import lit_with_shadows_shader 

from math import sin, cos, radians

app = Ursina()

window.size = (1280, 720)
window.title = "Projectile Motion Simulator"

# Enable orbit-style camera
EditorCamera()

# Environment
Entity(model='plane', scale=(100, 1, 100), texture='white_cube', color=color.light_gray,shader=lit_with_shadows_shader)
sky = Sky()

# Projectile
ball = Entity(model='sphere', color=color.azure, scale=0.5, position=(0, 1, 0), shader=lit_with_shadows_shader)
trail = []

# Sliders
angle_slider = Slider(min=10, max=80, default=45, step=1, position=(-0.6, 0.3), text='Angle (°)', scale=0.75)
speed_slider = Slider(min=5, max=50, default=20, step=1, position=(-0.6, 0.2), text='Speed (m/s)', scale=0.75)
height_slider = Slider(min=0, max=10, default=1, step=0.1, position=(-0.6, 0.4), text='Height (m)', scale=0.75)

# Launch Button
launch_button = Button(text='Launch', position=(-0.6, 0.1), scale=(0.15, 0.08), color=color.lime)

# Physics Constants
g = 9.8
t = 0
launched = False
vx = 0
vy = 0

def reset():
    global t, launched, vx, vy
    t = 0
    launched = True
    ball.position = (0, 1, 0)
    angle_rad = radians(angle_slider.value)
    speed = speed_slider.value
    vx = speed * cos(angle_rad)
    vy = speed * sin(angle_rad)
    for p in trail:
        destroy(p)
    trail.clear()

launch_button.on_click = reset

# Optional keyboard launch
def input(key):
    if key == 'space':
        reset()

# Simulation update
def update():

    global t, launched, vx, vy

    if launched == False:
        #height
        ball.position = (0, height_slider.value, 0)


    if launched:
        t += time.dt
        x = vx * t
        y = vy * t - 0.5 * g * t**2

        # Stop when it hits the ground
        if y + height_slider.value <= 0:
            launched = False

        ball.position = (x, y + height_slider.value, 0)
        trail.append(Entity(model='sphere', color=color.orange, scale=0.1, position=(x, y + height_slider.value, 0)))


EditorCamera()
app.run()
