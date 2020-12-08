import pygame, sys
from pygame.locals import *


class Mob:
    def __init__(self, mob_location, treshhold):
        self.treshhold = 30*treshhold
        self.mob_image = pygame.image.load('pictures/ghost.gif')
        self.moving_right = False
        self.last_side = 0
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.velocity = [0, 0]
        self.step_x = 5
        self.step_y = -15
        self.mob_location = mob_location
        self.mob_y_gravitation = 0
        self.gravity_step_down = 0.3
        self.mob_rect = pygame.Rect(self.mob_location[0], self.mob_location[1], self.mob_image.get_width(),
                                    self.mob_image.get_height())
        self.test_rect = pygame.Rect(500, 100, 100, 50)
        self.air_time = 0
        self.action_dist = 20

    def handle_mob(self, tiles, display, player_rect_x, player_rect_y, camera):
        self.drawing( display,  camera)
        self.define_velocity_mob(player_rect_x, player_rect_y)
        self.placement_mob(tiles)

    def placement_mob(self, tiles):
        self.collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.mob_rect.x += self.velocity[0]
        # left-right wall disabled
        self.mob_rect.y += self.velocity[1]
        touches = self.touching_mob(tiles)
        for tile in touches:
            if self.velocity[1] > 0:
                self.mob_rect.bottom = tile.top
                self.collision_types['bottom'] = True
            elif self.velocity[1] < 0:
                self.mob_rect.top = tile.bottom
                self.collision_types['top'] = True
        return self.mob_rect, self.collision_types

    def touching_mob(self, tiles):
        hit_list = []
        for tile in tiles:
            if self.mob_rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def define_velocity_mob(self, player_rect_x, player_rect_y):
        if abs(player_rect_x - self.mob_rect.x) < 300:
            if player_rect_x - self.treshhold > self.mob_rect.x:
                self.velocity[0] = self.step_x / 2
                self.moving_right = True
                self.moving_left = False
            if player_rect_x + self.treshhold < self.mob_rect.x:
                self.velocity[0] = -self.step_x / 2
                self.moving_left = True
                self.moving_right = False
            # y - axis
            if abs(player_rect_y - self.mob_rect.y) > 100 + self.treshhold:
                self.velocity[1] = -self.step_y / 2
                if abs(player_rect_y - self.mob_rect.y) == 100 :
                    self.velocity[1] = 0
            if abs(player_rect_y - self.mob_rect.y) < 100 - self.treshhold:
                self.velocity[1] = +self.step_y / 2
                if abs(player_rect_y - self.mob_rect.y) == 100:
                    self.velocity[1] = 0

    def health_mob(self, event, display, camera):
        self.red = pygame.Rect(500, 50, 50, 10)
        self.green = pygame.Rect(500, 50, 50, 10)
        if (event.pos[0] - self.mob_rect.x) ** 2 + (event.pos[1] - self.mob_rect.y) ** 2 < 10:
            display.blit(self.red, (500 - camera[0], 50 - camera[1]))
    
    def drawing(self, display, camera_speed):
        if self.moving_right:
            display.blit(pygame.transform.flip(self.mob_image, True, False),
                         (self.mob_rect.x - camera_speed[0], self.mob_rect.y - camera_speed[1]))
            self.last_side = 0
        elif self.moving_left:
            display.blit(pygame.transform.flip(self.mob_image, False, False),
                         (self.mob_rect.x - camera_speed[0], self.mob_rect.y - camera_speed[1]))
            self.last_side = 1
        elif not self.moving_right and not self.moving_left:
            if self.last_side == 0:
                display.blit(pygame.transform.flip(self.mob_image, False, False),
                             (self.mob_rect.x - camera_speed[0], self.mob_rect.y - camera_speed[1]))
            elif self.last_side == 1:
                display.blit(pygame.transform.flip(self.mob_image, True, False),
                             (self.mob_rect.x - camera_speed[0], self.mob_rect.y - camera_speed[1]))