from datetime import datetime
import hashlib


class Block:
    def __init__(self, data, prevHash='0'*64):
        self.__date = datetime.now()
        self.__data = data
        self.__nonce = 0
        self.__prev_hash = prevHash
        self.__hash = self.createHash()

    def createHash(self):
        date = str(self.__date).encode()
        data = str(self.__data).encode()
        nonce = str(self.__nonce).encode()
        if self.__prev_hash:
            prevHash = self.__prev_hash.encode()
        else:
            prevHash = str(None).encode()
        return hashlib.sha256(date + data + prevHash + nonce).hexdigest()

    def getDate(self):
        return self.__date

    def getData(self):
        return self.__data

    def getPrevHash(self):
        return self.__prev_hash

    def setPrevHash(self, _hash):
        self.__prev_hash = _hash

    def getHash(self):
        return self.__hash

    def getNonce(self):
        return self.__nonce

    def mineBlock(self, difficulty):
        while self.__hash[0:difficulty] != "0" * difficulty:
            self.__nonce += 1
            self.__hash = self.createHash()

    def __str__(self):
        if self.__prev_hash == '0'*64:
            return f"Block: {self.getHash()}; " \
                   f"Created: {self.getDate()}; " \
                   f"Nonce: {self.getNonce()}; " \
                   f"Data: {len(self.getData())}; " \
                   f"PrevBlock: {str(None)}"
        else:
            return f"Block: {self.getHash()}; " \
                   f"Created: {self.getDate()}; " \
                   f"Nonce: {self.getNonce()}; " \
                   f"Data: {len(self.getData())}; " \
                   f"PrevBlock: {self.getPrevHash()}"


class Blockchain:
    def __init__(self, difficulty):
        self.__chain = [Block([Transaction('Origin', 0)])]
        self.__DIFFICULTY = difficulty
        if self.__chain[0].getPrevHash() == '0'*64:
            self.__chain[0].mineBlock(self.__DIFFICULTY)

    def addBlock(self, new_block):
        new_block.setPrevHash(self.getLastBlock().getHash())
        new_block.mineBlock(self.__DIFFICULTY)
        self.__chain.append(new_block)

    def getLastBlock(self):
        return self.__chain[-1]

    def showChain(self):
        for block in self.__chain:
            print(block)
            for transaction in block.getData():
                print(f"Data: {transaction}")

    def integrityCheck(self):
        for index, block in enumerate(self.__chain):
            current_block = self.__chain[index]
            previous_block = self.__chain[index-1]
            if current_block.getPrevHash() != '0'*64:
                if current_block.getPrevHash() != previous_block.getHash():
                    return False, index
            if current_block.getHash() != current_block.createHash():
                return False, index
        return True, None

    def getBalance(self, user):
        balance = 0
        for block in self.__chain:
            for transaction in block.getData():
                if transaction.getUser() == user:
                    balance += transaction.getValue()
        return balance


class Transaction:
    def __init__(self, user, value):
        self.__date = datetime.now()
        self.__user = user
        self.__value = value

    def getUser(self):
        return self.__user

    def getValue(self):
        return self.__value

    def __str__(self):
        transaction = f"date: {self.__date}//user: {self.__user}//value: {self.__value}"
        return transaction


class User:
    def __init__(self, name):
        self.__created = str(datetime.now())
        self.__name = str(name)
        self.__userID = self.createUserID()

    def createUserID(self):
        return hashlib.sha256((self.__created+self.__name).encode()).hexdigest()

    def showUser(self):
        print(f"Name: {self.__name}")
        print(f"Created: {self.__created}")
        print(f"UserID: {self.__userID}")
        print('*' * 72)

    def getUserID(self):
        return self.__userID

    def __str__(self):
        return self.__userID


if __name__ == '__main__':
    users = [User('John'), User('Lisa')]
    for i in users:
        i.showUser()

    CarlosCoin = Blockchain(difficulty=4)
    CarlosCoin.addBlock(Block([Transaction(users[0].getUserID(), 1200), Transaction(users[1].getUserID(), -1200)]))
    CarlosCoin.addBlock(Block([Transaction(users[0].getUserID(), 40), Transaction(users[1].getUserID(), -40)]))
    CarlosCoin.addBlock(Block([Transaction(users[0].getUserID(), -140), Transaction(users[1].getUserID(), 140)]))
    CarlosCoin.showChain()
    valid, error_index = CarlosCoin.integrityCheck()
    print(valid, error_index)
    print(CarlosCoin.getBalance(users[0].getUserID()))
