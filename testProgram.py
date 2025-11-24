import zmq
import json
import time

# run the server in one terminal instance and run the client in another

def runClient():
    # connecting to the server that the microservice is on:
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5014")

    # sample data
    sample = {"collection": 
              [
                  {"type": "picture", "date": "10-01-2025"}, 
                  {"type": "post", "date": "10-12-2025"}
                ], 
                "sort_by": "date_range", 
                "target_value": 
                    {
                        "start_date": "10-01-2025", 
                        "end_date": "10-10-2025"
                    }
            }

    # convert the sample object to a string
    sample_json = json.dumps(sample)

    # send the data to the microservice
    socket.send_string(sample_json)

    response = socket.recv()

    dec = (json.loads(response.decode()))["count"]

    print(f"Microservice says {dec} items fit the filter parameter!")

    context.destroy()

if __name__ == "__main__":
    runClient()