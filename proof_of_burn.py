import json
import time
import copy
import random
from hashlib import sha256

class Coinbase:
    def __init__(self, total_coins):
        self.total_coins = total_coins
        self.burned_coins = 0

    def circ_coins(self, circ_amt):
        self.total_coins -=  circ_amt

    def reward_deduction(self, reward_amt):
        self.total_coins -= reward_amt

    def burn_coins(self, amount):
        if amount <= self.total_coins:
            self.total_coins -= amount
            self.burned_coins += amount
            return True
        else:
            print("Not enough coins to burn")
            return False

    def get_status(self):
        return {
            "total_coins": self.total_coins,
            "burned_coins": self.burned_coins
        }

class Block:
    def __init__(self, txn_data, block_hash, merkle_root=None, nonce=None):
        self.txn_data = txn_data
        self.block_hash = block_hash
        self.merkle_root = merkle_root
        self.nonce = nonce
        self.prev_block = None
        self.prev_hash = None

    def add_to_blockchain(self, blockchain):
        self.prev_block = blockchain.top_block
        self.prev_hash = blockchain.top_block.block_hash
        blockchain.top_block = self
        blockchain.chain.append(self)

class Blockchain:
    def __init__(self):
        self.chain = []
        self.top_block = self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis_block = Block("genesis", sha256("genesis".encode('utf-8')).hexdigest())
        return genesis_block

    def add_block(self, block: Block):
        block.add_to_blockchain(self)

    def get_blockchain_copy(self):
        return copy.deepcopy(self.chain)


class User:
    def __init__(self, user_addr: str, balance: float):
        self.user_addr = user_addr
        self.balance = balance

    @staticmethod
    def search_user(user_list, user_addr):
        for user in user_list:
            if user.user_addr == user_addr:
                return user
        return None

def hashmark(mem_pool, nonce):
    value = str(mem_pool) + str(nonce)
    return sha256(value.encode('utf-8')).hexdigest()

def merkle_root(mem_pool):
    return sha256(str(mem_pool).encode('utf-8')).hexdigest()

def pob_consensus(burn_proofs) -> str:
    consensus_probability = []
    for pub_key in burn_proofs:
        consensus_probability += [pub_key] * burn_proofs[pub_key]
    miner_id = random.choice(consensus_probability)
    return miner_id

def format_num(value):
    return float("{:.10f}".format(float(value)))

def reward_miner(user_dict, miner_id, reward_amount):
    if miner_id in user_dict:
        user_dict[miner_id] += reward_amount
    else:
        user_dict[miner_id] = reward_amount

def mine(mem_pool, blockchain, coinbase, user_dict):
    print("\n\n\n *** mining started ***")

	# this represents the custodians of the burn objective, plus a value in coins
    burn_proofs = {
        "usr001": random.randint(1, 15),
        "usr002": random.randint(1, 15),
        "usr003": random.randint(1, 15),
        "usr004": random.randint(1, 15),
        "usr005": random.randint(1, 15),
        "usr006": random.randint(1, 15),
        "usr007": random.randint(1, 15),
        "usr008": random.randint(1, 15),
        "usr009": random.randint(1, 15),
        "usr010": random.randint(1, 15),
        "usr011": random.randint(1, 15),
        "usr012": random.randint(1, 15),
        "usr013": random.randint(1, 15),
        "usr014": random.randint(1, 15)
    }

    miner_id = pob_consensus(burn_proofs)
    print("selected miner:", miner_id)
    difficulty_level = 5
    nonce = 1
    hashed = None
    while True:
        hashed = hashmark(mem_pool, nonce)
        nonce += 1
        if hashed[:difficulty_level] == "0" * difficulty_level:
            print("block created.")
            break

    if coinbase.burn_coins(burn_proofs[miner_id]):
        coinbase_txn = f"Coinbase: {miner_id} burned {burn_proofs[miner_id]} coins"
        mem_pool.append(coinbase_txn)
        block = Block(
            txn_data = mem_pool, 
            block_hash = hashed, 
            merkle_root=merkle_root(mem_pool), 
            nonce = nonce - 1
        )

        
        block.add_to_blockchain(blockchain)
        print(f'block added to blockchain: {block.block_hash}')
        print(f"new block data: {block.txn_data}")		
        print(f"new block merkle root: {block.merkle_root}")
        print(f"new block nonce: {block.nonce}")
        print(f"previous block: {block.prev_block.txn_data}")
        print(f"previous hash: {block.prev_hash}")
        low_reward = 0.05
        high_reward = 2.25
        reward = random.uniform(low_reward, high_reward)
        reward_miner(
                user_dict, 
                miner_id, 
                burn_proofs[miner_id] * reward
        )
        coinbase.reward_deduction(reward)
        print(f"miner: {miner_id} received {reward} coins for mining and burning.")
        print(f"new coinbase status:\n {coinbase.get_status()}")
        time.sleep(1)
        return user_dict

    else:
        print("failed to burn coins")


