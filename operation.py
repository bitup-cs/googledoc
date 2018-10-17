# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

class Operation:
    def __init__(self, drvier, url):
        self.driver = drvier
        self.driver.get(url)

    def check_paga_load(self):
        try:
            element = WebDriverWait(self.driver, 30, 0.5).until(
                EC.presence_of_element_located((By.ID, "mG61Hd")))
        except TimeoutError:
            print("page load time out !")
            return False

        return True

    #根据Excel的表头标签值填写表单中的单元格
    def process_input(self, input_para):
        inputs = self.driver.find_elements_by_tag_name('input')
        for input in inputs:
            if input is not None:
                label_name = input.get_attribute('aria-label')
                if label_name is None:
                    continue
                time.sleep(1)
                try:
                    input.send_keys(input_para[label_name])
                except:
                    print('Input fail : ', label_name)

    #点击checkbox，打钩
    def process_checkbox(self):
        labels = self.driver.find_elements_by_tag_name('label')
        for label in labels:
            if label is not None:
                time.sleep(1)
                checkbox = label.find_element_by_tag_name('span')
                ActionChains(self.driver).move_to_element(checkbox).click(checkbox).perform()


    #提交按钮
    def process_submit(self):
        button = self.driver.find_element_by_xpath("//div[@role='button']").find_element_by_tag_name('span')
        button.click()



if __name__ == "__main__":
    from configure import Configuration
    from fake_useragent import UserAgent
    from adsl import Adsl

    conf = Configuration('config.ini')
    ua = UserAgent()

    username, password = conf.get_adsl_user_pass()
    adsl = Adsl(username, password)
    adsl.connect()



    for inputs in conf.get_input_para():
        bw_paras = conf.get_browser_para()
        options = Options()

        if bw_paras['random-useragent']:
            cur_ua = ua.chrome
            options.add_argument("user-agent="+cur_ua)
            print(cur_ua)

        driver = webdriver.Chrome(chrome_options=options)

        with open('result.txt', 'a') as fw:
            try:
                op = Operation(driver, bw_paras['url'])

                op.check_paga_load()

                op.process_checkbox()
                op.process_input(inputs)
                time.sleep(bw_paras['interval'])
                op.process_submit()

            except:
                print("ERROR fail")

            finally:
                driver.quit()
        #重新拨号
        adsl.dial()


