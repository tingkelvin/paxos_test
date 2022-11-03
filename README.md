# Assignment 3

## Testing

Add the following argument to change the number of members, if you want to toy with it. We have a already setup a bunch of environment for testing.

```sh
  --verbose VERBOSE     verbose mode on proposer, default: true
  --verboseCS VERBOSECS
                        verbose mode on communicator sever, default: false
  --iter ITER           number of iteration, default: 1
  --a A                 number of acceptor, default: 1
  --i I                 number of immediate proposer, default: 1
  --no NO               number of normal proposer, default: 0
  --l L                 numner of late proposer, default: 0
  --nv NV               number of never proposer, default: 0
  --test TEST           test mode current choice: acceptors
  --rounds ROUNDS       number of rounds, default: 10
  --maxDelay MAXDELAY   delay on reproposing, default: 10
  --failure FAILURE     failure mode, default: false
```

## Kill alll java processes

```sh
killall -9 java
```

## Kill alll python processes

```sh
pkill python
```

## Test 1 how the number of acceptors affect the run time?

The test will run without failure mode on and one immediate proposer.

Number of acceptors: [3, 7, 15, 31, 63, 127, 255, 511, 1023, 2047]

The result is saved in acceptor-failure-False.

```sh
python3 test.py --test acceptor
```
