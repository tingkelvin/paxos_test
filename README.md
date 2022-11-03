# Assignment 3

## Testing

Add the following argument to change the number of members,

```sh
--iter no_of_iteration default: 10
--a no_of_acceptors
--i no_of_immediate_proposer
--no no_of_normal_proposer
--l no_of_late_proposer
--nv no_of_never_proposer
--test testmode #currently support acceptors
```

## Test 1 how the number of acceptors affect the run time?

```sh
python3 test.py --iter 10 --a 10 --i 2 --no 2 --l 2 --nv 1
```
