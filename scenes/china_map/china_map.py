import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))
from manim import *
from units.fourier_drawer import *
from map_data import map_data

class ChinaMap(DrawPathWithZoomed):
	map_dir = os.path.join("assert", "china_map")
	max_width = 12

	n_sample = 10000

	max_top_num = 10
	max_top_percent = 0.05

	drawing_period = 58
	vector_coef = 100

	def construct(self):
		for data in map_data:
			self.data = data
			self.run_one_cycle()

	def start_cycle(self):
		super().start_cycle()
		self.text = Text('\n'.join(self.data[0]), line_spacing = min(8 / (len(self.data[0]) * 2 - 1), 1.5), font="STKaiti").to_corner(UL)

	def show_up(self):
		self.suspend_drawing()
		self.play(FadeIn(self.drawer), FadeIn(self.text))
		self.resume_drawing()

	def generate_pop_image_animation(self):
		self.text.save_state()
		return *super().generate_pop_image_animation(), self.text.animate.to_edge(LEFT, -self.text.width - DEFAULT_MOBJECT_TO_EDGE_BUFFER)

	def generate_zoom_in_to_normal_animation(self):
		return *super().generate_zoom_in_to_normal_animation(), self.text.animate.restore()

	def hide_down(self):
		self.wait_until(lambda: self.drawer.process >= 1)
		self.suspend_drawing()
		self.play(FadeOut(self.drawer), FadeOut(self.text))
		self.clear()

	def generate_original_path(self):
		svg = SVGMobject(os.path.join(self.map_dir, self.data[0]) , height = 7, **self.contour_path_config)
		if svg.width > self.max_width:
			svg.scale_to_fit_width(self.max_width)
		return svg

