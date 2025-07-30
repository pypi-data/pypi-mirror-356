import glob
import os
import shutil
import zipfile
from collections import Counter, namedtuple

import defusedxml.ElementTree as ET
import numpy as np

from ensemble_eeg import ensemble_edf


def convert_brm_to_edf(fd, is_fs_64hz=None):
    """
    Converts a BRM file to EDF format.

    Parameters:
        fd (str): The path to the BRM file.
        is_fs_64hz (bool, optional): Indicates whether the sampling frequency
            is 64 Hz. Defaults to None.

    Raises:
        ValueError: If the file is not found.

    Returns:
        None
    """
    filename = os.path.basename(fd)
    file_exists = os.path.isfile(fd)

    if file_exists:
        file_dir = os.path.dirname(fd)
        tmp_dir = os.path.join(file_dir, "tmp")
        if os.path.isdir(tmp_dir):
            shutil.rmtree(tmp_dir)

        print(f"{filename}")
        print("\tUnzipping to temporary directory")
        with zipfile.ZipFile(fd, "r") as zip_ref:
            zip_ref.extractall(tmp_dir)

        index_xml = os.path.join(tmp_dir, "BRM_Index.xml")
        index = parse_xml(index_xml)
        device_xml = os.path.join(tmp_dir, "Device.xml")
        device = parse_xml(device_xml)

        if is_fs_64hz is None:
            is_fs_64hz = (
                input("is the sampling frequency 64 Hz? [y/N]: ").lower() == "y"
            )

        if is_fs_64hz:
            dat_files_left = sorted(
                glob.glob(os.path.join(tmp_dir, "DATA_RAW_EEG_LEFT*.dat"))
            )
            dat_files_right = sorted(
                glob.glob(os.path.join(tmp_dir, "DATA_RAW_EEG_RIGHT*.dat"))
            )

        else:
            dat_files_left = sorted(
                glob.glob(os.path.join(tmp_dir, "DATA_RAW_EEG_ELECTRODE_LEFT*.dat"))
            )
            dat_files_right = sorted(
                glob.glob(os.path.join(tmp_dir, "DATA_RAW_EEG_ELECTRODE_RIGHT*.dat"))
            )

        n_data_files_left = len(dat_files_left)
        n_data_files_right = len(dat_files_right)

        assert n_data_files_left == n_data_files_right

        for i in range(n_data_files_left):
            both_dat_files = [dat_files_left[i], dat_files_right[i]]
            data = extract_brm_file(index, device, both_dat_files)

            if i == 0:
                output_filename = os.path.splitext(fd)[0] + ".edf"
            else:
                output_filename = os.path.splitext(fd)[0] + "_" + str(i) + ".edf"

            hdr = prepare_edf_header(data)
            signal_header = prepare_edf_signal_header(data, device)
            header = ensemble_edf.Header(*hdr, signal_header)

            # write header to file
            print(f"\tprint header to {output_filename}")
            ensemble_edf.write_edf_header(output_filename, header)

            # write data to file
            print(f"\tprint data records to {output_filename}")
            write_brm_data_to_edf(output_filename, data)

        print("\tremoving temporary directory")
        shutil.rmtree(tmp_dir)
    else:
        raise ValueError("file not found")


def parse_xml(xml):
    """
    Parse an XML file and return a named tuple representing the parsed XML.

    Parameters:
        xml (str): The path to the XML file to be parsed.

    Returns:
        Parsed_XML: A named tuple representing the parsed XML. The fields of the
            named tuple correspond to the unique XML tags found in the file. If
            a tag appears only once, the corresponding field of the named tuple
            will contain the text content of the tag. If a tag appears multiple
            times, the corresponding field of the named tuple will contain a
            list of named tuples, each representing one occurrence of the tag.
            The fields of the nested named tuples correspond to the unique tags
            found within the repeated tag, and the values of the fields
            correspond to the text content of the corresponding tags.

    Raises:
        ValueError: If the specified XML file does not exist.

    Example:
        >>> parse_xml('data.xml')
        Parsed_XML(tag_names=['tag1', 'tag2'], tag1='text1', tag2=[Tag2(tag3='text3', tag4='text4')])
    """
    file_exists = os.path.isfile(xml)

    if file_exists:
        tree = ET.parse(xml)
        root = tree.getroot()

        all_tags = [child.tag for child in root]
        tag_names = list(Counter(all_tags).keys())
        tag_dict = list(Counter(all_tags).items())

        Parsed_XML = namedtuple("ParsedXML", tag_names)
        parsed_xml = []
        counter = 0
        for name, vals in tag_dict:
            if vals == 1:
                parsed_xml.append(root[counter].text)
                counter += 1
            else:
                parsed_child = []
                child_elems = root.findall(name)
                for child_elem in child_elems:
                    child_elem_tags = [el.tag for el in child_elem]
                    child_elem_vals = [el.text for el in child_elem]
                    tup = namedtuple(child_elem.tag, child_elem_tags)
                    parsed_child.append(tup(*child_elem_vals))
                    counter += 1
                parsed_xml.append(parsed_child)

    else:
        raise ValueError("file not found")

    return Parsed_XML(*parsed_xml)


