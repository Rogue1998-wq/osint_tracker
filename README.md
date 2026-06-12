# OSINT Username Tracker

This Python script allows you to track a given username across over 50 popular online platforms, helping you to quickly determine if a person uses the same username on different social media, coding, or other web services. This is a valuable tool for Open Source Intelligence (OSINT) gathering, useful for security researchers, investigators, or anyone looking to consolidate online presence information.

## Features

*   Checks username availability/existence on 50+ platforms.
*   Supports concurrent checks for speed.
*   Clear output indicating whether the username is found or not on each platform.
*   Easy to extend with new platforms.

## Supported Platforms (50+)

*   GitHub
*   Twitter
*   Instagram
*   Reddit
*   LinkedIn
*   Pinterest
*   TikTok
*   YouTube
*   Twitch
*   Medium
*   Dev.to
*   Flickr
*   Steam
*   Etsy
*   Cash App
*   Patreon
*   Blogger
*   About.me
*   Imgur
*   Pastebin
*   Vimeo
*   SoundCloud
*   Bandcamp
*   Last.fm
*   Gravatar
*   Keybase
*   HackerOne
*   Bugcrowd
*   Docker Hub
*   npmjs
*   PyPI
*   RubyGems
*   Wordpress
*   Disqus
*   Dribbble
*   Behance
*   Codepen
*   Replit
*   Stack Overflow
*   Ask.fm
*   Foursquare
*   Goodreads
*   ImgPile
*   LiveJournal
*   Periscope
*   Product Hunt
*   Quora
*   Scribd
*   Slideshare
*   SmugMug
*   Taringa!
*   Telegram
*   Tumblr
*   Vero
*   VK
*   We Heart It
*   Xing
*   Zhihu
*   Academia.edu
*   AngelList
*   Bitbucket
*   Dailymotion
*   Ebay
*   Fiverr
*   Freelancer
*   GitLab
*   Gfycat
*   ImgBB
*   Kickstarter
*   Mixcloud
*   OkCupid
*   Pexels
*   Pixabay
*   Pornhub
*   Redbubble
*   ReverbNation
*   ScribbleHub
*   Shutterstock
*   StackExchange
*   Unsplash
*   VSCO
*   Wattpad
*   Weebly
*   Wikipedia
*   Xvideos
*   YouPorn
*   Zillow

## Installation

1.  **Clone the repository** (or download the `username_tracker.py` file):
    ```bash
    git clone https://github.com/your-username/osint-username-tracker.git
    cd osint-username-tracker
    ```

2.  **Install dependencies**:
    This script requires the `requests` library. You can install it using pip:
    ```bash
    pip install requests
    ```

## Usage

Run the script from your terminal, providing the username you want to track as an argument:

```bash
python3 username_tracker.py <username>
```

**Example**:

```bash
python3 username_tracker.py johndoe123
```

## How it Works

The script iterates through a predefined list of platforms. For each platform, it constructs a URL using the provided username and then makes an HTTP GET request. It then analyzes the response (either the HTTP status code or the page content) to determine if the username exists on that platform. The `PLATFORMS` dictionary in the script contains the logic for each platform's existence check.

## Extending Supported Platforms

You can easily add more platforms by editing the `PLATFORMS` dictionary in `username_tracker.py`. For each new platform, you'll need:

*   **`url`**: The URL template where `{}` will be replaced by the username.
*   **`exists_check`**: The value to look for to determine if the username *does not* exist. This can be an HTTP status code (e.g., `404`) or a specific string in the response text (e.g., "Page Not Found").
*   **`method`**: Either `"status_code"` or `"text"`, indicating how the `exists_check` should be performed.

## Disclaimer

This tool is intended for educational and legitimate OSINT purposes only. Please use it responsibly and respect the privacy of individuals. Unauthorized access or misuse of information obtained through this tool is strictly prohibited. The accuracy of results may vary depending on changes to platform websites and their user existence checking mechanisms.
