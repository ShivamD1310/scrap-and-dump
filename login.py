import os

def main():
    # Fetch the credentials from environment variables
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    # Print the credentials for debugging purposes
    print(f"USERNAME: {username}")
    print(f"PASSWORD: {password}")

if __name__ == "__main__":
    main()
