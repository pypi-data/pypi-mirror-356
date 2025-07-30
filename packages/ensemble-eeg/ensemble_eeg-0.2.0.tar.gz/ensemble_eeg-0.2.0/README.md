<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![PyPI version](https://badge.fury.io/py/ensemble-eeg.svg)](https://badge.fury.io/py/ensemble-eeg)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

<!-- TABLE OF CONTENTS -->
- [ENSEMBLE EEG](#ensemble-eeg)
  - [Getting started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
      - [Start python](#start-python)
      - [Anonymizing EDF-files](#anonymizing-edf-files)
      - [Fixing EDF headers](#fixing-edf-headers)
      - [Combine left and right aEEG channels into one single file](#combine-left-and-right-aeeg-channels-into-one-single-file)
      - [Rename EDF-files according to BIDS and ENSEMBLE standards](#rename-edf-files-according-to-bids-and-ensemble-standards)
    - [Example scripts for specific situations](#example-scripts-for-specific-situations)
        - [1) File is already .edf, but you do not know whether header is EDF+, the file is not anonymized, and not renamed](#1-file-is-already-edf-but-you-do-not-know-whether-header-is-edf-the-file-is-not-anonymized-and-not-renamed)
        - [2) Your file is .brm and you want to convert it to .edf](#2-your-file-is-brm-and-you-want-to-convert-it-to-edf)
        - [3) Your files are .edf, but left and right channels are separate](#3-your-files-are-edf-but-left-and-right-channels-are-separate)
        - [4) You want to anonymize multiple .edf files in the same directory](#4-you-want-to-anonymize-multiple-edf-files-in-the-same-directory)
        - [5) You want to convert multiple .brm files in the same directory](#5-you-want-to-convert-multiple-brm-files-in-the-same-directory)
  - [Acknowledgements](#acknowledgements)

<!-- ABOUT THE PROJECT -->
# ENSEMBLE EEG
Ensemble EEG is a library of EEG analysis tools for the ENSEMBLE study. As of
today it is focuses on 5 separate things:

- **Anonymizing** EDF files in accordance with the ENSEMBLE study and the
  requirements of [EDF+](https://www.edfplus.info/specs/edfplus.html)
- **Fixing** EDF headers to adhere to the [EDF+](https://www.edfplus.info/specs/edfplus.html) standard
- **Converting** BRM to [EDF+](https://www.edfplus.info/specs/edfplus.html) files
- **Combining** separate aEEG channels into one [EDF+](https://www.edfplus.info/specs/edfplus.html) file
- **Renaming** EEG files according to ENSEMBLE and [BIDS](https://bids-specification.readthedocs.io/en/stable/) standards

<!-- GETTING STARTED -->
## Getting started
### Prerequisites
The following is required for the use of this software
- **Python 3.10** & **pip**
  - For instructions, please refer to the following [link](https://github.com/PackeTsar/Install-Python/blob/master/README.md)

### Installation
```sh
python -m pip install ensemble_eeg
```

<!-- USAGE EXAMPLES -->
## Usage
#### Start python
1) From command line
   1) Open cmd / terminal / powershell or your preferred command line interpreter
   2) Type python or python3
2) Using your preferred python interpreter
   1) [Jupyter notebook](https://jupyter.org/install)
   2) [PyCharm](https://www.jetbrains.com/help/pycharm/installation-guide.html#standalone)
   3) [Spyder](https://docs.spyder-ide.org/current/installation.html)

#### Anonymizing EDF-files
```python
from ensemble_eeg import ensemble_edf
ensemble_edf.anonymize_edf_header("path/2/your/edf/file") # for windows users, type an r before the " to ensure the use of raw strings (r"path/2/your/edf/file")
```
#### Fixing EDF headers
```python
from ensemble_eeg import ensemble_edf
ensemble_edf.fix_edf_header("path/2/your/edf/file") # for windows users, type an r before the " to ensure the use of raw strings (r"path/2/your/edf/file")
```
#### Combine left and right aEEG channels into one single file
```python
from ensemble_eeg import ensemble_edf
ensemble_edf.combine_aeeg_channels('path/2/your/left/channel', 'path/2/your/right/channel', 'new_filename') # for windows users, type an r before the " to ensure the use of raw strings (r"path/2/your/edf/file")
```
#### Rename EDF-files according to BIDS and ENSEMBLE standards
```python
from ensemble_eeg import ensemble_edf
ensemble_edf.rename_for_ensemble('path/2/your/edf/file') # for windows users, type an r before the " to ensure the use of raw strings (r"path/2/your/edf/file")
```
### Example scripts for specific situations
##### 1) File is already .edf, but you do not know whether header is EDF+, the file is not anonymized, and not renamed
```python
from ensemble_eeg import ensemble_edf
file = 'path/2/your/edf/file' # for windows users, type an r before the " to ensure the use of raw strings (r"path/2/your/edf/file")
ensemble_edf.fix_edf_header(file)       # for header check
ensemble_edf.anonymize_edf_header(file) # for anonymization

anonymized_file = 'path/2/your/anonymized/edf/file' # for windows users, type an r before the " to ensure the use of raw strings (r"path/2/your/edf/file")
ensemble_edf.rename_for_ensemble(file)  # for renaming

```
##### 2) Your file is .brm and you want to convert it to .edf
```python
from ensemble_eeg import brm_to_edf
from ensemble_eeg import ensemble_edf
brm_file = 'path/2/your/brm/file' # for windows users, type an r before the " to ensure the use of raw strings (r"path/2/your/brm/file")
brm_to_edf.convert_brm_to_edf(brm_file)     # for conversion, output edf is already anonymized
edf_file = 'path/2/your/edf/file'           # check which file was made in previous step
ensemble_edf.rename_for_ensemble(edf_file)  # for renaming

```
##### 3) Your files are .edf, but left and right channels are separate
```python
from ensemble_eeg import ensemble_edf
left_file = 'path/2/your/left/edf/file' # for windows users, type an r before the " to ensure the use of raw strings (r"path/2/your/edf/file")
right_file = 'path/2/your/right/edf/file' # for windows, type an r before the " to ensure the use of raw strings (r"path/2/your/edf/file")
ensemble_edf.combine_aeeg_channels(left_file, right_file) # output is automatically anonymized
ensemble_edf.rename_for_ensemble(file)                    # for renaming

```
##### 4) You want to anonymize multiple .edf files in the same directory
```python
from ensemble_eeg import ensemble_edf
import glob
import os
edf_directory = 'path/2/your/left/edf/directory' # for windows users, type an r before the " to ensure the use of raw strings (r"path/2/your/edf/file")
edf_files = glob.glob(os.path.join(edf_directory, "*.edf"))
for file in edf_files:
      ensemble_edf.fix_edf_header(file)
      ensemble_edf.anonymize_edf_header(file)

      anonymized_filename = Path(file).stem + "_ANONYMIZED" + Path(file).suffix
      ensemble_edf.rename_for_ensemble(anonymized_filename)
```
##### 5) You want to convert multiple .brm files in the same directory
```python
from ensemble_eeg import brm_to_edf
import glob
import os
brm_directory = 'path/2/your/left/edf/directory' # for windows users, type an r before the " to ensure the use of raw strings (r"path/2/your/edf/file")
brm_files = glob.glob(os.path.join(brm_directory, "*.brm"))
for file in brm_files:
      brm_to_edf.convert_brm_to_edf(file)
```

For more scripts, please refer to the [demos](https://github.com/ensemble2/ensemble_eeg/tree/main/demos) folder

<!-- ACKNOWLEDGMENTS -->
## Acknowledgements
- [edfrd](https://github.com/somnonetz/edfrd)
- [Install-Python-Instructions](https://github.com/PackeTsar/Install-Python/tree/master)

Software development has been funded by [La Fondation Paralysie Cérébrale](https://www.fondationparalysiecerebrale.org/) under grant [ENSEMBLE](https://www.fondationparalysiecerebrale.org/ensemble-european-newborn-study-early-markers-better-life).
