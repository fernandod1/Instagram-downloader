#!/usr/bin/env python3.5

# Copyright (c) 2019 Fernando
# Url: https://github.com/dlfernando/
# License: MIT

import sys
import requests
import time
import urllib.request
import os

# Set public instagram username you want to download photos from (Example: ladygaga):
instagram_username = "SET_INSTAGRAM_USERNAME"


def get_user_id(html):
    return html.json()["graphql"]["user"]["id"]

def get_total_photos(html):
    return int(html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["count"])

def create_download_directory(instagram_username):
    try:
        os.mkdir(instagram_username)
        print("Directory ", instagram_username, " Created ")
    except FileExistsError:
        print("Directory ", instagram_username, " already exists")

def remove_temp_file():
    ## Try to delete resume.txt file when all content downloaded ##
    try:
        os.remove("resume.txt")
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


def download_photos(instagram_username,user_id,nextpagcode,pag):
    filename = instagram_username
    url = "https://gramsave.com/media"
    data = {"username": instagram_username, "userid": user_id, "page": nextpagcode}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, json=data, headers=headers)
    i = 0
    for match in r.json()["media"]:
        print(match["download_src"])
        if 'mp4' in match["download_src"]:
            filename = instagram_username + "/" + str(pag) + "_" + str(i) + ".mp4"
        else:
            filename = instagram_username + "/" + str(pag) + "_" + str(i) + ".jpg"
            try:
                urllib.request.urlretrieve(match["download_src"], filename)
            except urllib.error.HTTPError as e:
                print(str(e.code) + " Can't download file")
                
        i = i + 1
    return r.json()["next_page"]

# --------------------------------- Main program -------------------------------------#

def main():
    global instagram_username
    create_download_directory(instagram_username)
    html = requests.get("https://www.instagram.com/" + instagram_username + "/?__a=1")
    nexttoken = ""
    pag = 0
    totalpages=int(get_total_photos(html)/13)
    if totalpages==0:
        totalpages=1
    user_id=int(get_user_id(html))
    try:
        with open("resume.txt") as f_obj:
            lines = f_obj.readlines()
            pag = int(lines[0])
            nexttoken = lines[1]
    except FileNotFoundError:
        print("resume.txt temporary file created.")
    print("--->" + instagram_username + "<---")
    print("--->" + str(user_id) + "<---")
    print("--->" + nexttoken + "<---")
    print("--->" + str(pag) + "<---")
    while pag<totalpages:
        nexttoken = download_photos(instagram_username, user_id, nexttoken, pag)
        print("******* PAGE " + str(pag) + " DONE *******")
        pag=pag+1
        file1 = open("resume.txt", "w")   # create file with last page done to resume if needed
        file1.write(str(pag) + "\n" + str(nexttoken))
        file1.close()
        time.sleep(0.5)
    remove_temp_file()
    print("DONE. All images and videos downloaded to /" + instagram_username + "/ folder.")

if __name__ == "__main__":

    main()
