import subprocess
import matplotlib.pyplot as plt

file_path = "src/lorawan/examples/complete-network-example.cc"

# Define the range of nFlows to test-
n_devices_list = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000]
realistic_channel_model =  False
command_template = "./ns3 run '{file_path} --nDevices={n_devices} --realisticChannelModel={realistic_channel_model}'"

expected = []
actual = []
actual_realistic = []
lost = []
for n_devices in n_devices_list:
    realistic_channel_model = False
    command = command_template.format(file_path=file_path, n_devices=n_devices, realistic_channel_model=realistic_channel_model)
    print(command)
    output = subprocess.check_output(command, shell=True)
    output_lines = output.decode('utf-8').strip('\n').split(' ')

    expected.append(float(output_lines[0]))
    actual.append(float(output_lines[1]))
    lost.append(float(output_lines[0]) - float(output_lines[1]))

    realistic_channel_model = True
    command = command_template.format(file_path=file_path, n_devices=n_devices, realistic_channel_model=realistic_channel_model)
    print(command)
    output = subprocess.check_output(command, shell=True)
    output_lines = output.decode('utf-8').strip('\n').split(' ')
    actual_realistic.append(float(output_lines[1]))


# plot the expected and actual values

plt.plot(n_devices_list, expected, label="Sent")
plt.plot(n_devices_list, actual, label="Received")
plt.plot(n_devices_list, actual_realistic, label="Received Realistic")
plt.scatter(n_devices_list, expected)
plt.scatter(n_devices_list, actual)
plt.scatter(n_devices_list, actual_realistic)

plt.grid()
plt.xlabel("Number of devices")
plt.ylabel("Number of packets")
plt.legend()
plt.savefig("lost_packets_wrt_chnaging_ndevices_realistic.png")




