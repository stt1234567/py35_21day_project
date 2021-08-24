import requests
from jsonpath import jsonpath
from common.handle_conf import conf
from common.handle_sign import HandleSign
class BaseTest:
    @classmethod
    def admin_login(cls):
        # -------------管理员登录---------------------------
        url = conf.get('env', 'base_url') + '/member/login'
        params = {
            "mobile_phone": conf.get('test_data', 'admin_mobile'),
            "pwd": conf.get('test_data', 'admin_pwd')
        }
        headers = eval(conf.get('env', 'headers'))
        responce = requests.post(url=url, json=params, headers=headers)
        res = responce.json()
        cls.admin_token = jsonpath(res, '$..token')[0]
        headers['Authorization'] = 'Bearer ' + cls.admin_token
        cls.admin_headers = headers
        cls.admin_member_id = jsonpath(res, '$..id')[0]

    @classmethod
    def user_login(cls):
        # -------------用户登录---------------------------
        url = conf.get('env', 'base_url') + '/member/login'
        params = {
            "mobile_phone": conf.get('test_data', 'mobile'),
            "pwd": conf.get('test_data', 'pwd')
        }
        headers = eval(conf.get('env', 'headers'))
        responce = requests.post(url=url, json=params, headers=headers)
        res = responce.json()
        cls.token = jsonpath(res, '$..token')[0]
        headers['Authorization'] = 'Bearer ' + cls.token
        cls.headers = headers
        cls.member_id = jsonpath(res, '$..id')[0]

    @classmethod
    def add_project(cls):
        # -----------创建项目获取项目id------------------------
        url = conf.get('env', 'base_url') + '/loan/add'
        params = {
            "member_id": cls.member_id,
            "title": "报名 Java 全栈自动化课程",
            "amount": 6300.00,
            "loan_rate": 12.0,
            "loan_term": 12,
            "loan_date_type": 1,
            "bidding_days": 5
        }
        # 000000000000000000V3版本的改动00000000000000000000
        par_sign = HandleSign.generate_sign(cls.token)
        print("签名和时间戳：", par_sign)
        params.update(par_sign)
        print(params)
        # 0000000000000000000V3版本的改动000000000000000000000000000
        response = requests.post(url=url, json=params, headers=cls.headers)
        res = response.json()
        cls.loan_id = jsonpath(res, '$..id')[0]

    @classmethod
    def invest_project(cls):
        # -------------管理员通过项目---------------------------
        url = conf.get('env', 'base_url') + '/loan/audit'
        params = {
            "loan_id": cls.loan_id,
            "approved_or_not": True
        }
        # 000000000000000000V3版本的改动00000000000000000000
        par_sign = HandleSign.generate_sign(cls.admin_token)
        print("签名和时间戳：", par_sign)
        params.update(par_sign)
        print(params)
        # 0000000000000000000V3版本的改动000000000000000000000000000
        requests.patch(url=url, json=params, headers=cls.admin_headers)
