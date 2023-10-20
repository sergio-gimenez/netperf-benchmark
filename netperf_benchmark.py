import subprocess
import csv


def check_if_test_is_valid(test_type):
    if test_type == "TCP_STREAM":
        netperf_command = "netperf -t TCP_STREAM -l 10 -H <server_ip>"
    elif test_type == "TCP_RR":
        netperf_command = "netperf -t TCP_RR -l 10 -H <server_ip>"
    else:
        raise ValueError(f"Invalid test type: {test_type}")
    return netperf_command


def parse_netperf_output(output, test_type, csv_writer):
    lines = output.splitlines()
    if test_type == "TCP_STREAM":
        data = lines[-1].split()
        socket_size, elapsed_time, throughput = data[0], data[3], data[4]
        csv_writer.writerow([test_type, socket_size, "", "", elapsed_time, throughput])
    elif test_type == "TCP_RR":
        data = lines[-1].split()
        socket_size, request_size, response_size, elapsed_time, trans_rate = data[0], data[1], data[2], data[4], data[5]
        csv_writer.writerow([test_type, socket_size, request_size, response_size, elapsed_time, trans_rate])
    else:
        raise ValueError(f"Invalid test type: {test_type}")


def run_netperf_test(test_type, iterations, csv_filename):
    with open(csv_filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Test Type", "Socket Size", "Request Size", "Response Size", "Elapsed Time", "Throughput"])

        for _ in range(iterations):
            netperf_command = check_if_test_is_valid(test_type)
            output = subprocess.check_output(netperf_command, shell=True).decode('utf-8')
            parse_netperf_output(output, test_type, csv_writer)


if __name__ == "__main__":
    test_iterations = 10
    test_types = ["TCP_STREAM", "TCP_RR"]

    for test_type in test_types:
        csv_filename = f"{test_type}_results.csv"
        run_netperf_test(test_type, test_iterations, csv_filename)
        print(f"{test_type} tests completed. Results saved in {csv_filename}")
