from ToyCipher import S_BOX

# Function to generate the Difference Distribution Table (DDT)
def generate_ddt(s_box):
    # Initialize a 16x16 table with zeros
    DDT = [[0 for _ in range(16)] for _ in range(16)]

    # Iterate over all possible input differences (ΔX)
    for delta_x in range(16):
        # Iterate over all possible input values (x)
        for x in range(16):
            # Compute the corresponding output difference ΔY
            y1 = s_box[x]                    # S-Box output for x
            y2 = s_box[x ^ delta_x]          # S-Box output for (x ⊕ ΔX)
            delta_y = y1 ^ y2                # Compute the difference ΔY
            
            # Increment the count in the table
            DDT[delta_x][delta_y] += 1

    return DDT

# Function to print the DDT in a readable format
def print_ddt(ddt):
    print("\nDifference Distribution Table (DDT):")
    print("    " + " ".join(f"{i:2X}" for i in range(16)))  # Column headers
    print("   " + "-" * 48)

    for i, row in enumerate(ddt):
        print(f"{i:2X} | " + " ".join(f"{val:2}" for val in row))

if __name__ == "__main__":
    # Generate and print the DDT for the given S-Box
    ddt = generate_ddt(S_BOX)
    print_ddt(ddt)


"""
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

"""