def extract_brm_file(index, device, dat_files):
    """
    Extracts data from BRM files based on the given index, device, and dat_files.

    Parameters:
        index (Index): The index object containing file descriptions.
        device (Device): The device to extract data for.
        dat_files (List[str]): The list of dat files to extract data from.

    Returns:
        List[List[Data]]: A list of data extracted from BRM files.
    """
    filenames = [fd.FileName for fd in index.FileDescription]

    data = [[] for _ in dat_files]

    for i, dat_file in enumerate(dat_files):
        df = os.path.basename(dat_file)
        file = index.FileDescription[filenames.index(df)]
        file = file._replace(FileName=dat_file)
        print(f"\textracting {df} datastream")
        data[i] = get_brm_data(file, device)

    return data


def get_brm_data(file, device):
    """
    Generates a named tuple containing the data from the given file and device.

    Parameters:
        file (namedtuple): The file containing the data.
        device (str): The device associated with the data.

    Returns:
        Data: A named tuple containing the data from the file, the sample rate, and the numerical data.
    """
    DAUSampleHz = 512

    Data = namedtuple("data", list(file._fields) + ["sampleHz", "data"])
    data = list(file)
    data.extend(
        (
            int(DAUSampleHz / int(file.SamplePeriod512thSeconds)),
            get_numerical_data(file, device),
        )
    )

    return Data(*data)


def get_numerical_data(file, device):
    """
    Reads numerical data from a file and returns it.

    Parameters:
        file (File): The file object representing the file to read from.
        device (str): The device to use for reading the file.

    Returns:
        np.ndarray: The numerical data read from the file.

    Raises:
        Exception: If the file format is unrecognized.
    """
    f = open(file.FileName, "rb")

    if file.FileType in {"FloatMappedToInt16", "Int16"}:
        data = np.fromfile(f, dtype=np.int16)
    elif file.FileType == "Float32":
        data = np.fromfile(f, dtype=np.float32)
    else:
        raise Exception(f"Unrecognized file format {file.FileType}")

    return data


def prepare_edf_header(data):
    """
    Generate the header for an EDF (European Data Format) file.

    Args:
        data: A list of objects containing the data for each channel.

    Returns:
        header: A list containing the header information for the EDF file.

    Raises:
        None.

    Examples:
        >>> data = [channel1, channel2]
        >>> prepare_edf_header(data)
        ['0', 'X X X X', 'Startdate X X X X', 'dd.mm.yy', 'hh.mm.ss',
        header_size, None, n_records, '1', n_signals]
    """
    n_channels = 2
    version = "0"
    PID = "X X X X"
    RID = "Startdate X X X X"

    start_date = "01.01.85"
    start_time = "00.00.00"

    bytes_in_header = (
        ensemble_edf.HEADER_SIZE + n_channels * ensemble_edf.SIGNAL_HEADER_SIZE
    )
    reserved = None
    fs = data[0].sampleHz
    n_records = int(np.floor(len(data[0].data) / fs))
    dur_data_record = "1"
    n_signals = len(data)
    header = [
        version,
        PID,
        RID,
        start_date,
        start_time,
        bytes_in_header,
        reserved,
        n_records,
        dur_data_record,
        n_signals,
    ]

    return header


def prepare_edf_signal_header(data, device):
    """
    Generate the signal headers for an EDF file based on the provided data
        and device.

    Parameters:
        data (list): A list of data objects.
        device (Device): The device object.

    Returns:
        tuple: A tuple of signal headers.
    """
    channel_ids = [channel.ID for channel in device.Channel]
    units = data[0].Units

    # replace non-ascii characters
    if "µ" in units:
        units = units.replace("µ", "u")

    signal_headers = [[] for _ in data]
    for i in range(len(data)):
        ichan = channel_ids.index(data[i].ChannelTitle)
        if data[i].ChannelTitle == "Left":
            label = "F3"
        elif data[i].ChannelTitle == "Right":
            label = "F4"

        transducer_type = None
        physical_dimension = units
        physical_min = round(-5e6 / float(device.Channel[ichan].Gain) / 2)
        physical_max = round(5e6 / float(device.Channel[ichan].Gain) / 2)
        digital_min = -(2**15)
        digital_max = 2**15 - 1
        prefiltering = None
        nr_samples = data[i].sampleHz
        reserved = None
        sig_header = [
            label,
            transducer_type,
            physical_dimension,
            physical_min,
            physical_max,
            digital_min,
            digital_max,
            prefiltering,
            nr_samples,
            reserved,
        ]
        signal_headers[i] = ensemble_edf.SignalHeader(*sig_header)

    return tuple(signal_headers)


def write_brm_data_to_edf(filename, data):
    """
    Write BRM data to EDF file.

    Args:
        filename (str): The name of the file to write the data to.
        data (list): A list of data objects.

    Returns:
        None
    """
    file_exists = os.path.isfile(filename)
    dat1 = data[0].data
    dat2 = data[1].data

    if file_exists:
        fs = data[0].sampleHz
        n_records = int(np.floor(len(data[0].data) / fs))
        fd = open(filename, "ab")

        index = 0
        for i_record in range(n_records):
            fd.write(dat1[index : (index + fs)])
            fd.write(dat2[index : (index + fs)])
            index = (i_record + 1) * fs

        fd.close()
