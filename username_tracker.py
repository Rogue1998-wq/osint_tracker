
import requests
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# Define platforms and their check URLs/methods
# A dictionary where keys are platform names and values are dictionaries
# containing 'url' (the base URL to check) and 'exists_check' (a string to look for
# if the username *does not* exist, or a status code to check).
# This is a simplified example; real-world would need more sophisticated checks.
PLATFORMS = {
    "GitHub": {
        "url": "https://github.com/{}",
        "exists_check": 200, # Status code 200 means user exists
        "method": "status_code"
    },
    "Twitter": {
        "url": "https://twitter.com/{}",
        "exists_check": "Sorry, that page doesn’t exist.", # Text if user does not exist
        "method": "text"
    },
    "Instagram": {
        "url": "https://www.instagram.com/{}",
        "exists_check": "Page Not Found", # Text if user does not exist
        "method": "text"
    },
    "Reddit": {
        "url": "https://www.reddit.com/user/{}",
        "exists_check": "Sorry, nobody on Reddit goes by that name.",
        "method": "text"
    },
    "LinkedIn": {
        "url": "https://www.linkedin.com/in/{}",
        "exists_check": 404, # Status code 404 means user does not exist
        "method": "status_code"
    },
    "Pinterest": {
        "url": "https://www.pinterest.com/{}",
        "exists_check": "Page not found",
        "method": "text"
    },
    "TikTok": {
        "url": "https://www.tiktok.com/@{}",
        "exists_check": "Couldn't find this account",
        "method": "text"
    },
    "YouTube": {
        "url": "https://www.youtube.com/@{}",
        "exists_check": "This channel does not exist.",
        "method": "text"
    },
    "Twitch": {
        "url": "https://www.twitch.tv/{}",
        "exists_check": "Sorry. Unless you’ve got a time machine, that content is unavailable.",
        "method": "text"
    },
    "Medium": {
        "url": "https://medium.com/@{}",
        "exists_check": 404,
        "method": "status_code"
    },
    "Dev.to": {
        "url": "https://dev.to/{}",
        "exists_check": 404,
        "method": "status_code"
    },
    "Flickr": {
        "url": "https://www.flickr.com/people/{}",
        "exists_check": "Page not found",
        "method": "text"
    },
    "Steam": {
        "url": "https://steamcommunity.com/id/{}",
        "exists_check": "The specified profile could not be found.",
        "method": "text"
    },
    "Etsy": {
        "url": "https://www.etsy.com/shop/{}",
        "exists_check": "Page not found",
        "method": "text"
    },
    "Cash App": {
        "url": "https://cash.app/$",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Patreon": {
        "url": "https://www.patreon.com/{}",
        "exists_check": "404: Not Found",
        "method": "text"
    },
    "Blogger": {
        "url": "https://{}.blogspot.com",
        "exists_check": "Sorry, the blog you were looking for does not exist.",
        "method": "text"
    },
    "About.me": {
        "url": "https://about.me/{}",
        "exists_check": "404 Not Found",
        "method": "text"
    },
    "Imgur": {
        "url": "https://imgur.com/user/{}",
        "exists_check": "Page not found",
        "method": "text"
    },
    "Pastebin": {
        "url": "https://pastebin.com/u/{}",
        "exists_check": "User not found!",
        "method": "text"
    },
    "Vimeo": {
        "url": "https://vimeo.com/{}",
        "exists_check": "Sorry, we couldn’t find that page.",
        "method": "text"
    },
    "SoundCloud": {
        "url": "https://soundcloud.com/{}",
        "exists_check": "Sorry, we can't find that sound.",
        "method": "text"
    },
    "Bandcamp": {
        "url": "https://bandcamp.com/{}",
        "exists_check": "Page not found",
        "method": "text"
    },
    "Last.fm": {
        "url": "https://www.last.fm/user/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Gravatar": {
        "url": "https://gravatar.com/profiles/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Keybase": {
        "url": "https://keybase.io/{}",
        "exists_check": "User not found",
        "method": "text"
    },
    "HackerOne": {
        "url": "https://hackerone.com/{}",
        "exists_check": "Page not found",
        "method": "text"
    },
    "Bugcrowd": {
        "url": "https://bugcrowd.com/{}",
        "exists_check": "Page not found",
        "method": "text"
    },
    "Docker Hub": {
        "url": "https://hub.docker.com/u/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "npmjs": {
        "url": "https://www.npmjs.com/~{}",
        "exists_check": "404 Not Found",
        "method": "text"
    },
    "PyPI": {
        "url": "https://pypi.org/user/{}",
        "exists_check": "404 Not Found",
        "method": "text"
    },
    "RubyGems": {
        "url": "https://rubygems.org/profiles/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Wordpress": {
        "url": "https://{}.wordpress.com",
        "exists_check": "doesn't exist",
        "method": "text"
    },
    "Disqus": {
        "url": "https://disqus.com/by/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Dribbble": {
        "url": "https://dribbble.com/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Behance": {
        "url": "https://www.behance.net/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Codepen": {
        "url": "https://codepen.io/{}",
        "exists_check": "404 Not Found",
        "method": "text"
    },
    "Replit": {
        "url": "https://replit.com/@{}",
        "exists_check": "404 Not Found",
        "method": "text"
    },
    "Stack Overflow": {
        "url": "https://stackoverflow.com/users/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Ask.fm": {
        "url": "https://ask.fm/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Foursquare": {
        "url": "https://foursquare.com/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Goodreads": {
        "url": "https://www.goodreads.com/user/show/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "ImgPile": {
        "url": "https://imgpile.com/user/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "LiveJournal": {
        "url": "https://{}.livejournal.com",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Medium": {
        "url": "https://medium.com/@{}",
        "exists_check": 404,
        "method": "status_code"
    },
    "Periscope": {
        "url": "https://www.pscp.tv/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Product Hunt": {
        "url": "https://www.producthunt.com/@{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Quora": {
        "url": "https://www.quora.com/profile/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Scribd": {
        "url": "https://www.scribd.com/user/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Slideshare": {
        "url": "https://www.slideshare.net/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "SmugMug": {
        "url": "https://{}.smugmug.com",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Taringa!": {
        "url": "https://www.taringa.net/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Telegram": {
        "url": "https://t.me/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Tumblr": {
        "url": "https://{}.tumblr.com",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Vero": {
        "url": "https://vero.co/app/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "VK": {
        "url": "https://vk.com/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "We Heart It": {
        "url": "https://weheartit.com/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Xing": {
        "url": "https://www.xing.com/profile/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Zhihu": {
        "url": "https://www.zhihu.com/people/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Academia.edu": {
        "url": "https://{}.academia.edu",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "AngelList": {
        "url": "https://angel.co/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Bitbucket": {
        "url": "https://bitbucket.org/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Dailymotion": {
        "url": "https://www.dailymotion.com/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Ebay": {
        "url": "https://www.ebay.com/usr/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Fiverr": {
        "url": "https://www.fiverr.com/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Freelancer": {
        "url": "https://www.freelancer.com/u/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "GitLab": {
        "url": "https://gitlab.com/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Gfycat": {
        "url": "https://gfycat.com/@{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "ImgBB": {
        "url": "https://imgbb.com/user/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Kickstarter": {
        "url": "https://www.kickstarter.com/profile/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Mixcloud": {
        "url": "https://www.mixcloud.com/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "OkCupid": {
        "url": "https://www.okcupid.com/profile/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Pexels": {
        "url": "https://www.pexels.com/@{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Pixabay": {
        "url": "https://pixabay.com/users/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Pornhub": {
        "url": "https://www.pornhub.com/users/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Redbubble": {
        "url": "https://www.redbubble.com/people/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "ReverbNation": {
        "url": "https://www.reverbnation.com/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "ScribbleHub": {
        "url": "https://www.scribblehub.com/profile/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Shutterstock": {
        "url": "https://www.shutterstock.com/g/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "StackExchange": {
        "url": "https://stackexchange.com/users/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Unsplash": {
        "url": "https://unsplash.com/@{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "VSCO": {
        "url": "https://vsco.co/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Wattpad": {
        "url": "https://www.wattpad.com/user/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Weebly": {
        "url": "https://{}.weebly.com",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Wikipedia": {
        "url": "https://en.wikipedia.org/wiki/User:{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Xvideos": {
        "url": "https://www.xvideos.com/profiles/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "YouPorn": {
        "url": "https://www.youporn.com/user/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Zillow": {
        "url": "https://www.zillow.com/profile/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Academia.edu": {
        "url": "https://{}.academia.edu",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "AngelList": {
        "url": "https://angel.co/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Bitbucket": {
        "url": "https://bitbucket.org/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Dailymotion": {
        "url": "https://www.dailymotion.com/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Ebay": {
        "url": "https://www.ebay.com/usr/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Fiverr": {
        "url": "https://www.fiverr.com/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Freelancer": {
        "url": "https://www.freelancer.com/u/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "GitLab": {
        "url": "https://gitlab.com/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Gfycat": {
        "url": "https://gfycat.com/@{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "ImgBB": {
        "url": "https://imgbb.com/user/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Kickstarter": {
        "url": "https://www.kickstarter.com/profile/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Mixcloud": {
        "url": "https://www.mixcloud.com/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "OkCupid": {
        "url": "https://www.okcupid.com/profile/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Pexels": {
        "url": "https://www.pexels.com/@{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Pixabay": {
        "url": "https://pixabay.com/users/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Pornhub": {
        "url": "https://www.pornhub.com/users/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Redbubble": {
        "url": "https://www.redbubble.com/people/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "ReverbNation": {
        "url": "https://www.reverbnation.com/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "ScribbleHub": {
        "url": "https://www.scribblehub.com/profile/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Shutterstock": {
        "url": "https://www.shutterstock.com/g/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "StackExchange": {
        "url": "https://stackexchange.com/users/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Unsplash": {
        "url": "https://unsplash.com/@{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "VSCO": {
        "url": "https://vsco.co/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Wattpad": {
        "url": "https://www.wattpad.com/user/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Weebly": {
        "url": "https://{}.weebly.com",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Wikipedia": {
        "url": "https://en.wikipedia.org/wiki/User:{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Xvideos": {
        "url": "https://www.xvideos.com/profiles/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "YouPorn": {
        "url": "https://www.youporn.com/user/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    },
    "Zillow": {
        "url": "https://www.zillow.com/profile/{}",
        "exists_check": "Page Not Found",
        "method": "text"
    }
}

def check_username_on_platform(platform_name, platform_info, username):
    url = platform_info["url"].format(username)
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=5)

        if platform_info["method"] == "status_code":
            if response.status_code == platform_info["exists_check"]:
                return platform_name, "FOUND", url
            else:
                return platform_name, "NOT FOUND", None
        elif platform_info["method"] == "text":
            if platform_info["exists_check"] in response.text:
                return platform_name, "NOT FOUND", None
            else:
                # If the 'not found' text is NOT present, it implies the user might exist
                # This is a heuristic and might need refinement for some platforms
                return platform_name, "FOUND", url

    except requests.exceptions.RequestException as e:
        return platform_name, f"ERROR ({e})", None
    except Exception as e:
        return platform_name, f"UNKNOWN ERROR ({e})", None
    return platform_name, "UNKNOWN", None

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 username_tracker.py <username>")
        sys.exit(1)

    username = sys.argv[1]
    print(f"[*] Searching for username: {username}\n")

    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_platform = {
            executor.submit(check_username_on_platform, name, info, username):
            name for name, info in PLATFORMS.items()
        }
        for future in as_completed(future_to_platform):
            platform_name, status, url = future.result()
            results.append((platform_name, status, url))

    # Sort results for consistent output
    results.sort(key=lambda x: x[0])

    for platform_name, status, url in results:
        if status == "FOUND":
            print(f"[+] {platform_name}: {status} - {url}")
        elif status == "NOT FOUND":
            print(f"[-] {platform_name}: {status}")
        else:
            print(f"[!] {platform_name}: {status}")

if __name__ == "__main__":
    main()