def transaction( sender_public_key, 
				receiver_public_key, 
				amount, 
				users,
                user_list,
				mem_pool, 
				unsuccessful_transactions ):
    if sender_public_key in users and receiver_public_key in users and amount <= users[sender_public_key]:
        print("successful")
        users[sender_public_key] -= amount
        users[receiver_public_key] += amount
        mem_pool.append({
            "sender": sender_public_key,
            "receiver": receiver_public_key,
            "transaction_amount": amount
        })
        print(mem_pool)
        return users
    else:

        print("unsuccessful")
        unsuccessful_transactions.append({
            "sender": sender_public_key,
            "receiver": receiver_public_key,
            "transaction_amount": amount
        })
        print(unsuccessful_transactions)
        return users

def create_user_list(users_dict):
    return [User(user_addr, balance) for user_addr, balance in users_dict.items()]

def generate_users(min_users=15, max_users=200):
    num_users = random.randint(min_users, max_users)
    users = {}
    for i in range(1, num_users + 1):
        user_id = f"usr{i:03d}"
        balance = round(random.uniform(0.01, 1000.0), 10)  # random balance between 0.01 and 1000.0 with up to 10 decimal places
        users[user_id] = balance
    return users

def main():
	# declarati
    
    blockchain = Blockchain()
    unsuccessful_transactions = []
    mem_pool = []
    coinbase = Coinbase(total_coins=1_000_000) # 1 million coins 
   
    '''
	# one can have a fixed user addr base 
    users = {
        "usr001": 101.0,
        "usr002": 102.0,
		"usr003": 132.5,
		"usr004": 252.2,
		"usr005": 142.8,
		"usr006": 231.2,
		"usr007": 138.7,
		"usr008": 116.2,
		"usr009": 121.11,
		"usr010": 68.334534534,
		"usr011": 24.834534,
		"usr012": 403.434
		"usr013": 10002.532
		"usr014": 60000.4533453
		"usr015": 233242.4333434
    }
    '''
    # or we can generate a random pool using the function
    users = generate_users()	
	
    #print("top block data: ")
    print(blockchain.top_block.txn_data)
    print("keys: ")
    # get account names/hashes
    ulist = [ key for key in users.keys() ]
    print(ulist)
    # adjust coinbase for known held coins
    amt_held = sum([ value for value in users.values() ])
    coinbase.circ_coins(amt_held)
    print(f"coinbase status after accounting for circulating coins:\n {coinbase.get_status()}")

    counter = 0
    while [ 1 ]:
        user_list = create_user_list(users)
        # debug
        #print(f"User List: {user_list}")
        print("miner list: ")
        for user in user_list[:15]:
            print(f"user_addr: {user.user_addr}, balance: {user.balance}")
        print(f"total number of user accounts: {len(user_list)}")

        #cont_inp = input("Would you like to continue? y/n : ")
        cont_inp = 'y'
        if cont_inp == 'y' or cont_inp == 'Y':
            # debug
            #sender_public_key = input("enter your public key : ")
            sender_public_key = random.choice(ulist)
            print(f"sender: {sender_public_key}")
            search_result = user.search_user(user_list, sender_public_key)
            if not search_result:
                print("sender_public_key not found.")
                continue
            # debug
            #receiver_public_key = input("enter receiver public key : ")
            receiver_public_key = random.choice(ulist) 
            print(f"receiver: {receiver_public_key}")
            time.sleep(1)
            search_result = user.search_user(user_list, receiver_public_key)
            if not search_result:
                print("receiver_public_key not found.")
                continue
            min_val = 0.1
            max_val = 14.9
            amount = random.uniform(min_val, max_val)
            amount = format_num( amount )


            users = transaction(
                    sender_public_key, 
                    receiver_public_key, 
                    amount, 
                    users, 
                    user_list, 
                    mem_pool, 
                    unsuccessful_transactions
            )
            if ( len ( mem_pool ) == 2):
                users = mine( mem_pool, blockchain, coinbase, users )
                mem_pool = []
            if counter % 20 == 0:
                blockchain_copy = blockchain.get_blockchain_copy()
                for block in blockchain_copy:
                    print(f"block hash: {block.block_hash}\nprevious hash: {block.prev_hash}")
            counter += 1
            time.sleep(1)
        else:
            break

if __name__ == "__main__":
    main()
