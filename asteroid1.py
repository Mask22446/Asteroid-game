import arcade
import math
import random
from abc import ABC
from abc import abstractmethod

#global contastans
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.05
SHIP_RADIUS = 30

ENERGY_BAR_X = 60
ENERGY_BAR_Y = SCREEN_HEIGHT - 20
ENERGY_BAR_WIDTH = 100
ENERGY_BAR_HEIGHT = 20

INTIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15
BIG_ROCK_POINT = 1

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5
MEDIUM_ROCK_POINT = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2
SMALL_ROCK_POINT = 10

class Point:
    #setting of zeros of coordinats to the center of screen
    def __init__(self):
        self.dx = 0.0
        self.dy = 0.0

class Velocity:
    #setting the speed of move for objects
    def  __init__(self):
        self.dx = 0.0
        self.dy = 0.0

class FlyingObject(ABC):
    #abstract basic class
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.alive = True
        self.radius = 0 
        self.angle = 0

    @abstractmethod
    def draw(self):
        pass

    def advance(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    def wrap(self,screen_width, screen_height):
        #appearing of object of screen if that object going out of screen
        if self.center.x > screen_width:
            self.center.x = 0
        elif self.center.x < 0:
            self.center.x = screen_width
        elif self.center.y > screen_height:
            self.center.y = 0
        elif self.center.y < 0:
            self.center.y = screen_height
    
class EnergyBar:
    #set the energy that measure the life of ship
    def __init__(self):
        self.center = Point()
        self.center.x = ENERGY_BAR_X
        self.center.y = ENERGY_BAR_Y
        self.alive = True
        self._width = ENERGY_BAR_WIDTH
        self.height = ENERGY_BAR_HEIGHT
        self.color = arcade.color.GREEN
        self.angle = 0

    #width as property
    @property
    def width(self):
        if self._width <= 0:
            return 0
        return self._width

    def draw(self):
        arcade.draw_rectangle_filled(self.center.x, self.center.y, self.width, self.height, self.color, self.angle)

    #decreasing of life bar when ship hitted by asteroid
    def lifereduce(self):
        self._width -= 20
        if self._width == 0:
            self.alive = False

class Ship(FlyingObject):
    #setting attributes and methods from flying object
    def __init__(self):
        super().__init__()
        self.radius = SHIP_RADIUS
        self.center.x = SCREEN_WIDTH // 2
        self.center.y = SCREEN_HEIGHT // 2
        self.turn = SHIP_TURN_AMOUNT


    def draw(self):
        img = "images/playerShip1_orange.png"
        texture = arcade.load_texture(img)
        width = texture.width
        height = texture.height
        alpha = 1
        x = self.center.x
        y = self.center.y
        angle = self.angle
        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)


class Bullet(FlyingObject):
    def __init__(self):
        super().__init__()
        self.velocity.dx = BULLET_SPEED
        self.velocity.dy = BULLET_SPEED
        self.radius = BULLET_RADIUS
        self.life = BULLET_LIFE
        self.angle = 90
    
    def draw(self):
        img = "images/laserBlue01.png"
        texture = arcade.load_texture(img)
        img = "images/playerShip1_orange.png"
        texture = arcade.load_texture(img)
        width = texture.width
        height = texture.height
        alpha = 1
        x = self.center.x
        y = self.center.y
        angle = self.angle
        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)

    def fire(self, angle):
        self.velocity.dx = math.cos(math.radians(angle - 270)) * BULLET_SPEED
        self.velocity.dy = math.sin(math.radians(angle - 270)) * BULLET_SPEED
        return(self.velocity.dx, self.velocity.dy)

    #store of bullets in the ship
    def store(self, ship):
        self.center.x = ship.center.x
        self.center.y = ship.center.y
        self.angle += ship.angle
        self.velocity.dx = ship.velocity.dx + self.fire(ship.angle)[0]
        self.velocity.dy = ship.velocity.dy + self.fire(ship.angle)[1]


class Asteroid(FlyingObject, ABC):
    #Abstract base class for asteroids based on flying object class
    def __init__():
        super().__init__()
        self.spinspeed = 0
        self.point = 0

    @abstractmethod
    def draw(self):
        pass

    #in addition to speed, asteroids spin over as it advances
    def advance(self):
        self.angle += self.spinspeed
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    @abstractmethod
    def divide(self):
        pass
    
    def hit(self):
        parts.divide()
        return [parts, self.point]

