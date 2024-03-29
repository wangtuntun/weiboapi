# -*- coding:utf-8 -*-
"""
:Author: Rossi
:Date: 2016-01-24

This module contains some utility functions.
"""
import base64
import time
import rsa
import binascii
try:
    from urllib import quote
except:
    from urllib.request import quote
from bs4 import BeautifulSoup
import json
import re


OK = 200


def quote_base64_encode(text):
    """
    Quoting and encoding string using base64 encoding.
    """
    quote_text = quote(text)
    quote_text = base64.b64encode(bytearray(quote_text, 'utf-8'))
    return quote(quote_text)


def base64_encode(text):
    return base64.b64encode(bytearray(text, 'utf-8')).decode('utf-8')


def get_systemtime():
    """
    Getting system time
    """
    t = str(time.time())
    t = t.replace(".", "")[:-3]
    return t


def check_status(r):
    return r.status_code == OK


def check_code(data):
    """
    Checking the response code. If the request is handled correctly,
    the code would be '100000'.

    :param data str: the data returned by the server, which is in json format.
    """
    json_data = json.loads(data)
    if json_data["code"] == "100000":
        return True
    else:
        return False


def decode(data, charset=None):
    """
    Decoding a bytes object.

    :param data bytes: the data to decode.

    :param charset str: the specified charset
    """
    if isinstance(data, bytes):
        if not charset:
            return data.decode("utf-8")
        else:
            return data.decode(charset)
    else:
        return data


def encrypt_password(p, st, nonce, pk, rsakv):
    """
    Encrypting the password using rsa algorithm.
    p: password
    st: server time
    nonce: random value
    pk: public key
    rsakv: rsa key value
    """
    pk = '0x' + pk
    pk = int(pk, 16)
    msg = str(st) + '\t' + str(nonce) + '\n' + p
    key = rsa.PublicKey(pk, 65537)
    psw = rsa.encrypt(msg.encode("utf-8"), key)
    psw = binascii.b2a_hex(psw)
    return decode(psw)


def timestamp_to_date(timestamp):
    """
    Converting timestamp to date.
    """
    ltime = time.localtime(timestamp)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", ltime)
    return time_str


def extract_script(html):
    """
    Extracting scripts from html.
    """
    soup = BeautifulSoup(html, "lxml")
    scripts = soup.find_all('script')
    return scripts


p = re.compile("\(({.+})\)")


def extract_html_from_script(text):
    """
    Extracting html from script text.
    """
    # begin = len('FM.view(')
    # end = len(text) - len(')')
    # json_data = json.loads(text[begin: end])
    # doc = json_data['html']
    # return doc
    match = p.search(text)
    json_data = json.loads(match.groups()[0])
    doc = json_data['html']
    return doc


def select_script(scripts, flag):
    """
    Selecting a script block according to the given flag.
    scripts: the script blocks
    flag: the given flag which is a string.
    """
    for script in scripts:
        text = script.text.strip()
        if text.find(flag) != -1:
            return script


def clean_text(text):
    text = text.strip()
    text = text.replace("\t", "")
    text = text.replace("\r", "")
    text = text.replace("\n", " ")
    text = text.replace("  ", " ")
    return text


p = re.compile('\((.*)\)')


def get_json(data):
    """
    Extracting json data from the given string.
    """
    json_data = p.search(data).group(1)
    json_data = json.loads(json_data)
    return json_data
