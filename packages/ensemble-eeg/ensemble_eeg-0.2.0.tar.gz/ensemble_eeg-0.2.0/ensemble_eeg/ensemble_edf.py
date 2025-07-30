import os
import shutil
import warnings
from collections import namedtuple
from datetime import datetime, timedelta
from itertools import starmap

import dateparser
import numpy as np


def _str(f, size, _):
    s = f.read(size).decode("ascii", "ignore").strip()
    while s.endswith("\x00"):
        s = s[:-1]
    return s


def _int(f, size, name):
    s = _str(f, size, name)
    try:
        return int(s)
    except ValueError:
        warnings.warn(f"{name}: Could not parse integer {s}.")


def _float(f, size, name):
    s = _str(f, size, name)
    try:
        return float(s)
    except ValueError:
        warnings.warn(f"{name}: Could not parse float {s}.")


def _discard(f, size, _):
    f.read(size)


HEADER = (
    ("version", 8, _str),
    ("local_patient_identification", 80, _str),
    ("local_recording_identification", 80, _str),
    ("startdate_of_recording", 8, _str),
    ("starttime_of_recording", 8, _str),
    ("number_of_bytes_in_header_record", 8, _int),
    ("reserved", 44, _discard),
    ("number_of_data_records", 8, _int),
    ("duration_of_a_data_record", 8, _float),
    ("number_of_signals", 4, _int),
)


SIGNAL_HEADER = (
    ("label", 16, _str),
    ("transducer_type", 80, _str),
    ("physical_dimension", 8, _str),
    ("physical_minimum", 8, _float),
    ("physical_maximum", 8, _float),
    ("digital_minimum", 8, _int),
    ("digital_maximum", 8, _int),
    ("prefiltering", 80, _str),
    ("nr_of_samples_in_each_data_record", 8, _int),
    ("reserved", 32, _discard),
)

INT_SIZE = 2
HEADER_SIZE = sum(size for _, size, _ in HEADER)
SIGNAL_HEADER_SIZE = sum(size for _, size, _ in SIGNAL_HEADER)

Header = namedtuple("Header", [name for name, _, _ in HEADER] + ["signals"])
SignalHeader = namedtuple("SignalHeader", [name for name, _, _ in SIGNAL_HEADER])

MONTH_DICT = {
    1: "JAN",
    2: "FEB",
    3: "MAR",
    4: "APR",
    5: "MAY",
    6: "JUN",
    7: "JUL",
    8: "AUG",
    9: "SEP",
    10: "OCT",
    11: "NOV",
    12: "DEC",
}


def read_edf_header(fd):
    """
    Reads the header of an EDF file.

    Parameters:
        fd (str or file-like object): The file descriptor or the path to the EDF file.

    Returns:
        Header: The header of the EDF file, including information about the signals.

    Raises:
        FileNotFoundError: If the file specified by `fd` does not exist.
        ValueError: If `fd` is not a valid EDF file.
    """
    opened = False
    if isinstance(fd, str):
        opened = True
        fd = open(fd, "rb")

    header = [func(fd, size, name) for name, size, func in HEADER]
    number_of_signals = header[-1]
    signal_headers = [[] for _ in range(number_of_signals)]

    for name, size, func in SIGNAL_HEADER:
        for signal_header in signal_headers:
            signal_header.append(func(fd, size, name))

    header.append(tuple(starmap(SignalHeader, signal_headers)))

    if opened:
        fd.close()

    return Header(*header)


def read_edf_data(fd, header, chans="all"):
    """
    Reads EDF data from a file or file-like object.

    Parameters:
        fd (str or file-like object): The file path or file-like object to read the EDF data from.
        header (Header): The EDF header object containing information about the data.

    Returns:
        generator: A generator that yields each data record as a list of signals.

    Raises:
        IOError: If there was an error opening or reading the EDF file.
    """
    opened = False
    if isinstance(fd, str):
        fd = open(fd, "rb")
        opened = True

        start = 0
        end = header.number_of_data_records

        if chans == "all":
            chans = list(range(header.number_of_signals))

        data_record_length = sum(
            signal.nr_of_samples_in_each_data_record for signal in header.signals
        )

        if opened:
            fd.seek(
                HEADER_SIZE
                + header.number_of_signals * SIGNAL_HEADER_SIZE
                + start * data_record_length * INT_SIZE
            )

        for _ in range(start, end):
            a = np.fromfile(fd, count=data_record_length, dtype=np.int16)

            offset = 0
            data_record = []
            for chan_nr, signal in enumerate(header.signals):
                new_offset = offset + signal.nr_of_samples_in_each_data_record
                if chan_nr in chans:
                    data_record.append(a[offset:new_offset])
                offset = new_offset

            yield data_record

    if opened:
        fd.close()


