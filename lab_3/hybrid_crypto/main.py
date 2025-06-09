import argparse
import sys

from rsa_operations import (
    generate_rsa_keys,
    serialize_rsa_keys,
    encrypt_symmetric_key_rsa,
    decrypt_symmetric_key_rsa,
    load_rsa_private_key,
    load_rsa_public_key
)
from idea_operations import (
    generate_idea_key,
    encrypt_idea_cbc,
    decrypt_idea_cbc,
    IDEA_BLOCK_SIZE_BYTES,
)
from work_file import read_file, write_file


def handle_key_generation(args):
    """Handles the RSA key generation command."""
    print("🏁 Starting RSA key generation mode...")
    priv_key, pub_key = generate_rsa_keys()
    serialize_rsa_keys(pub_key, priv_key, args.public_key_out, args.private_key_out)
    print(f"\n✅ RSA keys successfully generated and saved to:")
    print(f"   Public key: {args.public_key_out}")
    print(f"   Private key: {args.private_key_out}")


def handle_encryption(args):
    """Handles the file encryption command."""
    print("🏁 Starting file encryption mode...")
    
    idea_key = generate_idea_key()
    public_key = load_rsa_public_key(args.public_key_in)
    encrypt_symmetric_key_rsa(idea_key, public_key, args.sym_key_out)

    print(f"Reading file to encrypt: {args.input_file}")
    plaintext = read_file(args.input_file, is_binary=True)
    if plaintext is None:
        raise ValueError("Failed to read the input file.")

    iv, ciphertext = encrypt_idea_cbc(plaintext, idea_key)
    write_file(args.output_file, iv + ciphertext)
    
    print(f"\n✅ File successfully encrypted.")
    print(f"   Result saved to: {args.output_file}")
    print(f"   Encrypted IDEA key saved to: {args.sym_key_out}")


def handle_decryption(args):
    """Handles the file decryption command."""
    print("🏁 Starting file decryption mode...")

    private_key = load_rsa_private_key(args.private_key_in)
    idea_key = decrypt_symmetric_key_rsa(args.sym_key_in, private_key)
    if idea_key is None:
        raise ValueError("Failed to decrypt the symmetric key.")
    
    print(f"Reading encrypted file: {args.input_file}")
    encrypted_data = read_file(args.input_file, is_binary=True)
    if encrypted_data is None:
        raise ValueError("Failed to read the input file.")

    iv = encrypted_data[:IDEA_BLOCK_SIZE_BYTES]
    ciphertext = encrypted_data[IDEA_BLOCK_SIZE_BYTES:]
    
    plaintext = decrypt_idea_cbc(ciphertext, idea_key, iv)
    if plaintext is None:
        raise ValueError("Failed to decrypt the file data.")

    write_file(args.output_file, plaintext)
    
    print(f"\n✅ File successfully decrypted.")
    print(f"   Result saved to: {args.output_file}")


def main():
    """Main function to parse arguments and run modes."""
    parser = argparse.ArgumentParser(description="A hybrid encryption system using RSA and IDEA.")
    
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    parser_gen = subparsers.add_parser("gen", help="Generate a new RSA key pair.")
    parser_gen.add_argument('--public_key_out', default='keys/public_key.pem', help="Path to save the public key.")
    parser_gen.add_argument('--private_key_out', default='keys/private_key.pem', help="Path to save the private key.")

    parser_enc = subparsers.add_parser("enc", help="Encrypt a file.")
    parser_enc.add_argument('--input_file', required=True, help="Input file to encrypt.")
    parser_enc.add_argument('--output_file', required=True, help="Output file to save the ciphertext.")
    parser_enc.add_argument('--public_key_in', required=True, help="Recipient's public RSA key.")
    parser_enc.add_argument('--sym_key_out', required=True, help="File to save the encrypted symmetric key.")

    parser_dec = subparsers.add_parser("dec", help="Decrypt a file.")
    parser_dec.add_argument('--input_file', required=True, help="Input file to decrypt.")
    parser_dec.add_argument('--output_file', required=True, help="Output file to save the decrypted text.")
    parser_dec.add_argument('--private_key_in', required=True, help="Your private RSA key.")
    parser_dec.add_argument('--sym_key_in', required=True, help="File with the encrypted symmetric key.")

    args = parser.parse_args()
    
    try:
        if args.command == "gen":
            handle_key_generation(args)
        elif args.command == "enc":
            handle_encryption(args)
        elif args.command == "dec":
            handle_decryption(args)
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()