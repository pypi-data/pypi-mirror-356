import psutil
import platform
from datetime import datetime
from typing import Dict, List, Union

def get_system_info() -> Dict[str, str]:
    """Возвращает информацию о системе"""
    return {
        "System": platform.system(),
        "Node Name": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "Boot Time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    }

def get_cpu_info() -> Dict[str, Union[str, float]]:
    """Возвращает информацию о CPU"""
    return {
        "Physical Cores": psutil.cpu_count(logical=False),
        "Total Cores": psutil.cpu_count(logical=True),
        "Max Frequency": f"{psutil.cpu_freq().max:.2f}Mhz",
        "Current Frequency": f"{psutil.cpu_freq().current:.2f}Mhz",
        "CPU Usage": f"{psutil.cpu_percent()}%"
    }

def get_memory_info() -> Dict[str, str]:
    """Возвращает информацию о памяти"""
    mem = psutil.virtual_memory()
    return {
        "Total": f"{mem.total / (1024**3):.2f} GB",
        "Available": f"{mem.available / (1024**3):.2f} GB",
        "Used": f"{mem.used / (1024**3):.2f} GB",
        "Usage": f"{mem.percent}%"
    }

def get_disk_info() -> List[Dict[str, str]]:
    """Возвращает информацию о дисках"""
    disks = []
    for part in psutil.disk_partitions():
        usage = psutil.disk_usage(part.mountpoint)
        disks.append({
            "Device": part.device,
            "Mountpoint": part.mountpoint,
            "File System": part.fstype,
            "Total Size": f"{usage.total / (1024**3):.2f} GB",
            "Used": f"{usage.used / (1024**3):.2f} GB",
            "Free": f"{usage.free / (1024**3):.2f} GB",
            "Usage": f"{usage.percent}%"
        })
    return disks

def get_processes(sort_by: str = "cpu", limit: int = 5) -> List[Dict[str, Union[int, str, float]]]:
    """Возвращает список процессов"""
    procs = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        try:
            procs.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    reverse = sort_by in ['cpu_percent', 'memory_percent']
    return sorted(procs, key=lambda p: p.get(sort_by, 0), reverse=reverse)[:limit]

def kill_process(pid: int) -> bool:
    """Завершает процесс по PID"""
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        return True
    except psutil.NoSuchProcess:
        return False

def get_network_info() -> Dict[str, Union[str, int]]:
    """Возвращает сетевую статистику"""
    net = psutil.net_io_counters()
    return {
        "Bytes Sent": f"{net.bytes_sent / (1024**2):.2f} MB",
        "Bytes Received": f"{net.bytes_recv / (1024**2):.2f} MB",
        "Packets Sent": net.packets_sent,
        "Packets Received": net.packets_recv
    }

def format_seconds(seconds: int) -> str:
    """Форматирует секунды в читаемый вид"""
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return f"{days}d {hours}h {minutes}m {seconds}s"

def get_uptime() -> str:
    """Возвращает время работы системы"""
    return format_seconds(int(time.time() - psutil.boot_time()))

def get_users() -> List[Dict[str, str]]:
    """Возвращает список пользователей"""
    return [{
        "name": user.name,
        "terminal": user.terminal,
        "host": user.host,
        "started": datetime.fromtimestamp(user.started).strftime("%Y-%m-%d %H:%M:%S")
    } for user in psutil.users()]