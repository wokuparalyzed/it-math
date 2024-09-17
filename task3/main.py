import argparse
import struct
import time

import numpy as np
from PIL import Image

# Constants for file format and header size
SVD_HEADER = b'SVDS'
HEADER_SIZE = 16
EPSILON = 1e-8

# Methods for SVD
METHOD_NUMPY = 'numpy'
METHOD_SIMPLE = 'simple'
METHOD_ADVANCED = 'advanced'


def compress_image(input_file: str, output_file: str, compression_factor: float, method: str) -> None:
    """Compress an image using the selected SVD method."""
    img = Image.open(input_file)
    height, width = img.height, img.width
    k = np.floor(height * width / (4 * compression_factor * (height + width + 1))).astype(np.int32)

    img_arrays = np.asarray(img)
    compressed_image_data = bytes()

    # Apply SVD compression based on the method selected
    for i in range(3):  # Loop through the 3 color channels (RGB)
        channel = img_arrays[..., i]
        if method == METHOD_NUMPY:
            compressed_image_data += numpy_svd(channel, k)
        elif method == METHOD_SIMPLE:
            compressed_image_data += simple_svd(channel, k, 50000)
        elif method == METHOD_ADVANCED:
            compressed_image_data += advanced_svd(channel, k, 1000)
        else:
            raise NotImplementedError('This method is not supported.')

    # Write the compressed data to a file with a custom header
    with open(output_file, 'wb') as f:
        header_data = SVD_HEADER + struct.pack('<III', height, width, k)
        f.write(header_data)
        f.write(compressed_image_data)


def numpy_svd(channel: np.ndarray, k: int) -> bytes:
    """Perform SVD compression using NumPy's implementation."""
    u, s, vt = np.linalg.svd(channel, full_matrices=False)
    data = np.concatenate((u[:, :k].ravel(), s[:k], vt[:k, :].ravel()))
    return data.astype(np.float32).tobytes()


def simple_svd(channel: np.ndarray, k: int, duration: int) -> bytes:
    """Perform SVD compression using a basic power iteration method."""
    h, w = channel.shape
    v = np.random.rand(w)
    v /= np.linalg.norm(v)
    u = np.zeros((h, k))
    s = np.zeros(k)
    vt = np.zeros((k, w))

    time_bound = time.time() * 1000 + duration
    for i in range(k):
        ata = np.dot(channel.T, channel)
        counter = 0
        while time.time() * 1000 < time_bound:
            v_new = np.dot(ata, v)
            v_new /= np.linalg.norm(v_new)
            counter += 1
            if counter % 10 == 0 and np.allclose(v_new, v, EPSILON):
                break
            v = v_new

        eigenvalue = np.dot(np.dot(ata, v), v.T)
        vt[i, :] = v
        u[:, i] = np.dot(channel, v) / eigenvalue
        s[i] = eigenvalue

        if counter == 0:
            break
        channel = channel - eigenvalue * np.outer(u[:, i], v)

    data = np.concatenate((u.ravel(), s, vt.ravel()))
    return data.astype(np.float32).tobytes()


def advanced_svd(channel: np.ndarray, k: int, duration: int) -> bytes:
    """Perform SVD compression using an advanced method."""
    height, width = channel.shape
    u = np.zeros((height, k))
    s = np.zeros(k)
    v = np.zeros((width, k))

    counter = 0
    time_bound = time.time() * 1000 + duration

    while time.time() * 1000 < time_bound:
        q, r = np.linalg.qr(np.dot(channel, v))
        u = q[:, :k]
        q, r = np.linalg.qr(np.dot(channel.T, u))
        v = q[:, :k]
        s = np.diag(r[:k, :k])
        counter += 1
        if counter % 10 == 0 and np.allclose(np.dot(channel, v), np.dot(u, r[:k, :k]), EPSILON):
            break

    data = np.concatenate((u.ravel(), s, v.T.ravel()))
    return data.astype(np.float32).tobytes()


def unpack_compressed_data(byte_data, n, m, k) -> np.ndarray:
    """Unpack the compressed data into SVD components and reconstruct the matrix."""
    split_data = [byte_data[i:i + 4] for i in range(0, len(byte_data), 4)]
    map_obj = map(lambda x: struct.unpack('<f', x), split_data)
    matrix_data = np.array(list(map_obj))
    u = matrix_data[: n * k].reshape(n, k)
    s = matrix_data[n * k: n * k + k].ravel()
    vt = matrix_data[n * k + k:].reshape(k, m)
    return np.dot(np.dot(u, np.diag(s)), vt)


def decompress_image(input_file: str, output_image_file: str) -> None:
    """Decompress an image from its SVD-compressed format."""
    with open(input_file, 'rb') as f:
        header_data = f.read(HEADER_SIZE)
        if header_data[:4] != SVD_HEADER:
            raise ValueError(f'Incorrect format of {input_file}')
        
        n, m, k = struct.unpack('<III', header_data[4:])

        arrays = [unpack_compressed_data(f.read(4 * k * (n + m + 1)), n, m, k) for _ in range(3)]
        image_matrix = np.stack(arrays, axis=2).clip(0, 255).astype(np.uint8)
        result_image = Image.fromarray(image_matrix)
        result_image.save(output_image_file)


def main():
    parser = argparse.ArgumentParser(description="Image Compression and Decompression using SVD")
    parser.add_argument('--mode', type=str, choices=['compress', 'decompress'], required=True, help="Mode: compress or decompress the image")
    parser.add_argument('--method', type=str, choices=['numpy', 'simple', 'advanced'], help="SVD method (for compression)")
    parser.add_argument('--input', type=str, required=True, help="Input image file path")
    parser.add_argument('--output', type=str, required=True, help="Output file path")
    parser.add_argument('--compression', type=float, help="Compression factor (required for compression)")

    args = parser.parse_args()

    if args.mode == 'compress':
        if not args.method or not args.compression:
            parser.error("Compression requires --method and --compression.")
        compress_image(args.input, args.output, args.compression, args.method)
    elif args.mode == 'decompress':
        decompress_image(args.input, args.output)


if __name__ == "__main__":
    main()