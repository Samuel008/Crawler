# -*- coding: utf-8 -*-


class Get_Gap(object):

    def compare_pixel(self, image1, image2, x, y):
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]

        check_value = 40
        if abs(pixel1[0] - pixel2[0]) < check_value and abs(pixel1[1] - pixel2[1]) < check_value and abs(pixel1[2] - pixel2[2]) < check_value:
            return True
        else:
            return False

    def get_gap(self, image1, image2):

        left = 60
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.compare_pixel(image1, image2, i, j):
                    left = i
                    return left
        # return left
