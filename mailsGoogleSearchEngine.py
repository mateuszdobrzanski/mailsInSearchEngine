import re
import time
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
from googlesearch import search
import requests
import urllib
import urllib3
from urllib.request import Request, urlopen
import certifi
import ssl

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass


class TLSAdapter(requests.adapters.HTTPAdapter):

    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = ctx
        return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)


def emails_by_domain(domain):
    # to search
    query = "@" + domain

    EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+\\=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\\=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
    # EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    final_list = []

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }

    for j in search(query, tld="pl", num=10, stop=30, pause=5):
        cleaned_emails = []
        message = ""
        print(j)
        try:
            session = requests.session()
            session.mount('https://', TLSAdapter())

            req = urllib.request.Request(j, headers=header)

            if "tiktok" in j:
                message = "Error, weird page"
            else:
                try:
                    response = urllib.request.urlopen(req, context=ssl.create_default_context(cafile=certifi.where()))
                    try:
                        page = response.read().decode('utf-8')
                        get_emails = re.findall(EMAIL_REGEX, page)
                    except:
                        get_emails = re.findall(EMAIL_REGEX, response.read())

                    # page = response.read().decode('utf-8')
                    # get_emails = re.findall(EMAIL_REGEX, page)
                    cleaned_emails = list(dict.fromkeys(get_emails))

                    print(cleaned_emails)
                except Exception as ex:
                    # print("<<<<<<ERROR>>>>>>>")
                    # print(response.read())
                    template = "Error! An exception of type {0} occurred. Arguments:{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    # print("<<<<<<ERROR>>>>>>>")
                    # print(message)
                    # print("<<<<<<ERROR>>>>>>>")


        except Exception as ex:
            template = "Error! An exception of type {0} occurred. Arguments:{1!r}"
            message = template.format(type(ex).__name__, ex.args)

        dictionary = {
            "page": j,
            "emails": cleaned_emails,
            "error": message
        }
        final_list.append(dictionary)

        time.sleep(15)

    return final_list
