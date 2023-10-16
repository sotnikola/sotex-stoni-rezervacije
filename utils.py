import logging
import json
from datetime import datetime
import subprocess

TIME_FORMAT = "%H:%M"

def get_logger():
    FORMAT = '[%(asctime)s] %(levelname)-8s %(message)s'
    logging.basicConfig(format=FORMAT,level=logging.INFO)
    return logging.getLogger("reserver")

def is_overlap(range1, range2):
    return (range1[0] < range2[1] and range1[1] > range2[0])

def read_reservations(): 
    with open("facts/reservations.json", "r") as f:
        reservations = json.load(f)
        reservations = [{
            'start': datetime.strptime(reservation['start'], TIME_FORMAT).time(),
            'end': datetime.strptime(reservation['end'], TIME_FORMAT).time(),
            'committer': reservation['committer'],
            'players': reservation['players']
        } for reservation in reservations]
        return reservations


def get_entry(reservation):
    return f"""
        <tr>
            <td>{reservation['start']}</td>
            <td>{reservation['end']}</td>
            <td>{reservation['committer']}</td>
            <td>{reservation['players']}</td>
        </tr>
""".strip()

def create_readme(reservations):
    current_time = datetime.now().time()
    currently_occupied = any([is_overlap((reservation['start'], reservation['end']), (current_time, current_time)) for reservation in reservations])
    return f"""
<h1>Stoni tenis SOTEX rezervacije</h1>

{get_cross() if currently_occupied else get_checkmark()}

<table>
    <thead>
        <th>Početak</th>
        <th>Kraj</th>
        <th>Commiter</th>
        <th>Igrači</th>
    </thead>
    <tbody>{"".join([get_entry(reservation) for reservation in reservations])}</tbody>
</table>
<h3>Poslednji put osveženo: {current_time.strftime(TIME_FORMAT)}</h3>
"""

def get_checkmark():
    return """<img src="assets/checkmark.png" height="48px" />"""

def get_cross():
    return """<img src="assets/cross.png" height="48px" />"""

