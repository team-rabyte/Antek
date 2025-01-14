from numpy import load

data = load("./camera_calibration_data.npz")
lst = data.files
# print((lst[0]))
### print("camera_matrix:\n", data["camera_matrix"])
### print("dist_coeffs:\n", data["dist_coeffs"])
# print(data["rvecs"])
# print(data["tvecs"])

# Start with an empty dictionary
camera_calibration_data = {}
# print(f"camera_calibration_data dictionary has been initialized. Empty.")
keys = lst[0:2]
# print(keys)
# print(data)

for key in keys:
    camera_calibration_data[key] = []
    for value in data[key]:
        camera_calibration_data[key] = data[key].tolist()
# print(camera_calibration_data.keys())
# print(camera_calibration_data)


"""
bluetooth_data = {}

# Add the first key with values
bluetooth_data["paired_devices"] = ["Device_A", "Device_B"]

# Add another key with values
bluetooth_data["active_connections"] = ["Device_B"]

# Add a new key and initialize it with an empty list
bluetooth_data["discovered_devices"] = []

# Add values to the "discovered_devices" key
bluetooth_data["discovered_devices"].extend(["Device_C", "Device_D", "Device_E"])

# Print the final dictionary
print(bluetooth_data)

"""
#####

"""
# CREATE DICTIONARY FROM DATA:
# Initial dictionary
bluetooth_data = {
    "paired_devices": ["Device_A", "Device_B"],
    "active_connections": ["Device_B"]
}

# Adding a new key to the dictionary
bluetooth_data["discovered_devices"] = []

# Adding values to the new key
bluetooth_data["discovered_devices"].extend(["Device_C", "Device_D", "Device_E"])

# Printing the updated dictionary
print(bluetooth_data)
"""

import yaml

# Define the data (if different in .npz file)
datayaml = {
    "camera_matrix": [
        [687.5265699, 0.0, 638.7820053],
        [0.0, 686.26066077, 339.70162761],
        [0.0, 0.0, 1.0],
    ],
    "dist_coeffs": [[-0.3032556, 0.10938661, 0.00044179, -0.00318095, -0.01873825]],
}

print(camera_calibration_data)
print("\n")
print(datayaml)
data = camera_calibration_data
# data = camera_calibration_data

# Save to a YAML file
output_file = "calibration.yaml"
with open(output_file, "w") as file:
    yaml.dump(data, file, default_flow_style=False)

print(f"Data has been saved to {output_file}")
