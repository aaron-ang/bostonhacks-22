import csv
 
def getEventList():
    # replace path
    PATH = "./data.csv"
 
    with open(PATH, 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        list_of_events = list(csv_reader)
 
    return list_of_events[1:]