class LargeAstr(Asteroid):
    def __init__(self):
        super().__init__()
        self.center.x = random.uniform(0, SCREEN_WIDTH)
        self.center.y = random.uniform(0, SCREEN_HEIGHT)
        self.velocity.dx = random.uniform(-BIG_ROCK_SPEED, BIG_ROCK_SPEED)
        self.velocity.dy = random.uniform(-BIG_ROCK_SPEED, BIG_ROCK_SPEED)
        self.radius = BIG_ROCK_RADIUS
        self.spinspeed = BIG_ROCK_SPIN
        self.point = BIG_ROCK_POINT

    def draw(self):
        img = "images/meteorGrey_big1.png"
        texture = arcade.load_texture(img)
        width = texture.width
        height = texture.height
        alpha = 1
        x = self.center.x
        y = self.center.y
        angle = self.angle
        arcade.draw_texture_rectangle(x, y, width, height,texture,angle, alpha)

    def divide(self):
        parts=[MediumAster(), SmallAster(), SmallAster()]
        for part in parts:
            part.center.x = self.center.x
            part.center.y = self.center.y
        return parts
    
class MediumAster(Asteroid):
    def __init__(self):
        super().__init__()
        self.velocity.dx = random.uniform(-(BIG_ROCK_SPEED + 2), (BIG_ROCK_SPEED + 2))
        self.velocity.dy = random.uniform(-(BIG_ROCK_SPEED + 2), (BIG_ROCK_SPEED + 2))
        self.radius = MEDIUM_ROCK_RADIUS
        self.spinspeed = MEDIUM_ROCK_SPIN
        self.point = MEDIUM_ROCK_POINT

    def draw(self):
        img = "images/meteorGrey_med1.png"
        texture = arcade.load_texture(img)
        width = texture.width
        height = texture.height
        alpha = 1
        x = self.center.x
        y = self.center.y
        angle = self.angle
        arcade.draw_texture_rectangle(x, y, width, height,texture,angle, alpha)

    def divide(self):
        parts=[SmallAster(), SmallAster()]
        for part in parts:
            part.center.x = self.center.x
            part.center.y = self.center.y
        return parts
    
class SmallAster(Asteroid):
        def __init__(self):
        super().__init__()
        self.center.x = random.uniform(0, SCREEN_WIDTH)
        self.center.y = random.uniform(0, SCREEN_HEIGHT)
        self.velocity.dx = random.uniform(-(BIG_ROCK_SPEED + 5), (BIG_ROCK_SPEED + 5))
        self.velocity.dy = random.uniform(-(BIG_ROCK_SPEED + 5), (BIG_ROCK_SPEED + 5))
        self.radius = SMALL_ROCK_RADIUS
        self.spinspeed = SMALL_ROCK_SPIN
        self.point = SMALL_ROCK_POINT

    def draw(self):
        img = "images/meteorGrey_small1.png"
        texture = arcade.load_texture(img)
        width = texture.width
        height = texture.height
        alpha = 1
        x = self.center.x
        y = self.center.y
        angle = self.angle
        arcade.draw_texture_rectangle(x, y, width, height,texture,angle, alpha)

    def divide(self):
        parts=[]
        return parts
    
