import requests
import os


class PreEpiSeizuresDBClient:
    """
    Client for interacting with the PreEpiSeizures API.

    Handles authentication and provides methods to query sessions,
    download records, and retrieve events.

    Warning
    -------
    The seizure timestamps returned by the API are aligned with **hospital recordings**.
    Wearable data may contain incorrect or unsynchronized timestamps.

    Reliable synchronization of wearable and hospital data is **not guaranteed**.
    You must implement your own synchronization method if aligning the two.

    Patients with known reliable wearable timestamps: 
    ['BLIW', 'BSEA', 'GPPF', 'OFUF', 'RGNI', 'UDZG', 'YIVL']
    """

    def __init__(self, api_url, username, password):
        """
        Initialize the client and authenticate with the API.

        Parameters
        ----------
        api_url : str
            Base URL of the API (e.g., "http://localhost:8000").
        username : str
            Username for API authentication.
        password : str
            Password for API authentication.
        """
        self.api_url = api_url.rstrip("/")
        self.token = self._get_token(username, password)
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def _get_token(self, username, password):
        """
        Authenticate and retrieve a JWT access token.

        Parameters
        ----------
        username : str
            Username for API authentication.
        password : str
            Password for API authentication.

        Returns
        -------
        str
            JWT access token.

        Raises
        ------
        HTTPError
            If authentication fails.
        """
        response = requests.post(
            f"{self.api_url}/token/",
            data={"username": username, "password": password}
        )
        response.raise_for_status()
        return response.json()["access_token"]

    def download_record(self, record_id, save_path=None):
        """
        Download a record by its ID.

        Parameters
        ----------
        record_id : int
            ID of the record to download.
        save_path : str, optional
            Directory path to save the file. If None, returns the file content.

        Returns
        -------
        str or bytes
            File path if saved, or bytes if not saved.

        Raises
        ------
        HTTPError
            If the request fails.
        """
        response = requests.get(
            f"{self.api_url}/download/{record_id}",
            headers=self.headers,
            stream=True
        )
        response.raise_for_status()

        content_disposition = response.headers['content-disposition']
        filename = content_disposition.split("filename=")[-1].strip('";')

        if save_path:
            with open(os.path.join(save_path, filename), "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"File saved as: {os.path.join(save_path, filename)}")
            return os.path.join(save_path, filename)
        else:
            return response.content

    def download_records(self, record_ids, save_zip_path):
        """
        Download multiple records as a ZIP archive.

        Parameters
        ----------
        record_ids : list of int
            List of record IDs to download.
        save_zip_path : str
            Directory path to save the ZIP file. The ZIP maintains original directory structure.

        Raises
        ------
        HTTPError
            If the request fails.
        """
        params = [("record_ids", fid) for fid in record_ids]
        response = requests.get(
            f"{self.api_url}/download/",
            headers=self.headers,
            params=params,
            stream=True
        )
        response.raise_for_status()
        content_disposition = response.headers['content-disposition']
        zipname = content_disposition.split("filename=")[-1].strip('";')

        with open(os.path.join(save_zip_path, zipname), "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"ZIPs saved as: {os.path.join(save_zip_path, zipname)}")

    def get_sessions(self, patient_code=None, event_types=None, modality=None):
        """
        Retrieve sessions filtered by patient code, event type, or modality.

        Parameters
        ----------
        patient_code : str
            Code identifying the patient.
        event_types : list, optional
            List with seizure type classification which the events should match (all must be present for the event to be selected). Choose from 'focal', 'aware', 'motor', 'automatisms', 'impaired awareness', 'tonic', 'to bilateral tonic-clonic', 'generalized', 'absence', 'tonic-clonic', 'non-motor', 'behavior arrest', 'not seizure' 
        modality : str, optional
            Modality of the record (e.g., 'report', 'wearable', 'hospital_eeg', or 'hospital_video').

        Returns
        -------
        list of dict
            List of session metadata.

        Raises
        ------
        HTTPError
            If the request fails.
        """
        response = requests.get(
            f"{self.api_url}/sessions/",
            headers=self.headers,
            params={"patient_code": patient_code,
                    "event_types": event_types,
                    "modality": modality}
        )
        response.raise_for_status()
        return response.json()

    def get_records(self, patient_code=None, session_date=None, session_id=None, modality=None):
        """
        Retrieve records filtered by patient code, session date or id, or modality.

        Parameters
        ----------
        patient_code : str, optional
            Code identifying the patient.
        session_date : str or datetime, optional
            Date/time of the session ('YYYY-MM-DD HH:MM:SS' format).
        session_id : int, optional
            ID of the session.
        modality : str, optional
            Modality of the record (e.g., 'report', 'wearable', 'hospital_eeg', or 'hospital_video').

        Returns
        -------
        list of dict
            List of matching records.

        Raises
        ------
        HTTPError
            If the request fails.
        """
        response = requests.get(
            f"{self.api_url}/records/",
            headers=self.headers,
            params={"patient_code": patient_code,
                    "session_date": session_date,
                    "session_id": session_id,
                    "modality": modality}
        )
        response.raise_for_status()
        return response.json()

    def get_events(self, patient_code=None, session_date=None, session_id=None, event_types=None):
        """
        Retrieve events filtered by patient code, session date, or session ID.

        Parameters
        ----------
        patient_code : str, optional
            Code identifying the patient.
        session_date : str or datetime, optional
            Date/time of the session (ISO format).
        session_id : int, optional
            ID of the session.
        event_types : list, optional
            List with seizure type classification which the events should match (all must be present for the event to be selected). Choose from 'focal', 'aware', 'motor', 'automatisms', 'impaired awareness', 'unknown awareness', 'tonic', 'to bilateral tonic-clonic', 'generalized', 'absence', 'tonic-clonic', 'non-motor', 'behavior arrest', 'not seizure', 'seizure','subclinical'

        Returns
        -------
        list of dict
            List of matching events.

        Raises
        ------
        HTTPError
            If the request fails.
        """
        response = requests.get(
            f"{self.api_url}/events/",
            headers=self.headers,
            params={"patient_code": patient_code,
                    "session_date": session_date, "session_id": session_id,
                    "event_types": event_types}
        )
        response.raise_for_status()
        return response.json()
