from utils import get_logger, create_readme, read_reservations
import argparse
import json

def parse_args():
    parser = argparse.ArgumentParser(description="Script for refreshing the status")
    parser.add_argument("--empty", dest="empty", help="Empty the reservations", default=False, action="store_true")

    return parser.parse_args()

def main():
    logger = get_logger()
    args = parse_args()
    logger.info("Running refreshing of status...")
    reservations = read_reservations()

    if args.empty:
        logger.info("Emptying reservations")
        reservations = []
        with open("facts/reservations.json", "w") as f:
            json.dump(reservations, f, indent=4)

    logger.info("Generating README.md")
    with open("README.md", "w") as f:
        f.write(create_readme(reservations))

if __name__ == "__main__":
    main()