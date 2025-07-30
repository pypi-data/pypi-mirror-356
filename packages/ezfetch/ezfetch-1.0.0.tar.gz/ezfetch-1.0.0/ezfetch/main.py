from .logo import get_logo
from .info import *
from .colors import Colors

def display_info():
    logo = get_logo().splitlines()
    fields = [
        ("User", get_user_host()),
        ("OS", get_os()),
        ("Kernel", get_kernel()),
        ("Uptime", get_uptime()),
        ("Shell", get_shell()),
        ("CPU", get_cpu()),
        ("RAM", get_ram()),
        ("Disk", get_disk()),
        ("IP", get_ip())
    ]

    max_label = max(len(label) for label, _ in fields)
    field_lines = [
        f"{Colors.GREEN}{label:<{max_label}}{Colors.RESET}: {Colors.CYAN}{value}{Colors.RESET}"
        for label, value in fields
    ]

    for i in range(max(len(logo), len(field_lines))):
        logo_line = logo[i] if i < len(logo) else ""
        field_line = field_lines[i] if i < len(field_lines) else ""
        print(f"{logo_line:<30}  {field_line}")

if __name__ == "__main__":
    display_info()
