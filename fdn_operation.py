# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

class FDN_Operation:
    def __init__(self, drvier, url):
        self.driver = drvier
        self.driver.get(url)

    def check_paga_load(self):
        try:
            element = WebDriverWait(self.driver, 30, 0.5).until(
                EC.presence_of_element_located((By.ID, "fid")))
        except TimeoutError:
            print("page load time out !")
            return False

        return True

    #根据Excel的表头标签值填写表单中的单元格
    def process_input(self, input_para):
        inputs = self.driver.find_elements_by_tag_name('input')
        for input in inputs:
            if input is not None:
                hide = input.get_attribute('type')
                if hide == 'hidden':
                    continue
                label_name = input.get_attribute('name')
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

    def get_checkcode_img(self, xpath):
        self.driver.save_screenshot('printscreen.png')
        imgelement = self.driver.find_element_by_xpath(xpath)  # 定位验证码
        location = imgelement.location  # 获取验证码x,y轴坐标
        size = imgelement.size  # 获取验证码的长宽
        print(' localtion :',location, ' size :',size)
        rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
                  int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
        i = Image.open("printscreen.png")  # 打开截图
        i = i.convert("RGB")
        frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
        frame4.save('save.jpg')  # 保存我们接下来的验证码图片 进行打码


    #提交按钮
    def process_submit(self):
        button = self.driver.find_element_by_xpath("//a[@class='getcandy']")
        button.click()


if __name__ == "__main__":
    from configure import Configuration
    from fake_useragent import UserAgent
    from adsl import Adsl


    conf = Configuration('config.ini')
    ua = UserAgent()

    #首次拨号
    # username, password = conf.get_adsl_user_pass()
    # adsl = Adsl(username, password)
    # adsl.connect()

    # ruokuai_para = conf.get_ruokuai_para()
    # check_oper = CheckCode(ruokuai_para['username'], ruokuai_para['password'],ruokuai_para['softid'], ruokuai_para['softkey'], ruokuai_para['typeid'])


    for inputs in conf.get_input_para():
        bw_paras = conf.get_browser_para()
        options = Options()

        if bw_paras['random-useragent']:
            cur_ua = ua.chrome
            options.add_argument("user-agent="+cur_ua)
            print(cur_ua)

        driver = webdriver.Chrome(chrome_options=options)
        driver.maximize_window()

        with open('result.txt', 'a') as fw:
            try:
                op = FDN_Operation(driver, bw_paras['url'])

                op.check_paga_load()
                # op.get_checkcode_img('//*[@id="checkcode"]')
                # checkcode = check_oper.get_checkcode_byfile('save.jpg')
                # inputs['Verify Code'] = checkcode['Result']
                op.process_checkbox()
                op.process_input(inputs)

                op.process_submit()
                time.sleep(bw_paras['interval'])

            except:
                print("ERROR fail")

            finally:
                driver.quit()
        #重新拨号
        # adsl.dial()