import argparse
import json
from datetime import datetime, timedelta, time
import sys
from utils import get_logger, is_overlap, read_reservations, TIME_FORMAT, create_readme

class TimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, time):
            return obj.strftime(TIME_FORMAT)
        return super().default(obj)

def parse_args():
    parser = argparse.ArgumentParser(description="Script for making a reservation")
    parser.add_argument("start_time", type=str, help="Start time of the reservation")
    parser.add_argument("committer", type=str, help="Start time of the reservation")
    parser.add_argument("players", type=str, help="List of players")
    
    return parser.parse_args()


def main():
    args = parse_args()
    logger = get_logger()
    reservations = read_reservations()

    start_time = ""
    try:
        start_time = datetime.strptime(args.start_time, TIME_FORMAT).time()
    except ValueError:
        logger.error("Invalid time format. Expected {}".format(TIME_FORMAT))
        sys.exit(1)

    delta = timedelta(minutes=30)
    end_time = (datetime.combine(datetime.min, start_time) + delta).time()

    logger.info("Attempting reservation for {} in time range: {} - {}".format(args.committer, start_time, end_time))

    if any([is_overlap((start_time, end_time), (reservation['start'], reservation['end'])) for reservation in reservations]):
        logger.error("Reservation overlap... try with a different time")
        sys.exit(1)

    reservations.append({
        'start': start_time,
        'end': end_time,
        'committer': args.committer,
        'players': args.players
    })
    reservation = sorted(reservations, key=lambda x: x['start'])
    with open("facts/reservations.json", "w") as f:
        json.dump(reservation, f, indent=4, cls=TimeEncoder)

    logger.info("Reservation successful")
    logger.info("Generating README.md")
    with open("README.md", "w") as f:
        f.write(create_readme(reservation))


if __name__ == "__main__":
    main()