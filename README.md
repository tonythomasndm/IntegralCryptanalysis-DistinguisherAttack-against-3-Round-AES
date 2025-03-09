# Part-1 Toy Cipher Implementation

This part presents a custom toy cipher that I developed to explore and demonstrate the core concepts of symmetric encryption. The cipher operates on 16-bit plaintext through a series of transformation rounds, emphasizing the encryption process to provide a clear understanding of substitution and permutation in cryptographic design.

## Overview

The cipher uses a simple yet effective approach that includes:
- **Substitution:** A defined S-Box replaces each 4-bit nibble with another value. This introduces non-linearity, an essential characteristic for secure encryption.
- **Permutation:** A P-Box rearranges the bits after substitution. This bit shuffling ensures that small changes in the plaintext or key spread throughout the ciphertext.
- **Round Key Mixing:** Each encryption round starts with an XOR operation using a unique round key. These keys add another layer of security by incorporating external secret data.

While decryption is implemented to reverse these steps, the project particularly focuses on the encryption mechanism. By dissecting each step of the encryption, one can understand how the transformation of the plaintext into ciphertext occurs through multiple rounds of processing. In each round, after the XOR with the round key, the state is broken down into nibbles, substituted using the S-Box, reassembled into bits, and then permuted. The final round concludes with a substitution and a final XOR operation to produce the ciphertext.

## Note

I have also corrected the error in the code provided, as it was working in the reverse oprder in your code for the conversion of nibbles into integer it was doing lsb to msb instead of msb to lsb. I have corrected that in both instances at the step before applying permuatations converting the nibbles into integer and then the integer into bits as well as in the alst round before the final zxor, converting teh susbtituted nibbels into inetegr value. 

## How to Run

1. **Prerequisites:**  
   Ensure Python (version 3.x) is installed on your system.

2. **Execution:**  
   Save the code in a file named `ToyCipher.py` and run it from the command line:
   ```bash
   python ToyCipher.py


## Example output

Plaintext: 1234
Round Keys: [4369, 8738, 13107, 17476, 21845, 26214]
Ciphertext: 6092
Decrypted Text: 1234


# Part -2 Difference Distribution Table (DDT) Generation for Toy Cipher

This part is dedicated to creating a Difference Distribution Table (DDT) for the S-Box used in my toy cipher implementation. I developed this script as part of my work in differential cryptanalysis to trace how input differences propagate through the S-Box, thereby identifying potential trails that can be exploited in cryptanalysis.

## Overview

The DDT is a 16x16 table where:
- **Rows:** Represent all possible input differences (ΔX) from 0x0 to 0xF.
- **Columns:** Represent all possible output differences (ΔY) from 0x0 to 0xF.
- **Cell Values:** Indicate the number of times a specific output difference is produced for a given input difference when the S-Box is applied.

## Key Functions

- **`generate_ddt(s_box)`**  
  This function initializes a 16x16 table with zeros and computes the DDT by iterating over every possible input difference (ΔX) and input value (x). For each x, it calculates:
  - `y1 = s_box[x]` (the S-Box output for x)
  - `y2 = s_box[x ^ ΔX]` (the S-Box output for x ⊕ ΔX)
  - `ΔY = y1 ^ y2`  
  The function then updates the table by incrementing the count corresponding to each output difference ΔY.

- **`print_ddt(ddt)`**  
  This helper function formats and prints the DDT in a readable table format. It displays column headers and rows in hexadecimal format, making it easier to analyze the frequency of each ΔY for every ΔX.

## How It Works

1. **Initialization:**  
   A 16x16 table is created using list comprehensions, with all cells initialized to zero.

2. **DDT Calculation:**  
   The `generate_ddt(s_box)` function iterates through every possible input difference and, for each input value, computes the output difference using the S-Box. The computed ΔY values are recorded in the table, indicating how many times each output difference occurs.

3. **Display:**  
   The computed DDT is then printed using the `print_ddt(ddt)` function, which formats the table with headers for clarity.

## How to Run

1. **Prerequisites:**  
   - Python 3.x must be installed.
   - Ensure the `ToyCipher` module containing the S-Box is available in your project directory or Python path.

2. **Execution:**  
   Save the script as `DDT.py` and execute it in your terminal:
   ```bash
   python DDT.py

## Example Output - 
Output:

