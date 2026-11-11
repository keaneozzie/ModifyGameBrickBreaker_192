import random
import tkinter as tk


class GameObject(object):

  def __init__(self, canvas, item):
    self.canvas = canvas
    self.item = item

  def get_position(self):
    return self.canvas.coords(self.item)

  def move(self, x, y):
    self.canvas.move(self.item, x, y)

  def delete(self):
    try:
      self.canvas.delete(self.item)
    except Exception:
      pass

class Ball(GameObject):

  def __init__(self, canvas, x, y):
    self.radius = 15
    self.direction = [1, -1]
    self.speed = 10
    self.pulse_state = True
    item = canvas.create_oval(
        x - self.radius,
        y - self.radius,
        x + self.radius,
        y + self.radius,
        fill="#ff0000",
        outline="#ff5555",
        width=3,
    )
    super(Ball, self).__init__(canvas, item)

  def update(self):
    coords = self.get_position()
    width = self.canvas.winfo_width()
    if coords[0] <= 0 or coords[2] >= width:
      self.direction[0] *= -1
    if coords[1] <= 0:
      self.direction[1] *= -1

    self.pulse_state = not self.pulse_state
    if self.pulse_state:
      self.canvas.itemconfig(self.item, fill="#ff0033", outline="#ffffff")
    else:
      self.canvas.itemconfig(self.item, fill="#8b0000", outline="#ff0000")

    x = self.direction[0] * self.speed
    y = self.direction[1] * self.speed
    self.move(x, y)

  def collide(self, game_objects):
    coords = self.get_position()
    x = (coords[0] + coords[2]) * 0.5
    if len(game_objects) > 1:
      self.direction[1] *= -1
    elif len(game_objects) == 1:
      game_object = game_objects[0]
      coords = game_object.get_position()
      if x > coords[2]:
        self.direction[0] = 1
      elif x < coords[0]:
        self.direction[0] = -1
      else:
        self.direction[1] *= -1

    for game_object in game_objects:
      if isinstance(game_object, Brick):
        game_object.hit()


class Paddle(GameObject):

  def __init__(self, canvas, x, y):
    self.width = 130
    self.height = 15
    self.ball = None
    item = canvas.create_rectangle(
        x - self.width / 2,
        y - self.height / 2,
        x + self.width / 2,
        y + self.height / 2,
        fill="#550000",
        outline="#ff0000",
        width=2,
    )
    super(Paddle, self).__init__(canvas, item)

  def set_ball(self, ball):
    self.ball = ball

  def move(self, offset):
    coords = self.get_position()
    width = self.canvas.winfo_width()
    if coords[0] + offset >= 0 and coords[2] + offset <= width:
      super(Paddle, self).move(offset, 0)
      if self.ball is not None:
        self.ball.move(offset, 0)

  def set_position(self, x):
    coords = self.get_position()
    current_width = coords[2] - coords[0]
    width = self.canvas.winfo_width()

    new_x0 = x - current_width / 2
    new_x2 = x + current_width / 2

    if new_x0 >= 0 and new_x2 <= width:
      offset = new_x0 - coords[0]
      super(Paddle, self).move(offset, 0)
      if self.ball is not None:
        self.ball.move(offset, 0)

  def widen(self):
    coords = self.get_position()
    self.width = min(220, self.width + 40)
    self.canvas.coords(
        self.item, coords[0], coords[1], coords[0] + self.width, coords[3]
    )

    class Brick(GameObject):
  COLORS = {1: "#4a0000", 2: "#5c1d5c", 3: "#2b2b2b"}

  def __init__(self, canvas, x, y, hits, game_app):
    self.width = 85
    self.height = 22
    self.hits = hits
    self.game_app = game_app
    color = Brick.COLORS[hits]
    item = canvas.create_rectangle(
        x - self.width / 2,
        y - self.height / 2,
        x + self.width / 2,
        y + self.height / 2,
        fill=color,
        outline="#ff0000",
        tags="brick",
    )
    super(Brick, self).__init__(canvas, item)

  def hit(self):
    self.hits -= 1
    self.game_app.score += 15
    self.game_app.update_score_text()

    coords = self.get_position()
    cx = (coords[0] + coords[2]) / 2
    cy = (coords[1] + coords[3]) / 2
    self.game_app.spawn_particles(cx, cy)

    if self.hits == 0:
      self.delete()
      if random.random() < 0.25:
        self.game_app.spawn_powerup(cx, cy)
    else:
      self.canvas.itemconfig(self.item, fill=Brick.COLORS[self.hits])