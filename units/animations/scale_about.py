from manim import *
from manim.typing import Point3D

class ScaleAbout(Transform):
	def __init__(self, mobject: Mobject | None, scale_factor = 1, about_point: Mobject | Point3D = ORIGIN, **kwargs) -> None:
		super().__init__(mobject, **kwargs)
		self.scale_factor = scale_factor
		if isinstance(about_point, Mobject):
			self.about_point = about_point.get_center()
		else:
			self.about_point = about_point
	
	def create_target(self) -> Mobject:
		target = self.mobject.copy()
		shift = (target.get_center() - self.about_point) * self.scale_factor
		target.scale(self.scale_factor).move_to(self.about_point + shift)
		return target