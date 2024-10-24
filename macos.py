from .. datasets import chipset_data
from .. import cpu_identifier
from .. import cpuid
from .. import device_locator
from .. import gpu_identifier
from .. import utils
import time
import re
import platform
import subprocess
import json

class MacOSHardwareInfo:
    def __init__(self):
        self.os_name = platform.system()

    def get_system_info(self):
        return {
            "OS": self.os_name,
            "Machine": platform.machine(),
            "Processor": self.get_cpu_info(),
            "System Version": self.get_system_version(),
            "Hardware Overview": self.get_hardware_overview(),
            "Network Info": self.get_network_info(),
            "PnP Devices": self.pnp_devices(),
            "Motherboard": self.motherboard(),
            "CPU": self.cpu(),
            "GPU": self.gpu(),
            "Monitor": self.monitor(),
            "Sound": self.sound(),
            "USB Controllers": self.usb_controllers(),
            "Input_Devices": hardware_info.input(),  # Added input_devices() method
            "Storage Controllers": self.storage_controllers(),
            "Biometric": self.biometric(),
            "Bluetooth": self.bluetooth(),
            "SD Controller": self.sd_controller(),
            "System Devices": self.system_devices()
        }

    def run_system_profiler(self, data_type):
        try:
            output = subprocess.check_output(['system_profiler', '-json', data_type]).decode()
            return json.loads(output)
        except subprocess.CalledProcessError as e:
            return f"Error retrieving {data_type}: {e}"

    def get_system_version(self):
        return platform.mac_ver()[0]

    def get_hardware_overview(self):
        return self.run_system_profiler('SPHardwareDataType')

    def get_cpu_info(self):
        return subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"]).strip().decode()

    def pnp_devices(self):
        try:
            # Using ioreg to list devices, with error handling for decoding issues
            device_info = subprocess.check_output(['ioreg', '-p', 'IOService', '-l']).decode('utf-8', errors='replace')
            return device_info
        except subprocess.CalledProcessError as e:
            return f"Error retrieving PnP device info: {e}"

    def motherboard(self):
        return self.get_hardware_overview()  # Logic board info

    def cpu(self):
        return self.get_cpu_info()

    def gpu(self):
        return self.run_system_profiler('SPDisplaysDataType')

    def monitor(self):
        return self.run_system_profiler('SPDisplaysDataType')

    def network(self):
        return self.run_system_profiler('SPNetworkDataType')

    def sound(self):
        return self.run_system_profiler('SPSoundDataType')

    def usb_controllers(self):
        return self.run_system_profiler('SPUSBDataType')

    def input_devices(self):
        # Input devices such as keyboards and mice
        return self.run_system_profiler('SPUSBDataType')  # Most input devices are USB-based

    def storage_controllers(self):
        return self.run_system_profiler('SPStorageDataType')

    def biometric(self):
        return self.run_system_profiler('SPiBridgeDataType')

    def bluetooth(self):
        return self.run_system_profiler('SPBluetoothDataType')

    def sd_controller(self):
        return self.run_system_profiler('SPCardReaderDataType')

    def system_devices(self):
        return subprocess.check_output(['ioreg', '-p', 'IOService']).decode()

# Example of usage
if __name__ == "__main__":
    mac_info = MacOSHardwareInfo()
    system_info = mac_info.get_system_info()
    print(json.dumps(system_info, indent=4))
