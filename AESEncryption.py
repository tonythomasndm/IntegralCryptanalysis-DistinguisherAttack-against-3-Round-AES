import numpy as np

# AES S-Box (used in subWord and subBytes function) for faster lookup
sBox= np.array([
    [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76],
    [0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0],
    [0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15],
    [0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75],
    [0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84],
    [0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF],
    [0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8],
    [0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2],
    [0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73],
    [0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB],
    [0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79],
    [0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08],
    [0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A],
    [0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E],
    [0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF],
    [0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]
], dtype=np.uint8).flatten()

mixColumnsMatrix = np.array([
    [2, 3, 1, 1],
    [1, 2, 3, 1],
    [1, 1, 2, 3],
    [3, 1, 1, 2]
], dtype=np.uint8)


def subWord(word):
    """
    Apply the AES S-Box substitution to a word.
    A list of 4 bytes -> A list of SBox word 4 bytes.
    """
    # S-Box is now a flattened list of 256 elements for easier indexing and faster lookup
    return [sBox[(b >> 4) * 16 + (b & 0x0F)] for b in word]

def rotWord(word):
    """
    Perform a cyclic permutation (left rotation) on a word.
    A list of 4 bytes -> A list of rotated word.
    """
    return word[1:] + word[:1]  # This moves the first byte to the end

