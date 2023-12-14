import subprocess
import matplotlib.pyplot as plt

file_path = "src/lorawan/examples/complete-network-example.cc"

# Define the range of nFlows to test-
gamma_list = [1.5, 2, 2.5, 3, 3.5, 3.76, 4, 4.5, 5.0]
n_devices_list = [500, 1000, 1500, 2000]
# todo change the ndevices in the file
command_template = "./ns3 run '{file_path} --nDevices={n_devices} --gamma={gamma}'"

all_expected = []
all_actual = []
all_lost = []

for n_devices in n_devices_list:
    expected = []
    actual = []
    lost = []
    for gamma in gamma_list:
        command = command_template.format(file_path=file_path, n_devices=n_devices, gamma=gamma)
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
    plt.plot(gamma_list, all_expected[i], label="Sent nDevices={}".format(n_devices_list[i]))
    plt.plot(gamma_list, all_actual[i])
    plt.scatter(gamma_list, all_expected[i])
    plt.scatter(gamma_list, all_actual[i])

plt.grid()
plt.xlabel("Path exponents (gamma)")
plt.ylabel("Number of packets")
plt.legend()

plt.savefig("lost_packets_wrt_chnaging_gamma.png")