def write_edf_header(fd, header):
    """
    Writes the EDF header to the specified file-like object or file path.

    Args:
        fd (str): (Relative) path to file to write.
        header: The header information to write.

    Raises:
        AssertionError: If the length of the value to write is not equal to the expected size.

    Returns:
        None
    """
    opened = False
    if isinstance(fd, str):
        fd = open(fd, "wb")
        opened = True

        for val, (name, size, _) in zip(header, HEADER, strict=False):
            if val is None:
                val = b" " * size

            if not isinstance(val, bytes):
                if (
                    name in {"startdate_of_recording", "starttime_of_recording"}
                ) and not isinstance(val, str):
                    h = val[0]
                    m = val[1]
                    s = val[2] % 100
                    val = f"{h:02d}.{m:02d}.{s:02d}"
                val = bytes(val, encoding="ascii").ljust(size, b" ")

            assert len(val) == size
            fd.write(val)

        for vals, (_, size, _) in zip(zip(*header.signals), SIGNAL_HEADER):  # noqa: B905
            for val in vals:
                if val is None:
                    val = b" " * size

                if not isinstance(val, bytes):
                    val = bytes(val, encoding="ascii").ljust(size, b" ")

                if len(val) > size:
                    try:
                        val = float(val)
                    except ValueError as e:
                        raise AssertionError(
                            f"{val} too long! Need to be shorter than {size} bytes."
                        ) from e
                    # convert float to scientific expression
                    precision = 2 if val >= 0 else 1
                    val = bytes(f"{val:.{precision}e}", encoding="ascii").ljust(
                        size, b" "
                    )

                assert len(val) == size, (
                    f"{val} too long! Need to be shorter than {size} bytes."
                )
                fd.write(val)

    if opened:
        fd.close()


def write_edf_data(fd, data_records):
    """Function to check and fix edf files according to EDF plus standards

    Args:
        fd (str): (Relative) path to file to write.
        data_records (array): Variable with data_records to write to edf file\
            is output from read_edf_data function

    """
    opened = False
    if isinstance(fd, str):
        opened = True
        fd = open(fd, "ab")
        for data_record in data_records:
            for signal in data_record:
                signal.tofile(fd)
    # try:

    if opened:
        fd.close()


def fix_edf_header(fd):
    """
    Fix the EDF header.

    Args:
        fd (file object): The file descriptor for the EDF file.

    Returns:
        None
    """

    if not (os.path.isfile(fd)):
        raise FileNotFoundError(fd)
    else:
        print(f"fixing header for {fd} ... ", end="", flush=True)

    header = read_edf_header(fd)
    data = read_edf_data(fd, header)

    something_to_fix = False
    if ":" in header.startdate_of_recording:
        warnings.warn(
            f"start date {header.startdate_of_recording} "
            "contains colon (:), changing to dot (.)"
        )
        header = header._replace(
            startdate_of_recording=header.startdate_of_recording.replace(":", ".")
        )
        something_to_fix = True

    if ":" in header.starttime_of_recording:
        warnings.warn(
            f"start time {header.starttime_of_recording}"
            "contains colon (:), changing to dot (.)"
        )
        header = header._replace(
            starttime_of_recording=header.starttime_of_recording.replace(":", ".")
        )
        something_to_fix = True

    for signal in header.signals:
        if signal.physical_maximum <= signal.physical_minimum:
            warnings.warn(
                f"channel {signal.label}: physical maximum "
                f"({signal.physical_maximum}) is smaller or equal "
                f"to physical minimum ({signal.physical_minimum})"
            )

        if signal.digital_maximum <= signal.digital_minimum:
            warnings.warn(
                f"channel {signal.label}: digital maximum "
                f"({signal.digital_maximum}) is smaller or equal "
                f"to digital minimum ({signal.digital_minimum})"
            )

    if something_to_fix:
        tmp_fd = fd + "tmp"
        write_edf_header(tmp_fd, header)
        write_edf_data(tmp_fd, data)

        assert os.path.getsize(tmp_fd) == os.path.getsize(fd)
        os.replace(tmp_fd, fd)

    print("done")


def get_patient_age(header):
    """Get the age of the patient in days from the header of the edf file.

    Parameters
    ----------
    header: Header
        The EDF header object containing information about the data.
    """
    # get the info
    for header_info, val in zip(HEADER, header, strict=False):
        field_name = header_info[0]
        if field_name == "local_patient_identification":
            lpi = val.split(" ")
            birthdate = lpi[2]
        elif field_name == "local_recording_identification":
            lri = val.split(" ")
            recdate = lri[1]
        elif field_name == "startdate_of_recording":
            startdate = val

    # parse the dates
    try:
        birthdate = dateparser.parse(birthdate, date_formats=["%d-%b-%Y"])
    except ValueError as err:
        raise ValueError(f"Wrong formatting of birthdate: {birthdate}") from err
    try:
        recdate = dateparser.parse(recdate, date_formats=["%d-%b-%Y"])
    except ValueError as err:
        raise ValueError(f"Wrong formatting of recording startdate: {recdate}") from err
    try:
        startdate = dateparser.parse(startdate, date_formats=["%d.%m.%y"])
    except ValueError as err:
        raise ValueError(f"Wrong formatting of startdate: {startdate}") from err
    # check consistency
    assert recdate == startdate, (
        f"These values should be equal (?): {recdate} ; {startdate}"
    )

    # compute the age in days
    age_in_days = (recdate - birthdate).days

    return age_in_days


