#!/usr/bin/python


'''

ethereum.py provides basic classes and structures for contract testing.

This is not a substitute for the testnet, but should help increase the speed
of prototyping contracts.

To use, `import * from ethereum`

The following low level objects will become available:
EBN - an object that acts as either an int or a byte array depending on context.

TODO: EBN will be a representation of RLP in Ethereum. Arithmetic operations
cannot be done if there is a sublist involved. EG: [1,1] + 1 = ?. Unless meaning
can be found in that action it won't be implemented.

Does not yet support sublists.

'''



# LOW LEVEL OBJECTS



class EBN:
	'''EBN = Ethereum Byte Number
	Special data structure where it acts as a number and a byte array.
	Slices like a byte array
	Adds and compares like a number
	Hashes like a byte array
	'''
	def __init__(self, initString, fromHex=True):
		if fromHex == True:
			'''input should be a string in hex encoding'''
			self.this = initString.decode('hex') # byte array
		else:
			self.this = initString
		
	def __lt__(self, other):
		return int(self) < int(other)
	def __gt__(self, other):
		return int(self) > int(other)
	def __eq__(self, other):
		return int(self) == int(other)
	def __ne__(self, other):
		return int(self) != int(other)
	def __le__(self, other):
		return int(self) <= int(other)
	def __ge__(self, other):
		return int(self) >= int(other)
	def __cmp__(self, other):
		return int(self) - int(other)
		
	def __len__(self):
		return len(self.this)
	def __getitem__(self,key):
		return EBN(self.this[key], fromHex=False)
	def __setitem__(self,key,value):
		self.this[key] = value
		
	# do I need to do the r___ corresponding functions? (__radd__ for example)
	def __add__(self, other):
		return int(self) + int(other)
	def __sub__(self, other):
		return int(self) - int(other)
	def __mul__(self, other):
		return int(self) * int(other)
	def __div__(self, other):
		return int(self) / int(other)
	def __mod__(self, other):
		return int(self) % int(other)
	def __pow__(self, other):
		return int(self) ** int(other)
		
	def __str__(self):
		return self.this
	def __repr__(self):
		return self.hex()
	def __int__(self):
		return int(self.this.encode('hex'),16)
		
	def __hash__(self):
		return int(self.hex(), 16)
	
	def hex(self):
		return self.this.encode('hex')
	def to_JSON(self):
		return "\""+self.hex()+"\""
	def concat(self, other):
		return self.this + other.this
	
	
# HELPER FUNCTIONS


import hashlib
def sha256(message):
	# require EBN input at this stage
	return EBN(hashlib.sha256(str(message)).digest(), fromHex=False)





# HIGH LEVEL OBJECTS



class Transaction:
	def __init__(self, receiver, value, fee, data, sender):
		self.receiver = receiver
		self.sender = sender
		self.value = value
		self.fee = fee
		self.data = data
		self.datan = len(data)

class Block:
	def __init__(self, number, difficulty, parenthash, basefee, timestamp):
		self.number = number
		self.difficulty = difficulty
		self.parenthash = parenthash
		self.basefee = basefee
		self.timestamp = timestamp
		self.eth = None
		
	def setNetwork(self, eth):
		self.eth = eth
		
	def contract_storage(self, D):
		# D = name of contract (hash)
		return self.eth.contract_storage(D)
		
	def account_balance(self, a):
		return self.eth.account_balance(a)
		
class Ethereum:
	def __init__(self):
		self.contracts = {}
		self.accounts = {}
		self.blocks = []
		self.latestBlock = None
		
	def processTx(self, tx):
		if self.accounts[tx.sender] < (tx.value + tx.fee):
			raise Exception("Insufficient funds in acct %s" % tx.sender)
		if tx.receiver not in self.accounts:
			self.accounts[tx.receiver] = 0.0
		self.accounts[tx.receiver] += tx.value
		if tx.receiver in self.contracts:
			self.contracts[tx.receiver].run(tx, self.latestBlock)
		
	def addContract(self, contract):
		self.contracts[contract.name] = contract
		self.accounts[contract.name] = 0.0
		
	def addBlock(self, block):
		'''Presume block is correct, add to chain'''
		self.blocks.append(block)
		self.latestBlock = blocks[-1]
		for tx in self.latestBlock.transactions:
			self.processTx(tx)
	
	def contract_storage(self, D):
		# D : name of contract (hash)
		return self.contracts[D].storage

class ContractStorage:
	def __init__(self):
		# storage is technically not a dictionary but an array
		# A dictionary is used here for simplicity
		self._storage = {}
	def __getitem__(self,key):
		#if type(key) is not int:
		#	key = int(key)
		if key in self._storage:
			return self._storage[key]
		'bloop'
		return 0
	def __setitem__(self, key, val):
		#if type(key) is not int:
		#	key = int(key)
		self._storage[key] = val
		
class Contract:
	def __init__(self, name):
		self.name = name
		self.storage = ContractStorage()
		self.address = name
		
	def stop(self):
		raise Exception("Contract stopped")
		
	def run(self, tx, latestBlock):
		'''This should be overwritten when the class is inherited'''
		raise Exception("Contract not initialized correctly.")




