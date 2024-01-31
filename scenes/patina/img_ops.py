import random
from PIL import Image, ImageFilter, JpegPresets
from io import BytesIO
import numpy as np
from scipy.fftpack import dct, idct

def grey_scale(pixel_array):
	img = Image.fromarray(pixel_array)
	return np.array(img.convert("L"))

def yuv_scale(pixel_array):
	img = Image.fromarray(pixel_array)
	yuv_pixel = np.array(img.convert("YCbCr"))
	y_pixel = np.full(yuv_pixel.shape, 128, np.uint8)
	u_pixel = np.full(yuv_pixel.shape, 128, np.uint8)
	v_pixel = np.full(yuv_pixel.shape, 128, np.uint8)
	y_pixel[:, :, 0] = yuv_pixel[:, :, 0]
	u_pixel[:, :, 1] = yuv_pixel[:, :, 1]
	v_pixel[:, :, 2] = yuv_pixel[:, :, 2]
	y_img = Image.fromarray(y_pixel, "YCbCr")
	u_img = Image.fromarray(u_pixel, "YCbCr")
	v_img = Image.fromarray(v_pixel, "YCbCr")
	return np.array(y_img), np.array(u_img), np.array(v_img)

def uv_scale(pixel_array):
	img = Image.fromarray(pixel_array)
	uv_pixel = np.array(img.convert("YCbCr"))
	uv_pixel[:, :, 0] = 128
	uv_img = Image.fromarray(uv_pixel, "YCbCr")
	return np.array(uv_img)

def turn_green(pixel_array, times):
	green_array = pixel_array.copy()
	# return green_array
	for row in green_array:
		for pixel in row:
			r, g, b = pixel[0], pixel[1], pixel[2]
			for _ in range(times):
				nr, ng, nb = yuv2rgb(*rgb2yuv_skai(r, g, b))
				if nr == r and ng == g and nb == b:
					break
				else:
					r, g, b = nr, ng, nb
			pixel[0], pixel[1], pixel[2] = r, g, b
	return green_array

def jpeg_compress(pixel_array, quality):
	return jpeg_compress_width_random_quality(pixel_array, 1, quality, quality)

def jpeg_compress_width_random_quality(pixel_array, time, min_quality = 10, max_quality = 90):
	alpha = None
	if pixel_array.shape[2] == 4:
		alpha = pixel_array[:, :, 3]

	img = Image.fromarray(pixel_array).convert("RGB")

	for _ in range(time):
		file = BytesIO()
		img.save(file, format="JPEG", quality = random.randint(min_quality, max_quality))
		img = Image.open(file)

	new_array = np.array(img)

	if alpha is not None:
		new_array = np.concatenate((new_array, np.expand_dims(alpha, axis=2)), axis=2)
	return new_array

dct_block_cap = 8

def qtables():
	tables = {}
	desc_map = {
		"web_low" : "低质量",
		"web_medium" : "中质量",
		"web_high" : "高质量",
		"web_very_high" : "更高质量",
	}
	for k, v in desc_map.items():
		tables[v] = np.array(JpegPresets.presets[k]["quantization"][0]).reshape((dct_block_cap, dct_block_cap))
	return tables

std_luminance_quant_tbl = [
  16,  11,  10,  16,  24,  40,  51,  61,
  12,  12,  14,  19,  26,  58,  60,  55,
  14,  13,  16,  24,  40,  57,  69,  56,
  14,  17,  22,  29,  51,  87,  80,  62,
  18,  22,  37,  56,  68, 109, 103,  77,
  24,  35,  55,  64,  81, 104, 113,  92,
  49,  64,  78,  87, 103, 121, 120, 101,
  72,  92,  95,  98, 112, 100, 103,  99
]

#libjpeg-turbo/jcparam.c
def generate_quant_tbl(quality):
	if quality <= 0 :
		quality = 1
	elif quality > 100 :
		quality = 100

	if quality < 50:
		quality = 5000 / quality
	else:
		quality = 200 - quality * 2
	
	tbl_size = len(std_luminance_quant_tbl)
	tbl = np.zeros((tbl_size), int)

	for i in range(tbl_size):
		val = int((std_luminance_quant_tbl[i] * quality + 50) / 100)
		if val <= 0:
			val = 1
		elif val > 255:
			val = 255
		tbl[i] = val

	return tbl.reshape((dct_block_cap, dct_block_cap))

