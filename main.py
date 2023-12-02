import pygame
from pygame.math import Vector2
import math

class Body:
    def __init__(self, pos: Vector2, radius: int):
        self.pos = pos
        self.r = radius
    
    def draw(self, surf: pygame.Surface, color):
        pygame.draw.circle(surf, color, self.pos, self.r)

class Earth(Body):
    def __init__(self, pos: Vector2, radius: int, atmosphere_radius: int):
        super().__init__(pos, radius)
        self.atm_r = atmosphere_radius
    
    def draw(self, surf: pygame.Surface, color, atm_color):
        pygame.draw.circle(surf, atm_color, self.pos, self.atm_r)
        super().draw(surf, color)

class Sun(Body):
    def revolve(self, earth_pos: Vector2):
        self.pos -= earth_pos
        self.pos = (self.pos.x * Vector2( 0.9998, 0.0175 ) + self.pos.y * Vector2( -0.0175, 0.9998 )) + earth_pos # Baked from line 49
    
    def cast_ray(self, surf: pygame.Surface, earth: Earth, point: Vector2):
        # Delta vector
        d = ( point - self.pos ).normalize()
        # Ray vector begins at sun source
        ray = self.pos.copy()
        r_intensity = 100
        # Is set when ray hits earth
        hit = False
        for i in range( int( self.pos.distance_to(point) ) ):
            ray += d # Move by delta
            # Check collision
            if ray.distance_to(earth.pos) > earth.r: # If not colliding with earth
                if ray.distance_to(earth.pos) < earth.atm_r: # If colliding with atomosphere
                    r_intensity -= 1
                pygame.draw.line(surf, (0, r_intensity, 0), ray, ray + d, 3)
            else:
                hit = True

        if hit:
            return 0
        else:
            return r_intensity


# Check "maths.png" for the math on this part
# def revolve_vec(vec, pivot, angle):
#     vec -= pivot
#     radi = math.radians(angle)
#     radj = math.radians(angle + 90)

#     u = Vector2( math.cos(radi), math.sin(radi) )
#     v = Vector2( math.cos(radj), math.sin(radj) )
#     return (vec.x * u + vec.y * v) + pivot


# Inits
earth = Earth(Vector2(600, 400), 80, 120)
point = Vector2(600, 320)
sun = Sun(Vector2(600, 100), 35)

pygame.init()

size = Vector2(1200, 800)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Earth\'s Thermal System')


clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Clears screen each frame
    screen.fill((0, 0, 0))
    
    sun.revolve(earth.pos) # Revolves sun around earth
    # Draw
    sun.draw(screen, (255, 255, 0))
    earth.draw(screen, (100, 255, 255), (50, 150, 150))
    pygame.draw.circle(screen, (255, 0, 0), point, 5)
    
    # Track point intensity
    point_intensity = sun.cast_ray(screen, earth, point)
    print(point_intensity)

    # Write changes to the screen and limit framerate to 60 fps
    pygame.display.flip()
    clock.tick(60)