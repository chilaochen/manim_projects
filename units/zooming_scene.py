from manim import *

class ZommingScene(MovingCameraScene):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.cairo_line_width_multiple_factor = self.camera.cairo_line_width_multiple / self.camera.frame_width
		self.add_updater(self.update_cairo_line_width_multiple)

	def update_cairo_line_width_multiple(self, dt):
		self.camera.cairo_line_width_multiple = self.cairo_line_width_multiple_factor * self.camera.frame_width