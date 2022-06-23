from typing import Tuple, Union

import pygame as pg


class Predator(pg.sprite.Sprite):
    """This class represents the predator."""

    def __init__(
        self,
        pos: pg.Vector2 = pg.Vector2(0, 0),
        vel: pg.Vector2 = pg.Vector2(0, 0),
    ):
        super().__init__()
        use_ellipse = False
        if use_ellipse:
            self.orig_image = pg.Surface((20, 40))
            self.orig_image.fill(pg.Color("blue"))
            pg.draw.ellipse(
                self.orig_image,
                pg.Color("white"),
                [0, 0, *self.orig_image.get_size()],
            )
        else:
            # load the image
            self.orig_image = pg.image.load("bird_diamond.png").convert()
            self.orig_image = pg.transform.scale(self.orig_image, (20, 40))
            self.orig_image = pg.transform.rotate(self.orig_image, 90)
            self.orig_image.set_colorkey(pg.Color("white"))

        self.image = self.orig_image
        self.rect = self.image.get_rect()
        self.pos = pos
        self.vel = vel
        self.angle = 0
        self.prev_pos = self.pos

    def update(self):
        """Update the predator location."""
        # Store the old position
        self.prev_pos = self.pos

        predator_attack_model = "mouse"
        match predator_attack_model:
            case "attack_center":
                # Aim at the center of the flock
                flock_center = get_flock_center(boids)
                new_pos, self.vel = move_to(self.pos, flock_center, desired_speed=5)
            case "attack_nearest":
                # Aim at the nearest boid
                nearest_boid = self.get_nearest_boid(boids)
                new_pos, self.vel = move_to(self.pos, nearest_boid, desired_speed=5)
            #case "attack_isolated":
            #    # Aim at the most isolated boid
            #    most_isolated_boid = pg.Vector2()
            #    new_pos, self.vel = move_to(self.pos, most_isolated_boid, desired_speed=5)
            case default: # "mouse"
                # Aim at the mouse
                mouse_pos = pg.Vector2(pg.mouse.get_pos())
                new_pos, self.vel = move_to(self.pos, mouse_pos, desired_speed=5)

        if new_pos is not None:
            self.pos = new_pos

            # Find the angle of motion and rotate the image
            self.angle = self.vel.angle_to(pg.Vector2(0, 0)) - 180
            self.image = pg.transform.rotate(self.orig_image, self.angle)

            # Move the image to the correct position
            self.rect = self.image.get_rect(center=self.pos)

    def get_nearest_boid(self, boids):
        nearest_distance = 1_000_000_000
        for boid in boids:
            # Calculate the distance between in predator and the boids
            distance = boid.pos.distance_to(self.pos)
            if distance <= nearest_distance:
                nearest_boid = boid.pos
        return nearest_boid
        
def get_flock_center(boids):
    sum_positions = pg.Vector2(0, 0)
    num_boids = 0
    for boid in boids:
        sum_positions += boid.pos
        num_boids += 1

    # There should at least 2 boids, yourself and another boid
    if num_boids >= 2:
        # Calculate the center of mass
        center_of_mass = sum_positions / num_boids
    return center_of_mass

def move_to(
    curr_pos: pg.Vector2,
    desired_pos: pg.Vector2,
    desired_speed: float = 10,
    tolerance: float = 10,
) -> Tuple[Union[pg.Vector2, None], pg.Vector2]:
    """Move the object toward the desired position.

    Args:
        curr_pos (pg.Vector2): Current position vector
        desired_pos (pg.Vector2): Desired position vector
        desired_speed (float, optional): Desired speed toward new
            position. Defaults to 5.
        tolerance (float, optional): Minimum distance before calculating
            the new position. Defaults to 10.

    Returns:
        new_pos (pg.Vector2): New position vector. None if the object is
            within the tolerance.
        vel (pg.Vector2): Velocity vector
    """
    new_pos = None
    velocity = pg.Vector2(0, 0)

    # Distance from curr_pos to target_pos
    dist = curr_pos.distance_to(desired_pos)

    if dist > tolerance:
        # Velocity vector in direction of desired_pos
        velocity = (desired_pos - curr_pos).normalize() * desired_speed

        # Only update new position if distance is greater zero
        new_pos = curr_pos + velocity

    return new_pos, velocity  # type: ignore

