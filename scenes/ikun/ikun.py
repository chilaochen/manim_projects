import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))
from manim import *
from units.zooming_scene import *
from units.fourier_drawer import *
import numpy as np

class ikun(ZommingScene):
	ikun_file = os.path.join("assert", "ikun", "ikun")

	changing_num = 10
	changing_time = 76
	max_vector_num = pow(2, changing_num - 1)
	transform_time = 2
	ball_size = 350 / 2160 * config.frame_height

	def setup(self):
		Text.set_default(font = "DFBuDingW12-GB", fill_color = "#9775fa")
		self.generate_drawer()

	def construct(self):
		self.play_opening()
		self.play_changing()
		self.play_gif()

	def play_opening(self):
		ball_file = os.path.join("assert", "ikun", "ball")

		head = Text("从前，有一只")
		tail = Text("它练习了两分半钟")
		points = Text("……").next_to(tail)
		title = VGroup(head, tail, points).scale_to_fit_height(1)
		ball = ImageMobject(ball_file).scale_to_fit_height(self.ball_size).next_to(head)

		w = config.frame_width / 2
		k = 2 * (ball.get_x() - w)**2 / config.frame_height
		path_func = lambda x : - (x - w)**2 / k + config.frame_height / 2
		x = w
		start = np.array((x, path_func(x), 0))
		ball_path = VMobject()
		ball_path.start_new_path(start)
		while x >= ball.get_x():
			ball_path.add_line_to(np.array((x, path_func(x), 0)))
			x = x - 0.1

		self.play(MoveAlongPath(ball, ball_path, run_time = 1), AddTextLetterByLetter(head, run_time = 2))

		tail.next_to(ball, DOWN, LARGE_BUFF)
		points.next_to(tail)

		self.play(Succession(AddTextLetterByLetter(tail), AddTextLetterByLetter(points)), FadeOut(head, run_time = 1), self.camera.frame.animate(rate_func = rate_functions.smooth, run_time = 2).move_to(ball))
		self.wait(0.5)
		self.play(Succession(FadeOut(points, run_time = 0.1), AddTextLetterByLetter(points, run_time = 0.5), FadeOut(points, run_time = 0.1)))

		circle = Circle(fill_color = "#fb8400", fill_opacity = 1).scale_to_fit_height(ball.height).move_to(ball)
		self.play(FadeOut(tail), FadeOut(ball), FadeIn(circle), run_time = 1.5)

		self.drawer.center()
		self.play(ReplacementTransform(circle, self.drawer.circles[0]),  self.camera.frame.animate.center(), run_time = 2)

	def play_changing(self):
		self.play(GrowArrow(self.drawer.vectors[0]))

		self.add(self.drawer)

		explain = [
			Text("加一点细节……").to_corner(UL),
			Text("再加一点细节……").to_corner(UL),
			Text("更多更多的细节……").to_corner(UL),
		]

		step_time = self.changing_time / sum(self.pick_precent)

		last_idx = None
		count = 0
		left_path = None
		right_path = None

		for idx, precent in zip(self.pick_idx, self.pick_precent):
			self.drawer.suspend_updating()

			if count > 0:
				cur_path = VMobject(**self.drawer.drawn_path_cfg).append_points(self.drawer.cur_drawn_path.points)
				self.drawer.remove(self.drawer.cur_drawn_path)

				edge = RIGHT if (count % 2 == 0) else LEFT
				move_path = left_path if np.array_equal(edge, LEFT) else right_path

				target_path = cur_path.copy().to_edge(edge, LARGE_BUFF).set_stroke(width = 1).scale(0.6)

				mid_anime = None
				if move_path == None:
					move_path = cur_path
				else:
					mid_anime = FadeOut(cur_path)

				move_anime = ReplacementTransform(move_path, target_path)

				transform_group = []

				vectors = [vec.copy() for vec in self.drawer.vectors[0 : last_idx + 1]]
				circles = [cle.copy() for cle in self.drawer.circles[0 : last_idx + 1]]

				for i in range(0, last_idx + 1):
					transform_group.append(ReplacementTransform(self.drawer.vectors[i].copy(), self.drawer.vectors[i + last_idx + 1]))
					transform_group.append(ReplacementTransform(self.drawer.circles[i].copy(), self.drawer.circles[i + last_idx + 1]))

				if mid_anime != None:
					self.play(mid_anime)

				if count <= len(explain):
					self.play(AddTextLetterByLetter(explain[count - 1]))
					self.play(move_anime)

					transform_group.append(FadeOut(explain[count - 1], run_time = self.transform_time))
				else:
					move_anime.run_time = self.transform_time
					transform_group.append(move_anime)

				self.play(*transform_group, run_time = self.transform_time, rate_func = rate_functions.smooth)

				if np.array_equal(edge, LEFT):
					left_path = target_path
				else:
					right_path = target_path

			self.drawer.reset()
			self.drawer.period = step_time * precent
			self.drawer.active_drawn_path(idx)
			self.drawer.resume_updating()
			self.wait_until(lambda : self.drawer.finshed)

			last_idx = idx
			count = count + 1

		self.drawer.suspend_updating()
		self.wait(1)
		self.add(self.drawn_path[-1])
		self.play(FadeOut(self.drawer))
		self.clear()

	def play_gif(self):
		mid_path = self.drawn_path[-1].copy()
		left_path = self.drawn_path[-2 - self.changing_num % 2].copy().to_edge(LEFT).scale(0.6)
		right_path = self.drawn_path[-3 + self.changing_num % 2].copy().to_edge(RIGHT).scale(0.6)

		for path in self.drawn_path:
			mid_target = path.copy()
			left_target = mid_target.copy().to_edge(LEFT).scale(0.6)
			right_target = mid_target.copy().to_edge(RIGHT).scale(0.6)

			anime_group = [
				ReplacementTransform(mid_path, mid_target),
				ReplacementTransform(left_path, left_target),
				ReplacementTransform(right_path, right_target),
			]

			self.play(*anime_group)
			mid_path = mid_target
			left_path = left_target
			right_path = right_target

		mid_target = mid_path.copy().to_edge(DOWN, 0)

		anime_group = [
			ReplacementTransform(mid_path, mid_target),
			ReplacementTransform(left_path, mid_target),
			ReplacementTransform(right_path, mid_target),
		]
		self.play(*anime_group)

	def generate_drawer(self):
		svg = SVGMobject(self.ikun_file, height = config.frame_height - 2, fill_opacity = 0, stroke_width = 0).family_members_with_points()[0]
		curves_and_lengths = tuple(svg.get_curve_functions_with_lengths())
		total_length = sum(length for _, length in curves_and_lengths)
		self.drawer = fourier_multi_drawer(svg, self.max_vector_num, int(total_length * config.pixel_height / config.frame_height))

		self.pick_idx = [pow(2, i) - 1 for i in range(0, self.changing_num)]
		self.pick_path = [self.drawer.all_drawn_path[idx] for idx in self.pick_idx]

		self.max_frame = 10 * config.frame_rate

		for p in range(0, self.max_frame + 1, 1):
			self.drawer.process = p / self.max_frame
			for path in self.pick_path:
				path.update()

		self.drawn_path = [VMobject(**self.drawer.drawn_path_cfg).append_points(path.points) for path in self.pick_path]

		self.precent_list = []
		for path in self.drawer.all_drawn_path:
			curves_and_lengths = tuple(path.get_curve_functions_with_lengths())
			path_length = sum(length for _, length in curves_and_lengths)
			precent = path_length / total_length
			self.precent_list.append(precent)

		self.pick_precent = [self.precent_list[idx] for idx in self.pick_idx]