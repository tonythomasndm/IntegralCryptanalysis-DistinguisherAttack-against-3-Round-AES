# Toy Cipher Implementation with Encryption and Decryption

# S-Box for Substitution Step (4-bit input -> 4-bit output)
S_BOX = [0x6, 0x4, 0xC, 0x5, 0x0, 0x7, 0x2, 0xE, 0x1, 0xF, 0x3, 0xD, 0x8, 0xA, 0x9, 0xB]
# Inverse S-Box for Decryption (4-bit input -> 4-bit output)
INV_S_BOX = [S_BOX.index(i) for i in range(16)]  # Reverse of S_BOX
# Permutation Box (Bit Shuffling)
P = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
# Inverse Permutation Box for Decryptionn
INV_P = [P.index(i) for i in range(16)]  # Reverse of P

def substitute(nibble):
    """Apply S-Box substitution to a 4-bit nibble."""
    return S_BOX[nibble]

def inverse_substitute(nibble):
    """Apply inverse S-Box substitution to a 4-bit nibble."""
    return INV_S_BOX[nibble]

def permute(bits):
    """Apply bitwise permutation according to P-box."""
    # Creating a list to store the permuted bits and return it
    permuted = [0] * 16
    for i in range(16):
        # Permute the 16 bits according to the P-box
        permuted[P[i]] = bits[i]
    return permuted

def inverse_permute(bits):
    """Apply inverse bitwise permutation according to INV_P-box."""
    # Creating a list to store the inverse permuted bits and return it
    permuted = [0] * 16
    for i in range(16):
        # Permute the 16 bits according to the inverse P-box(Inverse Permutation Box)
        permuted[INV_P[i]] = bits[i]
    return permuted

def to_bits(val, size=16):
    """Convert an integer value to a list of bits i.e 0s and 1s. In this case, 16 bits."""
    return [(val >> i) & 1 for i in range(size - 1, -1, -1)]

def from_bits(bits):
    """Convert a list of 16 bits back to an integer value."""
    return sum(b << (15 - i) for i, b in enumerate(bits))

def encrypt(plaintext, round_keys):
    """Encrypt a 16-bit plaintext using the given round keys."""
    state = plaintext  # Initial state is the plaintext
    
    for i in range(4):  # Perform 4 rounds
        state ^= round_keys[i]  # XOR with round key
        
        # Convert integer state into 4 nibbles (4-bit values)
        state_nibbles = [(state >> (4 * j)) & 0xF for j in range(4)][::-1]
        # Apply S-Box substitution
        state_nibbles = [substitute(n) for n in state_nibbles]
        # Convert nibbles to bits representation
                # CORRECTED YOUR CODE HERE
        state_bits = to_bits(sum(n << (4 * (3-j)) for j, n in enumerate(state_nibbles)))
        # Apply permutation
        state_bits = permute(state_bits)
        
        # Convert 16 bits back to integer value
        state = from_bits(state_bits)
    
    # Final round (no permutation after S-Box)
    state ^= round_keys[4] # XOR with round key k4
    state_nibbles = [(state >> (4 * j)) & 0xF for j in range(4)][::-1] # Convert to nibbles
    state_nibbles = [substitute(n) for n in state_nibbles] # Apply S-Box substitution
    # Convert nibbles to integer representation
            # CORRECTED YOUR CODE HERE
    state = sum(n << (4 * (3-j)) for j, n in enumerate(state_nibbles))
    
    return state ^ round_keys[5]  # Final XOR with last round key


def decrypt(ciphertext, round_keys):
    """Decrypt a 16-bit ciphertext using the given round keys."""
    state = ciphertext ^ round_keys[5]  # Initial XOR with last round key
    
    # Reverse final round (Substitution step)
    # Convert to nibbles and reverse substitution
    state_nibbles = [(state >> (4 * j)) & 0xF for j in range(4)][::-1]
    state_nibbles = [inverse_substitute(n) for n in state_nibbles]

    # Convert nibbles to integer representation
    state = sum(n << (4 * (3-j)) for j, n in enumerate(state_nibbles))
    state ^= round_keys[4]  # Reverse the final round key XOR
    
    for i in range(3, -1, -1):  # Reverse 4 rounds
        state_bits = to_bits(state)  # Convert to bit representation
        state_bits = inverse_permute(state_bits)  # Reverse permutation
        state = from_bits(state_bits)  # Convert back to integer
        
        # Convert to nibbles and reverse substitution
        state_nibbles = [(state >> (4 * j)) & 0xF for j in range(4)][::-1]
        state_nibbles = [inverse_substitute(n) for n in state_nibbles]
        # Convert nibbles to integer representation
        state = sum(n << (4 * (3-j)) for j, n in enumerate(state_nibbles))
        
        state ^= round_keys[i]  # Reverse XOR with round key
    
    return state  # Decrypted plaintext

# THE SAME ROUND KEYS WILL BE USED FOR ENCRYPTION AND DECRYPTION IN KEY RECOVERY
round_keys = [0x1111, 0x2222, 0x3333, 0x4444, 0x5555, 0x6656]  # Example round keys 

if __name__ == "__main__":
    # Example usage
    plaintext = 0x1234  # Example 16-bit plaintext
    round_keys = [0x1111, 0x2222, 0x3333, 0x4444, 0x5555, 0x6666]  # Example round keys

    print(f"Plaintext: {plaintext:04X}")
    print("Round Keys:", round_keys)
    # Encrypt plaintext
    ciphertext = encrypt(plaintext, round_keys)
    print(f"Ciphertext: {ciphertext:04X}")

    # Decrypt back to plaintext
    decrypted_text = decrypt(ciphertext, round_keys)
    print(f"Decrypted Text: {decrypted_text:04X}")


"""

Output:
Plaintext: 1234
Round Keys: [4369, 8738, 13107, 17476, 21845, 26214]
Ciphertext: 6092
Decrypted Text: 1234

"""