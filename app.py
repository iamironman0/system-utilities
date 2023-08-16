import queue
import threading
import webbrowser

import customtkinter as ctk
from PIL import Image

from info_gather import InfoGather

# Fonts
FONT_20_BOLD = ("Helvetica", 20, "bold")
FONT_16_BOLD = ("Helvetica", 16, "bold")
FONT_16 = ("Helvetica", 16)
FONT_14_BOLD = ("Helvetica", 14, "bold")
FONT_14 = ("Helvetica", 14)

# Logo
APP_LOGO = "./icons/logo.ico"

# Icons
NAV_LOGO = ctk.CTkImage(
    light_image=Image.open("./icons/logo_light.png"),
    dark_image=Image.open("./icons/logo_dark.png"),
    size=(35, 35),
)
THEME_ICON = ctk.CTkImage(
    light_image=Image.open("./icons/theme_light.png"),
    dark_image=Image.open("./icons/theme_dark.png"),
    size=(25, 25),
)
HOME_ICON = ctk.CTkImage(
    light_image=Image.open("./icons/logo_light.png"),
    dark_image=Image.open("./icons/logo_dark.png"),
    size=(20, 20),
)
SYS_MONITOR_ICON = ctk.CTkImage(
    light_image=Image.open("./icons/sys_monitor_light.png"),
    dark_image=Image.open("./icons/sys_monitor_dark.png"),
    size=(20, 20),
)
SYS_INFO_ICON = ctk.CTkImage(
    light_image=Image.open("./icons/sys_info_light.png"),
    dark_image=Image.open("./icons/sys_info_dark.png"),
    size=(20, 20),
)
GITHUB_ICON = ctk.CTkImage(
    light_image=Image.open("./icons/github_light.png"),
    dark_image=Image.open("./icons/github_dark.png"),
    size=(20, 20),
)


# Buttons
ACTIVE_BUTTON = {
    "width": 200,
    "height": 40,
    "font": FONT_14_BOLD,
    "corner_radius": 5,
    "text_color": ("#232b32", "#ffffff"),
    "fg_color": ("#f4f4f2", "#232b32"),
    "hover_color": ("#f4f4f2", "#232b32"),
    "compound": "left",
    "anchor": "w",
}

NORMAL_BUTTON = {
    "width": 200,
    "height": 40,
    "font": FONT_14_BOLD,
    "corner_radius": 5,
    "text_color": ("#232b32", "#ffffff"),
    "fg_color": ("#e8e8e8", "#171f24"),
    "hover_color": ("#f4f4f2", "#232b32"),
    "compound": "left",
    "anchor": "w",
}

GITHUB_BUTTON = {
    "width": 150,
    "height": 40,
    "font": FONT_14_BOLD,
    "corner_radius": 5,
    "text_color": ("#232b32", "#ffffff"),
    "fg_color": ("#f4f4f2", "#232b32"),
    "hover_color": ("#f4f4f2", "#293239"),
    "compound": "left",
    "anchor": "center",
}


STORAGE_LIST = []
DEVICE_LIST = []
WINDOWS_LIST = []

INFO_GATHER = InfoGather()

GET_STORAGE = INFO_GATHER.get_storage_info()
STORAGE_LIST.append(GET_STORAGE)

GET_DEVICE_INFO = INFO_GATHER.get_device_info()
DEVICE_LIST.append(GET_DEVICE_INFO)

GET_WINDOWS_INFO = INFO_GATHER.get_windows_info()
WINDOWS_LIST.append(GET_WINDOWS_INFO)

IP_ADDRESS = INFO_GATHER.get_ip_address()


