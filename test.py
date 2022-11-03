import argparse
import os
import os
import time
from utils import killport, bcolors, compile, printStatus, generateProfiles


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
    '--i', help="number of immediate proposer, default: 1", type=int, default=1)
parser.add_argument(
    '--no', help="number of normal proposer, default: 0", type=int, default=0)
parser.add_argument(
    '--l', help="numner of late proposer, default: 0", type=int, default=0)
parser.add_argument(
    '--nv', help="number of never proposer, default: 0", type=int, default=0)
parser.add_argument(
    '--test', help="test mode current choice: acceptors", type=str, default="")
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
dir = None

if test == "acceptor" and failure == False:
    # configuration on acceptor test
    acceptersCount = [2**k-1 for k in range(2, 12)]
    max_delay = 100
    verbose = "false"
    iter = len(acceptersCount)

dir = f"{test}-failure-{failure}"

if not os.path.exists(dir):
    os.system(f"mkdir {dir}")


def init():
    killport(8080)
    compile()


def runTest():
    for round in range(rounds):
        continueTest = True

        open(f"{dir}/experiment-{round}.txt", 'w').close()
        for j in range(iter):
            if not continueTest:
                break
            open("result.txt", 'w').close()
            if test == "acceptor":
                accept = acceptersCount[j]
            # accept = accepters[j]
            # profiles = generateProfiles(accept, immed, normal, late, never)
            numRequiredVotes = int(accept/2) + 1

            profiles = generateProfiles(accept, immed, normal, late, never)
            print("Acceptors :", accept, "Immediate :", immed,
                  "Normal :", normal, "Late :", late, "Never :", never)
            n = accept + immed + normal + late + never
            os.system(
                f"java CommunicatorServer {n} {dir}/experiment-{round}.txt &")
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


if __name__ == "__main__":
    init()
    runTest()
