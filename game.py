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
    
class Ghost(GameObject):
  """Animasi Hantu Melayang di Latar Belakang"""

  def __init__(self, canvas, x, y):
    self.direction = random.choice([-2, 2])
    head = canvas.create_oval(
        x - 20, y - 30, x + 20, y + 10, fill="#1a1a1a", outline="#ff0000", width=1
    )
    body = canvas.create_rectangle(
        x - 20, y, x + 20, y + 35, fill="#1a1a1a", outline="#ff0000", width=1
    )
    eye1 = canvas.create_oval(
        x - 10, y - 15, x - 5, y - 10, fill="#ff0000", outline=""
    )
    eye2 = canvas.create_oval(
        x + 5, y - 15, x + 10, y - 10, fill="#ff0000", outline=""
    )

    self.items_group = [head, body, eye1, eye2]
    super(Ghost, self).__init__(canvas, head)

  def update(self):
    width = self.canvas.winfo_width()
    coords = self.canvas.coords(self.item)
    if not coords:
      return

    if coords[0] <= 30 or coords[2] >= width - 30:
      self.direction *= -1

    for item in self.items_group:
      self.canvas.move(item, self.direction, 0)

  def delete(self):
    for item in self.items_group:
      try:
        self.canvas.delete(item)
      except Exception:
        pass


class Particle(GameObject):

  def __init__(self, canvas, x, y):
    self.dx = random.uniform(-4, 4)
    self.dy = random.uniform(-6, -1)
    item = canvas.create_rectangle(x, y, x + 4, y + 4, fill="#ff0000", outline="")
    super(Particle, self).__init__(canvas, item)

  def update(self):
    self.move(self.dx, self.dy)
    self.dy += 0.5

class PowerUp(GameObject):

  def __init__(self, canvas, x, y):
    self.radius = 10
    item = canvas.create_oval(
        x - self.radius,
        y - self.radius,
        x + self.radius,
        y + self.radius,
        fill="#00ff66",
        outline="#ffffff",
        tags="powerup",
    )
    super(PowerUp, self).__init__(canvas, item)

  def update(self):
    self.move(0, 6)


