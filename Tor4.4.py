import requests
import os
from time import sleep
from colorama import init, Fore, Style

def main():
    # Initialize colorama
    init(autoreset=True)

    try:
        change = int(input("After how many seconds do you want to change IP? "))
    except KeyboardInterrupt:
        print(Fore.CYAN + "\nScript interrupted before input. Exiting cleanly...")
        return

    # Start Tor in Termux
    os.system("pkg install tor -y")
    os.system("tor &")

    url = "https://httpbin.org/ip"
    proxy = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }

    try:
        while True:
            try:
                response = requests.get(url, proxies=proxy)
                if response.status_code == 200:
                    print(Fore.GREEN + "Your current IP: {}".format(response.json().get("origin")))
                else:
                    print(Fore.RED + "Failed to get current IP")
            except requests.exceptions.RequestException as e:
                print(Fore.RED + f"An error occurred: {e}")
            
            sleep(change)
            os.system("pkill -HUP tor")
            print(Fore.YELLOW + "IP address changed, reloading Tor...")
    except KeyboardInterrupt:
        print(Fore.CYAN + "\nScript interrupted. Exiting cleanly...")
        os.system("pkill tor")
        print(Fore.CYAN + "Tor service stopped.")

if __name__ == "__main__":
    main()
