import argparse
import csv
import datetime

def is_within_date_range(date_str, start_date, end_date):
    try:
        date = datetime.strptime(date_str, '%m/%d/%Y') 
        return start_date <= date <= end_date
    except ValueError:
        return False 

def parse_file(input_file, start_date, end_date):
    complaints = {}
    with open(input_file) as csv_file:
        reader = csv.reader(csv_file)

        for row in reader:
            date_created = row[1]
            if is_within_date_range(date_created, start_date, end_date):
                complaint_type = row[5]
                borough = row[25]
                complaints[complaint_type][borough] += 1

    return complaints

def output_results(complaints, output_file=None):
    lines = ["complaint type,borough,count"]
    for complaint_type, boroughs in complaints.items():
        for borough, count in boroughs.items():
            lines.append(f"{complaint_type},{borough},{count}")
    
    output = "\n".join(lines)
    if output_file:
        with open(output_file, 'w') as file:
            file.write(output)
    else:
        print(output)


def main():
    parser = argparse.ArgumentParser(description="Count complaint types per borough for a given date range.")
    parser.add_argument('-i', required=True, help='the input file')
    parser.add_argument('-s', required=True, help='start date')
    parser.add_argument('-e', required=True, help='end date')
    parser.add_argument('-o', help = 'output file')
    args = parser.parse_args
    input = args.i
    start_date = args.s
    end_date = args.e
    output = args.o
    complaints = parse_file(input, start_date, end_date)
    output_results(complaints, output)

