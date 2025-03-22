# Implementation of the Distinguishing Attack with Integral Cryptanalysis against 3-Round AES

This project demonstrates how to distinguish between a 3-round AES encryption oracle and a random permutation oracle using integral cryptanalysis. The attack exploits a property of 3-round AES where the XOR sum of ciphertexts from 256 specially crafted plaintexts is expected to be zero. In contrast, a random permutation will almost never produce a zero XOR sum.

---

## 1. AES Encryption Tool

### Overview

The AES Encryption Tool is implemented in the `AESEncryption.py` file. It provides:
- **AES Encryption Function:** Encrypts a 128-bit plaintext using a 128-bit key for a specified number of rounds.
- **AES Encryption Oracle:** The `aesEncryptOracle` function encrypts plaintexts using 3-round AES and returns a 128-bit ciphertext as an integer.

### Input & Output

- **Input:**
  - Plaintext: 32-character hexadecimal string (16 bytes).
  - Key: 32-character hexadecimal string (16 bytes).
  - Rounds: Integer specifying the number of AES rounds (3 for this attack).
- **Output:**
  - Ciphertext: 32-character hexadecimal string.

### How to Run

1. **Install required packages:**
    ```bash
    pip install numpy
    ```
2. **Run the AES Encryption Tool:**
    ```bash
    python AESEncryption.py
    ```
3. **Example Output:**
    ```
    Enter the plain text (32 hex digits): 3243f6a8885a308d313198a2e0370734
    Enter the cipher key (32 hex digits): 2b7e151628aed2a6abf7158809cf4f3c
    Enter the number of rounds: 10
    Encrypted Cipher Text: 3925841d02dc09fbdc118597196a0b32
    ```

---

## 2. Random Permutation Oracle

### Overview

The Random Permutation Oracle is implemented in `RandomPermutation.py`. It generates a unique 128-bit random ciphertext for each plaintext, simulating a random permutation. The updated implementation also includes an interactive mode for user input.

### Input & Output

- **Input:**
  - Plaintext: 32-character hexadecimal string (16 bytes).
- **Output:**
  - Ciphertext: 128-bit integer (displayed as a hexadecimal string).

### How to Run

1. **Run the Random Permutation Oracle:**
    ```bash
    python RandomPermutation.py
    ```
2. **Example Output:**
    ```
    Enter the plain text (32 hex digits): 0123456789abcdef0123456789abcdef
    The cipher text is: 0x5e2f3c1a9b7d4e8f0123456789abcdef
    ```

---

## 3. Distinguisher Attack

### Overview

The Distinguisher Attack is implemented in `DistinguisherAttack.py`. It follows these steps:
1. Generate 256 plaintexts by varying one byte of a base plaintext.
2. Query the AES encryption oracle and the random permutation oracle.
3. Compute the XOR sum of the ciphertexts.
4. Distinguish between AES and a random permutation based on the XOR result.

### Input & Output

- **Input:**
  - Base Plaintext: 128-bit integer.
  - Key: 128-bit integer.
  - Rounds: Fixed to 3 for AES.
- **Output:**
  - XOR Sum: 128-bit integer.
  - Result: A message indicating whether the oracle is likely a 3-round AES or a random permutation.

### How to Run

1. **Ensure all files are in the same directory:**
    - `AESEncryption.py`
    - `RandomPermutation.py`
    - `DistinguisherAttack.py`
2. **Run the Distinguisher Attack:**
    ```bash
    python DistinguisherAttack.py
    ```
3. **Example Output:**
```
AES Oracle (3-round AES) Attack:
XOR sum of ciphertexts: 0x00000000000000000000000000000000
Result: Likely 3-round AES encryption (integral property holds).

Random Permutation Oracle Attack:
XOR sum of ciphertexts: 0x8f23c4a1d5b67890ef1234567890abcd
Result: Likely a random permutation (integral property does not hold).
```

---

## Conclusion

This project demonstrates the effectiveness of the distinguishing attack using integral cryptanalysis on 3-round AES. By analyzing the XOR sum of ciphertexts, the attack can reliably differentiate between a 3-round AES encryption oracle and a random permutation oracle.
