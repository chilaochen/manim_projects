static void rgb2yuv_32(uint8_t dst[], SkPMColor c) {
	int r = SkGetPackedR32(c);
	int g = SkGetPackedG32(c);
	int b = SkGetPackedB32(c);

	int  y = ( CYR*r + CYG*g + CYB*b + 128 ) >> CSHIFT;
	int  u = ( CUR*r + CUG*g + CUB*b + 128 ) >> CSHIFT;
	int  v = ( CVR*r + CVG*g + CVB*b + 128 ) >> CSHIFT;

	dst[0] = SkToU8(y);
	dst[1] = SkToU8(u + 128);
	dst[2] = SkToU8(v + 128);
}