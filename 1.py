import struct

# Convert a float to IEEE754 bytes
def float_to_ieee754(data):
    ieee754_bytes = struct.pack('f', data)
    return list(ieee754_bytes)

# Convert IEEE754 bytes to a float
def ieee754_to_float(ieee754_bytes):
    ieee754_data = bytes(ieee754_bytes)
    ieee754_float = struct.unpack('f', ieee754_data)[0]
    return ieee754_float

# Example usage:
original_float = 12.34
print("Original Float:", original_float)

# Convert the float to IEEE754 bytes
ieee754_bytes = float_to_ieee754(original_float)
print("IEEE754 Bytes:", ieee754_bytes)

# Convert the IEEE754 bytes back to a float
reconstructed_float = ieee754_to_float(ieee754_bytes)
print("Reconstructed Float:", reconstructed_float)
