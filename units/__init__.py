import os
from manim import *
from .mobjects import *
from .animations import *
from .zooming_scene import *
from .multi_zoomed_scene import *
from .fourier_drawer import *

mono_font = "Consolas"

#https://github.com/lxgw/LxgwWenKai
Text.set_default(font = "LXGW WenKai", font_size = 36)

NumberLine.set_default(tip_shape = StretchTip)
Arrow.set_default(tip_shape = StretchTip)
SurroundingRectangle.set_default(corner_radius = 0.1)

#tex_template
tex_template = TexTemplate.from_file(os.path.join("units", "template.tex"), tex_compiler="xelatex", output_format=".xdv")
# tex_template = TexTemplateFromFile(tex_compiler="xelatex", output_format=".xdv", tex_filename = os.path.join("units", "template.tex"))
SingleStringMathTex.set_default(tex_template = tex_template)
MathTex.set_default(tex_template = tex_template)
Tex.set_default(tex_template = tex_template)

FRAME_WIDTH = config["frame_width"]
FRAME_HEIGHT = config["frame_height"]

#leave some space at the bottom for subtitles
SUBTITLE_HEIGHT = 0.5
STAGE_WIDTH = FRAME_WIDTH
STAGE_HEIGHT = FRAME_HEIGHT - SUBTITLE_HEIGHT
STAGE_CENTER = UP * SUBTITLE_HEIGHT
STAGE_TOP = STAGE_CENTER + UP * STAGE_HEIGHT / 2
STAGE_BOTTOM = STAGE_CENTER + DOWN * STAGE_HEIGHT / 2
STAGE_LEFT = LEFT * STAGE_WIDTH / 2
STAGE_RIGHT = RIGHT * STAGE_WIDTH / 2

#move Camera down so Mobject create in the center of the subject of the video
def align_camera_with_stage(scene):
	scene.camera.frame_center = -STAGE_CENTER

#avoid moving Mobject up and out of view
def to_stage_corner(self, corner = DL, *args):
	if (corner == UL).all() or (corner == UR).all():
		return self.to_corner(corner, *args).shift(-STAGE_CENTER)
	else:
		return self.to_corner(corner, *args)

def to_stage_edge(self, edge = LEFT, *args):
	if (edge == UP).all():
		return self.to_edge(edge, *args).shift(-STAGE_CENTER)
	else:
		return self.to_edge(edge, *args)

# setattr(Scene, "align_camera_with_stage", align_camera_with_stage)
setattr(Mobject, "to_stage_corner", to_stage_corner)
setattr(Mobject, "to_stage_edge", to_stage_edge)

def prepare_for_nonlinear_transform(mobject : Mobject, num_inserted_curves: int = 50) -> Mobject:
	for mob in mobject.family_members_with_points():
		num_curves = mob.get_num_curves()
		if num_inserted_curves > num_curves:
			mob.insert_n_curves(num_inserted_curves - num_curves)
	return mobject

def attach_dots_on_cube(cube, **kwargs):
	dots = VGroup()
	for s in cube[0:2]:
		for i in range(len(s.get_vertices())):
			dots.add(Dot(**kwargs).add_updater(lambda m,s=s,i=i: m.move_to(s.get_vertices()[i]).set_opacity(s.get_stroke_opacity())))
	return dots.set_z_index(1)