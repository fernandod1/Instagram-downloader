# Instagram downloader
Instagram user's photos and videos downloader. Download all media files from any public username. Working 2021.

# I've forked this one from the original developer and am working on some extras.
# # Goals:
# Version with Banner and menu
# Create a color coded menu with progress printed to the screen. 
# Ability to select the directory for the new user file: os.chdir ??,  etc..
# Offer the ability to download more than just one Instagrammer at a time.
# Import the threading module & create def queueRequests():  
# Or use asyncio or other concurrency? Caveat: This could conflict with Instagram's API and result in being temporaraly blocked.
# Regardless, the current instagram_downloader.py  works very well.

LIMITS: 

Script does not requires a token or username/pass to use Instagram API, this causes some daily limits:

- Script has been tested in single execution and downloads around 2200 images/videos.
- Instagram API limits daily queries, so if script reachs limit, I recommend you to execute script again in 12 hours so that daily limit is expired.
- I have added a resume mode so that you can execute again script and it will continue from last image downladed.

Requirement: Python v3

CONFIGURE:

Set in line 14 public instagram username you want to download photos from (Example: ladygaga):
INSTAGRAM_USERNAME = "SET_INSTAGRAM_USERNAME"

USAGE COMMAND:

python instagram_downloader.py

DISCLAIMER:

"Instagram-downloader" repository is in no way affiliated with, authorized, maintained or endorsed by Instagram or any of its affiliates or subsidiaries. This is an independent and unofficial project. Use at your own risk and respect copyrights of media files.

COLLABORATIONS:

Collaborations to improve this script are always webcome.

