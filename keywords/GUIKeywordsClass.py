# -*- encoding=utf8 -*-
__author__ = "I3089"

from airtest.core.api import *
from airtest.cli.parser import cli_setup
from pathlib import Path
import logging
from base.BaseClass import BaseClass
from xml.etree.ElementTree import tostring
import requests
import urllib.parse
import base64
import json
import re
from lxml import html


class GUIKeywords(BaseClass):

    obj = None

    def __init__(self, obj):
        self.testResults = obj.testResults
        self.currentTest = obj.currentTest
        self.obj = obj

    def setUpConnection(self):
        currentDirectory = str(Path.cwd())
        logger = logging.getLogger("airtest")
        logger.setLevel(logging.ERROR)
        log("123", desc="this is title 01")
        if not cli_setup():
            # auto_setup(__file__, logdir=True, devices=["Android:///", ], project_root=currentDirectory + r'\..\..\log')
            auto_setup(__file__, logdir=True, devices=["Windows:///", ], project_root=currentDirectory + r'\..\..\log')
            # simple_report(__file__,logpath=True,logfile=currentDirectory+r"\log\log.txt",output=currentDirectory+r"\log\Report.html")
            # h1 = LogToHtml(script_root=currentDirectory, log_root=currentDirectory+r"\log", export_dir=currentDirectory ,logfile= currentDirectory+r'\log\log.txt', lang='en', plugins=["poco.utils.airtest.report"])
            # h1.report()

    def startApp(self, AppPath):
        print("Starting the Game - HILL CLIMB RACING")
        clear_app(AppPath)
        start_app(AppPath)
        sleep(12)

    def waitFor(self, imagePath):
        wait(Template(imagePath))

    def stopApp(self, AppPath):
        print("Closing the Game - HILL CLIMB RACING")
        stop_app(AppPath)

    def getCookies(self):

        req = requests.request('GET', 'https://www.imagetotext.info')
        cookie = req.headers['Set-Cookie']
        cookies = {}

        for part in cookie.split(';'):
            if 'XSRF-TOKEN' in part:
                cookies['XSRF-TOKEN'] = part.split('XSRF-TOKEN=')[1]
            if 'laravel_session' in part:
                cookies['laravel_session'] = part.split('laravel_session=')[1]
            if 'imagetotextinfo_session' in part:
                cookies['imagetotextinfo_session'] = part.split('imagetotextinfo_session=')[1]

        doc = html.fromstring(req.content)
        try:
            link = doc.xpath("//head//meta[@name='_token']")[0]
            cookies['x-csrf-token'] = tostring(link).decode().split('content="')[1].split('"')[0]
        except IndexError:
            print("No link found")

        return cookies

    def getTextFromImage(self, imagePath):

        base64Data = None

        cookies = self.getCookies()

        with open(imagePath, "rb") as img_file:
            base64Data = base64.b64encode(img_file.read())

        url = "https://www.imagetotext.info/image-to-text"

        pl = 'base64=data%3Aimage%2Fpng%3Bbase64%2C' + \
             urllib.parse.quote(base64Data)

        payload = pl
        headers = {
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Cookie': '_clck=g0wnhk|1|f95|0; _gid=GA1.2.1042132356.1676441850; _pbjs_userid_consent_data=6683316680106290; _sharedID=3b2c3b90-ca6b-4afc-9c2d-98a55b9eedd5; _sharedID_last=Wed%2C%2015%20Feb%202023%2006%3A17%3A30%20GMT; _lr_env_src_ats=false; __gads=ID=dac87f02f2d55ab9:T=1676441851:S=ALNI_MYZeOTAHS9U7_eL2lv-qyf7aBRjEg; _cc_id=901a8730e5846bf7dacd7f574672a115; panoramaId_expiry=1676528255099; panoramaId=2c139c3e367e5dec81b2daf9aafaa9fb927ae6278ea7e9abf222db0f9d7938d8; _lr_retry_request=true; __gpi=UID=00000bc3e9a47e71:T=1676441851:RT=1676464988:S=ALNI_MZZey8LbvYaa61iifMcG-UOxklTEQ; XSRF-TOKEN=' + cookies['XSRF-TOKEN'] + '; laravel_session=' + cookies['laravel_session'] + '; _ga_KJ1ZFKYBEY=GS1.1.1676464986.3.1.1676465175.0.0.0; _ga=GA1.2.1956691518.1676441848; _clsk=1ctv1sj|1676465177796|2|1|i.clarity.ms/collect; cto_bundle=KIcvqV9nRVBtYnlhOG9HVUslMkYzZEQ0M1FuSkM3Wm9QZG0lMkZRVVdFWEpWa2lWelE4M2VWTlJZV2Q1WWQ2bHgwYVMlMkIxcEozbEdlYkdmZmVQY2s0RUh5OWsyMWplRUllelJWT3dNS0pVTm9kZXZud3Z0cUpSRThVSm5KJTJCWTI4aU5xanJuRFBxRnhrTE5JZyUyQjdUVmhBQklIU3lBdlljJTJCU0FhclQweUg3eGtpeTNick5QTE0lM0Q; TawkConnectionTime=0; twk_uuid_63e5e15cc2f1ac1e203275f4=%7B%22uuid%22%3A%221.2BiI1BuFgaZ5itef0j6VWwN9XP3a1Q7MwQZrDBfTl64Onx9TK3VIsfwFgo2PAGAvgBiLCTrfadXiSRwfz02fsTevP9zfQtxwCF7NLNK1UmWQ1h3T2yb4BfvTOrU%22%2C%22version%22%3A3%2C%22domain%22%3A%22imagetotext.info%22%2C%22ts%22%3A1676465183727%7D',
            'Cookie': '_pbjs_userid_consent_data=6683316680106290; _sharedID=3e9bc2c6-ad54-47fd-b733-691465ca449f; _lr_env_src_ats=false; __gads=ID=a66a297e4620a6ea:T=1676440724:S=ALNI_MYZffY0qoiVehBT66fYjjYetgdh3Q; _cc_id=743a6aa60b4106847af72a77c868eba1; _clck=1klammy|1|f9d|0; _sharedID_last=Thu%2C%2023%20Feb%202023%2009%3A44%3A15%20GMT; _lr_retry_request=true; _gid=GA1.2.1420744678.1677145458; __gpi=UID=00000bc3e905455a:T=1676440724:RT=1677145459:S=ALNI_MY17XtuLik5no6r8RgoGbWsmEh4Fw; panoramaId_expiry=1677231864444; panoramaId=6decb0a04c0d4f926825dd675776a9fb927a022a9d18f224d5e9445688bdb0b8; XSRF-TOKEN=' +
                      cookies['XSRF-TOKEN'] + '; imagetotextinfo_session=' + cookies[
                          'imagetotextinfo_session'] + '; _ga_KJ1ZFKYBEY=GS1.1.1677145454.4.1.1677145861.0.0.0; _ga=GA1.2.372078224.1676440717; _clsk=8qgu8q|1677145863512|3|1|j.clarity.ms/collect; TawkConnectionTime=0; twk_uuid_63e5e15cc2f1ac1e203275f4=%7B%22uuid%22%3A%221.2BiI190k1lHlxKulhA4NEf0lIbBUH5Y27iswwQqpn0NRlUGGWlOBZ7ezIBA0WdYrX6IHey0XBw64ymCOdSjOpmSqYrhtDTZFl1T8jNkFw92iTtAP9s3FWgemTFQ%22%2C%22version%22%3A3%2C%22domain%22%3A%22imagetotext.info%22%2C%22ts%22%3A1677145869435%7D; cto_bundle=4JWjG19oanRQc3VDRGtBZnZXMmJXMkhvVkFPVlVHUG5xUE1Xb2pyQ2NtckZzbUhSYWl6dldDTUUlMkI2TkwlMkJyMWxJRWZmR29wMG53OEdnaWdGTnpLSUlycTRmU253blhSQTlqelRkR2FTbSUyQnhkS2xuQUlydTd3c2ZYa1JzQ0htV29idk1yYUVsQXJ3NkhnYWJvelRDU3ZaMXRpakElM0QlM0Q',
            'Origin': 'https://www.imagetotext.info',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'x-csrf-token': cookies['x-csrf-token'],  # '0CmB1YUOxeWSYAy0oesmZcHCDAMPeSe3isO37DoS',
            'x-requested-with': 'XMLHttpRequest'
        }

        response = requests.request('POST', url, headers=headers, data=payload)

        print(response.text)

        s0 = json.loads(response.text)['text']

        s1 = str('')
        for a in s0.replace('\r', '').split('\n'):
            s1 += re.sub(re.compile(r'''<.*?>'''), '', a) + 'separator'
            s1 = ''.join([i if ord(i) < 128 else '' for i in s1])

        final = [x for x in s1.split('separator') if len(x) > 0]

        return final