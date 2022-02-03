import argparse
import logging
import importlib
import pkgutil

from termcolor import colored

import core
import probes


def display_results(results):

    description = colored("[+] User ID used", "green") + "\n" + \
                  colored("[-] User ID not used", "magenta") + \
                  "\n" + colored("[x] Unknown - some error occured. Check the logs", "red")
    print(description)

    for username, user_results in results.items():
        print("*" * (len(username) + 10))
        print(username)
        print("*" * (len(username) + 10))
        for pname, result in user_results.items():
            if isinstance(result, core.ProbeResult) and result.id_found:
                resultstr = colored(f"[+] {pname}", "green")
            elif isinstance(result, core.ProbeResult) and not result.id_found:
                resultstr = colored(f"[-] {pname}", "magenta")
            else:
                resultstr = colored(f"[x] {pname}", "red")
            print(resultstr)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Check if ID exists at online service provider.")
    argparser.add_argument("username", nargs="*", help="The user_id to check. Depending on the service, "
                                                       "this can be the emailaddress or a username.")
    argparser.add_argument("-l", "--list", action="store_true", help="List available probes.")
    argparser.add_argument("-p", "--probes", required=False, help="Specific probes to be used. "
                                                                  "If not provided, all probes are used.")
    argparser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode.")
    args = argparser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    log = logging.getLogger()

    probes_list = [name for finder, name, ispkg in pkgutil.iter_modules(probes.__path__)]

    if args.list:
        print(f"These are the available probes (in folder {probes.__path__[0]}):")
        for p in probes_list:
            print(f"- {p}")
        exit()

    if args.probes:
        loaded_probes = {
            name: importlib.import_module(f"{probes.__name__}.{name}") for name in args.probes.split(",")
        }

    else:
        loaded_probes = {
            name: importlib.import_module(f"{probes.__name__}.{name}") for finder, name, ispkg in pkgutil.iter_modules(probes.__path__)
        }

    log.info("Loaded probes:")
    for p in loaded_probes.keys():
        log.info(p)

    results = {}
    for username in args.username:
        results[username] = {}
        for pname, pmod in loaded_probes.items():
            try:
                result = pmod.get_probe().probe_username(username)
                results[username][pname] = result
            except core.UnexpectedHTTPResponse as err:
                log.error(err)
                results[username][pname] = core.ErrorResult(str(err))

    display_results(results)