from manim import *
from units import right_triangle

class basel_circle(VMobject):
	def __init__(self, circle_num, radius = 1, angle_length = 0.1, color = BLUE, **kwargs):
		super().__init__(**kwargs)
		
		self.circle_num = 0
		self.radius = radius
		self.angle_length = angle_length
		self.color = color
		self.circles = VGroup()
		self.triangles = VGroup()
		self.add(self.circles)
		self.add(self.triangles)

		for _ in range(circle_num):
			self.add_circle(**kwargs)

	def add_circle(self, angle_length = None, color = None, **kwargs):
		circle = self.make_circle(angle_length, color, **kwargs)
		return self.attach_circle(circle)
	
	def attach_circle(self, circle):
		self.circles.add(circle)
		self.triangles.add(circle.triangles)
		self.circle_num += 1
		return self
	
	def make_circle(self, angle_length = None, color = None, **kwargs):
		if angle_length is None:
			angle_length = self.angle_length

		last_circle = None
		if self.circle_num == 0:
			radius = self.radius
		else:
			last_circle = self.circles[-1]
			radius = last_circle.height

		if color is None:
			color = self.color  if last_circle is None else last_circle.get_color()

		circle = Circle(radius, color, **kwargs).rotate(-PI / 2)
		circle.triangles = VGroup()

		if self.circle_num == 0:
			triangle = right_triangle(circle.get_right(), circle.get_bottom(), circle.get_center(), angle_length, False)
			circle.triangles.add(triangle)
		else:
			circle.match_x(last_circle).align_to(last_circle, DOWN)

			num = np.power(2, self.circle_num - 1)
			angle_start = PI * (0.25 / num - 0.5)
			angle_step = PI / num
			stroke_width = DEFAULT_STROKE_WIDTH / (np.log(num) + 1)

			for i in range(num):
				b_angle = angle_start + i * angle_step
				a_angle = b_angle + PI
				pa = pos_on_circle(circle, a_angle)
				pb = pos_on_circle(circle, b_angle)
				pc = circle.get_bottom()
				triangle = right_triangle(pa, pb, pc, angle_length).set_stroke(width = stroke_width)
				circle.triangles.add(triangle)

		return circle
	
def pos_on_circle(circle, angle):
	r = circle.height / 2
	return circle.get_center() + RIGHT * r * np.cos(angle) + UP * r * np.sin(angle)
