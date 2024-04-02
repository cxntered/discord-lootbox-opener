import requests
from colorama import Fore, Style
from time import localtime, strftime, sleep

url = "https://discord.com/api/v9/users/@me/lootboxes/open"

# headers taken directly from a native discord client's request,
# with the exception of the 'cookie' header (doesn't seem to be required, also don't wanna give out my cookie) 
# and 'authorization' header (gets set later)
headers = {
    "authority": "discord.com",
    "accept": "*/*",
    "accept-language": "en-US",
    "content-length": "0",
    "origin": "https://discord.com",
    "referer": "https://discord.com/channels/@me",
    "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9038 Chrome/120.0.6099.291 Electron/28.2.7 Safari/537.36",
    "x-debug-options": "bugReporterEnabled",
    "x-discord-locale": "en-US",
    "x-discord-timezone": "Australia/Sydney",
    "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDM4Iiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJpYTMyIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMzggQ2hyb21lLzEyMC4wLjYwOTkuMjkxIEVsZWN0cm9uLzI4LjIuNyBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMjguMi43IiwiY2xpZW50X2J1aWxkX251bWJlciI6MjgwNzA0LCJuYXRpdmVfYnVpbGRfbnVtYmVyIjo0NTUyNCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
}

items = {
    "1214340999644446720": "Buster Blade",
    "1214340999644446721": "Cute Plushie",
    "1214340999644446722": "Wump Shell",
    "1214340999644446723": "Speed Boost",
    "1214340999644446724": "⮕⬆⬇⮕⬆⬇",
    "1214340999644446725": "Power Helmet",
    "1214340999644446726": "Quack!!",
    "1214340999644446727": "OHHHHH BANANA", # 727 WYSI
    "1214340999644446728": "Dream Hammer"
}

class DiscordLootboxOpener:
    def __init__(self, token, lootboxes, delay):
        headers.update({"authorization": token})
        self.lootboxes = lootboxes
        self.delay = delay
            
    def open_lootboxes(self):
        opened_lootboxes = 0
        for i in range(self.lootboxes):
            response = requests.post("https://discord.com/api/v9/users/@me/lootboxes/open", headers=headers)

            if response.status_code == 429:
                print(f"{Fore.YELLOW}[{strftime("%H:%M:%S", localtime())}] | Rate limited, waiting 5 seconds... ({i+1}/{self.lootboxes})")
                sleep(5)
            elif response.status_code == 401:
                print(f"{Fore.RED}[{strftime("%H:%M:%S", localtime())}] | Error: 401 Unauthorized! Did you enter an invalid token? ({i+1}/{self.lootboxes})")
                print(f"{Fore.RED}Exiting due to invalid token...")
                return
            elif response.status_code != 200:
                print(f"{Fore.RED}[{strftime("%H:%M:%S", localtime())}] | Failed to open lootbox. Error code: {response.status_code} ({i+1}/{self.lootboxes})")
                break

            data = response.json()
            opened_item_id = data["opened_item"]
            opened_item_name = items[str(opened_item_id)]
            opened_item_count = data["user_lootbox_data"]["opened_items"][opened_item_id]
            opened_lootboxes = sum(data["user_lootbox_data"]["opened_items"].values())

            if response.status_code == 200:
                article = "an" if opened_item_name[0].lower() in "aeiou" else "a"
                print(f"{Fore.GREEN}[{strftime("%H:%M:%S", localtime())}] | You got {article} {Style.BRIGHT}{opened_item_name}{Style.NORMAL}! You now have {opened_item_count} of them! ({i+1}/{self.lootboxes})")

            if i != self.lootboxes - 1:
                sleep(self.delay)

        print(f"{Fore.GREEN}[{strftime("%H:%M:%S", localtime())}] | Finished opening {self.lootboxes} lootboxes! You now have a total of {Style.BRIGHT}{opened_lootboxes} opened lootboxes{Style.NORMAL}!")

if __name__ == "__main__":
    print(f"""{Fore.LIGHTMAGENTA_EX}.------------------------------------------------------------------------.
| cxntered's very epic and awesome                                       |
| ____  _                       _   _                _   _               |
||  _ \\(_)___  ___ ___  _ __ __| | | |    ___   ___ | |_| |__   _____  __|
|| | | | / __|/ __/ _ \\| '__/ _` | | |   / _ \\ / _ \\| __| '_ \\ / _ \\ \\/ /|
|| |_| | \\__ \\ (_| (_) | | | (_| | | |__| (_) | (_) | |_| |_) | (_) >  < |
||____/|_|___/\\___\\___/|_|  \\__,_| |_____\\___/ \\___/ \\__|_.__/ \\___/_/\\_\\|
| / _ \\ _ __   ___ _ __   ___ _ __                                       |
|| | | | '_ \\ / _ \\ '_ \\ / _ \\ '__|                                      |
|| |_| | |_) |  __/ | | |  __/ |                                         |
| \\___/| .__/ \\___|_| |_|\\___|_|                                         |
|      |_|                                                               |
| cxntered.dev • github.com/cxntered/discord-lootbox-opener              |
'------------------------------------------------------------------------'""")
    
    while True:
        try:
            token = input(f"{Fore.LIGHTMAGENTA_EX}[{strftime("%H:%M:%S", localtime())}] | Enter your Discord token (this does not get stored!): {Style.RESET_ALL}")
            if not token:
                print(f"{Fore.RED}You must enter a token!")
                continue

            while True:
                lootboxes = input(f"{Fore.LIGHTMAGENTA_EX}[{strftime("%H:%M:%S", localtime())}] | Enter the amount of lootboxes you want to open: {Style.RESET_ALL}")
                if not lootboxes or not lootboxes.isdigit() or int(lootboxes) < 0:
                    print(f"{Fore.RED}You must enter the amount of lootboxes you want to open!")
                    continue
                break

            while True:
                delay = input(f"{Fore.LIGHTMAGENTA_EX}[{strftime("%H:%M:%S", localtime())}] | Enter the delay between each lootbox opening in seconds (default is 3): {Style.RESET_ALL}")
                if not delay:
                    delay = 3
                elif not delay.isdigit() or int(delay) < 0:
                    print(f"{Fore.RED}You must enter a valid delay!")
                    continue
                break
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Exiting...")
            break

        try:
            DiscordLootboxOpener(token.strip(), int(lootboxes), int(delay)).open_lootboxes()
        except KeyboardInterrupt:
            print(f"{Fore.RED}Lootbox Opener stopped by keyboard interrupt, exiting...")
            break
        except Exception as e:
            print(f"{Fore.RED}An error occurred: {e}")
            continue
        break