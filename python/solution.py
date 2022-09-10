#!/usr/bin/env python3
import math

import numpy as np

from typing import (
    List,
    Tuple,
    Union
)

from utils.image import (
    ImageType,
    PackedImage,
    StrideImage,
)

from utils.function_tracer import FunctionTracer
from utils.eye_pattern import *

PATTERNS = (EYE_PATTERN_1, EYE_PATTERN_2, EYE_PATTERN_3, EYE_PATTERN_4)
RED_COMPONENT = 200
RED_COMPONENT_REDUCE = 150


def find_all(seq, subseq):
    n = len(seq)
    m = len(subseq)
    for i in range(n - m + 1):
        if all(seq[i + j] == subseq[j] for j in range(m) if j):
            yield i


def compute_solution(images: List[Union[PackedImage, StrideImage]]):
    ft = FunctionTracer("compute_solution", "seconds")

    for im in images:
        red_pxls_bool = np.array(im.pixels_red) >= RED_COMPONENT
        width = im.resolution.width
        heigth = im.resolution.height
        edited_pixels = []

        for pat in PATTERNS:
            first_pat_row = pat[0]

            row_bool = np.array(list(first_pat_row)) != ' '
            matches = find_all(red_pxls_bool, row_bool)
            for i in matches:
                # print(f'First match index {i}')
                counter = 0
                row = math.floor(i/width)  # index
                col = i - row * width  # index
                if (row + len(first_pat_row) > heigth) or (col + len(pat) > width):
                    continue
                counter += 1

                for pat_i in range(1, len(pat)):
                    idx_recalc = i+(width*pat_i)
                    # print(f'i:{i}  max_len:{(width * heigth)}')
                    if idx_recalc > (width * heigth):
                        # fix for not square resolutions
                        print(f'{idx_recalc} > {(width * heigth)}')
                        continue
                    row_slice = red_pxls_bool[idx_recalc:idx_recalc+len(pat)]
                    pat_row_bool = np.array(list(pat[pat_i])) != ' '

                    if all([pat_row_bool[i] == row_slice[i] for i, e in enumerate(pat_row_bool) if e]):
                        # if not all(pat_row_bool == row_slice):
                        #     print(f'Idx recalc: {idx_recalc}')
                        #     print(f'Image: {row_slice}')
                        #     print(f'Mask : {pat_row_bool}')
                        counter += 1

                if counter == len(pat):
                    for ip, p in enumerate(pat):
                        idx_recalc = i + (width * ip)
                        for offset in range(len(p)):
                            px_i = idx_recalc + offset

                            if p[offset] != ' ':
                                if px_i not in edited_pixels:
                                    # print(f'Editing pixel {px_i}, current value:{im.pixels_red[px_i]}, '
                                    #       f'new value:{im.pixels_red[px_i] - RED_COMPONENT_REDUCE}')
                                    edited_pixels.append(px_i)
                                    im.pixels_red[px_i] -= RED_COMPONENT_REDUCE
                                # else:
                                #     print(f'Trying to edit pixel {px_i} that was already edited')
    del ft
