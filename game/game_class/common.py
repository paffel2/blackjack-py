import csv
import sys
import os


def read_csv_to_list(list) -> list[dict[str, str, str]]:
    try:
        with open("./saves/results.csv", "r", newline="") as read_file:
            fieldnames = ["date", "bet", "result"]
            results_reader = csv.DictReader(read_file, fieldnames)
            for row in results_reader:
                list.append(row)
    except FileNotFoundError:
        return list


def resource_path(relative: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)
