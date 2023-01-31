import time
import string
import random
import hashlib
import ecdsa


class Blockchain:
    def __init__(self, Index, Time, Hash, PrevHash, Transaction, TransactionHash, FromAddress, ToAddress, quant, balance, Difficulty, nonce):
        self.Index = Index
        self.Time = Time
        self.Hash = Hash
        self.PrevHash = PrevHash
        self.Transaction = Transaction
        self.TransactionHash = TransactionHash
        self.FromAddress = FromAddress
        self.ToAddress = ToAddress
        self.quant = quant
        self.balance = 0
        self.Difficulty = Difficulty
        self.nonce = 0
       
        self.chain = []
        self.TransactionsList = []
        
 
    def GetIndex(self):
        self.Index = len(self.chain)
        self.Index = str(self.Index)
        return self.Index
 
    def GetData(self):
        #self.balance = 0
 
        while True:
            ans = str(input("1 to send, 2 to recieve, 3 to break: "))
 
            if ans == "1":
                self.FromAddress = input("Enter address to send from \"myaddress\" for your address: ")
                self.ToAddress = input("Enter who you are sending too: ")
                self.quant = float(input("Enter quantity of transaction: "))
                break
           
            elif ans == "2":
                self.FromAddress = input("Enter address to accept from: ")
                self.ToAddress = input("Enter \"myaddress\" to accept: ")
                self.quant = float(input("Enter quantity of transaction: "))
                break
 
            elif ans == "3":
                exit()
 
        self.Transaction = "-".join(self.FromAddress) + "-" + (self.ToAddress) + "-" + str((self.quant))
        self.TransactionsList.append(self.Transaction)
        if self.FromAddress == "myaddress":
            self.balance = float(self.balance - self.quant)
        elif self.FromAddress != "myaddress":
            self.balance = float(self.balance + self.quant)
        return self.TransactionsList
         
    
    def signTransaction(self):
            
        self.sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.vk = self.sk.get_verifying_key()
        
        hashtx = hashlib.sha256(self.Transaction.encode()).hexdigest()
        bytes_hashtx = bytes(hashtx, 'UTF-8')
        
        self.sig = self.sk.sign(bytes_hashtx)
        #self.Ver = self.vk.verify(self.sig, bytes_hashtx)
        

        return bytes_hashtx
    

    def GetPrevHash(self):
        self.PrevHash = self.chain[-1].Hash
        return self.PrevHash

    def GetTime(self):
        self.Time = time.time()
        self.Time = str(self.Time)
        return self.Time

    def GetHash(self):
        block_string = "-".join(self.GetIndex()) + "-" + (self.GetTime())  + "-" + (self.GetPrevHash())  + "-" + (self.Transaction) + "-"
        Blockhash = hashlib.sha256(block_string.encode()).hexdigest()
        return Blockhash
       
    def ProofOfWork(self):
        self.Difficulty = 2
 
        self.Hash = self.GetHash()
 
        while not self.Hash.startswith("0" * self.Difficulty):
            self.nonce+=1
            self.Hash = self.GetHash()
 
        return self.Hash
 
    def MakeGenesisBlock(self):
       
        letters = string.ascii_letters
        self.PrevHash = ( ''.join(random.choice(letters) for i in range(32)))
   
        GenesisBlockData = ( ''.join(random.choice(letters) for i in range(32)))
       
        GenesisDiff = 1
        GenesisNonce = 0
       
        GenesisBlockHash = hashlib.sha256(GenesisBlockData.encode()).hexdigest()
        #                   Blockchain(Index, Time, Hash, PrevHash, Transaction, TransactionHash, FromAddress, ToAddress, quant, balance, Difficulty, nonce)
        self.GenesisBlock = Blockchain(self.GetIndex(), self.GetTime(), GenesisBlockHash, self.PrevHash, GenesisBlockData, "", "", "", "", "", GenesisDiff, GenesisNonce)
       
        self.chain.append(self.GenesisBlock)
 
        return

    def MineBlocks(self):
        NewBlock = Blockchain(self.GetIndex(), self.GetTime(), self.ProofOfWork(), self.GetPrevHash, self.GetData(), "", "", "", self.balance, "", "", "")
        
        IV = self.signTransaction()
        
        self.Ver = self.vk.verify(self.sig, self.signTransaction())
            
        if IV is False:
            raise Exception("BAD SIGNATURE")
        
        elif IV is True:
            self.chain.append(NewBlock)
     
            self.TransactionsList = []
            
        print(IV)
        print(self.Ver)

        return

    def MiningRewards(self):
      if self.FromAddress == "myaddress":
          self.balance = float(self.balance + 10)
      elif self.ToAddress == "myaddress":
          self.balance = float(self.balance + 5)
      return
            
 
    def DisplayChain(self):
      print(len(self.chain))
     
      print("Index is: ",self.Index)
      print("Hash is: ",self.Hash)
      print("Transaction is: ",self.Transaction)
      print("Balance is: ", self.balance)
      print("Previous hash is: ",self.PrevHash)
      print("Timestamp is: ",self.Time)

if __name__ == "__main__":
    
    b = Blockchain("", "", "", "", "", "", "", "", 0, "","", "")
    
    b.MakeGenesisBlock()
    
    while True:
        ans = input("1 for do 2 for don't: ")
        if ans == "1":
            b.MineBlocks()
            b.MiningRewards()
            b.DisplayChain()
        elif ans == "2":
            print("Block not mined, try again.")
            
        elif ans == "3":
            break
    print("")