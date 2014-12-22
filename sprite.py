class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
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
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated == True:
            explosion_sound.rewind()
            explosion_sound.play()
            canvas.draw_image(self.image, [self.image_center[0] + self.age * self.image_size[0], self.image_center[1]], self.image_size,
                          self.pos, self.image_size, self.angle)
            return
        canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        self.age += 1
        if self.age > self.lifespan:
            return True
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        return False
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def collide(self, other_object):
        distance = dist(self.get_position(), other_object.get_position())
        sum_r = self.get_radius() + other_object.get_radius()
        if distance > sum_r:
            return False
        else:
            return True