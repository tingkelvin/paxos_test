import argparse
import os
import os
import time
from utils import killport, bcolors, compile, printStatus, generateProfiles


parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('--n', type=int, default=9)
parser.add_argument('--verbose', type=str, default="true")
parser.add_argument('--verboseCS', type=str, default="false")
parser.add_argument('--iter', type=int, default=1)
parser.add_argument('--a', type=int, default=6)
parser.add_argument('--i', type=int, default=1)
parser.add_argument('--no', type=int, default=0)
parser.add_argument('--l', type=int, default=0)
parser.add_argument('--nv', type=int, default=0)
parser.add_argument('--test', type=str, default="")
parser.add_argument('--rounds', type=int, default=10)
parser.add_argument('--failure', type=bool, default=False)
args = parser.parse_args()
verbose = args.verbose
verboseCS = args.verboseCS
iter = args.iter
rounds = args.rounds
failure = args.failure
# immed = 1
# normal = 0
# late = 0
# never = 0

accept = args.a
immed = args.i
normal = args.no
late = args.l
never = args.nv
test = args.test
maxDelay = 10
dir = None
if test == "acceptor" and failure == False:
    acceptersCount = [1 for k in range(2, 12)]
    max_delay = 100
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
            print(accept, immed, normal, late, never)
            n = accept + immed + normal + late + never
            os.system(
                f"java CommunicatorServer {n} {dir}/experiment-{round}.txt &")
            time.sleep(0.1)
            for i, (k, v) in enumerate(profiles.items()):
                # print(v)
                os.system(
                    f"java Member {k} {v} {numRequiredVotes} {accept} {maxDelay} {('' if i == len(profiles) -1  else '&')}")
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
