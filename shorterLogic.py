# This file is used to provide new shorter URL based on what the user post on our website
# We're using Base-62 encoding because it is more compact

CHARACTERS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE = len(CHARACTERS)

def encode_base62(num:int) -> str:
    # Convert a positive integer to a Base-62 string
    if num == 0:
        return CHARACTERS[0]
    
    result = []
    while num > 0:
        remainder = num % BASE
        result.append(CHARACTERS[remainder])
        num = num // BASE
    
    # THe result list contains the characters in reverse order (eg. if we read number by 123, the result will be 321)
    # That's why we need to reverse the result to get the correct order
    return "".join(reversed(result))