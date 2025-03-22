import random
from AESEncryption import aesEncryptOracle
from RandomPermutation import randomPermutationOracle

def generateSetOfPlaintextsInt(basePlaintext: int, byteIndex: int = 0) -> list:
    """
    Generates 256 plaintexts by varying one specific byte in the base plaintext.
    
    This function takes a 128-bit integer as the base plaintext and then varies
    one of its bytes (specified by byteIndex) through all 256 possible values.
    
    Args:
        basePlaintext (int): The base 128-bit plaintext as an integer.
        byteIndex (int): The byte position to vary (0 for most-significant, 15 for least-significant).
        
    Returns:
        list: A list of 256 modified 128-bit plaintexts (each as an integer).
    """
    # Initialize an empty list to hold all generated plaintexts.
    plaintexts = []
    
    # Calculate the bit shift needed to target the specified byte.
    # For example, if byteIndex is 0, then we are targeting the most-significant byte.
    shift = (15 - byteIndex) * 8
    
    # Create a bitmask that isolates the target byte (0xFF shifted to the correct position).
    mask = 0xFF << shift
    
    # Loop through all 256 possible values (0 to 255) for the target byte.
    for i in range(256):
        # Clear the target byte in the basePlaintext using the mask,
        # then set it to the new value. The expression (basePlaintext & ~mask)
        # clears the target byte, and (i << shift) places the new byte value.
        newPlaintext = (basePlaintext & ~mask) | (i << shift)
        
        # Append the new modified plaintext to our list.
        plaintexts.append(newPlaintext)
    
    # Return the complete list of 256 modified plaintexts.
    return plaintexts

def distinguisherAttack(ciphertexts: list) -> int:
    """
    Computes the XOR of all ciphertexts.
    
    According to the integral cryptanalysis property for 3-round AES, when you encrypt 256
    plaintexts that differ in only one byte, the XOR sum of all ciphertexts should be 0.
    For a random permutation, however, the XOR sum is almost never 0.
    
    Args:
        ciphertexts (list): A list of 128-bit ciphertexts (as integers).
        
    Returns:
        int: The XOR sum of all the ciphertexts.
    """
    # Initialize the XOR sum variable to 0.
    xorSum = 0
    
    # Iterate over each ciphertext in the list and update the XOR sum.
    for ct in ciphertexts:
        xorSum ^= ct
    
    # Return the final XOR result.
    return xorSum

if __name__ == "__main__":
    # -------------------------------------------------------------------
    # Setup Section: Define fixed values for the attack demonstration.
    # -------------------------------------------------------------------
    
    # Define a fixed 128-bit base plaintext as a hexadecimal integer.
    basePlaintext = 0x0123456789abcdef0123456789abcdef
    
    # Define a fixed 128-bit key as a hexadecimal integer.
    key = 0x00112233445566778899aabbccddeeff
    
    # Set the number of AES rounds to 3 for the integral cryptanalysis demonstration.
    rounds = 3  
    
    # -------------------------------------------------------------------
    # Part 1: Distinguishing using the AES 3-round Encryption Oracle.
    # -------------------------------------------------------------------
    
    # Generate 256 plaintexts by varying the most-significant byte (byteIndex = 0).
    plaintexts = generateSetOfPlaintextsInt(basePlaintext, byteIndex=0)
    
    # Initialize an empty list to store ciphertexts returned by the AES encryption oracle.
    aesCiphertexts = []
    
    # For each plaintext, query the AES encryption oracle.
    # The oracle function 'aes_encrypt_oracle' accepts a 128-bit plaintext, key, and rounds,
    # and returns the corresponding ciphertext as a 128-bit integer.
    for pt in plaintexts:
        ct = aesEncryptOracle(pt, key, rounds)
        aesCiphertexts.append(ct)
    
    # Compute the XOR sum of all ciphertexts using the distinguisher attack function.
    xorResultAes = distinguisherAttack(aesCiphertexts)
    
    # Display the results for the AES oracle attack.
    print("AES Oracle (3-round AES) Attack:")
    print("XOR sum of ciphertexts: 0x{:032x}".format(xorResultAes))
    if xorResultAes == 0:
        print("Result: Likely 3-round AES encryption (integral property holds).\n")
    else:
        print("Result: Likely a random permutation (unexpected for AES oracle).\n")
    
    # -------------------------------------------------------------------
    # Part 2: Distinguishing using the Random Permutation Oracle.
    # -------------------------------------------------------------------
    
    # Initialize an empty list to store ciphertexts returned by the random permutation oracle.
    randCiphertexts = []
    
    # For each plaintext, query the random permutation oracle.
    # This oracle assigns each plaintext a unique random 128-bit ciphertext.
    for pt in plaintexts:
        ct = randomPermutationOracle(pt)
        randCiphertexts.append(ct)
    
    # Compute the XOR sum of all ciphertexts from the random permutation oracle.
    xorResultRand = distinguisherAttack(randCiphertexts)
    
    # Display the results for the random permutation oracle attack.
    print("Random Permutation Oracle Attack:")
    print("XOR sum of ciphertexts: 0x{:032x}".format(xorResultRand))
    if xorResultRand == 0:
        print("Result: Likely 3-round AES encryption (unexpected for random permutation).")
    else:
        print("Result: Likely a random permutation (integral property does not hold).")