Difference Distribution Table (DDT):
     0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F
   ------------------------------------------------
 0 | 16  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
 1 |  0  0  6  0  0  0  0  2  0  2  0  0  2  0  4  0
 2 |  0  6  6  0  0  0  0  0  0  2  2  0  0  0  0  0
 3 |  0  0  0  6  0  2  0  0  2  0  0  0  4  0  2  0
 4 |  0  0  0  2  0  2  4  0  0  2  2  2  0  0  2  0
 5 |  0  2  2  0  4  0  0  4  2  0  0  2  0  0  0  0
 6 |  0  0  2  0  4  0  0  2  2  0  2  2  2  0  0  0
 7 |  0  0  0  0  0  4  4  0  2  2  2  2  0  0  0  0
 8 |  0  0  0  0  0  2  0  2  4  0  0  4  0  2  0  2
 9 |  0  2  0  0  0  2  2  2  0  4  2  0  0  0  0  2
 A |  0  0  0  0  2  2  0  0  0  4  4  0  2  2  0  0
 B |  0  0  0  2  2  0  2  2  2  0  0  4  0  0  2  0
 C |  0  4  0  2  0  2  0  0  2  0  0  0  0  0  6  0
 D |  0  0  0  0  0  0  2  2  0  0  0  0  6  2  0  4
 E |  0  2  0  4  2  0  0  0  0  0  2  0  0  0  0  6
 F |  0  0  0  0  2  0  2  0  0  0  0  0  0 10  0  2


# Part -3 - Differential Trail Analysis for the cipher

This part focuses on obtaining differential trails with the highest probability using a toy cipher. I developed this tool to explore the cipher's differential properties by leveraging the Difference Distribution Table (DDT) of the S-Box and simulating trails over multiple rounds.

## Overview

In this, I first compute the DDT for the S-Box and then precompute the best differential transitions for every nibble difference. The DDT provides frequency counts for output differences given an input difference, and for each nonzero nibble difference, the best output difference (with its probability) is stored. These probabilities are then used to simulate differential trails.

## Key Components and Functions

- **`generate_ddt(s_box)`**  
  Computes the DDT for the given S-Box by iterating over all possible input differences and values.

- **`int_to_nibbles(x)` and `nibbles_to_int(nibbles)`**  
  Convert between 16-bit integers and their 4-nibble (4-bit) representations, ensuring that operations can be applied nibble-wise.

- **`apply_best_substitution(nibbles)`**  
  For each nibble, this function uses the precomputed best differential transitions (from the DDT) to replace the current difference with the best output difference, while updating the round probability.

- **`simulate_trail(start_diff, rounds=4)`**  
  Simulates a differential trail over multiple rounds. Each round:
  1. Converts the 16-bit difference to 4 nibbles.
  2. Applies the best S-box differential transition (using `apply_best_substitution`).
  3. Reassembles the nibbles into a 16-bit integer.
  4. Applies a fixed permutation (using the `permute` function).
  
  The overall probability of the trail is the product of the probabilities from each round.

## Obtaining the Highest Probability Differential Trail

To find the most promising differential trail:
1. **Candidate Selection:**  
   I consider candidate starting differences where only one nibble is active. This yields 60 candidates (4 nibble positions × 15 nonzero values).
   
2. **Simulation and Evaluation:**  
   Each candidate is processed using `simulate_trail`, which produces a trail and its corresponding overall probability.
   
3. **Sorting and Selection:**  
   All candidate trails are sorted in descending order based on their overall probability. The trail with the highest probability is considered the best differential trail, indicating the most likely path for differential propagation through the cipher.

## How to Run

