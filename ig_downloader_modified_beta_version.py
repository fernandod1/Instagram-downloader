#!/usr/bin/env python3

# Much of this code was inspired by James Kettle's HTTP Request Smuggling Python tool/code
import argparse
import re
import requests
import time
import sys
import os
import os.path
import random
import string
import importlib
import hashlib
#import username
from lib import Url
from copy import deepcopy
from time import sleep
from datetime import datetime
from lib.colorama import Fore, Style

#  Version with banner menu and added features.
# --- UNDER CONSTRUCTION ----
# Goals:
# DONE! Create custom color banner- DONE!
# DONE! Create a menu tailored to this scraper,
# DONE! enter username prompt
# Make the code more redable
# Follow The Zen of Python guidelines
# !! Fix INDENTATION !!

# Thoughts, Ideas...
# Why limit this to just an Instagram user profile downloader/scraper??
# Why not turn it into a full-fledged OSINT-Style Social media scraper/Toolkit/framework/Suite? You could target a particular user/person/org/biz accross all platforms!?
# Scrape/download User info from Instagram, Twitter, Snapchat, Facebook, LinkedIn, any personal websites, blogs, etc..
# Maybe in lieu of messing with json and all the extra code & getting locked out maybe..
# Create a login credential module and import that? Use a sock account/dummy account..whatever you wanna call it.
# For OSINT purposes, Add a a Metadata exfiltration feature, (linux cmd line tools out there for that and Python scripts) could make them modules and import them.
# Is it possible to proxy individual requests/downloads through diffent servers to prevent IP ban?
# Offer the ability to download more than just one Instagrammer at a time. (need proxies?)
# ?? import threading module & create def queueRequests():
# Or, use asyncio or a different concurrency option? could conflict with API calls and result in being blocked
# How to succienctly call the classe(s) and functions to run the program ??
# ?? Any sepearate modules needed for importation?
# Probably need to up the sleep() function to 1 second time.sleep(1.00)  # pause to avoid ban
# Ultimately how to run the program? ie: Calling the classes, functions etc, a simple oneliner? or multiple lines calling each function sepearately?
# Fix indentation and clean up the code & remember..

# -------The ZEN of PYTHON-------#
# Complex is better than complicated.
# Flat is better than nested.
# Sparse is better than dense.
# Readability counts.
# Special cases aren't special enough to break the rules.
# Although practicality beats purity.
# Errors should never pass silently.
# Unless explicitly silenced.
# In the face of ambiguity, refuse the temptation to guess.
# There should be one-- and preferably only one --obvious way to do it.
# Although that way may not be obvious at first unless you're Dutch.
# Now is better than never.
# Although never is often better than *right* now.
# If the implementation is hard to explain, it's a bad idea.
# If the implementation is easy to explain, it may be a good idea.
# Namespaces are one honking great idea -- let's do more of those!
#---------------------------------

# anything to do different here with these variables?
# smhost is a throwbackto Kettle's smuggler.py , but as of now, the code needs both host & smhost, with the same URL value to run.
# IDK. ¯\_(ツ)_/¯
# Contrubuters feel free to analyze and suggest of that one.
host = "https://instagram.com"
smhost = "https://instagram.com"
# --------------------------------------------------------------------------------------#

# This indentation is..Ughhh, fix it Chris.
# Is the  (): needed on this class creation?
# Can you do it the basic way using just the : ??


