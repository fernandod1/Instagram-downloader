#!/usr/bin/env python3

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

# Doesn't run unless I provide the same URL twice as two similar but different variables, (redundant)
host = "https://instagram.com"
smhost = "https://instagram.com"


# -------------------------------------------------------------------------------------------------------- #
# Update: renamed all instances of username to user
# Any modifications to the current attributes needed???
# Seems like something is not quite right
# Just one class, but do any of the attributes need modification??
class Instagram_Downloader:
    def __init__(self, user):
        self.user = user
        self.user_id = ""
        self.jasondata = ""
        self.apilabel = "graphql"
        self.hash_timeline = ""


    # Main function that run this script
    def run(self):
        pass

    # This method's not working so well
    #def get_user(self):
    #    return self.username

    # Augmenting this method too
    def get_user(self, user):
        return self.user

    # No.
    name=property(get_user)

    # Creates an empty ' '
    def create_download_directory(self):
        try:
            user = self.user
            os.mkdir(self.user.new_dir(user))
            print("Directory ", self.user.new_dir, " created.")
        except FileExistsError:
            print("Directory ", self.user.new_dir, " already exists.")

    def get_total_photos(self):
        return int((self.jsondata.json()[self.apilabel]["user"]["edge_owner_to_timeline_media"]["count"]))

    def set_user_id(self):
        self.user_id=int(self.jsondata.json()[self.apilabel]["user"]["id"])

    def get_end_cursor_timeline_media(self):
        return self.jsondata.json()[self.apilabel]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]

    def write_resume_end_cursor_timeline_media(self):
        f = open("resume_"+ self.user+".txt", "w")  # create file with last page download to resume if needed.
        f.write(str(self.get_end_cursor_timeline_media()))
        f.close()

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
        else:
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

# Create menu.py and import it as a module instead of displaying it here???
def CF(text):
        global NOCOLOR
        if NOCOLOR:
                ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
                text = ansi_escape.sub('', text)
        return text


def banner(sm_version):
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


def print_info(msg): # file_handle=None
        ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        msg = Style.BRIGHT + Fore.MAGENTA + \
        "[%s] %s" % (Fore.CYAN + '+' + Fore.MAGENTA, msg) + Style.RESET_ALL
        plaintext = ansi_escape.sub('', msg)
        print(CF(msg))
        #if file_handle is not None:
                #file_handle.write(plaintext + "\n")


if __name__ == "__main__":
        global NOCOLOR
        if sys.version_info < (3, 0):
                print("Error: Instagram Downloader requires Python 3.x")
                sys.exit(1)

        # Goal: Offer the ability to select more than just one Instagram User
        # Something's off here, you're not using argparse correctly
        Parser = argparse.ArgumentParser()
        Parser.add_argument('-u', type=str, help='username')
        Parser.add_argument('-x', '--exit_early', action='store_true', help="Exit scan on first finding")
        Parser.add_argument('-t', '--timeout', default=5.0, help="Socket timeout value Default: 5")
        Parser.add_argument('--no-color', action='store_true', help="Suppress color codes")
        Args = Parser.parse_args()  # returns data from the options specified (ech

        NOCOLOR = Args.no_color
        if os.name == 'nt':
                NOCOLOR = True

        Version = "v2.0"
        banner(Version)

        print_info("Working: %s" % Fore.CYAN)
        print_info("Time: %s" % (Fore.CYAN + str(float(Args.timeout)) + Fore.MAGENTA + " seconds"))

        # Run it
        sm = Instagram_Downloader(user)
        sm.run()
