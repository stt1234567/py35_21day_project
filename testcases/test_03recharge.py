"""
充值的前提:登录-->提取token

unittest:
    用例级别的前置: setUp
    测试类级别的前置: setUpClass
        1、提取token,保存为类属性
        2、提取用户id，保存为类属性
    充值测试方法:
        1、动态的替换参数中的用用户id (字符串的replace中的参数要是字符串类型)
"""
import os
import unittest
import requests
from jsonpath import jsonpath
from unittestreport import ddt, list_data
from common.handle_excel import HandleExcel
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.handle_log import stt_log
from common.handle_mysql import HandleDB
from common.tools import replace_data
from testcases.fixture import BaseTest
from common.handle_sign import HandleSign
@ddt
class TestRecharge(unittest.TestCase,BaseTest):
    excel = HandleExcel(os.path.join(DATA_DIR, 'jiekou.xlsx'), 'recharge')
    cases = excel.read_data()
    db = HandleDB()
    @classmethod
    def setUpClass(cls):
        cls.user_login()
        """用例类的前置方法：登录提取token"""
        # 1、请求登录接口，进行登录
        # url = conf.get('env', 'base_url') + '/member/login'
        # params = {
        #     "mobile_phone": conf.get('test_data', 'mobile'),
        #     "pwd": conf.get('test_data', 'pwd')
        # }
        # headers = eval(conf.get('env', 'headers'))
        # responce = requests.post(url=url, headers=headers, json=params)
        # res = responce.json()
        # # 2、登录成功之后再去提取token
        # token = jsonpath(res, '$..token')[0]
        # # 将token添加到请求头中
        # headers['Authorization'] = 'Bearer ' + token
        # # 保存含有token的请求头为类属性
        # cls.headers = headers
        # # setattr(TestRecharge,'headers',headers)
        # # 3、提取用户的id给充值接口使用
        # cls.member_id = jsonpath(res, '$..id')[0]

    @list_data(cases)
    def test_recharge(self, item):
        # 第一步:准备数据
        url = conf.get('env', 'base_url') + item['url']
        # ========================动态替换参数=========================
        # 动态处理需要进行替换的参数
        # item['data'] = item['data'].replace('#member_id#', str(self.member_id))
        item['data'] = replace_data(item['data'],TestRecharge)
        params = eval(item['data'])
        #000000000000000000V3版本的改动00000000000000000000
        par_sign=HandleSign.generate_sign(self.token)
        print("签名和时间戳：", par_sign)
        params.update(par_sign)
        print(params)
        #0000000000000000000V3版本的改动000000000000000000000000000
        # ===========================================================
        expected = eval(item['expected'])
        method = item['method'].lower()
        # &&&&&&&&&&&&&&&&&&&&&&&&请求按口之前查询用户的余额&&&&&&&&&&&&&&&&&&&&&
        sql = 'SELECT leave_amount FROM futureloan.member WHERE mobile_phone="{}"'.format(conf.get("test_data", "mobile"))
        # 执行sql查询余额
        start_amount = self.db.find_one(sql)[0]
        print("用例执行之前用户的余额：", start_amount)

        # 第二步:发送请求，获取接口返回的实际结果
        response = requests.request(method=method, url=url, headers=self.headers, json=params)
        res = response.json()
        # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&请求按口之后查询用户的余额&&&&&&&&&&&&&&&&&&&&&
        # 执行sql查询余额
        end_amount = self.db.find_one(sql)[0]
        print("用例执行之后用户的余额：", end_amount)
        # 第三步;断言
        print("预期结果:", expected)
        print("实际结果:", res)
        try:
            # 断言code和msg字段是否一致
            # self.assertEqual(expected['code'],res['code'])
            # self.assertEqual(expected['msg'], res['msg'])
            self.assertDictIn(expected, res)
            # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&校验数据库中用户余额的变化是否等于充值的金额&&&&&&&&&&&&&&&&&&&&&
            if res['msg'] == "OK":
                # 充值成功，用户余额的变化为充值金额
                self.assertEqual(float(end_amount - start_amount), params['amount'])
            else:
                # 充值失败，用户余额的变化为0
                self.assertEqual(float(end_amount - start_amount), 0)
        except AssertionError as e:
            # 记录日志
            stt_log.error("用例--【{}】---执行失败".format(item['title']))
            # stt_log.error(e)
            stt_log.exception(e)
            # 回写结果到excel(根据公司中实际需求来决定用例结果写不写到excel中)#注:回写excel需要花费大量的时问
            raise e
        else:
            stt_log.info("用例--【{}】---执行成功".format(item['title']))

    def assertDictIn(self, expected, res):
        """字典成员运算的逻辑"""
        for k, v in expected.items():
            if res.get(k) == v:
                pass
            else:
                raise AssertionError("{} not in {}".format(expected, res))
