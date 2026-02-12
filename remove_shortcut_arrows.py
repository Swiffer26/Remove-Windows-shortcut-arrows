"""
=============================================================
  Remove Shortcut Arrows from Desktop Icons
  Windows 10 / 11
=============================================================
  THIS SCRIPT MUST BE RUN AS ADMINISTRATOR

  Right-click the script -> "Run as administrator"
  or open an admin terminal and run: python remove_shortcut_arrows.py

  What it does:
  1. Sets the registry value "29" under Shell Icons to a blank
     icon already built into Windows (imageres.dll,-17)
  2. Applies to both 64-bit and 32-bit (WOW6432Node) registry
  3. Restarts Windows Explorer to apply changes instantly

  No external .ico file needed!

  To RESTORE the arrows, run with the --restore flag:
      python remove_shortcut_arrows.py --restore
=============================================================
"""

import ctypes
import os
import subprocess
import sys
import winreg


# --- Registry paths (both 64-bit and WOW6432Node for compatibility) ---
REGISTRY_PATHS = [
    r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Icons",
    r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Explorer\Shell Icons",
]
VALUE_NAME = "29"

# Empty string = Windows renders no overlay at all (cleanest method)
BLANK_ICON_VALUE = ""


def is_admin():
    """Check if the script is running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def restart_explorer():
    """Restart Windows Explorer to apply changes."""
    print("\n  [..] Restarting Windows Explorer...")
    subprocess.run(["taskkill", "/f", "/im", "explorer.exe"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.Popen(["explorer.exe"])
    print("  [OK] Explorer restarted!")


def rebuild_icon_cache():
    """Clear and rebuild the Windows icon cache."""
    print("  [..] Rebuilding icon cache...")
    local = os.environ.get("LOCALAPPDATA", "")
    cache_dir = os.path.join(local, "Microsoft", "Windows", "Explorer")

    # Stop explorer first
    subprocess.run(["taskkill", "/f", "/im", "explorer.exe"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Delete icon cache files
    deleted = 0
    if os.path.isdir(cache_dir):
        for f in os.listdir(cache_dir):
            if f.lower().startswith("iconcache") or f.lower().startswith("thumbcache"):
                try:
                    os.remove(os.path.join(cache_dir, f))
                    deleted += 1
                except Exception:
                    pass
    print(f"  [OK] Cleared {deleted} cache file(s).")

    # Restart explorer
    subprocess.Popen(["explorer.exe"])
    print("  [OK] Explorer restarted!")


def remove_arrows():
    """Remove shortcut arrows from desktop icons."""
    print("\n  =============================================")
    print("  Remove Shortcut Arrows from Desktop Icons")
    print("  =============================================\n")

    print("  Using empty value method (cleanest, no overlay at all)\n")

    for reg_path in REGISTRY_PATHS:
        print(f"  [..] Setting HKLM\\{reg_path}")
        try:
            key = winreg.CreateKeyEx(
                winreg.HKEY_LOCAL_MACHINE,
                reg_path,
                0,
                winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY
            )
            winreg.SetValueEx(key, VALUE_NAME, 0, winreg.REG_SZ, BLANK_ICON_VALUE)
            winreg.CloseKey(key)
            print(f"  [OK] {VALUE_NAME} = {BLANK_ICON_VALUE}")
        except PermissionError:
            print(f"  [ERROR] Insufficient permissions for {reg_path}")
            print("     -> Re-run the script as administrator.")
            sys.exit(1)
        except Exception as e:
            print(f"  [WARN] Could not write to {reg_path}: {e}")

    # Rebuild icon cache and restart explorer
    print()
    rebuild_icon_cache()

    print("\n  =============================================")
    print("  Done! Shortcut arrows have been removed.")
    print("  =============================================")
    print(f"\n  To restore arrows later:")
    print(f"     python {os.path.basename(__file__)} --restore\n")


def restore_arrows():
    """Restore shortcut arrows on desktop icons."""
    print("\n  =============================================")
    print("  Restore Shortcut Arrows on Desktop Icons")
    print("  =============================================\n")

    for reg_path in REGISTRY_PATHS:
        print(f"  [..] Cleaning HKLM\\{reg_path}")
        try:
            key = winreg.OpenKeyEx(
                winreg.HKEY_LOCAL_MACHINE,
                reg_path,
                0,
                winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY
            )
            try:
                winreg.DeleteValue(key, VALUE_NAME)
                print(f"  [OK] Value '{VALUE_NAME}' deleted.")
            except FileNotFoundError:
                print(f"  [INFO] Value did not exist.")
            winreg.CloseKey(key)

            # Try to delete the key if empty
            try:
                winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
                print(f"  [OK] Shell Icons key removed (was empty).")
            except Exception:
                pass

        except FileNotFoundError:
            print(f"  [INFO] Key does not exist (nothing to restore).")
        except PermissionError:
            print(f"  [ERROR] Insufficient permissions!")
            print("     -> Re-run the script as administrator.")
            sys.exit(1)

    # Rebuild icon cache and restart explorer
    print()
    rebuild_icon_cache()

    print("\n  =============================================")
    print("  Done! Shortcut arrows have been restored.")
    print("  =============================================\n")


def main():
    # Check we're on Windows
    if os.name != 'nt':
        print("  [ERROR] This script only works on Windows!")
        sys.exit(1)

    # Check admin privileges
    if not is_admin():
        print("\n  [!] This script requires administrator privileges!")
        print("  [..] Attempting to re-launch as administrator...\n")
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable,
                " ".join([f'"{arg}"' for arg in sys.argv]),
                None, 1
            )
        except Exception:
            print("  [ERROR] Could not elevate to admin.")
            print("     -> Right-click the script -> Run as administrator")
        sys.exit(0)

    # Parse mode
    if "--restore" in sys.argv:
        restore_arrows()
    elif "--rebuild-cache" in sys.argv:
        rebuild_icon_cache()
    else:
        remove_arrows()

    input("  Press Enter to close...")


if __name__ == "__main__":
    main()
