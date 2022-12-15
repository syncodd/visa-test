import datetime
import hashlib
import hmac
from calendar import timegm

import requests

class VisaPayment():

    def __init__(self, timeout=10, api_key=None, shared_secret=None):

        self.timeout = timeout

        self.api_key = api_key if api_key else 'T43MPQCZL9YO67OPRHE821C6s0tA9sWwsEWIyfmpXZU_qzWVs'
        self.shared_secret = shared_secret if shared_secret else 'odtll9sm1zMrDKvOvSzgYg/9QT{1EJGm0JFyqrY-'
    

    def getXPayToken(self, resource_path, query_string, body):

        secret = bytes(self.shared_secret, 'utf-8')
        timestamp = str(timegm(datetime.datetime.utcnow().timetuple()))
        pre_hash_string = bytes(timestamp + resource_path + query_string + body, 'utf-8')

        hash_string = hmac.new(secret, pre_hash_string, digestmod=hashlib.sha256).hexdigest()
        x_pay_token = 'xv2:' + timestamp + ':' + hash_string

        return x_pay_token
    
    def hello_world(self):

        url = 'https://sandbox.api.visa.com/vdp/helloworld'

        query_string = "apiKey=" + self.api_key
        resource_path = "helloworld"
        body = ""

        return self.get(url, query_string, resource_path, body)

    def get(self, url, query_string, resource_path, body):

        x_pay_token = self.getXPayToken(resource_path, query_string, body)
        headers = {'x-pay-token': x_pay_token}

        try:
            response = requests.get(url + '?' + query_string,
                                    headers=headers,
                                    timeout=self.timeout
                                    )
        except Exception as e:
            print(e)
            return

        return response.json()


if __name__ == '__main__':

    visa = VisaPayment()
    hw = visa.hello_world()

    print(hw)