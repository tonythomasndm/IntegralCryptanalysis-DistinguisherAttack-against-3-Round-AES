import random

def randomPermutationOracle(plaintext: int) -> int:
    """
    For each plaintext (a 128-bit integer), returns a unique random 128-bit ciphertext.
    
    This function simulates a random permutation on 128-bit values. When a plaintext is
    queried for the first time, a new random 128-bit ciphertext is generated and returned.
    
    Args:
        plaintext (int): A 128-bit integer representing the plaintext.
        
    Returns:
        int: A unique random 128-bit integer representing the ciphertext.
    """
    
    ct = random.getrandbits(128)
    return ct

if __name__=="__main__":
    plainText = input("Enter the plain text (32 hex digits): ").strip()
    plainText = int(plainText, 16)
    cipherText = randomPermutationOracle(plainText)
    print("The cipher text is: ", hex(cipherText))
    