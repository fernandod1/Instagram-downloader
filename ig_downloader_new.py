#!/usr/bin/env python3

# Too many imports? Which ones aren't needed?   ¯\_(ツ)_/¯
import os
import os.path
import re
import sys
import time
import json
import random
import string
import hashlib
import requests
import argparse
import importlib
import urllib.request
from time import sleep
from copy import deepcopy
from datetime import datetime
from instagram_downloader import user
from lib.colorama import Fore, Style

# Doesn't run unless I provide the same URL twice as two similar but different variables.. 
#  ¯\_(ツ)_/¯
host = "https://instagram.com"
shost = "https://instagram.com"

# Experimenting with creating the user directory
# destination = "/temp"
# sub_folder = "test"
# -------------------------------------------------------------------------------------------------------- #
# Running better now, but not 100%
# ATTENTION! Updates & Changes:
# I know that line length in Python should be limited to 79 characters. But this script is less buggy as is.
# 1. Renamed all instances of username to user
# 2. Inserted a space between all vars and their values, example name = property(get_user)
# 3. Eliminated spaces between plus '+' and it's neighboring characters. (script runs better that way)
# Question: Any modifications needed to the class or any of it's current attributes ??

class Instagram_Downloader:
    def __init__(self, shost, user=""):
        self.user = user
	self.shost = shost
        self.user_id = ""
        self.jasondata = ""
        self.apilabel = "graphql"
        self.hash_timeline = ""


    # Main function:
    # What to use?? arguments to pass etc..
    def run(self):
        pass

    # Add the user via the arg parser
    def get_user(self, user):
        return self.user

    # Problem: This is creating an empty/nameless directory ' '
    # needs to create a user directory based on the function above
    def create_download_directory(self):
        try:
            user = self.user
            os.mkdir(self.user(user))
            print("Directory ", self.user.new_dir, " created.")
        except FileExistsError:
            print("Directory ", self.user.new_dir, " already exists.")

    def get_total_photos(self):
        return int((self.jsondata.json()[self.apilabel]["user"]["edge_owner_to_timeline_media"]["count"]))

    def set_user_id(self):
        self.user_id=int(self.jsondata.json()[self.apilabel]["user"]["id"])

    def get_end_cursor_timeline_media(self):
        return self.jsondata.json()[self.apilabel]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]
     
    # Eliminated spaces between '+' and it's neighboring characters..less buggy See next comment.
    def write_resume_end_cursor_timeline_media(self):
        f = open("resume_"+ self.user+".txt", "w")  # create file with last page download to resume if needed.
        f.write(str(self.get_end_cursor_timeline_media()))
        f.close()

    # Notice no space between the plus sign in ("resume_"+ self.user+".txt"). Again, not causing problems this way.
    def read_resume_end_cursor_timeline_media(self):
        if os.path.isfile("resume_"+ self.user+ ".txt"):
            with open("resume_"+ self.user+".txt") as f:
                self.hash_timeline = f.readline().strip()
                print("****************\nResume mode ON\n****************")
                return True
        else:
            print("Not resume pending")
            return False

    def remove_resume_file(self):
        if os.path.exists("resume_"+self.user+".txt"):
            os.remove("resume_"+self.user+".txt")

    def set_apilabel(self, label):
        self.apilabel = label

    def has_next_page(self):
        return self.jsondata.json()[self.apilabel]["user"]["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]

    def get_jsondata_instagram(self):
        headers = {
            "Host": "www.instagram.com",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
        }
        if self.apilabel=="graphql":
            self.jsondata = requests.get("https://www.instagram.com/" + self.user + "/feed/?__a=1", headers=headers)
            self.hash_timeline = self.get_end_cursor_timeline_media()
            self.set_user_id()
        else:               # Eliminated word wrap on the long lines. Not appropriate line length of 79, but less buggy this way. ¯\_(ツ)_/¯
            self.jsondata = requests.get("https://www.instagram.com/graphql/query/?query_id=17888483320059182&variables=%7B%22id%22%3A%22" + str(self.user_id) + "%22%2C%22first%22%3A12%2C%22after%22%3A%22" + str(self.hash_timeline) + "%22%7D", headers=headers)
            if user.has_next_page():
                self.hash_timeline = self.get_end_cursor_timeline_media()
        if (self.jsondata.status_code==200):
            print(
                "----------------\nJson url loaded:\n----------------\nhttps://www.instagram.com/graphql/query/?query_id=17888483320059182&variables=%7B%22id%22%3A%22" + str(self.user_id) + "%22%2C%22first%22%3A12%2C%22after%22%3A%22" + str(self.hash_timeline) + "%22%7D")
        else:
            print("ERROR: Incorrect json data url received.")
        return self.jsondata

    def download_photos(self):
        i = 0
        for match in self.jsondata.json()[self.apilabel]["user"]["edge_owner_to_timeline_media"]["edges"]:
            time.sleep(0.5)
            print("Downloading IMAGE:\n" +match["node"]["display_url"])
            filename = self.user + "/" + self.jsondata.json()[self.apilabel]["user"]["edge_owner_to_timeline_media"]["edges"][i]["node"]["shortcode"] + ".jpg"
            try:
                if not os.path.exists(filename ):
                    urllib.request.urlretrieve(match["node"]["display_url"], filename)
                else:
                    print("Notice: "+ filename+ " image already downloaded, skipped.")
            except urllib.error.HTTPError as e:
                print(str(e.code) + " Can't download image")
            i = i + 1

    def download_videos(self):
        i = 0
        if 'edge_felix_video_timeline' in self.jsondata.json()[self.apilabel]["user"]:
            for match in self.jsondata.json()[self.apilabel]["user"]["edge_felix_video_timeline"]["edges"]:
                time.sleep(0.5)
                print("Downloading VIDEO:\n" +match["node"]["video_url"])
                filename = self.user + "/" + self.jsondata.json()[self.apilabel]["user"]["edge_felix_video_timeline"]["edges"][i]["node"]["shortcode"] + ".mp4"
                try:
                    if not os.path.exists(filename ):
                        urllib.request.urlretrieve(match["node"]["video_url"], filename)
                    else:
                        print("Notice: "+ filename+ " video already downloaded, skipped.")
                except urllib.error.HTTPError as e:
                    print(str(e.code) + " Can't download video")
                i = i + 1


# ---------------------------------Color banner and user input menu -------------------------------------#

# Update: Increased all indents from here down.
def CF(text):
        global NOCOLOR
        if NOCOLOR:
                ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
                text = ansi_escape.sub('', text)
        return text

# Doubled the indent
def banner(s_version):
	    print(CF(Fore.CYAN))
	    print(CF(r" _                                                                                                  "))
	    print(CF(r"| |                    ___________              _______                         __      __          "))
	    print(CF(r"| |                   (____   ____) ___        /  _____)              ___      /  \    /  \         "))
	    print(CF(r"| |  _____         ______  | |     /   \      / /                    /   \    / /\ \  / /\ \        "))
	    print(CF(r"| | |  _  \       /  ____) | |    / / \ \     | |    ____   _____   / / \ \   | | \ \/ /  \ \       "))
	    print(CF(r"| | | |  \ \     ( (_____  | |   / /___\ \    | |   (_   ) /  __   / /___\ \  | |  \__/    \ \      "))
	    print(CF(r"| | | |   \ \     \_____  \| |  / _______ \   | |     \  \ | |    / _______ \ | |           \ \     "))
	    print(CF(r"| | | |    \ \__________)  ) | / /       \ \_/ /______|  | | |   / /       \ \| |            \ \    "))
	    print(CF(r"|_| |_|     \_____________/|_|/_/         \______________/ |_|  /_/         \___/             \_\   "))
	    print(CF(r"                                                                                                                             "))
	    print(CF(r"                                                                                                                             "))
	    print(CF(r" _______       ____                                                                                                          "))
	    print(CF(r"/  _____ \    / __ \     _            _                                              _______      _____       ________       "))
	    print(CF(r"| |     \ \  / /  \ \   | |          | |           _          ____                  /  ____  \   | ____|     |  ____  \      "))
	    print(CF(r"| |     | |  | |   | |  | |          | |           | |       / /\ \       ___       | |     \    | |         | |____| |      "))
	    print(CF(r"| |     | |  | |   | |  | |    _     | |  _____    | |      | |  | |     /   \      | |     | |  | |___      | ____  /       "))
	    print(CF(r"| |     | |  | |   | |  | |   | |    | |  |  _ \   | |      | |  | |    / / \ \     | |     | |  |  ___|     | |   \ \       "))
	    print(CF(r"| |     | |  | |   | |  | |   | |    | |  | | \ \  | |      | |  | |   / /___\ \    | |     | |  | |         | |    \ \      "))
	    print(CF(r"| |     | |  | |   | |  | |   | |    | |  | |  \ \ | |      | |  | |  / ______  \   | |     | |  | |     _   | |     \ \     "))
	    print(CF(r"| |____/  /  | |___| |  | \__/ / \ __/ |  | |   \ \|  \_____\  \/ /  / /       \ \__| |____ / /__| |____| |__| |      \ \    "))
	    print(CF(r"|________/   \_______/  \ ____/   \____/  |_|    \_______________/  /_/         \______________________________/       \_\   "))
	    print(CF(r"                                                                                                                             "))
	    print(CF(r""))
	    print(CF(r"     LinuxUser255                                                                     %s" % (sm_version)))
	    print(CF(Style.RESET_ALL))

# Update: Commented out all references to 'file_handle', it was in regards to an old config file
def print_info(msg): # file_handle = None
        ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        msg = Style.BRIGHT + Fore.MAGENTA + \
        "[%s] %s" % (Fore.CYAN + '+' + Fore.MAGENTA, msg) + Style.RESET_ALL
        plaintext = ansi_escape.sub('', msg)
        print(CF(msg))
        #if file_handle is not None:
                #file_handle.write(plaintext + "\n")

# Doubled/increased indent
if __name__ == "__main__":
        global NOCOLOR
        if sys.version_info < (3, 0):
                print("Error: Instagram Downloader requires Python 3.x")
                sys.exit(1)

        # Goal: Offer the ability to select more than just one Instagram User
        # Thought: Something's off here, don't think argparse is deployed correctly
        Parser = argparse.ArgumentParser()
	Parser.add_argument('-u', '--user', help="Provide an Instagram Username")
        #Parser.add_argument('-u', type=str, help='username')
        Parser.add_argument('-x', '--exit_early', action='store_true', help="Exit scan on first finding")
        Parser.add_argument('-t', '--timeout', default=5.0, help="Socket timeout value Default: 5")
        Parser.add_argument('--no-color', action='store_true', help="Suppress color codes")
        Args = Parser.parse_args()  # returns data from the options specified (ech

        NOCOLOR = Args.no_color
        if os.name == 'nt':
                NOCOLOR = True

        Version = "v2.0"
        banner(Version)

	# Goal: pass the selected user/new directory name here where it says "Working"
        print_info("Working: %s" % Fore.CYAN)
        print_info("Time: %s" % (Fore.CYAN + str(float(Args.timeout)) + Fore.MAGENTA + " seconds"))

        # Run it
        s = Instagram_Downloader(user)
        s.run()
