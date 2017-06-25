from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from random import randint

Builder.load_file("PongApp.kv")

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongPaddle(Widget):
    score =  NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity

            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.2
            ball.velocity = vel.x, vel.y + offset


class PongGame(Widget):

    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down, on_key_up = self._on_keyboard_up)

        self.paddle_speed = 10
        self.controlls = {
            "w": False,
            "s": False,
            "up": False,
            "down": False,
        }

    def _keyboard_closed(self):
        print("released!")
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None


    def serve_ball(self, vel=(4,0)):
        self.ball.center = self.center
        self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))

    def update(self, dt):
        self.ball.move()

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        if self.ball.x < self.x:
            self.player1.score += 1
            self.serve_ball(vel=(4,0))

        if self.ball.x > self.width:
            self.player2.score += 1
            self.serve_ball(vel=(-4,0))

        
        if self.controlls["up"] == True:
            self.player2.center_y += self.paddle_speed

        if self.controlls["down"] == True:
            self.player2.center_y -= self.paddle_speed

        if self.controlls["w"] == True:
            self.player1.center_y += self.paddle_speed

        if self.controlls["s"] == True:
            self.player1.center_y -= self.paddle_speed

    def _on_keyboard_down(self, *args):
        k = args[1][1]

        if k in self.controlls:
            self.controlls[k] = True
    
    def _on_keyboard_up(self, *args):
        k = args[1][1]

        if k in self.controlls:
            self.controlls[k] = False
    
    

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1/60)
        return game

if __name__ == "__main__":
    PongApp().run()