class Instagram_Downloader:
	def __init__(self, smhost, username=""):
		self._host = smhost  # Does this attribute need the ._ for data access?
		self.username = username
		self.user_id = ""
		self.jsondata = ""
		self.apilabel = "graphql"
		self.hash_timeline = ""

	def run(self):
		"""receivess the call sm.run() to execute the code"""
		while True:
			Parser = argparse.ArgumentParser()

	def create_download_directory(self):
		try:
			os.mkdir(self.username)
			print("Directory ", self.username, " created.")
		except FileExistsError:
			print("Directory ", self.username, " already exists.")

	def get_total_photos(self):
		return int((self.jsondata.json()[self.apilabel]["user"]["edge_owner_to_timeline_media"]["count"]))

	def set_user_id(self):
		self.user_id = int(self.jsondata.json()[self.apilabel]["user"]["id"])

	def get_end_cursor_timeline_media(self):
		return self.jsondata.json()[self.apilabel]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]

	def write_resume_end_cursor_timeline_media(self):
		# create file with last page downladed to resume if needed
		f = open("resume_"+self.username+".txt", "w")
		f.write(str(self.get_end_cursor_timeline_media()))
		f.close()

	def read_resume_end_cursor_timeline_media(self):
		if os.path.isfile("resume_"+self.username+".txt"):
			with open("resume_"+self.username+".txt") as f:
				self.hash_timeline = f.readline().strip()
				print("****************\nResume mode ON\n****************")
				return True
		else:
			print("Not resume pending")
			return False

	def remove_resume_file(self):
		if os.path.exists("resume_"+self.username+".txt"):
			os.remove("resume_"+self.username+".txt")

	def set_apilabel(self, label):
		self.apilabel = label

	# A lot of this lengthy & hard to read code could be eliminated with aan account login feature.
	def has_next_page(self):
		return self.jsondata.json()[self.apilabel]["user"]["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]

	def get_jsondata_instagram(self):
		headers = {
                    "Host": "www.instagram.com", "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
		}
		if self.apilabel == "graphql":
			self.jsondata = requests.get(
			    "https://www.instagram.com/" + self.username + "/feed/?__a=1", headers=headers)
			self._set_user_id()
		else:
			self.jsondata = requests.get("https://www.instagram.com/graphql/query/?query_id=17888483320059182&variables=%7B%22id%22%3A%22" + str(
			    self.user_id) + "%22%2C%22first%22%3A12%2C%22after%22%3A%22" + str(self.hash_timeline) + "%22%7D", headers=headers)
        		if user.has_next_page(): #This error keeps poping up:  if user.has_next_page():  TabError: inconsistent use of tabs and spaces in indentation
				self.hash_timeline = self.get_end_cursor_timeline_media()
		if (self.jsondata.status_code == 200):
			print("----------------\nJson url loaded:\n----------------\nhttps://www.instagram.com/graphql/query/?query_id=17888483320059182&variables=%7B%22id%22%3A%22" +
			      str(self.user_id) + "%22%2C%22first%22%3A12%2C%22after%22%3A%22" + str(self.hash_timeline) + "%22%7D")
		else:
			print("Error: Incorrect json data url received.")
		return self.jsondata

	def download_photos(self):
		i = 0
		for match in self.jsondata.json()[self.apilabel]["user"]["edge_owner_to_timeline_media"]["edges"]:
			time.sleep(1.00)
			print("Downloading photos:\n" + match["node"]["display_url"])
			filename = self.username + "/" + self.jasondata.jason(
			)[self.apilabel]["user"]["edge_owner_to_timeline_media"]["edges"][i]["node"]["shortcode"] + ".jpg"
			try:
				if not os.path.exists(filename):
					urllib.requests.urlretrieve(match["node"]["display_url"], filename)
				else:
					print("Notice: " + filename + " image already downloaded, skipped.")
			except urllib.error.HTTPError as e:
				print(str(e.code) + "Unable to download image")
			i = i + 1

	def download_videos(self):
		i = 0
		if 'edge_felix_video_timeline' in self.jasondata.jason()[self.apilabel]["user"]:
			for match in self.jsondata.json()[self, apilabel]["user"]["edge_felix_video_timeline"]["edges"]:
				time.sleep(1.00)
				print("Downloading Video:\n" + match["node"]["video_url"])
				filename = self.username + "/" self.jsondata.json()[self.apilabel][apilabel]["user"]["edge_felix_video_timeline"]["edges"][i]["node"]["shortcode"] + ".mp4"
				try:
					if not os.path.exists(filename):
						urllib.requests.urlretrieve(match["node"]["video_url"], filename)
					else:
						print("Notice: " + filename + " video already downloaded, skipped.")
				except urllib.error.HTTPError as e:
					print(str(e.code) + "Unable to download video.")
				i = i + 1


# --------------------------------- SMUGGLER CODE -------------------------------------#

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
	print(CF(r"                                                                                                                             "))
	print(CF(r"     LinuxUser255                                                                                        				 %s" % (sm_version)))
	print(CF(Style.RESET_ALL))


def print_info(msg, file_handle=None):
	ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
	msg = Style.BRIGHT + Fore.MAGENTA + \
            "[%s] %s" % (Fore.CYAN + '+' + Fore.MAGENTA, msg) + Style.RESET_ALL
	plaintext = ansi_escape.sub('', msg)
	print(CF(msg))
	if file_handle is not None:
		file_handle.write(plaintext + "\n")


if __name__ == "__main__":
	global NOCOLOR
	if sys.version_info < (3, 0):
		print("Error: Instagram Downloader requires Python 3.x")
		sys.exit(1)

# Goal: Offer the ability to select more than just one Instagram User
# Redo-EDIT this menue for its puposes.
Parser = argparse.ArgumentParser()
Parser.add_argument('-u', '--user', help="INSTAGRAM_USERNAME")
Parser.add_argument('-x', '--exit_early', action='store_true',
                    help="Exit scan on first finding")
Parser.add_argument('--no-color', action='store_true',
                    help="Suppress color codes")
#Parser.add_argument('-c', '--configfile', default="default.py",help="Filepath to the configuration file of payloads")
Args = Parser.parse_args()  # returns data from the options specified (ech

NOCOLOR = Args.no_color
if os.name == 'nt':
	NOCOLOR = True

Version = "v1.1"
banner(Version)

# Run it
sm = Instagram_Downloader(host, smhost)
# this still needed??
sm.run()


# Original way of calling/executing Instagram Downloader script

# -----------Main program function calls for Instagram_Downloader -------------------------------------#
#
# try:
#    user = Instagram_Downloader(INSTAGRAM_USERNAME)
#    user.create_download_directory()
#    user.get_jsondata_instagram()
#    user.download_photos()
#    user.download_videos()
#    user.set_apilabel("data")
#    user.read_resume_end_cursor_timeline_media()
#    while True:
#        time.sleep(5)  # pause to avoid ban
#        user.get_jsondata_instagram()
#        user.download_photos()
#        user.download_videos()
#        user.write_resume_end_cursor_timeline_media()
#        if user.has_next_page() == False:
#            user.remove_resume_file()
#            print("Done. All images/videos downloaded for " +
#                  INSTAGRAM_USERNAME+" account.")
#            break
# except:
#    print("Notice: script premature finished due to daily limit of number of requests to Instagram API.")
#    print("Just execute script AGAIN in few hours to continue RESUME of pending images/videos to downloa#
#

