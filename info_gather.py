import socket
import subprocess
from datetime import datetime

import GPUtil
import psutil
import wmi


class InfoGather:
    def __init__(self):
        # Initialize wmi object
        self.computer = wmi.WMI()
        self.system_info = self.computer.Win32_ComputerSystem()[0]
        self.os_info = self.computer.Win32_OperatingSystem()[0]

    def get_device_info(self):
        """Gets information about the system, such as the device name, processor, installed RAM, GPU, system type, and product ID (serial number).

        Returns:
        A dictionary containing the system information.
        """
        # Get the system information.
        proc_info = self.computer.Win32_Processor()[0]
        installed_ram = round(
            float(self.system_info.TotalPhysicalMemory) / 1024 / 1024 / 1024
        )
        gpu = self.computer.Win32_VideoController()[0]

        # Return the system information.
        return {
            "device_name": self.system_info.Name,
            "processor": proc_info.Name.strip(),
            "installed_ram": installed_ram,
            "gpu": gpu.Name,
            "system_type": self.system_info.SystemType,
            "product_id": self.os_info.SerialNumber,
        }

    def get_windows_info(self):
        """Returns the following information about the system:

        - Windows edition
        - Windows version
        - Installed date
        - OS build
        - Boot up time
        - Registered user

        Returns:
        A dictionary containing the system information.
        """

        # Get the system information from the Windows API.
        windows_edtion = self.os_info.Caption
        windows_version = self.os_info.Version
        build_number = self.os_info.BuildNumber

        get_installed_date = self.os_info.InstallDate
        installed_date_parsed_date = datetime.strptime(
            get_installed_date[:14], "%Y%m%d%H%M%S"
        )
        installed_date = installed_date_parsed_date.strftime("%Y/%m/%d")

        get_last_boot_up = self.os_info.LastBootUpTime
        last_boot_up_parsed_date = datetime.strptime(
            get_last_boot_up[:14], "%Y%m%d%H%M%S"
        )
        last_boot_up = last_boot_up_parsed_date.strftime("%Y/%m/%d, %H:%M:%S")

        registered_user = self.os_info.RegisteredUser

        # Convert the system information to a dictionary.
        system_info_dict = {
            "windows_edition": windows_edtion,
            "windows_version": windows_version,
            "installed_date": installed_date,
            "os_build": build_number,
            "boot_up_time": last_boot_up,
            "registered_user": registered_user,
        }

        # Return the system information dictionary.
        return system_info_dict

    def get_storage_info(self):
        """Gets storage information like:
        drive letter, total size and free size in GB.

        Returns:
        A dictionary containing the storage information.
        """

        # Get the storage information.
        storage_info = self.computer.Win32_LogicalDisk()

        # Create lists to store the storage information.
        drive = []
        free = []
        total = []

        # Iterate over the storage information.
        for storage in storage_info:
            # Get the drive letter.
            drive_letter = storage.DeviceID

            # Get the free size.
            free_size = round(int(storage.FreeSpace) / (1024**3))

            # Get the total size.
            total_size = round(int(storage.Size) / (1024**3))

            # Append the storage information to their lists.
            drive.append(drive_letter)
            free.append(free_size)
            total.append(total_size)

        # Add the storage information to the dictionary.
        storage_info_dict = {
            "drive_letter": drive,
            "free_size": free,
            "total_size": total,
        }

        # Return the storage information dictionary.
        return storage_info_dict

    def get_ip_address(self):
        """
        Returns:
        The IP address of the machine.
        """

        # Get the IP address.
        ip_address = socket.gethostbyname(socket.gethostname())

        # Return the IP address.
        return ip_address

    def get_network_bandwidth(self):
        """
        Get information about network bandwidth usage.

        Returns:
            dict: A dictionary containing sent and received bandwidth in megabytes (MB).
        """
        # Get network information using psutil
        network_info = psutil.net_io_counters()

        # Calculate sent and received bandwidth in megabytes (MB)
        sent_bandwidth_mb = network_info.bytes_sent / (1024**2)
        received_bandwidth_mb = network_info.bytes_recv / (1024**2)

        round_sent = round(sent_bandwidth_mb)
        round_received = round(received_bandwidth_mb)

        # Create a dictionary to store network bandwidth information
        network_bandwidth = {
            "sent_bandwidth": round_sent,
            "received_bandwidth": round_received,
        }

        return network_bandwidth

    def get_cpu_usage(self):
        """Gets the current CPU usage in percentage.

        Returns:
            int: The current CPU usage in percentage.
        """

        # Get the list of all CPU objects.

        cpu_info = self.computer.Win32_PerfFormattedData_PerfOS_Processor()

        # Get the first CPU object.

        total_cpu = cpu_info[0]

        # Get the idle percentage.

        idle_percentage = int(total_cpu.PercentIdleTime)

        # Calculate the CPU usage.

        cpu_usage = 100 - idle_percentage

        # Return the CPU usage.

        return cpu_usage

    def get_gpu_info(self):
        """Gets the current GPU temperature and utilization in percentage.

        Returns:
            tuple: A tuple containing the GPU temperature and utilization in percentage.
        """

        # Get the list of all GPU objects.

        gpu_info = GPUtil.getGPUs()

        # Get the first GPU object.

        gpu = gpu_info[0]

        # Get the GPU temperature.

        gpu_temperature = int(gpu.temperature)

        # Get the GPU utilization.

        output = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=utilization.gpu",
                "--format=csv,nounits,noheader",
            ]
        )
        gpu_utilization = int(output.decode("utf-8").strip())

        # Return the GPU temperature and utilization.

        return gpu_temperature, gpu_utilization

    def get_ram_info(self):
        """
        Get information about RAM utilization and capacity.

        Returns:
            dict: A dictionary containing RAM utilization, used RAM, and total RAM.
            RAM utilization is in percentage, while used RAM and total RAM are in GB.
        """
        # Get RAM information using psutil
        ram_info = psutil.virtual_memory()

        # Calculate RAM utilization percentage
        ram_utilization = ram_info.percent

        # Calculate used RAM in gigabytes
        used_ram_gb = ram_info.used / (1024**3)

        # Calculate total RAM in gigabytes
        total_ram_gb = ram_info.total / (1024**3)

        # Format used RAM and total RAM as strings with one decimal place
        formatted_used_ram = "{:.1f}".format(used_ram_gb)
        formatted_total_ram = "{:.1f}".format(total_ram_gb)

        # Create a list to store RAM information
        ram_info_list = [ram_utilization, formatted_used_ram, formatted_total_ram]

        return ram_info_list
