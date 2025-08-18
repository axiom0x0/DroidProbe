#!/usr/bin/env python3

import adbutils
import time
import argparse
import subprocess
from datetime import datetime, UTC
import sys

def parse_args():
    parser = argparse.ArgumentParser(description="Connect to Android devices over ADB and gather system info.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-i", "--ip", help="Single IP address of the device")
    group.add_argument("-f", "--file", help="File containing list of IP addresses")
    return parser.parse_args()

def main():
    args = parse_args()

    if args.ip:
        targets = [args.ip]
    else:
        with open(args.file) as f:
            targets = [line.strip() for line in f if line.strip()]

    scantime = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    time.sleep(1)

    print('IPAddr,MACAddr,Whoami,Model,OSVer,CPUArch,su_present,rootable,scantime')
    for target in targets:
        line = target + ":5555"
        try:
            device = adb.connect(line, timeout=2.0)
            d = adb.device()
            ip = line.split(':')[0]
            mac = subprocess.run(["adb", "shell", "ip", "addr", "show", "eth0", "|grep", "link/ether", "|", "cut", "-d", "\' \'", "-f6"], capture_output=True, text=True)
            whoami = d.shell(["whoami"])
            Model = d.shell(["getprop", "ro.product.model"])
            OSver = "Android " + d.shell(["getprop", "ro.build.version.release"])
            CPUArch = d.shell(["getprop", "ro.product.cpu.abilist"]).replace(',', ';')
            su_present = d.shell("which su")
            if su_present != "":
                su_present = True
            else:
                su_present = False
            if whoami.strip() == 'root':
                rootable = True
            elif su_present:
                su_output = d.shell("echo id | su")
                if "uid=0" in su_output:
                    rootable = True
                else:
                    rootable = False
            else:
                rootable = False
            print(ip, mac.stdout.strip().replace(':',''), whoami, Model, OSver, CPUArch, su_present, rootable, scantime, sep=',')
            adb.disconnect(line)
        except KeyboardInterrupt:
            adb.disconnect(line)
            sys.exit(1)
        except Exception as e:
            adb.disconnect(line)

if __name__ == "__main__":
    main()
