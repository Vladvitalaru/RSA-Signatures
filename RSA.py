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


def main():
    print()
    for line in sys.stdin:
        line = line.strip().split(" ", 1)
        print(line)        
        mode = line[0]
        if mode == "sign": #If we have to sign
            print("sign mode")
            message = line[1]
            print(message)            
            
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