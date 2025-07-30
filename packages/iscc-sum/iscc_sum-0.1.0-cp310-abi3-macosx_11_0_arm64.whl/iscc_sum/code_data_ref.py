"""
ISO Reference Implementation of ISCC Data-Code

This module serves only as reference for correctness and performance of the actual Data-Code
implementation. The library does not use this code.
"""

import mmap
from base64 import b32encode
from io import BufferedReader, BytesIO
from math import log2
from typing import BinaryIO, Generator, List, Optional, Union

import xxhash

from iscc_sum.constants import (
    CDC_GEAR,  # List of 256 positive integers (max 31-bit)
    MPA,  # List of 64 positive integers (max 61-bit)
    MPB,  # List of 64 positive integers (max 61-bit)
)

__all__ = [
    "gen_data_code",
]

DATA_BITS = 64
DATA_IO_READ_SIZE = 2097152

DATA_MAINTYPE = "0011"  # Data-Code
DATA_SUBTYPE = "0000"  # None
DATA_VERSION = "0000"  # V0

MAXI64 = (1 << 64) - 1
MPRIME = (1 << 61) - 1
MAXH = (1 << 32) - 1

BIT_LEN_MAP = {
    32: "0000",
    64: "0001",
    96: "0010",
    128: "0011",
    160: "0100",
    192: "0101",
    224: "0110",
    256: "0111",
}

DATA_AVG_CHUNK_SIZE = 1024

Data = Union[bytes, bytearray, memoryview]
Stream = Union["BinaryIO", "mmap.mmap", "BytesIO", "BufferedReader"]


def gen_data_code(stream, bits=DATA_BITS):
    # type: (Stream, int) -> dict
    """
    Create an ISCC Data-Code with algorithm v0.

    :param stream: Input data stream (file-like object, mmap, BytesIO, or BufferedReader).
    :param bits: Bit-length of ISCC Data-Code (32, 64, 96, 128, 160, 192, 224, or 256).
    :return: Dictionary with 'iscc' key containing the ISCC Data-Code string.
    """

    hasher = DataHasher()
    data = stream.read(DATA_IO_READ_SIZE)

    while data:
        hasher.push(data)
        data = stream.read(DATA_IO_READ_SIZE)

    data_code = hasher.code(bits=bits)
    iscc = "ISCC:" + data_code
    return dict(iscc=iscc)


