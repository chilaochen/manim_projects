from typing import Callable
from manim import *
from manim.typing import Point3D

class right_triangle(VMobject):
	def __init__(self, pa:Point3D|Callable[[],Point3D], pb:Point3D|Callable[[],Point3D], pc:Point3D|Callable[[],Point3D], length = 0.12, has_h = True, **kwargs):
		super().__init__(**kwargs)

		self.pos_a = pa
		self.pos_b = pb
		self.pos_c = pc
		self.length = length

		self.line_a = Line().rotate(1)
		self.line_b = Line().rotate(2)
		self.line_c = Line().rotate(3)
		self.t_angle = RightAngle(self.line_a, self.line_b)
		self.lines = Group(self.line_a, self.line_b, self.line_c)

		self.add(self.line_a, self.line_b, self.line_c, self.t_angle)

		self.has_h = False
		if has_h:
			self.add_h()

		right_triangle.triangle_updater(self)
		if callable(pa) or callable(pb) or callable(pc):
			self.add_updater(right_triangle.triangle_updater)

	def add_h(self):
		if not self.has_h:
			self.line_h = self.line_c.copy().rotate(1)
			self.h_angle = RightAngle(self.line_h, self.line_c)
			self.add(self.line_h, self.h_angle)
			self.has_h = True
			right_triangle.triangle_updater(self)

	@property
	def pa(self):
		return self.line_c.get_end()
	
	@property
	def pb(self):
		return self.line_c.get_start()
	
	@property
	def pc(self):
		return self.line_a.get_start()
	
	@property
	def ph(self):
		return self.line_h.get_end()

	@staticmethod
	def triangle_updater(self):
		pa = np.array(self.pos_a() if callable(self.pos_a) else self.pos_a)
		pb = np.array(self.pos_b() if callable(self.pos_b) else self.pos_b)
		pc = np.array(self.pos_c() if callable(self.pos_c) else self.pos_c)
		self.line_a.put_start_and_end_on(pc, pb)
		self.line_b.put_start_and_end_on(pc, pa)
		self.line_c.put_start_and_end_on(pb, pa)
		self.t_angle.become(RightAngle(self.line_a, self.line_b, self.length))

		if self.has_h:
			v1 = pa - pb
			v2 = pc - pb
			w = np.dot(v1, v2) / np.dot(v1, v1)
			ph = w * pa + (1 - w) * pb

			self.line_h.put_start_and_end_on(pc, ph)
			self.h_angle.become(RightAngle(self.line_h, self.line_c, self.length, quadrant = (-1, 1)))