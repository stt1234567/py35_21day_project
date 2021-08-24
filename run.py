import unittest
from unittestreport import TestRunner
from common.handle_path import CASES_DIR, REPORT_DIR
from unittestreport.core.sendEmail import SendEmail


def main():
    # 程序的入口函数
    suite = unittest.defaultTestLoader.discover(CASES_DIR)

    runner = TestRunner(suite,
                        filename="report.html",
                        report_dir=REPORT_DIR,
                        tester='邵婷婷',
                        title='。。。的测试报告')

    runner.run()
    # 将测试结果发到邮箱
    # runner.send_email(host='smtp.qq.com',
    #                   port=465,
    #                   user='musen_nmb@qq.com',
    #                   password='algmmzptupjccbab',
    #                   to_addrs='1071689010@qq.com',
    #                   # to_addrs=[...qq.com,...qq.com,...qq.com]
    #                   is_file=True)
    # 测试结果推送到钉钉群
    # webhook = 'https://oapi.dingtalk.com/robot/send?access_token=118b3c8692ccd4d153ad635c5dc3463b97d2a53e5a283a76526331719be43a02'
    # runner.dingtalk_notice(url=webhook, key='测试')
    # 企业微信通知-----参照企业微信官方的API平台-------


# ---------扩展自定义邮件的标题和内容--------------
# em = SendEmail(host='smtp.qq.com',
#                port=465,
#                user='musen_nmb@qq.com',
#                password='algmmzptupjccbab')
# em.send_email(self, subject="测试报告", content=None, filename=None, to_addrs=None)

if __name__ == '__main__':
    main()

"""
扩展知识讲解:
一、测试结果的推送
    1、通过邮件发生到相关人员邮箱
    2、推送测试结果到钉钉群

"""
