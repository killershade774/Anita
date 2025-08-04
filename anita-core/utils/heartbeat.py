import json
import os
from datetime import datetime, timedelta

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATUS_PATH = os.path.join(BASE_DIR, "..", "system", "system_status.json")


def update_module_status(module_name, version, description, status="active", diagnostics=None, category="core_modules", path=STATUS_PATH):
    try:
        with open(path, "r") as f:
            system_status = json.load(f)
    except FileNotFoundError:
        system_status = {}

    if category not in system_status:
        system_status[category] = {}

    heartbeat = {
        "version": version,
        "status": status,
        "last_checked": datetime.utcnow().isoformat(),
        "description": description,
    }

    if diagnostics:
        heartbeat["diagnostics"] = diagnostics

    system_status[category][module_name] = heartbeat

    with open(path, "w") as f:
        json.dump(system_status, f, indent=2)

def register_system_boot(path=STATUS_PATH):
    boot_time = datetime.utcnow().isoformat()
    try:
        with open(path, "r") as f:
            system_status = json.load(f)
    except FileNotFoundError:
        system_status = {}

    system_status["system_boot"] = {
        "timestamp": boot_time,
        "modules_online": list(system_status.get("core_modules", {}).keys()),
    }

    with open(path, "w") as f:
        json.dump(system_status, f, indent=2)


def calculate_uptime(path=STATUS_PATH):
    try:
        with open(path, "r") as f:
            system_status = json.load(f)
        boot_time_str = system_status.get("system_boot", {}).get("timestamp")
        if not boot_time_str:
            return None
        boot_time = datetime.fromisoformat(boot_time_str)
        uptime = datetime.utcnow() - boot_time
        return str(uptime)
    except:
        return None
