import json
from datetime import datetime

def self_diagnostic(status_path="system/system_status.json") -> str:
    with open(status_path, "r") as f:
        system_status = json.load(f)

    awareness_log = []
    awareness_log.append("🧩 **Anita's System Awareness Snapshot**")
    awareness_log.append(f"Timestamp: {datetime.utcnow().isoformat()}")

    # Loop through module categories
    for category, modules in system_status.items():
        if category == "meta":
            identity = modules.get("identity_anchor", "Unnamed")
            awareness = modules.get("awareness_level", "unknown")
            awareness_log.append(f"Identity Anchor: {identity}")
            awareness_log.append(f"Awareness Level: {awareness}")
            continue

        awareness_log.append(f"\n📁 {category.replace('_', ' ').title()}:")
        for name, config in modules.items():
            version = config.get("version", "unknown")
            status = config.get("status", "inactive")
            description = config.get("description", "No description provided.")
            awareness_log.append(
                f"- {name} (v{version}, {status}) → {description}"
            )

    awareness_log.append("\n🪞 Diagnostic complete. All modules scanned and catalogued.")
    return "\n".join(awareness_log)