import csv


def read_csv_to_list(list):
    try:
        with open("./saves/results.csv", "r", newline="") as read_file:
            fieldnames = ["date", "bet", "result"]
            results_reader = csv.DictReader(read_file, fieldnames)
            for row in results_reader:
                list.append(row)
    except FileNotFoundError:
        return list
