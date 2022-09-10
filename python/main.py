#!/usr/bin/env python3

from typing import List
import utils.file_parser as fp
from utils.image import (
    StrideImage,
    to_image,
    to_stride_image,
)
from solution import compute_solution


def main():  # pylint: disable=missing-function-docstring
    # Use the provided implementation that best suits your needs
    # image_type: fp.ImageType = fp.ImageType.PackedImageType
    image_type: fp.ImageType = fp.ImageType.StrideImageType

    input_file_name = "input.bin"
    output_file_name = "output.bin"

    # NOTE: data loading could take at least several seconds with big test files
    input_images, output_images = fp.generate_io_data(input_file_name, output_file_name, image_type)

    # input_images = [input_images[1]]
    # output_images = [output_images[1]]

    compute_solution(input_images)

    if input_images == output_images:
        print("Solution status - [SUCCESS]\n")
    else:
        print("Solution status - [FAIL]\n")
        # for ix, im in enumerate(input_images):
        #     for i in range(len(im.pixels_red)):
        #         if im.pixels_red[i] != output_images[ix].pixels_red[i]:
        #             print(f'In image {ix} Pixel {i} should be '
        #                   f'{output_images[ix].pixels_red[i]} but is {im.pixels_red[i]}')


if __name__ == "__main__":
    main()
