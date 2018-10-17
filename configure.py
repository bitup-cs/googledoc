# -*- coding: utf-8 -*-
import xlrd
import configparser


class Configuration:
    def __init__(self, file):
        self.cf = configparser.ConfigParser()
        self.cf.read(file, encoding='utf-8')

    def get_adsl_user_pass(self):
        username, password = None, None
        try:
            username = self.cf.get('adsl', 'username')
            password = self.cf.get('adsl', 'password')
        except:
            print("请在config.ini填写adsl username和adsl password")

        return username, password

    def get_browser_para(self):
        bw_paras = {}
        bw_paras['url'] = self.cf.get('browser', 'url')
        if self.cf.get('browser', 'random-useragent') == 'true':
            bw_paras['random-useragent'] = True
        else:
            bw_paras['random-useragent'] = False

        bw_paras['interval'] = int(self.cf.get('browser', 'interval'))

        return bw_paras

    def get_input_para(self):
        try:
            f_name = self.cf.get('input', 'file')
        except:
            print("请在cofnig.ini填写input file")

        try:
            book = xlrd.open_workbook(f_name)
        except:
            print("请在config.ini中填写正确的input file名称")

        sheet = book.sheet_by_index(0)

        cols_label = {}
        for col_index in range(0, sheet.ncols):
            cols_label[col_index] = sheet.cell(0, col_index).value

        input_para = {}
        for row_index in range(1, sheet.nrows):
            for col_index in range(0, sheet.ncols):
                input_para[cols_label[col_index]] = sheet.cell(row_index, col_index).value
            yield input_para


if __name__ == "__main__":
    import pprint
    conf = Configuration('config.ini')

    print(conf.get_adsl_user_pass())

    for x in conf.get_input_para():
        pprint.pprint(x)

