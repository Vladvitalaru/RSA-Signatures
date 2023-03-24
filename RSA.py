#Vlad Vitalaru
#CS427 
#RSA Signatures

import sys
import random

# Sign mode which generates 2 primes, a modulus and totient. Creates a signed hash for verification
def sign(message):
    p, q = generate_primes()
    message = message.strip('"')
    # p = 0x9da5 !hardcoded primes for testing
    # q = 0xb28b
    
    # Calculate modulus and totient from generarted primes
    modulus = p * q 
    totient = (p - 1) * (q - 1)
    
    # totient = int("6df10268", base=16) !hardcoded totient for testing
    print(f'p = {p:x}, q = {q:x}, n = {modulus:x}, t = {totient:x}')
    print(f'received message: {message}')
    
    #Generate hash using elf hashing
    hash = elf_hash(message)
    print(f'message hash: {hash:x}')
    public = 65537
    
    #Generate private key using extended euclidian algorithm
    private = euclidian_key(public, totient)
    print(f'signing with the following private key: {private:x}')
    
    #Generate signed hash using modular exponentiation
    signed = power(hash, private, modulus) 
    print(f'signed hash: {signed:x}')
    uninverted_hash = power(signed, public, modulus)
    print(f'uninverted message to ensure integrity: {uninverted_hash:x}')
    print(f'complete output for verification:\n{modulus:x} "{message}" {signed:x}\n')

# Use extended euclidian algorithm to obtain private key
# https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
def euclidian_key(public, totient):
    t = 0
    newt = 1
    r = totient
    newr = public
    
    while newr != 0:
        quotient = r // newr
        t, newt = newt, t - quotient * newt
        r, newr = newr, r - quotient * newr
        
    if r > 1:
        return "A is not invertible"
    if t < 0:
        t = t + totient
            
    return t
    

# Generate 2 random prime numbers, use the Miller Rabin test
def generate_primes():
    primes = []
    while len(primes) < 2: 
        number = random.randrange(32768, 65535)
        result = miller_rabin(number)
        if result is True:
            primes.append(number)
    return primes[0], primes[1]

        
# Miller Rabin test for determining prime numbers
# https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
def miller_rabin(number):
    round = 0
    
    while round < 20: #Do 20 rounds of the Miller Rabin Test
        if number % 2 == 0 or number<=1: 
            return False
        
        d = number-1
        while(d%2==0): d/=2
        
        a = random.randrange(3, number-2)
        x = power(a, d, number)
        
        if (x == 1 or x == number - 1):
            return True

        while (d!= number - 1):
            x = power(a, d, number)
            d*= 2
            
            if (x == 1): return False
            if (x == number - 1): return True
            
        round+=1
    
# Modular exponentiation, returning (a^b % p)
def power(a, b, p):
    result = 1
    
    #Update a if >= p
    a = a % p
    while (b > 0):
        #If b is odd, multiply a with result
        if (int(b) & 1):    
            result = (result * a) % p
        b = int(b)>>1
        a = (a * a) % p
    return result
    
# Elf Hashing algorithm used to hash message
# https://en.wikipedia.org/wiki/PJW_hash_function
def elf_hash(message):
    h, high = 0, 0
    
    #Convert string into bytes and iterate over them
    for i in message.encode():
        #Shift over by 4 bits
        h = (h << 4) + i
        high = h & 0xF0000000
        
        if high != 0:
            h = h ^ high >> 24
        h = h & (~high)
        
    return h

# Verify given modulus, message and signature by comparing the uninverted hash with the message hash
def verify(modulus, message, signature):
    #Convert strings to int
    modulus = int(modulus,base=16)
    signature = int(signature, base=16)
    
    #Compute hash from message
    hash = elf_hash(message)
    
    #Compute hash from given signature, modulus and public key
    uninverted_hash = power(signature, 65537, modulus)
    
    #Compare hashes for verification
    if hash == uninverted_hash:
        print("message verified!\n")
        return
    else:
        print("!!! message forged !!!\n")
        return

def main():
    print()
    for line in sys.stdin:
        line = line.strip().split(" ", 1)
        mode = line[0]
        
        if mode == "sign": #If we have to sign
            try:
                message = line[1]
            except:
                print("Incorrect Input!\n") 
                continue
                        
            sign(message)
            
        elif mode == "verify": #If we have to verify
            try:
                line[1] = line[1].strip().split('"')
                modulus = line[1][0].strip(" ")
                message = line[1][1]
                signature = line[1][2].strip(" ")
            except:
                print("Incorrect Input!\n")
                continue
            
            verify(modulus, message, signature)
    
        else:
            print("Incorrect Input!\n")

if __name__ == "__main__":
    main()