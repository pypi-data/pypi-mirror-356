import os, subprocess, shutil
import colorama as clr
import toml

clr.init(autoreset=True)

def print_err(msg): print(clr.Fore.RED + f":: ERROR : {msg}")
def print_warn(msg): print(clr.Fore.YELLOW + f":: WARN : {msg}")

Supported_aur_helpers = ["yay", "paru"]
Supported_pkg_managers = ["pacman", "flatpak"] + Supported_aur_helpers
# Opens config file
try:
    cfg_path = os.getenv("XDG_CONFIG_HOME") + "/ecdysys/config.toml"
    with open(cfg_path) as c:
        cfg = toml.load(c)
except FileNotFoundError:
    print_err(f"No config.toml found at {cfg_path}")
    exit()

# get values from config file
#- Packages managers
try: Pkgms = cfg['pkg_managers']
except KeyError: print_err("No package managers found in config.toml in `pkg_manager`"); exit()
# - Aur helpers
try: Slc_aur =  cfg['aur_helper']
except KeyError: Slc_aur =  str()
#- Post-install scripts
try: Post_install_script = cfg['post_install_script']
except KeyError: Post_install_script = str()
#- Insert aur helper in list if pacman and aur helper are set
if "pacman" in Pkgms and Slc_aur: Pkgms.insert(Pkgms.index("pacman") + 1, Slc_aur)

def prepare_pkgms():
    """checks and filters if the package managers exists"""
    err_unsupported_msg = str()
    err_missing_msg = str()
    pkgms_path = []
    if any(map(lambda v: v in Supported_aur_helpers, Pkgms)) and "pacman" not in Pkgms:
        print_warn("Aur helper selected but not pacman")
        Pkgms.remove(Slc_aur)
    for pkgm in Pkgms:
        # Check if package manager is supported
        if pkgm not in Supported_pkg_managers:
            Pkgms.remove(pkgm)
            err_unsupported_msg += f"Unsupported package manager: {pkgm}" if not err_unsupported_msg else f", {pkgm}"
        else:
            # Check if the package manager is installed
            try:
                subprocess.run([pkgm, "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except FileNotFoundError:
                Pkgms.remove(pkgm)
                if not err_missing_msg:
                    err_missing_msg += f"Missing package managers: {pkgm}"
                else:
                    err_missing_msg += f", {pkgm}"
    return Pkgms,f"{err_unsupported_msg}\n{err_missing_msg}" if err_unsupported_msg or err_missing_msg else str()

def check_update(pkgms, err_msg):
    """checks and returns update from all package managers in the list"""
    update_list = str()
    if err_msg: print_err(clr.Fore.RED + err_msg)
    for pkgm in pkgms:
        match pkgm:
            case "pacman":
                pacman_upd = subprocess.run(shutil.which("checkupdates"), capture_output=True, text=True)
                update_list += clr.Fore.CYAN + "::Pacman updates::\n" + clr.Fore.RESET +  pacman_upd.stdout
            case aur_helper if aur_helper == Slc_aur:
                aur_upd = subprocess.run([shutil.which(Slc_aur), "-Qua"], capture_output=True, text=True)
                update_list += clr.Fore.CYAN + "::Aur updates::\n" + clr.Fore.RESET + aur_upd.stdout
            case "flatpak":
                flatpak_upd = subprocess.run([shutil.which("flatpak"), "remote-ls", "--updates"], capture_output=True, text=True)
                update_list += clr.Fore.BLUE + "::Flatpak updates::\n" + clr.Fore.RESET + flatpak_upd.stdout
    return update_list

def update(pkgms, err_msg):
    """update system"""
    if err_msg: print_err(clr.Fore.RED + err_msg)
    for pkgm in pkgms:
        try: args = cfg[f"args_{pkgm}"]
        except KeyError: args = str()
        match pkgm:
            case "pacman":
                if Slc_aur:
                    cmd = f"{shutil.which(Slc_aur)} -Syu {args}"
                    print(clr.Fore.CYAN + f"::Arch update::\n{cmd}")
                    os.system(cmd)
                    pkgms.remove(Slc_aur)
                else:
                    cmd = f"{shutil.which("pacman")} -Syu {args}"
                    print(clr.Fore.CYAN + f"::Pacman update::\n{shutil.which("pacman")} -Syu")
                    os.system(f"sudo {cmd}")
            case "flatpak":
                cmd = f"{shutil.which("flatpak")} update {args}"
                print(clr.Fore.BLUE + f"::Flatpak update::\n{cmd}")
                os.system(cmd)
    if Post_install_script:
        print(clr.Fore.GREEN + f"::Custom post install script::\n{Post_install_script}")
        os.system(Post_install_script)