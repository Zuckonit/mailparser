#!/usr/bin/env python
# encoding: utf-8


"""
    查看email源码， 发现email这个标准库解析邮件头的时候， 暴露的接口只返回第一个邮件地址。
    当收件人有多个的时候， 没法得到所有的收件地址, 所以这里我自己封装下

    ~~~~~~~~~~
    mailparser.py
"""


import logging
import functools
import email
from email._parseaddr import AddressList as _AddressList


def _log_on_error(default=False):
    logger = logging.getLogger(__name__)
    def func(f):
        @functools.wraps(f)
        def _func(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                log = '{0} error: {1}'.format(f.__name__, e)
                print log
                logger.error(log)
                return default
        return _func
    return func


class ParseHeader(object):
    def __init__(self, header):
        header = r"%s"%header
        header = header.encode('utf-8')
        self.msg = email.message_from_string(header)
    
    @_log_on_error(default=None)
    def get_email_from(self):
        efrom = _AddressList(self.msg.get("from")).addresslist
        return efrom[0][1]
    
    @_log_on_error(default=[])
    def get_email_to(self, unique=True):
        etos = _AddressList(self.msg.get("to")).addresslist
        etos = [e[1] for e in etos]
        return list(set(etos)) if unique else etos
    
    @_log_on_error(default=[])
    def get_email_cc(self, unique=True):
        ccs = _AddressList(self.msg.get("cc")).addresslist
        ccs =  [c[1] for c in ccs]
        return list(set(ccs)) if unique else ccs
    
    @_log_on_error(default=[])
    def get_cc_to(self, unique=True):
        to = self.get_email_to(unique=False)
        cc = self.get_email_cc(unique=False)
        to.extend(cc)
        return list(set(to)) if unique else to

    @_log_on_error(default='')
    def get_subject(self):
        subj = self.msg.get('subject')
        return subj


if __name__ == '__main__':
    header = u'X-Account-Key: account1\r\nX-UIDL: ZC4706-sq0K95C_dbf_wVoKxWyYG29\r\nX-Mozilla-Status: 0001\r\nX-Mozilla-Status2: 10000000\r\nX-Mozilla-Keys:  \r\nX-QQ-mid: Yesmtp11t1346908060t416t1211\r\nReceived: from bigseaPC (unknown [222.95.243.130])\tby esmtp4.qq.com (ESMTP) with SMTP id 0\tfor <list_everyone@test.com>; Thu, 06 Sep 2012 13:07:39 +0800 (CST)\r\nX-QQ-SSF: 00010000000000F0FxF200000000000\r\nFrom:\u5434\u6668\u6656 <test@test.com>\r\nTo: <list_everyone@test.com>\r\nSubject:\u3010\u7fbd\u6bdb\u7403\u6bd4\u8d5b\u3011\r\nDate: Thu, 6 Sep 2012 13:07:39 +0800\r\nMessage-ID: <002501cd8bed$89a4c780$9cee5680$@test.com>\r\nMIME-Version: 1.0\r\nContent-Type: multipart/mixed;\tboundary="----=_NextPart_000_0026_01CD8C30.97C80780"\r\nX-Mailer: Microsoft Outlook 14.0\r\nThread-Index: Ac2L7ElOSevHm0QbQJWRKIvXeM8sNQ==\r\nContent-Language: zh-cn\r\n'
    p = ParseHeader(header)
    print p.get_email_from()
    print p.get_email_to()
    print p.get_email_cc()
    print p.get_cc_to()
    print p.get_subject()
