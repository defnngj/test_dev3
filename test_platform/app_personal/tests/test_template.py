import unittest
from time import sleep
from selenium import webdriver
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class LoginUITEst(StaticLiveServerTestCase):

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_login_null(self):
        self.driver.get(self.live_server_url + '/login/')
        self.driver.find_element_by_name("username").send_keys("")
        self.driver.find_element_by_name("password").send_keys("")
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        sleep(1)
        error = self.driver.find_element_by_id("hint").text
        self.assertEqual(error, "用户名或密码为空！")

    def test_login_error(self):
        self.driver.get(self.live_server_url + '/login/')
        self.driver.find_element_by_name("username").send_keys("user")
        self.driver.find_element_by_name("password").send_keys("abc1234")
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        sleep(1)
        error = self.driver.find_element_by_id("hint").text
        self.assertEqual(error, "用户名或密码错误！")

    def test_login(self):
        self.driver.get(self.live_server_url + '/login/')
        self.driver.find_element_by_name("username").send_keys("admin")
        self.driver.find_element_by_name("password").send_keys("admin123456")
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        sleep(3)
        user = self.driver.find_element_by_xpath("//span[@class='text-dark']").text
        self.assertEqual(user, "admin")


class ProjectUITEst(StaticLiveServerTestCase):

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    # def tearDown(self):
    #     self.driver.quit()

    def test_add_project(self):
        self.driver.get(self.live_server_url + '/login/')
        self.driver.find_element_by_name("username").send_keys("admin")
        self.driver.find_element_by_name("password").send_keys("admin123456")
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        sleep(3)
        self.driver.find_element_by_xpath("//button[text()='创建']").click()
        sleep(2)
        self.driver.find_element_by_id("id_name").send_keys("测试项目")
        self.driver.find_element_by_id("id_describe").send_keys("测试项目的描述")
        self.driver.find_element_by_id("id_status").click()
        self.driver.find_element_by_xpath("//input[@type='submit']").click()
        sleep(2)
        project_name = self.driver.find_element_by_xpath("//tbody/tr/td[2]").text
        print(project_name)
        self.assertEqual(project_name, "测试项目")


