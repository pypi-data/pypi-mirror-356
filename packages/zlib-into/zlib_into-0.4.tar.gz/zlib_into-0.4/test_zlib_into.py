# Copyright (C) European XFEL GmbH Schenefeld. All rights reserved.
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import zlib

import numpy as np
import pytest

from zlib_into import compress_into, decompress_into, shuffle, unshuffle


def test_compress_into():
    buf_size = 5000
    data_in = b"abcde" * 5000
    buf = bytearray(buf_size)
    n_bytes_out = compress_into(data_in, buf)

    assert isinstance(n_bytes_out, int)
    assert 0 < n_bytes_out < buf_size

    # Remaining space in buffer should not have been touched
    assert bytes(buf[n_bytes_out:]) == b"\0" * (buf_size - n_bytes_out)

    # Roundtrip
    assert zlib.decompress(buf[:n_bytes_out]) == data_in


def test_compress_into_err():
    buf_size = 5000
    data_in = b"abcde" * 5000
    buf = bytearray(5000)
    with pytest.raises(BufferError):
        compress_into(memoryview(data_in)[::2], buf)  # Input not contiguous

    with pytest.raises(TypeError):
        compress_into(data_in, memoryview(buf).toreadonly())  # Output not writable

    with pytest.raises(ValueError):
        compress_into(data_in, buf[:10])  # Output too small


def test_decompress_into():
    expanded_data = b"abcde" * 5000
    compressed_data = zlib.compress(expanded_data)
    buf = bytearray(len(expanded_data) + 10)

    n_bytes_out = decompress_into(compressed_data, buf)

    assert isinstance(n_bytes_out, int)
    assert n_bytes_out == len(expanded_data)
    assert buf[:n_bytes_out] == expanded_data

    # Remaining space in buffer should not have been touched
    assert bytes(buf[n_bytes_out:]) == b"\0" * (len(buf) - n_bytes_out)

    # Exactly the right amount of space
    buf2 = bytearray(len(expanded_data))
    assert decompress_into(compressed_data, buf2) == len(expanded_data)

    # Not enough space, by 1 byte
    buf3 = bytearray(len(expanded_data) - 1)
    with pytest.raises(ValueError):
        decompress_into(compressed_data, buf3)

    # Corner case: decompress 0 bytes
    compressed_nothing = zlib.compress(b"")
    buf_size_0 = bytearray(0)
    n_bytes_out = decompress_into(compressed_nothing, buf_size_0)
    assert n_bytes_out == 0


def test_decompress_into_err():
    expanded_data = b"abcde" * 5000
    compressed_data = zlib.compress(expanded_data)
    buf = bytearray(len(expanded_data) + 10)

    with pytest.raises(BufferError):
        decompress_into(memoryview(compressed_data)[::2], buf)  # Input not contiguous

    with pytest.raises(TypeError):  # Output not writable
        decompress_into(compressed_data, memoryview(buf).toreadonly())


@pytest.mark.parametrize("dtype", [np.uint16, np.float32, np.int64])
def test_unshuffle(dtype):
    orig = np.arange(65_536, dtype=dtype)
    shuffled = np.ascontiguousarray(
        orig.view(np.uint8).reshape(-1, orig.itemsize).transpose()
    )

    out = np.zeros_like(orig)
    unshuffle(shuffled, out, itemsize=orig.itemsize)
    np.testing.assert_array_equal(out, orig)


def test_unshuffle_err():
    data = b"aaabbbcccddd"
    out = bytearray(12)
    unshuffle(data, out, 4)
    assert bytes(out) == b"abcd" * 3

    with pytest.raises(BufferError):
        unshuffle(memoryview(data)[::2], out, 4)  # Input not contiguous

    with pytest.raises(TypeError):  # Output not writable
        unshuffle(data, memoryview(out).toreadonly(), 4)

    with pytest.raises(ValueError):  # Size not a multiple of 4
        unshuffle(data[:10], out[:10], 4)

    with pytest.raises(ValueError):  # Sizes don't match
        unshuffle(data, out[:8], 4)


@pytest.mark.parametrize("dtype", [np.uint16, np.float32, np.int64])
def test_shuffle(dtype):
    orig = np.arange(16 * 1024, dtype=dtype)
    shuffled = bytearray(orig.size * orig.itemsize)
    shuffle(orig, shuffled, itemsize=orig.itemsize)

    unshuffled = np.ascontiguousarray(
        np.frombuffer(shuffled, np.uint8).reshape(orig.itemsize, -1).transpose()
    ).reshape(-1).view(dtype)
    np.testing.assert_array_equal(unshuffled, orig)


def test_shuffle_err():
    data = b"abcd" * 3
    out = bytearray(12)
    shuffle(data, out, 4)
    assert bytes(out) == b"aaabbbcccddd"

    with pytest.raises(BufferError):
        shuffle(memoryview(data)[::2], out, 4)  # Input not contiguous

    with pytest.raises(TypeError):  # Output not writable
        shuffle(data, memoryview(out).toreadonly(), 4)

    with pytest.raises(ValueError):  # Size not a multiple of 4
        shuffle(data[:10], out[:10], 4)

    with pytest.raises(ValueError):  # Sizes don't match
        shuffle(data, out[:8], 4)
