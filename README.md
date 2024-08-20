# proof_of_burn


#### blockchain proof of concept and economics experiment using diminishing coinbase value

- since proof of burn blockchains provide natural scarcity by diminishing the coinbase over time, we can play with standard variables to see what a sustainable burn rate is, practically
- this script uses a mining function which both burns a randomized number of coins and rewards the miner for doing so
- we can alter the rewards, the burn function, the coinbase, and the account functions to see what levels or equilibrium can be achieved
- the script is designed to be run as an experiment over time, but can be altered to run more or less quickly, and show relevant results and progress thereof
- there is a mining difficulty that is adjustable for speed or more reaslistic scenarios - higher difficulties will take a single processor quite a while 
- every 20 iterations the blockchain will be printed for reference, showing linked progression through hashes
- there is a potential for unsuccessful transactions, which do not trigger changes in balances or mining and are collected into a seperate list; most of these are simply addresses that have been drained before being selected for payment transfers
- this proof of burn implementation differs from the "unspendable address" proof of burn because there aren't addresses implemented in hashed units - so the coins are simply deducted from the coinbase
