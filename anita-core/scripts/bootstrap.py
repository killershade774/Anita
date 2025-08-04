import os
import subprocess

# Define available subsystems and their requirement files
SUBSYSTEMS = {
    "Core": "requirements-core.txt",
    "NLP": "requirements-nlp.txt",
    "GUI": "requirements-gui.txt",
    "Reasoning": "requirements-reasoning.txt",
    "Extras": "requirements-extras.txt"
}

def install_requirements(file):
    print(f"\n🔧 Installing from {file}...")
    subprocess.run(["pip", "install", "-r", file], check=True)
    print("✅ Done.\n")

def prompt_user():
    print("📦 Choose which subsystems to install:")
    for i, name in enumerate(SUBSYSTEMS.keys(), 1):
        print(f"{i}. {name}")
    print("0. Install All")
    
    choice = input("\nEnter your selections (comma-separated, e.g., 1,3): ")
    return choice.split(",")

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    selections = prompt_user()

    if "0" in selections:
        for file in SUBSYSTEMS.values():
            install_requirements(file)
    else:
        for sel in selections:
            try:
                sel_idx = int(sel.strip()) - 1
                file = list(SUBSYSTEMS.values())[sel_idx]
                install_requirements(file)
            except (IndexError, ValueError):
                print(f"⚠️ Skipping invalid selection: {sel.strip()}")

if __name__ == "__main__":
    main()