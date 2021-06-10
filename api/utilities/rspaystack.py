import os
import requests
from requests.exceptions import (
    HTTPError,
    Timeout,
)


class RSPaystack:
    """
    Paystack payment Verification class for python app
    by Rastaarc
    """
    __CONTENT_TYPE = 'application/json'
    __PAYSTACK_VERIFY_ENDPOINT = 'https://api.paystack.co/transaction/verify/'

    def __init__(self, auth_key=None):
        if auth_key:
            self.__AUTH_KEY = auth_key

        else:
            self.__AUTH_KEY = os.getenv('PAYSTACK_AUTH_KEY', None)

        if not self.__AUTH_KEY:
            raise Exception("Paystack Authentication Key Missing")

    def __headers(self):
        return {
            "Content-Type": self.__CONTENT_TYPE,
            "Authorization": f"Bearer {self.__AUTH_KEY}",
            "user-agent": "Paystack-payment-verification-by-Rastaarc-for-python",
        }

    def __dump_payload(self, response_obj):
        payload = response_obj.json()

        status = payload.get("status", None)
        msg = payload.get("message", None)
        data = payload.get("data", None)

        return {'status': status, 'msg': msg, 'data': data}

    def verify(self, reference):
        """
        Verifies a transaction using the provided reference number

        args:
        reference -- reference of the transaction to verify
        error --- error message
        """
        error = ""

        if not reference:
            raise Exception("Reference Number Missing")

        try:
            url = f'{self.__PAYSTACK_VERIFY_ENDPOINT}{str(reference)}'
            resp = requests.get(url, headers=self.__headers(), timeout=(5, 9))

            rstatus = resp.status_code
            if rstatus == 404:
                raise Exception("Request not found")

        except HTTPError as http_err:
            error = f'HTTP Error: {http_err}'
            print(error)

        except Timeout:
            error = 'The Request timed out'
            print(error)

        except Exception as err:
            error = f'Error Occured: {err}'
            print(error)

        else:
            payload = self.__dump_payload(resp)
            return payload

        return {"error": error}


"""
###Test###
p = RSPaystack('sk_test_f83558740705a906961bb24e9c2c156ee7a8afda')

v = p.verify('MathsNet-REF-mupdz7fYQI8ROOZzRjLj')


if v["status"] and v["data"]["status"] == "success" and v["msg"] == "Verification successful":
    print("yes")
else:
    print("Noe")
"""
