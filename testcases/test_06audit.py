"""
审核接口：管理员去审核

审核的前置条件:
    1、管理员登录（类级别的前置)
    2、普通用户的角色添加项目
        1)、普通用户登录（类级别的前置)
        2)、创建一个项目（用例级别的前置）
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
from common.handle_sign import HandleSign
from common.tools import replace_data
from testcases.fixture import BaseTest

@ddt
class TestAudit(unittest.TestCase,BaseTest):
    excel = HandleExcel(os.path.join(DATA_DIR, 'jiekou.xlsx'), 'audit')
    cases = excel.read_data()
    db = HandleDB()

    @classmethod
    def setUpClass(cls) -> None:
        cls.admin_login()
        cls.user_login()
        # url = conf.get('env', 'base_url') + '/member/login'
        # # -------------管理员登陆----------------------------
        # """用例类的前置方法：登录提取token"""
        # # 1、请求登录接口，进行登录
        #
        # params = {
        #     "mobile_phone": conf.get('test_data', 'admin_mobile'),
        #     "pwd": conf.get('test_data', 'admin_pwd')
        # }
        # headers = eval(conf.get('env', 'headers'))
        # responce = requests.post(url=url, headers=headers, json=params)
        # res = responce.json()
        # # 2、登录成功之后再去提取token
        # token = jsonpath(res, '$..token')[0]
        # # 将token添加到请求头中
        # headers['Authorization'] = 'Bearer ' + token
        # # 保存含有token的请求头为类属性
        # cls.admin_headers = headers
        # # setattr(TestRecharge,'headers',headers)
        # # 3、提取用户的id给充值接口使用
        # cls.admin_member_id = jsonpath(res, '$..id')[0]
        # # -------------普通用户登陆----------------------------
        # # 1、请求登录接口，进行登录
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

    def setUp(self) -> None:
        self.add_project()

    @list_data(cases)
    def test_audit(self, item):
        # 第一步:准备数据
        url = conf.get('env', 'base_url') + item['url']
        # ========================动态替换参数=========================
        # 动态处理需要进行替换的参数
        # item['data']=item['data'].replace('#member_id#',str(self.member_id))
        item['data'] = replace_data(item['data'], TestAudit)
        # print(item['data'])
        params = eval(item['data'])
        # 000000000000000000V3版本的改动00000000000000000000
        par_sign = HandleSign.generate_sign(self.admin_token)
        print("签名和时间戳：", par_sign)
        params.update(par_sign)
        print(params)
        # 0000000000000000000V3版本的改动000000000000000000000000000
        # ===========================================================
        expected = eval(item['expected'])
        method = item['method'].lower()
        # 调用接口之前:查询数据库该用户的项目数量
        sql = 'SELECT status FROM futureloan.loan WHERE id={}'.format(self.loan_id)
        start_status = self.db.find_one(sql)
        print("调用项目前的状态：", start_status)
        # 第二步:发送请求，获取接口返回的实际结果
        response = requests.request(method=method, url=url, headers=self.admin_headers, json=params)
        res = response.json()
        # 调用接口之后:查询数据库该用户的项目数量
        end_status = self.db.find_one(sql)
        print("调用项目后的状态：", end_status)
        print(self.loan_id)
        # add_id = str(self.db.find_count(sql)[0])
        # print("项目id为：", add_id)
        # 判断是否是审核通过的用例，并且审核成功，如果是则保存项目id为审核通过的项目id
        if item['title']=='审核通过' and res['msg']=='OK':
            TestAudit.pass_loan_id=params['loan_id']
        # 第三步;断言
        print("预期结果:", expected)
        print("实际结果:", res)
        try:
            # 断言code和msg字段是否一致
            # self.assertEqual(expected['code'],res['code'])
            # self.assertEqual(expected['msg'], res['msg'])
            self.assertDictIn(expected, res)
            # =====================读取excel中有标记成功的==============================
            # 根据添加项目是否成功，来对数据库进分别的校验
            if res['msg'] == "OK":
                # 注册成功
                self.assertNotEqual(start_status, end_status)
                print('审核通过或不通过')
            else:
                self.assertEqual(start_status, end_status)
                print('审核错误')
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