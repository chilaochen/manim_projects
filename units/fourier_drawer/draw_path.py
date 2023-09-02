from manim import *
from .fourier_drawer import *

class DrawPath(Scene):
	contour_path_config = {
        "fill_opacity" : 0.0,
        "stroke_width" : 1,
        "stroke_color" : WHITE,
        "stroke_opacity" : 0.6,
	} 

	n_vector = 100
	n_sample = 10000
	drawing_period = 10

	def setup(self):
		super().setup()

		self.generate_contour_path()
		self.generate_drawer()
		
	def construct(self):
		self.run_one_cycle()

	def generate_drawer(self):
		self.drawer = FourierDrawer(self.contour_path, self.n_vector, self.n_sample)
		self.drawer.set_process_func(lambda t: t / self.drawing_period)
		self.add(self.drawer)

	def run_one_cycle(self):
		self.wait_until(lambda : self.drawer.process >= 1)

	def suspend_drawing(self):
		self.drawer.suspend_updating()

	def resume_drawing(self):
		self.drawer.resume_updating()

	def generate_contour_path(self):
		contour_path = self.generate_original_path().family_members_with_points()[0]
		self.contour_path = contour_path
		return contour_path

	def generate_original_path(self):
		return MathTex(r"\pi", font_size=1000, **self.contour_path_config)