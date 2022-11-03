import filecmp
from genericpath import isfile
import os
import signal
from subprocess import PIPE, Popen
import random

bcolors = {
    "HEADER": '\033[95m',
    "OKBLUE": '\033[94m',
    "OKCYAN": '\033[96m',
    "OKGREEN": '\033[92m',
    "WARNING": '\033[4m\033[1m\u001b[31m',
    "FAIL": '\033[91m',
    "ENDC": '\033[0m',
    "BOLD": '\033[1m',
    "UNDERLINE": '\033[4m',
}


def killport(port):
    # printStatus("HEADER}")
    printStatus(
        "HEADER", f"Killilng process at PORT {port} and java process...")
    try:
        process = Popen(
            ["lsof", "-i", ":{0}".format(port)], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        for process in str(stdout.decode("utf-8")).split("\n")[1:]:
            data = [x for x in process.split(" ") if x != '']
            if (len(data) <= 1):
                continue
            os.kill(int(data[1]), signal.SIGKILL)
    except:
        # printStatus("WARNING}Failed to kill.")
        printStatus("WARNING", "Failed to kill.")


def compile():
    # printStatus("HEADER}Removing .class and .txt files...")
    printStatus("HEADER", "Removing .class and .txt files...")
    try:
        os.system("rm *.class")

    except:
        printStatus("WARNING", "Failed to remove.")
    printStatus("HEADER", "Removed sucessfully.")

    printStatus("HEADER", "Compiling java files... Then run.")
    try:
        os.system("javac utils/*.java")
        os.system("javac *.java")
    except:
        printStatus("WARNING", "Failed to compile.")


def printStatus(type, str):
    type = bcolors[type]
    end = bcolors["ENDC"]
    print(f"{type}{str}{end}")


def generateID(size):
    return random.sample(range(1, size+1), size), random.randint(1, size)


def generateProfilesID(start, size):
    return random.sample(range(start, start+size), size)


def generateRandomProfilesID(size, profiles):
    return random.sample(range(1, size+1), size), random.sample(range(1, size+1), profiles)


def generateProfiles(accept, immed, normal, late, never):
    setting = ["acceptor", "immediate", "unresponsive", "normal", "never"]
    profiles = {}
    currentID = 1

    immedID = generateProfilesID(currentID, immed)
    for id in immedID:
        profiles[id] = "immediate"
    currentID = currentID + len(immedID)
    unresID = generateProfilesID(currentID, never)
    for id in unresID:
        profiles[id] = "unresponsive"
    currentID = currentID + len(unresID)
    normalID = generateProfilesID(currentID, normal)
    for id in normalID:
        profiles[id] = "normal"
    currentID = currentID + len(normalID)
    lateID = generateProfilesID(currentID, late)
    for id in lateID:
        profiles[id] = "late"
    currentID = currentID + len(lateID)
    acceptorID = generateProfilesID(currentID, accept)
    for id in acceptorID:
        profiles[id] = "acceptor"

    return profiles


def generateDelay(maxDelay, profiles):
    delay = {}
    for i in range(1, 10):
        delay[i] = random.randint(0, maxDelay)
    delay[profiles[0]] = 0
    delay[profiles[1]] = maxDelay
    return delay


def generateResponseRate(maxRate, profiles):
    rate = {}
    for i in range(1, 10):
        rate[i] = maxRate

    rate[profiles[1]] = random.randint(0, 40)
    rate[profiles[2]] = random.randint(40, 80)

    return rate
