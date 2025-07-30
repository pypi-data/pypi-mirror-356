"""MassIVE datasets."""

import logging
import re
import socket
import xml.etree.ElementTree as ET  # noqa: N817
from pathlib import Path

import requests

from .ftp import FTPParser
from .project import BaseProject

LOGGER = logging.getLogger(__name__)

UCSD_EDU = "massive.ucsd.edu"
FTP_UCSD_EDU = "massive-ftp.ucsd.edu"


class MassiveProject(BaseProject):
    """Retrieve information about a MassIVE project.

    MassIVE: `<https://massive.ucsd.edu>`_

    Parameters
    ----------
    msv_id : str
        The MassIVE identifier.
    local : str, pathlib.Path, or cloudpathlib.CloudPath, optional
        The local data directory in which the project files will be
        downloaded. In addition to local paths, paths to AWS S3,
        Google Cloud Storage, or Azure Blob Storage can be used.
    fetch : bool, optional
        Should ppx check the remote repository for updated metadata?
    timeout : float, optional
        The maximum amount of time to wait for a server response.

    Attributes
    ----------
    id : str
    local : Path object
    url : str
    title : str
    description : str
    metadata : dict
    fetch : bool
    timeout : float

    """

    _api = "https://datasetcache.gnps2.org/datasette/database.csv"
    _proxy_api = "https://massive.ucsd.edu/ProteoSAFe/proxi/v0.1/datasets/"

    def __init__(self, msv_id, local=None, fetch=False, timeout=10.0):
        """Instantiate a MSVDataset object"""
        super().__init__(msv_id, local, fetch, timeout)
        self._params = {
            "_stream": "on",
            "_sort": "filepath",
            "_size": "max",
            "sql": f'SELECT * FROM filename WHERE dataset = "{self.id}"',
        }

    def _validate_id(self, identifier):
        """Validate a MassIVE identifier.

        Parameters
        ----------
        identifier : str
            The project identifier to validate.

        Returns
        -------
        str
            The validated identifier.

        """
        identifier = str(identifier).upper()
        if not re.match("(MSV|RMSV)[0-9]{9}", identifier):
            raise ValueError("Malformed MassIVE identifier.")

        return identifier

    @property
    def url(self):
        """The FTP URL of the dataset."""
        if self._url is not None:
            return self._url

        res = requests.get(self._proxy_api + self.id, timeout=self.timeout)
        for link in res.json()["datasetLink"]:
            if link["accession"] == "MS:1002852":
                # Fix the incorrect arrival of FTP hostname
                # (some datasets' metadata may still have it)
                self._url = link["value"].replace(UCSD_EDU, FTP_UCSD_EDU)
                return self._url

        raise ValueError(f"No FTP link was found for {self.id}")

    @property
    def metadata(self):
        """The project metadata as a dictionary."""
        if self._metadata is None:
            remote_file = "ccms_parameters/params.xml"
            metadata_file = self.local / remote_file
            try:
                # Only fetch file if it doesn't exist and self.fetch is true:
                if metadata_file.exists():
                    assert self.fetch

                # Fetch the data from the remote repository:
                self.download(remote_file, force_=True, silent=True)

            except (AssertionError, socket.gaierror) as err:
                if not metadata_file.exists():
                    raise err

            # Parse the XML
            root = ET.parse(metadata_file).getroot()
            self._metadata = {e.attrib["name"]: e.text for e in root}

        return self._metadata

    @property
    def title(self):
        """The title of this project."""
        return self.metadata["desc"]

    @property
    def description(self):
        """A description of this project."""
        return self.metadata["dataset.comments"]

    def remote_files(self, glob=None):
        """List the project files in the remote repository.

        Parameters
        ----------
        glob : str, optional
            Use Unix wildcards to return specific files. For example,
            :code:`"*.mzML"` would return all of the mzML files.

        Returns
        -------
        list of str
            The remote files available for this project.

        """
        if (
            self.fetch
            or self._remote_files is None
            or len(self._remote_files) == 0
        ):
            try:
                self.remote_files_from_info()
            except (
                TimeoutError,
                ConnectionRefusedError,
                ConnectionResetError,
                socket.gaierror,
                socket.herror,
                EOFError,
                OSError,
                AssertionError,
            ):
                LOGGER.debug("Scraping the FTP server for files...")
                self._remote_files = self._parser.files

        if glob is not None:
            files = [f for f in self._remote_files if Path(f).match(glob)]
        else:
            files = self._remote_files

        return files

    def remote_files_from_info(self):
        """Retrieves files list from project's files info"""
        # First line is a CSV header
        # we are interested in the `filepath` column.
        header = self.file_info().splitlines()[0].split(",")

        # The column position is not guaranteed to be the next one (usi,
        # filepath,dataset,collection...),
        # so we need to detect it
        pos = header.index("filepath")

        info = self.file_info().splitlines()[1:]

        result = []
        sep = self.id + "/"
        for r in info:
            parts = r.split(",")
            path = parts[pos]
            # the MassiVE ID might be present in a path (not always)
            # handle it
            if sep in path:
                result.append(path.split(sep, 1)[1])
            else:
                result.append(path)

        self._remote_files = result

        assert self._remote_files

    def file_info(self):
        """Retrieve information about the project files.

        Returns
        -------
        str
            Information about the files in a CSV format.

        """
        file_info_path = self.local / ".file_info.csv"
        if file_info_path.exists() and not self.fetch:
            with file_info_path.open("r") as ref:
                return ref.read()

        res = requests.get(
            self._api,
            params=self._params,
            timeout=self.timeout,
        )

        if res.status_code != 200:
            raise requests.HTTPError(f"Error {res.status_code}: {res.text}")

        with file_info_path.open("w+", newline="") as ref:
            ref.write(res.text)

        return res.text


def list_projects(timeout=10.0):
    """List all available projects on MassIVE.

    MassIVE: `<https://massive.ucsd.edu>`_

    Parameters
    ----------
    timeout : float, optional
        The maximum amount of time to wait for a response from the server.

    Returns
    -------
    list of str
        A list of MassIVE identifiers.

    """
    url = "https://datasetcache.gnps2.org/datasette/database.csv"
    params = {"sql": "select distinct dataset from filename", "_size": "max"}
    try:
        res = requests.get(url, params, timeout=timeout).text.splitlines()[1:]
        res.sort()
        return res

    except (
        TimeoutError,
        ConnectionRefusedError,
        ConnectionResetError,
        socket.gaierror,
        socket.herror,
        EOFError,
        OSError,
    ):
        LOGGER.debug("Scraping the FTP server for projects...")

    parser = FTPParser(f"ftp://{FTP_UCSD_EDU}/", max_depth=1, timeout=timeout)
    return [d.split("/")[1] for d in parser.dirs if "/" in d]
