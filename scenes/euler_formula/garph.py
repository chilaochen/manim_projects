import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))

from units import *

class graph(MultiZoomedScene):
	def setup(self):
		align_camera_with_stage(self)

	def construct(self):
		self.next_section(skip_animations = False)
		self.overview()
		self.next_section(skip_animations = False)
		self.euler_formula()
		self.next_section(skip_animations = False)
		self.triangle_on_sphere()
		self.next_section(skip_animations = False)
		self.triangle_area()
		self.next_section(skip_animations = False)
		self.calc_area()
		self.next_section(skip_animations = False)
		self.cube_in_circle()
		self.next_section(skip_animations = False)
		self.projection_area()
		self.next_section(skip_animations = False)
		self.simple_proof()
		self.wait()

	def overview(self):
		euler_tex = SingleStringMathTex(r"e^{\pi i} + 1 = 0").scale_to_fit_width(STAGE_WIDTH / 3)
		self.add(euler_tex)
		self.wait(1)

		self.remove(euler_tex)
		euler_tex = SingleStringMathTex(r"V - E + F = 2").scale_to_fit_width(STAGE_WIDTH / 3)
		self.add(euler_tex)

		title = Text("欧拉公式").match_height(euler_tex).next_to(euler_tex, UP)
		self.play(FadeIn(title, shift = UP))
		euler_tex.add(title)
		self.wait()

		self.play(euler_tex.animate.shift(UP * STAGE_HEIGHT / 4))

		p4 = Tetrahedron(STAGE_HEIGHT * 0.4, faces_config = {"fill_opacity" : 0}).rotate(-45 * DEGREES, Y_AXIS).rotate(np.arccos(1 / 3) / 2, X_AXIS)
		p4.move_to(LEFT * STAGE_WIDTH / 5)
		graph_title = Text("图论").next_to(p4, DOWN)

		seven_bridge = ImageMobject(os.path.join("assert", "topology", "seven_bridge")).scale_to_fit_width(p4.width * 0.8)
		seven_bridge_graph = ImageMobject(os.path.join("assert", "topology", "seven_bridge_graph")).match_width(seven_bridge)
		right_arrow = SingleStringMathTex(r"\Rightarrow")
		seven_bridge_group = Group(seven_bridge, right_arrow, seven_bridge_graph).arrange(RIGHT).move_to(RIGHT * STAGE_WIDTH / 5)
		topology_title = Text("著名的七桥问题\n  拓扑学的起源").next_to(seven_bridge_group, DOWN).match_y(graph_title)
		self.play(FadeIn(p4, target_position = euler_tex.get_bottom()), FadeIn(seven_bridge_group, target_position = euler_tex.get_bottom()))
		self.play(FadeIn(graph_title, shift = DOWN), FadeIn(topology_title, shift = DOWN))
		self.wait()

		euler_tex.remove(title)
		self.play(FadeOut(title, graph_title, shift = UP), euler_tex.animate.move_to(seven_bridge_group), FadeOut(seven_bridge_group, topology_title, shift = RIGHT * 2))
		self.euler_tex = euler_tex
		self.p4 = p4

	def euler_formula(self):
		graph = self.p4.graph
		vertices = VGroup(*graph.vertices.values()).set_z_index(1)
		edges = VGroup(*[Line(*e.get_start_and_end(), color = BLUE) for e in graph.edges.values()])
		faces = VGroup(*[f.copy().set_fill(BLUE, 0.5).set_stroke(width = 0) for f in self.p4.faces[0:3]])
		graph = VGroup(vertices, edges)
		self.remove(self.p4)
		self.add(graph)
		self.graph = graph.copy().add(faces.copy().set_fill(None, 0))

		v = self.euler_tex[0]
		e = self.euler_tex[2]
		f = self.euler_tex[4]
		v_text = Text("点").match_width(v).next_to(v, UP)
		e_text = Text("线").match_width(e).next_to(e, UP)
		f_text = Text("面").match_width(f).next_to(f, UP)
		num_tex = SingleStringMathTex(r"4 - 6 + 4 = 2").match_height(self.euler_tex).next_to(self.euler_tex, DOWN, MED_LARGE_BUFF)
		for i in range(len(num_tex)):
			num_tex[i].match_x(self.euler_tex[i])

		focus_rect = SurroundingRectangle(v)
		back_rect = SurroundingRectangle(vertices).set_fill(BLUE, 0.5).set_stroke(width = 2).scale(1.2).set_z_index(-1)
		self.play(LaggedStart(*[v.animate.set_color(YELLOW).scale(2) for v in vertices], lag_ratio = 0.2), Create(focus_rect), run_time = 2)
		self.play(FadeIn(v_text, shift = UP), FadeIn(num_tex[0], shift = DOWN), v.animate.match_color(vertices[0]), *[v.animate.set_color(YELLOW).scale(0.5) for v in vertices])
		self.wait()
		self.play(LaggedStart(*[e.animate.set_color(ORANGE).set_stroke(width = 6) for e in edges], lag_ratio = 0.15), focus_rect.animate.move_to(e), run_time = 2)
		self.play(FadeIn(e_text, shift = UP), FadeIn(num_tex[2], shift = DOWN), e.animate.match_color(edges[0]), edges.animate.set_stroke(width = 4))
		self.wait()
		self.play(LaggedStart(*[FadeIn(f, scale = 0.1) for f in faces], lag_ratio = 0.3, run_time = 1.8), Succession(Wait(1), FadeIn(back_rect, run_time = 1)), focus_rect.animate(run_time = 2).move_to(f))
		self.play(FadeIn(f_text, shift = UP), FadeIn(num_tex[4], shift = DOWN), f.animate.match_color(faces[0]))

		top_title = Text("连通图：图中没有孤立的点").next_to(back_rect, UP)
		self.play(FadeIn(top_title, shift = UP / 2))
		self.play(FadeIn(num_tex[1], num_tex[3], num_tex[5:]), *[FadeOut(f, scale = 0) for f in faces], FadeOut(back_rect, focus_rect))
		self.wait()

		graph.add(top_title)
		self.legendre = ImageMobject(os.path.join("assert", "portrait", "Legendre")).scale_to_fit_height(STAGE_HEIGHT / 2).move_to(graph)
		name = Text("勒让德").next_to(self.legendre, DOWN)
		self.play(FadeOut(graph, shift = UP * self.legendre.height), FadeIn(self.legendre, shift = UP * self.legendre.height), FadeOut(num_tex, shift = UP))
		self.play(FadeIn(name, shift = DOWN / 2))

		self.remove(name)
		self.legendre.add(name)
		self.tex_title = VGroup(v_text, e_text, f_text)
		self.euler_group = Group(self.euler_tex, self.tex_title)

		color_map = dict(
			V = v.get_color(),
			E = e.get_color(),
			F = f.get_color(),
		)
		MathTex.set_default(tex_to_color_map = color_map)

	def triangle_on_sphere(self):
		triangle = Triangle().match_width(self.legendre).move_to(self.legendre)

		dot_a = Dot(triangle.get_top(), color = YELLOW)
		dot_b = Dot(triangle.get_corner(DL), color = YELLOW)
		dot_c = Dot(triangle.get_corner(DR), color = YELLOW)
		line_a = Line(dot_b.get_center(), dot_c.get_center())
		line_b = Line(dot_b.get_center(), dot_a.get_center())
		line_c = Line(dot_c.get_center(), dot_a.get_center())
		
		dots = VGroup(dot_a, dot_b, dot_c).set_z_index(2)
		lines = VGroup(line_a, line_b, line_c).set_z_index(1)
		self.play(FadeIn(dots, lines), FadeOut(self.legendre))

		triangle_tex = SingleStringMathTex(r"S_{\text{三角形}}=?").match_x(self.euler_tex).match_y(dots)
		self.play(FadeOut(self.euler_group, shift = UP * 2), FadeIn(triangle_tex, target_position = dots))
		self.wait()

		radius = 3
		self.radius = radius
		center = LEFT * STAGE_WIDTH / 4
		dot = Dot(color = BLUE).move_to(center)
		circle = Circle(radius, color = BLUE, fill_opacity = 0.3, stroke_width = 3).move_to(center)

		c1 = Circle(radius, ORANGE).rotate(-45 * DEGREES)
		dc1 = DashedVMobject(c1, 128, 0.5)
		dc1.add(c1.set_stroke(width = 0))
		dc1.circle = c1
		line1 = Line(IN * radius, OUT * radius)
		line12 = Line(dc1.get_left(), dc1.get_right())
		line13 = line12.copy()

		start_angle = -75 * DEGREES
		angle = 45 * DEGREES
		end_angle = start_angle + angle
		angle_plane = 60 * DEGREES
		angle23 = np.arctan((1 - np.cos(angle)) / (np.sin(angle) * np.cos(-angle_plane)))

		arc1 = Arc(radius, start_angle, angle, stroke_width = 6).match_color(dc1).set_z_index(1)
		arc2 = Arc(radius, start_angle, angle23, stroke_width = 6, color = LIGHT_PINK).set_z_index(1)
		arc3 = Arc(radius, end_angle, -angle23, stroke_width = 6, color = GREEN).set_z_index(1)

		Group(dc1, line1, line12, line13, arc1, arc2, arc3).rotate(-75 * DEGREES, X_AXIS).move_to(center)
		line12.rotate(start_angle, line_to_axis(line1))
		line13.rotate(end_angle, line_to_axis(line1))

		c2 = c1.copy()
		c3 = c1.copy()
		dc2 = dc1.copy().match_color(arc2).add(c2)
		dc3 = dc1.copy().match_color(arc3).add(c3)
		dc2.circle = c2
		dc3.circle = c3
		line2 = line1.copy()
		line3 = line1.copy()
		Group(dc2, arc2, line2).rotate(angle_plane, line_to_axis(line12), center)
		Group(dc3, arc3, line3).rotate(-angle_plane, line_to_axis(line13), center)
		
		dc1.axis = line_to_axis(line1)
		dc2.axis = line_to_axis(line2)
		dc3.axis = line_to_axis(line3)

		dot13 = Dot(line13.get_end())
		dot12 = Dot(line12.get_end())
		dot23 = dot12.copy().rotate(angle23, dc2.axis, center)
		line23 = Line(center, dot23.get_center())
		axes = [line_to_axis(line) for line in (line12, line13, line23)]

		circles = VGroup(dc3, dc2, dc1)
		self.play(
			lines.animate.become(VGroup(arc1, arc2, arc3)),
			dot_a.animate.move_to(dot23), dot_b.animate.move_to(dot12), dot_c.animate.move_to(dot13), 
			triangle_tex[0:4].animate.set_color_by_gradient(*[c.get_color() for c in circles]),
			FadeIn(circle), FadeIn(dot),
			run_time = 2
		)
		self.wait()

		self.play(LaggedStart(*[Create(c) for c in circles], lag_ratio = 0.5), run_time = 3)

		angle1 = PI - angle_between_vectors(dc2.axis, dc3.axis)
		area11 = Sphere(center, radius, [7, 20], (0, angle1), stroke_width = 2, stroke_opacity = 0.02, fill_opacity = 0.3).match_color(circle)
		area11.rotate(15 * DEGREES, X_AXIS, center).rotate(end_angle - 90 * DEGREES, dc1.axis, center).rotate(-angle_plane, axes[1], center).rotate(-angle23, dc3.axis, center)
		area12 = area11.copy().rotate(PI, axes[2], center)
		area21 = Sphere(center, radius, [7, 20], (0, angle_plane), stroke_width = 2, stroke_opacity = 0.02, fill_opacity = 0.3).match_color(circle)
		area21.rotate(15 * DEGREES, X_AXIS, center).rotate(end_angle - 90 * DEGREES, dc1.axis, center)
		area22 = area21.copy().rotate(PI, axes[1], center)
		area31 = area22.copy().match_color(circle).rotate(PI - angle, dc1.axis, center)
		area32 = area31.copy().rotate(PI, axes[0], center)

		self.triangle_tex = triangle_tex
		self.axes = axes
		self.circles = circles
		self.circle = circle
		self.circle.dot = dot
		self.center = center
		self.triangle = VMobject().add(lines, dots)
		self.triangle.lines = lines
		self.triangle.dots = dots
		self.area_group = VGroup(VGroup(area31, area32), VGroup(area21, area22), VGroup(area11, area12))

	def triangle_area(self):
		fadein_animations = []
		for pair in self.area_group:
			for area in pair:
				fadein_animations.append(FadeIn(area, scale = 1.2, shift = self.center - area.get_center()))
		self.play(LaggedStart(*fadein_animations, lag_ratio = 0.3, run_time = 6))

		mirror_triangle = self.triangle.copy().apply_function(lambda pos: self.center * 2 - pos)
		self.play(FadeIn(mirror_triangle))
		self.play(Indicate(self.triangle, color = None), Indicate(mirror_triangle, color = None))
		
		dias = VGroup(*[DashedLine(self.triangle.dots[i].get_center(), mirror_triangle.dots[i].get_center(), 0.25) for i in range(3)])
		self.play(*[Create(d) for d in dias])
		self.wait()
		self.play(FadeOut(dias))

		area_tex = MathTex(r"{{S_{\text{绿}}}}+{{S_{\text{粉}}}}+{{S_{\text{橙}}}}={{S_{\text{球}}}}+4\times{{S_{\text{三角形}}}}").align_to(self.circle, UP).match_x(self.triangle_tex)
		area_tex[6].match_color(self.circle)
		area_tex[-2].set_color_by_gradient(*[c.get_color() for c in self.circles])

		for i in range(3):
			area_tex[i * 2].match_color(self.circles[i])
			self.play(self.area_group[i].animate.scale(1.2))
			self.play(self.area_group[i].animate.match_color(self.circles[i]), FadeIn(area_tex[i * 2], shift = RIGHT))
			self.play(self.area_group[i].animate.scale(1 / 1.2))

		self.wait()
		self.play(FadeIn(area_tex[1], area_tex[3]))
		self.play(FadeIn(area_tex[5:7]))
		self.play(FadeIn(area_tex[7]), ReplacementTransform(self.triangle_tex[0:4].copy(), area_tex[-2]))

		circle_tex = MathTex(r"{{S_{\text{球}}}}=4\pi R^2{{=4\pi}}").next_to(area_tex, DOWN, MED_LARGE_BUFF)#.align_to(area_tex, LEFT)
		circle_tex[0].match_color(self.circle)
		self.play(FadeIn(circle_tex[0:-1], shift = RIGHT))
		self.play(FadeIn(circle_tex[-1], shift = RIGHT))

		focus_rect = SurroundingRectangle(area_tex[0:5])
		self.play(Create(focus_rect))
		self.play(
			focus_rect.animate.become(SurroundingRectangle(area_tex[0])),
			FadeOut(self.circles[0], self.area_group[1:], self.triangle, mirror_triangle),
		)
		self.area_tex = area_tex
		self.focus_rect = focus_rect
		self.circle_tex = circle_tex

	def calc_area(self):
		green_area = self.area_group[0]
		angle_tracker = ValueTracker(60)
		angle_tracker.save_state()
		fix_circle = self.circles[2]
		rotate_circle = self.circles[1]

		def area_updater(m):
			angle = angle_tracker.get_value()
			area = Sphere(self.center, self.radius, [int(np.ceil(abs(angle) / 9)), 20], (0, angle * DEGREES), stroke_width = 2, stroke_opacity = 0.02, fill_opacity = 0.3).match_color(m)
			area.rotate(15 * DEGREES, X_AXIS, self.center).rotate(15 * DEGREES, fix_circle.axis, self.center)
			m[0].become(area)
			m[1].become(area.copy().rotate(PI, self.axes[0], self.center))
		green_area.add_updater(area_updater)

		def circle_updater(m):
			m.become(fix_circle.copy().rotate(angle_tracker.get_value() * DEGREES, self.axes[0], self.center).match_color(m))
		rotate_circle.add_updater(circle_updater)

		dot = self.triangle.dots[1]
		line1 = Line(fix_circle.get_left(), fix_circle.get_right()).rotate(15 * DEGREES, fix_circle.axis, self.center).move_to(dot)
		xy_func = lambda pos: np.array([*pos[0:2], 0])
		line1_xy = line1.copy().apply_function(xy_func).set_opacity(0)
		line2_xy = line1_xy.copy()
		line2_xy.add_updater(lambda m: m.become(line1.copy().rotate(angle_tracker.get_value() * DEGREES, self.axes[0], dot.get_center()).apply_function(xy_func)).set_opacity(0))
		line2_xy.update()

		self.add(line1_xy, line2_xy)
		self.play(angle_tracker.animate.set_value(120), run_time = 2)
		self.play(angle_tracker.animate.set_value(45), run_time = 2)

		angle = Angle(line1_xy, line2_xy).add_updater(lambda m: m.become(Angle(line1_xy, line2_xy, color = YELLOW, radius = 0.3)).set_z_index(1))
		angle.update()
		self.play(Create(angle))

		angle_dot = dot.copy().rotate(12 * DEGREES, fix_circle.axis, self.center)
		angle_tex = SingleStringMathTex(r"\alpha").set_z_index(1)
		angle_tex.add_updater(lambda m: m.move_to(angle_dot.copy().rotate(angle_tracker.get_value() / 2 * DEGREES, self.axes[0], self.center)))
		angle_tex.update()
		self.play(FadeIn(angle_tex, target_position = angle))
		self.wait()

		self.play(*[c.circle.animate.set_fill(BLUE, 0.5) for c in (fix_circle, rotate_circle)])
		self.play(*[c.circle.animate.set_fill(None, 0) for c in (fix_circle, rotate_circle)])
		self.play(Indicate(angle_tex, rate_func = rate_functions.there_and_back_with_pause, run_time = 3))
		self.play(angle_tracker.animate.set_value(179.9), run_time = 3)

		alpha_tex = SingleStringMathTex(r"=\pi").next_to(angle_tex)
		self.play(FadeIn(alpha_tex, shift = RIGHT))
		self.play(ShowPassingFlash(self.circle.copy().set_fill(opacity=0).set_stroke(YELLOW, 6), run_time = 2, time_width = 1))

		area_rect = SurroundingRectangle(self.circle_tex[-1][-2:])
		self.play(Create(area_rect))

		down_arrow = SingleStringMathTex(r"\Downarrow").next_to(self.area_tex[0], DOWN)
		green_tex = SingleStringMathTex(r"4\alpha").next_to(down_arrow, DOWN).match_color(green_area)
		self.play(Group(self.circle_tex, area_rect, self.triangle_tex).animate.next_to(green_tex, DOWN, MED_LARGE_BUFF).match_x(self.area_tex))
		self.play(
			FadeIn(down_arrow, shift = DOWN),
			ReplacementTransform(angle_tex.copy(), green_tex[1]),
			ReplacementTransform(self.circle_tex[-1][-2].copy(), green_tex[0]),
		)

		self.wait()
		self.play(angle_tracker.animate(run_time = 2).set_value(60), FadeOut(alpha_tex, area_rect))
		self.play(FadeIn(self.circles[0], self.area_group[1:], self.triangle))

		green_area.clear_updaters()
		rotate_circle.clear_updaters()
		line2_xy.clear_updaters()
		angle.clear_updaters()
		angle_tex.clear_updaters()

		dot = self.triangle.dots[2]
		line1.rotate(45 * DEGREES, fix_circle.axis, self.center)
		line2 = line1.copy().rotate(-60 * DEGREES, self.axes[1], dot.get_center())
		angle2 = Angle(line2.copy().apply_function(xy_func), line1.copy().apply_function(xy_func), color = YELLOW, quadrant = (-1, -1), radius = 0.3)
		angle_tex2 = SingleStringMathTex(r"\beta").move_to(dot.copy().rotate(-16 * DEGREES, fix_circle.axis, self.center).rotate(-30 * DEGREES, self.axes[1], dot.get_center()))
		pink_tex = SingleStringMathTex(r"4\beta").match_x(self.area_tex[2]).match_y(green_tex).match_color(self.area_group[1])
		self.play(Create(angle2), FadeIn(angle_tex2))
		self.play(self.focus_rect.animate.move_to(self.area_tex[2]), down_arrow.animate.match_x(self.area_tex[2]), FadeIn(pink_tex, target_position = green_tex))

		dot = self.triangle.dots[0]
		line2.rotate(-angle_between_vectors(self.axes[1], self.axes[2]), self.circles[0].axis, self.center)
		line1 = line2.copy().rotate(angle_between_vectors(self.circles[1].axis, self.circles[0].axis) - PI, self.axes[2], dot.get_center())
		angle3 = Angle(line1.copy().apply_function(xy_func), line2.copy().apply_function(xy_func), color = YELLOW, radius = 0.3)
		angle_tex3 = SingleStringMathTex(r"\gamma").move_to(dot.copy().rotate(12 * DEGREES, self.circles[0].axis, self.center).rotate(-40 * DEGREES, self.axes[2], dot.get_center()))
		orange_tex = SingleStringMathTex(r"4\gamma").match_x(self.area_tex[4]).match_y(pink_tex).match_color(self.area_group[2])
		self.play(Create(angle3), FadeIn(angle_tex3))
		self.play(self.focus_rect.animate.move_to(self.area_tex[4]), down_arrow.animate.match_x(self.area_tex[4]), FadeIn(orange_tex, target_position = green_tex))

		pi_tex = self.circle_tex[-1][-2:].copy()
		self.play(self.focus_rect.animate.move_to(self.area_tex[6]), down_arrow.animate.match_x(self.area_tex[6]), pi_tex.animate.match_x(self.area_tex[6]).match_y(green_tex))
		other_tex = Group(self.area_tex[1], self.area_tex[3], self.area_tex[5], *self.area_tex[7:]).copy().match_y(green_tex)
		self.play(FadeIn(other_tex), FadeOut(self.focus_rect))

		calc_tex = Group(green_tex, pink_tex, orange_tex, pi_tex, other_tex)
		down_arrow2 = down_arrow.copy().move_to(center_of_mass([calc_tex.get_center(), self.triangle_tex.get_center()]))
		self.play(FadeOut(down_arrow), FadeOut(self.circle_tex))
		
		final_tex = SingleStringMathTex(r"S_{\text{三角形}}=\alpha+\beta+\gamma-\pi").move_to(self.triangle_tex)
		final_tex[0:4].set_color_by_gradient(*[c.get_color() for c in self.circles])
		final_tex[5].match_color(green_tex)
		final_tex[7].match_color(pink_tex)
		final_tex[9].match_color(orange_tex)
		self.play(FadeIn(down_arrow2, target_position = calc_tex.get_bottom()), FadeOut(self.triangle_tex[-1]))
		self.play(ReplacementTransform(self.triangle_tex[0:5], final_tex[0:5]), FadeIn(final_tex[5:]))
		self.wait()

		self.euler_group.move_to(Group(self.area_tex, calc_tex))
		self.remove(*self.area_tex, *calc_tex, *green_tex, down_arrow2)
		self.add(self.euler_group)
		self.calc_tex = calc_tex
		self.triangle_tex = final_tex
		self.down_arrow = down_arrow2
		self.triangle.add(angle, angle2, angle3, angle_tex, angle_tex2, angle_tex3)
		self.wait()

	def cube_in_circle(self):
		cube = Cube(self.radius * 0.7, fill_opacity = 0.5, stroke_width = 4, stroke_color = ORANGE)#.next_to(circle)
		graph = cube.copy().rotate(PI, Y_AXIS).set_fill(opacity=0).apply_function(lambda pos: pos * (1 - (pos[2] - cube[0].get_z()) * 0.2))
		gdots = attach_dots_on_cube(graph, color = YELLOW).set_z_index(1)
		dot = Dot().match_x(self.euler_group).match_y(self.circle)
		graph.match_y(self.circle).match_x(self.euler_group)
		cube.rotate(15 * DEGREES, X_AXIS).rotate(15 * DEGREES, Y_AXIS).move_to(dot)
		self.add(gdots)
		self.play(FadeIn(graph, scale = 0.5), self.euler_group.animate.to_stage_edge(UP), self.triangle_tex.animate.next_to(cube, DOWN, MED_LARGE_BUFF))

		rotate_cube = cube.copy().move_to(midpoint(dot.get_center(), self.circle.get_right()))
		dots = attach_dots_on_cube(rotate_cube, color = YELLOW).set_z_index(1)
		self.add(dots)
		self.play(graph.animate.move_to(midpoint(dot.get_center(), STAGE_RIGHT)), FadeIn(rotate_cube, target_position = dot))

		cube_pos = Dot(rotate_cube.get_center(), fill_opacity = 0)
		rotate_cube.angle = 0
		def cube_updater(m, dt):
			m.angle += dt * PI / 3.5
			m.become(cube.copy().move_to(cube_pos).rotate(m.angle, Y_AXIS))
		rotate_cube.add_updater(cube_updater)
		self.wait(3)
		
		rotate_cube.suspend_updating()
		animate_cube = rotate_cube.copy().clear_updaters()
		animate_dots = attach_dots_on_cube(animate_cube, color = YELLOW)
		self.add(animate_dots)
		self.play(ReplacementTransform(animate_cube, graph), run_time = 2)
		self.remove(animate_dots)

		rotate_cube.resume_updating()
		srect = SurroundingRectangle(graph, buff = MED_SMALL_BUFF)
		self.play(Create(srect))
		title = Text("施莱格尔图").next_to(srect, DOWN)
		self.play(FadeIn(title, shift = DOWN), srect.animate.become(SurroundingRectangle(title)), self.triangle_tex.animate.next_to(title, DOWN).match_x(dot))
		self.play(FadeOut(srect))
		self.wait()

		self.play(FadeOut(self.circles[0:2], self.area_group, self.triangle))
		self.play(Flash(self.circle.dot), self.circle.dot.animate.set_color(YELLOW), self.circle.animate.set_color(YELLOW))

		self.play(
			# rotate_cube.animate.move_to(cube.move_to(self.center)),
			cube_pos.animate.move_to(self.center),
			FadeOut(Group(graph, title), target_position = STAGE_RIGHT),
		)
		self.remove(gdots)
		self.wait()
		
		rotate_cube.clear_updaters()
		trans_cube = rotate_cube.copy().set_fill(opacity = 0).set_stroke(opacity = 0)
		prepare_for_nonlinear_transform(trans_cube)
		animate_dots = VGroup(*[Dot().match_color(d).move_to(d) for d in dots])
		dots_on_circle = VGroup(*[Dot().match_color(d).add_updater(lambda m,d=d: m.move_to(self.circle_projection(d.get_center()))) for d in dots]).set_z_index(1)
		edges_on_circle = trans_cube.copy().add_updater(lambda m : m.become(trans_cube.copy().set_stroke(opacity = 1).apply_function(self.circle_projection)))
		face_on_circle = self.circle.copy().set_fill(BLUE, 0.5).set_stroke(width = 0)
		edges_on_circle.update()
		dots_on_circle.update()
		self.play(FadeIn(face_on_circle, scale = 0.6), ReplacementTransform(trans_cube.copy(), edges_on_circle), ReplacementTransform(animate_dots, dots_on_circle))
		self.add(edges_on_circle, dots_on_circle)
		self.wait()
		self.play(Rotating(VGroup(trans_cube, rotate_cube), Y_AXIS, TAU, self.center, rate_func = rate_functions.ease_in_out_cubic, run_time = 3))

		graph.dots = gdots
		rotate_cube.shadow = trans_cube
		rotate_cube.dots = dots
		self.graph = graph
		self.cube = rotate_cube
		self.projection_group = VGroup(dots_on_circle, edges_on_circle, face_on_circle)
		dots_on_circle.clear_updaters()
		edges_on_circle.clear_updaters()

	def projection_area(self):
		projection_tex = MathTex(r"""
			S_{\text{投影}}=S_{\text{球}}&=4\pi\\
			{{\text{所有内角和}-\pi\cdot (F+N)&=4\pi\\}}
			2V-(F+N)&=4\\
			{{2(E+N)-3(F+N)&=0}}
		""").next_to(self.euler_group, DOWN, MED_LARGE_BUFF).to_stage_edge(RIGHT, LARGE_BUFF)
		projection_tex[0][0:3].set_color(BLUE)
		projection_tex[0][4:6].set_color(BLUE)
		self.play(Write(projection_tex[0].match_x(self.euler_group)))
		self.play(Circumscribe(self.triangle_tex, fade_out = True))

		extra_edgs = VGroup()
		for s in self.cube:
			vs = s.get_vertices()
			extra_edgs.add(DashedLine(vs[0], vs[2], 0.25, color = WHITE))
		self.play(Create(extra_edgs, run_time = 3))
		prepare_for_nonlinear_transform(extra_edgs)

		extra_edgs_projection = extra_edgs.copy().add_updater(lambda m: m.become(extra_edgs.copy().apply_function(self.circle_projection)))
		self.play(ReplacementTransform(extra_edgs.copy(), extra_edgs_projection))
		extra_edgs_projection.clear_updaters()

		top_tex = MathTex(r"\begin{array}{ccc}\text{点}&\text{线}&\text{面}\\V&E+N&F+N\end{array}", tex_to_color_map = None)[0].match_x(self.euler_group).align_to(self.euler_group, UP)
		top_tex[3].set_color(YELLOW)
		top_tex[4].set_color(ORANGE)
		top_tex[7].set_color(BLUE)

		self.play(FadeOut(self.euler_group, shift = UP * 2), FadeIn(top_tex, target_position = self.euler_group.get_bottom()))

		line1 = VGroup()
		for tex in projection_tex[1:4] : line1.add(*tex)
		focus_rect = SurroundingRectangle(top_tex[-3:])
		self.play(Create(focus_rect))
		self.play(FadeIn(line1, shift = DOWN / 2), focus_rect.animate.become(SurroundingRectangle(line1[-8:-3])))

		angel_tex = line1[0:5]
		circles = VGroup(*[Circle(DEFAULT_DOT_RADIUS * 3, YELLOW, stroke_width = 4).move_to(d) for d in self.projection_group[0]])
		self.play(Create(circles, run_time = 3))
		self.play(focus_rect.animate.become(SurroundingRectangle(angel_tex)))
		
		line2 = VGroup()
		for tex in projection_tex[4:9] : line2.add(*tex)
		v_tex = MathTex(r"2\pi \cdot V").move_to(angel_tex).align_to(angel_tex, RIGHT)
		self.play(angel_tex.animate.become(v_tex), focus_rect.animate.become(SurroundingRectangle(v_tex)))
		self.play(FadeOut(circles, focus_rect), FadeIn(line2, shift = DOWN / 2))
		self.play(FadeOut(self.triangle_tex))

		line3 = VGroup()
		for tex in projection_tex[9:-1] : line3.add(*tex)
		e_group= VGroup(*[MathTex("E") for _ in range(3)]).arrange(DOWN).next_to(line2, DOWN)
		f_group= VGroup(*[MathTex("F") for _ in range(2)]).arrange(DOWN, MED_LARGE_BUFF).next_to(e_group, RIGHT, 2)
		ef_lines = VGroup()
		for f in f_group:
			ef_lines.add(Line(e_group[1].get_right(), f.get_left()))
			ef_lines.add(Line(f.get_left(), e_group[0].get_right()))
			ef_lines.add(Line(f.get_left(), e_group[2].get_right()))
		ef_group = VGroup(e_group, ef_lines, f_group)
		ef_group.match_x(line3)

		self.play(FadeIn(e_group[1], shift = RIGHT))
		self.play(FadeIn(f_group), Create(ef_lines[0]), Create(ef_lines[3]))
		self.play(FadeIn(e_group[0], e_group[2]), Create(ef_lines[1:3], lag_ratio = 0), Create(ef_lines[4:], lag_ratio = 0))
		self.play(Circumscribe(e_group))
		self.play(Circumscribe(f_group))
		self.play(ef_group.animate.next_to(line3, DOWN), FadeIn(line3))
		self.play(FadeOut(projection_tex[0], line1, angel_tex, ef_group), VGroup(line2, line3).animate.align_to(projection_tex, UP))

		final_tex = MathTex(r"""
			2V-2(E+N)+2(F+N)&=4\\
			V-(E+N)+(F+N)&=2\\
			V-E+F&=2
		""").next_to(line3, DOWN, MED_LARGE_BUFF).align_to(line3, RIGHT)
		final_group = VGroup()
		final_group.add(final_tex[0:7]) 
		final_group.add(final_tex[7:13]) 
		final_group.add(final_tex[13:]) 

		for tex in final_group:
			self.play(FadeIn(tex, shift = DOWN / 2))

		fc1 = SurroundingRectangle(top_tex[-4])
		fc2 = SurroundingRectangle(top_tex[-1])
		self.play(Create(fc1), Create(fc2))
		self.play(Uncreate(fc1), Uncreate(fc2))

	def simple_proof(self):
		self.clear()
		self.add(self.euler_group.to_stage_edge(UP).set_x( - STAGE_WIDTH / 4))
		graph = Cube(STAGE_HEIGHT * 0.4, fill_opacity = 0.5, stroke_width = 4, stroke_color = ORANGE)
		graph.apply_function(lambda pos: pos * (1 - (pos[2] - graph[0].get_z()) * 0.15)).next_to(self.euler_group, DOWN, LARGE_BUFF)
		dots = attach_dots_on_cube(graph, color = YELLOW).update()
		self.add(graph, dots)

		edge_tex = MathTex(",\ ".join([r"k_{{{0}}}".format(i + 1) for i in range(5)]) + r"\cdots k_{F}")
		edge_brace = BraceLabel(edge_tex, r"F\text{个多边形的边数}")
		edge_group = VGroup(edge_tex, edge_brace).next_to(self.euler_group, RIGHT, LARGE_BUFF)
		self.play(Write(edge_tex))
		self.play(edge_brace.creation_anim())

		gon_obj = VGroup(*[RegularPolygon(i*2 + 1, stroke_color = ORANGE) for i in range(2, 5)]).scale_to_fit_height(STAGE_HEIGHT / 4)
		gon_obj.arrange(RIGHT, MED_LARGE_BUFF).match_y(graph).align_to(self.euler_group.get_right(), LEFT)
		self.play(Create(gon_obj))

		gon_lines = VGroup()
		gon_tex = VGroup()
		for gon in gon_obj:
			vs = gon.get_vertices()
			for i in range(2, len(vs) - 1):
				gon_lines.add(DashedLine(vs[0], vs[i]))
			tex = SingleStringMathTex(r"({0}-2)\pi".format(len(vs))).next_to(gon, DOWN)
			tex[1].set_color(YELLOW)
			gon_tex.add(tex)
		self.play(Create(gon_lines), run_time = 3)
		self.play(FadeIn(gon_tex, shift = DOWN / 2))

		gon_group = VGroup(gon_obj, gon_lines, gon_tex)
		graph_target = graph.copy().to_stage_edge(LEFT)
		angle_sum_tex = MathTex(r"""
			\text{内角和}&=(k_{1}-2)\pi+(k_{2}-2)\pi+\cdots+(k_{F}-2)\pi\\
			{{&=(k_{1}+k_{2}+\cdots+k_{F})\pi-2F\cdot\pi\\}}
			&=(2E-2F)\cdot\pi\\
			{{\text{内角和}&=(V-m)\cdot 2\pi + 2(m-2)\cdot\pi\\}}
			&=(2V-4)\cdot\pi
		""", tex_to_color_map = None).next_to(edge_brace, DOWN, MED_LARGE_BUFF).align_to(graph_target.get_right() + RIGHT * MED_LARGE_BUFF, LEFT)
		angle_sum_tex[0][-5].set_color(BLUE)
		angle_sum_tex[1][-3].set_color(BLUE)
		angle_sum_tex[1][-8].set_color(BLUE)
		angle_sum_tex[2][3].set_color(ORANGE)
		angle_sum_tex[2][6].set_color(BLUE)
		angle_sum_tex[3][5].set_color(YELLOW)
		angle_sum_tex[4][3].set_color(YELLOW)

		self.play(
			FadeIn(angle_sum_tex[0], shift = DOWN / 2),
			gon_group.animate.next_to(angle_sum_tex[0], DOWN).match_x(gon_group),
			graph.animate.move_to(graph_target),
		)
		self.play(FadeIn(angle_sum_tex[1], shift = DOWN / 2), FadeOut(gon_group, shift = DOWN))

		focus_rect = SurroundingRectangle(angle_sum_tex[1][1:15])
		self.play(Create(focus_rect))
		self.play(FadeIn(angle_sum_tex[2]), focus_rect.animate.become(SurroundingRectangle(angle_sum_tex[2][2:4])))
		self.play(FadeOut(focus_rect))

		inside_rect = SurroundingRectangle(graph[1], buff = MED_SMALL_BUFF)
		outside_rect = SurroundingRectangle(graph[0], buff = MED_SMALL_BUFF)
		self.play(Create(inside_rect))
		self.play(FadeIn(angle_sum_tex[3][0:12]), inside_rect.animate.become(SurroundingRectangle(angle_sum_tex[3][4:12])))
		self.play(FadeOut(inside_rect), FadeIn(outside_rect))
		self.play(FadeIn(angle_sum_tex[3][12:]), outside_rect.animate.become(SurroundingRectangle(angle_sum_tex[3][13:])))
		self.play(FadeIn(angle_sum_tex[4], shift = DOWN / 2), FadeOut(outside_rect))
		self.play(Circumscribe(angle_sum_tex[2]), Circumscribe(angle_sum_tex[4]))

	def circle_projection(self, pos):
		vec = pos - self.center
		scale = self.radius / np.linalg.norm(vec)
		return self.center + vec * scale
	
def line_to_axis(line : Line):
	return np.array(line.get_end()) - np.array(line.get_start())