import argparse, os
from key import generate_public_key, show_public_key, delete_public_key
def main():
    parser = argparse.ArgumentParser(description="Functions")
    parser.add_argument("command", choices=["create_key", "show_key", "delete_key"])
    args = parser.parse_args()


    if args.command == "create_key":
        generate_public_key()
    elif args.command == "show_key":
        show_public_key()
    elif args.command == "delete_key":
        delete_public_key()


if __name__ == "__main__":
    main()
