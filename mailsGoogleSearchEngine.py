import re
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from googlesearch import search
import requests

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass


def emails_by_domain(domain):

    # to search
    query = "@" + domain

    # EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+\\=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\\=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
    EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    final_list = []

    for j in search(query, tld="pl", num=10, stop=10, pause=5):
        page = requests.get(j, verify=False)
        get_emails = re.findall(EMAIL_REGEX, page.text)
        cleaned_emails = list(dict.fromkeys(get_emails))
        dictionary = {
            "page": j,
            "emails": cleaned_emails
        }
        final_list.append(dictionary)

    return final_list