def anonymize_edf_header(fd):
    """Function to anonymize edf files according to ENSEMBLE and BIDS standards.
    The output file will be appended with ANONYMIZED in the filename. Please
    make sure to only upload the anonymized files.


    Args:
    fd (str): (Relative) path to file to rename.

    """
    if not (os.path.isfile(fd)):
        raise FileNotFoundError(fd)
    else:
        print(f"anonymizing {fd} ... ", end="", flush=True)

    header = read_edf_header(fd)
    data = read_edf_data(fd, header)

    filename = os.path.splitext(os.path.basename(fd))[0]
    ext = os.path.splitext(os.path.basename(fd))[1]
    folder = os.path.dirname(fd)
    split_filename = filename.split("_")
    is_ensemble_approved = (
        split_filename[0][:4] == "sub-"
        and len(split_filename[0][4:]) == 10
        and ("E" in split_filename[0])
    )

    # define anonymized versions of the header fields
    if is_ensemble_approved:
        pseudo_code = split_filename[0][4:]
        anonymized_pid = pseudo_code + " X 01-JAN-1985 X"
    else:
        anonymized_pid = "X X 01-JAN-1985 X"

    # define the startdate as 01/01/1985 + the patient age
    age_in_days = get_patient_age(header)
    startdate = datetime(1985, 1, 1) + timedelta(age_in_days)

    # use MONTH DICT to bypass local language month abreviations
    startdate_str = f"{startdate.date().day:0>2}-{MONTH_DICT[startdate.date().month]}-{startdate.date().year:0>4}"
    anonymized_rid = f"Startdate {startdate_str} X X X"

    startdate_str = startdate.strftime("%d.%m.%y")
    anonymized_startdate = startdate_str
    # anonymized_starttime = "00.00.00"

    header = header._replace(
        local_patient_identification=anonymized_pid,
        local_recording_identification=anonymized_rid,
        startdate_of_recording=anonymized_startdate,
        # starttime_of_recording=anonymized_starttime,
    )

    fd_out = os.path.join(folder, filename + "_ANONYMIZED" + ext)
    write_edf_header(fd_out, header)
    write_edf_data(fd_out, data)

    print("done")


def rename_for_ensemble(fd):
    """Function to rename edf files according to ENSEMBLE and BIDS standards

    Args:
        fd (str): (Relative) path to file to rename.

    """
    if not os.path.isfile(fd):
        raise FileNotFoundError(fd)

    filedir = os.path.expanduser(os.path.dirname(fd))
    if not filedir:
        filedir = os.getcwd()

    filename = os.path.basename(fd)
    do_renaming = check_filename_ensemble(filename)

    if not (do_renaming):
        print("File already uses ENSEMBLE standards, no renaming required")
        return

    while True:
        print(f"changing name of {fd}")

        header = read_edf_header(fd)

        # get the new subject code
        subject_code = get_subject_code()

        # check type of acquisition
        acq = get_acquisition_type(header)

        # check type of session
        ses = get_session_type()

        split_new_filename = [subject_code, ses, acq, "run-1_eeg.edf"]
        new_filename = "_".join(split_new_filename)

        print(f"new filename is {new_filename}")
        correct_filename = input("Is this correct? [Y/n]: ")

        if correct_filename.lower() == "y":
            break

    # Create new directory and copy renamed file
    new_dirname = os.path.join(filedir, subject_code)
    new_filename = os.path.join(new_dirname, new_filename)

    if not os.path.isdir(new_dirname):
        os.mkdir(new_dirname)

    if os.path.isfile(new_filename):
        print("File already exists, not overwriting")
    else:
        shutil.copy(fd, new_filename)


