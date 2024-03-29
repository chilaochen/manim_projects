import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))

from units import *

class rectangle_area(MultiZoomedScene):
	def setup(self):
		align_camera_with_stage(self)

	def construct(self):
		self.next_section(skip_animations = False)
		self.integer_prove()
		self.next_section(skip_animations = False)
		self.rational_prove()
		self.next_section(skip_animations = False)
		self.real_prove()
		self.next_section(skip_animations = False)
		self.measure_overview()
		self.next_section(skip_animations = False)
		self.integration()
		self.wait()

	def integer_prove(self):
		width = 4
		height = 3
		rect = Rectangle(YELLOW, height, width).scale_to_fit_height(STAGE_HEIGHT * 0.4)
		title = Text("长方形").match_color(rect).scale_to_fit_height(0.5).next_to(rect, UP, MED_LARGE_BUFF)
		self.play(Create(rect))
		self.play(FadeIn(title))

		area_tex = SingleStringMathTex(r"S_{\text{长方形}}=\text{长}\times\text{宽}").match_height(title).move_to(title)
		tex_head = area_tex[0:4]
		tex_head[0].set_color(BLUE)
		tex_head[1:].set_color(YELLOW)
		tex_head.save_state()
		tex_head.match_x(rect)
		self.play(rect.animate.set_fill(BLUE, 1), FadeIn(tex_head[0]), ReplacementTransform(title, tex_head[1:]))
		
		tex_tail = area_tex[4:]
		width_brace = BraceLabel(rect, "长", DOWN, Text)
		height_brace = BraceLabel(rect, "宽", LEFT, Text)
		self.play(width_brace.creation_anim(), height_brace.creation_anim())
		self.play(tex_head.animate.restore(), FadeIn(tex_tail))
		self.add(area_tex)

		question = Text("?", color = RED).match_height(area_tex).next_to(area_tex, RIGHT)
		self.play(FadeIn(question, scale = 3))

		width_brace_target = BraceLabel(rect, str(width), DOWN, Text)
		height_brace_target = BraceLabel(rect, str(height), LEFT, Text)
		self.play(width_brace.animate.become(width_brace_target))
		self.play(height_brace.animate.become(height_brace_target))

		h_lines = VGroup(*[Line(rect.get_left(), rect.get_right(), color = ORANGE) for _ in range(height - 1)]).arrange(DOWN, rect.height / height).move_to(rect)
		v_lines = VGroup(*[Line(rect.get_top(), rect.get_bottom(), color = ORANGE) for _ in range(width - 1)]).arrange(RIGHT, rect.width / width).move_to(rect)
		self.play(Create(h_lines, 1 / height), Create(v_lines, 1 / width))
		
		square_group = VGroup(*[Square(rect.height / height, stroke_width = 0) for _ in range(width * height)]).arrange_in_grid(height, buff = 0).move_to(rect)
		for i in range(len(square_group)):
			s = square_group[i]
			s.add(Text(str(i+1)).scale_to_fit_height(s.height * 0.4).move_to(s))
		self.play(LaggedStart(*[FadeIn(s, scale = 0.1) for s in square_group], lag_ratio = 0.1))

		self.play(FadeOut(h_lines), FadeOut(v_lines), FadeOut(square_group), FadeOut(question))
		self.rect = rect
		self.area_tex = area_tex
		self.width_brace = width_brace
		self.height_brace = height_brace
		
	def rational_prove(self):
		width = 4.2
		height = 3.2

		width_brace_target = BraceLabel(self.rect, str(width), DOWN, Text)
		height_brace_target = BraceLabel(self.rect, str(height), LEFT, Text)
		self.play(self.width_brace.animate.become(width_brace_target))
		self.play(self.height_brace.animate.become(height_brace_target))

		rect_target = self.rect.copy().scale(0.7)
		width_brace_target = BraceLabel(rect_target, str(width), DOWN, Text)
		height_brace_target = BraceLabel(rect_target, str(height), LEFT, Text)
		VGroup(rect_target, width_brace_target, height_brace_target).to_stage_edge(LEFT)
		self.play(
			self.rect.animate.become(rect_target),
			self.area_tex.animate.next_to(rect_target, UP, MED_LARGE_BUFF),
			self.width_brace.animate.become(width_brace_target),
			self.height_brace.animate.become(height_brace_target),
		)

		h_num = 5
		v_num = 5
		big_width = int(width * h_num)
		big_height = int(height * v_num)
		big_rect = VGroup(*[self.rect.copy() for _ in range(h_num * v_num)]).arrange_in_grid(v_num, buff = 0).scale_to_fit_height(STAGE_HEIGHT * 0.6).to_stage_edge(RIGHT)
		self.play(LaggedStart(*[ReplacementTransform(self.rect.copy().set_opacity(0.1), rect, rate_func = rate_functions.ease_in_out_quad) for rect in big_rect], lag_ratio = 0.1, run_time = 3))

		big_width_brace = BraceLabel(big_rect, str(big_width), DOWN, Text)
		big_height_brace = BraceLabel(big_rect, str(big_height), LEFT, Text)
		self.play(big_width_brace.creation_anim(), big_height_brace.creation_anim())

		big_area_tex = SingleStringMathTex(r"S_{{\text{{大长方形}}}}={0} \times {1}".format(big_width, big_height)).match_height(self.area_tex).next_to(big_rect, UP, MED_LARGE_BUFF)
		big_area_tex[0].set_color(BLUE)
		big_area_tex[1:5].set_color(YELLOW)
		self.play(FadeIn(big_area_tex))

		head_tex = self.area_tex[0:5].copy()
		mid_tex = SingleStringMathTex(r"\frac{21 \times 16}{5 \times 5}").next_to(head_tex, RIGHT)
		top_group = VGroup(head_tex, mid_tex).match_x(self.rect).match_y(big_area_tex)
		left_arrow = SingleStringMathTex(r"\Leftarrow").move_to(center_of_mass((top_group.get_center(), big_area_tex.get_center())))
		self.play(FadeIn(left_arrow, shift = LEFT))
		self.play(FadeIn(top_group, shift = LEFT))

		tail_tex = SingleStringMathTex(r"= 4.2 \times 3.2").next_to(mid_tex, RIGHT)
		top_target = top_group.copy().add(tail_tex).match_x(self.rect)
		focus_rect = SurroundingRectangle(tail_tex[1:])
		self.play(top_group.animate.align_to(top_target, LEFT), FadeIn(tail_tex, scale = 0.5), Create(focus_rect))
		self.play(focus_rect.animate.become(SurroundingRectangle(self.area_tex[-3:])))

		top_group.add(tail_tex)
		self.play(FadeOut(big_rect, big_width_brace, big_height_brace, big_area_tex, focus_rect, left_arrow))

		area = Rectangle(width = STAGE_WIDTH / 4, height = STAGE_WIDTH / 4 * 0.618, stroke_width = 0).set_fill(BLUE, 1).move_to(big_rect).align_to(big_rect, LEFT)
		length = Line(color = YELLOW).stretch_to_fit_width(area.width).align_to(area, UP).match_x(area)
		length_brace = BraceLabel(length, "长度？", UP, Text)
		length_target = length.copy().align_to(area, DOWN).set_color(BLUE)
		area_text = Text("面积？").match_height(length_brace.label).move_to(area)
		area_line = area.copy().stretch_to_fit_height(length.height).move_to(length)
		self.play(Create(length), length_brace.creation_anim())
		self.play(
			length.animate.become(length_target),
			ReplacementTransform(area_line, area),
		)
		self.play(FadeIn(area_text, scale = area.width / area_text.width))
		self.play(FadeOut(area, length, length_brace, area_text), FadeOut(top_group, shift = UP))
		self.remove(tail_tex)

	def real_prove(self):
		step_tex = MathTex(r"""
				\begin{array}{c}
					\text{长,宽} \in \mathbb{N}^+ \\
					\Downarrow \\
					\text{长,宽} \in \mathbb{Q}^+ \\
					\Downarrow \\
					\text{长,宽} \in \mathbb{R}^+ \\
				\end{array}"""
		).move_to(RIGHT * STAGE_WIDTH / 5)[0]
		self.play(FadeIn(step_tex[0:6]))
		self.play(FadeIn(step_tex[6:13], shift = DOWN / 2))
		self.play(FadeIn(step_tex[13:], shift = DOWN / 2))

		rect_tex = SingleStringMathTex(r"a, b \in \mathbb{R}^+").next_to(self.rect, UP, MED_LARGE_BUFF)
		self.play(
			self.width_brace.animate.change_label("a"),
			self.height_brace.animate.change_label("b"),
		)
		self.play(FadeOut(self.area_tex, shift = UP), FadeIn(rect_tex, shift = UP / 2))

		rect_target = self.rect.copy().scale_to_fit_height(STAGE_HEIGHT * 0.4)#.align_to(self.rect, LEFT)
		width_brace_target = BraceLabel(rect_target, "a", DOWN, Text)
		height_brace_target = BraceLabel(rect_target, "b", LEFT, Text)
		VGroup(rect_target, width_brace_target, height_brace_target).to_stage_edge(LEFT)

		self.play(
			self.rect.animate.replace(rect_target), 
			self.width_brace.animate.become(width_brace_target),
			self.height_brace.animate.become(height_brace_target),
			rect_tex.animate.next_to(rect_target, UP, 0.6).align_to(rect_target, RIGHT),
			FadeOut(step_tex, target_position = STAGE_RIGHT),
		)

		width = 4
		height = 3
		k = 2
		m = width * k - 1
		n = height * k - 1
		side = self.rect.width / (m + 1)

		m_group = VGroup(*[DashedLine(self.rect.get_bottom(), self.rect.get_top(), dash_length = 0.1, dashed_ratio = 0.5, stroke_width = 3, color = PINK) for _ in range(m + 2)])
		n_group = VGroup(*[DashedLine(self.rect.get_left(), self.rect.get_right(), dash_length = 0.1, dashed_ratio = 0.5, stroke_width = 3, color = PINK) for _ in range(n + 2)])
		m_group.arrange(RIGHT, side).move_to(self.rect)
		n_group.arrange(UP, side).move_to(self.rect)
		dash_group = VGroup(m_group, n_group)
		self.play(Create(m_group, lag_ratio = 0.1), Create(n_group, lag_ratio = 0.1), run_time = 2)

		square = Square(side, color = PINK).align_to(self.rect, UR)
		square_brace = BraceLabel(square, r"\frac{1}{k}\ ,\ k \in \mathbb{N}^+", RIGHT)
		self.play(square_brace.creation_anim())

		focus_rect = SurroundingRectangle(rect_tex)
		self.play(Create(focus_rect))

		factor = (m + 0.5) / m
		about_point = self.rect.get_corner(DL)
		square_target = square.copy().scale_about(factor, about_point)
		brace_target = square_brace.copy().shift_brace(square_target)
		self.play(
			ScaleAbout(dash_group, factor, about_point),
			square_brace.brace.animate.become(brace_target.brace),
			square_brace.label.animate.become(brace_target.label),
		)

		square = square_target
		square_group = VGroup(square, square_brace)
		square_target = square_group.copy().to_stage_corner(UR)
		self.play(Create(square), FadeOut(focus_rect))
		self.play(
			rect_tex.animate.next_to(square_target, LEFT, MED_LARGE_BUFF),
			square_group.animate.move_to(square_target),
		)

		m_line = Line(*m_group[m].get_start_and_end(), color = YELLOW)
		m_label = Text("第m个").next_to(m_group[m], UP, 0.8)
		m_arrow = Arrow(m_label.get_bottom(), m_group[m], buff = SMALL_BUFF)
		self.play(Create(m_line))
		self.play(FadeIn(m_label), GrowArrow(m_arrow))

		n_line = Line(*n_group[n].get_start_and_end(), color = YELLOW)
		n_label = Text("第n个").next_to(n_group[n], RIGHT, 0.8)
		n_arrow = Arrow(n_label.get_left(), n_group[n], buff = SMALL_BUFF)
		self.play(Create(n_line))
		self.play(FadeIn(n_label), GrowArrow(n_arrow))

		side *= factor
		inner_rect = Rectangle(ORANGE, n * side, m * side, stroke_width = 6).align_to(self.rect, DL)
		focus_rect = SurroundingRectangle(Group(m_line, n_line), buff = MED_SMALL_BUFF, corner_radius = 0.2)
		prepare_for_nonlinear_transform(focus_rect)
		self.play(Create(focus_rect))
		self.play(ReplacementTransform(focus_rect, inner_rect), FadeOut(m_line, n_line))

		inner_m_brace = BraceLabel(inner_rect, r"\frac{m}{k}", UP).shift(DOWN * inner_rect.height)
		inner_n_brace = BraceLabel(inner_rect, r"\frac{n}{k}", RIGHT).shift(LEFT * inner_rect.width)
		self.play(FadeOut(m_group[1:-2], n_group[1:-2]))
		self.play(inner_m_brace.creation_anim())
		self.play(inner_n_brace.creation_anim())

		top_group = VGroup(rect_tex, square_group)
		inequation = MathTex(r"""
						\begin{array}{rcl}
							\frac{m}{k}<&a&<\frac{m+1}{k}\\
							\frac{n}{k}<&b&<\frac{n+1}{k}\\
							\frac{mn}{k^2}<&ab&<\frac{(m+1)(n+1)}{k^2}\\
							\frac{mn}{k^2}<&S_{\text{长方形}}&<\frac{(m+1)(n+1)}{k^2}
						\end{array}
					""")[0].next_to(top_group, DOWN, MED_LARGE_BUFF).to_stage_edge(RIGHT)
		line1 = inequation[0:11]
		line2 = inequation[11:22]
		line3 = inequation[22:44]
		line4 = inequation[44:]
		self.play(FadeOut(m_label, m_arrow, n_label, n_arrow, scale = 0.5))
		self.play(
			ReplacementTransform(inner_m_brace.label[0].copy(), line1[0:3]),
			ReplacementTransform(self.width_brace.label[0].copy(), line1[4]),
			FadeIn(line1[3]),
		)
		self.play(FadeIn(line2[0:5], shift = DOWN / 2))

		outter_rect = Rectangle(GREEN, (n + 1) * side, (m + 1) * side, stroke_width = 6).align_to(self.rect, DL)
		self.play(Create(outter_rect))

		outter_m_brace = BraceLabel(outter_rect, r"\frac{m+1}{k}", UP)
		outter_n_brace = BraceLabel(outter_rect, r"\frac{n+1}{k}", RIGHT)
		self.play(outter_m_brace.creation_anim())
		self.play(outter_n_brace.creation_anim())
		self.play(FadeIn(line1[5:], line2[5:], shift = RIGHT / 2))

		focus_rect = SurroundingRectangle(Group(line1, line2))
		self.play(Create(focus_rect))
		self.play(
			FadeIn(line3, shift = DOWN / 2),
			focus_rect.animate.become(SurroundingRectangle(line3)),
		)

		mn_tex = SingleStringMathTex(r"m,n \in \mathbb{N}^+").match_y(square).to_stage_edge(RIGHT)
		mn_line = Underline(mn_tex, color = YELLOW).rotate(PI, Z_AXIS)
		self.play(
			top_group.animate.next_to(mn_tex, LEFT, MED_LARGE_BUFF),
			FadeIn(mn_tex, shift = LEFT),
			Create(mn_line),
		)
		self.remove(mn_tex)
		top_group.add(mn_tex)

		line4[6].set_color(BLUE)
		line4[7:10].set_color(YELLOW)
		self.play(
			FadeIn(line4, shift = DOWN / 2),
			Uncreate(mn_line),
			focus_rect.animate.become(SurroundingRectangle(Group(line3, line4))),
		)

		section_tex = SingleStringMathTex(r"ab,\ S_{\text{长方形}} \in (\frac{mn}{k^2},\ \frac{(m+1)(n+1)}{k^2})").next_to(line4, DOWN, MED_LARGE_BUFF).to_stage_edge(RIGHT)
		section_tex[3].set_color(BLUE)
		section_tex[4:7].set_color(YELLOW)
		self.play(
			FadeIn(section_tex, shift = DOWN / 2),
			focus_rect.animate.become(SurroundingRectangle(section_tex)),
		)

		self.rect.add(self.width_brace, self.height_brace)
		inner_rect.add(inner_m_brace, inner_n_brace)
		outter_rect.add(outter_m_brace, outter_n_brace)
		rect_group = VGroup(self.rect, m_group[-2:], n_group[-2:], inner_rect, outter_rect)
		factor = (top_group.get_left() - rect_group.get_left())[0] / rect_group.width
		self.remove(m_group[0], n_group[0])
		self.play(
			ScaleAbout(rect_group, factor, rect_group.get_left()),
			FadeOut(inequation, shift = UP),
			Group(section_tex, focus_rect).animate.next_to(top_group, DOWN, MED_SMALL_BUFF).align_to(section_tex, RIGHT)
		)

		minus_tex = SingleStringMathTex(r"""
						\lvert S_{\text{长方形}}-ab\rvert &< \frac{(m+1)(n+1)}{k^2}-\frac{mn}{k^2}\\
						&=\frac{m+n+1}{k^2}\\
						&=(\frac{m}{k}+\frac{n}{k}+\frac{1}{k})\cdot \frac{1}{k}\\
						&<\frac{a+b+1}{k}\\
					""").next_to(section_tex, DOWN, MED_SMALL_BUFF)
		line1 = minus_tex[0:29]
		line2 = minus_tex[29:38]
		line3 = minus_tex[38:56]
		line4 = minus_tex[56:]
		line1[1].set_color(BLUE)
		line1[2:5].set_color(YELLOW)
		self.play(FadeIn(line1, shift = DOWN / 2), focus_rect.animate.become(SurroundingRectangle(line1)))
		self.play(focus_rect.animate.become(SurroundingRectangle(line1[10:])))
		self.play(FadeIn(line2, shift = DOWN / 2), focus_rect.animate.become(SurroundingRectangle(line2[1:])))

		line4.match_y(line3)
		line3.match_y(line2)
		self.play(
			FadeOut(line2, shift = UP / 2),
			FadeIn(line3, shift = UP / 2),
			focus_rect.animate.become(SurroundingRectangle(line3[1:])),
		)

		rectm = focus_rect.copy()
		rectn = focus_rect.copy()
		rect1 = focus_rect.copy()
		km = line3[2:5]
		kn = line3[6:9]
		k1 = line3[10:13]

		self.remove(focus_rect)
		self.play(
			rectm.animate.become(SurroundingRectangle(km)),
			rectn.animate.become(SurroundingRectangle(kn)),
			rect1.animate.become(SurroundingRectangle(k1)),
		)

		ta =line4[1] 
		tb =line4[3] 
		t1 =line4[5] 
		tmpa = ta.copy().match_x(km)
		tmpb = tb.copy().match_x(kn)
		tmp1 = t1.copy().match_x(k1)

		self.play(
			ReplacementTransform(km.copy(), tmpa),
			rectm.animate.become(SurroundingRectangle(tmpa)),
		)
		self.play(
			ReplacementTransform(kn.copy(), tmpb),
			rectn.animate.become(SurroundingRectangle(tmpb)),
		)
		self.play(
			ReplacementTransform(k1.copy(), tmp1),
			rect1.animate.become(SurroundingRectangle(tmp1)),
		)
		self.play(FadeOut(rectm, rectn, rect1))
		self.play(
			ReplacementTransform(tmpa, ta),
			ReplacementTransform(tmpb, tb),
			ReplacementTransform(tmp1, t1),
			FadeIn(line4[0], line4[2], line4[4], line4[6:]),
		)

		line2.set_opacity(0)
		self.play(
			FadeOut(section_tex, shift = UP / 2),
			minus_tex.animate.align_to(section_tex, UP),
		)

		focus_rect = SurroundingRectangle(line4[-1])
		lim_tex = SingleStringMathTex(r"\lim_{k \to \infty } \frac{a+b+1}{k}=0").next_to(minus_tex, DOWN).align_to(line4, LEFT)
		self.play(Create(focus_rect))
		self.play(focus_rect.animate.become(SurroundingRectangle(line4[1:])))
		self.play(
			FadeIn(lim_tex, shift = UP / 2),
			focus_rect.animate.become(SurroundingRectangle(lim_tex))
		)

		left_arrow = SingleStringMathTex(r"\Leftarrow").next_to(lim_tex, LEFT, MED_LARGE_BUFF)
		area_tex = SingleStringMathTex(r"S_{\text{长方形}} = ab\cdot").next_to(left_arrow, LEFT, MED_LARGE_BUFF)
		area_tex[0].set_color(BLUE)
		area_tex[1:4].set_color(YELLOW)
		under_line = Underline(area_tex[:-1], color = YELLOW).rotate(PI, Z_AXIS)
		self.play(FadeIn(left_arrow, shift = LEFT / 2))
		self.play(
			FadeIn(area_tex[:-1], shift = LEFT / 2),
			FadeOut(focus_rect),
			Create(under_line),
		)

		unit_squre = Square(color = YELLOW, fill_color = BLUE, fill_opacity = 1).match_height(area_tex).next_to(left_arrow, LEFT, MED_LARGE_BUFF)
		unit_brace = BraceLabel(unit_squre, "1", UP, Text, font_size = 24)
		unit_group = VGroup(unit_squre, unit_brace)
		area_target = area_tex.copy().next_to(unit_squre, LEFT)
		self.play(
			FadeIn(area_tex[-1]),
			area_tex.animate.move_to(area_target),
			under_line.animate.match_width(Group(area_target, unit_group)).align_to(area_target, LEFT),
			FadeIn(unit_group, scale = 0.1),
		)
		self.play(
			area_tex[:-1].animate.align_to(unit_group, RIGHT),
			FadeOut(area_tex[-1], unit_group, scale = 0.1),
			Uncreate(under_line),
		)

		self.play(FadeOut(top_group, shift = UP / 2), FadeOut(minus_tex, target_position = STAGE_RIGHT), FadeOut(area_tex, left_arrow, lim_tex, shift = DOWN / 2))
		self.rect_group = rect_group

	def measure_overview(self):
		condition_tex = SingleStringMathTex(r"a \in \mathbb{R}\quad  k,\ m_{k} \in \mathbb{N}")
		cauchy_tex = SingleStringMathTex(r"\{" + r",\ ".join([r"\frac{{m_{{{0}}}}}{{{0}}}".format(i+1) for i in range(5)])+r",\ \cdots \frac{m_{k}}{k} \}")
		equation = SingleStringMathTex(r"\lim_{k \to \infty}\frac{m_{k}}{k} = a")
		tex_group = VGroup(condition_tex, cauchy_tex, equation).arrange(DOWN, LARGE_BUFF).next_to(self.rect_group, RIGHT, LARGE_BUFF)
		condition_tex.align_to(cauchy_tex, LEFT)
		equation.align_to(cauchy_tex, LEFT)

		self.play(Write(condition_tex))
		self.play(LaggedStart(*[FadeIn(obj, scale = 0.1, shift = RIGHT) for obj in cauchy_tex], lag_ratio = 0.1, run_time = 3))
		self.play(FadeIn(equation, shift = DOWN / 2))

		r_tex = condition_tex[2].copy()
		focus_rect = SurroundingRectangle(r_tex)
		self.play(Create(focus_rect))
		self.play(
			FadeOut(self.rect_group, target_position = STAGE_LEFT),
			FadeOut(tex_group, scale = 0.1), 
			Group(r_tex, focus_rect).animate.scale(2).move_to(UP * STAGE_HEIGHT / 5)
		)

		line = Line(LEFT * 2, RIGHT * 2, color = YELLOW, stroke_width = 6).next_to(focus_rect, DOWN, MED_LARGE_BUFF)
		rect = Rectangle(stroke_width = 0, width = line.width, height = 2.5).set_fill(BLUE, 1).align_to(line, UP).match_x(line).set_z_index(-1)
		rect_line = rect.copy().stretch_to_fit_height(line.height).align_to(line, UP)
		dot = Dot(line.get_start(), color = ORANGE).set_z_index(1)
		self.play(Create(dot))
		self.play(Create(line), dot.animate.move_to(line.get_end()), FadeOut(focus_rect))
		self.play(ReplacementTransform(rect_line, rect), line.animate.shift(DOWN * 2.5))
		self.play(FadeOut(dot, scale = rect.height / dot.height, shift = DL * 1.5), Group(rect, line).animate.match_color(dot))
		
		self.play(rect.animate.stretch_to_fit_height(line.height).move_to(line))
		self.remove(rect)

		line_brace = BraceLabel(line, r"\infty")
		self.play(line_brace.creation_anim())

		n_tex = SingleStringMathTex(r"\mathbb{N}").match_height(r_tex).next_to(line, LEFT).match_y(r_tex)
		q_tex = SingleStringMathTex(r"\mathbb{Q}").match_height(r_tex).next_to(line, RIGHT).match_y(r_tex)
		self.play(FadeIn(n_tex, shift = LEFT))
		self.play(FadeIn(q_tex, shift = RIGHT))

		arrow_group = VGroup()
		for tex in r_tex, n_tex, q_tex:
			arrow_pair = VGroup(
				Arrow(tex.get_bottom(), line.get_top()),
				Arrow(line.get_top(), tex.get_bottom()),
			)
			arrow_group.add(arrow_pair)
		self.play(GrowArrow(arrow_group[0][0]), GrowArrow(arrow_group[0][1]), r_tex.animate.match_color(line))

		double = Text("双 射").move_to(arrow_group[0]).shift(UP * 0.5)
		self.play(FadeIn(double, scale = 0.1))

		n_cross = Text("❌", color = RED).move_to(arrow_group[1]).shift(DL * 0.2)
		q_cross = Text("❌", color = RED).move_to(arrow_group[2]).shift(DR * 0.2)
		self.play(
			GrowArrow(arrow_group[1][0]),
			GrowArrow(arrow_group[1][1]),
			FadeIn(n_cross, scale = 0.1),
			GrowArrow(arrow_group[2][0]),
			GrowArrow(arrow_group[2][1]),
			FadeIn(q_cross, scale = 0.1),
		)
		arrow_group.add(double, n_cross, q_cross)

		title = Text("可数：集合中的全部元素可以依次列出来").to_stage_edge(UP)
		under_line = Underline(title, color = YELLOW)
		self.play(FadeIn(title, shift = DOWN / 2), Create(under_line))

		n_list_tex = SingleStringMathTex(r"0,\ 1,\ 2,\ 3,\ 4,\ 5\cdots").move_to((n_tex.get_right() + STAGE_LEFT) / 2).match_y(arrow_group)
		q_list_tex = SingleStringMathTex(r"0,\ \frac{1}{2},\ \frac{1}{3},\ \frac{2}{3},\ \frac{1}{4},\ \frac{3}{4}\cdots").move_to((q_tex.get_left() + STAGE_RIGHT) / 2).match_y(arrow_group)
		
		self.play(
			LaggedStart(*[FadeIn(c, target_position = n_tex, scale = 0.1) for c in n_list_tex], lag_ratio = 0.1),
			LaggedStart(*[FadeIn(c, target_position = q_tex, scale = 0.1) for c in q_list_tex], lag_ratio = 0.1),
			run_time = 3,
		)

		self.play(
			FadeOut(n_list_tex, target_position = STAGE_LEFT),
			FadeOut(q_list_tex, target_position = STAGE_RIGHT),
		)

		tex_group = VGroup(r_tex, n_tex, q_tex)
		set_group = VGroup(tex_group, arrow_group, line, line_brace)
		self.play(set_group.animate.shift(LEFT * STAGE_WIDTH / 4))

		m_tex = SingleStringMathTex(r"""
					\begin{array}{ll}
						m(\text{集合})&=\text{集合的大小}\\
						m(\mathbb{N})&=0\\
						m(\mathbb{Q})&=0 \\
						m(\mathbb{R})&=\infty \\
						m([0,1])&= 1\\
					\end{array}
				""").move_to(RIGHT * STAGE_WIDTH / 4)
		first_line = m_tex[0:11]
		first_underline = Underline(first_line, color = BLUE)
		for i in (0, 11, 17, 23, 29):
			m_tex[i].set_color(BLUE) 

		self.play(Write(first_line), Create(first_underline))
		self.play(Write(m_tex[11:]))

		m_title = Text("测度论(Measure)：度量集合大小的方法").move_to(title)
		m_title[4].set_color(BLUE).set_opacity(0)
		m_copy = m_tex[0].copy()
		self.play(
			FadeOut(title, shift = UP / 2),
			FadeIn(m_title, shift = UP / 2),
			under_line.animate.become(Underline(m_title, color = YELLOW)),
			m_copy.animate.move_to(m_title[4]),
		)
		self.play(m_copy.animate.become(m_title[4].copy().set_opacity(1)))
		m_title[4].set_opacity(1)
		self.remove(m_copy)

		self.play(FadeOut(set_group, target_position = STAGE_LEFT), FadeOut(m_tex, first_underline, target_position = STAGE_RIGHT))
		self.play(FadeOut(m_title, under_line, shift = UP))

	def integration(self):
		axes = Axes(
			x_range = [-0.5, 2.5],
			y_range = [-0.5, 1.5],
			x_length = 6,
			y_length = 4,
			# axis_config = {"include_numbers" : True},
		).next_to(ORIGIN, LEFT, LARGE_BUFF)
		labels = axes.get_axis_labels()
		labels[0].align_to(axes, RIGHT)
		labels[1].align_to(axes, UP)
		self.play(Create(axes), FadeIn(labels))

		func = lambda x: np.sin(5*x)*np.log10(x+1) + 0.7
		curve = axes.plot(func, [0, 2], color = YELLOW)
		curve_label = axes.get_graph_label(curve, "y=f(x)", x_val = 1.5, direction = UP)
		self.play(Create(curve), Write(curve_label))

		a = 0.3
		b = 1.8
		dot_a = Dot(axes.i2gp(a, curve), color = LIGHT_PINK)
		curve_area = axes.get_area(curve, [a, a], BLUE, 0.8).set_z_index(-1)
		a_label = Text("a").next_to(curve_area, DOWN).match_color(dot_a)
		self.play(Create(curve_area), Create(dot_a), FadeIn(a_label))

		dot_b = dot_a.copy()
		traced_path = TracedPath(dot_b.get_center, stroke_width = 6, stroke_color = ORANGE)
		x_tracker = ValueTracker(a)
		dot_b.add_updater(lambda m: m.move_to(axes.i2gp(x_tracker.get_value(), curve)))
		curve_area.add_updater(lambda m: m.become(axes.get_area(curve, [a, x_tracker.get_value()], BLUE, 0.8).set_z_index(-1)))
		b_label = Text("b").move_to(axes.i2gp(b, curve)).match_y(a_label).match_color(dot_b)

		self.add(curve_area, traced_path, dot_b)
		self.play(
			x_tracker.animate.set_value(b),
			FadeIn(b_label, target_position = a_label),
			run_time = 2,
		)
		dot_b.suspend_updating()
		curve_area.suspend_updating()
		traced_path.suspend_updating()

		length_tex = SingleStringMathTex(r"\text{长度}_{[a,b]} = \int_{a}^{b}\sqrt{1+(f'(x))^2}dx").next_to(ORIGIN, RIGHT).align_to(axes, UP)
		area_tex = SingleStringMathTex(r"\text{面积}_{[a,b]} = \int_{a}^{b}f(x)dx").next_to(ORIGIN, RIGHT).align_to(a_label, DOWN)
		length_tex[0:2].match_color(traced_path)
		area_tex[0:2].match_color(curve_area)
		length_tex[16:21].match_color(curve)
		area_tex[11:15].match_color(curve)
		for i in (3,5,9,10): 
			length_tex[i].match_color(a_label)
			area_tex[i].match_color(a_label)

		self.play(ReplacementTransform(traced_path.copy(), length_tex[0:2]))
		self.play(Write(length_tex[2:]))
		self.play(ReplacementTransform(DashedVMobject(curve_area, 50, 1), area_tex[0:2]))
		self.play(Write(area_tex[2:]))
		