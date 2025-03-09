# Import functions from the toy cipher module and the DDT module.
from ToyCipher import S_BOX, to_bits, from_bits, permute
from DDT import generate_ddt

# -------------------------------
# Helper Functions: Conversion between integer and nibbles
# -------------------------------
def int_to_nibbles(x):
    """
    Convert a 16-bit integer to a list of 4 nibbles (MSB first).
    For example, 0x1234 -> [0x1, 0x2, 0x3, 0x4].
    """
    nibbles = []
    for i in range(4):
        nibble = (x >> (4 * (3 - i))) & 0xF
        nibbles.append(nibble)
    return nibbles

def nibbles_to_int(nibbles):
    """
    Convert a list of 4 nibbles (MSB first) to a 16-bit integer.
    For example, [0x1, 0x2, 0x3, 0x4] -> 0x1234.
    """
    x = 0
    for nib in nibbles:
        x = (x << 4) | nib
    return x

# -------------------------------
# Generate the DDT using the provided S_BOX.
# -------------------------------
ddt = generate_ddt(S_BOX)

# -------------------------------
# Precompute Best Differential Transitions for a Nibble
# -------------------------------
# For each input nibble difference d (1 <= d <= 15), choose the output difference dy
# that occurs most frequently, and compute its probability as count/16.
best_transitions = {}
for d in range(16):
    if d == 0:
        best_transitions[d] = (0, 1.0)  # Trivial: 0 -> 0 with probability 1.
    else:
        best_count = 0
        best_dy = 0
        for dy in range(16):
            if ddt[d][dy] > best_count:
                best_count = ddt[d][dy]
                best_dy = dy
        best_transitions[d] = (best_dy, best_count / 16.0)
# For instance, the provided DDT suggests that for input F the best output is D (with probability 10/16 = 0.625).

# -------------------------------
# Differential Trail Simulation over 4 Rounds
# -------------------------------
def apply_best_substitution(nibbles):
    """
    For each nibble in the list, if nonzero, replace it with the best output difference
    (as precomputed in best_transitions) and multiply the round probability.
    Returns the new list of nibbles and the product probability for the round.
    """
    new_nibbles = []
    round_prob = 1.0
    for nib in nibbles:
        best_out, p = best_transitions[nib]
        new_nibbles.append(best_out)
        round_prob *= p
    return new_nibbles, round_prob

def simulate_trail(start_diff, rounds=4):
    """
    Simulate the differential trail over 'rounds' rounds starting from start_diff.
    In each round:
      - Convert the 16-bit difference to 4 nibbles (MSB first).
      - Apply the best S-box differential transition for each nibble.
      - Reassemble the nibbles to a 16-bit integer.
      - Convert to bits and apply the fixed permutation (using the imported permute function).
    Returns:
      - trail: list of 16-bit differences for each round (including the starting difference)
      - overall_prob: overall probability of the trail (product of round probabilities).
    """
    trail = [start_diff]
    overall_prob = 1.0
    current_diff = start_diff
    for r in range(rounds):
        # Split current difference into nibbles (MSB first)
        nibbles = int_to_nibbles(current_diff)
        # Apply best substitution for each nibble
        new_nibbles, round_prob = apply_best_substitution(nibbles)
        overall_prob *= round_prob
        # Reassemble to a 16-bit integer (before permutation)
        diff_before_perm = nibbles_to_int(new_nibbles)
        # Convert to bits, apply permutation, and convert back to a 16-bit integer
        bits = to_bits(diff_before_perm)
        permuted_bits = permute(bits)
        next_diff = from_bits(permuted_bits)
        trail.append(next_diff)
        current_diff = next_diff
    return trail, overall_prob

# -------------------------------
# Search Over Candidate Starting Differences
# -------------------------------
# For simplicity, we consider candidates where only one nibble is active (nonzero).
# There are 4 positions × 15 possible nonzero values = 60 candidates.
candidate_trails = []
for pos in range(4):  # Nibble positions 0 (MSB) to 3 (LSB)
    for val in range(1, 16):  # Nonzero nibble value
        nibbles = [0, 0, 0, 0]
        nibbles[pos] = val
        start_diff = nibbles_to_int(nibbles)
        trail, prob = simulate_trail(start_diff, rounds=4)
        candidate_trails.append((start_diff, trail, prob))

# Sort candidate trails by overall probability in descending order.
candidate_trails.sort(key=lambda x: x[2], reverse=True)

# -------------------------------
# Output the Top 10 Differential Trails
# -------------------------------
print("\nTop 10 Differential Trails (over 4 rounds):")
for i, (start_diff, trail, prob) in enumerate(candidate_trails[:10], start=1):
    # Format each difference in the trail as a 4-digit hexadecimal number.
    trail_hex = " -> ".join(f"{d:04X}" for d in trail)
    print(f"Trail {i}: Start Diff = {start_diff:04X}, Trail: {trail_hex}, Overall Probability = {prob:.6f}")


"""
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

"""