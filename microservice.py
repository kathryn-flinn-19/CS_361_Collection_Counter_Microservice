import json
import zmq


# for testing json formatting and accessing elements w/i the json; not used in final microservice
def test():
    my_str = "{ \"collection\": [{\"type\": \"picture\", \"date\": \"10-01-2025\"}, " \
        "{\"type\": \"post\", \"date\": \"10-12-2025\"}], \"sort_by\": \"date\", \"target_value\": {\"start_date\": \"10-01-2025\", \"end_date\": \"10-10-2025\"}}"

    my_str_json = json.loads(my_str)

    print(my_str_json)

    collection = my_str_json['collection']
    sort_by = my_str_json['sort_by']
    target_value = my_str_json['target_value']

    print(collection)
    print(sort_by)
    print(target_value)    

    for c in collection:
        d = (c['date']).split("-")

        print(c)

        if d[0] == ((target_value['start_date']).split("-"))[0] and d[1] == ((target_value['start_date']).split("-"))[1] and d[2] == ((target_value['start_date']).split("-"))[2]:
            print("item is within date range!")
        else:
            print("not in date range...")


def server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    socket.bind("tcp://flip.engr.oregonstate.edu:5014")

    while True:
        # receive and decode a request from the client
        message = socket.recv()

        full_msg = message.decode()

        # if asked to quit, break
        if full_msg == 'Q':
            break

        # interpret the string as a json obj
        json_data = json.loads(full_msg)

        # grab the list of collection items
        collection = json_data['collection']

        sort_by = json_data['sort_by']

        target_value = json_data['target_value']

        # example json structure:
        '''
        data = { 
                "collection": 
                    [
                        {"type": "txt", "date": "date", "other info": "txt", . . . }, 
                        {"type": "txt", "date": "date", "other info": "txt", . . . },
                        {"type": "txt", "date": "date", "other info": "txt", . . . }
                    ],
                "sort_by": "field",
                "target_value": "val" 
        }
        
        '''

        # do some manipulation with the collection --- i.e. call a function w/ collection, 
        # sort_by, and target_value
        # ex: count = foo(collection, sort_by, target_value)
        count = 0       # EDIT THIS 

        socket.send_string(count)

    context.destroy()    

test()