import random
from ToyCipher import S_BOX, to_bits, from_bits, permute, substitute, round_keys, encrypt, inverse_substitute
from DDT import generate_ddt


# ----------------------------------------------------------
# Data collection phase: Generate unique plaintext-ciphertext pairs with a fixed input difference.
# ----------------------------------------------------------
def generate_unique_plaintext_ciphertext_pairs(num_pairs, input_diff=0x0020):
    """
    Generate unique random plaintext pairs with a fixed input difference and compute their ciphertexts.
    
    Parameters:
      num_pairs (int): Number of unique plaintext pairs to generate.
      input_diff (int): The 16-bit input difference to use (default: 0x0020, corresponding to nibbles [0, 0, 2, 0]).
    
    Returns:
      pairs (list of tuples): Each tuple contains:
         (plaintext m, plaintext m' = m XOR input_diff, ciphertext of m, ciphertext of m').
    """
    # Use random.sample to generate unique 16-bit plaintexts.
    unique_plaintexts = random.sample(range(0, 0x10000), num_pairs)
    
    pairs = []
    for m in unique_plaintexts:
        # Generate paired plaintext by XORing with the fixed input difference.
        m_prime = m ^ input_diff
        
        # Encrypt both plaintexts using the toy cipher's encrypt function. For 5 rounds
        c = encrypt(m, round_keys)
        c_prime = encrypt(m_prime, round_keys)
        
        # Store the tuple (plaintext, plaintext pair, ciphertext, ciphertext pair).
        pairs.append((m, m_prime, c, c_prime))
    
    return pairs

# Generate unique pairs.
num_pairs = 51  # Example: 64 pairs. We can do 2**6 = 64 pairs to have a high probability of finding the correct key.
# The probability of the choosen differential trail is 0.019775. So the inverse of this probability is 51.
# This means that we need to generate 51 pairs to have a high probability of finding the correct key.
pairs = generate_unique_plaintext_ciphertext_pairs(num_pairs)

# Print the first 5 pairs to verify:
print("Unique Plaintext and Ciphertext Pairs (first 3):")
for i, (m, m_prime, c, c_prime) in enumerate(pairs[:3], start=1):
    print(f"Pair {i}:")
    print(f"   Plaintext 1: {m:04X}, Plaintext 2: {m_prime:04X}")
    print(f"   Ciphertext 1: {c:04X}, Ciphertext 2: {c_prime:04X}")

#-------------------------------------------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# Filtering Phase: Discard the pairs that have dont have the zero difference in the other nibbles except the non zero nibble of the output difference.
# ------------------------------------------------------------------------------------------------------------------------------------------------------

# For each pair, compute the ciphertext difference diff = c XOR c_prime.
# We interpret diff as 4 nibbles (MSB first) and check if it is of the form (0, 0, z, 0)
# (i.e. the first, second, and fourth nibbles are 0, while the third nibble can be any value).
# If so, we keep only the correct filtered pair for key recovery pair for the key recovery phase.
filtered_pairs = []
for m, m_prime, c, c_prime in pairs:
    diff = c ^ c_prime
    nibble0 = (diff >> 12) & 0xF  # Bits 15-12 (MSB)
    nibble1 = (diff >> 8) & 0xF   # Bits 11-8
    nibble2 = (diff >> 4) & 0xF   # Bits 7-4
    nibble3 = diff & 0xF          # Bits 3-0 (LSB)
    if nibble0 == 0 and nibble1 == 0 and nibble3 == 0:
        filtered_pairs.append((m, m_prime, c, c_prime, diff))

print("\n\nNumber of pairs with ciphertext difference of form (0, 0, z, 0):", len(filtered_pairs),"\n\n")

# Print the first 3 filtered pairs to verify:
print("\nFiltered pairs (first 3):")
for i, (m, m_prime, c, c_prime, diff) in enumerate(filtered_pairs[:3], start=1):
    print(f"Pair {i}:")
    print(f"  Plaintext 1: {m:04X}, Plaintext 2: {m_prime:04X}")
    print(f"  Ciphertext 1: {c:04X}, Ciphertext 2: {c_prime:04X}")
    print(f"  Difference: {diff:04X}   (nibbles: {(diff >> 12) & 0xF:X} {(diff >> 8) & 0xF:X} {(diff >> 4) & 0xF:X} {diff & 0xF:X})")




# ----------------------------------------------------------
# ----------------------------------------------------------
# Key Recovery Phase for the Last Round Key
# Sub part-1 : Compute the nibbles of the round key with non zero values in the output difference.
# ----------------------------------------------------------
def compute_v(ciphertext, candidate_key):
    """
    Compute the intermediate value v = S^{-1}(ciphertext XOR candidate_key)
    using the provided inverse substitution snippet from the ToyCipher module.
    
    Steps:
      1. XOR the ciphertext with candidate_key.
      2. Split the result into 4 nibbles (MSB first).
      3. Apply inverse S-box substitution to each nibble.
      4. Reassemble the nibbles into a 16-bit integer (MSB first).
    """
    state = ciphertext ^ candidate_key
    state_nibbles = [(state >> (4 * j)) & 0xF for j in range(4)][::-1]
    state_nibbles = [inverse_substitute(n) for n in state_nibbles]
    v = sum(n << (4 * (3 - j)) for j, n in enumerate(state_nibbles))
    return v

