import numpy as np

# Function to print checkerboard pattern
def print_checkerboard01(num):
    """
    Prints a checkerboard pattern of size num x num.

    Args:
        num (int): The size of the checkerboard pattern.

    The function generates a two-dimensional numpy array of zeros
    and fills it with ones in alternating positions to create the
    checkerboard pattern. It then prints each row of the pattern.
    """

    print("Checkerboard pattern:")
    # create a n * n matrix
    buffer = np.zeros((num, num), dtype=int)
    # fill with 1 the alternate cells in rows and columns
    buffer[1::2, ::2] = 1
    buffer[::2, 1::2] = 1
    # print the pattern
    for i in range(num):
        for j in range(num):
            print(buffer[i][j], end=" ")
        print()

# Test
test_num01 = 8
print_checkerboard01(test_num01)

def print_checkerboard02(num):
    """
    Prints a checkerboard pattern of size num x num.

    Args:
        num (int): The size of the checkerboard pattern.

    The function generates a two-dimensional numpy array of zeros
    and fills it with ones in alternating positions to create the
    checkerboard pattern. It then prints each row of the pattern.
    """
    final = []
    for i in range(num):
        final.append((list(np.tile([0, 1], int(num / 2)))) if i % 2 == 0 else list(np.tile([1, 0], int(num / 2))))
    print(np.array(final))

test_num02 = 9
print_checkerboard02(test_num02)
