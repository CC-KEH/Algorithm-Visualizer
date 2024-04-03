def animate(self):
    self.animation_radius += 2
    if self.animation_radius > self.size // 2:
        self.animation_radius = 0