class Game(arcade.Window):
    def __init__(self, width, height):
        super().__init__()
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        self.ship = Ship()
        self.eneergybar = EnergyBar()
        self.held_keys = set()
        self.bullets = list()
        self.asteroids = list()
        self.score = 0
        for i in range(5):
            asteroid = LargeAstr()
            self.asteroids.append(asteroid)

    def on_draw(self):
        arcade.start_render()
        
        self.draw_score()

        for bullet in self.bullets:
            bullet.draw()
        
        for asteroid in self.asteroids:
            asteroid.draw()

        if self.energybar.alive:
            self.energybar.draw()
            
        if self.ship.alive:
            self.ship.draw()
        
        # if ship died or all asteroids disappeared, it will show game over message.
        if not self.ship.alive or len(self.asteroids) == 0:
            self.ship.alive = False
            self.energybar.alive = False


    def draw_score(self):
        score_text = "Score: {}".format(self.score)
        start_x = SCREEN_WIDTH - 80
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.WHITE)            


    def update(self, delta_time):
        self.check_keys()
        self.check_collisions()

        if self.ship.alive:
            self.ship.advance()
            self.ship.wrap(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        for bullet in self.bullets:
            bullet.advance()
            
        for asteroid in self.asteroids:
            asteroid.advance()
            asteroid.wrap(SCREEN_WIDTH, SCREEN_HEIGHT)


    def check_collisions(self):
        for asteroid in self.asteroids:

            if self.ship.alive and asteroid.alive:
                    too_close = self.ship.radius + asteroid.radius

                    if (abs(self.ship.center.x - asteroid.center.x) < too_close and
                                abs(self.ship.center.y - asteroid.center.y) < too_close):
                        self.energybar.lifereduce()
                        asteroid.alive = False
                        if not self.energybar.alive:
                            self.ship.alive = False


        for bullet in self.bullets:
            for asteroid in self.asteroids:
                if bullet.alive and asteroid.alive:
                    too_close = bullet.radius + asteroid.radius

                    if (abs(bullet.center.x - asteroid.center.x) < too_close and
                                abs(bullet.center.y - asteroid.center.y) < too_close):
                        bullet.alive = False
                        asteroid.alive = False
                        self.score += asteroid.hit()[1]
                        

                            
        self.cleanup_zombies()


    def cleanup_zombies(self):
        for bullet in self.bullets:
            if (abs(self.ship.center.x - bullet.center.x) > BULLET_LIFE or
                                abs(self.ship.center.y - bullet.center.y) > BULLET_LIFE):
                bullet.alive = False
            if not bullet.alive:
                self.bullets.remove(bullet)
            
                
        for asteroid in self.asteroids:
            if not asteroid.alive:
                self.asteroids.remove(asteroid)
                self.asteroids += asteroid.hit()[0]


    def check_keys(self):
        # regenerate the ship and energybar as it is initiated.
        if arcade.key.ENTER in self.held_keys:
            if not self.ship.alive and not self.energybar.alive:
                self.energybar.__init__()
                self.ship.__init__()
            
        
        if arcade.key.LEFT in self.held_keys:
            self.ship.angle += self.ship.turn
    

        if arcade.key.RIGHT in self.held_keys:
            self.ship.angle -= self.ship.turn

        if arcade.key.UP in self.held_keys:
            self.ship.velocity.dx += math.cos(math.radians(self.ship.angle + 90)) * SHIP_THRUST_AMOUNT
            self.ship.velocity.dy += math.sin(math.radians(self.ship.angle + 90)) * SHIP_THRUST_AMOUNT
            # limit the speed of ship from -5 to 5
            if self.ship.velocity.dx > 5:
                self.ship.velocity.dx = 5
            if self.ship.velocity.dx < -5:
                self.ship.velocity.dx = -5
            if self.ship.velocity.dy > 5:
                self.ship.velocity.dy = 5
            if self.ship.velocity.dy < -5:
                self.ship.velocity.dy = -5

        if arcade.key.DOWN in self.held_keys:
            self.ship.velocity.dx -= math.cos(math.radians(self.ship.angle + 90)) * SHIP_THRUST_AMOUNT
            self.ship.velocity.dy -= math.sin(math.radians(self.ship.angle + 90)) * SHIP_THRUST_AMOUNT
            # limit the speed of ship from -5 to 5
            if self.ship.velocity.dx > 5:
                self.ship.velocity.dx = 5
            if self.ship.velocity.dx < -5:
                self.ship.velocity.dx = -5
            if self.ship.velocity.dy > 5:
                self.ship.velocity.dy = 5
            if self.ship.velocity.dy < -5:
                self.ship.velocity.dy = -5



    def on_key_press(self, key: int, modifiers: int):
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # TODO: Fire the bullet here!      
                bullet = Bullet()
                bullet.store(self.ship)
                self.bullets.append(bullet)
                
                    
            if key == arcade.key.LEFT:
                self.held_keys.add(arcade.key.LEFT)
                
            if key == arcade.key.RIGHT:
                self.held_keys.add(arcade.key.RIGHT)
                          
            if key == arcade.key.UP:
                self.held_keys.add(arcade.key.UP)
                
            if key == arcade.key.DOWN:
                self.held_keys.add(arcade.key.DOWN)
        
        if key == arcade.key.ENTER:
            self.held_keys.add(arcade.key.ENTER)
            

    def on_key_release(self, key: int, modifiers: int):
        if key in self.held_keys:
            self.held_keys.remove(key)
            


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()