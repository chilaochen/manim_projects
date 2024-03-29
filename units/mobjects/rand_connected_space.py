from manim import *
import random

class rand_connected_space(VMobject):
	default_path_config = {
		"stroke_width" : 6,
		"stroke_color" : ORANGE,
	}

	default_square_config = {
		"fill_color" : BLUE,
		"fill_opacity" : 1,
		"stroke_width" : 2,
		"stroke_color" : YELLOW,
	}

	def __init__(self, v_num = 4, h_num = 6, path_config = None, square_config = None, **kwargs):
		super().__init__(**kwargs)

		self.v_num = v_num
		self.h_num = h_num
		self.path_config = path_config or rand_connected_space.default_path_config
		self.square_config = square_config or rand_connected_space.default_square_config

		self.generate_squares()
		self.generate_path()

	def generate_squares(self):
		count = self.v_num * self.h_num
		squares = VGroup(*[Square(1, **self.square_config) for _ in range(count)])
		squares.arrange_in_grid(self.v_num, buff = 0)

		self.inner_squares = VGroup(VGroup())
		self.edge_squares = VGroup()
		self.add(self.inner_squares, self.edge_squares)

		for r in range(1, self.v_num - 1):
			for c in range(1, self.h_num - 1):
				idx = r * self.h_num + c
				s = squares[idx]
				self.inner_squares[0].add(s)

		idxs = [self.h_num - 1, 0, count - self.h_num, count - 1]
		shift = [-1, self.h_num, 1, -self.h_num]
		num = [self.h_num - 1, self.v_num - 1, self.h_num - 1, self.v_num - 1]
		for i in range(4): 
			s_group = VGroup()
			self.edge_squares.add(s_group)
			for k in range(num[i]):
				idx = idxs[i] + k * shift[i]
				s = squares[idx]
				s_group.add(s)

		self.squares = squares

	def generate_path(self):
		corner = [[DL, UL], [DR, DL], [UR, DR], [UL, UR]]
		points = []
		curve_idx = -1
		for i in range(len(self.edge_squares)):
			s_group = self.edge_squares[i]
			c0 = corner[i][0]
			c1 = corner[i][1]
			direction = (c0 - c1) / 2
			for square in s_group:
				p0 = square.get_corner(c0)
				p1 = square.get_corner(c1)

				r = random.random() * 0.8
				p = p0 * (r + 0.1) + p1 * (0.9 - r)
				points.append(p)

				square.direction = direction
				square.curve_idx = curve_idx
				square.curve_min = 0
				square.curve_max = 1
				curve_idx += 1
			s_group[0].direction = c0
		points.append(points[0])

		self.remove(self.edge_squares)
		edge_squares = VGroup()
		for g in self.edge_squares:
			edge_squares.add(*g)
		self.edge_squares = edge_squares
		self.add(self.edge_squares)

		self.path = VMobject(**self.path_config)
		self.path.set_points_smoothly(points)
		self.add(self.path)

	def start_checking(self):
		self.curve_data = list(self.path.get_curve_functions_with_lengths())

	def check_edge(self, auto_update = False):
		if not hasattr(self, "curve_data"):
			self.start_checking()

		inner_squares = VGroup()
		edge_squares = VGroup()

		for square in self.edge_squares:
			curve_data = self.curve_data[square.curve_idx]
			curve_func = curve_data[0]
			curve_length = curve_data[1]
			curve_min = square.curve_min
			curve_max = square.curve_max

			small_group = VGroup(*[square.copy() for _ in range(4)]).arrange_in_grid(2, buff = 0).scale(0.5).move_to(square)
			stroke_width = max(0.1, square.get_stroke_width() * 0.8)
			center = square.get_center()

			num = int(np.ceil((curve_length * (curve_max - curve_min) * 64))) + 1
			setp = (curve_max - curve_min) / (num - 1)
			curve_ranges = [[curve_max, curve_min] for _ in range(4)]
			for i in range(num):
				k = curve_min + i * setp
				shift = curve_func(k) - center
				idx = None
				if shift[0] > 0 and shift[1] > 0:
					idx = 1
				elif shift[0] > 0 and shift[1] < 0:
					idx = 3
				elif shift[0] < 0 and shift[1] > 0:
					idx = 0
				elif shift[0] < 0 and shift[1] < 0:
					idx = 2

				cr = curve_ranges[idx]
				cr[0] = min(k, cr[0])
				cr[1] = max(k, cr[1])
			
			p0 = curve_func(curve_min)
			p1 = curve_func(curve_max)
			pc = curve_func((curve_min + curve_max) / 2)
			vec = p0 - p1
			tangent = np.array([vec[1], -vec[0], vec[2]])
			if np.dot(tangent, square.direction) < 0:
				tangent = -tangent

			for i in range(4):
				cr = curve_ranges[i]
				small_square = small_group[i]
				small_square.set_stroke(width = stroke_width)
				small_square.parent = square
				small_square.direction = square.direction	
				if cr[0] < cr[1]:
					edge_squares.add(small_square)
					small_square.curve_idx = square.curve_idx
					small_square.curve_min = cr[0]
					small_square.curve_max = cr[1]
				else:
					small_center = small_square.get_center()
					if np.dot(tangent, small_center - pc) >= 0:
						inner_squares.add(small_square)

		if auto_update:
			self.update_squares(inner_squares, edge_squares)
		
		return inner_squares, edge_squares

	def update_squares(self, inner_squares, edge_squares):
		if len(inner_squares) > 0:
			self.inner_squares.add(inner_squares)
		
		if len(edge_squares) > 0:
			self.remove(self.edge_squares)
			self.edge_squares = edge_squares
			self.add(self.edge_squares)

		self.add(self.path)