def split_freq_by_block(pixel_array, low_ratio = 0.5, block_cap = dct_block_cap):
	height = pixel_array.shape[0]
	width = pixel_array.shape[1]
	v_count = int(np.ceil(height / block_cap))
	h_count = int(np.ceil(width / block_cap))
	v_full = int(v_count * block_cap)
	h_full = int(h_count * block_cap)

	if len(pixel_array.shape) >= 3:
		scale_count = min(3, pixel_array.shape[2])
	else:
		scale_count = 1

	full_pixel = np.zeros((v_full, h_full, scale_count))
	if scale_count == 1:
		full_pixel[:height, :width, 0] = pixel_array
	else:
		full_pixel[:height, :width, :] = pixel_array[:, :, :scale_count]

	for k in range(scale_count):
		for i in range(v_count - 1):
			v_start = i * block_cap
			v_end = v_start + block_cap
			full_pixel[v_start:v_end, width:h_full, k] = np.mean(full_pixel[v_start:v_end, (h_full - block_cap):width, k])
		for j in range(h_count - 1):
			h_start = j * block_cap
			h_end = h_start + block_cap
			full_pixel[height:v_full, h_start:h_end, k] = np.mean(full_pixel[(v_full - block_cap):height, h_start:h_end, k])
		full_pixel[height:v_full:, width:h_full, k] = np.mean(full_pixel[(v_full - block_cap):height, (h_full - block_cap):width, k])

	full_low_pixel = np.zeros(full_pixel.shape)
	full_high_pixel = np.zeros(full_pixel.shape)
	scan_list = make_z_scan(block_cap, block_cap, low_ratio)

	for i in range(v_count):
		v_start = i * block_cap
		v_end = v_start + block_cap
		for j in range(h_count):
			h_start = j * block_cap
			h_end = h_start + block_cap
			low_pixel, high_pixel = split_freq(full_pixel[v_start:v_end, h_start:h_end], scan_list = scan_list)
			full_low_pixel[v_start:v_end, h_start:h_end] = low_pixel
			full_high_pixel[v_start:v_end, h_start:h_end] = high_pixel

	split_low_pixel = pixel_array.copy()
	split_high_pixel = pixel_array.copy()

	if scale_count == 1:
		split_low_pixel[:,:] = full_low_pixel[0:height, 0:width, 0]
		split_high_pixel[:,:] = full_high_pixel[0:height, 0:width, 0]
	else:
		split_low_pixel[:,:,:scale_count] = full_low_pixel[0:height, 0:width, :]
		split_high_pixel[:,:,:scale_count] = full_high_pixel[0:height, 0:width, :]

	return split_low_pixel, split_high_pixel

def split_freq(pixel_array, low_ratio = 0.5, scan_list = None):
	dct_vals = pixel2dct(pixel_array)
	height = pixel_array.shape[0]
	width = pixel_array.shape[1]
	l_dct = np.zeros(pixel_array.shape)

	if scan_list is None:
		scan_list = make_z_scan(height, width, low_ratio)
	for pos in scan_list:
		l_dct[pos[0]][pos[1]] = dct_vals[pos[0]][pos[1]]

	h_dcts = dct_vals - l_dct
	l_pixel = dct2pixel(l_dct)
	h_pixel = dct2pixel(h_dcts)

	return np.uint8(l_pixel), np.uint8(h_pixel)

def scale_pixel_to_fit_origin(origin_pixel, l_pixel, h_pixel):
	omax, omin = np.max(origin_pixel) , np.min(origin_pixel)
	lmax, lmin, lmean = np.max(l_pixel) , np.min(l_pixel) , np.mean(l_pixel)
	hmax, hmin, hmean = np.max(h_pixel) , np.min(h_pixel) , np.mean(h_pixel)

	if lmax > omax or lmin < omin:
		scale = max(1, (lmax - lmean) / (omax - lmean), (lmean - lmin) / (lmean - omin))
		l_pixel -= lmean
		l_pixel /= scale
		l_pixel += lmean

	if hmax > 255 or hmin < 0:
		scale = max(1, (hmax - hmean) / (255 - hmean), (hmean - hmin) / (hmean - 0))
		h_pixel -= hmean
		h_pixel /= scale
		h_pixel += hmean

def make_z_scan(h, w, ratio = 1):
	num = round(h * w * ratio)
	scan_list = np.zeros((num, 2), np.uint)
	pos = 0

	while pos < num:
		for k in range(h + w - 1):
			if k % 2 == 0:
				j = max(k - h + 1, 0)
				while pos < num and j < min(k + 1, w):
					scan_list[pos] = [k - j, j]
					pos += 1
					j += 1
			else:
				i = max(k - w + 1, 0)
				while pos < num and i < min(k + 1, h):
					scan_list[pos] = [i, k - i]
					pos += 1
					i += 1
	return scan_list

