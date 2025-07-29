import os
import sys
import configparser

import h5py
import datetime as dt
import numpy as np
from matplotlib import pyplot as plt

_DATETIME_FORMAT_STRING = "%Y-%m-%dT%H-%M-%S"
_DATETIME_FORMAT_PATH = "%Y/%m/%d/%H-%M-%S/"


def _get_pip_freeze():
    """
    Based on https://stackoverflow.com/a/31304042
    """

    try:
        from pip._internal.operations import freeze
    except ImportError:
        from pip.operations import freeze

    return list(freeze.freeze())


def _get_path_from_config():
    path = None
    config_path_dir = os.path.expanduser("~")
    config_path_dir += "/.config/pogger/"
    if not os.path.exists(config_path_dir):
        os.makedirs(config_path_dir)
    config_path = config_path_dir + "pogger.conf"
    if os.path.exists(config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        if "path" in config:
            if "archive" in config["path"]:
                path = \
                    os.path.expanduser(config["path"]["archive"])
                if path[-1] != "/":
                    path += "/"

    # If config isn't there, then set a default path
    if path is None:
        path = os.path.expanduser("~")
        path += "/pogger_archives/"

    return path


def _get_datetime_strings(datetime):
    """
    Gets formatted datetimes file name and path from a `datetime` object.

    Parameters
    ----------
    datetime : obj
        Date to format.

    Returns
    -------
    datetime_string : str
        File name.
    datetime_path : str
        Path.
    """

    datetime_string = dt.datetime.strftime(
        datetime, _DATETIME_FORMAT_STRING
    )
    datetime_path = dt.datetime.strftime(
        datetime, _DATETIME_FORMAT_PATH
    )

    return datetime_string, datetime_path


def _get_datetime_paths(project_name, datetime, path):
    """
    Generates project paths based on project name and timestamp.

    Parameter
    ---------
    project_name: str
        Directory of project (under `path`).
    datetime: obj
        Time stamp.
    path: str
        Path to pogger archive.

    Returns
    -------
    datetime_string: str
        Timestamp for file.
    datetime_path: str
        Timestamp for path.
    path_dir: str
        Full path with embedded timestamp.
    path_full: str
        File name included.
    """

    datetime_string, datetime_path = \
        _get_datetime_strings(datetime)
    path_dir = path + datetime_path
    path_full = path_dir + datetime_string + "_" + project_name

    return datetime_string, datetime_path, path_dir, path_full


class Pogger():
    """
    A class that logs the results of a python script in three ways:
    1. Any console output run after the instance is created is automatically
        saved to a log file.
    2. One can wrap any function using the `Pogger.record` decorator.
        The outputs of wrapped functions will be automatically saved to an hdf5
        file.
    3. Any figures generated in `matplotlib.pyplot` of wrapped functions will
        also be automatically saved.

    All three methods of logging are saved within a timestamped directory.

    Parameters
    ----------
    project_name: str
        A label of the the script being logged.
        The default name is `"default"`.
    pogger_path: str
        The root path where the log files saved.
        If not specified, it will choose the value set in
        ~/.config/pogger/pogger.conf.
        If this value is not set, then it will default to
        ~/pogger_archives/.
    verbose: bool
        If set to True, the `Pogger` object will print debug-style messages to
        the console and log file.
    """

    def __init__(
            self, project_name="default", pogger_path=None, verbose=False):
        self._project_name = project_name
        self._is_verbose = verbose
        self._path = pogger_path
        self._initialise_context()
        self._initialise_paths()
        self._initialise_printer()
        self._initialise_h5()
        self._initialise_figures()

        if self._is_verbose:
            print("Logging initialised")

    def __enter__(
            self, project_name="default", pogger_path=None, verbose=False):
        return self

    def exit(self):
        self._exit_printer()

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.exit()

    def _initialise_paths(self):
        if self._path is None:
            self._path = _get_path_from_config()

        # Script name
        self._python_name = __name__
        self._path += self._project_name + "/"

        # Timestamp
        self._datetime = dt.datetime.now()
        self._datetime_string, self._datetime_path, \
            self._path_dir, self._path_full = \
            _get_datetime_paths(self._project_name, self._datetime, self._path)
        if not os.path.exists(self._path_dir):
            os.makedirs(self._path_dir)

    def record(self, result_names=None, result_units=None):
        """
        When a function is decorated with this method,
        1. Any return values of the function will be saved to an hdf5 archive,
            and,
        2. Any plots generated by `matplotlib.pyplot` will be saved to disk.

        Parameters
        ----------
        result_names: tuple
            A `tuple` of strings which are the names of any return values of
            the decorated function.
            Informs the labelling in hdf5 file.
        result_units: tuple
            A `tuple` of strings which are the units of any return values of
            the decorated function.
            For example, one might want to state that measured points in time
            are measured in us rather than s.

        Returns
        -------
        function: callable
            A decorated function.
        """

        def write_result(result=None, result_name=None, result_unit=None):
            if result is None:
                return
            elif type(result) is tuple:
                for result_index, result_value in enumerate(result):
                    result_name_value = result_name[result_index]
                    if result_unit is None:
                        result_unit_value = None
                    else:
                        result_unit_value = result_unit[result_index]

                    write_result(
                        result_value,
                        result_name_value,
                        result_unit_value
                    )
            elif type(result) is dict:
                for result_name_sub, result_value in result.items():
                    result_name_value = result_name + "/" + result_name_sub
                    if result_unit is None:
                        result_unit_value = None
                    elif type(result_unit) is dict:
                        result_unit_value = result_unit[result_name_sub]
                    else:
                        result_unit_value = result_unit

                    write_result(
                        result_value,
                        result_name_value,
                        result_unit_value
                    )
            elif isinstance(result, np.ndarray):
                self.write_array(result_name, result, result_unit)
            else:
                self.write_value(result_name, result, result_unit)

        def wrapper(function: callable):
            def wrapped(*arguments, **keyword_arguments):
                """
                A wrapped version of a function, generated by a
                `Pogger.record` decorator.
                """

                try:
                    results = function(*arguments, **keyword_arguments)
                except Exception as exception:
                    results = None
                    raise exception
                finally:
                    write_result(results, result_names, result_units)

                    figure_numbers = plt.get_fignums()
                    figure_labels = plt.get_figlabels()
                    for figure_number, figure_label in \
                            zip(figure_numbers, figure_labels):
                        if figure_number not in self._plotted_figures:
                            plt.figure(figure_number)
                            plt.savefig(
                                self._figure_path
                                + self.get_context().replace("/", "_")
                                + "_" + figure_label + ".png")
                            plt.savefig(
                                self._figure_path
                                + self.get_context().replace("/", "_")
                                + "_" + figure_label + ".pdf")
                            self._plotted_figures.append(figure_number)
                            if self._is_verbose:
                                print(
                                    "Figure written to",
                                    self.get_context().replace("/", "_")
                                    + "_" + figure_label)
                return results
            return wrapped
        return wrapper

    def _initialise_figures(self):
        self._figure_path_dir = self._path_dir + "figures/"
        if not os.path.exists(self._figure_path_dir):
            os.makedirs(self._figure_path_dir)
        self._figure_path = self._figure_path_dir \
            + self._datetime_string + "_" + self._project_name + "_"

        self._plotted_figures = []

    def _initialise_h5(self):
        self._path_h5 = self._path_full + ".h5"

        self._pip_freeze = _get_pip_freeze()

        with h5py.File(self._path_h5, "w") as file_h5:
            group_metadata = file_h5.require_group("metadata")
            group_metadata["pip_freeze"] = np.array(
                self._pip_freeze, dtype=object)

    def _initialise_context(self):
        self.set_context()

    def _initialise_printer(self):
        self._normal_out = sys.stdout
        self._normal_error_out = sys.stderr
        self._log_out_path = self._path_full + ".log"
        self._printer = Printer(self._normal_out, self._log_out_path)
        sys.stdout = self._printer
        sys.stderr = self._printer

    def _exit_printer(self):
        sys.stdout = self._normal_out
        sys.stderr = self._normal_error_out
        self._printer = None

    def set_context(self, context=None):
        """
        Arrays, values and figures are labelled under the current context of
        the `Pogger` object.
        Changing the context enables, eg., running the same decorated function
        multiple times, saving the return values under different labels.

        Parameters
        ----------
        context: str
            The context to be changed to.
            If not specified, the context will return to a root context.
        """

        if context is None:
            self._context = ""
        else:
            self._context = context

    def get_context(self):
        """
        Returns the current context of the `Pogger` object.

        Returns
        -------
        context: str
            The current context of the `Pogger` object.
        """

        return self._context

    def get_datetime(self):
        """
        Returns the timestamp of the log that is being written to.

        Returns
        -------
        datetime_string: str
            A `str` representation of the timestamp being written to.
        """

        return self._datetime_string

    def write_array(self, path, array, units=None):
        """
        Logs an array to the logging hdf5 file.

        Note
        ----
            Data is saved to a path dependent on the current context of the
            `Pogger`.
            Change this by using the `Pogger.set_context` method.

        Parameters
        ----------
        path: str
            The name of the array being written.
        array: `numpy.ndarray`
            The array to be written.
        units: str
            (Optional) The units of the array being written.
            For example, if the array is a list of times, one might want to
            specify if they are measured in us or s.
        """

        path_full = "data/" + self._context + "/" + path
        path_split = path_full.split("/")
        with h5py.File(self._path_h5, "a") as file_h5:
            path_dir = ""
            for dir_index in range(0, len(path_split) - 1):
                path_dir += path_split[dir_index] + "/"
                file_h5.require_group(path_dir[:-1])

            file_h5[path_full] = array
            if units is not None:
                file_h5[path_full].attrs["_units"] = units
        if self._is_verbose:
            print("Array written to hdf5 path", path_full)

    def write_value(self, path, value, units=None):
        """
        Logs a non-array value to the logging hdf5 file.
        Values are stored in hdf5 attributes.

        Note
        ----
            Data is saved to a path dependent on the current context of the
            `Pogger`.
            Change this by using the `Pogger.set_context` method.

        Parameters
        ----------
        path: str
            The name of the value being written.
        value: obj
            The value to be written.
        units: str
            (Optional) The units of the value being written.
            For example, if the array is a time, one might want to specify if
            it is measured in us or s.
        """

        path_full = "data/" + self._context + "/" + path
        path_split = path_full.split("/")
        with h5py.File(self._path_h5, "a") as file_h5:
            path_dir = ""
            for dir_index in range(0, len(path_split) - 1):
                path_dir += path_split[dir_index] + "/"
                file_h5.require_group(path_dir[:-1])
            file_h5[path_dir].attrs[path_split[-1]] = value
            if units is not None:
                file_h5[path_dir].attrs[path_split[-1] + "_units"] = units
        if self._is_verbose:
            print("Value written to hdf5 path", path_full)


class Read:
    """
    A class that reads the archives produced with a `pogger.Pogger` class.

    Parameters
    ----------
    project_name: str
        A label for the script that is being logged.
    datetime: str
        A timestamp for the log that is to be read.
    path: str
        The path to the archive directory.
        If not specified, it will read the value set in
        ~/.config/pogger/pogger.conf if that exists, or
        it will read directly from
        ~/pogger_archives/
    """

    def __init__(
            self, project_name: str = "default",
            datetime: str = None, path: str = None):

        self._project_name = project_name

        self._path = path
        if self._path is None:
            self._path = _get_path_from_config()

        self._path += self._project_name + "/"

        self._datetime_string = datetime
        self._get_datetime_from_string()

        self._datetime_string, self._datetime_path, \
            self._path_dir, self._path_full = \
            _get_datetime_paths(self._project_name, self._datetime, self._path)

        self._path_h5 = self._path_full + ".h5"

    def _get_datetime_from_string(self):
        self._datetime = dt.datetime.strptime(
            self._datetime_string, _DATETIME_FORMAT_STRING)

    def read_array(self, name: str, context: str = None):
        """
        Reads a `numpy.ndarray` from the specified hdf5 archive file.

        Parameters
        ----------
        name: str
            Name of the array saved to the hdf5 file.
        context: str
            Path to the array within the hdf5 file.

        Returns
        -------
        array: numpy.ndarray
            The array specified.
        units: str
            If there is a `units` entry in the hdf5 file for the array, the
            array will be placed in a tuple, and the units of the array will
            also be returned as the second entry.
        """

        if context is not None:
            path = "data/" + context + "/" + name
        else:
            path = "data/" + name

        with h5py.File(self._path_h5) as file_h5:
            array = np.asarray(file_h5[path])
            units = None
            if "_units" in file_h5[path].attrs:
                units = file_h5[path].attrs["_units"]

        if units is None:
            return array
        else:
            return array, units

    def read_value(self, name: str, context: str = None):
        """
        Reads a non-array from the specified hdf5 archive file.

        Parameters
        ----------
        name: str
            Name of the value saved to the hdf5 file.
        context: str
            Path to the value within the hdf5 file.

        Returns
        -------
        value: obj
            The value specified.
        units: str
            If there is a `units` entry in the hdf5 file for the value, the
            value will be placed in a tuple, and the units of the value will
            also be returned as the second entry.
        """

        if context is not None:
            path = "data/" + context
        else:
            path = "data/"

        with h5py.File(self._path_h5) as file_h5:
            value = file_h5[path].attrs[name]
            units = None
            if name + "_units" in file_h5[path].attrs:
                units = file_h5[path].attrs[name + "_units"]

        if units is None:
            return value
        else:
            return value, units


class Printer:
    """
    A "virtual" output stream that prints to both the console and a log file.
    The log file is closed when not being written to.

    Parameters
    ----------
    normal_out: obj
        The console stream.
    log_out_path: str
        Path of a file to write to.
    """

    def __init__(self, normal_out, log_out_path: str):
        self._normal_out = normal_out
        self._log_out_path = log_out_path
        with open(self._log_out_path, "w"):
            pass

    def write(self, *arguments, **keyword_arguments):
        """
        Calls `write` method of both the console and the log file.
        """
        self._normal_out.write(*arguments, **keyword_arguments)
        with open(self._log_out_path, "a") as log_file:
            log_file.write(*arguments, **keyword_arguments)

    def flush(self, *arguments, **keyword_arguments):
        """
        Calls the `flush` method of both the console and the log file.
        """
        self._normal_out.flush(*arguments, **keyword_arguments)
        with open(self._log_out_path, "a") as log_file:
            log_file.flush(*arguments, **keyword_arguments)
