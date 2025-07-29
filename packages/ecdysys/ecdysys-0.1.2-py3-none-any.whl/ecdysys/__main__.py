import argparse
from ecdysys.utils import check_update, check_deps, update

def main():

    pkg_managers, err_msg = check_deps()

    parser = argparse.ArgumentParser(description="Python CLI to update your system packages")
    parser.add_argument("-l", "--list", action="store_true" ,help="List available updates")
    parser.add_argument("-u", "--update", action="store_true", help="Update package")
    args = parser.parse_args()

    if args.list:
        print(check_update(pkg_managers, err_msg))
    elif args.update:
        update(pkg_managers, err_msg)

if __name__ == "__main__":
    main()
