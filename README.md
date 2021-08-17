# Instagram downloader
Instagram user's photos and videos downloader.
Download all media files from any public username. 
Rewritten and updated using Object Oriented Programming by https://github.com/fernandod1 for 2021.

I've forked this one from the original developer whith whom I collaborated on the original 
Instagram Downloader: https://github.com/fernandod1/Instagram-downloader
and am working on an enhanced version: see beta.py in this repo.

# Goals & Ideas:
Create a color coded menu & banner & have progress printed to the screen. 
Offer the ability to download more than just one Instagrammer at a time.
?? Import the threading module & create def queueRequests() etc..??
?? Or use asyncio or other concurrency?
Caveat: This will conflict with Instagram's API and result in being temporaraly blocked. (bypass using proxiess/API calls? like in the sms flooders??)
Implement a metadata exfiltration tool within the script.

# Ultimate goal: 
Integrate this or another Instagram scraper into a larger OSINT Framework.
Scrape a target's entire social media presence and then some..such as FB, IG, Twitter, personal websites and more, etc..
Could be used inconjuction with Spiderfoot to create an even more comprehensive dossier.  

# Current Limits of instagram_downloader.py
Script does not requires a token or username/pass to use Instagram API, 
Having said that, this can cause some daily limits.

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