1. Ensure Python 3.x is installed and the project modules (`ToyCipher` and `DDT`) are correctly structured in your project.
2. Save the script as, for example, `DifferentialTrail.py`.
3. Run the script:
   ```bash
   python DifferentialTrail.py

## Example Output

Top 10 Differential Trails (over 4 rounds):
Trail 1: Start Diff = 0010, Trail: 0010 -> 0020 -> 0002 -> 0001 -> 0010, Overall Probability = 0.019775
Trail 2: Start Diff = 0020, Trail: 0020 -> 0002 -> 0001 -> 0010 -> 0020, Overall Probability = 0.019775
Trail 3: Start Diff = 0001, Trail: 0001 -> 0010 -> 0020 -> 0002 -> 0001, Overall Probability = 0.019775
Trail 4: Start Diff = 0002, Trail: 0002 -> 0001 -> 0010 -> 0020 -> 0002, Overall Probability = 0.019775
Trail 5: Start Diff = 1000, Trail: 1000 -> 0080 -> 2000 -> 0008 -> 1000, Overall Probability = 0.008789
Trail 6: Start Diff = 2000, Trail: 2000 -> 0008 -> 1000 -> 0080 -> 2000, Overall Probability = 0.008789
Trail 7: Start Diff = 0080, Trail: 0080 -> 2000 -> 0008 -> 1000 -> 0080, Overall Probability = 0.008789
Trail 8: Start Diff = 0008, Trail: 0008 -> 1000 -> 0080 -> 2000 -> 0008, Overall Probability = 0.008789
Trail 9: Start Diff = 8000, Trail: 8000 -> 8000 -> 8000 -> 8000 -> 8000, Overall Probability = 0.003906
Trail 10: Start Diff = 0100, Trail: 0100 -> 0040 -> 0220 -> 0006 -> 0100, Overall Probability = 0.003296


## Note

I choose the trail with input diference 0020 to 0020 for the Key recovery step as it is one of the highest proabbaility like 0.019775

# Part - 4 Key Recovery using the differnetial trail obtained

This pART implements a comprehensive differential cryptanalysis attack on a toy cipher. The code is structured into three major phases: data collection, filtering, and key recovery. The aim is to recover the last round key by analyzing how specific differences in the plaintext propagate through the cipher, using both statistical analysis (via differential trails) and brute-force techniques.

---

## Overview

The attack leverages several cryptographic components:
- **ToyCipher Module:** Supplies the S-Box (`S_BOX`), conversion functions (`to_bits`, `from_bits`), permutation (`permute`), substitution functions (`substitute` and `inverse_substitute`), encryption routine (`encrypt`), and a set of predefined round keys (`round_keys`) - here we need to find the last round key.
- **DDT Module:** Provides `generate_ddt`, a function to compute the Difference Distribution Table (DDT) for the S-Box, which is crucial for understanding the differential behavior of the cipher.

---

## Data Collection Phase

### Generating Unique Plaintext-Ciphertext Pairs

- **Function:** `generate_unique_plaintext_ciphertext_pairs(num_pairs, input_diff=0x0020)`
- **Purpose:**  
  Generates a set of unique 16-bit plaintexts and computes corresponding ciphertext pairs with a fixed input difference.  
- **Process:**  
  - **Unique Plaintexts:** Uses `random.sample` to select unique values from the range 0 to 0xFFFF.
  - **Paired Plaintexts:** For each plaintext `m`, computes `m_prime = m XOR input_diff` (using `0x0020` by default).
  - **Encryption:** Encrypts both `m` and `m_prime` using the `encrypt` function with the predetermined `round_keys`.
  - **Output:** Returns a list of tuples `(m, m_prime, c, c_prime)`.

A sample of the first three pairs is printed to verify that the data collection is working correctly.

---

## Filtering Phase

### Selecting Pairs with Specific Ciphertext Differences

- **Objective:**  
  Identify pairs where the ciphertext difference has a particular structure: only the third nibble is nonzero, i.e., a difference of the form `(0, 0, z, 0)` (MSB-first).
- **Process:**  
  - For each pair, compute `diff = c XOR c_prime`.
  - Extract each nibble:
    - **nibble0:** Bits 15-12
    - **nibble1:** Bits 11-8
    - **nibble2:** Bits 7-4
    - **nibble3:** Bits 3-0
  - Only pairs with `nibble0 == 0`, `nibble1 == 0`, and `nibble3 == 0` are kept.
- **Outcome:**  
  The filtered list (`filtered_pairs`) contains pairs that are most promising for key recovery, and the number of such pairs is printed along with a sample.

---

## Key Recovery Phase

### Part 1: Recovering Non-Zero Nibbles of the Last Round Key

- **Function:** `compute_v(ciphertext, candidate_key)`
  - **Purpose:**  
    Calculates the intermediate value \( v \) which is one round back using the formula:  
    \[
    v = S^{-1}(\text{ciphertext} \oplus \text{candidate\_key})
    \]
  - **Steps:**  
    1. XOR the ciphertext with the candidate key.
    2. Split the result into 4 nibbles (ensuring MSB-first order).
    3. Apply the inverse S-box substitution to each nibble.
    4. Reassemble the nibbles into a 16-bit integer.
  
- **Function:** `recover_last_round_key_non_zero_nibbles(filtered_pairs, expected_delta_y_list)`
  - **Purpose:**  
    Identifies the candidate key for the nibbles that are associated with a nonzero output difference.
  - **Process:**  
    - Iterate over all \( 2^{16} \) candidate keys.
    - For each filtered pair, compute \( v \) and \( v' \) for the two ciphertexts i.e normal one and the input difference encrypted one.
    - Check if \( v \oplus v' \) is within an expected set of differences (`expected_delta_y_list`, e.g., `[0x0010, 0x0020, 0x0090, 0x00A0]`).
    - Increment a counter for each candidate key that meets the condition.
    - The candidate key with the highest counter is selected as the best candidate for the nonzero nibbles.
  
The recovered key portion and its counter are printed.

### Part 2: Brute-Force Recovery for the Full Last Round Key

- **Objective:**  
  After recovering the key part corresponding to nonzero differences, the remaining key bits (from the nibbles with zero output differences) are recovered by brute-forcing over a reduced key space.
- **Function:** `brute_force_last_round_key_zero_nibbles_output_differences(test_pairs, fixed_round_keys, recovered_nibble)`
  - **Purpose:**  
    Uses two test pairs (a subset of filtered pairs) and a known fixed nibble (recovered in Part 1) to brute-force the remaining unknown nibbles of the last round key.
  - **Process:**  
    - Iterate over \( 2^{12} \) candidates corresponding to the three unknown nibbles.
    - Decompose the 12-bit candidate into three 4-bit nibbles: nibble0 (MSB), nibble1, and nibble3 (LSB).
    - Construct a candidate last round key by inserting the recovered nibble into the third nibble position.
    - Combine this candidate with the known first five round keys to form a full round key set.
    - Validate the candidate key by re-encrypting the plaintext from each test pair and comparing with the given ciphertext.
    - Return the candidate key if it is consistent with all test pairs.
  
The full recovered last round key is then printed if found.

---

## How to Run the Code

1. **Prerequisites:**
   - Python 3.x installed.
   - The `ToyCipher` and `DDT` modules must be available and correctly referenced in your project.
2. **Execution:**
   - Save the script as, for example, `KeyRecovery.py`.
   - Run the script from the terminal:
     ```bash
     python KeyRecovery.py
     ```
3. **Expected Output:**
   - A printed list of unique plaintext-ciphertext pairs.
   - The number of filtered pairs meeting the ciphertext difference criterion.
   - Sample details of a few filtered pairs.
   - The recovered candidate key portion (for nonzero nibbles) and its counter.
   - The fully recovered last round key after brute-forcing the unknown nibbles.

---

## Example ouput

Output: 
Unique Plaintext and Ciphertext Pairs (first 3):
Pair 1:
   Plaintext 1: 4718, Plaintext 2: 4738
   Ciphertext 1: 1E06, Ciphertext 2: 6E81
Pair 2:
   Plaintext 1: C8AB, Plaintext 2: C88B
   Ciphertext 1: A2BB, Ciphertext 2: 59FB
Pair 3:
   Plaintext 1: 0C13, Plaintext 2: 0C33
   Ciphertext 1: DB97, Ciphertext 2: 8EBD


Number of pairs with ciphertext difference of form (0, 0, z, 0): 11 



Filtered pairs (first 3):
Pair 1:
  Plaintext 1: F1DF, Plaintext 2: F1FF
  Ciphertext 1: 44D4, Ciphertext 2: 44C4
  Difference: 0010   (nibbles: 0 0 1 0)
Pair 2:
  Plaintext 1: 3976, Plaintext 2: 3956
  Ciphertext 1: FD9D, Ciphertext 2: FD0D
  Difference: 0090   (nibbles: 0 0 9 0)
Pair 3:
  Plaintext 1: 63BC, Plaintext 2: 639C
  Ciphertext 1: D368, Ciphertext 2: D348
  Difference: 0020   (nibbles: 0 0 2 0)


Recovered Last Round Key with the nibbles having non zero output difference: 0050 with counter = 11

Using the following two pairs for key validation:
Test Pair 1: Plaintext: F1DF -> Ciphertext: 44D4
Test Pair 2: Plaintext: 3976 -> Ciphertext: FD9D

Recovered Last Round Key: 6656


## Conclusion

This detailed script demonstrates a full differential cryptanalysis attack on a toy cipher. By carefully generating plaintext-ciphertext pairs, filtering them based on a specific difference pattern, and applying a two-part key recovery process, the project illustrates the practical challenges and methodologies involved in recovering secret keys. The combination of statistical differential analysis and targeted brute-force search exemplifies a robust approach to cryptographic key recovery.