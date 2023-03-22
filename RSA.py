#Vlad Vitalaru
#CS427 
#RSA Signatures


'''
The two modes:
sign "message text"
verify <modulus_n> "message text" <message_signature>
'''

# 65,537 (public key)


import sys
import random

# Sign mode
def sign(message):
    p, q = generate_primes()
    
    print(message)
    print(p)
    print(q)


def verify():
    pass

# Generate 2 random prime numbers, call the Miller Rabin test for assistance
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
    
    while round < 5: #Do 5 rounds of the Miller Rabin Test
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
    
    a = a % p
    while (b > 0):
        if (int(b) & 1):
            result = (result * a) % p
        b = int(b)>>1
        a = (a * a) % p
    return result
    
def elf_hash():
    pass

def main():
    print()
    for line in sys.stdin:
        line = line.strip().split(" ", 1)
        print(line)        
        mode = line[0]
        if mode == "sign": #If we have to sign
            print("sign mode")
            message = line[1]
            sign(message)            
            
        elif mode == "verify": #If we have to verify
            print("verify mode")
            line[1] = line[1].strip().split('"')
            modulus = line[1][0]
            message = line[1][1]
            signature = line[1][2]
            print(f'modulus: {modulus}')
            print(f'message: {message}')
            print(f'signature: {signature}')
    
        else:
            print("Incorrect Input!")


if __name__ == "__main__":
    main()