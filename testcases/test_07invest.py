"""
前置操作:
    1、普通用户登录（类级别)
    2、管理员登录（类级别)
    3、添加项目（类级别)
    4、审核项目(类级别)
    self是实例方法的第一个参数，代表的是实例对象本身
    cls是类方法的第一个参数，代表的是类的本身
用例方法:
    1、准备数据
    2、发生请求
    3、断言
用例前置操作的封装优化:
    1、把多个用例要使用的一些前置步骤封装到一个类中
    2、需要使用这些前置步骤的测试类，直接去继承（多继承）咱们封装好的前置步骤方法
    3、在类级别的前和用例级别的前置中，调用对应的前置方法即可


    #数据校验
        用户表:用户的余额投资前后会变化
            投资前-投资后==投资的金额
        流水记录表:投资成功会新增一条流水记录
            投资后用户流水记录数量-投资前用户流水记录数量==1
        投资表:投资成功会新增一条投资记录
            投资后用户的记录数量-投资前用户的记录数量==1
    --扩展投资后（可投金额为0）满标的情况，会生成回款计划------
        1、先把项目的投资记录id都查询出来
        2、遍历投资记录id
        3、根据每个投资记录的id去查询是否生成回款计划表:



"""

import unittest
import os
import requests
from jsonpath import jsonpath
from unittestreport import ddt, list_data
from common.handle_excel import HandleExcel
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.handle_sign import HandleSign
from common.tools import replace_data
from common.handle_mysql import HandleDB
from common.handle_log import stt_log
from testcases.fixture import BaseTest

@ddt
class TestInvest(unittest.TestCase,BaseTest):
    excel = HandleExcel(os.path.join(DATA_DIR, 'jiekou.xlsx'), 'invest')
    cases = excel.read_data()
    db = HandleDB()

    @classmethod
    def setUpClass(cls) -> None:
        cls.admin_login()
        cls.user_login()
        cls.add_project()
        cls.invest_project()


    @list_data(cases)
    def test_invest(self, item):
        url = conf.get('env', 'base_url') + item['url']
        item['data'] = replace_data(item['data'], TestInvest)
        params = eval(item['data'])
        # 000000000000000000V3版本的改动00000000000000000000
        par_sign = HandleSign.generate_sign(self.token)
        print("签名和时间戳：", par_sign)
        params.update(par_sign)
        print(params)
        # 0000000000000000000V3版本的改动000000000000000000000000000
        expected = eval(item['expected'])
        method = item['method'].lower()
        #用户
        sql = 'SELECT leave_amount FROM futureloan.member WHERE id="{}"'.format(self.member_id)
        #投资
        sql2 = 'SELECT * FROM futureloan.invest WHERE member_id="{}"'.format(self.member_id)
        #流水
        sql3 = 'SELECT * FROM futureloan.financelog WHERE pay_member_id="{}"'.format(self.member_id)
        start_amount = self.db.find_one(sql)[0]
        start_invest_mount = self.db.find_count(sql2)
        start_financelog_mount = self.db.find_count(sql3)
        print("投资前用户的余额：", start_amount)
        response = requests.request(method=method, url=url, json=params, headers=self.headers)
        res = response.json()
        end_amount = self.db.find_one(sql)[0]
        print("投资后用户的余额：", end_amount)
        print("预期结果：", expected)
        print("实际结果：", res)
        end_invest_mount = self.db.find_count(sql2)
        end_financelog_mount = self.db.find_count(sql3)
        try:
            # self.asserDicIn(expected, res)
            self.assertEqual(expected['code'],res['code'])
            self.assertIn(expected['msg'],res['msg'])
            if res['msg'] == 'OK':
                self.assertEqual(float(start_amount - end_amount), params['amount'])
                self.assertEqual(end_invest_mount - start_invest_mount,1)
                self.assertEqual(end_financelog_mount - start_financelog_mount, 1)
            else:
                self.assertEqual(start_amount,end_amount)
        except AssertionError as e:
            stt_log.error("用例--------【{}】---------执行失败".format(item['title']))
            stt_log.exception(e)
            raise e
        else:
            stt_log.info("用例--------【{}】---------执行成功".format(item['title']))

    def asserDicIn(self, expected, res):
        for k, v in expected.items():
            if res.get(k) == v:
                pass
            else:
                raise AssertionError('{} is not {}'.format(expected, res))
