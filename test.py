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
    '--test', help="test mode current choice: acceptors", type=str, default="")
parser.add_argument(
    '--rounds', help="number of rounds, default: 10", type=int, default=10)
parser.add_argument(
    '--failure', help="failure mode, default: false", type=bool, default=False)
parser.add_argument(
    '--port', help="port, default: 8080", type=int, default=8080)
args = parser.parse_args()
verbose = args.verbose
verboseCS = args.verboseCS
iter = args.iter
rounds = args.rounds
failure = args.failure
port = args.port
test = args.test
dir = None
normalCount = None

if test == "acceptor":
    # configuration on acceptor test
    acceptersCount = [2**k-1 for k in range(2, 12)]
    verbose = "false"
    max_delay = 100
    iter = len(acceptersCount)

if test == "immed":
    # configuration on acceptor test
    proposerCount = [i for i in range(1, 11)]
    verbose = "false"
    iter = len(proposerCount)

if test == "normal":
    # configuration on acceptor test
    normalCount = [i for i in range(1, 11)]
    verbose = "false"
    iter = len(normalCount)

if test == "late":
    # configuration on acceptor test
    lateCount = [i for i in range(1, 11)]
    verbose = "false"
    iter = len(lateCount)

dir = f"{test}-failure-{failure}"

if not os.path.exists(dir):
    os.system(f"mkdir {dir}")


def init():
    killport(port)
    compile()


def runTest():
    normal, immed, accept, late = 0, 0, 0, 0
    for j in range(iter):
        continueTest = True
        if test == "acceptor":
            accept = acceptersCount[j]
            immed = 3
            maxDelay = 100
            file = f"{accept}-ACCEPTORS.csv"
            fileDir = f"{dir}/{file}"
            open(fileDir, 'w').close()

        if test == "immed":
            accept = 10
            if failure:
                maxDelay = 6*accept*2
            else:
                maxDelay = 2*accept*2
            immed = proposerCount[j]
            file = f"{immed}-IMMED-PROPOSERS"
            fileDir = f"{dir}/{file}"
            open(fileDir, 'w').close()

        if test == "normal":
            accept = 10
            maxDelay = 6*accept
            normal = normalCount[j]
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
            with open('id.txt', 'w') as f:
                f.write('%d' % 0)

            numRequiredVotes = int(accept/2) + 1
            profiles = generateProfiles(
                accept, immed, normal, late, failure)
            counter = {}
            for i, (k, v) in enumerate(profiles.items()):
                if v in counter:
                    counter[v] += 1
                else:
                    counter[v] = 1
            print(counter)

            n = accept + immed + normal + late
            os.system(
                f"java CommunicatorServer {n} {fileDir} {port}&")
            time.sleep(0.1)
            for i, (k, v) in enumerate(profiles.items()):
                # print(v)
                os.system(
                    f"java Member {k} {v} {numRequiredVotes} {accept} {maxDelay} {port} {('' if i == len(profiles) -1  else '&')}")
                time.sleep(0.1)
            # printStatus("OKCYAN", "Comparing Test Results")

            # Checking if the value is consistent

            # f = open("result.txt", "r")
            # value = None
            # for line in f:
            #     content = line.split(", ")
            #     if content[0] == "value":
            #         if value == None:
            #             value = int(content[1])
            #             print(f"value : {value}")
            #         if int(content[1]) != value:
            #             continueTest = False
            #             printStatus(
            #                 "WARNING", f"Test did not passed. The value does not match.")
            #             raise Exception('The value does not match.')
            #     else:
            #         member = int(content[0])
            #         memberValue = content[1].strip()
            #         printStatus("OKCYAN", f"Member {member} : {value}")
            #         if int(memberValue) != value:
            #             continueTest = False
            #             printStatus(
            #                 "WARNING", f"Test did not passed.")
            #             raise Exception('The value does not match.')

            # printStatus("OKGREEN", f"Test {j} passed.")
            time.sleep(1)
            killport(port)
        df = pd.read_csv(fileDir, names=["run time", "consensus  time", "value",  "messages", "delay",
                         "immediate", "normal", "late", "never",  "acceptors"])
        df.to_excel(f"{dir}/{file}.xlsx",
                    f"{file}", index=False)


if __name__ == "__main__":
    init()
    runTest()
