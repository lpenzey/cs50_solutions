# Questions

## What's `stdint.h`?

stdint.h is a header file in C99 that provides typedefs for integer widths.
Width here refers to the number of bits required to store the value of the integer in binary.
Also defined by header file are macros that specify limits of various integer types.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

The difference between `uint8_t` and `int32_t` is that the `u` prefix designates an unsigned integer,
whereas the absence of a `u` denotes a signed integer. An unsigned integer uses the leading bit as part
of the int value. A signed int using the leading bit to mark whether the integer is positive or negative.
Because of this, an unsigned int has more "room" for data pertaining to the int value, and thus can hold
a larger value than a signed int. While unsigned ints can be larger they can also only be positive, so there's
a tradeoff between the various typedefs. The point of using something like `uint8_t`, `uint16_t` or `uint32_t` would be
if you have large values in either an 8, 16 or a 32-bit width. You would want to use `int32_t` if you want to represent
a negative integer (or a positive value of a certain size).

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

`BYTE`  = 8 bits or one byte
`DWORD` = 32 bits or 4 bytes
`LONG`  = 32 bits or 4 bytes
`WORD`  = 16 bits or 2 bytes

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

The first two bytes are the header field, and in hexadecimal they are 0x42 0x4D, or BM is ASCII.

## What's the difference between `bfSize` and `biSize`?

bfSize is the toal size, in bits, of the entire bitmap file including headers and any padding.
biSize is the site, in bits, of the actual image (the RGB triples).

## What does it mean if `biHeight` is negative?

If biHeight is negative then the image is top-down oriented and starts in the upper left corner.
If it's positive then its orientation is bottom-up, and starts from the bottom left.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount specifies the BMP image's color depth.

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

`fopen` would only return `NULL` if the file that it's trying to open doesn't exist.

## Why is the third argument to `fread` always `1` in our code?

It's 1 because you want to iterate over every pixel in the image, rather than a multiple that would skip certain pixels.


## What value does line 65 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?
The formula for determining padding is as follows:

`int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;`

Padding is added in order to ensure that the number of bytes in every row is a multiple of 4.

With a `bi.biWidth` of 3 the padding would also equate to 3.

## What does `fseek` do?

`fseek` sets the offset of a pointer. In whodunit.c we use it to offset the stream by the amount
of padding, if necessary.

## What is `SEEK_CUR`?

`SEEK_CUR` is the current position of the file pointer.

## Whodunit?

Professor Plum with the candlestick in the library.
