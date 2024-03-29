from manim import *
from manim.typing import Point3D

class ScaleAbout(Transform):
	def __init__(self, mobject: Mobject | None, scale_factor = 1, about_point: Mobject | Point3D = ORIGIN, **kwargs) -> None:
		super().__init__(mobject, **kwargs)
		self.scale_factor = scale_factor
		self.about_point = about_point
	
	def create_target(self) -> Mobject:
		target = self.mobject.copy()
		target.scale_about(self.scale_factor, self.about_point)
		return target

def scale_about(self, scale_factor, about_point: Mobject | Point3D = ORIGIN):
	if isinstance(about_point, Mobject):
		about_point = about_point.get_center()
	shift = (self.get_center() - about_point) * scale_factor
	return self.scale(scale_factor).move_to(about_point + shift)

setattr(Mobject, "scale_about", scale_about)
