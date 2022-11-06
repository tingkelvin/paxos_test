import argparse
import os
import os
import time
from utils import killport, bcolors, compile, printStatus, generateProfiles
import pandas as pd

parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument(
    '--verbose', help="verbose mode on proposer, default: true", type=str, default="true")
parser.add_argument(
    '--verboseCS', help="verbose mode on communicator sever, default: false", type=str, default="false")
parser.add_argument(
    '--iter', help="number of iteration, default: 1", type=int, default=1)
parser.add_argument(
    '--a', help="number of acceptor, default: 1", type=int, default=1)
parser.add_argument(
    '--i', help="number of immediate proposer, default:0", type=int, default=0)
parser.add_argument(
    '--no', help="number of normal proposer, default: 0", type=int, default=0)
parser.add_argument(
    '--l', help="numner of late proposer, default: 0", type=int, default=0)
parser.add_argument(
    '--nv', help="number of never proposer, default: 0", type=int, default=0)
parser.add_argument(
    '--test', help="test mode current choice: acceptors", type=str, default="")
parser.add_argument(
    '--proposer', help="test mode current choice: acceptors", type=str, default="")
parser.add_argument(
    '--rounds', help="number of rounds, default: 10", type=int, default=10)
parser.add_argument(
    '--maxDelay', help="delay on reproposing, default: 10", type=int, default=10)
parser.add_argument(
    '--failure', help="failure mode, default: false", type=bool, default=False)
args = parser.parse_args()
verbose = args.verbose
verboseCS = args.verboseCS
iter = args.iter
rounds = args.rounds
failure = args.failure
accept = args.a
immed = args.i
normal = args.no
late = args.l
never = args.nv
test = args.test
maxDelay = args.maxDelay
proposerType = args.proposer
dir = None
normalCount = None

if test == "acceptor":
    # configuration on acceptor test
    acceptersCount = [2**k-1 for k in range(2, 12)]
    verbose = "false"
    iter = len(acceptersCount)

if test == "proposer":
    # configuration on acceptor test
    proposerCount = [i for i in range(11)]
    verbose = "false"
    iter = len(proposerCount)

if test == "normal":
    # configuration on acceptor test
    normalCount = [i for i in range(11)]
    verbose = "false"
    iter = len(normalCount)

if test == "late":
    # configuration on acceptor test
    lateCount = [i for i in range(11)]
    verbose = "false"
    iter = len(lateCount)

dir = f"{test}-failure-{failure}"

if not os.path.exists(dir):
    os.system(f"mkdir {dir}")


def init():
    killport(8080)
    compile()


def runTest():
    global normal, accept, immed, late

    for j in range(iter):
        continueTest = True
        if test == "acceptor":
            accept = acceptersCount[j]
            immed = 3
            maxDelay = 100
            file = f"{accept}-ACCEPTORS.csv"
            fileDir = f"{dir}/{file}"
            open(fileDir, 'w').close()
        if test == "proposer":
            accept = 10
            maxDelay = 2*accept
            immed = proposerCount[j]
            file = f"{immed}-PROPOSERS"
            fileDir = f"{dir}/{file}"
            open(fileDir, 'w').close()

        if test == "normal":
            accept = 10
            maxDelay = 6*accept
            normal = normalCount[j]
            immed = 10 - normalCount[j]
            file = f"{normal}-NORMAL-PROPOSERS"
            fileDir = f"{dir}/{file}.csv"
            open(fileDir, 'w').close()

        if test == "late":
            accept = 10
            maxDelay = 6*accept
            normal = lateCount[j]
            immed = 10 - lateCount[j]
            file = f"{late}-LATE-PROPOSERS"
            fileDir = f"{dir}/{file}.csv"
            open(fileDir, 'w').close()

        for round in range(rounds):
            if not continueTest:
                break
            open("result.txt", 'w').close()

            numRequiredVotes = int(accept/2) + 1

            profiles = generateProfiles(
                accept, immed, normal, late, never, failure)
            counter = {}
            for i, (k, v) in enumerate(profiles.items()):
                if v in counter:
                    counter[v] += 1
                else:
                    counter[v] = 1
            print(counter)

            n = accept + immed + normal + late + never
            os.system(
                f"java CommunicatorServer {n} {fileDir} &")
            time.sleep(0.1)
            for i, (k, v) in enumerate(profiles.items()):
                # print(v)
                os.system(
                    f"java Member {k} {v} {numRequiredVotes} {accept} {maxDelay} {verbose} {('' if i == len(profiles) -1  else '&')}")
                time.sleep(0.1)
            printStatus("OKCYAN", "Comparing Test Results")
            print(numRequiredVotes)
            # Checking if the value is consistent

            f = open("result.txt", "r")
            value = None
            for line in f:
                content = line.split(", ")
                if content[0] == "value":
                    if value == None:
                        value = int(content[1])
                        print(f"value : {value}")
                    if int(content[1]) != value:
                        continueTest = False
                        printStatus(
                            "WARNING", f"Test did not passed. The value does not match.")
                        raise Exception('The value does not match.')
                else:
                    member = int(content[0])
                    memberValue = content[1].strip()
                    printStatus("OKCYAN", f"Member {member} : {value}")
                    if int(memberValue) != value:
                        continueTest = False
                        printStatus(
                            "WARNING", f"Test did not passed.")
                        raise Exception('The value does not match.')

            printStatus("OKGREEN", f"Test {j} passed.")
            time.sleep(1)
            killport(8080)
        df = pd.read_csv(fileDir, names=["run time", "consensus  time", "value",  "messages", "delay",
                         "immediate", "normal", "late", "never",  "acceptors"])
        df.to_excel(f"{dir}/{file}.xlsx",
                    f"{file}", index=False)


if __name__ == "__main__":
    init()
    runTest()
