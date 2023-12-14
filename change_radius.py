import subprocess
import matplotlib.pyplot as plt

file_path = "src/lorawan/examples/complete-network-example.cc"

# Define the range of nFlows to test-
n_radius_list = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000]
command_template = "./ns3 run '{file_path} --radius={radius}'"

expected = []
actual = []
lost = []
for radius in n_radius_list:
    command = command_template.format(file_path=file_path, radius=radius)
    print(command)
    output = subprocess.check_output(command, shell=True)
    output_lines = output.decode('utf-8').strip('\n').split(' ')
    print(output_lines)
    expected.append(float(output_lines[0]))
    actual.append(float(output_lines[1]))
    lost.append(float(output_lines[0]) - float(output_lines[1]))


# plot the expected and actual values

plt.plot(n_radius_list, expected, label="Sent")
plt.plot(n_radius_list, actual, label="Received")
plt.scatter(n_radius_list, expected)
plt.scatter(n_radius_list, actual)

plt.grid()
plt.xlabel("Radius")
plt.ylabel("Number of packets")
plt.legend()
plt.savefig("lost_packets_wrt_chnaging_radius.png")


print(lost)
