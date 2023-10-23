import grpc
import sum_pb2
import sum_pb2_grpc
import struct
import sys
from time import perf_counter

# Check if the user provided the server IP and endpoint as command-line arguments
if len(sys.argv) < 4:
    print("Usage: python grpc-client.py <server_ip> <num_iterations> <endpoint>")
    sys.exit(1)

# Extract the server IP, number of iterations, and endpoint from command-line arguments
server_ip = sys.argv[1]
num_iterations = int(sys.argv[2])
endpoint = sys.argv[3]
img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()

# Open a gRPC channel to the specified server IP and port 50051
channel = grpc.insecure_channel(f'{server_ip}:50051')

if endpoint == 'add':
    stub = sum_pb2_grpc.addStub(channel)
    count = 1
    t1_start = perf_counter()
    while count <= num_iterations:
        number = sum_pb2.addMsg(a=5, b=10)
        response = stub.add(number)
        print(response.a)
        count = count + 1
    t1_stop = perf_counter()
    total_time = t1_stop - t1_start
    time_per_query = total_time / num_iterations
    print(time_per_query)
else:
    stub = sum_pb2_grpc.imageStub(channel)
    count = 1
    t1_start = perf_counter()
    while count <= num_iterations:
        number = sum_pb2.imageMsg(img=img)
        response = stub.image(number)
        print(response.a, response.b)
        count = count + 1
    t1_stop = perf_counter()
    total_time = t1_stop - t1_start
    time_per_query = total_time / num_iterations
    print(time_per_query)
