import os

import vlconf
from importlib import reload

cf_loc = vlconf.__file__


def overwrite_verbosity_level(verb_type, verb_val):
    """Change the verbosity value for the given verbosity type verb_val"""
    ee = os.popen(
        f"sed -i '/{verb_type}_verbosity/c\\{verb_type}_verbosity"
        f"={verb_val}' {cf_loc}"
    )

    print(f"{verb_type} verbosity has been set to {verb_val} at {cf_loc}")


class levels:
    def __init__(self, log_verbosity=1, print_verbosity=1):

        self._log_verbosity = log_verbosity
        self._print_verbosity = print_verbosity

        if not os.path.exists(f"{cf_loc}"):
            with open(f"{cf_loc}", "w") as verbosity_file:
                verbosity_file.write("# Configuration file\n# Verbosity\n")
                verbosity_file.write("log_verbosity = 1\n")
                verbosity_file.write("print_verbosity = 1\n")

    def set_log_verbosity(self, log_verbosity):
        self._log_verbosity = log_verbosity
        overwrite_verbosity_level("log", log_verbosity)

    def set_print_verbosity(self, print_verbosity):
        self._print_verbosity = print_verbosity
        overwrite_verbosity_level("print", print_verbosity)

    @property
    def log_verbosity(self):
        reload(vlconf)
        return vlconf.log_verbosity
        # return self._log_verbosity

    @property
    def print_verbosity(self):
        reload(vlconf)
        return vlconf.print_verbosity
        # return self._print_verbosity

    def get_file_location(self):
        return vlconf.__file__