class SystemUtilities(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("System Utilities")
        self.geometry("1280x720")
        self.maxsize(1280, 720)
        self.minsize(1280, 720)
        self.resizable(False, False)
        self.iconbitmap(APP_LOGO)
        self.center_window(1280, 720)

        self.monitor_queue = queue.Queue()
        self.monitor_event = threading.Event()
        self.monitor_flag = True
        self.bandwidth_queue = queue.Queue()
        self.bandwidth_event = threading.Event()
        self.bandwidth_flag = False

        self.create_layout()
        self.navbar_widgets()
        self.sidebar_widgets()
        self.home_page()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # Create Layout
    def create_layout(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_propagate(False)

        self.sidebar_frame = ctk.CTkFrame(
            self, width=250, corner_radius=0, fg_color=("#e8e8e8", "#171f24")
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", rowspan=2)

        self.navbar_frame = ctk.CTkFrame(
            self, height=100, corner_radius=0, fg_color=("#f4f4f2", "#232b32")
        )
        self.navbar_frame.grid(row=0, column=1, sticky="nsew")

        self.main_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color=("#f4f4f2", "#232b32")
        )
        self.main_frame.grid(row=1, column=1, sticky="nsew")

    # Widgets
    def navbar_widgets(self):
        self.navbar_frame.grid_columnconfigure(0, weight=1)

        self.page_name = ctk.CTkLabel(
            self.navbar_frame,
            text="Home Page",
            font=FONT_20_BOLD,
            text_color=("#232b32", "#ffffff"),
        )
        self.page_name.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        theme_label = ctk.CTkLabel(
            self.navbar_frame,
            text="",
            image=THEME_ICON,
        )
        theme_label.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        theme_option = ctk.CTkOptionMenu(
            self.navbar_frame,
            values=["System", "Dark", "Light"],
            corner_radius=5,
            width=150,
            height=35,
            fg_color=("#e8e8e8", "#293239"),
            text_color=("#232b32", "#ffffff"),
            button_color=("#e8e8e8", "#293239"),
            button_hover_color=("#e8e8e8", "#293239"),
            dropdown_fg_color=("#e8e8e8", "#293239"),
            dropdown_hover_color=("#ffffff", "#272f37"),
            dropdown_text_color=("#232b32", "#ffffff"),
            font=FONT_14,
            command=self.change_theme,
        )
        theme_option.set("System")
        theme_option.grid(row=0, column=2, padx=10, pady=10, sticky="e")

    def sidebar_widgets(self):
        # self.sidebar_frame.rowconfigure(0, weight=1) # Comment out if center buttons
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.sidebar_frame.grid_propagate(False)

        logo = ctk.CTkLabel(
            self.sidebar_frame,
            text="System Utilities",
            font=FONT_20_BOLD,
            text_color=("#232b32", "#ffffff"),
            image=NAV_LOGO,
            compound="left",
        )
        logo.grid(row=0, column=0, padx=10, pady=20, sticky="new")

        self.home_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="Home",
            image=HOME_ICON,
            **ACTIVE_BUTTON,
            command=lambda: self.set_active(self.home_btn, self.home_page),
        )
        self.home_btn.grid(row=1, column=0, padx=25, pady=10, sticky="nsew")

        self.sys_monitor_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="System Monitor",
            image=SYS_MONITOR_ICON,
            **NORMAL_BUTTON,
            command=lambda: self.set_active(
                self.sys_monitor_btn, self.sys_monitor_page
            ),
        )
        self.sys_monitor_btn.grid(row=2, column=0, padx=25, pady=10, sticky="nsew")

        self.sys_info_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="System Info",
            image=SYS_INFO_ICON,
            **NORMAL_BUTTON,
            command=lambda: self.set_active(self.sys_info_btn, self.sys_info_page),
        )
        self.sys_info_btn.grid(row=3, column=0, padx=25, pady=10, sticky="nsew")

        github_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="Github",
            image=GITHUB_ICON,
            command=self.open_github,
            **GITHUB_BUTTON,
        )
        github_btn.grid(row=4, column=0, padx=25, pady=10, sticky="sew")

        version_label = ctk.CTkLabel(self.sidebar_frame, text="Version 1.0")
        version_label.grid(row=5, column=0, padx=10, pady=10, sticky="sew")

    def sys_monitor_widgets(self):
        self.sys_monitor_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=("#e8e8e8", "#272f37"),
            corner_radius=5,
            width=1000,
            height=295,
        )
        self.sys_monitor_frame.grid(row=0, column=0, padx=10, pady=10, sticky="snew", columnspan=2)
        self.sys_monitor_frame.grid_propagate(False)

        sys_monitor_title = ctk.CTkLabel(
            self.sys_monitor_frame,
            text="System Monitor",
            font=FONT_16_BOLD,
            text_color=("#232b32", "#ffffff"),
        )
        sys_monitor_title.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        _, self.cpu_value, self.cpu_usage = self.create_monitor_widget(
            parent=self.sys_monitor_frame,
            title_text="CPU",
            value_text="N/A",
            value_label="Temperature",
            usage_text="N/A",
            usage_label="Utilization",
            row=1,
            column=0,
        )
        _, self.gpu_temp, self.gpu_usage = self.create_monitor_widget(
            parent=self.sys_monitor_frame,
            title_text="GPU",
            value_text="N/A",
            value_label="Temperature",
            usage_text="N/A",
            usage_label="Utilization",
            row=1,
            column=1,
        )
        _, self.ram_in_use, self.ram_usage = self.create_monitor_widget(
            parent=self.sys_monitor_frame,
            title_text="RAM",
            value_text="N/A",
            value_label="In Use",
            usage_text="N/A",
            usage_label="Utilization",
            row=1,
            column=2,
        )

    def create_monitor_widget(
        self,
        parent,
        title_text,
        value_text,
        value_label,
        usage_text,
        usage_label,
        row,
        column,
    ):
        monitor_frame = ctk.CTkFrame(
            parent,
            fg_color=("#ffffff", "#232b32"),
            corner_radius=5,
            width=300,
            height=150,
        )
        monitor_frame.grid(row=row, column=column, padx=10, pady=10, sticky="snew")
        monitor_frame.grid_rowconfigure((1, 2), weight=1)
        monitor_frame.grid_columnconfigure((1, 2), weight=1)
        monitor_frame.grid_propagate(False)

        title = ctk.CTkLabel(
            monitor_frame,
            text=title_text,
            font=FONT_16_BOLD,
            text_color=("#232b32", "#ffffff"),
        )
        title.grid(row=0, column=0, padx=10, pady=10, sticky="new")

        value_value = ctk.CTkLabel(
            monitor_frame,
            text=value_text,
            font=FONT_16_BOLD,
            text_color=("#232b32", "#ffffff"),
        )
        value_value.grid(row=1, column=1, padx=10, pady=10, sticky="snew")

        value_label = ctk.CTkLabel(
            monitor_frame,
            text=value_label,
            font=FONT_14,
            text_color=("#232b32", "#ffffff"),
        )
        value_label.grid(row=2, column=1, padx=10, pady=10, sticky="snew")

        usage_value = ctk.CTkLabel(
            monitor_frame,
            text=usage_text,
            font=FONT_16_BOLD,
            text_color=("#232b32", "#ffffff"),
        )
        usage_value.grid(row=1, column=2, padx=10, pady=10, sticky="snew")

        usage_label = ctk.CTkLabel(
            monitor_frame,
            text=usage_label,
            font=FONT_14,
            text_color=("#232b32", "#ffffff"),
        )
        usage_label.grid(row=2, column=2, padx=10, pady=10, sticky="snew")

        return monitor_frame, value_value, usage_value

    def sys_info_widgets(self):
        sys_info_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=("#e8e8e8", "#272f37"),
            corner_radius=5,
            width=1000,
            height=295,
        )
        active_fg = ("#f4f4f2", "#232b32")
        if self.sys_info_btn.cget("fg_color") == active_fg:
            sys_info_frame.grid(row=0, column=0, padx=10, pady=10, sticky="snew")
        else:
            sys_info_frame.grid(row=1, column=0, padx=10, pady=10, sticky="snew")
        sys_info_frame.grid_columnconfigure((0, 1), weight=1)
        sys_info_frame.grid_propagate(False)

        sys_info_title = ctk.CTkLabel(
            sys_info_frame,
            text="System Information",
            font=FONT_16_BOLD,
            text_color=("#232b32", "#ffffff"),
        )
        sys_info_title.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        device_spec_frame = ctk.CTkFrame(
            sys_info_frame,
            fg_color=("#ffffff", "#232b32"),
            corner_radius=5,
            width=470,
            height=235,
        )

        device_spec_frame.grid(row=1, column=0, padx=10, pady=10, sticky="snew")

        device_spec_title = ctk.CTkLabel(
            device_spec_frame, text="Device Specification", font=FONT_14_BOLD
        )
        device_spec_title.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        device_label_1 = ctk.CTkLabel(
            device_spec_frame, text="Device Name", font=FONT_14
        )
        device_label_1.grid(row=1, column=0, padx=10, pady=0, sticky="sw")
        device_label_2 = ctk.CTkLabel(device_spec_frame, text="Processor", font=FONT_14)
        device_label_2.grid(row=2, column=0, padx=10, pady=0, sticky="sw")
        device_label_3 = ctk.CTkLabel(
            device_spec_frame, text="Installed RAM", font=FONT_14
        )
        device_label_3.grid(row=3, column=0, padx=10, pady=0, sticky="sw")
        device_label_4 = ctk.CTkLabel(device_spec_frame, text="GPU", font=FONT_14)
        device_label_4.grid(row=4, column=0, padx=10, pady=0, sticky="sw")
        device_label_5 = ctk.CTkLabel(
            device_spec_frame, text="System Type", font=FONT_14
        )
        device_label_5.grid(row=5, column=0, padx=10, pady=0, sticky="sw")
        device_label_6 = ctk.CTkLabel(
            device_spec_frame, text="Product ID", font=FONT_14
        )
        device_label_6.grid(row=6, column=0, padx=10, pady=(0, 20), sticky="sw")

        self.device_value_1 = ctk.CTkLabel(device_spec_frame, text="N/A", font=FONT_14)
        self.device_value_1.grid(row=1, column=1, padx=10, pady=0, sticky="sw")
        self.device_value_2 = ctk.CTkLabel(device_spec_frame, text="N/A", font=FONT_14)
        self.device_value_2.grid(row=2, column=1, padx=10, pady=0, sticky="sw")
        self.device_value_3 = ctk.CTkLabel(device_spec_frame, text="N/A", font=FONT_14)
        self.device_value_3.grid(row=3, column=1, padx=10, pady=0, sticky="sw")
        self.device_value_4 = ctk.CTkLabel(device_spec_frame, text="N/A", font=FONT_14)
        self.device_value_4.grid(row=4, column=1, padx=10, pady=0, sticky="sw")
        self.device_value_5 = ctk.CTkLabel(device_spec_frame, text="N/A", font=FONT_14)
        self.device_value_5.grid(row=5, column=1, padx=10, pady=0, sticky="sw")
        self.device_value_6 = ctk.CTkLabel(device_spec_frame, text="N/A", font=FONT_14)
        self.device_value_6.grid(row=6, column=1, padx=10, pady=(0, 20), sticky="sw")

        windows_spec_frame = ctk.CTkFrame(
            sys_info_frame,
            fg_color=("#ffffff", "#232b32"),
            corner_radius=5,
            width=470,
            height=235,
        )

        windows_spec_frame.grid(row=1, column=1, padx=10, pady=10, sticky="snew")

        windows_spec_title = ctk.CTkLabel(
            windows_spec_frame, text="Windows Specification", font=FONT_14_BOLD
        )
        windows_spec_title.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        windows_label_1 = ctk.CTkLabel(windows_spec_frame, text="Edition", font=FONT_14)
        windows_label_1.grid(row=1, column=0, padx=10, pady=0, sticky="sw")
        windows_label_2 = ctk.CTkLabel(windows_spec_frame, text="Version", font=FONT_14)
        windows_label_2.grid(row=2, column=0, padx=10, pady=0, sticky="sw")
        windows_label_3 = ctk.CTkLabel(
            windows_spec_frame, text="Installed on", font=FONT_14
        )
        windows_label_3.grid(row=3, column=0, padx=10, pady=0, sticky="sw")
        windows_label_4 = ctk.CTkLabel(
            windows_spec_frame, text="OS build", font=FONT_14
        )
        windows_label_4.grid(row=4, column=0, padx=10, pady=0, sticky="sw")
        windows_label_5 = ctk.CTkLabel(
            windows_spec_frame, text="Boot up time", font=FONT_14
        )
        windows_label_5.grid(row=5, column=0, padx=10, pady=0, sticky="sw")
        windows_label_6 = ctk.CTkLabel(
            windows_spec_frame, text="Registered User", font=FONT_14
        )
        windows_label_6.grid(row=6, column=0, padx=10, pady=(0, 20), sticky="sw")

        self.windows_value_1 = ctk.CTkLabel(
            windows_spec_frame, text="N/A", font=FONT_14
        )
        self.windows_value_1.grid(row=1, column=1, padx=10, pady=0, sticky="sw")
        self.windows_value_2 = ctk.CTkLabel(
            windows_spec_frame, text="N/A", font=FONT_14
        )
        self.windows_value_2.grid(row=2, column=1, padx=10, pady=0, sticky="sw")
        self.windows_value_3 = ctk.CTkLabel(
            windows_spec_frame, text="N/A", font=FONT_14
        )
        self.windows_value_3.grid(row=3, column=1, padx=10, pady=0, sticky="sw")
        self.windows_value_4 = ctk.CTkLabel(
            windows_spec_frame, text="N/A", font=FONT_14
        )
        self.windows_value_4.grid(row=4, column=1, padx=10, pady=0, sticky="sw")
        self.windows_value_5 = ctk.CTkLabel(
            windows_spec_frame, text="N/A", font=FONT_14
        )
        self.windows_value_5.grid(row=5, column=1, padx=10, pady=0, sticky="sw")
        self.windows_value_6 = ctk.CTkLabel(
            windows_spec_frame, text="N/A", font=FONT_14
        )
        self.windows_value_6.grid(row=6, column=1, padx=10, pady=(0, 20), sticky="sw")

    def storage_widgets(self):
        storage_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=("#e8e8e8", "#272f37"),
            corner_radius=5,
            width=470,
            height=200,
        )

        storage_frame.grid(row=1, column=0, padx=10, pady=10, sticky="snew")
        storage_frame.grid_propagate(False)

        storage_title = ctk.CTkLabel(
            storage_frame,
            text="Storage",
            font=FONT_16_BOLD,
            text_color=("#232b32", "#ffffff"),
        )
        storage_title.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        drive_data = STORAGE_LIST[0]
        drive = drive_data["drive_letter"]
        free = drive_data["free_size"]
        total = drive_data["total_size"]

        for i, drive_letter in enumerate(drive, start=1):
            drive_label = ctk.CTkLabel(storage_frame, text=f"Drive {drive_letter}\\")
            drive_label.grid(row=i, column=0, padx=10, pady=5)

            progress_value = int((free[i - 1] / total[i - 1]) * 100)
            new_vlaue = f"0.{progress_value}"
            progress_bar = ctk.CTkProgressBar(
                storage_frame,
                mode="determinate",
                width=200,
                height=10,
                corner_radius=4,
                progress_color="#98a1b7",
            )
            progress_bar.set(float(new_vlaue))
            progress_bar.grid(row=i, column=1, padx=10, pady=2, sticky="w")

            free_of_label = ctk.CTkLabel(
                storage_frame, text=f"{free[i - 1]} GB free of {total[i - 1]} GB"
            )
            free_of_label.grid(row=[i], column=2, padx=10, pady=2, sticky="w")

    def network_widgets(self):
        network_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=("#e8e8e8", "#272f37"),
            corner_radius=5,
            width=470,
            height=200,
        )

        network_frame.grid(row=1, column=1, padx=10, pady=10, sticky="snew")
        network_frame.grid_propagate(False)

        netowkr_title = ctk.CTkLabel(
            network_frame,
            text="Network",
            font=FONT_16_BOLD,
            text_color=("#232b32", "#ffffff"),
        )
        netowkr_title.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        ip_address_label = ctk.CTkLabel(
            network_frame,
            text="IP Address",
            font=FONT_14_BOLD,
            text_color=("#232b32", "#ffffff"),
        )
        ip_address_label.grid(row=1, column=0, padx=10, pady=10, sticky="sw")

        ip_address_value = ctk.CTkLabel(
            network_frame,
            text=IP_ADDRESS,
            font=FONT_14,
            text_color=("#232b32", "#ffffff"),
        )
        ip_address_value.grid(row=1, column=1, padx=10, pady=10, sticky="se")

        sent_label = ctk.CTkLabel(
            network_frame,
            text="Sent",
            font=FONT_14_BOLD,
            text_color=("#232b32", "#ffffff"),
        )
        sent_label.grid(row=2, column=0, padx=10, pady=10, sticky="sw")

        self.sent_value = ctk.CTkLabel(
            network_frame,
            text="N/A",
            font=FONT_14,
            text_color=("#232b32", "#ffffff"),
        )
        self.sent_value.grid(row=2, column=1, padx=10, pady=10, sticky="se")

        received_label = ctk.CTkLabel(
            network_frame,
            text="Received",
            font=FONT_14_BOLD,
            text_color=("#232b32", "#ffffff"),
        )
        received_label.grid(row=3, column=0, padx=10, pady=10, sticky="sw")

        self.received_value = ctk.CTkLabel(
            network_frame,
            text="N/A",
            font=FONT_14,
            text_color=("#232b32", "#ffffff"),
        )
        self.received_value.grid(row=3, column=1, padx=10, pady=10, sticky="se")

    def other_info_frame(self):
        other_info_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=("#e8e8e8", "#272f37"),
            corner_radius=5,
            width=1000,
            height=295,
        )
        other_info_frame.grid(row=1, column=0, padx=10, pady=10, sticky="snew")
        other_info_frame.grid_columnconfigure(0, weight=1)

        other_info_title = ctk.CTkLabel(
            other_info_frame,
            text="Other Information",
            font=FONT_16_BOLD,
            text_color=("#232b32", "#ffffff"),
        )
        other_info_title.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        coming_soon = ctk.CTkLabel(
            other_info_frame,
            text="Coming Soon",
            font=FONT_16,
            text_color=("#232b32", "#ffffff"),
        )
        coming_soon.grid(row=1, column=0, padx=10, pady=10, sticky="snew")

    # Pages
    def home_page(self):
        self.main_frame.grid_rowconfigure((0,1), weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.monitor_flag = True
        self.monitor_event.clear()
        self.sys_monitor_widgets()
        self.start_monitor()
        self.after(100, self.update_monitor)
        self.sys_info_widgets()
        self.after(100, self.update_sys_info)

    def sys_monitor_page(self):
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure((0,1), weight=1)
        self.main_frame.grid_propagate(False)
        self.monitor_flag = True
        self.monitor_event.clear()
        self.sys_monitor_widgets()
        self.start_monitor()
        self.after(100, self.update_monitor)
        self.after(100, self.storage_widgets)
        self.bandwidth_flag = True
        self.bandwidth_event.clear()
        self.network_widgets()
        self.start_bandwidth()
        self.after(100, self.update_bandwidth)

    def sys_info_page(self):
        self.main_frame.grid_rowconfigure((0,1), weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.sys_info_widgets()
        self.after(100, self.update_sys_info)
        self.other_info_frame()

    # Methods
    def start_bandwidth(self):
        self.bandwidth_thread = threading.Thread(
            target=self.bandwidth_worker, daemon=True
        )
        self.bandwidth_thread.start()

    def bandwidth_worker(self):
        bandwidth_info_gather = InfoGather()
        while not self.bandwidth_event.is_set():
            get_bandwidth = bandwidth_info_gather.get_network_bandwidth()

            bandwidth_info = {
                "sent_bandwidth": get_bandwidth["sent_bandwidth"],
                "received_bandwidth": get_bandwidth["received_bandwidth"],
            }
            self.bandwidth_queue.put(bandwidth_info)
            self.bandwidth_event.wait(1)

    def update_bandwidth(self):
        if not self.bandwidth_flag:
            return
        try:
            bandwidth_data = self.bandwidth_queue.get_nowait()
            self.sent_value.configure(
                text=f"{bandwidth_data['sent_bandwidth']} Mbps"
            )
            self.received_value.configure(
                text=f"{bandwidth_data['received_bandwidth']} Mbps"
            )
        except queue.Empty:
            pass

        if not self.bandwidth_event.is_set():
            self.after(100, self.update_bandwidth)

    def update_sys_info(self):
        device_info = DEVICE_LIST[0]
        windows_info = WINDOWS_LIST[0]

        self.device_value_1.configure(text=f"{device_info['device_name']}")
        self.device_value_2.configure(text=f"{device_info['processor']}")
        self.device_value_3.configure(text=f"{device_info['installed_ram']} GB")
        self.device_value_4.configure(text=f"{device_info['gpu']}")
        self.device_value_5.configure(text=f"{device_info['system_type']}")
        self.device_value_6.configure(text=f"{device_info['product_id']}")

        self.windows_value_1.configure(text=f"{windows_info['windows_edition']}")
        self.windows_value_2.configure(text=f"{windows_info['windows_version']}")
        self.windows_value_3.configure(text=f"{windows_info['installed_date']}")
        self.windows_value_4.configure(text=f"{windows_info['os_build']}")
        self.windows_value_5.configure(text=f"{windows_info['boot_up_time']}")
        self.windows_value_6.configure(text=f"{windows_info['registered_user']}")

    def start_monitor(self):
        self.monitor_thread = threading.Thread(target=self.monitor_worker, daemon=True)
        self.monitor_thread.start()

    def monitor_worker(self):
        monitor_info_gather = InfoGather()
        while not self.monitor_event.is_set():
            cpu_usage = monitor_info_gather.get_cpu_usage()
            gpu_info = monitor_info_gather.get_gpu_info()
            ram_info = monitor_info_gather.get_ram_info()

            monitor_info = {
                "cpu_usage": cpu_usage,
                "gpu_temperature": gpu_info[0],
                "gpu_usage": gpu_info[1],
                "ram_usage": ram_info[0],
                "ram_used": ram_info[1],
                "ram_total": ram_info[2],
            }
            self.monitor_queue.put(monitor_info)
            self.monitor_event.wait(1)

    def update_monitor(self):
        if not self.monitor_flag:
            return
        try:
            monitor_data = self.monitor_queue.get_nowait()
            self.cpu_usage.configure(text=f"{monitor_data['cpu_usage']}%")
            self.gpu_temp.configure(text=f"{monitor_data['gpu_temperature']}°C")
            self.gpu_usage.configure(text=f"{monitor_data['gpu_usage']}%")
            self.ram_in_use.configure(
                text=f"{monitor_data['ram_used']}/{monitor_data['ram_total']} GB"
            )
            self.ram_usage.configure(text=f"{monitor_data['ram_usage']}%")
        except queue.Empty:
            pass

        if not self.monitor_event.is_set():
            self.after(100, self.update_monitor)

    # Main methods
    def set_active(self, btn, page):
        self.set_deactive()
        btn.configure(**ACTIVE_BUTTON)
        self.destroy_pages()
        page()

    def destroy_pages(self):
        self.monitor_flag = False
        self.monitor_event.set()
        self.monitor_thread.join()
        try:
            self.bandwidth_flag = False
            self.bandwidth_event.set()
            self.bandwidth_thread.join()
        except:
            pass

        for frame in self.main_frame.winfo_children():
            frame.destroy()

    def set_deactive(self):
        self.home_btn.configure(**NORMAL_BUTTON)
        self.sys_monitor_btn.configure(**NORMAL_BUTTON)
        self.sys_info_btn.configure(**NORMAL_BUTTON)

    def center_window(self, window_width, window_height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

    def change_theme(self, new_theme):
        ctk.set_appearance_mode(new_theme)

    def open_github(self):
        webbrowser.open("https://github.com/iamironman0")

    def on_close(self):
        self.monitor_flag = False
        self.monitor_event.set()
        self.monitor_thread.join()
        try:
            self.bandwidth_flag = False
            self.bandwidth_event.set()
            self.bandwidth_thread.join()
        except:
            pass
        self.destroy()

if __name__ == "__main__":
    app = SystemUtilities()
    app.mainloop()
