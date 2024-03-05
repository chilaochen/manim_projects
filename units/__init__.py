import os
from manim import *
from .mobjects import *
from .animations import *
from .zooming_scene import *
from .multi_zoomed_scene import *
from .fourier_drawer import *

mono_font = "Consolas"

#https://github.com/lxgw/LxgwWenKai
Text.set_default(font = "LXGW WenKai", font_size = 24)

NumberLine.set_default(tip_shape = StretchTip)
Arrow.set_default(tip_shape = StretchTip)

#tex_template
tex_template = TexTemplateFromFile(tex_filename = os.path.join("units", "template.tex"))
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

#move Camera down so Mobject create in the center of the subject of the video
def align_camera_with_stage(self):
	self.camera.frame_center = -STAGE_CENTER

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

setattr(Scene, "align_camera_with_stage", align_camera_with_stage)
setattr(Mobject, "to_stage_corner", to_stage_corner)
setattr(Mobject, "to_stage_edge", to_stage_edge)