def combine_aeeg_channels(fd_left, fd_right, new_filename="two_channel_aeeg"):
    """
    Combine left and right aEEG channels into a single edf file.

    Args:
        fd_left (str): The file path of the left aEEG channel.
        fd_right (str): The file path of the right aEEG channel.
        new_filename (str, optional): The name of the new combined file. Defaults to "two_channel_aeeg".

    Raises:
        FileNotFoundError: If fd_left or fd_right is not a valid file path.
    """
    if not os.path.isfile(fd_left):
        raise FileNotFoundError(fd_left)
    elif not os.path.isfile(fd_right):
        raise FileNotFoundError(fd_right)

    filename_left = os.path.basename(fd_left)
    filename_right = os.path.basename(fd_right)
    print(f"Combining {filename_left} and {filename_right} ... ", end="", flush=True)

    output_dir = os.path.dirname(fd_left)
    path_to_file = os.path.join(output_dir, new_filename + ".edf")

    hdr_left = read_edf_header(fd_left)
    hdr_right = read_edf_header(fd_right)

    opened = False
    if isinstance(fd_left, str):
        opened = True
        fd = open(fd_left, "rb")

    # create new header by combining left and right channel headers, get the
    # annotation channel from right channel
    header = [func(fd, size, name) for name, size, func in HEADER]

    # create new signal headers
    signal_headers_left = [hdr_left.signals[0]]
    signal_headers_right = list(hdr_right.signals)
    signal_headers = signal_headers_left + signal_headers_right
    header[-1] = len(signal_headers)
    header.append(tuple(starmap(SignalHeader, signal_headers)))

    # calculate new header length
    header_length = HEADER_SIZE + len(signal_headers) * SIGNAL_HEADER_SIZE
    header[5] = header_length

    # read in data from both left and right channels, read - if possible -
    # annotation channel from right channel edf file
    labels_left = [signal.label for signal in hdr_left.signals]
    chans = list(range(hdr_left.number_of_signals))
    if "EDF Annotations" in labels_left:
        chans.remove(labels_left.index("EDF Annotations"))

    data_left = list(read_edf_data(fd_left, hdr_left, chans=chans))
    data_right = list(read_edf_data(fd_right, hdr_right))

    # append channels
    data_all = append_channels(data_left, data_right)

    write_edf_header(path_to_file, Header(*header))
    write_edf_data(path_to_file, data_all)

    if opened:
        fd.close()

    print("done")


def append_channels(data_left, data_right):
    """
    This function takes two lists of data and appends the corresponding elements from the second list to the elements in the first list. It yields the appended elements.
    """
    for elements_left, elements_right in zip(data_left, data_right, strict=True):
        elements_left.extend(elements_right)
        yield elements_left


def check_filename_ensemble(filename):
    """
    Helper function to check filename and compare to the ENSEMBLE standard

     Args:
        fd (str): (Relative) path to file to rename.

    """
    split_filename = filename.split("_")
    do_renaming = True

    if (
        (split_filename[0] == "subj")
        and ("ses" in split_filename[2])
        and ("acq" in split_filename[3])
        and ("run" in split_filename[4])
        and (split_filename[-1] == "eeg.edf")
    ):
        do_renaming = False
        warnings.warn(
            "The filename already seems to adhere to the ensemble and BIDS standard "
        )
        continue_renaming = input("Are you sure you want to rename this file? [y/N]")
        do_renaming = continue_renaming.lower() == "y"

    return do_renaming


def get_subject_code():
    """
    Helper code to get subject code with user input
    """

    # Get centre code
    while True:
        centre_code = input("Please input your centre code [xxx]: ")
        if len(centre_code) != 3 or not centre_code.isdigit():
            print("Centre code must consist of three digits")
            continue
        break

    # Get subject number
    while True:
        subject_number = input("Please input your subject number [xxxxx]: ")
        if len(subject_number) != 5 or not subject_number.isdigit():
            print("Subject number must consist of five digits")
            continue
        break

    # Get sibling number
    while True:
        sibling_number = input("Please input the sibling number [x]: ")
        if len(sibling_number) != 1 or not sibling_number.isdigit():
            print("Sibling number must consist of a single digit")
            continue
        break

    subject_code = "sub-" + centre_code + "E" + subject_number + sibling_number

    return subject_code


def get_acquisition_type(header):
    """
    Helper code to get acquisition type with user input or header information.

    Args:
        header: The header information of the file.

    Returns:
        acq: The determined acquisition type.
    """
    # Check number of signals in file
    if header.number_of_signals <= 4:
        acq = "acq-aeeg"
        print("file automatically determined to be aEEG")
        correct_acq = input("is this correct? [Y/n]: ").lower()

        if correct_acq == "n":
            acq = "acq-ceeg"

    else:
        acq = "acq-ceeg"
        print("file automatically determined to be cEEG")
        correct_acq = input("is this correct? [Y/n]: ").lower()

        if correct_acq == "n":
            acq = "acq-aeeg"

    return acq


def get_session_type():
    """
    Helper code to get session type with user input
    """
    while 1:
        ses_string = (
            "During which session was this recordig taken? " + "[(d)iag/(f)ollowup]: "
        )
        ses = input(ses_string).lower()
        if ses in {"d", "diag"}:
            ses = "ses-diag"
            break
        elif ses in {"f", "followup"}:
            ses = "ses-term"
            break

    return ses
