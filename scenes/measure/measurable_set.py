import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))

from units import *

class measurable_set(MultiZoomedScene):
	def setup(self):
		random.seed(37)
		align_camera_with_stage(self)

	def construct(self):
		self.inner_and_exterior()
		self.wait()

	def inner_and_exterior(self):
		left_rcp = rand_connected_space().scale_to_fit_height(STAGE_HEIGHT * 0.4)
		self.play(Create(left_rcp.path))

		left_rcp.squares.set_opacity(0)
		left_rcp.path.set_z_index(1)
		right_rcp = left_rcp.copy()
		self.play(left_rcp.animate.shift(LEFT * STAGE_WIDTH / 5), right_rcp.animate.shift(RIGHT * STAGE_WIDTH / 5))

		left_title = Text("填充：内测度").next_to(left_rcp, DOWN, MED_LARGE_BUFF)
		right_title = Text("覆盖：外测度").next_to(right_rcp, DOWN, MED_LARGE_BUFF)
		left_rcp.remove(left_rcp.inner_squares, left_rcp.edge_squares)
		right_rcp.remove(right_rcp.inner_squares, right_rcp.edge_squares)
		left_rcp.inner_squares.set_opacity(1)
		right_rcp.squares.set_opacity(1)
		self.play(LaggedStart(*[FadeIn(s, scale = 0.1) for s in left_rcp.inner_squares[0]], lag_ratio = 0.1))
		self.play(FadeIn(left_title, shift = DOWN / 2))
		self.play(LaggedStart(*[FadeIn(s, scale = 2) for s in right_rcp.squares], lag_ratio = 0.1), run_time = 2)
		self.play(FadeIn(right_title, shift = DOWN / 2))

		shift = left_rcp.get_center() - right_rcp.get_center()
		for _ in range(5):
			right_inner, right_edge = right_rcp.check_edge()
			left_inner = right_inner.copy().shift(shift)
			
			self.play(
				LaggedStart(*[FadeIn(s, scale = 0.1) for s in left_inner], lag_ratio = 0.1),
				run_time = 1,
			)
			left_rcp.inner_squares.add(left_inner)

			self.remove(*right_rcp.edge_squares)
			self.play(
				LaggedStart(*[ReplacementTransform(s.parent.copy(), s) for s in right_edge], lag_ratio = 0.1),
				LaggedStart(*[ReplacementTransform(s.parent.copy(), s) for s in right_inner], lag_ratio = 0.1),
				run_time = 1,
			)
			right_rcp.update_squares(right_inner, right_edge)

		left_rcp.add(left_rcp.inner_squares)
		right_rcp.add(right_rcp.inner_squares)

		equal = Text("=").move_to(midpoint(left_title.get_right(), right_title.get_left())).scale_to_fit_height(left_title.height * 0.5)
		under_line = Underline(Group(left_title, right_title), color = BLUE)
		self.play(left_rcp.inner_squares.animate.set_opacity(0.7), right_rcp.inner_squares.animate.set_opacity(0.7))
		self.play(left_rcp.animate.center(), right_rcp.animate.center(), run_time = 2)
		self.play(
			FadeIn(equal), GrowFromCenter(under_line),
			left_rcp.inner_squares.animate.set_opacity(1), 
			right_rcp.inner_squares.animate.set_opacity(1), 
		)

		measurable_title = Text("可测集", color = BLUE).next_to(left_rcp, UP, MED_LARGE_BUFF)
		focus_rect = SurroundingRectangle(measurable_title)
		self.play(
			ReplacementTransform(left_rcp.path.copy(), focus_rect),
			FadeIn(measurable_title, shift = UP / 2, scale = 0.1),
		)

		measurable_desc = VGroup(left_title[-3:], equal, right_title[-3:])
		measurable_group = VGroup(measurable_title, right_rcp, measurable_desc)
		for g in left_rcp.inner_squares: self.remove(*g)
		self.remove(left_rcp.path)
		self.play(FadeOut(focus_rect, under_line))
		self.play(
			measurable_group[0:2].animate.set_x(- STAGE_WIDTH / 5),
			measurable_desc.animate.arrange(RIGHT).move_to(measurable_desc).set_x(- STAGE_WIDTH / 5).set_color(BLUE),
			FadeOut(left_title[0:3], scale = 0.1),
			FadeOut(right_title[0:3], scale = 0.1),
		)

		nonmeasurable_title = Text("不可测集", color = LIGHT_PINK).match_y(measurable_title).set_x(STAGE_WIDTH / 5)
		nonmeasurable_desc = Text("内测度 ≠ 外测度", color = LIGHT_PINK).match_y(measurable_desc).match_x(nonmeasurable_title)
		self.play(FadeIn(nonmeasurable_title, nonmeasurable_desc, shift = RIGHT))

		nonmeasurable_jpg = Text("不可测集.jpg").scale_to_fit_width(right_rcp.width - LARGE_BUFF).match_x(nonmeasurable_title)
		nonmeasurable_rect = RoundedRectangle(0.1, stroke_width = 6, width = right_rcp.width, height = right_rcp.height - MED_LARGE_BUFF, color = ORANGE).move_to(nonmeasurable_jpg)
		self.play(FadeIn(nonmeasurable_jpg, scale = 0.1), Create(nonmeasurable_rect))

		nonmeasurable_group = VGroup(nonmeasurable_title, nonmeasurable_jpg, nonmeasurable_rect, nonmeasurable_desc)
		self.play(FadeOut(measurable_group, target_position = STAGE_LEFT), FadeOut(nonmeasurable_group, target_position = STAGE_RIGHT))


