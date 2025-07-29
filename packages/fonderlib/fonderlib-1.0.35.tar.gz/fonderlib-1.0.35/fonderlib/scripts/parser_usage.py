# test_parser.py

from fonderlib.common.parser import CustomParser


def main():
    parser = CustomParser(description="Test CLI parser usage")

    # Add arguments dynamically
    parser.add_argument("--name", type=str, required=True, help_text="Your full name")
    parser.add_argument("--age", type=int, required=False, help_text="Your age")
    parser.add_argument(
        "--active", type=bool, required=False, help_text="Active status"
    )

    args = parser.parse()

    # Print results
    print("Parsed arguments:")
    print(f"Name: {args.name}")
    print(f"Age: {args.age}")
    print(f"Active: {args.active}")


if __name__ == "__main__":
    main()
