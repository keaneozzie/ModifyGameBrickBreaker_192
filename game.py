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