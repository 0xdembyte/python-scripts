# Process: Subnet mask -> 32 bit address -> count how many bits are active and turn it into a prefix -> /bits_active
def convert_to_binary(number):
    binary_number = ""
    current_bit   = 128
  
    for _ in range(8):
        if number >= current_bit:
            binary_number += "1"
            number -= current_bit
        else:
            binary_number += "0"
        current_bit //= 2
      
    return binary_number

def get_active_bits(subnet_mask):
    total_active_bits = 0

    for octet in subnet_mask.split("."):
        thirty_two_bit_address = convert_to_binary(int(octet))
        for bit in thirty_two_bit_address:
            total_active_bits += int(bit)
    
    return total_active_bits

def build_prefix_length(subnet_mask):
    total_active_bits = get_active_bits(subnet_mask)
    prefix_length = f"/{total_active_bits}"
    return prefix_length

subnet_mask = input("Subnet mask: ")
print(build_prefix_length(subnet_mask))

# Example
# Input: 255.255.255.0
# Binary: 11111111.11111111.11111111.00000000
# Active bits: 24
# Output: /24
