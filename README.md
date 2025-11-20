# ft_otp: Time-based One-Time Password Tool

`ft_otp` is a command-line tool written in Python that implements a Time-based One-Time Password (TOTP) system, compliant with RFC 6238. It allows for the secure storage of a secret key and the generation of 6-digit one-time passwords that are compatible with standard authenticator applications.

## Features

-   **Secure Key Storage**: Encrypts and stores your hexadecimal secret key in a local file (`ft_otp.key`) using strong, password-based encryption (PBKDF2 and Fernet).
-   **TOTP Generation**: Generates standard 6-digit one-time passwords that are valid for 30-second intervals.
-   **Password Protection**: Prompts for a user-defined password to encrypt the secret key and requires the same password for decryption, ensuring the key is never stored in plain text.
-   **RFC Compliant**: Implements the core logic of HOTP (RFC 4226) with a time-based moving factor (RFC 6238).

## Prerequisites

-   Python 3.6+
-   pip (Python package installer)

## Installation

1.  **Clone the repository or download the project files:**
    ```bash
    git clone https://github.com/ACH4Q/ft_otp
    cd ft_otp
    ```

2.  **Install the required Python libraries:**
    The project relies on the `cryptography` library for secure key handling.
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The program has two main modes of operation: generating a secure key store (`-g`) and generating a one-time password (`-k`).

### Step 1: Create a Hexadecimal Secret Key

First, you need a secret key to share between `ft_otp` and your authenticator app. The key must be a hexadecimal string of at least 64 characters.

You can generate a secure one with `openssl`:
```bash
openssl rand -hex 32 > my_secret.hex
```
This command creates a file named `my_secret.hex` containing a 64-character hex key.

### Step 2: Encrypt and Store the Key (`-g`)

Use the `-g` flag to encrypt the key from your `.hex` file and store it securely. You will be prompted to create a password to protect this file.

```bash
python3 ft_otp.py -g my_secret.hex
```

**Example Interaction:**
```
$ python3 ft_otp.py -g my_secret.hex
Enter a password to encrypt the key: 
Confirm password: 
Key was successfully saved in ft_otp.key.
```
This will create an encrypted file named `ft_otp.key`. You can now safely delete the original `my_secret.hex` file.

### Step 3: Generate a One-Time Password (`-k`)

Use the `-k` flag followed by the path to your encrypted key file to generate a TOTP. You will be prompted for the password you created in the previous step.

```bash
python3 ft_otp.py -k ft_otp.key
```

**Example Interaction:**
```
$ python3 ft_otp.py -k ft_otp.key
Enter password to decrypt the key: 
836492
```
The program will output a 6-digit code that changes every 30 seconds.

## How It Works

The program follows the standard TOTP algorithm:
1.  **Key Derivation**: When storing the key, a master password is used with a random salt and the PBKDF2 algorithm to derive a strong encryption key.
2.  **Encryption**: The derived key is used with the Fernet symmetric encryption scheme to encrypt and save the hexadecimal secret.
3.  **TOTP Calculation**:
    - The current Unix time is divided by 30 to get a unique time-step counter.
    - An HMAC-SHA1 hash is computed using the decrypted secret key and the time-step counter.
    - A dynamic truncation process (as defined in RFC 4226) is used to extract a 4-byte value from the hash.
    - This value is converted to an integer, and the last 6 digits are returned as the final OTP.

## Project Structure

```
.
├── ft_otp.py             # Main executable: handles arguments and user I/O
├── otp_logic.py          # Core module: contains encryption and TOTP algorithms
└── requirements.txt      # Project dependencies
``` 