import requests
import argparse
import re


def login():
    url = "https://account.coolapk.com/auth/loginByCoolapk"
    response = requests.get(url)
    match = re.search(r"requestHash\s*:\s*'(\w+)'", response.text)
    if match:
        request_hash = match.group(1)
        print(f"The request hash is {request_hash}")
    else:
        print("Failed to extract the request hash from the response.")
        exit(255)


def main():
    parser = argparse.ArgumentParser(description="A script for publishing the Coolapk application")
    parser.add_argument("-u", "--username", help="Your Coolapk Username")
    parser.add_argument("-p", "--password", help="Your Coolapk Password")
    parser.add_argument("-id", "--apk_id", dest="id", help="Your APK ID")
    parser.add_argument("-path", "--apk_path", dest="path", help="Your Apk Path")
    parser.add_argument("-log", "--update_logs", dest="log", help="Your Apk Update Logs")

    args = parser.parse_args()

    if not (args.username and args.password and args.id and args.path and args.log):
        parser.print_help()
        exit()

    print("Username: ", args.username)
    print("Password: ", args.password)
    print("APK ID: ", args.id)
    print("APK Path: ", args.path)
    print("Update Logs: ", args.log)
    login()


if __name__ == '__main__':
    main()