class DataHasher:
    """Incremental Data-Hash generator."""

    def __init__(self, data=None):
        # type: (Optional[Data]) -> None
        """
        Create a DataHasher for incremental Data-Code generation.

        :param data: Initial payload for hashing (bytes, bytearray, or memoryview).
        """
        self.chunk_features = []  # type: List[int]
        self.chunk_sizes = []  # type: List[int]
        self.tail = None  # type: Optional[bytes]
        data = data or b""
        self.push(data)

    def push(self, data):
        # type: (Data) -> None
        """
        Push data to the Data-Hash generator.

        Processes data using content-defined chunking and updates internal state.

        :param data: Data chunk to process (bytes, bytearray, or memoryview).
        """
        if self.tail:
            data = self.tail + data

        for chunk in alg_cdc_chunks(data, utf32=False, avg_chunk_size=DATA_AVG_CHUNK_SIZE):
            self.chunk_sizes.append(len(chunk))
            self.chunk_features.append(xxhash.xxh32_intdigest(chunk))
            self.tail = chunk  # Last chunk may not be final

        self.chunk_features = self.chunk_features[:-1]
        self.chunk_sizes = self.chunk_sizes[:-1]

    def digest(self):
        # type: () -> bytes
        """
        Calculate 256-bit minhash digest from accumulated chunk features.

        :return: 256-bit binary digest.
        """
        self._finalize()
        return alg_minhash_256(self.chunk_features)

    def code(self, bits=DATA_BITS):
        # type: (int) -> str
        """
        Encode digest as an ISCC Data-Code unit.

        :param bits: Number of bits for the ISCC Data-Code (32, 64, 96, 128, 160, 192, 224, or 256).
        :return: Base32-encoded ISCC Data-Code string with header.
        """
        length = BIT_LEN_MAP[bits]
        header = int(DATA_MAINTYPE + DATA_SUBTYPE + DATA_VERSION + length, 2).to_bytes(2, byteorder="big")
        data_code = encode_base32(header + self.digest()[: bits // 8])

        return data_code

    def _finalize(self):
        if self.tail is not None:
            self.chunk_features.append(xxhash.xxh32_intdigest(self.tail))
            self.chunk_sizes.append(len(self.tail))
            self.tail = None


def encode_base32(data):
    # type: (bytes) -> str
    """
    Standard RFC4648 base32 encoding without padding.

    :param data: Binary data to encode.
    :return: Base32-encoded string without padding characters.
    """
    return b32encode(data).decode("ascii").rstrip("=")


########################################################################################
# Content Defined Chunking (CDC)                                                       #
########################################################################################


def alg_cdc_chunks(data, utf32, avg_chunk_size=DATA_AVG_CHUNK_SIZE):
    # type: (Data, bool, int) -> Generator[bytes, None, None]
    """
    Generate content-defined chunks using a rolling hash algorithm.

    Usage Example:

    ```python
    for chunk in alg_cdc_chunks(data, utf32=False):
        hash(chunk)
    ```

    :param data: Raw data for variable-sized chunking (bytes, bytearray, or memoryview).
    :param utf32: If True, ensure chunk boundaries align to 4-byte UTF-32 boundaries.
    :param avg_chunk_size: Target average chunk size in bytes.
    :return: Generator yielding variable-sized data chunks.
    """

    stream = BytesIO(data)
    buffer = stream.read(DATA_IO_READ_SIZE)
    if not buffer:
        yield b""

    mi, ma, cs, mask_s, mask_l = alg_cdc_params(avg_chunk_size)

    buffer = memoryview(buffer)
    while buffer:
        if len(buffer) <= ma:
            buffer = memoryview(bytes(buffer) + stream.read(DATA_IO_READ_SIZE))
        cut_point = alg_cdc_offset(buffer, mi, ma, cs, mask_s, mask_l)

        # Make sure cut points are at 4-byte aligned for utf32 encoded text
        if utf32:
            cut_point -= cut_point % 4

        yield bytes(buffer[:cut_point])
        buffer = buffer[cut_point:]


def alg_cdc_params(avg_size: int) -> tuple:
    """
    Calculate content-defined chunking parameters.

    :param avg_size: Target average chunk size in bytes.
    :return: Tuple of (min_size, max_size, center_size, mask_s, mask_l).
    """

    def ceil_div(x, y):
        return (x + y - 1) // y

    def mask(b):
        return 2**b - 1

    min_size = avg_size // 4
    max_size = avg_size * 8
    offset = min_size + ceil_div(min_size, 2)
    center_size = avg_size - offset
    bits = round(log2(avg_size))
    mask_s = mask(bits + 1)
    mask_l = mask(bits - 1)
    return min_size, max_size, center_size, mask_s, mask_l


def alg_cdc_offset(buffer, mi, ma, cs, mask_s, mask_l):
    # type: (Data, int, int, int, int, int) -> int
    """
    Find chunk boundary offset using Gear-based rolling hash.

    :param buffer: Data buffer to analyze.
    :param mi: Minimum chunk size in bytes.
    :param ma: Maximum chunk size in bytes.
    :param cs: Center size threshold in bytes.
    :param mask_s: Small mask for early boundary detection.
    :param mask_l: Large mask for late boundary detection.
    :return: Offset of chunk boundary in bytes.
    """

    pattern = 0
    size = len(buffer)
    i = min(mi, size)
    barrier = min(cs, size)
    while i < barrier:
        pattern = (pattern >> 1) + CDC_GEAR[buffer[i]]
        if not pattern & mask_s:
            return i + 1
        i += 1
    barrier = min(ma, size)
    while i < barrier:
        pattern = (pattern >> 1) + CDC_GEAR[buffer[i]]
        if not pattern & mask_l:
            return i + 1
        i += 1
    return i


########################################################################################
# Minhash                                                                              #
########################################################################################


def alg_minhash_256(features):
    # type: (List[int]) -> bytes
    """
    Create 256-bit minhash digest from feature list.

    :param features: List of integer feature hashes.
    :return: 256-bit binary digest.
    """
    return alg_minhash_compress(alg_minhash(features), 4)


def alg_minhash(features):
    # type: (List[int]) -> List[int]
    """
    Calculate 64-dimensional minhash vector using universal hash functions.

    :param features: List of integer feature hashes.
    :return: List of 64 minimum hash values.
    """
    return [min([(((a * f + b) & MAXI64) % MPRIME) & MAXH for f in features]) for a, b in zip(MPA, MPB)]


def alg_minhash_compress(mhash, lsb=4):
    # type: (List[int], int) -> bytes
    """
    Compress minhash vector to binary digest.

    Concatenates `lsb` least-significant bits from each minhash value.
    Example: 64 values with lsb=4 produces 256-bit digest.

    :param mhash: List of minhash values.
    :param lsb: Number of least-significant bits per value.
    :return: Binary digest of compressed minhash.
    """
    bits: str = ""
    for bitpos in range(lsb):
        for h in mhash:
            bits += str(h >> bitpos & 1)
    return int(bits, 2).to_bytes((len(bits) + 7) // 8, "big")
