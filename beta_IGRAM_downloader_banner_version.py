#!/usr/bin/env python3


#  Version with Banner and menu
# --- UNDER CONSTRUCTION ----

# Goals:
# Ctreate custom color banner- DONE!
# Create a color coded menue and output, this will Give the user the ability, to select the directory for the new user file.
# os.chdir ?? etc..
# Offer the ability to download more than just one Instagrammer at a time.
# import threading module & create def queueRequests():  
# or use asyncio or other concurrency? could conflict with API calls and result in being blocked
# How to call the class and functions to run the program ??
# create a separate module , (menu.py) to be imported??
# What adjstments to the class, ( or more classes?), attributes and functions will be needed?
# Ultimately how to run the program? ie: Calling the classes, functions etc..

import sys
import requests
import time
import urllib.request
import os
import json
import pyfiglet

# INSTAGRAM_USERNAME = " "
host = "instagram.com"
#username = input("Type the Instagram user to download: ")
#--------------------------------------------------------------------------------------#

# class Instagram_Downloader:
#     def __init__(self, username):
#         self.username = username
#         self.user_id = ""
#         self.jsondata = ""
#         self.apilabel = "graphql"
#         self.hash_timeline = ""


class Instagram_Downloader:
	def __init__(self, smhost, username="", smargs=None):
		self._host = smhost
		self._username = username
		self.user_id = ""
		self.jsondata = ""
		self.apilabel = "graphql"
		self.hash_timeline = ""
		self._attempts = 0


	def create_download_directory(self):
		try:
			os.mkdir(self.username)
			print("Directory ", self.username, " created.")
		except FileExistsError:
			print("Directory ", self.username, " already exists.")

	def get_total_photos(self):
		pass


	def set_user_id(self):
		pass


	def get_end_cursor_timeline_media(self):
		pass


	def write_resume_end_cursor_timeline_media(self):
		pass


	def read_resume_end_cursor_timeline_media(self):
		pass


	def remove_resume_file(self):
		pass


	def set_apilabel(self, label):
		pass


	def has_next_page(self):
		pass


	def get_jsondata_instagram(self):
		pass


	def download_photos(self):
		pass


	def download_videos(self):
		 pass



# --------------------------------- Main program -------------------------------------#

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
    print(CF(r" _______       ____                                                                                                          "))
    print(CF(r"/  _____ \    / __ \     _            _                                              _______      _____       ________       "))
    print(CF(r"| |     \ \  / /  \ \   | |          | |           _          ____                  /  ____  \   | ____|     |  ____  \      "))
    print(CF(r"| |     | |  | |   | |  | |          | |           | |       / /\ \       ___       | |     \    | |         | |____| |      "))
    print(CF(r"| |     | |  | |   | |  | |    _     | |  _____    | |      | |  | |     /   \      | |     | |  | |___      | ____  /       "))
    print(CF(r"| |     | |  | |   | |  | |   | |    | |  |  _ \   | |      | |  | |    / / \ \     | |     | |  |  ___|     | |   \ \       "))
    print(CF(r"| |     | |  | |   | |  | |   | |    | |  | | \ \  | |      | |  | |   / /___\ \    | |     | |  | |         | |    \ \      "))
    print(CF(r"| |     | |  | |   | |  | |   | |    | |  | |  \ \ | |      | |  | |  / ______  \   | |     | |  | |     _   | |     \ \     "))                                                                                 "))
    print(CF(r"| |____/  /  | |___| |  | \__/ / \ __/ |  | |   \ \|  \_____\  \/ /  / /       \ \__| |____ / /__| |____| |__| |      \ \    "))
    print(CF(r"|________/   \_______/  \ ____/   \____/  |_|    \_______________/  /_/         \______________________________/       \_\   "))                                                                "))
    print(CF(r"                                                                                                                             "))
    print(CF(r"                                                                                                                             "))
    print(CF(r""))
    print(CF(r"     @defparam                                                                                                    %s"%(sm_version)))
    print(CF(Style.RESET_ALL))








def print_info(msg, file_handle=None):
	ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
	msg = Style.BRIGHT + Fore.MAGENTA + \
		"[%s] %s" % (Fore.CYAN+'+'+Fore.MAGENTA, msg) + Style.RESET_ALL
	plaintext = ansi_escape.sub('', msg)
	print(CF(msg))
	if file_handle is not None:
		file_handle.write(plaintext+"\n")


if __name__ == "__main__":
	global NOCOLOR
	if sys.version_info < (3, 0):
		print("Error: Instagram Downloader requires Python 3.x")
		sys.exit(1)

# Offer the ability to select more than just one Instagram User

Parser = argparse.ArgumentParser()
#Parser.add_argument('-h', '--help', help="help menu:")
Parser.add_argument('-u', '--Instagram Username(s)', help="Target Instgram Username(s)")
#Parser.add_argument('-v', '--vhost', default="", help="Specify a virtual host")
#Parser.add_argument('-x', '--exit_early', action='store_true', help="Exit scan on first finding")
#Parser.add_argument('-m', '--method', default="POST", help="HTTP method to use (e.g GET, POST) Default: POST")
#Parser.add_argument('-l', '--log', help="Specify a log file")
Parser.add_argument('-q', '--quiet', action='store_true', help="Quiet mode will only log issues found")
Parser.add_argument('-t', '--timeout', default=5.0, help="Socket timeout value Default: 5")
Parser.add_argument('--no-color', action='store_true', help="Suppress color codes")
#Parser.add_argument('-c', '--configfile', default="default.py", help="Filepath to the configuration file of payloads")
Args = Parser.parse_args()  # returns data from the options specified (echo

NOCOLOR = Args.no_color
if os.name == 'nt':
		NOCOLOR = True

Version = "v1.1"
banner(Version)

if sys.version_info < (3, 0):
		print_info("Error: Instagram Downloader requires Python 3.x")
		sys.exit(1)

	# If the Username argument is not specified then check stdin
#if Args.username is None:
#        if sys.stdin.isatty():
#            print_info("Error: no direct Username specified\n")
#            Parser.print_help()
#            exit(1)
#        username = sys.stdin.read(),split("\n")
#        #Servers = sys.stdin.read().split("\n")
#else:
#        Username = [Args.username]
#        #Servers = [Args.url + " " + Args.method]
#
#FileHandle = None
#if Args.log is not None:
#        try:
#            FileHandle = open(Args.log, "w")
#        except:
#            print_info("Error: Issue with log file destination")
#            print(Parser.print_help())
#            sys.exit(1)
#
##for username in Usersnames:
		# If the next on the list is blank, continue
 #       if username == "":
 #           continue
		# Tokenize
  #      username = username.split(" ")

		# This is for the stdin case, if no method was specified default to GET
#        if len(server) == 1:
#            server += [Args.method]

		# If a protocol is not specified then default to https
#        if server[0].lower().strip()[0:4] != "http":
#            server[0] = "https://" + server[0]

		host, port, endpoint, SSLFlagval = process_uri(server[0])
#        method = server[1].upper()
#       configfile = Args.configfile

		print_info("Username        : %s" % (Fore.CYAN + server[0]), FileHandle)
		print_info("Method     : %s" % (Fore.CYAN + method), FileHandle)
#        print_info("Endpoint   : %s" % (Fore.CYAN + endpoint), FileHandle)
#        print_info("Configfile : %s" % (Fore.CYAN + configfile), FileHandle)
		print_info("Timeout    : %s" % (
			Fore.CYAN + str(float(Args.timeout)) + Fore.MAGENTA + " seconds"), FileHandle)

		sm = Instagram_Downloader(host,  username="", smargs=Args)
		sm.run()
