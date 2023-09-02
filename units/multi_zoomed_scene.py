from manim import *

class MultiZoomedScene(MovingCameraScene):
	def __init__(self, camera_class = MultiCamera, **kwargs):
		super().__init__(camera_class = camera_class, **kwargs)

	def add_zooming(self, 
			camera_center = ORIGIN, 
			display_width = 4, display_height = 3, 
			display_corner = UR, display_buff = DEFAULT_MOBJECT_TO_EDGE_BUFFER,
			display_center = None,
			factor = 10,

			camera_frame_config = {
				"default_frame_stroke_width" : 1
			},

			display_frame_config = {
				"stroke_width": 1,
				"stroke_color": WHITE,
				"buff": 0,
			},
		):

		camera = MovingCamera(**camera_frame_config)
		image = ImageMobjectFromCamera(camera, default_display_frame_config = display_frame_config)
		camera.image = image

		image.add_display_frame()
		image.stretch_to_fit_width(display_width)
		image.stretch_to_fit_height(display_height)

		if display_center != None:
			image.move_to(display_center)
		else:
			image.to_corner(display_corner, display_buff)

		self.camera.add_image_mobject_from_camera(image)

		camera.frame_center = camera_center
		self.set_zoomed_factor(camera, factor)

		return camera, image

	def activate_zooming(self, camera, animate = False):
		image = camera.image

		if not image:
			raise "invalid camera"

		# self.camera.add_image_mobject_from_camera(image)

		self.add_foreground_mobject(camera.frame)

		if animate:
			self.play(self.generate_camera_animation(camera))
			self.play(self.generate_image_animation(image))

		self.add_foreground_mobject(image)

	def set_zoomed_factor(self, camera, factor):
		image = camera.image

		if not image:
			raise "invalid camera"
		
		camera.frame_width = image.get_width() / factor
		camera.frame_height = image.get_height() / factor
		camera.cairo_line_width_multiple = self.camera.cairo_line_width_multiple / factor

	def generate_camera_animation(self, camera):
		frame = camera.frame
		frame.save_state()
		frame.center()
		frame.stretch_to_fit_width(self.camera.frame_width)
		frame.stretch_to_fit_height(self.camera.frame_height)
		frame.set_stroke(width = 0)
		return ApplyMethod(frame.restore)

	def generate_image_animation(self, image):
		image.save_state()
		image.replace(image.camera.frame, stretch=True)
		return ApplyMethod(image.restore)

	def inactivate_zooming(self, camera, animate = False):
		pass