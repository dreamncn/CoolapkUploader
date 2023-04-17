import argparse

import CoolApi
from Log import *

debuggable = False


def main():
    parser = argparse.ArgumentParser(description="A script for publishing the coolapk application")
    parser.add_argument("-u", "--username", help="your coolapk username")
    parser.add_argument("-p", "--password", help="your coolapk password")
    parser.add_argument("-id", "--apk_id", dest="id", help="your apk id")
    parser.add_argument("-path", "--apk_path", dest="path", help="your apk path")
    parser.add_argument("-log", "--update_logs", dest="log", help="your apk update logs")
    parser.add_argument("-app", "--baidu_app", dest="baidu_app", help="baidu app id")
    parser.add_argument("-bid", "--baidu_id", dest="baidu_id", help="baidu key id")
    parser.add_argument("-s", "--baidu_secret", dest="baidu_secret", help="baidu secret id")

    parser.add_argument("-d", "--debuggable", default=False, dest="debug", help="is debuggable")
    argv = parser.parse_args()
    global debuggable
    debuggable = argv.debug == "True"
    log("IsDebuggable", argv.debug, WARNING)
    if not (argv.username and argv.password and argv.id and argv.path and argv.log):
        parser.print_help()
        exit(255)
    log("--------------Command Info Start-----------------", None, INFO)
    log("Username", argv.username, INFO)
    log("Password", argv.password, INFO)
    log("APK ID", argv.id, INFO)
    log("APK Path", argv.path, INFO)
    log("Update Logs", argv.log, INFO)
    log("Baidu App Id", argv.baidu_app, INFO)
    log("Baidu Key Id", argv.baidu_id, INFO)
    log("Baidu key Secret", argv.baidu_secret, INFO)
    log("--------------Command Info End-----------------", None, INFO)
    args = {
        'username': argv.username,
        'password': argv.password,
        'id': argv.id,
        'path': argv.path,
        'log': argv.log,
        'baidu_app': argv.baidu_app,
        'baidu_id': argv.baidu_id,
        'baidu_secret': argv.baidu_secret,
    }
    CoolApi.login(args)
  # CoolApi.listApps()


if __name__ == '__main__':
    main()
