import argparse
import getpass
from cryptography.fernet import InvalidToken
import logic

# Define the constant for the output file name
ENCRYPTED_KEY_FILENAME = "ft_otp.key"

def handle_generate_key(key_file_path):
    """Handles the -g flag: encrypts and stores a key."""
    try:
        with open(key_file_path, 'r') as f:
            hex_key = f.read().strip()

        if len(hex_key) < 64 or not all(c in '0123456789abcdefABCDEF' for c in hex_key):
            print("Error: Key must be at least 64 valid hexadecimal characters.")
            return

        password = getpass.getpass("Enter a password to encrypt the key: ")
        password_confirm = getpass.getpass("Confirm password: ")

        if password != password_confirm:
            print("Error: Passwords do not match.")
            return

        encrypted_key = logic.encrypt_data(hex_key.encode(), password)

        with open(ENCRYPTED_KEY_FILENAME, 'wb') as f:
            f.write(encrypted_key)
        
        print(f"Key was successfully saved in {ENCRYPTED_KEY_FILENAME}.")

    except FileNotFoundError:
        print(f"Error: The file '{key_file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def handle_get_password(encrypted_key_path):
    """Handles the -k flag: generates a one-time password."""
    try:
        with open(encrypted_key_path, 'rb') as f:
            encrypted_data = f.read()

        password = getpass.getpass("Enter password to decrypt the key: ")
        
        decrypted_key = logic.decrypt_data(encrypted_data, password)
        hex_key = decrypted_key.decode()
        
        one_time_password = logic.generate_totp(hex_key)
        print(one_time_password)

    except FileNotFoundError:
        print(f"Error: Encrypted key file '{encrypted_key_path}' not found.")
        print("Hint: Generate one first with the -g option.")
    except InvalidToken:
        print("Error: Invalid password or corrupted key file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    """Main function to parse arguments and run the program."""
    parser = argparse.ArgumentParser(
        description="ft_otp: A tool to generate Time-based One-Time Passwords.",
        epilog="Example usage: python3 ft_otp.py -g my_key.hex"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    
    group.add_argument("-g", "--generate", metavar="HEX_KEY_FILE",
                       help="Generate and store an encrypted key from a hexadecimal key file.")
    
    group.add_argument("-k", "--key", metavar="ENCRYPTED_KEY_FILE",
                       help="Generate a new password using an encrypted key file.")

    args = parser.parse_args()

    if args.generate:
        handle_generate_key(args.generate)
    elif args.key:
        handle_get_password(args.key)

if __name__ == "__main__":
    main()