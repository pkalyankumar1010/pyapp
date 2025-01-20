from cryptography.fernet import Fernet
import datetime

# Generate the secret key only once and save it to `license_key.key`
# Uncomment and run the following lines if you haven't generated the key already.
# key = Fernet.generate_key()
# with open("license_key.key", "wb") as key_file:
#     key_file.write(key)
# exit()
# Load the secret key


def load_secret_key():
    with open("license_key.key", "rb") as key_file:
        return key_file.read()


def generate_license(expiration_date):
    """
    Generate a license file with an expiration date.

    Args:
        expiration_date (str): Expiration date in "YYYY-MM-DD HH:MM" format.
                               If only "YYYY-MM-DD" is provided, defaults to "12:00".
    """
    # Parse expiration date and time
    try:
        if len(expiration_date.split()) == 1:
            expiration_date += " 12:00"  # Default to 12:00 PM if time is not provided
        expiration_datetime = datetime.datetime.strptime(
            expiration_date, "%Y-%m-%d %H:%M")
    except ValueError:
        print("Invalid date format! Use 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM'.")
        return

    # Encrypt the expiration date
    secret_key = load_secret_key()
    cipher = Fernet(secret_key)
    encrypted_date = cipher.encrypt(expiration_date.encode())

    # Save the license file
    with open("license.lic", "wb") as license_file:
        license_file.write(encrypted_date)

    print(f"License generated successfully! Valid until {expiration_date}")


# Example usage
if __name__ == "__main__":
    future_date = input(
        "Enter the expiration date (YYYY-MM-DD [HH:MM]): ").strip()
    generate_license(future_date)
