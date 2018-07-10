# -*- coding: utf-8 -*-
from PIL import Image


class Get_Captcha(object):

    def __init__(self, driver):
        self.driver = driver

    def click_button(self):
        button = self.driver.find_element_by_class_name('geetest_radar_tip')
        button.click()

    def get_slider(self):
        slider = self.driver.find_element_by_class_name('geetest_slider_button')
        return slider

    def get_screenshot(self):
        self.driver.get_screenshot_as_file('test.png')
        screenshot = Image.open('test.png')
        return screenshot

    def get_captcha_position(self):
        img = self.driver.find_element_by_class_name('geetest_canvas_img')
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        return top, bottom, left, right

    def get_captcha_image(self):
        top, bottom, left, right = self.get_captcha_position()
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        return captcha