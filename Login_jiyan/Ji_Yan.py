# -*- coding: utf-8 -*-
from selenium import webdriver
from PIL import Image
import time
from get_gap import Get_Gap
from get_track import Get_Track
from get_captcha import Get_Captcha
from selenium.webdriver import ActionChains


class CrackGeetest(object):
    def __init__(self):
        self.url = r'https://auth.geetest.com/login'
        self.email = '879633186@qq.com'
        self.password = '879633186s'
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.get_gap = Get_Gap()
        self.get_track = Get_Track()
        self.get_captcha = Get_Captcha(self.driver)

    def move_to_gap(self, slider, track):
        ActionChains(self.driver).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.driver).release().perform()

    def input(self):
        self.driver.get(self.url)
        time.sleep(5)
        self.driver.find_element_by_xpath('//input[@type="email"]').send_keys(self.email)
        self.driver.find_element_by_xpath('//input[@type="password"]').send_keys(self.password)

    def login(self):
        self.driver.find_element_by_class_name('btn-text').click()

    def main(self):
        self.input()
        self.get_captcha.click_button()
        time.sleep(5)
        image1 = self.get_captcha.get_captcha_image()
        slider = self.get_captcha.get_slider()
        slider.click()
        time.sleep(5)
        image2 = self.get_captcha.get_captcha_image()
        image1.save('captcha1.png')
        image2.save('captcha2.png')

        gap = self.get_gap.get_gap(image1, image2)
        print('缺口位置：', gap)
        gap = gap - 6

        track = self.get_track.get_track(gap)

        self.move_to_gap(slider, track)
        time.sleep(3)
        if not self.driver.find_element_by_xpath('//span[text()="验证成功"]'):
            print('fail')
        else:
            print('success')
            self.login()

if __name__ == "__main__":
    test = CrackGeetest()
    test.main()




