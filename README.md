# RSA-Signatures :key:

Python script which computes RSA digital signatures and verifies them.

### Sign mode :pencil:
- Generate two random primes using Miller-Rabin test, 'p' and 'q', aswell as a modulus (p * q).
- Use Euler's totient for calculating a totient.
- Use Extended Euclidean algorithm to generate a private key "e", given the totient and a public key (65,537).
- Generate a hash from the given message using 32-bit ELFhash.
- Perform modular exponentiation (hash^e % modulus) to generate a signed digital signature, which may be verified using the same message. 

### Verify mode :heavy_check_mark:
- Program reads a given modulus, message and signature from STDIN.
- Prints "Message verified!" if signature matches the hash computed from the given modulus
- Prints "Message is forged!" if signature does not computed hash.
