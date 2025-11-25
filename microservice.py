import json
import zmq
from datetime import datetime


# for testing json formatting and accessing elements w/i the json; not used in final microservice
def test():
    my_str = (
        '{ "collection": [{"type": "picture", "date": "10-01-2025"}, '
        '{"type": "post", "date": "10-12-2025"}], "sort_by": "date", "target_value": {"start_date": "10-01-2025", "end_date": "10-10-2025"}}'
    )

    my_str_json = json.loads(my_str)

    print(my_str_json)

    collection = my_str_json["collection"]
    sort_by = my_str_json["sort_by"]
    target_value = my_str_json["target_value"]

    print(collection)
    print(sort_by)
    print(target_value)

    for c in collection:
        d = (c["date"]).split("-")

        print(c)

        if (
            d[0] == ((target_value["start_date"]).split("-"))[0]
            and d[1] == ((target_value["start_date"]).split("-"))[1]
            and d[2] == ((target_value["start_date"]).split("-"))[2]
        ):
            print("item is within date range!")
        else:
            print("not in date range...")


##### HELPER FUNCTIONS TO DO COUNTING #####


def count_all(collection):
    return len(collection)


def count_by_date(collection, start_date, end_date):
    """
    Helper function to count items in a collection within a specified time period.

    Start and end dates must be formatted as so: MM-DD-YYYY
    """
    start = datetime.strptime(start_date, "%m-%d-%Y")
    end = datetime.strptime(end_date, "%m-%d-%Y")
    count = 0
    for item in collection:
        try:
            date = datetime.strptime(item["date"], "%m-%d-%Y")
        except:
            continue # if date is missing or a different error occurs, skip item
        # datetime class allows the program to easily compare dates
        if start <= date <= end:
            count += 1
    return count


def count_by_tag(collection, target_tag):
    target_tag = target_tag.lower().strip()
    count = 0
    for item in collection:
        # tags are all contained in one string using commas as delimiters
        tags = [tag.strip().lower() for tag in item.get("tags", "").split(",")]
        if target_tag in tags:
            count += 1
    return count


def call(collection, sort_by, target_value):
    """
    Function that decides which helper to call depending on incoming JSON request.

    Args:
        collection (list[dict]): List of items to count.
        sort_by (str): Field to sort by before counting
        target_value: Additional args depending on sort field

    Returns:
        int: Number of items fitting sort filter
    """
    if sort_by == "all":
        return count_all(collection)
    elif sort_by == "date_range":
        return count_by_date(
            collection, target_value["start_date"], target_value["end_date"]
        )
    elif sort_by == "tag":
        return count_by_tag(collection, target_value)
    else:
        return count_all(collection)


def server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    # socket.bind("tcp://flip.engr.oregonstate.edu:5014")
    socket.bind("tcp://*:5014")

    while True:
        # receive and decode a request from the client
        message = socket.recv()

        full_msg = message.decode()

        # if asked to quit, break
        if full_msg == "Q":
            break

        # interpret the string as a json obj
        json_data = json.loads(full_msg)

        # grab the list of collection items
        collection = json_data.get("collection", [])

        sort_by = json_data.get("sort_by", "all")

        target_value = json_data.get("target_value", None)

        count = call(collection, sort_by, target_value)
        response = {"count": count}
        socket.send_string(json.dumps(response))

    context.destroy()
    socket.close()


# test()

if __name__ == "__main__":
    server()