def run_length_encode(array):
	count = 0
	last = None
	code_list = []

	for val in [*array, None]:
		if last is None or last == val:
			count += 1
		else:
			if count > 1:
				code_list.append("{0}:{1}".format(last, count))

			else:
				code_list.append("{0}".format(last))
			count = 1
		last = val

	return code_list

def pixel2dct(pixel_array):
	pixel = color2float(pixel_array)
	return dct2(pixel)

def dct2pixel(dct_block):
	pixel = idct2(dct_block)
	return float2color(pixel)

def dct2(array):
	return dct(dct(array, axis=0, norm='ortho'), axis=1, norm='ortho')

def idct2(array):
	return idct(idct(array, axis=0 , norm='ortho'), axis=1 , norm='ortho')

def color2float(color):
	return np.float64(color) - 128

def float2color(val):
	cval = val.copy()
	cmax, cmin = np.max(cval), np.min(cval)
	if cmax > 127 or cmin < -128:
		cval /= max(cmax / 127, cmin / (-128))
	return np.uint8(np.round(cval + 128))

def dct_base_to_color(dct_base):
	return np.uint8(np.round((dct_base + 0.5) * 255))
	
def make_dct_base_pixel_array(block_cap = dct_block_cap):
	dct_base_pixel = np.zeros((block_cap, block_cap, block_cap, block_cap))
	for u in range(block_cap):
		u_func = lambda x: np.cos(x * u / block_cap * np.pi) * np.sqrt(((u==0) and 1 or 2) / block_cap)
		for v in range(block_cap):
			v_func = lambda x: np.cos(x * v / block_cap * np.pi) * np.sqrt(((v==0) and 1 or 2) / block_cap)
			for i in range(block_cap):
				i_val = u_func(i + 0.5)
				for j in range(block_cap):
					j_val = v_func(j + 0.5)
					dct_base_pixel[u][v][i][j] = i_val * j_val
	return dct_base_pixel

def box_blurry(pixel_array, radius = 5):
	#return pixel_array
	img = Image.fromarray(pixel_array)
	img = img.filter(ImageFilter.BoxBlur(radius))
	return np.array(img)

def split_rgb(color):
	rgb = np.zeros((3, 3), np.uint8)
	for i in range(3):
		rgb[i][i] = color[i]
	return rgb, color

def split_yuv(color):
	yuv = rgb2yuv(*color)
	rgb = np.full((3, 3), 128, np.uint8)
	for i in range(3):
		rgb[i][i] = yuv[i]
		rgb[i] = [*yuv2rgb(*rgb[i])]
	return rgb, yuv

rgb2yuv_map = np.full((256**3, 3), -1, np.int16)
rgb2yuv_skia_map = np.full((256**3, 3), -1, np.int16)
yuv2rgb_map = np.full((256**3, 3), -1, np.int16)

#https://en.wikipedia.org/wiki/YCbCr#JPEG_conversion
def rgb2yuv(R, G, B):
	idx = (R << 16) | (G << 8) | B
	yuv = rgb2yuv_map[idx] 
	if yuv[0] == -1:
		Y =      0.299 * R +    0.587 * G +    0.114 * B
		U = - 0.168736 * R - 0.331264 * G +      0.5 * B + 128
		V =        0.5 * R - 0.418688 * G - 0.081312 * B + 128
		yuv[:] = round(Y), round(U), round(V)
	return yuv

def yuv2rgb(Y, U, V):
	idx = (Y << 16) | (U << 8) | V
	rgb = yuv2rgb_map[idx] 
	if rgb[0] == -1:
		R = Y +                         1.402 * (V - 128)
		G = Y - 0.344136*(U - 128) - 0.714136 * (V - 128)
		B = Y +    1.772*(U - 128)
		rgb[:] = max(0, min(255, round(R))), max(0, min(255, round(G))), max(0, min(255, round(B)))
	return rgb

#https://github.com/google/skia/commit/c7d01d3e1d3621907c27b283fb7f8b6e177c629d
def rgb2yuv_skai(R, G, B):
	idx = (R << 16) | (G << 8) | B
	yuv = rgb2yuv_skia_map[idx] 
	if yuv[0] == -1:
		Y =   (   77 * R + 150 * G +  29 * B ) >> 8
		U = ( ( - 43 * R -  85 * G + 128 * B ) >> 8 ) + 128
		V = ( (  128 * R - 107 * G -  21 * B ) >> 8 ) + 128
		yuv[:] = Y, U, V
	return yuv
