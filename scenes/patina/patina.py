import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))

import random

from units import *
import img_ops
import tex_maker

class Patina(MultiZoomedScene):
	def setup(self):
		self.align_camera_with_stage()
		self.title_height = 0.4
		random.seed(42)

	def construct(self):
		self.next_section(skip_animations = False)
		self.overview()
		self.next_section(skip_animations = False)
		self.show_feature1()
		self.next_section(skip_animations = False)
		self.color_space()
		self.next_section(skip_animations = False)
		self.rgb_and_yuv()
		self.next_section(skip_animations = False)
		self.color_space_convert()
		self.next_section(skip_animations = False)
		self.skia_bug()
		self.next_section(skip_animations = False)
		self.jpeg_quailty()
		self.next_section(skip_animations = False)
		self.show_feature2()
		self.next_section(skip_animations = False)
		self.jpeg_dct()
		self.next_section(skip_animations = False)
		self.dct_base_img()
		self.next_section(skip_animations = False)
		self.dct_example()
		self.next_section(skip_animations = False)
		self.quantization()

	def overview(self):
		image = ImageMobject(os.path.join("assert", "jpeg", "image.png")).scale_to_fit_width(2).move_to(LEFT * STAGE_WIDTH / 4)
		website = ImageMobject(os.path.join("assert", "mass", "landing-page.png")).scale_to_fit_width(3).move_to(RIGHT * STAGE_WIDTH / 4)
		arrow = Arrow(LEFT * 2, RIGHT * 2)
		compress = ImageMobject(os.path.join("assert", "jpeg", "compressed.png")).scale_to_fit_width(1).next_to(arrow, UP)

		self.upload = Group(image, arrow, website, compress)

		self.jpg = ImageMobject(os.path.join("assert", "jpeg", "jpg-file.png")).scale_to_fit_width(2)
		title = Text("JPEG").scale_to_fit_width(self.jpg.width).next_to(arrow, DOWN)
		self.jpg.next_to(title, DOWN, SMALL_BUFF)

		self.jpeg = Group(title, self.jpg)

		self.play(FadeIn(image, scale = 0.5))
		self.play(GrowArrow(arrow), FadeIn(website, scale = 0.5))
		self.play(FadeIn(compress, target_position = arrow))

		self.play(Write(title))
		self.play(FadeIn(self.jpg, target_position = title))
		self.play(Circumscribe(title, fade_out = True))

		self.play(self.jpeg.animate.center().scale(2), FadeOut(self.upload, target_position = UP * STAGE_HEIGHT / 2))

		note = Text("有损压缩").scale_to_fit_width(self.jpg.width * 0.8).next_to(self.jpeg, DOWN, SMALL_BUFF)
		
		self.eye = ImageMobject(os.path.join("assert", "mass", "eye.png")).scale_to_fit_width(2).to_stage_edge(LEFT, LARGE_BUFF)

		self.feature1 = Text("特点一")
		self.feature2 = Text("特点二")
		self.eye2jpg1 = LabeledArrow(self.feature1, label_frame = False, start = self.eye.get_right(), end = self.jpeg.get_left() + UP * 1.2)
		self.eye2jpg2 = LabeledArrow(self.feature2, label_frame = False, start = self.eye.get_right(), end = self.jpeg.get_left() + DOWN * 1.2)

		self.eye_area = Group(self.eye, self.eye2jpg1, self.eye2jpg2)

		self.step1 = Text("色彩空间转换")
		self.step2 = Text("离散余弦变换")
		jpg2green = LabeledArrow(self.step1, label_frame = False, start = self.jpeg.get_right() + UP * 1.2, end = self.jpeg.get_right() + UP * 1.2 + RIGHT * 4)
		jpg2blurry = LabeledArrow(self.step2, label_frame = False, start = self.jpeg.get_right() + DOWN * 1.2, end = self.jpeg.get_right() + DOWN * 1.2 + RIGHT * 4)

		eye_scale = 0.8
		eye_space = self.eye_area.width * (1 - eye_scale)

		self.play(ReplacementTransform(title.copy(), note))
		self.jpeg.add(note)

		self.play(FadeIn(self.eye, target_position = LEFT * STAGE_WIDTH / 2), scale = 0.5)
		self.play(GrowArrow(self.eye2jpg1), GrowArrow(self.eye2jpg2))
		self.play(ReplacementTransform(self.eye2jpg1.copy(), jpg2green))
		self.play(ReplacementTransform(self.eye2jpg2.copy(), jpg2blurry))

		self.play(
			self.eye_area.animate.scale(eye_scale).to_stage_edge(LEFT, LARGE_BUFF),
			self.jpeg.animate.scale(0.5).center().shift((self.jpeg.width / 4 + eye_space) * LEFT), Group(jpg2green, jpg2blurry).animate.shift((self.jpeg.width / 2 + eye_space) * LEFT)
		)

		green_tmp = self.jpeg[1].copy().move_to(jpg2green).set_z_index(-1)
		blurry_tmp = self.jpeg[1].copy().move_to(jpg2blurry).set_z_index(-1)
		green = ImageMobject(img_ops.turn_green(green_tmp.get_pixel_array(), 60), resampling_algorithm = 0).scale_to_fit_height(2.5).next_to(jpg2green).shift(UP / 2)
		blurry = ImageMobject(img_ops.box_blurry(blurry_tmp.get_pixel_array(), 20), resampling_algorithm = 0).scale_to_fit_height(2.5).next_to(jpg2blurry).shift(DOWN / 2)

		self.ops_area = Group(jpg2green, jpg2blurry, green, blurry)

		self.play(FadeIn(green_tmp, target_position = self.jpeg[1]), FadeIn(blurry_tmp, target_position = self.jpeg[1]))
		self.play(ReplacementTransform(green_tmp, green), ReplacementTransform(blurry_tmp, blurry))

	def show_feature1(self):
		target_eye = self.eye.copy().scale_to_fit_height(self.title_height).to_stage_corner(UL)
		self.title_txt = Text("对亮度变化更敏感").match_height(target_eye).next_to(target_eye)
		self.title_img = self.eye
		self.title = Group(self.title_img, self.title_txt)

		self.play(Circumscribe(self.feature1, fade_out = True))
		self.play(
			self.eye.animate.become(target_eye),
			ReplacementTransform(self.feature1.copy(), self.title_txt),
			FadeOut(Group(self.eye2jpg1, self.eye2jpg2, self.jpeg, self.ops_area))
		)

		self.title_underline = Underline(self.title)
		self.play(Create(self.title_underline))

		luma = Text("亮度变化").scale_to_fit_height(STAGE_HEIGHT / 4).shift(UP * STAGE_HEIGHT / 6)
		chroma = Text("颜色变化").scale_to_fit_height(STAGE_HEIGHT / 4).shift(DOWN * STAGE_HEIGHT / 6).set_fill(ManimColor([*img_ops.yuv2rgb(128, 255, 255)]))

		luma.count = 0
		def luma_updater(m, dt):
			m.count = m.count + dt
			grey = int((1 + np.cos(m.count * PI)) * 255 / 2)
			m.set_fill(ManimColor([grey, grey, grey]), 1)

		chroma.count = 0
		def chroma_updater(m, dt):
			m.count = m.count + dt
			u = int((1 + np.cos(m.count * PI * 0.5)) * 255 / 2)
			v = int((1 + np.cos(m.count * PI * 0.7)) * 255 / 2)
			m.set_fill(ManimColor([*img_ops.yuv2rgb(128, u, v)]), 1)

		self.play(Create(luma), Create(chroma))
		luma.add_updater(luma_updater)
		chroma.add_updater(chroma_updater)
		self.wait(5)

		luma.clear_updaters(True)
		chroma.clear_updaters(True)
		self.play(FadeOut(luma), FadeOut(chroma))

		self.duck = ImageMobject(os.path.join("assert", "mass", "duck.jpg")).scale_to_fit_width(STAGE_WIDTH / 5)
		y_array = img_ops.grey_scale(self.duck.get_pixel_array())
		uv_array = img_ops.uv_scale(self.duck.get_pixel_array())
		self.duck_y = ImageMobject(y_array).match_width(self.duck).shift(LEFT * STAGE_WIDTH * 0.3)
		self.duck_uv = ImageMobject(uv_array).match_width(self.duck).shift(RIGHT * STAGE_WIDTH * 0.3)
		y_title = Text("亮度信号", color = LIGHTER_GREY).scale_to_fit_height(0.4).next_to(self.duck_y, DOWN)
		uv_title = Text("色度信号").scale_to_fit_height(0.4).set_fill([GREEN, RED], 1).next_to(self.duck_uv, DOWN)
		self.play(FadeIn(self.duck))
		self.play(ReplacementTransform(self.duck.copy(), self.duck_y))
		self.play(FadeIn(y_title, target_position = self.duck_y.get_bottom()))
		self.play(ReplacementTransform(self.duck.copy(), self.duck_uv))
		self.play(FadeIn(uv_title, target_position = self.duck_uv.get_bottom()))
		self.duck_y.add(y_title)
		self.duck_uv.add(uv_title)

	def color_space(self):
		jpg = self.jpg.copy().scale_to_fit_height(self.title_height).to_stage_corner(UL)
		txt = Text("色彩空间转换").match_height(jpg).next_to(jpg)
		underline = Underline(Group(jpg, txt))

		self.play(
			FadeOut(self.title_img), FadeIn(jpg), 
			ReplacementTransform(self.title_txt, txt), 
			ReplacementTransform(self.title_underline, underline),
			FadeOut(Group(self.duck_y, self.duck_uv)), 
		)

		self.title_img = jpg
		self.title_txt = txt
		self.title_underline = underline

		self.title = Group(self.title_img, self.title_txt, self.title_underline)
		self.add_foreground_mobject(self.title)

		duck_array = self.duck.get_pixel_array()
		img_height, img_width = duck_array.shape[:2]
		max_unit_pixel = img_height / self.duck.height
		self.min_unit_pixel = 2 / 3

		min_factor = 5
		max_factor = max_unit_pixel / self.min_unit_pixel
		display_width = int(STAGE_WIDTH / 2 + 1)
		display_height = int(STAGE_HEIGHT - 2)
		duck_camera, duck_image = self.add_zooming(self.duck.get_center(), display_width, display_height, display_center = RIGHT * 2  , factor = min_factor)

		self.play(self.generate_camera_animation(duck_camera))
		self.play(Group(self.duck, duck_camera.frame).animate.to_stage_edge(LEFT), self.generate_image_animation(duck_image))
		self.activate_zooming(duck_camera, False)

		self.zoom_rect = duck_camera.frame.copy()
		self.duck_zoom = ImageMobject(np.zeros((1,1,3), np.uint8)).set_resampling_algorithm(0).move_to(duck_image)
		self.add(self.zoom_rect, self.duck_zoom)
		self.remove(duck_camera.frame, duck_image)

		self.image_factor = 2
		self.zoom_camera, self.zoom_image = self.add_zooming(self.duck_zoom.get_center(), display_width, display_height, display_center = self.duck_zoom.get_center() , factor = self.image_factor)
		self.zoom_image.set_resampling_algorithm(0)
		self.activate_zooming(self.zoom_camera, False)

		cur_factor = ValueTracker(min_factor)
		def zoom_updater(dt):
			self.zoom_rect.scale_to_fit_height(display_height / cur_factor.get_value())

			cur_uint_pixel = max_unit_pixel / cur_factor.get_value()
			v_pixel = np.ceil(cur_uint_pixel * display_height)
			h_pixel = np.ceil(cur_uint_pixel * display_width)
			space_v = int(img_height - v_pixel) >> 1
			space_h= int(img_width - h_pixel) >> 1
			self.duck_zoom.pixel_array = duck_array[space_v : -space_v, space_h : -space_h, :]
			h, w = self.duck_zoom.pixel_array.shape[:2]
			self.duck_zoom.stretch_to_fit_height(h / cur_uint_pixel / self.image_factor)
			self.duck_zoom.stretch_to_fit_width(w / cur_uint_pixel / self.image_factor)

		self.add_updater(zoom_updater)
		self.play(cur_factor.animate(rate_func = rate_functions.ease_in_out_sine).set_value(max_factor), run_time = 3)
		cur_factor.set_value(max_factor)
		self.update_self(0)
		self.remove_updater(zoom_updater)
		
	def rgb_and_yuv(self):
		zoom_pixel = self.duck_zoom.get_pixel_array()
		zoom_height = zoom_pixel.shape[0]
		zoom_width = zoom_pixel.shape[1]
		zoom_size = zoom_width * zoom_height

		cell_size = 1 / self.min_unit_pixel / self.image_factor
		txt_height = cell_size / 6
		grid_group = VGroup(*[Rectangle(width = cell_size, height = cell_size, stroke_width = 0.3) for _ in range(zoom_size)])
		grid_group.arrange_in_grid(rows = zoom_pixel.shape[0], buff = 0).align_to(self.duck_zoom, UL)

		for x in range(zoom_height):
			for y in range(zoom_width):
				color = zoom_pixel[x][y]
				cell = grid_group[x * zoom_width + y]
				cell.r = Text("R: %03d"%color[0], color = ManimColor("#FF0000")).scale_to_fit_height(txt_height)
				cell.g = Text("G: %03d"%color[1], color = ManimColor("#00FF00")).scale_to_fit_height(txt_height)
				cell.b = Text("B: %03d"%color[2], color = ManimColor("#0000FF")).scale_to_fit_height(txt_height)
				Group(cell.r, cell.g, cell.b).arrange(DOWN, SMALL_BUFF).move_to(cell)
				cell.add(cell.r, cell.g, cell.b)

		self.play(LaggedStart(*[FadeIn(obj) for obj in grid_group], lag_ratio = 0.12))

		self.focus_image = ImageMobject(zoom_pixel.copy()).set_resampling_algorithm(0).replace(self.zoom_image)
		grid_group.scale(self.image_factor).set_z_index(1)

		tr_group = Group()
		tg_group = Group()
		tb_group = Group()
		txt_group = Group(tr_group, tg_group, tb_group)

		for cell in grid_group:
			tr_group.add(cell.r.copy())
			tg_group.add(cell.g.copy())
			tb_group.add(cell.b.copy())
			cell.remove(cell.r, cell.g, cell.b)
			cell.set_stroke(width = 0.5)

		self.remove(self.zoom_image, self.zoom_camera.frame, self.duck_zoom)
		self.add(self.focus_image, txt_group)

		split_scale = 0.4
		self.play(
			Group(grid_group, self.focus_image).animate.scale(split_scale).center(),
			txt_group.animate.arrange(DOWN, 1.6).scale(split_scale).to_stage_edge(RIGHT),
		)

		cell_size = 1 / self.min_unit_pixel * split_scale
		color_group = Group()
		for group in txt_group:
			rect_group = Group()
			for txt in group:
				rect = Rectangle(width = cell_size, height = cell_size, stroke_width = 0.5, fill_opacity = 1).move_to(txt)
				rect_group.add(rect)
			color_group.add(rect_group)

		split_color = img_ops.split_rgb
		def color_group_updater(m, dt):
			for i in range(zoom_size):
				color = self.focus_image.get_pixel_array()[int(i / zoom_width)][int(i % zoom_width)][:3]
				c, _ = split_color(color)
				for j in range(3):
					m[j][i].set_fill(ManimColor(c[j]))

		color_group_updater(color_group, 0)

		self.rgb_img = ImageMobject(os.path.join("assert", "jpeg", "rgb.png")).scale_to_fit_height(2).next_to(self.focus_image, DOWN)
		color_brace = Brace(color_group.copy().scale(2 / 3), LEFT).move_to((self.focus_image.get_center() + color_group.get_center()) / 2)
		self.play(FadeOut(txt_group), FadeIn(color_group), FadeIn(color_brace), FadeIn(self.rgb_img))
		color_group.add_updater(color_group_updater)

		pick_idx = 0
		pick_x = int(pick_idx / zoom_width)
		pick_y = int(pick_idx % zoom_width)
		split_group = Group(Rectangle(stroke_width = 0.8).replace(grid_group[pick_idx], stretch = True).scale(1.1))
		val_group = Group()

		for i in range(3):
			split_group.add(Rectangle(stroke_width = 0.8).replace(color_group[i][pick_idx], stretch = True).scale(1.1))
			val_group.add(Integer(888).scale_to_fit_width(0.6))

		arrow = Arrow(start = self.zoom_rect.get_center(), end = self.focus_image.get_left())
		self.play(*[Create(rect) for rect in split_group], GrowArrow(arrow))
		arrow.add_updater(lambda m, dt: m.put_start_and_end_on(self.zoom_rect.get_center(), self.focus_image.get_left()))

		def split_updater(dt):
			color = self.focus_image.get_pixel_array()[pick_x][pick_y][:3]
			split_group[0].set_fill(ManimColor(color), 1)
			rgb, scales = split_color(color)
			for i in range(3):
				split_group[i+1].set_fill(ManimColor(rgb[i]), 1)
				val_group[i].set_value(scales[i])

		split_updater(0)

		target_group = split_group.copy()
		for rect in target_group:
			rect.scale_to_fit_height(0.8)
		target_group.arrange(RIGHT, 0.5).next_to(self.focus_image, UP, LARGE_BUFF)

		self.play(*[split_group[i].animate.become(target_group[i]) for i in range(4)])

		for i in range(3):
			val_group[i].next_to(split_group[i+1], DOWN)

		simbol_group = Group(Text("="), Text("+"), Text("+"))
		name_group = Group(Text("R"), Text("G"), Text("B"))
		for i in range(3):
			txt = simbol_group[i]
			txt.scale_to_fit_width(0.25)
			txt.move_to((split_group[i].get_center() + split_group[i+1].get_center()) / 2)
			name_group[i].scale_to_fit_height(0.4).move_to(split_group[i+1])

		self.play(FadeIn(simbol_group), FadeIn(name_group), *[FadeIn(val_group[i], target_position = split_group[i+1]) for i in range(3)])
		self.add_updater(split_updater)

		zoom_center_x = ValueTracker(0)
		zoom_center_y = ValueTracker(0)

		def zoom_rect_updater(m, dt):
			x = self.duck.get_center()[0] + zoom_center_x.get_value() * self.duck.width
			y = self.duck.get_center()[1] + zoom_center_y.get_value() * self.duck.height
			m.move_to([x, y, 0])

		self.zoom_rect.add_updater(zoom_rect_updater)

		duck_pixel = self.duck.get_pixel_array()
		duck_height = duck_pixel.shape[0]
		duck_width = duck_pixel.shape[1]
		def zoom_image_updater(m, dt):
			x = round(duck_height * (zoom_center_y.get_value() + 0.5))
			y = round(duck_width * (zoom_center_x.get_value() + 0.5))
			m.pixel_array = duck_pixel[int(x - zoom_height / 2) : int(x + zoom_height / 2), int(y - zoom_width / 2) : int(y + zoom_width / 2)]

		self.focus_image.add_updater(zoom_image_updater)

		def random_move_zoom_center(count = 1, run_time = 1, wait_time = 0.5):
			for _ in range(count):
				self.play(zoom_center_x.animate.set_value(random.random() * 0.8 - 0.4), zoom_center_y.animate.set_value(random.random() * 0.8 - 0.4), rate_func = rate_functions.ease_in_out_cubic, run_time = run_time)
				self.wait(wait_time)

		random_move_zoom_center(3)

		y_img = ImageMobject(np.uint8([[[i, i, i]] for i in range(255, -1, -1)])).stretch_to_fit_height(2).stretch_to_fit_width(0.5)
		uv000_img = ImageMobject(np.uint8([[[*img_ops.yuv2rgb(0, u, 255 - v)] for u in range(256)] for v in range(256)]))
		uv128_img = ImageMobject(np.uint8([[[*img_ops.yuv2rgb(128, u, 255 - v)] for u in range(256)] for v in range(256)]))
		uv255_img = ImageMobject(np.uint8([[[*img_ops.yuv2rgb(255, u, 255 - v)] for u in range(256)] for v in range(256)]))
		uv_img = uv000_img.copy().scale_to_fit_height(2)
		self.yuv_area = Group(y_img, uv_img).arrange(RIGHT, 0.1).next_to(self.focus_image, DOWN).align_to(split_group, RIGHT)
		self.yuv_area.add(SurroundingRectangle(y_img, color = WHITE, stroke_width = 1, buff = 0))
		self.yuv_area.add(SurroundingRectangle(uv_img, color = WHITE, stroke_width = 1, buff = 0))
		uv000_img.replace(uv_img)
		uv128_img.replace(uv_img)
		uv255_img.replace(uv_img)

		self.play(self.rgb_img.animate.next_to(self.yuv_area, LEFT), FadeIn(self.yuv_area, scale = 0))

		y_txt = Text("Y").scale_to_fit_width(0.3).move_to(y_img)
		uv_ax = Axes([-4, 4, 1], [-4, 4, 1], x_length = 2, y_length = 2, tips=False).move_to(uv_img)
		uv_ax.add(uv_ax.get_x_axis_label("U").align_to(uv_ax, RIGHT).scale(0.7), uv_ax.get_y_axis_label("V").align_to(uv_ax, UP).scale(0.7))

		self.play(Circumscribe(y_img, fade_out = True), FadeIn(y_txt))
		self.play(Circumscribe(uv_img, fade_out = True), FadeIn(uv_ax))
		self.yuv_area.add(y_txt, uv_ax)
		
		y_rect = Rectangle(width = 0.6, height = 0.15, stroke_width = 1.5).move_to([y_img.get_x(), y_img.get_bottom()[1], 0])
		self.yuv_area.add(y_rect)
		self.play(Create(y_rect))
		self.add(self.yuv_area)

		y_val = ValueTracker(0)
		def yuv_updater(m, dt):
			y_rect.move_to([y_img.get_x(), y_img.get_bottom()[1] + y_val.get_value() * y_img.height, 0])

		self.yuv_area.add_updater(yuv_updater)
		self.play(y_val.animate.set_value(0.5), uv_img.animate.become(uv128_img))
		self.play(y_val.animate.set_value(1), uv_img.animate.become(uv255_img))
		self.play(y_val.animate.set_value(0.5), uv_img.animate.become(uv128_img))
		
		yuv_group = Group(Text("Y"), Text("U"), Text("V"))
		for i in range(3):
			yuv_group[i].replace(name_group[i])

		pick_color = self.focus_image.get_pixel_array()[pick_x][pick_y][:3]
		rgb, yuv = img_ops.split_yuv(pick_color)
		group_color = np.zeros((3, zoom_size, 3), np.uint8)
		color_group_animate = []
		for i in range(zoom_size):
			color = self.focus_image.get_pixel_array()[int(i / zoom_width)][int(i % zoom_width)][:3]
			c, _ = img_ops.split_yuv(color)
			for j in range(3):
				color_group_animate.append(color_group[j][i].animate.set_fill(ManimColor(c[j])))

		self.remove_updater(split_updater)
		color_group.remove_updater(color_group_updater)

		self.play(
			FadeOut(self.rgb_img, target_position = self.rgb_img.get_left()), 
			self.yuv_area.animate.set_x(self.focus_image.get_x()),
			*[name_group[i].animate.become(yuv_group[i]) for i in range(3)],
			*[split_group[i+1].animate.set_fill(ManimColor(rgb[i]), 1) for i in range(3)],
			*[val_group[i].animate.set_value(yuv[i]) for i in range(3)],
			*color_group_animate,
		)

		self.add_updater(split_updater)
		color_group.add_updater(color_group_updater)

		split_color = img_ops.split_yuv
		random_move_zoom_center(3)

		yuv_target = self.yuv_area.copy()
		Group(self.rgb_img, yuv_target).arrange(RIGHT, LARGE_BUFF).scale(1.25).center()

		self.remove(self.yuv_area, self.title)
		mobjects = self.mobjects
		self.add(self.yuv_area, self.title)

		self.focus_image.remove_updater(zoom_image_updater)
		self.remove_updater(split_updater)
		self.play(*[FadeOut(obj) for obj in mobjects], self.yuv_area.animate.replace(yuv_target), FadeIn(self.rgb_img))

	def color_space_convert(self):
		rgb2yuv_arrow = Arrow(self.rgb_img.get_corner(UR), self.yuv_area.get_corner(UL))
		yuv2rgb_arrow = Arrow(self.yuv_area.get_corner(DL), self.rgb_img.get_corner(DR))

		self.play(GrowArrow(rgb2yuv_arrow), GrowArrow(yuv2rgb_arrow))

		rgb2yuv_arrow.add_updater(lambda m, dt: m.put_start_and_end_on(self.rgb_img.get_corner(UR), self.yuv_area.get_corner(UL)))
		yuv2rgb_arrow.add_updater(lambda m, dt: m.put_start_and_end_on(self.yuv_area.get_corner(DL), self.rgb_img.get_corner(DR)))

		self.play(self.rgb_img.animate.to_stage_edge(LEFT), self.yuv_area.animate.to_stage_edge(RIGHT))

		rgb2yuv_tex = MathTex(tex_maker.rgb2yuv_str, tex_to_color_map = tex_maker.color_map).scale_to_fit_height(1)
		yuv2rgb_tex = MathTex(tex_maker.yuv2rgb_str, tex_to_color_map = tex_maker.color_map).scale_to_fit_height(1)

		tex_group = Group(rgb2yuv_tex, yuv2rgb_tex).arrange(DOWN).match_width(rgb2yuv_arrow)
		rgb2yuv_tex.next_to(rgb2yuv_arrow, UP)
		yuv2rgb_tex.next_to(yuv2rgb_arrow, DOWN)

		self.play(LaggedStart(Write(rgb2yuv_tex), Write(yuv2rgb_tex), lag_ratio = 0.5, run_time = 3))

		total_convert = 5
		def make_random_rgb_val():
			init_val = [random.randint(10, 255) for _ in range(3)]
			convert_val = [init_val]
			for i in range(total_convert):
				convert_val.append([*img_ops.yuv2rgb(*img_ops.rgb2yuv(*convert_val[i]))])
			return convert_val

		rgb_val = make_random_rgb_val()

		val_font_size = 72
		convert_table = MobjectTable(
			[[Integer(rgb_val[i][j], font_size = val_font_size, color = tex_maker.color_map["RGB"[j]]) for i in range(total_convert + 1)] for j in range(3)],
			col_labels = [Integer(i, font_size = val_font_size) for i in range(total_convert + 1)],
			row_labels = [Text(c, color = tex_maker.color_map[c], font_size = 48) for c in "RGB"],
			top_left_entry = Text("转换次数", font_size = 48),
		)

		convert_table.move_to(tex_group).scale_to_fit_height((rgb2yuv_arrow.get_bottom() - yuv2rgb_arrow.get_top())[1])
		convert_table.get_col_labels().set_opacity(0)
		convert_table.get_entries_without_labels().set_opacity(0)
		convert_table.get_vertical_lines()[0].set_color(PURPLE)
		convert_table.get_horizontal_lines()[0].set_color(PURPLE)
		for line in convert_table.get_vertical_lines()[1:], convert_table.get_horizontal_lines()[1:]:
			line.set_stroke(width = 0.5)

		self.play(convert_table.create(0.5))

		first_col = convert_table.get_columns()[1]
		surround_rect = SurroundingRectangle(first_col)
		self.play(first_col.animate.set_opacity(1), Create(surround_rect))

		rgb2yuv_tex.save_state()
		yuv2rgb_tex.save_state()

		first_col_copy = Group(*[first_col.copy() for _ in range(3)])
		yuv_lag_list = []
		for i in range(3):
			tex_objs = rgb2yuv_tex.get_parts_by_tex("RGB"[i])
			yuv_lag_list.append(AnimationGroup(tex_objs.animate.set_opacity(0), *[first_col_copy[j][i+1].animate.move_to(tex_objs[j]).align_to(tex_objs[j], LEFT) for j in range(len(tex_objs))]))
		
		yuv = [*img_ops.rgb2yuv(*rgb_val[0])]
		yuv_equals = yuv2rgb_tex.get_parts_by_tex("=").copy().next_to(tex_group).match_y(rgb2yuv_tex)
		yuv_result = Group(*[Integer(yuv[i], color = tex_maker.color_map["YUV"[i]]).next_to(yuv_equals[i]).match_height(first_col[1]) for i in range(3)])

		self.play(LaggedStart(*yuv_lag_list, lag_ratio = 0.3, run_time = 2))
		self.play(FadeIn(Group(yuv_equals, yuv_result), target_position = rgb2yuv_tex.get_right()))

		rgb_lag_list = []
		yuv_result_copy = Group(*[yuv_result.copy() for _ in range(3)])
		for i in range(3):
			tex_objs = yuv2rgb_tex.get_parts_by_tex("YUV"[i])
			rgb_lag_list.append(AnimationGroup(tex_objs.animate.set_opacity(0), *[yuv_result_copy[j][i].animate.move_to(tex_objs[j]).align_to(tex_objs[j], LEFT) for j in range(len(tex_objs))]))

		rgb = rgb_val[1]
		rgb_equals = yuv2rgb_tex.get_parts_by_tex("=").copy().next_to(tex_group).match_y(yuv2rgb_tex)
		rgb_result = Group(*[Integer(rgb[i], color = tex_maker.color_map["RGB"[i]]).next_to(rgb_equals[i]).match_height(first_col[1]) for i in range(3)])

		self.play(LaggedStart(*rgb_lag_list, lag_ratio = 0.3, run_time = 2))
		self.play(FadeIn(Group(rgb_equals, rgb_result), target_position = yuv2rgb_tex.get_right()))

		second_col_copy = convert_table.get_columns()[2].copy()
		rgb_result_copy = rgb_result.copy()

		self.play(
			surround_rect.animate.become(SurroundingRectangle(second_col_copy)),
			second_col_copy[0].animate.set_opacity(1),
			*[rgb_result_copy[i].animate.become(second_col_copy[i + 1].set_opacity(1)) for i in range(3)],
		)

		convert_table.get_columns()[2].set_opacity(1)
		self.remove(*rgb_result_copy, *second_col_copy)

		for i in range(total_convert - 1):
			cur_col = convert_table.get_columns()[i + 2].copy()
			next_col = convert_table.get_columns()[i + 3].copy().set_opacity(1)
			self.play(
				surround_rect.animate.become(SurroundingRectangle(next_col)),
				cur_col.animate.become(next_col),
			)
			self.remove(cur_col)
			convert_table.get_columns()[i + 3].set_opacity(1)

		self.play(
				FadeOut(surround_rect), FadeOut(first_col_copy),  
				FadeOut(yuv_equals), FadeOut(yuv_result), FadeOut(yuv_result_copy),
				FadeOut(rgb_equals), FadeOut(rgb_result),
				Restore(rgb2yuv_tex), Restore(yuv2rgb_tex),
			)

		for _ in range(3):
			rgb_val = make_random_rgb_val()
			self.play(LaggedStart(*[AnimationGroup(*[convert_table.get_entries_without_labels((r+1,c+1)).animate.set_value(rgb_val[c][r]).move_to(convert_table.get_cell((r+2,c+2))) for r in range(3)]) for c in range(total_convert + 1)], lag_ratio = 0.5, run_time = 2))
			self.wait()

		self.remove(self.title)
		mobjects = self.mobjects
		self.add_foreground_mobject(self.title)
		self.play(*[FadeOut(obj) for obj in mobjects])

	def skia_bug(self):
		skia = ImageMobject(os.path.join("assert", "logo", "skia")).scale_to_fit_width(STAGE_WIDTH / 3)
		bug = ImageMobject(os.path.join("assert", "mass", "bug")).scale_to_fit_width(1).align_to(skia, UR).shift(RIGHT * 0.3)
		google = ImageMobject(os.path.join("assert", "logo", "google")).scale_to_fit_width(STAGE_WIDTH / 4).next_to(skia, DOWN)
		self.play(FadeIn(skia, scale = 0))
		self.play(FadeIn(bug, scale = 5))

		skia_group = Group(skia, bug)
		target_group = Group(skia_group, google).copy().set_y(0)
		google = target_group[1]
		self.play(skia_group.animate.move_to(target_group[0]), FadeIn(google, target_position = skia))

		android = ImageMobject(os.path.join("assert", "logo", "android")).scale_to_fit_width(STAGE_WIDTH / 3).move_to(LEFT * STAGE_WIDTH / 4)
		chrome = ImageMobject(os.path.join("assert", "logo", "chrome")).scale_to_fit_height(STAGE_HEIGHT / 6).next_to(android, UP, 0.5)
		firefox = ImageMobject(os.path.join("assert", "logo", "firefox")).scale_to_fit_height(STAGE_HEIGHT / 6).next_to(android, DOWN, 0.5)
		self.play(Group(skia_group, google).animate.move_to(RIGHT * STAGE_WIDTH / 4), FadeIn(android, target_position = LEFT * 2))
		self.play(FadeIn(chrome, target_position = android.get_top()), FadeIn(firefox, target_position = android.get_bottom()))
		self.play(*[FadeOut(obj) for obj in (google, chrome, android, firefox)])

		bug = bug.copy().set_z_index(1)
		self.play(skia_group.animate.scale_to_fit_height(0.8).to_stage_corner(UR), bug.animate.center())

		code_height = (STAGE_HEIGHT * 0.6)
		code_config = {
			"font" : mono_font,
			"tab_width" : 4,
			"background_stroke_width" : 1,
			"background_stroke_color" : PURPLE,
			"insert_line_no" : False,
			"style" : "monokai",
			"background" : "window",
			"language" :"cpp",
		}

		skia_code = Code(
			os.path.join("assert", "code", "skia_bug.cpp"),
			**code_config
		).scale_to_fit_height(code_height)

		self.play(FadeIn(skia_code.background_mobject, scale = 0.3), bug.animate.match_height(skia_code).set_opacity(0))
		self.play(Write(skia_code.code))
		self.add(skia_code)

		bug_snippet = Group(*skia_code.code[5:12]).copy()
		bug_pos = bug_snippet.get_center()
		focus_rect = SurroundingRectangle(bug_snippet).shift(DOWN / 4)
		self.add(bug_snippet)
		self.play(Create(focus_rect))
		self.play(FadeOut(skia_code), FadeOut(bug))

		skia_rgb2yuv_tex = MathTex(tex_maker.skia_rgb2yuv_str, tex_to_color_map = tex_maker.color_map)
		skia_rgb2yuv_equ_tex = MathTex(tex_maker.skia_rgb2yuv_equ_str, tex_to_color_map = tex_maker.color_map)
		rgb2yuv_tex = MathTex(tex_maker.rgb2yuv_str, tex_to_color_map = tex_maker.color_map)
		Group(skia_rgb2yuv_tex, skia_rgb2yuv_equ_tex, rgb2yuv_tex).arrange(DOWN).scale_to_fit_width(STAGE_WIDTH * 0.8)
		skia_rgb2yuv_equ_tex.move_to(bug_snippet).align_to(DOWN * 0.3, UP)
		skia_rgb2yuv_tex.move_to(skia_rgb2yuv_equ_tex)
		rgb2yuv_tex.move_to(skia_rgb2yuv_equ_tex)

		self.play(
			bug_snippet.animate.align_to(UP * 0.3, DOWN),
			FadeIn(skia_rgb2yuv_tex, scale = 0.6, target_poisition = bug_snippet.get_top()),
			focus_rect.animate.become(SurroundingRectangle(skia_rgb2yuv_tex))
		)
		self.wait()

		self.play(focus_rect.animate.become(SurroundingRectangle(skia_rgb2yuv_tex.get_parts_by_tex("256"))))
		self.play(FadeOut(focus_rect))
		self.play(skia_rgb2yuv_tex.animate.become(skia_rgb2yuv_equ_tex))
		self.play(*[Circumscribe(obj, fade_out = True) for obj in skia_rgb2yuv_equ_tex.get_parts_by_tex("256")])
		self.play(skia_rgb2yuv_tex.animate.become(rgb2yuv_tex))
		self.wait()

		math_div_tex = MathTex(tex_maker.math_div_str)
		cs_div_tex = MathTex(tex_maker.cs_div_str)
		div_group = Group(math_div_tex, cs_div_tex).arrange(RIGHT, 2).scale_to_fit_height(STAGE_HEIGHT / 5).align_to(DOWN, UP)
		math_brace = BraceLabel(math_div_tex, "数学", LEFT, Text)
		cs_brace = BraceLabel(cs_div_tex, "C++", RIGHT, Text)
		div_group.add(math_brace, cs_brace)
		self.play(Write(math_div_tex), Write(cs_div_tex), Unwrite(skia_rgb2yuv_tex, run_time = 0.5))
		self.play(FadeIn(math_brace, target_position = math_div_tex.get_left()), FadeIn(cs_brace, target_position = cs_div_tex.get_right()))
		self.wait()

		self.yuv_area.move_to(div_group)
		self.duck.move_to(div_group)
		self.play(FadeOut(div_group), FadeIn(self.yuv_area))
		self.play(self.yuv_area.animate.shift(LEFT * STAGE_WIDTH / 4), FadeIn(self.duck, scale = 0))

		self.green_duck = ImageMobject(img_ops.turn_green(self.duck.get_pixel_array(), 100)).replace(self.duck).shift(RIGHT * STAGE_WIDTH / 4)
		self.play(ReplacementTransform(self.duck.copy(), self.green_duck))
		self.wait()
		self.play(bug_snippet.animate.set_y(0), *[FadeOut(obj) for obj in (self.yuv_area, self.duck, self.green_duck)])

		fix_code = Code(
			os.path.join("assert", "code", "skia_bug_fix.cpp"),
			**code_config
		).scale_to_fit_height(code_height)
		fix_snippet = fix_code.code[5:12].copy().shift(ORIGIN - bug_pos)

		self.play(
			*[Group(*bug_snippet[i][-12:]).animate.align_to(fix_snippet, RIGHT) for i in range(3)],
			*[Group(*bug_snippet[i][0:-12]).animate.align_to(fix_snippet, LEFT) for i in range(3)],
			*[Group(*bug_snippet[i+4]).animate.align_to(fix_snippet, LEFT) for i in range(3)],
		)
		self.play(*[FadeIn(Group(*fix_snippet[i][-18:-13])) for i in range(3)])
		self.add(bug_snippet)
		self.remove(bug_snippet)
		self.add(fix_snippet)
		self.play(fix_snippet.animate.shift(bug_pos))
		self.play(FadeIn(fix_code), FadeOut(skia_group[1], scale = 3))
		self.remove(fix_snippet)
		self.wait()

		fix_commit_img = ImageMobject(os.path.join("assert", "mass", "skia_fix_commit")).scale_to_fit_height(STAGE_HEIGHT * 0.8)
		img_size = fix_commit_img.get_pixel_array().shape[0:2]
		date_size = [45 / img_size[0] * fix_commit_img.height, 88 / img_size[1] * fix_commit_img.width]
		date_tl = [(390 / img_size[1] - 0.5) * fix_commit_img.width, (0.5 - 676 / img_size[0]) * fix_commit_img.height, 0]
		date_rect = Rectangle(stroke_color = RED, height = date_size[0], width = date_size[1]).align_to(date_tl, UL)
		date_rect.save_state()
		date_rect.replace(fix_commit_img, stretch = True).set_stroke(opacity = 0.3)
		line_start = [(40 / img_size[1] - 0.5) * fix_commit_img.width, (0.5 - 260 / img_size[0]) * fix_commit_img.height, 0]
		line_end = [(488 / img_size[1] - 0.5) * fix_commit_img.width, (0.5 - 260 / img_size[0]) * fix_commit_img.height, 0]
		fix_line = Line(line_start, line_end, color = RED)
		self.play(FadeIn(fix_commit_img, scale = 0.5), FadeOut(fix_code))
		self.play(date_rect.animate.restore())
		self.play(Create(fix_line))
		self.wait()

	def jpeg_quailty(self):
		self.play(*[FadeOut(obj) for obj in self.mobjects])

		self.jpeg.center().scale_to_fit_height(STAGE_HEIGHT / 2)
		self.play(FadeIn(self.jpeg, scale = 0.5))

		quality_label = Text("压缩质量").scale_to_fit_height(self.jpeg[2].height * 0.8)
		self.play(self.jpeg.animate.align_to(RIGHT, LEFT), FadeIn(quality_label, target_position = self.jpeg))

		max_quality = 100
		min_quality = 1
		self.dog = ImageMobject(os.path.join("assert", "ikun", "dog")).scale_to_fit_height(STAGE_HEIGHT * 0.6).to_stage_edge(LEFT, LARGE_BUFF)
		self.blurry_dog = ImageMobject(img_ops.jpeg_compress(self.dog.get_pixel_array(), max_quality)).match_height(self.dog).to_stage_edge(RIGHT, LARGE_BUFF)
		self.play(FadeIn(self.dog, scale = 0.5), quality_label.animate.center(), FadeOut(self.jpeg, target_position = self.jpeg.get_top()))

		blurry_arrow = Arrow(self.dog.get_right(), self.blurry_dog.get_left())
		quality_label_copy = quality_label.copy()
		quality_var = Variable(max_quality, quality_label, var_type = Integer).next_to(blurry_arrow, UP)
		target_pos = quality_var.get_left()
		quality_var.align_to(quality_label_copy, LEFT).match_y(quality_label_copy).set_opacity(0)

		self.play(
			GrowArrow(blurry_arrow),
			quality_var.animate.next_to(blurry_arrow, UP).set_opacity(1),
			quality_label_copy.animate.align_to(target_pos, LEFT).set_y(target_pos[1]),
			FadeIn(self.blurry_dog, scale = 0.5),
		)
		self.remove(quality_label_copy)

		blurry_pixel = {}
		for q in range(min_quality, max_quality + 1, 1):
			blurry_pixel[q] = img_ops.jpeg_compress(self.dog.get_pixel_array(), q)

		def blurry_updater(m):
			m.pixel_array = blurry_pixel[round(quality_var.tracker.get_value())]

		self.blurry_dog.add_updater(blurry_updater)
		self.play(quality_var.tracker.animate.set_value(min_quality), run_time = 3)

		times_var = Variable(1, Text("压缩次数").match_height(quality_label), var_type = Integer).next_to(blurry_arrow, DOWN).align_to(quality_var, LEFT)
		self.play(FadeIn(times_var, target_position = blurry_arrow))
		self.blurry_dog.remove_updater(blurry_updater)
		self.play(times_var.tracker.animate.set_value(999), run_time = 3)
		self.wait()

		random_blurry_pixel = []
		cur_pixel = self.dog.get_pixel_array().copy()

		random_quality = [i for i in range(1, 26)]
		for _ in range(4):
			random.shuffle(random_quality)
			for q in random_quality:
				cur_pixel = img_ops.jpeg_compress(cur_pixel, q)
				random_blurry_pixel.append([q, cur_pixel])

		times_var.tracker.set_value(1)
		quality_var.tracker.add_updater(lambda m: m.set_value(random_blurry_pixel[int(times_var.tracker.get_value()) - 1][0]))

		def random_blurry_updater(m):
			m.pixel_array = random_blurry_pixel[round(times_var.tracker.get_value()) - 1][1]

		self.blurry_dog.add_updater(random_blurry_updater)
		self.play(times_var.tracker.animate.set_value(len(random_blurry_pixel)), run_time = 3)
		self.blurry_dog.remove_updater(random_blurry_updater)
		self.wait()

	def show_feature2(self):
		# self.dog = ImageMobject(os.path.join("assert", "ikun", "dog")).scale_to_fit_height(STAGE_HEIGHT * 0.6).to_stage_edge(LEFT, LARGE_BUFF)
		self.remove(self.dog)
		mobjects = self.mobjects
		self.add(self.dog)
		self.play(self.dog.animate.center().scale(0.8), *[FadeOut(obj) for obj in mobjects])

		self.title_img = ImageMobject(os.path.join("assert", "mass", "eye")).scale_to_fit_height(self.title_height).to_stage_corner(UL)
		self.title_txt = Text("低频信号易于识别").match_height(self.title_img).next_to(self.title_img)
		self.title_underline = Underline(Group(self.title_img, self.title_txt))
		self.title = Group(self.title_img, self.title_txt, self.title_underline)

		dog_pixel = self.dog.get_pixel_array()
		y_pixel = img_ops.grey_scale(dog_pixel)
		uv_pixel = img_ops.uv_scale(dog_pixel)
		y_dog = ImageMobject(y_pixel).match_width(self.dog).to_stage_edge(LEFT, LARGE_BUFF)
		uv_dog = ImageMobject(uv_pixel).match_width(self.dog).to_stage_edge(RIGHT, LARGE_BUFF)
		luma = Text("亮度", color = LIGHTER_GREY).scale_to_fit_height(0.4).next_to(y_dog, DOWN)
		chroma = Text("颜色").set_fill([GREEN, PINK], 1).scale_to_fit_height(0.4).next_to(uv_dog, DOWN)
		self.play(
			ReplacementTransform(self.dog.copy(), y_dog), ReplacementTransform(self.dog.copy(), uv_dog),
			FadeIn(self.title_img, target_position = self.title_img.get_left()),
		)
		self.play(FadeIn(luma, target_position = y_dog.get_bottom()), FadeIn(chroma, target_position = uv_dog.get_bottom()))

		low_freq = Text("低频信号").move_to(luma).match_height(luma)
		high_freq = Text("高频信号").move_to(chroma).match_height(chroma)
		ratio = 0.005
		low_pixel, high_pixel = img_ops.split_freq(dog_pixel[:,:,:3], ratio)
		low_dog = ImageMobject(np.uint8(low_pixel), resampling_algorithm = 0).replace(y_dog)
		high_dog = ImageMobject(np.uint8(high_pixel), resampling_algorithm = 0).replace(uv_dog)
		low_dog.ratio = ratio
		self.remove(luma, y_dog)
		self.play(ReplacementTransform(luma, low_freq), ReplacementTransform(y_dog, low_dog))
		self.remove(chroma, uv_dog)
		self.play(ReplacementTransform(chroma, high_freq), ReplacementTransform(uv_dog, high_dog))
		self.play(FadeIn(self.title_txt, target_position = self.title_img.get_right()), Create(self.title_underline))
		self.add_foreground_mobject(self.title)

		arrow = Arrow(self.dog.get_left(), low_dog.get_right())
		ratio_str = str(int(1 / ratio))
		ratio_tex = MathTex(r"\frac{{1}}{{{0}}}".format(ratio_str), substrings_to_isolate = [ratio_str]).next_to(arrow, UP).scale_to_fit_height(1.3)
		self.play(Circumscribe(low_dog, fade_out = True))
		self.play(GrowArrow(arrow), FadeIn(ratio_tex, target_position = arrow))

		ratio = 0.1
		low_dog.ratio = ratio
		low_pixel, high_pixel = img_ops.split_freq_by_block(dog_pixel[:,:,:3], ratio)
		denominator = ratio_tex.get_part_by_tex(ratio_str)
		self.play(
			low_dog.animate.become(ImageMobject(np.uint8(low_pixel), resampling_algorithm = 0).replace(low_dog)),
			high_dog.animate.become(ImageMobject(np.uint8(high_pixel), resampling_algorithm = 0).replace(high_dog)),
			denominator.animate.become(MathTex(str(int(1 / ratio))).match_height(denominator).move_to(denominator)),
		)
		self.wait()

	def jpeg_dct(self):
		self.remove(self.title)
		mobjects = self.mobjects
		title_img = ImageMobject(os.path.join("assert", "jpeg", "jpg-file")).scale_to_fit_height(self.title_height).to_stage_corner(UL)
		full_title_txt = Text("离散余弦变换-DCT").match_height(title_img).next_to(title_img)
		sub_title_txt = Group(*full_title_txt.submobjects[:6])
		title_underline = Underline(Group(title_img, sub_title_txt))
		self.play(
			*[FadeOut(obj) for obj in mobjects],
			FadeOut(self.title_img), FadeIn(title_img),
			FadeOut(self.title_txt), FadeIn(sub_title_txt),
			self.title_underline.animate.become(title_underline),
		)

		dct_txt = sub_title_txt.copy()
		self.play(dct_txt.animate.scale_to_fit_width(STAGE_WIDTH / 2).center())
		
		dct_english = Text("Discrete Cosine Transform", t2c={"D":BLUE, "C":BLUE, "T":BLUE}).match_width(dct_txt).next_to(dct_txt, DOWN)
		self.play(FadeIn(dct_english, target_position = dct_txt.get_bottom()))

		dct_short = Group(*[dct_english.submobjects[idx] for idx in (0, 8, 14)])
		dct_english.remove(*[obj for obj in dct_short])
		self.play(
			FadeOut(dct_txt, dct_english), FadeIn(*full_title_txt.submobjects[6:]),
			title_underline.animate.become(Underline(Group(title_img, full_title_txt))),
			dct_short.animate.arrange(RIGHT, 0.05).center(),
		)

		self.title_img = title_img
		self.title_txt = full_title_txt
		self.title_underline = title_underline
		self.title = Group(self.title_img, self.title_txt, self.title_underline)
		self.add_foreground_mobject(self.title)

		cos_color = [ORANGE, MAROON, TEAL, LIGHT_PINK, GREEN]
		count = len(cos_color)
		left_ax = Axes(
			x_range = [0, count + 0.8],
			y_range = [-140, 160, 127],
			x_length = STAGE_WIDTH / 3.5,
			y_length = STAGE_HEIGHT * 0.6,
			axis_config = {"include_numbers" : True},
			y_axis_config = {"numbers_to_include" : [-128, 127]}
		).to_stage_edge(LEFT, MED_SMALL_BUFF)

		right_ax = left_ax.copy().to_stage_edge(RIGHT, MED_SMALL_BUFF)

		def make_rand_dct():
			rand_dct = [[(random.random() * 0.3 + 0.1) * random.choice([-1, 1]) * 255 for _ in range(count)]]
			rand_pt = img_ops.idct2(rand_dct)
			max_pt = np.max(np.abs(rand_pt))
			if max_pt > 127:
				rand_pt /= (max_pt / 127)
				rand_dct = img_ops.dct2(rand_pt)

			rand_param = [rand_dct[0][0] * np.sqrt(1 / count), *[k * np.sqrt(2 / count) for k in rand_dct[0][1:]]]
			rand_cos = [lambda x, i=i: rand_param[i] * np.cos(x * i / count * np.pi) for i in range(count)]
			rand_plot = VGroup(*[left_ax.plot(lambda x: rand_pt[0][int(x)], [i, i + 0.99], color = BLUE) for i in range(count)])
			rand_cos_plot = VGroup(*[right_ax.plot(lambda x: rand_param[i] * np.cos(x * i / count * np.pi), [0, count], color = cos_color[i]) for i in range(count)])
			rand_mtx = IntegerMatrix(rand_pt).match_width(rand_plot).next_to(left_ax, DOWN).match_x(rand_plot).set_fill(BLUE, 1)
			for i in range(count):
				rand_mtx.get_entries()[i].match_x(rand_plot[i])
			rand_pixel = img_ops.float2color(rand_pt[0])
			return rand_dct, rand_cos, rand_plot, rand_cos_plot, rand_mtx, rand_pixel
		
		rand_dct, rand_cos, rand_plot, rand_cos_plot, rand_mtx, rand_pixel= make_rand_dct()
		pixel_rects = VGroup(*[Rectangle(height = 1, width = 1, stroke_width = 2).set_fill(ManimColor([v]*3), 1) for v in rand_pixel]).arrange(RIGHT, 0).scale_to_fit_width(STAGE_WIDTH / 4)
		pixel_vals = VGroup(*[Integer(rand_pixel[i]).set_fill(BLUE, 1).match_x(pixel_rects[i]).scale_to_fit_height(pixel_rects.height * 0.3) for i in range(count)]).next_to(pixel_rects, DOWN)
		map_vals = rand_mtx.get_entries().copy()
		for i in range(count): map_vals[i].match_x(pixel_rects[i])
		map_vals.match_x(pixel_vals)
		map_arrow = Arrow(pixel_vals.get_bottom(), map_vals.get_top())
		self.play(FadeIn(pixel_rects, scale = 0, target_position = ORIGIN), dct_short.animate.next_to(pixel_rects, UP, MED_LARGE_BUFF))
		self.play(FadeIn(pixel_vals, target_position = pixel_rects))
		self.play(GrowArrow(map_arrow), FadeIn(map_vals, shift = DOWN * map_arrow.height))
		self.wait()

		for i in range(count):
			pixel_vals[i].add_updater(lambda m, i=i: m.match_x(pixel_rects[i]))

		self.play(map_vals.animate.become(rand_mtx.get_entries()), FadeOut(map_arrow), Create(left_ax))
		self.play(LaggedStart(*[ReplacementTransform(map_vals[i].copy(), rand_plot[i]) for i in range(count)], lag_ratio = 0.5, run_time = 2))
		self.play(FadeIn(rand_mtx))
		self.remove(*map_vals)

		dct_mtx = DecimalMatrix(rand_dct, element_to_mobject_config = {"num_decimal_places" : 1}).match_width(rand_mtx).match_y(rand_mtx).set_fill(RED, 1)
		self.play(Circumscribe(dct_short), FadeIn(dct_mtx, target_position = rand_mtx.get_right()))

		pixel_group = VGroup(pixel_rects, pixel_vals)
		dct_arrow = Arrow(left_ax.get_right(), right_ax.get_left()).next_to(dct_short, DOWN)
		self.play(pixel_group.animate.next_to(dct_mtx, UP))
		self.play(GrowArrow(dct_arrow), Create(right_ax))

		rand_tex_str = [tex_maker.dct_cos_str.format(round(rand_dct[0][i], 1), 1 if i == 0 else 2, count, i) for i in range(count)]
		rand_tex = VGroup(*[MathTex(rand_tex_str[i]) for i in range(count)]).match_x(right_ax).match_y(rand_mtx).scale_to_fit_height(rand_mtx.height * 1.4)
		for tex in rand_tex:
			tex[1].set_color(RED)
			tex[3].set_color(BLUE)

		animate_tex = rand_tex[0]
		dct_vals = dct_mtx.get_entries()
		focus_rect = SurroundingRectangle(dct_vals[0])
		self.play(Create(focus_rect))
		self.play(ReplacementTransform(dct_vals[0].copy(), animate_tex[1]), FadeIn(animate_tex))
		self.play(ReplacementTransform(animate_tex.copy(), rand_cos_plot[0]))
		self.wait()
	
		last_plot = rand_cos_plot[0]
		sum_plot = last_plot.copy().set_stroke(width = 1)
		for i in range(1, count):
			sum_cos = lambda x: sum([f(x) for f in rand_cos[:i + 1]])
			cur_sum_plot = right_ax.plot(sum_cos, [0, count], color = BLUE)
			self.play(
				focus_rect.animate.become(SurroundingRectangle(dct_vals[i])),
			 	animate_tex.animate.become(rand_tex[i]), 
				Create(rand_cos_plot[i]), 
				last_plot.animate.set_stroke(width = 1),
			)
			self.play(ReplacementTransform(sum_plot, cur_sum_plot), rand_cos_plot[i].animate.set_stroke(width = 1))
			last_plot = rand_cos_plot[i]
			sum_plot = cur_sum_plot
			self.wait(0.5)

		def make_lines(rand_plot, sum_plot, rand_mtx):
			right_lines = VGroup(*[right_ax.get_vertical_line(right_ax.i2gp(i + 0.5, sum_plot), color = YELLOW, stroke_width = 4) for i in range(count)])
			right_dots = VGroup(*[Dot(line.get_end(), color = YELLOW) for line in right_lines])
			mid_dash = VGroup(*[DashedLine(right_dots[i], rand_plot[i], dash_length = 0.1, dashed_ratio = 0.3, color = PURPLE) for i in range(count)])
			cos_mtx = rand_mtx.copy().next_to(right_ax, DOWN).set_fill(BLUE, 1)
			return right_lines, right_dots, mid_dash, cos_mtx
		
		right_lines, right_dots, mid_dash, cos_mtx = make_lines(rand_plot, sum_plot, rand_mtx)
		for i in range(count):
			right_dots[i].move_to(right_lines[i].get_start())

		self.play(LaggedStart(*[FadeIn(dot) for dot in right_dots], lag_ratio = 0.3, run_time = 1))
		self.play(
			LaggedStart(*[Create(line) for line in right_lines], lag_ratio = 0.3, run_time = 1),
			LaggedStart(*[right_dots[i].animate.move_to(right_lines[i].get_end()) for i in range(count)], lag_ratio = 0.3, run_time = 1),
		)

		pts = cos_mtx.get_entries().copy()
		self.play(FadeOut(animate_tex, focus_rect), LaggedStart(*[FadeIn(pts[i], target_position = right_dots[i]) for i in range(count)], lag_ratio = 0.3, run_time = 2))
		self.play(FadeIn(cos_mtx))
		self.remove(*pts)

		self.play(Circumscribe(rand_mtx), Circumscribe(cos_mtx))
		self.play(*[Create(line) for line in mid_dash], run_time = 1)
		self.wait()

		for _ in range(5):
			next_dct, next_cos, next_plot, next_cos_polt, next_mtx, nex_pixel = make_rand_dct()
			next_dct_mtx = DecimalMatrix(next_dct, element_to_mobject_config = {"num_decimal_places" : 1}).set_fill(RED, 1).replace(dct_mtx)
			next_cos_polt.set_stroke(width = 1)
			next_sum_plot = right_ax.plot(lambda x: sum([f(x) for f in next_cos]), [0, count], color = BLUE)
			next_lines, next_dots, next_dash, next_cos_mtx= make_lines(next_plot, next_sum_plot, next_mtx)
			self.play(
				*[pixel_rects[i].animate.set_fill(ManimColor([nex_pixel[i]]*3), 1) for i in range(count)],
				*[ChangeDecimalToValue(pixel_vals[i], nex_pixel[i]) for i in range(count)],
				dct_mtx.animate.become(next_dct_mtx),
				rand_plot.animate.become(next_plot),
				rand_mtx.animate.become(next_mtx),
				rand_cos_plot.animate.become(next_cos_polt),
				sum_plot.animate.become(next_sum_plot),
				right_lines.animate.become(next_lines),
				right_dots.animate.become(next_dots),
				cos_mtx.animate.become(next_cos_mtx),
				mid_dash.animate.become(next_dash),
				run_time = 1.5,
			)
			self.wait(0.5)

		self.remove(self.title)
		mobjects = self.mobjects
		self.add_foreground_mobject(self.title)
		self.play(FadeOut(*mobjects))

	def dct_base_img(self):
		dog = ImageMobject(os.path.join("assert", "ikun", "dog"))
		grey_pixel = img_ops.grey_scale(dog.get_pixel_array())
		grey_dog = ImageMobject(img_ops.grey_scale(grey_pixel)).scale_to_fit_height(STAGE_HEIGHT * 0.5).set_resampling_algorithm(0)
		self.play(FadeIn(grey_dog.set_z_index(-1)))

		h_count = 4
		v_count = 6
		full_rect = FullScreenRectangle().to_stage_edge(UP, 0).scale(1.1)
		scale_area = Rectangle(height = h_count, width = v_count).scale_to_fit_height(STAGE_HEIGHT * 0.7).move_to(dog)
		dog_mask = Cutout(full_rect, scale_area, fill_opacity = 1, color = config.background_color, stroke_width = 0, stroke_color = LIGHTER_GRAY)
		self.add(dog_mask)

		block_cap = img_ops.dct_block_cap
		block_size = scale_area.height / h_count
		pixel_size = block_size / block_cap
		h, w = grey_pixel.shape[0:2]
		scale_factor = pixel_size * h / grey_dog.height
		self.play(grey_dog.animate.scale(scale_factor), dog_mask.animate.set_stroke(width = 4), run_time = 3)

		h_start = round((h + (h_count - 2) * block_cap) / 2)
		v_start= round((w - v_count * block_cap) / 2)
		block_pixel = grey_pixel[h_start:h_start + block_cap, v_start:v_start + block_cap]
		pick_block = ImageMobject(block_pixel).scale_to_fit_height(block_size).set_resampling_algorithm(0).move_to(grey_dog).shift((LEFT * (v_count - 1) + DOWN * (h_count - 1)) * block_size / 2)
		self.add(pick_block.set_z_index(-1))

		h_block_lines = VGroup(*[Line(scale_area.get_left(), scale_area.get_right(), color = BLUE, stroke_width = 6) for _ in range(h_count + 1)]).arrange(DOWN, block_size).move_to(dog).set_z_index(2)
		v_block_lines = VGroup(*[Line(scale_area.get_top(), scale_area.get_bottom(), color = BLUE, stroke_width = 6) for _ in range(v_count + 1)]).arrange(RIGHT, block_size).move_to(dog).set_z_index(2)
		self.play(
			LaggedStart(*[Create(line) for line in h_block_lines], lag_ratio = 0.5, run_time = 1),
			LaggedStart(*[Create(line) for line in v_block_lines], lag_ratio = 0.5, run_time = 1),
		)

		h_pixel_lines = VGroup(*[Line(pick_block.get_left(), pick_block.get_right(), color = BLUE, stroke_width = 2) for _ in range(block_cap - 1)]).arrange(DOWN, pixel_size).move_to(pick_block).set_z_index(2)
		v_pixel_lines = VGroup(*[Line(pick_block.get_top(), pick_block.get_bottom(), color = BLUE, stroke_width = 2) for _ in range(block_cap - 1)]).arrange(RIGHT, pixel_size).move_to(pick_block).set_z_index(2)
		self.play(
			LaggedStart(*[Create(line) for line in h_pixel_lines], lag_ratio = 0.2, run_time = 1.5),
			LaggedStart(*[Create(line) for line in v_pixel_lines], lag_ratio = 0.2, run_time = 1.5),
		)

		top_brace = BraceLabel(pick_block, str(block_cap), UP)
		left_brace = BraceLabel(pick_block, str(block_cap), LEFT)
		self.play(FadeIn(top_brace), FadeIn(left_brace))

		block_rect = Square(color = BLUE, stroke_width = 6).replace(pick_block)
		self.block_group = Group(pick_block, block_rect, h_pixel_lines, v_pixel_lines, top_brace, left_brace)
		pick_block.set_z_index(0)

		pixel_scale = 2
		block_size *= pixel_scale
		pixel_size *= pixel_scale
		self.play(self.block_group.animate.scale(pixel_scale).center().to_stage_edge(LEFT), FadeOut(grey_dog, h_block_lines, v_block_lines), dog_mask.animate.set_stroke(width = 0))
		self.remove(dog_mask)

		pos_group = VGroup(*[Rectangle() for _ in range(block_cap)]).arrange_in_grid(4, buff = 0)
		pos_group.stretch_to_fit_height(STAGE_HEIGHT * 0.7)
		pos_group.stretch_to_fit_width((self.camera.frame.get_right() - self.block_group.get_right())[0])
		pos_group.align_to(self.block_group.get_right(), LEFT)

		cos_tex_group = VGroup()
		for i in range(block_cap):
			k = 1 if i == 0 else 2
			cos_tex = MathTex(tex_maker.dct_cos_base_str.format(k, block_cap, i)).scale_to_fit_width(pos_group[i].width * 0.8).move_to(pos_group[i])
			cos_tex[1].set_color(RED)
			cos_tex[5].set_color(BLUE)
			cos_tex_group.add(cos_tex)

		self.play(FadeIn(cos_tex_group, scale = 0, target_position = self.block_group.get_right()))
		self.play(LaggedStart(*[Circumscribe(tex[5][0], fade_out=True) for tex in cos_tex_group], lag_ratio = 0.3, run_time = 2))
		self.wait()
		self.play(*[Circumscribe(tex[1]) for tex in cos_tex_group])
		self.play(
			LaggedStart(*[FadeOut(*tex[1:4], scale = 0) for tex in cos_tex_group], lag_ratio = 0.3, run_time = 2),
			LaggedStart(*[Group(*tex[4:]).animate.align_to(tex[1], LEFT) for tex in cos_tex_group], lag_ratio = 0.3, run_time = 2),
		)

		for tex in cos_tex_group:
			tex.remove(*tex[1:4])

		base_pixel_factor = 0.5
		base_rect = block_rect.copy().scale(base_pixel_factor).to_stage_edge(UP).match_x(pos_group)
		tex_target = cos_tex_group[0].copy().to_stage_edge(DOWN)

		base_ax = Axes(
			x_range = [0, block_cap + 0.8],
			y_range = [-0.55, 0.7, 0.5],
			x_length = pos_group.width * 0.75,
			y_length = (base_rect.get_bottom() - tex_target.get_top())[1] - DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2,
			axis_config = {"include_numbers" : True},
			y_axis_config = {
				"numbers_to_include" : [-0.5, 0.5],
				"decimal_number_config" : {"num_decimal_places" : 1},
			}
		).next_to(base_rect, DOWN).match_x(pos_group)

		base_rect.align_to(base_ax.c2p(block_cap, 0), RIGHT)
		tex_group_target = cos_tex_group.copy().arrange(DOWN).next_to(base_ax, DOWN)
		for tex in tex_group_target[1:]:
			tex.set_opacity(0)
		self.play(LaggedStart(cos_tex_group.animate.become(tex_group_target), Create(base_ax), lag_ratio = 0.5, run_time = 2))

		ax_ul = base_ax.c2p(0, 0.5)
		ax_dr = base_ax.c2p(block_cap, -0.5)
		grey_img = ImageMobject([[255 - i] * 256 for i in range(256)]).set_z_index(-1)
		grey_img.stretch_to_fit_width(ax_dr[0] - ax_ul[0])
		grey_img.stretch_to_fit_height(ax_ul[1] - ax_dr[1])
		grey_img.align_to(ax_ul, UL)
		self.play(FadeIn(grey_img))

		self.dct_base_pixel = img_ops.make_dct_base_pixel_array(block_cap)
		first_row_pixel = img_ops.dct_base_to_color(self.dct_base_pixel[0] * np.sqrt(block_cap))
		base_img_pixel = img_ops.dct_base_to_color(self.dct_base_pixel)

		pos_buff = MED_SMALL_BUFF * 0.6
		first_row = Group(Square(pos_group.width * 0.7 / block_cap - pos_buff, stroke_width = 0)).next_to(base_rect, LEFT, MED_SMALL_BUFF)

		for i in range(block_cap):
			next_tex = cos_tex_group[i]
			next_plot = base_ax.plot(lambda x: np.sqrt((1 if i == 0 else 2) / block_cap) * np.cos(i / block_cap * np.pi * x), [0, block_cap], color = BLUE)
			next_lines = VGroup(*[base_ax.get_vertical_line(base_ax.i2gp(i + 0.5, next_plot), color = RED, stroke_width = 4) for i in range(block_cap)])
			next_pixels = VGroup(*[Square(pixel_size * base_pixel_factor, color = ORANGE, stroke_width = 2).move_to(line.get_end()) for line in next_lines]).set_z_index(1)
			next_img = ImageMobject(first_row_pixel[i]).set_resampling_algorithm(0).replace(base_rect)

			for k in range(block_cap):
				next_pixels[k].set_fill(ManimColor([first_row_pixel[i][0][k]]*3), 1)

			if i == 0:
				next_pixels.save_state()
				pickers = next_pixels.copy()
				for k in range(block_cap):
					pickers[k].set_fill(None, 0)
					pickers[k].move_to(next_lines[k].get_start())

				self.play(Create(next_plot))
				self.play(LaggedStart(*[Create(p) for p in pickers], lag_ratio = 0.1))
				self.play(
					LaggedStart(*[Create(line) for line in next_lines], lag_ratio = 0.1),
					LaggedStart(*[pickers[k].animate.move_to(next_lines[k].get_end()) for k in range(block_cap)], lag_ratio = 0.1),
				)

				pixels_target = next_pixels.copy().arrange(RIGHT, 0).align_to(base_rect.get_corner(DL), DL)
				for pixel in pixels_target:
					pixel.set_stroke(color = pixel.get_color())

				next_img = ImageMobject(first_row_pixel[i]).set_resampling_algorithm(0).replace(base_rect)
				self.play(Create(base_rect.set_z_index(1)), FadeIn(next_pixels))
				self.play(LaggedStart(*[ReplacementTransform(next_pixels[k].copy(), pixels_target[k]) for k in range(block_cap)], lag_ratio = 0.1))
				self.play(pixels_target.animate.stretch_to_fit_height(next_img.height).match_y(next_img))
				self.remove(*pickers)
				self.remove(*pixels_target)
				self.add(next_img)

				cur_plot = next_plot
				cur_lines = next_lines
				cur_pixels = next_pixels
				cur_img = next_img
			else:
				self.play(
					cur_tex.animate.next_to(cur_tex, UP).set_opacity(0),
					next_tex.animate.move_to(cur_tex).set_opacity(1),
					cur_plot.animate.become(next_plot),
					cur_lines.animate.become(next_lines),
					cur_pixels.animate.become(next_pixels),
					cur_img.animate.become(next_img),
				)

			img = Group(cur_img.copy(), base_rect.copy().set_stroke(width = 2))
			self.play(
				img.animate.replace(first_row[-1]),
				first_row.animate.next_to(first_row[-1], LEFT, pos_buff)
			)
			first_row.add(img)
			cur_tex = next_tex
			self.wait(0.5)

		buff = STAGE_HEIGHT * 0.8 / (block_cap + 2) / (block_cap + 1) / 2
		base_block_size = buff * block_cap * 2
		row_target = first_row.copy().scale_to_fit_height(base_block_size).arrange(RIGHT, buff)
		col_target = row_target.copy().rotate(np.pi / 2 * 3, about_point = row_target[0].get_center())
		row_bottom = row_target.copy().shift(DOWN * (base_block_size + buff) * (block_cap + 1))
		col_right = col_target.copy().shift(RIGHT * (base_block_size + buff) * (block_cap + 1))
		Group(row_target, col_target, row_bottom, col_right).match_x(pos_group).match_y(self.block_group)

		self.play(
			FadeOut(base_ax, base_rect, cur_img, cur_pixels, cur_lines, cur_plot, grey_img, cur_tex),
			first_row.animate.arrange(RIGHT, first_row.height / row_target.height * buff).move_to(row_target)
		)
		self.wait()

		first_col = first_row.copy()
		self.play(
			first_row.animate.match_width(row_target),
			first_col.animate.match_width(row_target).rotate(np.pi / 2 * 3, about_point = row_target[0].get_center()),
		)
		self.wait()

		base_img = Group()
		for i in range(block_cap):
			row =Group()
			base_img.add(row)
			for j in range(block_cap):
				img = ImageMobject(base_img_pixel[i][j]).set_resampling_algorithm(0).scale_to_fit_height(base_block_size)
				img.match_x(first_row[j + 1])
				img.match_y(first_col[i + 1])
				row.add(img)

		show_up_list = []
		for i in range(block_cap):
			blocks = Group(base_img[i][i])
			for k in range(i):
				blocks.add(base_img[i][k])
				blocks.add(base_img[k][i])
			show_up_list.append(AnimationGroup(*[FadeIn(block, scale = 0) for block in blocks]))

		self.play(
			row_target.animate.move_to(row_bottom),
			col_target.animate.move_to(col_right),
			LaggedStart(Wait(1), *show_up_list, lag_ratio = 0.25),
			run_time = 3,
		)
		self.wait()

		base_img_bg = Group()
		base_img_bg.add(Square(base_img.height + buff * 2, stroke_width = 0).set_fill(BLUE, 1).move_to(base_img))
		base_img_bg.add(BraceLabel(base_img, str(block_cap), UP))
		base_img_bg.add(BraceLabel(base_img, str(block_cap), LEFT))
		base_img_bg.set_z_index(-1)
		self.play(FadeIn(base_img_bg), FadeOut(first_row, first_col, row_target, col_target))
		self.base_img_group = Group(base_img, *base_img_bg)

	def dct_example(self):
		pick_block = self.block_group[0]
		base_img = self.base_img_group[0]
		g = ImageMobject(os.path.join("assert", "jpeg", "G88")).set_resampling_algorithm(0).replace(pick_block)
		self.play(pick_block.animate.become(g))

		self.play(
			FadeOut(*self.block_group[-2:]),
			FadeOut(*self.base_img_group[-2:]),
		)

		img_size = STAGE_HEIGHT * 0.6
		self.block_group.remove(*self.block_group[-2:])
		base_img.add(self.base_img_group[1])
		self.add(self.block_group, base_img)
		self.play(
			self.block_group.animate.scale_to_fit_height(img_size).move_to(LEFT * STAGE_WIDTH / 4),
			base_img.animate.scale_to_fit_height(img_size).move_to(RIGHT * STAGE_WIDTH / 4),
		)
		pixel = g.get_pixel_array()
		h, w = pixel.shape[0:2]
		dct_val = img_ops.pixel2dct(pixel[:, :, 0])

		color_mtx = Group()
		dct_mtx = Group()
		for i in range(h):
			val_row = Group()
			dct_row = Group()
			color_mtx.add(val_row)
			dct_mtx.add(dct_row)
			for j in range(w):
				val = Integer(pixel[i][j][0], color = RED).scale_to_fit_height(base_img[i][j].height * 0.4).move_to(base_img[i][j])
				dct = Integer(dct_val[i][j], color = YELLOW).scale_to_fit_height(val.height * 0.8).move_to(val)
				val_row.add(val)
				dct_row.add(dct)

		color_mtx.move_to(self.block_group)
		self.play(LaggedStart(*[LaggedStart(*[FadeIn(val, scale = 0) for val in row]) for row in color_mtx]), run_time = 2)
		self.play(LaggedStart(*[LaggedStart(*[FadeIn(dct_mtx[i][j], scale = 0, target_position = color_mtx[i][j]) for j in range(w)]) for i in range(h)]), run_time = 2)
		self.wait()

		sum_pixel = np.zeros((h, w))
		sum_img = ImageMobject(np.uint8(sum_pixel)).set_resampling_algorithm(0).replace(pick_block).set_z_index(-1)
		self.play(FadeOut(pick_block, color_mtx))
		self.add(sum_img)

		loop_time = 1
		time_base = 0.6

		z_scan = img_ops.make_z_scan(h, w)

		for pos in z_scan:
			i, j = pos[:]
			pixel = self.dct_base_pixel[i][j] * dct_val[i][j]
			sum_pixel += pixel

			cur_img =  ImageMobject(img_ops.float2color(sum_pixel)).set_resampling_algorithm(0).replace(sum_img)
			loop_time = pow(time_base, (i + j))

			if loop_time > 0.1:
				img = ImageMobject(img_ops.float2color(pixel)).set_resampling_algorithm(0).replace(base_img[i][j])
				self.play(FadeOut(dct_mtx[i][j]), FadeIn(img), run_time = loop_time)
				self.play(img.animate.replace(sum_img), run_time = loop_time)
				self.play(img.animate.become(cur_img), run_time = loop_time)
				self.remove(img)
				sum_img.pixel_array = cur_img.get_pixel_array()
			else:
				self.play(FadeOut(dct_mtx[i][j]), sum_img.animate.become(cur_img), run_time = loop_time * 3)

		self.wait()

		grid = Group(*self.block_group[1:4]).copy().move_to(base_img)
		self.play(FadeIn(dct_mtx), FadeIn(grid), FadeOut(base_img))

		low_pixel = np.zeros((h, w))
		cut_idx = round(len(z_scan) / 2)
		for pos in z_scan[:cut_idx]:
			i, j = pos[:]
			low_pixel += self.dct_base_pixel[i][j] * dct_val[i][j]

		fadeout = []
		for pos in reversed(z_scan[cut_idx:]) :
			i, j = pos[:]
			fadeout.append(FadeOut(dct_mtx[i][j]))

		self.play(
			sum_img.animate.become(ImageMobject(img_ops.float2color(low_pixel)).set_resampling_algorithm(0).replace(sum_img)),
			LaggedStart(*fadeout, lag_ratio = 0.1),
			run_time = 2,
		)

		self.block_group = Group(sum_img, *self.block_group[1:4])
		self.dct_group = Group(dct_mtx, grid)
		self.dct_val = dct_val
	
	def quantization(self):
		title_tex = Text("量化").match_height(self.title_img).next_to(self.title_img)
		title_underline = Underline(Group(self.title_img, title_tex))
		self.play(
			FadeOut(self.title_txt), FadeIn(title_tex),
			self.title_underline.animate.become(title_underline),
		)
		self.title_txt = title_tex
		self.title = Group(self.title_img, self.title_txt, self.title_underline)
		self.add_foreground_mobject(self.title)

		dmtx = self.dct_group[0]
		self.play(
			FadeOut(self.block_group[0]),
			dmtx.animate.set_opacity(1),
		)

		qtitle = Text("量化表").scale_to_fit_height(0.3).next_to(self.block_group, UP)
		qtables = img_ops.qtables()
		qnames = list(qtables.keys())
		qvals = qtables[qnames[0]]
		qmtx = Group(*[Group(*[Integer(v, color = RED) for v in row]) for row in qvals])
		h, w = qvals.shape[:]
		for i in range(h):
			for j in range(w):
				qmtx[i][j].match_height(dmtx[i][j]).move_to(dmtx[i][j])
		qmtx.move_to(self.block_group)
		self.play(
			FadeIn(qtitle, target_position = self.block_group.get_top(), run_time = 1),
			LaggedStart(*[LaggedStart(*[FadeIn(val, scale = 0) for val in row]) for row in qmtx], run_time = 2),
		)

		self.qgroup = Group(qmtx, qtitle, *self.block_group[1:4])
		self.play(
			self.qgroup.animate.scale_to_fit_width(STAGE_WIDTH / 4).to_stage_edge(LEFT),
			self.dct_group.animate.scale_to_fit_width(STAGE_WIDTH / 4).to_stage_edge(RIGHT),
		)

		tex_str = r"\frac{{{0}}}{{{1}}}"
		tex_mtx = Group()
		result_mtx = Group()
		for i in range(h):
			tex_row = Group()
			result_row = Group()
			tex_mtx.add(tex_row)
			result_mtx.add(result_row)
			for j in range(w):
				dobj = dmtx[i][j]
				qobj = qmtx[i][j]
				dval = dobj.get_value()
				qval = qobj.get_value()
				dlen = len(str(dval))
				qlen = len(str(qval))	

				tex = SingleStringMathTex(tex_str.format(dval, qval)).scale_to_fit_width(max(dobj.width, qobj.width) * 0.8).move_to(qobj)
				result = Integer(round(dval / qval), color = TEAL).match_height(qobj).move_to(qobj)
				tex_row.add(tex)
				result_row.add(result)

				tex.up = tex[0:dlen]
				tex.mid = tex[dlen]
				tex.down = tex[-qlen:]
				tex.up.match_color(dobj)
				tex.down.match_color(qobj)

		tex_mtx.center().scale_to_fit_width(STAGE_WIDTH * 0.35)
		result_mtx.center().scale_to_fit_width(STAGE_WIDTH * 0.35)

		self.play(
			LaggedStart(*[
				LaggedStart(*[
					AnimationGroup(*[
						ReplacementTransform(dmtx[i][j].copy(), tex_mtx[i][j].up),
						ReplacementTransform(qmtx[i][j].copy(), tex_mtx[i][j].down),
						FadeIn(tex_mtx[i][j].mid, scale = 0),
					])
					for j in range(w)
				], lag_ratio = 0.1)
				for i in range(h)
			], lag_ratio = 0.1)
		)

		self.wait()

		self.play(
			LaggedStart(*[
				LaggedStart(*[
					ReplacementTransform(tex_mtx[i][j], result_mtx[i][j])
					for j in range(w)
				], lag_ratio = 0.1)
				for i in range(h)
			], lag_ratio = 0.1)
		)

		z_scan = img_ops.make_z_scan(h, w)
		code_mtx = Group()
		arrow_mtx = Group()
		start, end = None, None
		val_list = []
		for pos in z_scan:
			obj = result_mtx[pos[0]][pos[1]]
			code_mtx.add(obj.copy())
			val_list.append(obj.get_value())
			start = end
			end = obj.get_center()
			if start is not None:
				arrow_mtx.add(Arrow(start, end))

		self.play(LaggedStart(*[GrowArrow(arrow) for arrow in arrow_mtx], run_time = 2.5))
		self.wait()
		self.play(Group(arrow_mtx, result_mtx).animate.align_to(self.dct_group, DOWN))

		code_mtx.move_to(result_mtx)
		code_target = code_mtx.copy().arrange_in_grid(2).next_to(result_mtx, DOWN, MED_LARGE_BUFF)
		self.play(
			LaggedStart(*[FadeOut(arrow, scale = 0) for arrow in arrow_mtx]),
			LaggedStart(*[code_mtx[i].animate.move_to(code_target[i]) for i in range(h * w)]),
		)

		code_list = list(img_ops.run_length_encode(val_list))
		code_len = sum([len(code) + 1 for code in code_list])
		cut_pos = -1
		first_len = 0
		while first_len < code_len / 2:
			cut_pos += 1
			first_len += len(code_list[cut_pos]) + 1

		code_str = ", ".join(code_list[0:cut_pos]) + ",\n" + ", ".join(code_list[cut_pos:])
		run_length_code = Text(code_str, color = ORANGE).match_height(code_mtx).move_to(code_mtx)
		self.play(
			FadeOut(code_mtx, scale = 0, run_time = 1.5),
			Succession(Wait(0.5), FadeIn(run_length_code, scale = 0, run_time = 1)),
		)
		self.wait()

		qname = Text(qnames[0]).scale_to_fit_height(0.4).match_x(qmtx).align_to(result_mtx.copy().center(), DOWN)
		self.play(
			FadeIn(qname, target_position = qmtx.get_bottom()),
			FadeOut(run_length_code),
			result_mtx.animate.center(),
		)
		self.wait()

		for name in qnames[1:]:
			qvals = qtables[name]
			results = np.round(self.dct_val / qvals)
			self.play(
				qname.animate.become(Text(name).match_height(qname).move_to(qname)),
				*[AnimationGroup(*[result_mtx[i][j].animate.set_value(results[i][j]).move_to(result_mtx[i][j]) for j in range(w)]) for i in range(h)],
				*[AnimationGroup(*[qmtx[i][j].animate.set_value(qvals[i][j]).move_to(qmtx[i][j]) for j in range(w)]) for i in range(h)],
				run_time = 1.5
			)
			self.wait(0.5)

		dct_rect = SurroundingRectangle(dmtx[0][0])
		q_rect = SurroundingRectangle(qmtx[0][0])
		r_rect = SurroundingRectangle(result_mtx[0][0]).stretch(1.5, 0)
		self.play(Create(dct_rect))
		self.play(Create(q_rect))
		self.play(Create(r_rect))

		qresult = self.dct_val.copy()
		qresult = np.round(qresult / qvals) * qvals
		self.play(result_mtx[0][0].animate.set_value(qresult[0][0]).move_to(result_mtx[0][0]))
		self.play(
			LaggedStart(*[
				LaggedStart(*[
					result_mtx[i][j].animate.set_value(qresult[i][j]).move_to(result_mtx[i][j])
					for j in range(w)
				])
				for i in range(h)
			])
		)

		pixel = img_ops.float2color(img_ops.idct2(qresult))
		img = ImageMobject(pixel).set_resampling_algorithm(0).replace(result_mtx).set_z_index(-1)
		self.play(FadeIn(img), FadeOut(dct_rect, q_rect, r_rect))
		self.play(
			img.animate.replace(self.dct_group),
			FadeOut(dmtx, target_position = dmtx.get_right()),
		)
		self.wait()

		self.play(qname.animate.become(Text("随机质量").match_height(qname).move_to(qname)))

		quality_range = range(1, 101)
		loop_times = len(quality_range)
		quality_list = list(quality_range)
		random.shuffle(quality_list)

		target_result = np.zeros((loop_times, h, w))
		target_tables = np.zeros((loop_times, h, w), int)

		count = 0
		for q in quality_list:
			qvals = img_ops.generate_quant_tbl(q)
			qresult = np.round(qresult / qvals) * qvals
			target_result[count] = qresult
			target_tables[count] = qvals
			count += 1

		target_pixel = img_ops.float2color(img_ops.idct2(target_result[-1]))
		count_tracker = ValueTracker(1)

		qmtx_pos = qmtx.copy()
		rmtx_pos = result_mtx.copy()
		def mtx_updater(m, dt):
			idx = round(count_tracker.get_value()) - 1
			qvals = target_tables[idx]
			qresult = target_result[idx]
			for i in range(h):
				for j in range(w):
					qmtx[i][j].set_value(qvals[i][j]).move_to(qmtx_pos[i][j])
					result_mtx[i][j].set_value(qresult[i][j]).move_to(rmtx_pos[i][j])

		self.add(qmtx, result_mtx, count_tracker)
		qmtx.add_updater(mtx_updater)

		self.play(
			count_tracker.animate.set_value(loop_times),
			img.animate.become(ImageMobject(target_pixel).set_resampling_algorithm(0).replace(img)),
			run_time = 5
		)
