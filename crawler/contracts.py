# -*- coding: utf-8 -*-

from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail


class ItemValidateContract(Contract):
    """Itemが期待通りかチェックする

    取得結果は常に変わる可能性があるため、
    不変な値を想定しているのところだけテストするのがいいと思います。
    """
    name = 'item_validate'

    def post_process(self, output):
        item = output[0]
        if 'title' not in item:
            raise ContractFail('title is invalid.')


class CookiesContract(Contract):
    """リクエストに(scrapyの)cookiesを追加するContract

    @cookies key1 value1 key2 value2
    """
    name = 'cookies'

    def adjust_request_args(self, kwargs):
        # self.argsを辞書形式に変換してcookiesにいれる
        kwargs['cookies'] = {t[0]: t[1]
                             for t in zip(self.args[::2], self.args[1::2])}
        return kwargs
