import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))

from units import *
from basel_circle import *

class basel_problem(MultiZoomedScene):
	def setup(self):
		self.align_camera_with_stage()

	def construct(self):
		self.next_section(skip_animations = False)
		self.overview()
		self.next_section(skip_animations = False)
		self.euler_slove()
		self.next_section(skip_animations = False)
		self.new_slove()
		self.next_section(skip_animations = False)
		self.triangle_in_circle()
		self.next_section(skip_animations = False)
		self.big_circle()
		self.next_section(skip_animations = False)
		self.more_circles()
		self.wait()

	def overview(self):
		basel_tex_str = "".join([r"\frac{{1}}{{{0}^2}}+".format(i) for i in range(1, 10)]) + r"\cdots = \ ?"
		self.basel_tex = SingleStringMathTex(basel_tex_str)
		self.play(Write(self.basel_tex))

		shift_lenght = STAGE_WIDTH / 5
		self.mengoli = ImageMobject(os.path.join("assert", "portrait", "Pietro_Mengoli")).scale_to_fit_height(STAGE_HEIGHT * 0.4)
		self.euler = ImageMobject(os.path.join("assert", "portrait", "Leonhard_Euler")).match_height(self.mengoli).shift(LEFT *  shift_lenght)
		year_1650 = Text("1650年").scale_to_fit_height(0.5).next_to(self.mengoli, DOWN)
		year_1735 = Text("1735年").scale_to_fit_height(0.5).next_to(self.euler, DOWN)
		self.play(
			self.basel_tex.animate.to_stage_edge(UP),
			FadeIn(self.mengoli),
		)
		self.play(FadeIn(year_1650, target_position = self.mengoli.get_bottom()))

		self.mengoli.add(year_1650)
		self.play(
			self.mengoli.animate.shift(RIGHT * shift_lenght),
			FadeIn(year_1735, target_position = year_1650),
		)
		self.play(FadeIn(self.euler))
		self.euler.add(year_1735)
		self.add(self.mengoli, self.euler)

	def euler_slove(self):
		euler_target = self.euler.copy().to_stage_edge(LEFT)
		root_expand_first = SingleStringMathTex(r"\frac{\sin x}{x} = (1+\frac{x}{\pi})(1-\frac{x}{\pi})(1+\frac{x}{2\pi})(1-\frac{x}{2\pi})(1+\frac{x}{3\pi})(1-\frac{x}{3\pi})\cdots").scale_to_fit_width(STAGE_WIDTH * 0.6).next_to(euler_target, buff = LARGE_BUFF)
		sine_tex = root_expand_first[0:6]
		self.play(
			FadeOut(self.mengoli),
			self.euler.animate.replace(euler_target),
			FadeIn(sine_tex, target_position = self.euler.get_right()),
		)

		root_expand_second = MathTex(r"={{(1-\frac{x^2}{\pi^2})}}{{(1-\frac{x^2}{4\pi^2})}}{{(1-\frac{x^2}{9\pi^2})}}\cdots").match_height(sine_tex).next_to(root_expand_first, DOWN).align_to(root_expand_first[6], LEFT)
		self.play(FadeIn(root_expand_first[6:]))
		self.play(FadeIn(root_expand_second, shift = DOWN))

		root_group = Group(root_expand_first, root_expand_second)
		root_target = root_group.copy().align_to(self.euler, UP)
		taylor_expand = SingleStringMathTex(r"\frac{\sin x}{x}=1" + "".join([r"{0}\frac{{ x^{{ {1} }} }}{{ {2}! }}".format('+' if i%2==0 else '-', i*2, i*2+1) for i in range(1,10)]) + "\cdots").match_width(root_group).next_to(root_target, DOWN, MED_LARGE_BUFF).align_to(root_target, LEFT)
		self.play(
			root_group.animate.replace(root_target), 
			FadeIn(taylor_expand, shift = DOWN),
		)

		font_size = 48
		equation_str = r"""
			{{-\frac{x^2}{\pi^2}}}{{-\frac{x^2}{4\pi^2}}}{{-\frac{x^2}{9\pi^2}}}\cdots&{{=}}{{-\frac{x^{2} }{3!}}}\\
			{{-\frac{1}{\pi^2}-\frac{1}{4\pi^2}-\frac{1}{9\pi^2}\cdots&=-\frac{1}{3!}}}\\
			{{\frac{1}{1}+\frac{1}{4}+\frac{1}{9}\cdots&=\frac{\pi^2}{3!}}}\\
			{{\frac{1}{1^2}+\frac{1}{2^2}+\frac{1}{3^2}\cdots&=\frac{\pi^2}{6}}}
		"""
		equation = MathTex(equation_str, font_size = font_size).align_to(root_group, UP)
		equation.save_state()
		equal = equation.get_part_by_tex("=").next_to(taylor_expand, DOWN, LARGE_BUFF)
		root_terms = equation[0:7].next_to(equal, LEFT, MED_LARGE_BUFF)
		taylor_terms = equation[8].next_to(equal, RIGHT, MED_LARGE_BUFF)
		root_sub = Group(root_expand_second[1][2:8], root_expand_second[2][2:9], root_expand_second[3][2:9], root_expand_second[4])
		taylor_sub = taylor_expand[8:14]
		self.play(*[Circumscribe(tex[1:3]) for tex in root_sub[0:3]], Circumscribe(taylor_sub[1:3]))
		self.play(root_sub.animate.set_color(YELLOW), taylor_sub.animate.set_color(YELLOW))

		root_terms.match_color(root_sub)
		taylor_terms.match_color(taylor_sub)

		root_sub_copy = root_sub.copy()
		taylor_sub_copy = taylor_sub.copy()
		self.play(
			*[root_sub_copy[i].animate.become(root_terms[i * 2 + 1]) for i in range(3)],
			root_sub_copy[3].animate.become(root_terms[6]),
		)
		self.play(taylor_sub_copy.animate.become(taylor_terms))
		self.play(FadeIn(equal))

		expands = Group(root_sub_copy, equal, taylor_sub_copy)
		self.play(
			expands.animate.center().align_to(root_group, UP).set_color(WHITE),
			FadeOut(Group(root_group, taylor_expand), target_position = root_group.get_top()),
		)
		self.play(FadeIn(equation[10], shift = DOWN))
		self.play(FadeIn(equation[12], shift = DOWN))
		self.play(FadeIn(equation[14], shift = DOWN))

		result = equation[14][-4:].copy()
		self.play(Circumscribe(result))

		result.next_to(self.basel_tex).align_to(self.basel_tex[-1], LEFT)
		self.play(self.basel_tex[-1].animate.become(result))

		equation.restore()
		self.remove(root_sub_copy, taylor_sub_copy)
		self.play(FadeOut(self.euler, equation, shift = LEFT * STAGE_WIDTH / 3))

	def new_slove(self):
		# basel_tex_str = "".join([r"\frac{{1}}{{{0}^2}}+".format(i) for i in range(1, 10)]) + r"\cdots = \ ?"
		# self.basel_tex = SingleStringMathTex(basel_tex_str).to_stage_edge(UP)
		# self.add(self.basel_tex)

		bc = basel_circle(8).scale_to_fit_height(STAGE_HEIGHT * 0.7).next_to(self.basel_tex, DOWN)
		self.play(*[Create(circle) for circle in bc.circles], lag_ratio = 0.1)
		self.play(LaggedStart(*[LaggedStart(*[Create(t) for t in triangles], lag_ratio = 1 / len(triangles)) for triangles in bc.triangles], lag_ratio = 0.2))
		self.play(bc.animate.scale(128).align_to(bc.get_bottom(), DOWN).set_opacity(0), run_time = 3, rate_func = rate_functions.ease_in_out_cubic)

		rect = SurroundingRectangle(self.basel_tex[-1][0:2])
		self.play(Create(rect))

		self.circle = Circle(STAGE_HEIGHT * 0.35, BLUE).next_to(self.basel_tex, DOWN, MED_LARGE_BUFF)
		self.play(ReplacementTransform(rect, self.circle))

		underline = Underline(self.basel_tex[0:-5], color = YELLOW)
		self.play(Create(underline))
		self.play(self.circle.animate.align_to(self.basel_tex, LEFT))

		pa, pb, pc = [1, 0, 0], [-1, 0, 0], [-0.5, np.sqrt(3) / 2, 0]
		triangle = right_triangle(pa, pb, pc).scale_to_fit_height(STAGE_HEIGHT / 4).align_to(self.basel_tex, RIGHT).align_to(self.circle.get_center(), DOWN)
		triangle.suspend_updating()
		self.play(FadeIn(triangle.lines.set_color(BLUE), shift = DOWN), Uncreate(underline))

		self.play(Create(triangle.t_angle))

		a = Tex("a").move_to(triangle.line_a).shift(UL * MED_SMALL_BUFF)
		b = Tex("b").move_to(triangle.line_b).shift(UR * MED_SMALL_BUFF)
		c = Tex("c").next_to(triangle.line_c, DOWN)
		self.play(
			FadeIn(a, target_position = triangle.line_a),
			FadeIn(b, target_position = triangle.line_b),
			FadeIn(c, target_position = triangle.line_c),
		)

		h = Tex("h").next_to(triangle.line_h)
		self.play(LaggedStart(Create(triangle.line_h), Create(triangle.h_angle), FadeIn(h, target_position = triangle.line_h), lag_ratio = 0.1))

		trangle_tex = SingleStringMathTex(r"\frac{1}{h^2}=\frac{1}{a^2}+\frac{1}{b^2}").next_to(c, DOWN, MED_LARGE_BUFF)
		self.play(FadeIn(trangle_tex, shift = DOWN))

		self.triangle_group = Group(triangle, a, b ,c, h, trangle_tex)

		proof_tex_str = r"""
			{{ S_{\triangle} = \frac{1}{2}  c\times h&=\frac{1}{2} a\times b\\ }}
			{{ &\Downarrow \\}}
			{{ c^2\times h^2 &= a^2\times b^2\\}}
			{{ &\Downarrow \\}}
			{{ \frac{1}{h^2} =\frac{c^2}{a^2\times b^2}&=\frac{a^2+b^2}{a^2\times b^2}=\frac{1}{a^2}+\frac{1}{b^2}}}
		"""
		proof_tex = MathTex(proof_tex_str).scale_to_fit_height(STAGE_HEIGHT * 0.5).align_to(self.circle, LEFT).align_to(self.triangle_group, DOWN)

		self.play(
			FadeOut(self.circle, target_position = self.circle.get_left()),
			FadeIn(proof_tex[1], target_position = triangle),
		)
		
		self.play(FadeIn(proof_tex[3:6], shift = DOWN))
		self.play(FadeIn(proof_tex[7:], shift = DOWN))

		right_arrow = SingleStringMathTex(r"\Rightarrow").move_to(midpoint(proof_tex[-2].get_right(), trangle_tex.get_left()))
		self.play(FadeIn(right_arrow, shift = RIGHT))

		circle_left = self.circle.get_left()
		self.circle.set_y(0)
		self.play(
			FadeIn(self.circle, target_position = circle_left),
			FadeOut(proof_tex, right_arrow),
			FadeOut(self.basel_tex, shift = UP),
			self.triangle_group.animate.match_y(self.circle),
		)

	def triangle_in_circle(self):
		angle_tracker = ValueTracker(PI / 6)
		self.circle.set_z(0)
		triangle = right_triangle(self.circle.get_right, self.circle.get_left, lambda : pos_on_circle(self.circle, angle_tracker.get_value()), 0.3, False)
		self.play(Create(triangle.line_c))

		self.circle.dot = Dot(color = ORANGE).set_z_index(1)
		self.circle.dot.add_updater(lambda m: m.move_to(pos_on_circle(self.circle, angle_tracker.get_value())))
		self.circle.dot.update()
		self.play(Create(self.circle.dot))
		self.play(LaggedStart(Create(triangle.line_a), Create(triangle.line_b), Create(triangle.t_angle), lag_ratio = 0.1))
		self.add(triangle)

		self.play(angle_tracker.animate.set_value(PI / 6 * 11), run_time = 3)
		self.wait()
		self.play(angle_tracker.animate.set_value(PI / 2 * 3))
		triangle.suspend_updating()
		self.circle.dot.clear_updaters()

		triangle.add_h()
		self.play(LaggedStart(Create(triangle.line_h), Create(triangle.h_angle), lag_ratio = 0.3))

		self.circle.r = Tex("r").next_to(triangle.line_h)
		self.play(Indicate(triangle.line_h, 1))
		self.play(FadeIn(self.circle.r, target_position = triangle.line_h))
		self.add(triangle)

		self.circle.a = Tex("L").move_to(triangle.line_a).shift(DL * MED_SMALL_BUFF)
		self.circle.b = Tex("L").move_to(triangle.line_b).shift(DR * MED_SMALL_BUFF)
		self.play(Indicate(triangle.line_a, 1), Indicate(triangle.line_b, 1))
		self.play(FadeIn(self.circle.a, target_position = triangle.line_a), FadeIn(self.circle.b, target_position = triangle.line_b))

		tex_rect = SurroundingRectangle(self.triangle_group[-1])
		self.play(Create(tex_rect))

		triangle_target = self.triangle_group.copy().align_to(self.circle, UP)
		triangle_tex = SingleStringMathTex(r"\frac{1}{r^2}=\frac{2}{L^2}").next_to(triangle_target, DOWN, MED_LARGE_BUFF)
		self.play(
			self.triangle_group.animate.move_to(triangle_target),
			tex_rect.animate.become(SurroundingRectangle(triangle_tex)),
			FadeIn(triangle_tex, shift = DOWN),
		)
		self.play(FadeOut(tex_rect))

		self.circle.lb_color = triangle.line_b.copy().set_color(YELLOW)
		self.circle.arc_dr = Arc(self.circle.radius, PI / 2 * 3, PI / 2, arc_center = self.circle.get_center(), color = YELLOW)
		brace_dr = ArcBrace(self.circle.arc_dr)
		self.circle.label_dr = Tex("1").move_to(BraceLabel(brace_dr, "", DR))
		self.play(LaggedStart(Create(self.circle.lb_color), Create(self.circle.arc_dr), lag_ratio = 0.5))
		self.play(FadeIn(brace_dr, target_position = self.circle.arc_dr), FadeIn(self.circle.label_dr, shift = DR * MED_SMALL_BUFF))

		brace_ul = brace_dr.copy().rotate(PI, about_point = self.circle.get_center())
		brace_ur = brace_dr.copy().rotate(PI / 2, about_point = self.circle.get_center())
		brace_dl = brace_dr.copy().rotate(-PI / 2, about_point = self.circle.get_center())
		label_ul = self.circle.label_dr.copy().move_to(self.circle.get_center() * 2 - self.circle.label_dr.get_center())
		label_ur = label_ul.copy().match_x(self.circle.label_dr)
		label_dl = label_ul.copy().match_y(self.circle.label_dr)
		self.play(FadeIn(brace_ul, brace_ur, brace_dl, label_ul, label_ur, label_dl))

		r_tex = SingleStringMathTex(r"r = \frac{2}{\pi}").next_to(triangle.line_c, UP)
		right_arrow = SingleStringMathTex(r"\Rightarrow").move_to(r_tex)
		c_tex = SingleStringMathTex(r"C=4").move_to(r_tex)
		r_tex.next_to(right_arrow)
		self.play(FadeIn(c_tex, target_position = triangle.line_c))
		self.play(c_tex.animate.next_to(right_arrow, LEFT), FadeIn(right_arrow, r_tex, shift = RIGHT))

		tex_group = Group(triangle_tex, r_tex.copy())
		tex_target = tex_group.copy().arrange(RIGHT, MED_LARGE_BUFF).move_to(triangle_tex)
		self.play(tex_group[0].animate.move_to(tex_target[0]), tex_group[1].animate.move_to(tex_target[1]))

		down_arrow = SingleStringMathTex(r"\Downarrow").match_x(tex_group).match_y(self.circle)
		pi_tex = SingleStringMathTex(r"\frac{\pi^2}{8}=\frac{1}{L^2}").next_to(down_arrow, DOWN)
		self.play(
			FadeOut(self.triangle_group, target_position = self.triangle_group.get_top()),
			tex_group.animate.next_to(down_arrow, UP),
		)
		self.play(FadeIn(down_arrow, pi_tex, shift = DOWN))

		self.play(
			FadeOut(brace_dl, brace_dr, brace_ul, brace_ur, label_dl, label_ul, label_ur, c_tex, right_arrow, r_tex),
			self.circle.label_dr.animate.shift(UL * MED_SMALL_BUFF),
		)

		self.circle.lb_color.set_z_index(1)
		self.circle.arc_dr.set_z_index(1)
		self.circle.add(self.circle.lb_color, self.circle.arc_dr)
		self.circle_attach = Group(self.circle.r, self.circle.b, self.circle.label_dr, self.circle.dot)
		self.triangle = triangle
		self.tex_group = Group(tex_group, down_arrow, pi_tex)

	def big_circle(self):
		pi_tex = self.tex_group[-1]
		t0_tex = pi_tex[-4:]
		self.play(FocusOn(t0_tex))
		self.play(t0_tex.animate.set_color(YELLOW))

		bc = basel_circle(1, self.circle.height / 2, 0.3, self.circle.get_color()).match_x(self.circle).align_to(self.circle, DOWN)
		self.play(
			self.triangle.line_c.animate.become(bc.triangles[0][0].line_b),
			Uncreate(self.triangle.line_a),
			Uncreate(self.triangle.t_angle),
			FadeOut(self.circle.a),
		)

		c0 = bc.circles[0].add(self.circle.arc_dr)
		t0 = c0.triangles[0]
		t0.line_c.add(self.circle.lb_color)
		self.remove(self.circle, self.circle.a, *self.triangle.submobjects)
		self.add(c0, t0)
		self.circle_attach.set_z_index(1)

		ld = DashedLine(c0.get_right(), c0.get_top(), color = PINK).scale(1.3)
		h_angle = RightAngle(t0.line_c, ld, 0.3, quadrant = (-1, 1))
		h_angle.add_updater(lambda m: m.become(RightAngle(t0.line_c, ld, 0.3, quadrant = (-1, 1))))
		self.play(Create(ld), Create(h_angle))

		down_dot = self.circle_attach[-1].set_z_index(2)
		top_dot = Dot(c0.get_top()).match_color(down_dot).set_z_index(2)
		top_dot.add_updater(lambda m: m.move_to(c0.get_top()))
		down_dot.add_updater(lambda m: m.move_to(c0.get_bottom()))
		dia = Line(top_dot, c0.get_center())
		self.play(Create(top_dot))
		self.play(FocusOn(h_angle))
		self.play(Circumscribe(top_dot), Circumscribe(down_dot))
		self.play(Create(dia))

		c0.add(dia)
		self.play(ScaleAbout(Group(c0, t0, ld, self.circle_attach[0:-1]), 0.5, down_dot))

		bc.add_circle()
		c1 = bc.circles[1]
		t1 = c1.triangles[0]
		self.play(Create(c1))
		self.play(ReplacementTransform(ld, t1.line_c))

		a_dot = Dot().match_color(down_dot).add_updater(lambda m: m.move_to(t1.pa)).set_z_index(2)
		b_dot = Dot().match_color(down_dot).add_updater(lambda m: m.move_to(t1.pb)).set_z_index(2)
		self.play(Create(a_dot), Create(b_dot))
		self.play(LaggedStart(Create(t1.line_a), Create(t1.line_b), Create(t1.t_angle), lag_ratio = 0.3))
		self.remove(h_angle)
		self.add(bc)
		self.wait()

		lb = t0.line_c.submobjects[0]
		lbc = lb.copy()
		t0.line_c.remove(lb)
		self.play(
			lb.animate.become(t1.line_a.copy().match_color(lb)),
			lbc.animate.become(t1.line_b.copy().match_color(lb)),
		)
		t1.line_a.add(lb)
		t1.line_b.add(lbc)

		a_direction = np.array([np.tan(PI / 8), -1, 0])
		b_direction = np.array([-1, -np.tan(PI / 8), 0])
		l1 = SingleStringMathTex("L_{1}").next_to(t1.line_a.get_center(), a_direction)
		l2 = SingleStringMathTex("L_{2}").next_to(t1.line_b.get_center(), b_direction)
		self.play(FadeIn(l1, target_position = t1.line_a), FadeIn(l2, target_position = t1.line_b))

		self.play(self.tex_group.animate.align_to(bc, UP))

		equal = pi_tex[4]
		t1_tex = SingleStringMathTex(r"=\frac{1}{L_{1}^2}+\frac{1}{L_{2}^2}").next_to(pi_tex, DOWN).align_to(equal, LEFT)
		t1_tex[1:].set_color(YELLOW)
		self.play(ReplacementTransform(l1.copy(), t1_tex[3:6]), ReplacementTransform(l2.copy(), t1_tex[9:]))
		self.play(
			FadeIn(t1_tex[0:3], t1_tex[6:9]),
			t0_tex.animate.set_color(WHITE),
		)

		angle0 = Angle(dia, t1.line_c, color = RED, quadrant = (1, -1))
		label0 = SingleStringMathTex(r"\theta").scale_to_fit_height(0.3).move_to((angle0.get_center() * 5 - top_dot.get_center() * 2) / 3)
		self.play(ReplacementTransform(t0.line_c.copy(), angle0))
		self.play(FadeIn(label0, target_position = angle0))
		self.play(ReplacementTransform(angle0.copy(), t1.line_a))

		angle1 = Angle(t1.line_b, t1.line_c, radius = 0.8, color = RED, quadrant = (-1, -1))
		label1 = SingleStringMathTex(r"\frac{\theta}{2}").scale_to_fit_height(0.5).move_to((angle1.get_center() * 5 - t1.pa * 2) / 3)
		self.play(ReplacementTransform(t1.line_a.copy(), angle1))
		self.play(FadeIn(label1, target_position = angle1))

		arc_0 = c0.submobjects[0]
		c0.remove(arc_0)
		arc_a = Arc(c1.height / 2, -PI / 2, PI / 4, arc_center = c1.get_center()).match_color(arc_0)
		self.play(ReplacementTransform(arc_0, arc_a))

		brace_a = ArcBrace(arc_a, buff = MED_LARGE_BUFF)
		label_a = Tex("1").move_to(BraceLabel(brace_a, "", a_direction))
		self.play(FadeIn(brace_a, target_position = arc_a), ReplacementTransform(self.circle_attach[2], label_a))

		arc_b = Arc(c1.height / 2, -PI / 2, - PI / 4 * 3, arc_center = c1.get_center()).match_color(arc_0)
		brace_b = ArcBrace(arc_b, buff = MED_LARGE_BUFF)
		label_b = Tex("3").move_to(BraceLabel(brace_b, "", b_direction))
		self.play(ReplacementTransform(lbc.copy(), arc_b))
		self.play(FadeIn(brace_b, target_position = arc_b), FadeIn(label_b, shift = b_direction))

		l0 = self.circle_attach[1]
		self.play(Indicate(l0, color = RED), Indicate(l1, color = RED), Indicate(l2, color = RED))
		self.play(
			l0.animate.become(SingleStringMathTex(r"L_{_{1,1}}").match_height(l0).move_to(l0)),
			l1.animate.become(SingleStringMathTex(r"L_{_{2,1}}").match_height(l1).move_to(l1)),
			l2.animate.become(SingleStringMathTex(r"L_{_{2,3}}").match_height(l2).move_to(l2)),
		)

		t0_tex_target = SingleStringMathTex(r"\frac{1}{L_{_{1,1}}^2}").align_to(t0_tex, LEFT).match_y(t0_tex)
		t1_tex_target = SingleStringMathTex(r"=\frac{1}{L_{_{2,1}}^2}+\frac{1}{L_{_{2,3}}^2}").align_to(equal, LEFT).match_y(t1_tex)
		t1_tex_target[1:].set_color(YELLOW)
		self.play(Circumscribe(Group(pi_tex, t1_tex)))
		self.play(
			ReplacementTransform(t0_tex[0:2], t0_tex_target[0:2]),
			ReplacementTransform(t0_tex[2:], t0_tex_target[2:]),
			ReplacementTransform(t1_tex[0:3], t1_tex_target[0:3]),
			ReplacementTransform(t1_tex[3:6], t1_tex_target[3:8]),
			ReplacementTransform(t1_tex[6:9], t1_tex_target[7:11]),
			ReplacementTransform(t1_tex[9:], t1_tex_target[11:]),
		)


		self.remove(*t0_tex, *t1_tex)
		t1_tex = t1_tex_target
		t0_tex = t0_tex_target
		pi_tex = Group(*pi_tex[0:-4], *t0_tex)
		self.tex_group = Group(*self.tex_group[:-1], pi_tex, t1_tex)
		self.add(*self.tex_group)

		self.play(FadeOut(angle0, label0, angle1, label1, arc_a, arc_b, brace_a, brace_b, label_a, label_b))
		self.circle_attach.remove(self.circle_attach[2])
		bc.attach = VGroup(*self.circle_attach[0:-1], l1, l2)
		bc.add(bc.attach)
		self.basel_circle = bc
		self.circle_dots = Group(down_dot, top_dot, a_dot, b_dot)

	def more_circles(self):
		self.basel_circle.dots = VGroup()
		self.basel_circle.add(self.basel_circle.dots)
		for dot in self.circle_dots:
			dot.clear_updaters()
			self.basel_circle.dots.add(dot)

		circle_target = self.basel_circle.copy().to_edge(LEFT)
		expand_tex = self.tex_group[-2:]
		expand_target = expand_tex.copy().next_to(circle_target, RIGHT, 0).align_to(self.basel_circle, UP)
		self.play(
			self.basel_circle.animate.move_to(circle_target),
			FadeOut(self.tex_group[0:-2], shift = expand_target.get_center() - expand_tex.get_center()),
			expand_tex.animate.move_to(expand_target),
		)
		self.tex_group = Group(*expand_tex)

		last_tex = self.tex_group[-1]
		bottom = self.basel_circle.circles[0].get_bottom()
		space = STAGE_WIDTH / 2 - last_tex.get_left()[0] - MED_LARGE_BUFF

		for _ in range(2):
			self.play(ScaleAbout(self.basel_circle, 0.5, bottom))
			circle = self.basel_circle.make_circle(0)
			dots = []
			for t in circle.triangles:
				dots.append(Dot(t.pa, color = ORANGE).set_z_index(2))
				dots.append(Dot(t.pb, color = ORANGE).set_z_index(2))

			self.play(Create(circle))
			self.play(*[GrowFromPoint(t.line_c, t.ph) for t in circle.triangles])
			self.play(*[Create(dot) for dot in dots])
			self.play(*[AnimationGroup(Create(t.line_a), Create(t.line_b)) for t in circle.triangles])
			
			line_animations = []
			last_triangles = self.basel_circle.triangles[-1]
			for i in range(len(last_triangles)):
				lt = last_triangles[i]
				nt1 = circle.triangles[i * 2]
				nt2 = circle.triangles[i * 2 + 1]
				la = lt.line_a.submobjects[0]
				lb = lt.line_b.submobjects[0]
				lt.line_a.remove(la)
				lt.line_b.remove(lb)
				lac = la.copy()
				lbc = lb.copy()
				line_animations.append(la.animate.become(nt1.line_a.copy().match_color(la)))
				line_animations.append(lac.animate.become(nt1.line_b.copy().match_color(la)))
				line_animations.append(lb.animate.become(nt2.line_a.copy().match_color(lb)))
				line_animations.append(lbc.animate.become(nt2.line_b.copy().match_color(lb)))
				nt1.line_a.add(la)
				nt1.line_b.add(lac)
				nt2.line_a.add(lb)
				nt2.line_b.add(lbc)
			self.play(*line_animations)

			num = self.basel_circle.circle_num + 1
			new_tex = SingleStringMathTex("=" + "+".join([r"\frac{{1}}{{L_{{_{{{0},{1}}}}}^2}}".format(num, 2*i+1) for i in range(pow(2, num-1))]))
			new_tex[1:].set_color(YELLOW)
			new_tex.match_height(last_tex)

			if new_tex.width > space:
				factor = space / new_tex.width
				self.play(ScaleAbout(self.tex_group, factor, self.tex_group.get_corner(UL)))
				new_tex.scale(factor)

			new_tex.next_to(last_tex, DOWN).align_to(last_tex, LEFT)
			self.play(
				last_tex.animate.set_color(WHITE),
				FadeIn(new_tex, shift = DOWN),
			)

			self.tex_group.add(new_tex)
			last_tex = new_tex

			self.basel_circle.attach_circle(circle)
			self.basel_circle.dots.add(*dots)

		n_tex_str = "=" + "+".join([r"\frac{{1}}{{L_{{_{{n,{0}}}}}^2}}".format(2*i+1) for i in range(5)]) + r"+\cdots + \frac{1}{L_{_{n,{2^n}-1}}^2}"
		n_tex = SingleStringMathTex(n_tex_str).match_width(last_tex).next_to(last_tex, DOWN).align_to(last_tex, LEFT)
		n_tex[1:].set_color(YELLOW)
		self.play(
			last_tex.animate.set_color(WHITE),
			FadeIn(n_tex, shift = DOWN),
		)

		self.basel_circle.remove(self.basel_circle.dots)
		lines = []
		for t in self.basel_circle.triangles[-1]:
			l1 = t.line_a.submobjects[0]
			l2 = t.line_b.submobjects[0]
			lines.append(l1)
			lines.append(l2)
			t.line_a.remove(l1)
			t.line_b.remove(l2)
		self.play(
			*[FadeOut(dot, target_position = bottom) for dot in self.basel_circle.dots],
			*[Uncreate(line) for line in lines],
			n_tex.animate.set_color(WHITE),
		)

		circle_target = self.basel_circle.copy().set_x(0).to_stage_edge(UP)
		pi_tex = self.tex_group[0]
		tex_target = SingleStringMathTex(r"\frac{\pi^2}{8}" + n_tex_str).match_height(n_tex).next_to(circle_target, DOWN)
		self.play(
			self.basel_circle.animate.move_to(circle_target),
			pi_tex[0:4].animate.match_height(tex_target[0:4]).move_to(tex_target[0:4]),
			n_tex.animate.become(tex_target[4:]),
			FadeOut(pi_tex[4:], self.tex_group[1:]),
		)
		self.add(tex_target)
		self.remove(*pi_tex, n_tex)
		n_tex = tex_target

		for _ in range(5):
			circle = self.basel_circle.make_circle(0)
			self.play(Create(circle))
			self.play(Create(circle.triangles))
			self.basel_circle.attach_circle(circle)

		circle = self.basel_circle.circles[-1]
		bottom = self.basel_circle.circles[0].get_bottom()
		self.play(ScaleAbout(VGroup(circle, circle.triangles), 10, circle.get_bottom()), run_time = 3)

		l_tex = SingleStringMathTex(r"\ ,L_{_{n,m}}=m").scale_to_fit_height(n_tex.height / 2).move_to(n_tex.get_right())
		self.play(n_tex.animate.next_to(l_tex, LEFT), FadeIn(l_tex, shift = RIGHT))

		tex_group = Group(n_tex, l_tex)

		self.play(
			FadeOut(self.basel_circle, shift = UP * STAGE_HEIGHT / 4, scale = 0),
			tex_group.animate.to_stage_edge(UP),
		)
		self.clear()
		self.add(n_tex, l_tex)

		down_arrow = SingleStringMathTex(r"\Downarrow").next_to(tex_group, DOWN)
		all_tex = MathTex(
						r"{{\frac{\pi^2}{8}&=" + "+".join([r"\frac{{1}}{{{0}^2}}".format(i*2+1) for i in range(7)]) + r"\cdots \\}}"
						r"x&=" + "+".join([r"\frac{{1}}{{{0}^2}}".format(i+1) for i in range(7)]) + r"\cdots \\" +
						r"{{\frac{x}{4}&=" + "+".join([r"\frac{{1}}{{4\times {0}^2}}".format(i+1) for i in range(4)]) + r"\cdots \\}}" +
					 	r"&=" + "+".join([r"\frac{{1}}{{{0}^2}}".format((i+1)*2) for i in range(7)]) + r"\cdots \\"+
						r"{{\frac{3}{4}x&=" + "+".join([r"\frac{{1}}{{{0}^2}}".format(i*2+1) for i in range(7)]) + r"\cdots \\}}"+
						r"\frac{\pi^2}{6}&=x=" + "+".join([r"\frac{{1}}{{{0}^2}}".format(i+1) for i in range(7)]) + r"\cdots"
					 ).next_to(down_arrow, DOWN)
		self.play(FadeIn(down_arrow, all_tex[0], shift = DOWN))
		self.play(FadeIn(all_tex[1], target_position = all_tex[1].get_left()))
		self.play(FadeIn(all_tex[2], shift = DOWN))
		self.play(FadeIn(all_tex[3], shift = DOWN))

		self.play(Circumscribe(Group(all_tex[1][0], all_tex[2][0:3]), fade_out = True))
		x = all_tex[4:].get_x()
		all_tex[4:].next_to(all_tex[0], DOWN).set_x(x)
		self.play(FadeOut(all_tex[1:4], scale = 0), FadeIn(all_tex[4], shift = UP))

		self.play(Circumscribe(Group(all_tex[0][0:4], all_tex[4][0:4]), fade_out = True))
		self.play(FadeIn(all_tex[-1], shift = DOWN))
		self.play(FadeOut(all_tex[-1][4:6], scale = 0), all_tex[-1][6:].animate.shift(all_tex[-1][4].get_center() - all_tex[-1][6].get_center()))