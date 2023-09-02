from manim import *
from ..multi_zoomed_scene import *
from .draw_path import *

class DrawPathWithZoomed(DrawPath, MultiZoomedScene):
	zoom_in_camera_stroke = 0.5
	zoom_in_display_corner = UR
	zoom_in_display_buff = 0.5
	zoom_in_display_width = 8
	zoom_in_display_height = 5
	zoom_in_display_stroke = 1
	
	zoom_out_factor = 1 / 3
	zoom_out_corner = DL

	vector_coef = 100
	drawing_period = 30

	max_top_num = 10
	max_top_percent = 0.1

	min_zooming_factor = 6

	def setup(self):
		self.generate_cameras()
		self.calc_key_time()

	def run_one_cycle(self):
		self.start_cycle()
		self.show_up()
		self.normal_to_zoom_in()
		self.zoom_in_to_fullcreen()
		self.fullscreen_to_zoom_in()
		self.zoom_in_to_normal()
		self.hide_down()

	def start_cycle(self):
		self.generate_drawer()
		
		self.generate_speed_tracker()
		self.generate_factor_tracker()
		self.drawer.set_process_func(self.process_func)

		self.normal_rect = Rectangle().replace(self.drawer, stretch=True)
		self.zoom_in_rect = self.normal_rect.copy().to_edge()
		self.zoom_out_rect = self.normal_rect.copy().scale(self.zoom_out_factor).to_corner(self.zoom_out_corner)

	def show_up(self):
		self.suspend_drawing()
		self.play(FadeIn(self.drawer))
		self.resume_drawing()

	def generate_drawer(self):
		self.generate_contour_path()

		curves_and_lengths = tuple(self.contour_path.get_curve_functions_with_lengths())
		total_length = sum(length for _, length in curves_and_lengths)
		tor = total_length / (self.contour_path.width + self.contour_path.height) / 2

		self.n_vector = int(self.vector_coef * tor)
		self.drawer = FourierDrawer(self.contour_path, self.n_vector, self.n_sample)
		self.add_foreground_mobject(self.drawer)

		self.n_top = max(1, int(self.n_vector * self.max_top_percent))
		self.max_zooming_factor = 0.5 / np.average([vec.length for vec in self.drawer.vectors[-self.n_top]])
		self.mid_zooming_factor = np.sqrt(self.min_zooming_factor * self.max_zooming_factor)

	def normal_to_zoom_in(self):
		self.wait_until(lambda: self.drawer.drawn_time >= self.zoom_in_time)

		self.play(*self.generate_zoom_in_camera_animation())
		self.add_foreground_mobject(self.zoom_in_camera.frame)
		self.add_updater(self.zoomed_camera_updater)

		self.play(*self.generate_pop_image_animation())

	def zoom_in_to_fullcreen(self):
		self.wait_until(lambda : self.drawer.drawn_time >= self.zoom_to_full_time)
		self.play(*self.generate_fullscreen_animation())

	def fullscreen_to_zoom_in(self):
		self.wait_until(lambda: self.drawer.drawn_time >= self.full_to_zoom_time)
		self.play(*self.generate_fullscreen_to_zoom_in_animation())

	def generate_fullscreen_to_zoom_in_animation(self):
		image_anima = self.zoom_in_image.animate.replace(self.zoom_in_display_rect, stretch = True)
		display_anima = self.zoom_in_image.display_frame.animate.set_stroke(opacity = 1).replace(self.zoom_in_display_rect, stretch = True)
		camera_anima = self.zoom_in_camera.frame.animate.set_stroke(opacity = 1)
		drawer_anima = self.drawer.animate.replace(self.zoom_in_rect)

		return image_anima, display_anima, camera_anima, drawer_anima

	def zoom_in_to_normal(self):
		self.wait_until(lambda: self.drawer.drawn_time >= self.zoom_out_time)
		self.play(*self.generate_zoom_in_to_normal_animation())
		self.remove_updater(self.zoomed_camera_updater)

	def generate_zoom_in_to_normal_animation(self):
		camera_anima = FadeOut(self.zoom_in_camera.frame)

		self.suspend_drawing()
		future = self.drawer.drawn_time + 1
		future_drawer = self.drawer.copy().center()
		future_drawer.process = self.process_func(future)
		image_anima = FadeOut(self.zoom_in_image, target_position = future_drawer.pen_point, scale = 0.01)
		self.resume_drawing()

		drawer_anima = self.drawer.animate.replace(self.normal_rect)

		return camera_anima, image_anima, drawer_anima

	def hide_down(self):
		self.wait_until(lambda: self.drawer.process >= 1)
		self.suspend_drawing()
		self.play(FadeOut(self.drawer))
		self.clear()

	def generate_fullscreen_animation(self):
		image_anima = self.zoom_in_image.animate.replace(self.fullscreen_rect, stretch = True)
		display_anima = self.zoom_in_image.display_frame.animate.set_stroke(opacity = 0).replace(self.fullscreen_rect, stretch = True)
		camera_anima = self.zoom_in_camera.frame.animate.set_stroke(opacity = 0)
		drawer_anima = self.drawer.animate.replace(self.zoom_out_rect)

		return image_anima, display_anima, camera_anima, drawer_anima

	def generate_pop_image_animation(self):
		return self.generate_image_animation(self.zoom_in_image), self.drawer.animate.replace(self.zoom_in_rect)

	def generate_zoom_in_camera_animation(self):
		self.suspend_drawing()
		future = self.drawer.drawn_time + 1
		future_drawer = self.drawer.copy()
		future_drawer.process = self.process_func(future)
		self.zoom_in_camera.frame_center = future_drawer.pen_point
		self.set_zoomed_factor(self.zoom_in_camera, self.min_zooming_factor)
		self.resume_drawing()
		return [ReplacementTransform(self.fullscreen_rect.copy(), self.zoom_in_camera.frame)]

	def zoomed_camera_updater(self, dt):
		factor = self.factor_tracker.get_value()
		self.set_zoomed_factor(self.zoom_in_camera, factor * (self.normal_rect.get_width() / self.drawer.get_width()))

		c1 = center_of_mass([vec.get_end() for vec in self.drawer.vectors[int(-self.n_vector / 2)]])
		c2 = self.drawer.pen_point
		k = min(1, 800* (self.drawer.process - 0.5)**2)
		self.zoom_in_camera.frame_center = k * c1 + (1 - k) * c2

	def generate_cameras(self):
		self.zoom_in_camera, self.zoom_in_image = self.add_zooming(camera_frame_config = {"default_frame_stroke_width" : self.zoom_in_camera_stroke})

		self.zoom_in_display_rect = Rectangle(width = self.zoom_in_display_width, height = self.zoom_in_display_height).to_corner(self.zoom_in_display_corner, self.zoom_in_display_buff)
		self.fullscreen_rect = FullScreenRectangle(stroke_width = 0)

		self.zoom_in_image.replace(self.zoom_in_display_rect, stretch=True)

	def calc_key_time(self):
		self.zoom_in_time = 0.1 * self.drawing_period - 1
		self.zoom_to_full_time = 0.3 * self.drawing_period - 1
		self.full_to_zoom_time = 0.7 * self.drawing_period
		self.zoom_out_time = 0.9 * self.drawing_period

	def factor_updater(self, factor_tracker, dt):
		factor_tracker.set_value(self.factor_func(self.drawer.drawn_time))

	def speed_updater(self, speed_tracker, dt):
		speed_tracker.set_value(self.speed_func(self.drawer.drawn_time))

	def generate_speed_tracker(self):
		self.min_speed_factor = 6 / (self.max_zooming_factor + 2)
		self.speed_func, self.process_func = DrawPathWithZoomed.generate_speed_process_func(self.drawing_period, self.min_speed_factor)
		self.speed_tracker = ValueTracker(0)
		self.speed_tracker.add_updater(self.speed_updater, call_updater=False)
		self.add(self.speed_tracker)

	def generate_factor_tracker(self):
		self.factor_tracker = ValueTracker(1)
		self.factor_tracker.add_updater(self.factor_updater, call_updater=False)
		self.add(self.factor_tracker)

	def factor_func(self, time):
		if time < (self.zoom_in_time + 1) or time >= (self.zoom_out_time + 1):
			factor = 1
		elif time <= self.zoom_to_full_time or time >= (self.full_to_zoom_time + 1):
			factor = self.min_zooming_factor
		elif time <= (self.zoom_to_full_time + 1) or time >= (self.full_to_zoom_time):
			dt = min(time - self.zoom_to_full_time, self.full_to_zoom_time + 1 - time)
			factor = self.min_zooming_factor + (self.mid_zooming_factor - self.min_zooming_factor) * dt**2
		else:
			m = (self.max_zooming_factor - self.mid_zooming_factor) / (self.drawing_period / 5)**2
			factor = self.max_zooming_factor - m*(time - self.drawing_period / 2)**2

		return factor

	@staticmethod
	def generate_speed_process_func(t, k):
		m = (1 - k) / t**3
		speed_func = lambda x : m*3 * (2*x-t)**2 + k/t
		process_func = lambda x : m/2 * (2*x-t)**3 + k/t*x + (1-k)/2

		return speed_func, process_func