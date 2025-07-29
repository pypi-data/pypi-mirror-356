from typing import Union

CHARSET = "ACEFHKLMNPRTWXYadeghknrtwxy34679"
CHARSET_INDEX = {c: i for i, c in enumerate(CHARSET)}


def encode(data: bytes) -> str:
    """
    Encode bytes to eBase32 string.
    :param data: Bytes to encode
    :return: eBase32 string
    """
    bits = 0
    bit_buffer = 0
    encoded = []

    for byte in data:
        bit_buffer = (bit_buffer << 8) | byte
        bits += 8

        while bits >= 5:
            bits -= 5
            index = (bit_buffer >> bits) & 0b11111
            encoded.append(CHARSET[index])

    if bits > 0:
        index = (bit_buffer << (5 - bits)) & 0b11111
        encoded.append(CHARSET[index])

    return ''.join(encoded)


def decode(encoded: str) -> bytes:
    """
    Decode eBase32 string to bytes.
    :param encoded: eBase32 string
    :return: Original bytes
    """
    bits = 0
    bit_buffer = 0
    decoded = bytearray()

    for char in encoded:
        if char not in CHARSET_INDEX:
            raise ValueError(f"Invalid character in input: '{char}'")
        bit_buffer = (bit_buffer << 5) | CHARSET_INDEX[char]
        bits += 5

        if bits >= 8:
            bits -= 8
            decoded.append((bit_buffer >> bits) & 0xFF)

    return bytes(decoded)


class EBase32:
    CHARSET = CHARSET
    CHARSET_INDEX = CHARSET_INDEX

    def __init__(self, value: Union[bytes, str]):
        if isinstance(value, bytes):
            self._bytes = value
            self._encoded = encode(value)
        elif isinstance(value, str):
            self._encoded = value
            self._bytes = decode(value)
        else:
            raise TypeError("EBase32 must be initialized with bytes or str")

    @staticmethod
    def encode(data: bytes) -> str:
        return encode(data)

    @staticmethod
    def decode(encoded: str) -> bytes:
        return decode(encoded)

    @property
    def bytes(self) -> bytes:
        return self._bytes

    @property
    def string(self) -> str:
        return self._encoded

    def __str__(self) -> str:
        return self._encoded

    def __bytes__(self) -> bytes:
        return self._bytes

    def __eq__(self, other) -> bool:
        if isinstance(other, EBase32):
            return self._bytes == other._bytes
        if isinstance(other, bytes):
            return self._bytes == other
        if isinstance(other, str):
            return self._encoded == other
        return NotImplemented
