import subprocess
import matplotlib.pyplot as plt

file_path = "src/lorawan/examples/complete-network-example.cc"

# Define the range of nFlows to test-
packet_size_list = [25, 50, 75, 100, 125, 150, 175, 200]
n_devices_list = [500, 2000]
# todo change the ndevices in the file
command_template = "./ns3 run '{file_path} --nDevices={n_devices} --packetSize={packet_size}'"

all_expected = []
all_actual = []
all_lost = []

for n_devices in n_devices_list:
    expected = []
    actual = []
    lost = []
    for packet_size in packet_size_list:
        command = command_template.format(file_path=file_path, n_devices=n_devices, packet_size=packet_size)
        print(command)
        output = subprocess.check_output(command, shell=True)
        output_lines = output.decode('utf-8').strip('\n').split(' ')

        expected.append(float(output_lines[0]))
        actual.append(float(output_lines[1]))
        lost.append(float(output_lines[0]) - float(output_lines[1]))
    all_actual.append(actual)
    all_expected.append(expected)
    all_lost.append(lost)


# plot the expected and actual values for each n_devices in the same plot
for i in range(len(n_devices_list)):
    plt.plot(packet_size_list, all_expected[i], label="Sent nDevices={}".format(n_devices_list[i]))
    plt.plot(packet_size_list, all_actual[i])
    plt.scatter(packet_size_list, all_expected[i])
    plt.scatter(packet_size_list, all_actual[i])

plt.grid()
plt.xlabel("Packet size")
plt.ylabel("Number of packets")
plt.legend()

plt.savefig("lost_packets_wrt_chnaging_packet_size.png")