def keyExpansion(keyMatrix, rounds):
    """
    This function performs the AES Key Expansion to generate round keys.

    Args:
        keyMatrix (np.ndarray): A 4x4 numpy array representing the cipher key.
        rounds (int): The number of AES rounds (10 for AES-128).

    Returns:
        list: A list of round keys, where each round key is a 4x4 numpy array.
    """
    Nk = 4  # Number of 32-bit words in the key
    Nb = 4  # Number of 32-bit words in a block
    Nr = rounds  # Number of rounds

    # Round constant array (Rcon)
    rcon = [
        [0x01, 0x00, 0x00, 0x00],
        [0x02, 0x00, 0x00, 0x00],
        [0x04, 0x00, 0x00, 0x00],
        [0x08, 0x00, 0x00, 0x00],
        [0x10, 0x00, 0x00, 0x00],
        [0x20, 0x00, 0x00, 0x00],
        [0x40, 0x00, 0x00, 0x00],
        [0x80, 0x00, 0x00, 0x00],
        [0x1B, 0x00, 0x00, 0x00],
        [0x36, 0x00, 0x00, 0x00]
    ]

    # Initialize the array to hold words
    words = []
    for i in range(Nk):
        words.append(list(keyMatrix[:, i]))  # Extract the ith column from the key matrix

    for i in range(Nk, Nb * (Nr + 1)):  # Total words = Nb * (Nr + 1)
        temp = words[i - 1]  # Previous word
        if i % Nk == 0:  # Perform special operations every Nk words
            temp = subWord(rotWord(temp))  # Substitute and rotate the word
            temp = [t ^ r for t, r in zip(temp, rcon[i // Nk - 1])]  # XOR with Rcon
        words.append([t ^ p for t, p in zip(words[i - Nk], temp)])

    roundKeys = []
    for i in range(0, len(words), 4):
        roundKeys.append(np.array(words[i:i + 4]).T)

    return roundKeys

def subBytes(state: np.ndarray) -> np.ndarray:
    """
    This function applies the SubBytes transformation using the S-Box.

    Args:
        state (np.ndarray): 4x4 state matrix.

    Returns:
        np.ndarray: Transformed 4x4 state matrix.
    """
    # Use `np.vectorize` to apply a function to every element in the 4x4 state matrix.
    # The lambda function `lambda x: sBox[x]` takes each byte `x` in the state matrix
    # and replaces it with its corresponding value from the S-Box (`sBox[x]`).

    return np.vectorize(lambda x: sBox[x])(state)


def shiftRows(state: np.ndarray) -> np.ndarray:
    """
    This function perform the ShiftRows transformation on the state.
    
    Args:
        state (numpy.ndarray): The state matrix (4x4) to be transformed.
    
    Returns:
        numpy.ndarray: The transformed state matrix.
    """
    state[1] = np.roll(state[1], -1)  # Shift row 1 left by 1
    state[2] = np.roll(state[2], -2)  # Shift row 2 left by 2
    state[3] = np.roll(state[3], -3)  # Shift row 3 left by 3
    return state

def gmul(a: int, b: int) -> int:
    """
   This function performs Galois field multiplication of two bytes (0-255) in AES (GF(2^8)).

    Args:
        a (int): First byte (0-255).
        b (int): Second byte (0-255).

    Returns:
        int: Result of multiplication (0-255).
    """
    # Initialize the result of the multiplication
    p=0 

    # Loop through each bit of the second byte `b` (since it's 8 bits long)
    for i in range(8):
        # If the least significant bit of `b` is set, XOR `a` into the result
        if b & 1:
            p ^= a  # XOR the value of `a` into `p`
        
        # Check if the highest bit of `a` is set (for reduction)
        highBitSet = a & 0x80  # 0x80 = 10000000 in binary
        
        # Shift `a` one bit to the left (equivalent to multiplication by 2 in GF(2^8))
        a = (a << 1) & 0xFF  # Mask with 0xFF to ensure it stays within 8 bits
        
        # If the highest bit was set, reduce `a` using the AES irreducible polynomial
        if highBitSet:
            a ^= 0x1B  # XOR with 0x1B (the irreducible polynomial x^8 + x^4 + x^3 + x + 1)
        
        # Shift `b` one bit to the right (process the next bit)
        b >>= 1

    # Return the result of the Galois field multiplication
    return p

def mixColumns(state: np.ndarray) -> np.ndarray:
    """
    Perform the MixColumns transformation for AES encryption. This function helps in more diffusion of the data. therefore it is used in all rounds except the last round.
    And makes it more secure

    Args:
        state (np.ndarray): 4x4 state matrix.

    Returns:
        np.ndarray: Transformed 4x4 state matrix.
    """
    # This involves initialize the result matrix with the same shape as the input state matrix
    result = np.zeros_like(state)

    # Iterate over each column of the state matrix (total 4 columns)
    for c in range(4):
        """
        The mixColumnsMatrix is multiplied with each column of the state matrix using gmul function which performs Galois field multiplication.
        The result is stored in the result matrix.
        Row `i` of the output is calculated as the dot product of the `i`th row of the MixColumns matrix with the `c`th column of the state matrix.
        """
        result[:, c] = [
           gmul(mixColumnsMatrix[i, 0], state[0, c]) ^  # Multiply and XOR for first row 
            gmul(mixColumnsMatrix[i, 1], state[1, c]) ^  # Multiply and XOR for second row 
            gmul(mixColumnsMatrix[i, 2], state[2, c]) ^  # Multiply and XOR for third row 
            gmul(mixColumnsMatrix[i, 3], state[3, c])    # Multiply and XOR for fourth row
            for i in range(4)  # Repeat for all rows in the state matrix
        ]

    return result

def addRoundKey(state: np.ndarray, roundKey: np.ndarray) -> np.ndarray:
    """
    This function performs AddRoundKey transformation which involves xoring the state matrix with the round key matrix.

    Args:
        state (np.ndarray): 4x4 state matrix.
        roundKey (np.ndarray): 4x4 round key matrix.

    Returns:
        np.ndarray: Transformed 4x4 state matrix.
    """

    # Xoring the state matrix with the round key matrix each element by element in 4x4 matrix for both in numpy format
    return state ^ roundKey


def aesEncrypt(plainText: str, key: str, rounds: int) -> str:
    """
    Encrypt the plaintext using AES.
    
    Args:
        plainText (str): Hexadecimal string of the plaintext (32 hex digits).
        key (str): Hexadecimal string of the key (32 hex digits).
        rounds (int): Number of rounds (e.g., 10 for AES-128).
        
    Returns:
        str: Hexadecimal string of the ciphertext (32 hex digits).
    """
    state = np.array([int(plainText[i:i+2], 16) for i in range(0, len(plainText), 2)], dtype=np.uint8)
    state = state.reshape(4, 4).T
    keyMatrix = np.array([int(key[i:i+2], 16) for i in range(0, len(key), 2)], dtype=np.uint8)
    keyMatrix = keyMatrix.reshape(4, 4).T
    roundKeys = keyExpansion(keyMatrix, rounds)
    state = addRoundKey(state, roundKeys[0])
    for round in range(1, rounds):
        state = subBytes(state)
        state = shiftRows(state)
        state = mixColumns(state)
        state = addRoundKey(state, roundKeys[round])
    state = subBytes(state)
    state = shiftRows(state)
    state = addRoundKey(state, roundKeys[rounds])
    return ''.join(f'{byte:02x}' for byte in state.T.flatten())

def aesEncryptLastRoundProper(plainText: str, key: str, rounds: int) -> str:
    """
    Encrypts the plaintext using AES. Here the Last round has mixcolumns.
    
    Args:
        plainText (str): Hexadecimal string of the plaintext (32 hex digits).
        key (str): Hexadecimal string of the key (32 hex digits).
        rounds (int): Number of rounds (e.g., 10 for AES-128).
        
    Returns:
        str: Hexadecimal string of the ciphertext (32 hex digits).
    """
    state = np.array([int(plainText[i:i+2], 16) for i in range(0, len(plainText), 2)], dtype=np.uint8)
    state = state.reshape(4, 4).T
    keyMatrix = np.array([int(key[i:i+2], 16) for i in range(0, len(key), 2)], dtype=np.uint8)
    keyMatrix = keyMatrix.reshape(4, 4).T
    roundKeys = keyExpansion(keyMatrix, rounds)
    state = addRoundKey(state, roundKeys[0])
    for round in range(0, rounds):
        state = subBytes(state)
        state = shiftRows(state)
        state = mixColumns(state)
        state = addRoundKey(state, roundKeys[round])
    return ''.join(f'{byte:02x}' for byte in state.T.flatten())

# --- New Helper Fn: aesEncryptOracle ---
def aesEncryptOracle(plaintextInt: int, keyInt: int, rounds: int) -> int:
    """
    Encrypts a 128-bit plaintext (provided as an integer) using AES encryption.
    
    This helper function performs the following steps:
      1. Converts the 128-bit integer plaintext and key into their 32-digit hexadecimal
         string representations. This conversion ensures that the AES encryption function,
         which expects a hexadecimal string, receives properly formatted input.
      2. Calls the AES encryption function (aesEncrypt) using the hexadecimal strings and
         the specified number of rounds. The aesEncrypt function is assumed to return a
         ciphertext as a 32-digit hexadecimal string.
      3. Converts the resulting ciphertext (hex string) back into a 128-bit integer, which
         is then returned.
    
    Args:
        plaintextInt (int): The 128-bit plaintext represented as an integer.
        keyInt (int): The 128-bit encryption key represented as an integer.
        rounds (int): The number of AES rounds to perform.
        
    Returns:
        int: The resulting 128-bit ciphertext as an integer.
    """
    # Convert the plaintext integer to a 32-digit hexadecimal string.
    plaintextHex = f'{plaintextInt:032x}'
    
    # Convert the key integer to a 32-digit hexadecimal string.
    keyHex = f'{keyInt:032x}'
    
    # Call the AES encryption function (aesEncrypt) with the hexadecimal plaintext,
    # key, and the number of rounds. The function is expected to return a hexadecimal
    # string representing the ciphertext.
    cipherHex = aesEncryptLastRoundProper(plaintextHex, keyHex, rounds)
    
    # Convert the ciphertext hexadecimal string back to a 128-bit integer and return it.
    return int(cipherHex, 16)






if __name__ == "__main__":
    intro_message = """
Welcome to AES-128 Encryption Tool

This tool will encrypt your message using the AES-128 encryption algorithm.
Please provide:
1) Plain Text - 16 bytes as a 32-character hexadecimal string.
2) Encryption Key - 16 bytes as a 32-character hexadecimal string.
3) Number of rounds (default is 10)
"""
    print(intro_message)
    plainText = input("Enter the plain text (32 hex digits): ").strip()
    key = input("Enter the cipher key (32 hex digits): ").strip()
    rounds = int(input("Enter the number of rounds: ").strip())
    cipher_text = aesEncrypt(plainText, key, rounds)
    print(f"\nEncrypted Cipher Text: {cipher_text}")
    print("\nThank you for using the AES-128 Encryption Tool.")