class Game(tk.Frame):

  def __init__(self, master):
    super(Game, self).__init__(master)
    self.master = master

    self.width = master.winfo_screenwidth()
    self.height = master.winfo_screenheight()

    self.lives = 3
    self.score = 0

    self.canvas = tk.Canvas(
        self, bg="#030303", width=self.width, height=self.height, highlightthickness=0
    )
    self.canvas.pack(fill=tk.BOTH, expand=True)
    self.pack(fill=tk.BOTH, expand=True)

    self.items = {}
    self.ball = None
    self.powerups = []
    self.particles = []
    self.ghosts = []

    self.paddle = Paddle(self.canvas, self.width / 2, self.height - 80)
    self.items[self.paddle.item] = self.paddle

    self.build_level()
    self.spawn_ghosts()

    self.hud_lives = None
    self.hud_score = None
    self.setup_game()
    self.canvas.focus_set()

    self.pressed_keys = set()
    self.canvas.bind("<KeyPress>", self.on_key_press)
    self.canvas.bind("<KeyRelease>", self.on_key_release)
    self.canvas.bind("<Motion>", self.on_mouse_motion)

    master.bind("<Escape>", lambda event: master.attributes("-fullscreen", False))

    self.handle_continuous_movement()

  def spawn_ghosts(self):
    for x_pos in [150, self.width / 2, self.width - 150]:
      ghost = Ghost(self.canvas, x_pos, 230)
      self.ghosts.append(ghost)

  def on_key_press(self, event):
    self.pressed_keys.add(event.keysym)

  def on_key_release(self, event):
    if event.keysym in self.pressed_keys:
      self.pressed_keys.remove(event.keysym)

  def on_mouse_motion(self, event):
    self.paddle.set_position(event.x)

  def handle_continuous_movement(self):
    speed = 16
    if "Left" in self.pressed_keys or "a" in self.pressed_keys or "A" in self.pressed_keys:
      self.paddle.move(-speed)
    if "Right" in self.pressed_keys or "d" in self.pressed_keys or "D" in self.pressed_keys:
      self.paddle.move(speed)

    self.master.after(20, self.handle_continuous_movement)

  def build_level(self):
    start_x = 70
    spacing = 90
    for x in range(start_x, self.width - start_x, spacing):
      self.add_brick(x, 90, 3)
      self.add_brick(x, 120, 2)
      self.add_brick(x, 150, 1)

  def setup_game(self):
    self.add_ball()
    self.update_hud()
    self.text = self.draw_text(
        self.width / 2, self.height / 2 - 40, "▶ TEKAN SPASI UNTUK BERTAHAN ◀", "#ff0000", 28
    )
    self.canvas.bind("<space>", lambda _: self.start_game())

  def add_ball(self):
    if self.ball is not None:
      self.ball.delete()
    paddle_coords = self.paddle.get_position()
    x = (paddle_coords[0] + paddle_coords[2]) * 0.5
    self.ball = Ball(self.canvas, x, self.height - 110)
    self.paddle.set_ball(self.ball)

  def add_brick(self, x, y, hits):
    brick = Brick(self.canvas, x, y, hits, self)
    self.items[brick.item] = brick

  def spawn_powerup(self, x, y):
    p = PowerUp(self.canvas, x, y)
    self.powerups.append(p)

  def spawn_particles(self, x, y):
    for _ in range(5):
      p = Particle(self.canvas, x, y)
      self.particles.append(p)

  def draw_text(self, x, y, text, color="#ff0000", size=24):
    font = ("Courier New", size, "bold")
    return self.canvas.create_text(
        x, y, text=text, font=font, fill=color, anchor="center"
    )

  def update_hud(self):
    lives_str = f"NYAWA: {self.lives}"
    score_str = f"SKOR: {self.score}"
    if self.hud_lives is None:
      self.hud_lives = self.canvas.create_text(
          90, 30, text=lives_str, fill="#ff0000", font=("Courier New", 14, "bold")
      )
      self.hud_score = self.canvas.create_text(
          self.width - 100,
          30,
          text=score_str,
          fill="#00ffcc",
          font=("Courier New", 14, "bold"),
      )
    else:
      self.canvas.itemconfig(self.hud_lives, text=lives_str)
      self.canvas.itemconfig(self.hud_score, text=score_str)

  def update_score_text(self):
    self.canvas.itemconfig(self.hud_score, text=f"SKOR: {self.score}")

  def start_game(self):
    self.canvas.unbind("<space>")
    self.canvas.delete(self.text)
    self.paddle.ball = None
    self.game_loop()

  def trigger_jump_scare_flash(self):
    self.canvas.config(bg="#4a0000")
    self.master.after(120, lambda: self.canvas.config(bg="#1a0000"))
    self.master.after(240, lambda: self.canvas.config(bg="#030303"))

  def game_loop(self):
    self.check_collisions()

    for ghost in self.ghosts:
      ghost.update()

    for p in self.particles[:]:
      p.update()
      coords = p.get_position()
      if not coords or coords[3] >= self.height:
        p.delete()
        self.particles.remove(p)

    for p in self.powerups[:]:
      p.update()
      p_coords = p.get_position()
      paddle_coords = self.paddle.get_position()
      if (
          p_coords
          and paddle_coords
          and p_coords[2] >= paddle_coords[0]
          and p_coords[0] <= paddle_coords[2]
          and p_coords[3] >= paddle_coords[1]
      ):
        self.paddle.widen()
        p.delete()
        self.powerups.remove(p)
      elif p_coords and p_coords[3] >= self.height:
        p.delete()
        self.powerups.remove(p)

    num_bricks = len(self.canvas.find_withtag("brick"))
    if num_bricks == 0:
      self.ball.speed = None
      self.draw_text(
          self.width / 2, self.height / 2 - 40, "💀 SELAMAT... KAU BERTAHAN! 💀", "#00ff66", 35
      )
    elif self.ball.get_position()[3] >= self.height:
      self.ball.speed = None
      self.lives -= 1
      self.trigger_jump_scare_flash()
      self.update_hud()
      if self.lives < 0:
        self.draw_text(
            self.width / 2, self.height / 2 - 40, "☠ GAME OVER - DIA MENGAMBILMU ☠", "#ff0000", 40
        )
      else:
        self.after(1200, self.setup_game)
    else:
      self.ball.update()
      self.after(22, self.game_loop)

  def check_collisions(self):
    ball_coords = self.ball.get_position()
    items = self.canvas.find_overlapping(*ball_coords)
    objects = [self.items[x] for x in items if x in self.items]
    self.ball.collide(objects)


if __name__ == "__main__":
  root = tk.Tk()
  root.title("Horror Ghost Brick Breaker")
  root.attributes("-fullscreen", True)

  game = Game(root)
  game.mainloop()