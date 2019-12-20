"""
@author '彼时思默'
@time 2019/12/7 15:54
@describe:
  访问百度api来实现ocr
"""
import json
import sys
import requests
from loguru import logger
from root import *
import arrow
from requests import adapters

class Baidu:
    def __init__(self):
        self.token=self.baidu_token()
        adapter = adapters.HTTPAdapter(max_retries=3)
        self.s=requests.session()
        # 告诉requests，http协议和https协议都使用这个适配器
        self.s.mount('http://', adapter)
        self.s.mount('https://', adapter)


    def baidu_token(self):
        token_file_path = os.path.join(root, 'config/baidu_token.josn')
        now_timestamp = arrow.now().timestamp
        if os.path.exists(token_file_path):  # 如果存在token文件
            logger.debug('从文件读取Token')
            with open(token_file_path)as file:
                token_data = json.load(file)
            if token_data['end_timestamp'] > now_timestamp:  # 如果token未过期
                logger.debug('Token未过期')
                return token_data['token']
        #  不存在文件或者token过期
        logger.debug('Token过期,重新申请')
        api_id = 'b7ohindzenMGRKIBmX26MP1q'
        secret_key = 'xtlFNWtyW4NLlwaMiLsDt5ZyFs9GoH92'
        token_url = 'https://aip.baidubce.com/oauth/2.0/token'
        params = {'grant_type': 'client_credentials', 'client_id': api_id, 'client_secret': secret_key}
        r = self.s.get(token_url, params=params).json()
        token = r['access_token']
        valid = r['expires_in']
        end_timestamp = valid + now_timestamp
        logger.debug(token)
        store_data = {'token': token, 'end_timestamp': end_timestamp}
        with open(token_file_path, 'w')as file:
            json.dump(store_data, file)
        return token

    def baidu_ocr(self, img_base64):
        logger.debug(sys.getsizeof(img_base64))
        url = f'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        params = {'access_token': self.token}
        data = {'image': img_base64}
        r = requests.post(url, data, params=params, headers=headers).json()
        result = ''
        try:
            words_result = r['words_result']
            for word in words_result:
                result+=word['words']
        except:
            logger.error(r)
        return result


baidu = Baidu()
