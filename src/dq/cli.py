import argparse

def main():
    parser = argparse.ArgumentParser(description="DQ Lite")
    parser.add_argument("--name", help="Enter your name")
    args = parser.parse_args()
    print(f"Hello, {args.name}!")

if __name__ == "__main__":
    main()