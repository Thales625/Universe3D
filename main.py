from ursina import *
from json import loads
from time import sleep

from sys import path
path.append('D:\Codes\www\Vector')
from Vector import Vector3

def toVec3(vector3):
    return Vec3(vector3.x, vector3.y, vector3.z)

class Body:
    def getBodies():
        with open('bodies.txt', 'r') as f:
            bodies_txt = f.readlines()[1:]
            f.close()

        bodies = []

        for line in bodies_txt:
            name, pos, vel, radius, mass = line.replace('\n', '').split('|')
            bodies.append(Body(name, Vector3(loads(pos)), Vector3(loads(vel)), float(radius), float(mass), color.random_color()))

        return bodies

    def __init__(self, name, pos, vel, radius, mass, color) -> None:
        self.name = name

        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.mass = mass

        self.scalled_pos = self.pos * SCALE
        self.scalled_radius = self.radius * SCALE

        self.entity = Entity(model='sphere', scale=self.scalled_radius, position=toVec3(self.scalled_pos), texture='2k_sun', color=color, eternal=True)
        #self.border = Entity(model='sphere', scale=10, position=toVec3(self.scalled_pos), color=color, eternal=True)


SCALE = 1e-7
G = 6.6744882e-20 #6.67430e-11

app = Ursina()

camera.clip_plane_far = 9999999999999999999999999999999
camera.clip_plane_near = 1

camera = EditorCamera(rotation_speed=50, move_speed=100)

bodies = Body.getBodies()

bodies[0].entity.scale = 400

b_target = bodies[1]
#camera.set_position(b_target.entity.position)

print('NAME:', b_target.name)
print("DISTANCE: ", b_target.pos.magnitude())
print("RADIUS: ", b_target.radius)
print("MASS: ", b_target.mass)

def update():
    dt = time.dt
    for body in bodies:
        accel = Vector3()   

        for other in bodies:
            if other is not body:
                delta = other.pos - body.pos
                dist = delta.magnitude()
                direction = delta / dist
                accel += (G * other.mass / dist**2) * direction

        body.vel += accel * dt
        body.pos += body.vel * dt

        body.entity.position = toVec3(body.pos * SCALE)
    
    camera.set_position(b_target.entity.position)



window.color = color.black
app.run()
