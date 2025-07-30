import argparse
from autoscrap.core import get_text, extract_table


def main():
    parser = argparse.ArgumentParser(description='AutoScrap: Simple Web Scraping Automation')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # get_text command
    parser_text = subparsers.add_parser('get_text', help='Extract text from a specific HTML tag')
    parser_text.add_argument('url', help='URL of the web page')
    parser_text.add_argument('tag', help='HTML tag to extract text from')

    # extract_table command
    parser_table = subparsers.add_parser('extract_table', help='Extract the first table from a web page')
    parser_table.add_argument('url', help='URL of the web page')
    parser_table.add_argument('--as-dataframe', action='store_true', help='Output as pandas DataFrame (requires pandas)')

    args = parser.parse_args()

    if args.command == 'get_text':
        results = get_text(args.url, args.tag)
        for i, text in enumerate(results, 1):
            print(f"[{i}] {text}")
    elif args.command == 'extract_table':
        table = extract_table(args.url, as_dataframe=args.as_dataframe)
        if table is None:
            print("No table found or error occurred.")
        elif args.as_dataframe:
            print(table)
        else:
            for row in table:
                print("\t".join(row))

if __name__ == '__main__':
    main() 