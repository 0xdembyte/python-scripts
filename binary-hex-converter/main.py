# Developer details: Demarjio Brady
# Description: This python script contains two ways of converting decimal numbers into different formats (binary, and hex code) 

def convert_to_binary(number):
    '''
        Takes a decimal number (8 bit number assumed) and converts it into a 8 bit binary system number
    '''

    # String used for constructing the final binary number
    binary_number = ""

    # Set the current bit to 128 since 128 is the highest bit for an 8 bit binary system
    current_bit   = 128

    # Iterate 8 times since binary only contains 8 bits
    for _ in range(8):
        # Check if the number is greater than or equal to the current bit
        if number >= current_bit:
            # Addon to the binary number a 1 (meaning enabled for that bit) since it meets the conditions required
            binary_number += "1"

            # Set the number to the remainder left over after enabling the current bit
            number -= current_bit
        else:
            # Addon to the binary number 0 (meaning disabled) since we didn't meet the conditions required
            binary_number += "0"
        
        # Divide the current bit by 2 (e.g. 128 -> 64)
        current_bit //= 2
    
    # Return the final constructed binary number
    return binary_number


def convert_to_hex(number):
    '''
        Takes a decimal number and converts it into hex code.
    '''

    # String used for constructing the final hex code
    hex_code = ""

    # List used to store the remainders
    remainders = []

    # Keep dividing the number until we hit 0
    while number  > 0:
        # Store the remainder
        remainders.append(number % 16)

        # Set the quotient
        number = number // 16

    # Since hex numbers are reversed we reverse the list of remainders
    # and then iterate through them
    for remainder in reversed(remainders):
        # Check if the remainder goes over 9
        if remainder > 9:
            # Addon to the hex code, with the corresponding letter (e.g. A for 10)
            hex_code += chr(ord("A") + remainder - 10)
        else:
            # The remainder is lower or equal to nine
            # We add the remainder to the hex code
            hex_code += str(remainder)

    # Return the final structured hex code
    return hex_code            


# Examples                       | Outputs
# print(convert_to_binary(182))  | 10110110
# print(convert_to_hex(1820000)) | 1BC560