def recover_last_round_key_non_zero_nibbles(filtered_pairs, expected_delta_y_list):
    """
    Recover the last round key with non zero nibbles for output difference (kr) from the filtered ciphertext pairs.
    
    Parameters:
      filtered_pairs (list): Each element is a tuple (m, m_prime, c, c_prime, diff).
      expected_delta_y_list (list): A list of acceptable values for v XOR v',
          for example, [0x0010, 0x0020, 0x0090, 0x00A0].
    
    Returns:
      best_key (int): The candidate last round key with the highest counter.
      best_count (int): The maximum counter value.
    """
    num_keys = 1 << 16  # 2^16 possible candidate keys.
    counters = [0] * num_keys
    
    for (m, m_prime, c, c_prime, diff) in filtered_pairs:
        for candidate_key in range(num_keys):
            v  = compute_v(c, candidate_key)
            v_prime = compute_v(c_prime, candidate_key)
            if (v ^ v_prime) in expected_delta_y_list:
                counters[candidate_key] += 1
                
    best_key = max(range(num_keys), key=lambda k: counters[k])
    best_count = counters[best_key]
    return best_key, best_count

# Expected Δ(y) values after the last round's inverse S-box, from the differential trail:
expected_delta_y_list = [0x0010, 0x0020, 0x0090, 0x00A0]

# Recover the last round key using the filtered pairs.
recovered_key_with_non_zero_nibbles_recovered, count = recover_last_round_key_non_zero_nibbles(filtered_pairs, expected_delta_y_list)
print(f"\n\nRecovered Last Round Key with the nibbles having non zero output difference: {recovered_key_with_non_zero_nibbles_recovered:04X} with counter = {count}")


# ----------------------------------------------------------
# Key Recovery Phase for the Full Key
# Sub part -2 : Brute-force the Last Round Key for the nibbles having zero output difference, in this case the nibbles except the third position
# ----------------------------------------------------------

test_pairs = filtered_pairs[:2]  # Use the first two filtered pairs for key validation.
print("\nUsing the following two pairs for key validation:")
for i, (m, m_prime, c, c_prime, diff) in enumerate(test_pairs, start=1):
    print(f"Test Pair {i}: Plaintext: {m:04X} -> Ciphertext: {c:04X}")

# Brute-force the last round key using the two test pairs.
# We assume from differential analysis that the third nibble (MSB-first) of the last round key is recovered as 0x6.
# The candidate key has the form: [nibble0, nibble1, 0x6, nibble3]
# We brute-force over the remaining 12 bits (i.e., nibble0, nibble1, and nibble3 each range over 0x0-0xF).

def brute_force_last_round_key_zero_nibbles_output_differences(test_pairs, fixed_round_keys, recovered_nibble):
    """
    Brute-force the last round key using two plaintext-ciphertext pairs.
    
    Parameters:
      test_pairs (list): A list of tuples (m, m_prime, c, c_prime, diff) for testing.
      fixed_round_keys (list): The known first 5 round keys. The last round key is unknown. So it is a candidate or experimentative key.
      recovered_nibble (int): The recovered nibble (4 bits) that must be in the third position (MSB-first) of the last round key.
      
    Returns:
      The full 16-bit last round key if found, else None.
    """
    for candidate in range(2**12):  # 0 to 4095
        # Decompose the 12-bit candidate into three nibbles.
        nibble0 = (candidate >> 8) & 0xF  # Most significant unknown nibble.
        nibble1 = (candidate >> 4) & 0xF  # Second nibble.
        nibble3 = candidate & 0xF         # Least significant nibble.
        
        # Construct the full candidate key: [nibble0, nibble1, recovered_nibble, nibble3]
        candidate_last_key = (nibble0 << 12) | (nibble1 << 8) | (recovered_nibble << 4) | nibble3
        
        # Combine with the fixed first five round keys.
        candidate_round_keys = fixed_round_keys[:] + [candidate_last_key]
        
        valid = True
        # Test the candidate key on each of the two test pairs.
        for (m, m_prime, c, c_prime, _) in test_pairs:
            test_cipher = encrypt(m, candidate_round_keys)
            if test_cipher != c:
                valid = False
                break
        if valid:
            return candidate_last_key
    return None

# Use the known first five round keys.
fixed_round_keys = round_keys[:5]

# Attempt to recover the full last round key using two test pairs.
recovered_last_key = brute_force_last_round_key_zero_nibbles_output_differences(test_pairs, fixed_round_keys, recovered_key_with_non_zero_nibbles_recovered>> 4)
if recovered_last_key is not None:
    print(f"\nRecovered Last Round Key: {recovered_last_key:04X}")
else:
    print("\nNo candidate key produced the expected ciphertext for both test pairs. Re-check your analysis or try additional pairs. Cause : again the use of random function")




"""
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
"""