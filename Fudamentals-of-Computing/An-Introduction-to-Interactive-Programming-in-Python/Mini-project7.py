# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
ship_angle = 0
ship_angle_vel = 0
ship_angle_vel_inc = 0.05
ship_vel = 0
ship_vel_inc = 5
key_flag = False
missile_flag = False
missile_pos = []
missile_angle = 0
shoot_vel = [0, 0]

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

ship_info2 = ImageInfo([135, 45], [90, 90], 35)
ship_image2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.sound = sound
    
    def get_vel(self):
        return [self.vel[0], self.vel[1]]
            
    def get_pos(self):
        return [self.pos[0], self.pos[1]]
    
    def get_angle(self):
        return self.angle
        
    def draw(self,canvas):
        global ship_image, ship_image2, key_flag
        if key_flag == False:
            self.image = ship_image
            self.image_center = ship_info.get_center()
            canvas.draw_image(self.image, self.image_center, self.image_size, [self.pos[0], self.pos[1]], self.image_size, self.angle)
        else:
            self.image = ship_image2
            self.image_center = ship_info2.get_center()
            canvas.draw_image(ship_image2, self.image_center, self.image_size, [self.pos[0], self.pos[1]], self.image_size, self.angle)
        
    def update(self):
        global ship_vel
        self.angle += ship_angle_vel
        self.vel[0] = ship_vel * angle_to_vector(self.angle)[0]
        self.vel[1] = ship_vel * angle_to_vector(self.angle)[1]
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        if key_flag == False:
            ship_vel *= 0.99
        
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [random.randrange(0, WIDTH),random.randrange(0, HEIGHT)]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        
    
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, [self.pos[0], self.pos[1]], self.image_size, self.angle)

    def update(self):
        self.angle += (random.randrange(-1, 1) / 10.0)
        self.vel[0] = random.randrange(0, 3) * angle_to_vector(self.angle)[0]
        self.vel[1] = random.randrange(0, 3) * angle_to_vector(self.angle)[1]
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        
# Missile class     
class Missile:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = my_ship.get_pos()
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.sound = sound
   
    def draw(self, canvas):
        global missile_pos, missile_angle
        canvas.draw_image(self.image, self.image_center, self.image_size, [self.pos[0], self.pos[1]], self.image_size, self.angle)

    def update(self):
        global missile_pos, missile_angle, shoot_vel
        self.vel[0] += (shoot_vel[0] + 5 * angle_to_vector(missile_angle)[0])
        self.vel[1] += (shoot_vel[1] + 5 * angle_to_vector(missile_angle)[1])
        self.pos[0] = (missile_pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (missile_pos[1] + self.vel[1]) % HEIGHT
            

# define keyhandlers to control firing_angle
def keydown(key):
    global ship_angle_vel, ship_vel, ship_vel_inc, key_flag
    global missile_flag, missile_pos, missile_angle, shoot_vel
    if simplegui.KEY_MAP["left"] == key:
        ship_angle_vel -= ship_angle_vel_inc
    elif simplegui.KEY_MAP["right"] == key:
        ship_angle_vel += ship_angle_vel_inc
    if simplegui.KEY_MAP["up"] == key:
        key_flag = True
        ship_vel = ship_vel_inc
        my_ship.sound.rewind()
        my_ship.sound.play()
    if simplegui.KEY_MAP["space"] == key:
        missile_angle = my_ship.get_angle()
        missile_pos = my_ship.get_pos()
        missile_pos[0] += angle_to_vector(missile_angle)[0] * 45
        missile_pos[1] += angle_to_vector(missile_angle)[1] * 45
        a_missile.vel = [0,0]
        missile_flag = True
        shoot_vel[0] = my_ship.get_vel()[0]
        shoot_vel[1] = my_ship.get_vel()[1]
        a_missile.update()
        a_missile.sound.play()
        

def keyup(key):
    global ship_angle_vel, ship_vel, key_flag
    if simplegui.KEY_MAP["left"] == key:
        ship_angle_vel += ship_angle_vel_inc
    elif simplegui.KEY_MAP["right"] == key:
        ship_angle_vel -= ship_angle_vel_inc
    if simplegui.KEY_MAP["up"] == key:
        key_flag = False
        my_ship.sound.pause()
    if simplegui.KEY_MAP["space"] == key:
        #a_missile.sound.pause()
        pass
    

def draw(canvas):
    global time
    global missile_flag, a_missile
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    if missile_flag == True:
        a_missile.draw(canvas)
        
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    if missile_flag == True:
        a_missile.update()
        
    canvas.draw_text("Life : " + str(lives), [20, 40], 30, "White")
    canvas.draw_text("Score : " + str(score), [650, 40], 30, "White")
            
# timer handler that spawns a rock    
def rock_spawner():
    a_rock.pos = [random.randrange(0, WIDTH),random.randrange(0, HEIGHT)]

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], ship_angle, ship_image, ship_info, ship_thrust_sound)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Missile([0,0], [0,0], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()