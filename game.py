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
    item = canvas.create_oval(...)
    super(Ball, self).__init__(canvas, item)

  def update(self):
    # Logika pergerakan dan pantulan bola
    ...


class Paddle(GameObject):

  def __init__(self, canvas, x, y):
    self.width = 130
    self.height = 15
    self.ball = None
    item = canvas.create_rectangle(...)
    super(Paddle, self).__init__(canvas, item)

  def move(self, offset):
    ...