from manim import *
from img_ops import *

color_map = dict(
	R = ManimColor([255, 0, 0]),
	G = ManimColor([0, 255, 0]),
	B = ManimColor([0, 0, 255]),
	Y = ManimColor([*yuv2rgb(200, 128, 128)]),
	U = ManimColor([*yuv2rgb(200, 128, 0)]),
	V = ManimColor([*yuv2rgb(200, 0, 128)]),
)

rgb2yuv_str = r"""
	Y & =          &   {{0.299}} &\times  R \quad + &   {{0.587}} &\times  G \quad + &   {{0.114}} &\times  B \\
	U & = \quad -  &{{0.168736}} &\times  R \quad - &{{0.331264}} &\times  G \quad + &     {{0.5}} &\times  B \quad + \quad 128 \\
	V & =          &     {{0.5}} &\times  R \quad - &{{0.418688}} &\times  G \quad - &{{0.081312}} &\times  B \quad + \quad 128 \\
"""

yuv2rgb_str = r"""
	R & = Y \quad + &          &                                     &   1.402 &\times (V \quad - \quad 128) \\
	G & = Y \quad - & 0.344136 &\times (U \quad - \quad 128) \quad - &0.714136 &\times (V \quad - \quad 128) \\
	B & = Y \quad + &    1.772 &\times (U \quad - \quad 128)
"""

skia_rgb2yuv_str = r"""
	Y & = (         & {{77}} &\times R \quad + &{{150}} &\times G \quad + & {{29}} &\times B) \quad {{{{\div \quad 256}}}} \\
	U & = ( \quad - & {{43}} &\times R \quad - & {{85}} &\times G \quad + &{{128}} &\times B) \quad {{{{\div \quad 256}}}} \quad + \quad 128 \\
	V & = (         &{{128}} &\times R \quad - &{{107}} &\times G \quad - & {{21}} &\times B) \quad {{{{\div \quad 256}}}} \quad + \quad 128
"""

skia_rgb2yuv_equ_str = r"""
	Y & =         & {{\frac{77}{256}}} &\times R \quad + &{{\frac{150}{256}}} &\times G \quad + & {{\frac{29}{256}}} &\times B \\
	U & = \quad - & {{\frac{43}{256}}} &\times R \quad - & {{\frac{85}{256}}} &\times G \quad + &{{\frac{128}{256}}} &\times B \quad + \quad 128 \\
	V & =         &{{\frac{128}{256}}} &\times R \quad - &{{\frac{107}{256}}} &\times G \quad - & {{\frac{21}{256}}} &\times B \quad + \quad 128
"""

math_div_str = r"""
	1 \div 2 & = 0.5 \\
	4 \div 3 & = 1.33\cdots\\
	9 \div 4 & = 2.5
"""

cs_div_str = r"""
	1 \div 2 & = 0 \\
	4 \div 3 & = 1 \\
	9 \div 4 & = 2
"""

dct_cos_str = r"f(x)={{{{{0}}}}} \times \sqrt{{ \tfrac{{ {1} }}{{ {2} }} }} \cdot \cos( {{{{ \frac{{ {3} }} {{ {2} }} }}}} \pi \cdot x)"
dct_cos_base_str = r"f(x)={{{{\omega}}}} {{{{\times}}}} \sqrt{{ \tfrac{{ {0} }}{{ {1} }} }} \cdot \cos( {{{{ \frac{{ {2} }} {{ {1} }} }}}} \pi \cdot x)"