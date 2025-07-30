import argparse, importlib.metadata
from ecdysys.utils import check_update, prepare_pkgms, update

def main():

    pkg_managers, err_msg = prepare_pkgms()

    parser = argparse.ArgumentParser(description="Python CLI to update your system packages")
    parser.add_argument("-v", "--version", action="store_true", help="Prints program's version number")
    parser.add_argument("-l", "--list", action="store_true" ,help="List available updates")
    parser.add_argument("-u", "--update", action="store_true", help="Update package")
    args = parser.parse_args()

    if args.list:
        print(check_update(pkg_managers, err_msg))
    elif args.update:
        update(pkg_managers, err_msg)
    elif args.version:
        print(f"Ecdysys v{importlib.metadata.version("ecdysys")}")

if __name__ == "__main__":
    main()
