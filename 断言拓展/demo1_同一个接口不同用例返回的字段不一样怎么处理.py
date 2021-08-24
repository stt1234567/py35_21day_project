#同一个接口不同用例返回的字段不一样怎么处理
import unittest
class TestDome(unittest.TestCase):
    def test_demo(self):
        #实际结果
        res = { "code":0,"msg":"OK","time":'20201212'}
        #预期结果
        expected = {"code" : 0,"msg" :"OK"}
        # assert res['code']==expected['code']
        # assert res['msg']==expected['code']
        self.assertDictIn(expected,res)

    def assertDictIn(self, expected, res):
        """字典成员运算的逻辑"""
        for k, v in expected.items():
            if res.get(k) == v:
                pass
            else:
                raise AssertionError("{} not in {}".format(expected,res))
