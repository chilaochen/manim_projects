static void rgb2yuv_32(uint8_t dst[], SkPMColor c) {
	int r = SkGetPackedR32(c);
	int g = SkGetPackedG32(c);
	int b = SkGetPackedB32(c);

	int  y = ( CYR*r + CYG*g + CYB*b ) >> CSHIFT;
	int  u = ( CUR*r + CUG*g + CUB*b ) >> CSHIFT;
	int  v = ( CVR*r + CVG*g + CVB*b ) >> CSHIFT;

	dst[0] = SkToU8(y);
	dst[1] = SkToU8(u + 128);
	dst[2] = SkToU8(v + 128);
}