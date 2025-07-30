"""
DICOM Client.

This module provides a clean interface to pynetdicom functionality,
abstracting the details of DICOM networking.
"""
import os
import time
import tempfile
from typing import Dict, List, Any, Tuple

from pydicom import dcmread
from pydicom.dataset import Dataset
from pynetdicom import AE, evt, build_role
from pynetdicom.sop_class import (
    PatientRootQueryRetrieveInformationModelFind,
    StudyRootQueryRetrieveInformationModelFind,
    PatientRootQueryRetrieveInformationModelGet,
    PatientRootQueryRetrieveInformationModelMove,  # For C-MOVE
    StudyRootQueryRetrieveInformationModelGet,
    StudyRootQueryRetrieveInformationModelMove,    # For C-MOVE
    Verification,
    EncapsulatedPDFStorage
)

from .attributes import get_attributes_for_level

class DicomClient:
    """DICOM networking client that handles communication with DICOM nodes."""
    
    def __init__(self, host: str, port: int, calling_aet: str, called_aet: str):
        """Initialize DICOM client.
        
        Args:
            host: DICOM node hostname or IP
            port: DICOM node port
            calling_aet: Local AE title (our AE title)
            called_aet: Remote AE title (the node we're connecting to)
        """
        self.host = host
        self.port = port
        self.called_aet = called_aet
        self.calling_aet = calling_aet
        
        # Create the Application Entity
        self.ae = AE(ae_title=calling_aet)
        
        # Add the necessary presentation contexts
        self.ae.add_requested_context(Verification)
        self.ae.add_requested_context(PatientRootQueryRetrieveInformationModelFind)
        self.ae.add_requested_context(PatientRootQueryRetrieveInformationModelGet)
        self.ae.add_requested_context(PatientRootQueryRetrieveInformationModelMove)
        self.ae.add_requested_context(StudyRootQueryRetrieveInformationModelFind)
        self.ae.add_requested_context(StudyRootQueryRetrieveInformationModelGet)
        self.ae.add_requested_context(StudyRootQueryRetrieveInformationModelMove)
        
        # Add specific storage context for PDF - instead of adding all storage contexts
        self.ae.add_requested_context(EncapsulatedPDFStorage)
    
    def verify_connection(self) -> Tuple[bool, str]:
        """Verify connectivity to the DICOM node using C-ECHO.
        
        Returns:
            Tuple of (success, message)
        """
        # Associate with the DICOM node
        assoc = self.ae.associate(self.host, self.port, ae_title=self.called_aet)
        
        if assoc.is_established:
            # Send C-ECHO request
            status = assoc.send_c_echo()
            
            # Release the association
            assoc.release()
            
            if status and status.Status == 0:
                return True, f"Connection successful to {self.host}:{self.port} (Called AE: {self.called_aet}, Calling AE: {self.calling_aet})"
            else:
                return False, f"C-ECHO failed with status: {status.Status if status else 'None'}"
        else:
            return False, f"Failed to associate with DICOM node at {self.host}:{self.port} (Called AE: {self.called_aet}, Calling AE: {self.calling_aet})"
    
    def find(self, query_dataset: Dataset, query_model) -> List[Dict[str, Any]]:
        """Execute a C-FIND request.
        
        Args:
            query_dataset: Dataset containing query parameters
            query_model: DICOM query model (Patient/StudyRoot)
        
        Returns:
            List of dictionaries containing query results
        
        Raises:
            Exception: If association fails
        """
        # Associate with the DICOM node
        assoc = self.ae.associate(self.host, self.port, ae_title=self.called_aet)
        
        if not assoc.is_established:
            raise Exception(f"Failed to associate with DICOM node at {self.host}:{self.port} (Called AE: {self.called_aet}, Calling AE: {self.calling_aet})")
        
        results = []
        
        try:
            # Send C-FIND request
            responses = assoc.send_c_find(query_dataset, query_model)
            
            for (status, dataset) in responses:
                if status and status.Status == 0xFF00:  # Pending
                    if dataset:
                        results.append(self._dataset_to_dict(dataset))
        finally:
            # Always release the association
            assoc.release()
        
        return results
    
    def query_patient(self, patient_id: str = None, name_pattern: str = None, 
                     birth_date: str = None, attribute_preset: str = "standard",
                     additional_attrs: List[str] = None, exclude_attrs: List[str] = None) -> List[Dict[str, Any]]:
        """Query for patients matching criteria.
        
        Args:
            patient_id: Patient ID
            name_pattern: Patient name pattern (can include wildcards * and ?)
            birth_date: Patient birth date (YYYYMMDD)
            attribute_preset: Attribute preset (minimal, standard, extended)
            additional_attrs: Additional attributes to include
            exclude_attrs: Attributes to exclude
            
        Returns:
            List of matching patient records
        """
        # Create query dataset
        ds = Dataset()
        ds.QueryRetrieveLevel = "PATIENT"
        
        # Add query parameters if provided
        if patient_id:
            ds.PatientID = patient_id
            
        if name_pattern:
            ds.PatientName = name_pattern
            
        if birth_date:
            ds.PatientBirthDate = birth_date
        
        # Add attributes based on preset
        attrs = get_attributes_for_level("patient", attribute_preset, additional_attrs, exclude_attrs)
        for attr in attrs:
            if not hasattr(ds, attr):
                setattr(ds, attr, "")
        
        # Execute query
        return self.find(ds, PatientRootQueryRetrieveInformationModelFind)
    
    def query_study(self, patient_id: str = None, study_date: str = None, 
                   modality: str = None, study_description: str = None, 
                   accession_number: str = None, study_instance_uid: str = None,
                   attribute_preset: str = "standard", additional_attrs: List[str] = None, 
                   exclude_attrs: List[str] = None) -> List[Dict[str, Any]]:
        """Query for studies matching criteria.
        
        Args:
            patient_id: Patient ID
            study_date: Study date or range (YYYYMMDD or YYYYMMDD-YYYYMMDD)
            modality: Modalities in study
            study_description: Study description (can include wildcards)
            accession_number: Accession number
            study_instance_uid: Study Instance UID
            attribute_preset: Attribute preset (minimal, standard, extended)
            additional_attrs: Additional attributes to include
            exclude_attrs: Attributes to exclude
            
        Returns:
            List of matching study records
        """
        # Create query dataset
        ds = Dataset()
        ds.QueryRetrieveLevel = "STUDY"
        
        # Add query parameters if provided
        if patient_id:
            ds.PatientID = patient_id
            
        if study_date:
            ds.StudyDate = study_date
            
        if modality:
            ds.ModalitiesInStudy = modality
            
        if study_description:
            ds.StudyDescription = study_description
            
        if accession_number:
            ds.AccessionNumber = accession_number
            
        if study_instance_uid:
            ds.StudyInstanceUID = study_instance_uid
        
        # Add attributes based on preset
        attrs = get_attributes_for_level("study", attribute_preset, additional_attrs, exclude_attrs)
        for attr in attrs:
            if not hasattr(ds, attr):
                setattr(ds, attr, "")
        
        # Execute query
        return self.find(ds, StudyRootQueryRetrieveInformationModelFind)
    
    def query_series(self, study_instance_uid: str, series_instance_uid: str = None,
                    modality: str = None, series_number: str = None, 
                    series_description: str = None, attribute_preset: str = "standard",
                    additional_attrs: List[str] = None, exclude_attrs: List[str] = None) -> List[Dict[str, Any]]:
        """Query for series matching criteria.
        
        Args:
            study_instance_uid: Study Instance UID (required)
            series_instance_uid: Series Instance UID
            modality: Modality (e.g. "CT", "MR")
            series_number: Series number
            series_description: Series description (can include wildcards)
            attribute_preset: Attribute preset (minimal, standard, extended)
            additional_attrs: Additional attributes to include
            exclude_attrs: Attributes to exclude
            
        Returns:
            List of matching series records
        """
        # Create query dataset
        ds = Dataset()
        ds.QueryRetrieveLevel = "SERIES"
        ds.StudyInstanceUID = study_instance_uid
        
        # Add query parameters if provided
        if series_instance_uid:
            ds.SeriesInstanceUID = series_instance_uid
            
        if modality:
            ds.Modality = modality
            
        if series_number:
            ds.SeriesNumber = series_number
            
        if series_description:
            ds.SeriesDescription = series_description
        
        # Add attributes based on preset
        attrs = get_attributes_for_level("series", attribute_preset, additional_attrs, exclude_attrs)
        for attr in attrs:
            if not hasattr(ds, attr):
                setattr(ds, attr, "")
        
        # Execute query
        return self.find(ds, StudyRootQueryRetrieveInformationModelFind)
    
    def query_instance(self, series_instance_uid: str, sop_instance_uid: str = None,
                      instance_number: str = None, attribute_preset: str = "standard",
                      additional_attrs: List[str] = None, exclude_attrs: List[str] = None) -> List[Dict[str, Any]]:
        """Query for instances matching criteria.
        
        Args:
            series_instance_uid: Series Instance UID (required)
            sop_instance_uid: SOP Instance UID
            instance_number: Instance number
            attribute_preset: Attribute preset (minimal, standard, extended)
            additional_attrs: Additional attributes to include
            exclude_attrs: Attributes to exclude
            
        Returns:
            List of matching instance records
        """
        # Create query dataset
        ds = Dataset()
        ds.QueryRetrieveLevel = "IMAGE"
        ds.SeriesInstanceUID = series_instance_uid
        
        # Add query parameters if provided
        if sop_instance_uid:
            ds.SOPInstanceUID = sop_instance_uid
            
        if instance_number:
            ds.InstanceNumber = instance_number
        
        # Add attributes based on preset
        attrs = get_attributes_for_level("instance", attribute_preset, additional_attrs, exclude_attrs)
        for attr in attrs:
            if not hasattr(ds, attr):
                setattr(ds, attr, "")
        
        # Execute query
        return self.find(ds, StudyRootQueryRetrieveInformationModelFind)
    
    def move_series(
            self, 
            destination_ae: str,
            series_instance_uid: str
        ) -> dict:
        """Move a DICOM series to another DICOM node using C-MOVE.
        
        This method performs a simple C-MOVE operation to transfer a specific series
        to a destination DICOM node.
        
        Args:
            destination_ae: AE title of the destination DICOM node
            series_instance_uid: Series Instance UID to be moved
            
        Returns:
            Dictionary with operation status:
            {
                "success": bool,
                "message": str,
                "completed": int,  # Number of successful transfers
                "failed": int,     # Number of failed transfers
                "warning": int     # Number of warnings
            }
        """
        # Create query dataset for series level
        ds = Dataset()
        ds.QueryRetrieveLevel = "SERIES"
        ds.SeriesInstanceUID = series_instance_uid
        
        # Associate with the DICOM node
        assoc = self.ae.associate(self.host, self.port, ae_title=self.called_aet)
        
        if not assoc.is_established:
            return {
                "success": False,
                "message": f"Failed to associate with DICOM node at {self.host}:{self.port}",
                "completed": 0,
                "failed": 0,
                "warning": 0
            }
        
        result = {
            "success": False,
            "message": "C-MOVE operation failed",
            "completed": 0,
            "failed": 0,
            "warning": 0
        }
        
        try:
            # Send C-MOVE request with the destination AE title
            responses = assoc.send_c_move(
                ds, 
                destination_ae, 
                PatientRootQueryRetrieveInformationModelMove
            )
            
            # Process the responses
            for (status, dataset) in responses:
                if status:
                    # Record the sub-operation counts if available
                    if hasattr(status, 'NumberOfCompletedSuboperations'):
                        result["completed"] = status.NumberOfCompletedSuboperations
                    if hasattr(status, 'NumberOfFailedSuboperations'):
                        result["failed"] = status.NumberOfFailedSuboperations
                    if hasattr(status, 'NumberOfWarningSuboperations'):
                        result["warning"] = status.NumberOfWarningSuboperations
                    
                    # Check the status code
                    if status.Status == 0x0000:  # Success
                        result["success"] = True
                        result["message"] = "C-MOVE operation completed successfully"
                    elif status.Status == 0x0001 or status.Status == 0xB000:  # Success with warnings
                        result["success"] = True
                        result["message"] = "C-MOVE operation completed with warnings or failures"
                    elif status.Status == 0xA801:  # Refused: Move destination unknown
                        result["message"] = f"C-MOVE refused: Destination '{destination_ae}' unknown"
                    else:
                        result["message"] = f"C-MOVE failed with status 0x{status.Status:04X}"
                        
                    # If we got a dataset with an error comment, add it
                    if dataset and hasattr(dataset, 'ErrorComment'):
                        result["message"] += f": {dataset.ErrorComment}"
        
        finally:
            # Always release the association
            assoc.release()
        
        return result

    def move_study(
            self, 
            destination_ae: str,
            study_instance_uid: str
        ) -> dict:
        """Move a DICOM study to another DICOM node using C-MOVE.
        
        This method performs a simple C-MOVE operation to transfer a specific study
        to a destination DICOM node.
        
        Args:
            destination_ae: AE title of the destination DICOM node
            study_instance_uid: Study Instance UID to be moved
            
        Returns:
            Dictionary with operation status:
            {
                "success": bool,
                "message": str,
                "completed": int,  # Number of successful transfers
                "failed": int,     # Number of failed transfers
                "warning": int     # Number of warnings
            }
        """
        # Create query dataset for study level
        ds = Dataset()
        ds.QueryRetrieveLevel = "STUDY"
        ds.StudyInstanceUID = study_instance_uid
        
        # Associate with the DICOM node
        assoc = self.ae.associate(self.host, self.port, ae_title=self.called_aet)
        
        if not assoc.is_established:
            return {
                "success": False,
                "message": f"Failed to associate with DICOM node at {self.host}:{self.port}",
                "completed": 0,
                "failed": 0,
                "warning": 0
            }
        
        result = {
            "success": False,
            "message": "C-MOVE operation failed",
            "completed": 0,
            "failed": 0,
            "warning": 0
        }
        
        try:
            # Send C-MOVE request with the destination AE title
            responses = assoc.send_c_move(
                ds, 
                destination_ae, 
                PatientRootQueryRetrieveInformationModelMove
            )
            
            # Process the responses
            for (status, dataset) in responses:
                if status:
                    # Record the sub-operation counts if available
                    if hasattr(status, 'NumberOfCompletedSuboperations'):
                        result["completed"] = status.NumberOfCompletedSuboperations
                    if hasattr(status, 'NumberOfFailedSuboperations'):
                        result["failed"] = status.NumberOfFailedSuboperations
                    if hasattr(status, 'NumberOfWarningSuboperations'):
                        result["warning"] = status.NumberOfWarningSuboperations
                    
                    # Check the status code
                    if status.Status == 0x0000:  # Success
                        result["success"] = True
                        result["message"] = "C-MOVE operation completed successfully"
                    elif status.Status == 0x0001 or status.Status == 0xB000:  # Success with warnings
                        result["success"] = True
                        result["message"] = "C-MOVE operation completed with warnings or failures"
                    elif status.Status == 0xA801:  # Refused: Move destination unknown
                        result["message"] = f"C-MOVE refused: Destination '{destination_ae}' unknown"
                    else:
                        result["message"] = f"C-MOVE failed with status 0x{status.Status:04X}"
                        
                    # If we got a dataset with an error comment, add it
                    if dataset and hasattr(dataset, 'ErrorComment'):
                        result["message"] += f": {dataset.ErrorComment}"
        
        finally:
            # Always release the association
            assoc.release()
        
        return result
    def extract_pdf_text_from_dicom(
            self, 
            study_instance_uid: str,
            series_instance_uid: str,
            sop_instance_uid: str
        ) -> Dict[str, Any]:
        """Retrieve a DICOM instance with encapsulated PDF and extract its text content.
        
        This function retrieves a DICOM instance that contains an encapsulated PDF document
        using C-GET and extracts the PDF content using PyPDF2 to parse the text content.
        
        Args:
            study_instance_uid: Study Instance UID
            series_instance_uid: Series Instance UID
            sop_instance_uid: SOP Instance UID
            
        Returns:
            Dictionary with extracted text information and status:
            {
                "success": bool,
                "message": str,
                "text_content": str,
                "file_path": str  # Path to the temporary DICOM file
            }
        """
        # Create temporary directory for storing retrieved files
        temp_dir = tempfile.mkdtemp()
        
        # Create dataset for C-GET query
        ds = Dataset()
        ds.QueryRetrieveLevel = "IMAGE"
        ds.StudyInstanceUID = study_instance_uid
        ds.SeriesInstanceUID = series_instance_uid
        ds.SOPInstanceUID = sop_instance_uid
        
        # Define a handler for C-STORE operations during C-GET
        received_files = []
        
        def handle_store(event):
            """Handle C-STORE operations during C-GET"""
            ds = event.dataset
            sop_instance = ds.SOPInstanceUID if hasattr(ds, 'SOPInstanceUID') else "unknown"
            
            # Ensure we have file meta information
            if not hasattr(ds, 'file_meta') or not hasattr(ds.file_meta, 'TransferSyntaxUID'):
                from pydicom.dataset import FileMetaDataset
                if not hasattr(ds, 'file_meta'):
                    ds.file_meta = FileMetaDataset()
                
                if event.context.transfer_syntax:
                    ds.file_meta.TransferSyntaxUID = event.context.transfer_syntax
                else:
                    ds.file_meta.TransferSyntaxUID = "1.2.840.10008.1.2.1"
                
                if not hasattr(ds.file_meta, 'MediaStorageSOPClassUID') and hasattr(ds, 'SOPClassUID'):
                    ds.file_meta.MediaStorageSOPClassUID = ds.SOPClassUID
                
                if not hasattr(ds.file_meta, 'MediaStorageSOPInstanceUID') and hasattr(ds, 'SOPInstanceUID'):
                    ds.file_meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID
            
            # Save the dataset to file
            file_path = os.path.join(temp_dir, f"{sop_instance}.dcm")
            ds.save_as(file_path, write_like_original=False)
            received_files.append(file_path)
            
            return 0x0000  # Success
        
        # Define event handlers - using the proper format for pynetdicom
        handlers = [(evt.EVT_C_STORE, handle_store)]
        
        # Create an SCP/SCU Role Selection Negotiation item for PDF Storage
        # This is needed to indicate our AE can act as an SCP (receiver) for C-STORE operations
        # during the C-GET operation
        role = build_role(EncapsulatedPDFStorage, scp_role=True)
        
        # Associate with the DICOM node, providing the event handlers during association
        # This is the correct way to handle events in pynetdicom
        assoc = self.ae.associate(
            self.host, 
            self.port, 
            ae_title=self.called_aet,
            evt_handlers=handlers,
            ext_neg=[role]  # Add extended negotiation for SCP/SCU role selection
        )
        
        if not assoc.is_established:
            return {
                "success": False,
                "message": f"Failed to associate with DICOM node at {self.host}:{self.port}",
                "text_content": "",
                "file_path": ""
            }
        
        success = False
        message = "C-GET operation failed"
        pdf_path = ""
        extracted_text = ""
        
        try:
            # Send C-GET request - without evt_handlers parameter since we provided them during association
            responses = assoc.send_c_get(ds, PatientRootQueryRetrieveInformationModelGet)
            
            for (status, dataset) in responses:
                if status:
                    status_int = status.Status if hasattr(status, 'Status') else 0
                    
                    if status_int == 0x0000:  # Success
                        success = True
                        message = "C-GET operation completed successfully"
                    elif status_int == 0xFF00:  # Pending
                        success = True  # Still processing
                        message = "C-GET operation in progress"
        finally:
            # Always release the association
            assoc.release()
        
        # Process received files
        if received_files:
            dicom_file = received_files[0]
            
            # Read the DICOM file
            ds = dcmread(dicom_file)
            
            # Check if it's an encapsulated PDF
            if (hasattr(ds, 'SOPClassUID') and 
                ds.SOPClassUID == '1.2.840.10008.5.1.4.1.1.104.1'):  # Encapsulated PDF Storage
                
                # Extract the PDF data
                pdf_data = ds.EncapsulatedDocument
                
                # Write to a temporary file
                pdf_path = os.path.join(temp_dir, "extracted.pdf")
                with open(pdf_path, 'wb') as pdf_file:
                    pdf_file.write(pdf_data)
                
                import PyPDF2
                
                # Extract text from the PDF
                with open(pdf_path, 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    text_parts = []
                    
                    # Extract text from each page
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        text_parts.append(page.extract_text())
                    
                    extracted_text = "\n".join(text_parts)
                
                return {
                    "success": True,
                    "message": "Successfully extracted text from PDF in DICOM",
                    "text_content": extracted_text,
                    "file_path": dicom_file
                }
            else:
                message = "Retrieved DICOM instance does not contain an encapsulated PDF"
                success = False
        
        return {
            "success": success,
            "message": message,
            "text_content": extracted_text,
            "file_path": received_files[0] if received_files else ""
        }
    
    def retrieve_dicom_instances(
            self,
            series_instance_uid: str,
            output_directory: str = None,
            sop_instance_uid: str = None,
            study_instance_uid: str = None
        ) -> Dict[str, Any]:
        """Retrieve DICOM instances from the server and save them to a local directory.
        
        This method uses C-GET to download DICOM instances from the server to a local
        directory. You can retrieve an entire series or specific instances within a series.
        
        Files are saved with meaningful names based on DICOM metadata:
        Format: PatientID_PatientName_StudyDate_Modality_SeriesDescription_InstXXX.dcm
        Example: "12345_SMITH_20230215_CT_CHEST_AXIAL_Inst001.dcm"
        
        Args:
            series_instance_uid: Series Instance UID to retrieve (required)
            output_directory: Local directory to save the DICOM files (optional, uses temp dir if not provided)
            sop_instance_uid: Specific SOP Instance UID to retrieve (optional, retrieves all if not provided)
            study_instance_uid: Study Instance UID (optional, helps with organization)
            
        Returns:
            Dictionary with operation status and details:
            {
                "success": bool,
                "message": str,
                "output_directory": str,
                "files_retrieved": list,  # List of retrieved file paths
                "total_files": int,
                "total_size_mb": float
            }
        """
        # Create output directory if not provided
        if output_directory is None:
            output_directory = tempfile.mkdtemp(prefix="dicom_retrieve_")
        else:
            os.makedirs(output_directory, exist_ok=True)
        
        # Create dataset for C-GET query
        ds = Dataset()
        if sop_instance_uid:
            # Retrieve specific instance
            ds.QueryRetrieveLevel = "IMAGE"
            ds.SeriesInstanceUID = series_instance_uid
            ds.SOPInstanceUID = sop_instance_uid
            if study_instance_uid:
                ds.StudyInstanceUID = study_instance_uid
        else:
            # Retrieve entire series
            ds.QueryRetrieveLevel = "SERIES"
            ds.SeriesInstanceUID = series_instance_uid
            if study_instance_uid:
                ds.StudyInstanceUID = study_instance_uid
        
        # Track retrieved files
        retrieved_files = []
        total_size_bytes = 0
        
        def handle_store(event):
            """Handle C-STORE operations during C-GET"""
            dataset = event.dataset
            sop_instance = dataset.SOPInstanceUID if hasattr(dataset, 'SOPInstanceUID') else "unknown"
            
            # Ensure we have proper file meta information
            if not hasattr(dataset, 'file_meta') or not hasattr(dataset.file_meta, 'TransferSyntaxUID'):
                from pydicom.dataset import FileMetaDataset
                if not hasattr(dataset, 'file_meta'):
                    dataset.file_meta = FileMetaDataset()
                
                if event.context.transfer_syntax:
                    dataset.file_meta.TransferSyntaxUID = event.context.transfer_syntax
                else:
                    dataset.file_meta.TransferSyntaxUID = "1.2.840.10008.1.2.1"  # Implicit VR Little Endian
                
                if not hasattr(dataset.file_meta, 'MediaStorageSOPClassUID') and hasattr(dataset, 'SOPClassUID'):
                    dataset.file_meta.MediaStorageSOPClassUID = dataset.SOPClassUID
                
                if not hasattr(dataset.file_meta, 'MediaStorageSOPInstanceUID') and hasattr(dataset, 'SOPInstanceUID'):
                    dataset.file_meta.MediaStorageSOPInstanceUID = dataset.SOPInstanceUID
            
            def clean_filename(text, max_length=50):
                """Clean text for use in filename"""
                if not text:
                    return "unknown"
                # Remove or replace invalid filename characters
                import re
                text = str(text).strip()
                text = re.sub(r'[<>:"/\\|?*\[\]]', '_', text)  # Replace invalid chars
                text = re.sub(r'\s+', '_', text)  # Replace spaces with underscores
                text = re.sub(r'_+', '_', text)  # Replace multiple underscores with single
                text = text.strip('_')  # Remove leading/trailing underscores
                return text[:max_length] if len(text) > max_length else text
            
            # Extract meaningful information for filename
            patient_id = clean_filename(getattr(dataset, 'PatientID', ''), 15)
            patient_name = clean_filename(str(getattr(dataset, 'PatientName', '')).split('^')[0], 15) if hasattr(dataset, 'PatientName') else ''
            study_date = clean_filename(getattr(dataset, 'StudyDate', ''), 8)
            series_number = clean_filename(getattr(dataset, 'SeriesNumber', ''), 5)
            series_description = clean_filename(getattr(dataset, 'SeriesDescription', ''), 20)
            modality = clean_filename(getattr(dataset, 'Modality', ''), 5)
            instance_number = clean_filename(getattr(dataset, 'InstanceNumber', ''), 5)
            
            # Build filename components
            filename_parts = []
            
            # Add patient info
            if patient_id and patient_id != 'unknown':
                filename_parts.append(patient_id)
            if patient_name and patient_name != 'unknown':
                filename_parts.append(patient_name)
            
            # Add study date
            if study_date and study_date != 'unknown':
                filename_parts.append(study_date)
            
            # Add series info
            if modality and modality != 'unknown':
                filename_parts.append(modality)
            if series_description and series_description != 'unknown':
                filename_parts.append(series_description)
            elif series_number and series_number != 'unknown':
                filename_parts.append(f"Series{series_number}")
            
            # Add instance number
            if instance_number and instance_number != 'unknown':
                filename_parts.append(f"Inst{instance_number}")
            
            # If we couldn't extract meaningful info, fall back to SOP Instance UID
            if not filename_parts:
                filename_parts.append(sop_instance[:20])  # Use first 20 chars of SOP Instance UID
            
            # Join parts and add extension
            base_filename = '_'.join(filename_parts)
            
            # Ensure filename is not too long (max 255 chars for most filesystems)
            max_base_length = 240  # Leave room for .dcm extension and potential numbering
            if len(base_filename) > max_base_length:
                base_filename = base_filename[:max_base_length]
            
            filename = f"{base_filename}.dcm"
            file_path = os.path.join(output_directory, filename)
            
            # Handle filename conflicts by adding a number suffix
            counter = 1
            original_file_path = file_path
            while os.path.exists(file_path):
                base_name = base_filename
                if len(base_name) > max_base_length - 10:  # Leave room for counter
                    base_name = base_name[:max_base_length - 10]
                filename = f"{base_name}_{counter:03d}.dcm"
                file_path = os.path.join(output_directory, filename)
                counter += 1
            
            # Save the dataset
            try:
                dataset.save_as(file_path, write_like_original=False)
                file_size = os.path.getsize(file_path)
                retrieved_files.append({
                    "file_path": file_path,
                    "sop_instance_uid": sop_instance,
                    "size_bytes": file_size
                })
                nonlocal total_size_bytes
                total_size_bytes += file_size
            except Exception as e:
                print(f"Error saving DICOM file {filename}: {str(e)}")
                return 0xA700  # Failure - Out of Resources
            
            return 0x0000  # Success
        
        # Set up event handlers
        handlers = [(evt.EVT_C_STORE, handle_store)]
        
        # Add role negotiation for common storage SOP classes
        from pynetdicom.sop_class import (
            CTImageStorage, MRImageStorage, ComputedRadiographyImageStorage,
            DigitalXRayImageStorageForPresentation, DigitalXRayImageStorageForProcessing,
            UltrasoundImageStorage, SecondaryCaptureImageStorage
        )
        
        # Define common storage SOP classes that we might receive
        storage_classes = [
            CTImageStorage, MRImageStorage, ComputedRadiographyImageStorage,
            DigitalXRayImageStorageForPresentation, DigitalXRayImageStorageForProcessing,
            UltrasoundImageStorage, SecondaryCaptureImageStorage, EncapsulatedPDFStorage
        ]
        
        # Build role negotiations
        roles = [build_role(sop_class, scp_role=True) for sop_class in storage_classes]
        
        # Associate with the DICOM node
        assoc = self.ae.associate(
            self.host,
            self.port,
            ae_title=self.called_aet,
            evt_handlers=handlers,
            ext_neg=roles
        )
        
        if not assoc.is_established:
            return {
                "success": False,
                "message": f"Failed to associate with DICOM node at {self.host}:{self.port}",
                "output_directory": output_directory,
                "files_retrieved": [],
                "total_files": 0,
                "total_size_mb": 0.0
            }
        
        success = False
        message = "C-GET operation failed"
        
        try:
            # Send C-GET request
            responses = assoc.send_c_get(ds, PatientRootQueryRetrieveInformationModelGet)
            
            for (status, dataset) in responses:
                if status:
                    status_int = status.Status if hasattr(status, 'Status') else 0
                    
                    if status_int == 0x0000:  # Success
                        success = True
                        message = "C-GET operation completed successfully"
                    elif status_int == 0xFF00:  # Pending
                        success = True  # Still processing
                        message = "C-GET operation in progress"
                    elif status_int == 0xA701:  # Refused: Out of Resources - Unable to calculate number of matches
                        message = "C-GET refused: Unable to calculate number of matches"
                    elif status_int == 0xA702:  # Refused: Out of Resources - Unable to perform sub-operations
                        message = "C-GET refused: Unable to perform sub-operations"
                    elif status_int == 0xFE00:  # Cancel
                        message = "C-GET operation was cancelled"
                    else:
                        message = f"C-GET failed with status 0x{status_int:04X}"
        
        finally:
            # Always release the association
            assoc.release()
        
        # Calculate total size in MB
        total_size_mb = total_size_bytes / (1024 * 1024)
        
        # Create final result
        result = {
            "success": success,
            "message": message,
            "output_directory": output_directory,
            "files_retrieved": [f["file_path"] for f in retrieved_files],
            "total_files": len(retrieved_files),
            "total_size_mb": round(total_size_mb, 2)
        }
        
        # Add detailed file information if successful
        if success and retrieved_files:
            result["file_details"] = retrieved_files
            result["message"] = f"Successfully retrieved {len(retrieved_files)} DICOM files ({total_size_mb:.2f} MB)"
        
        return result
    
    @staticmethod
    def _dataset_to_dict(dataset: Dataset) -> Dict[str, Any]:
        """Convert a DICOM dataset to a dictionary.
        
        Args:
            dataset: DICOM dataset
            
        Returns:
            Dictionary representation of the dataset
        """
        if hasattr(dataset, "is_empty") and dataset.is_empty():
            return {}
        
        result = {}
        for elem in dataset:
            if elem.VR == "SQ":
                # Handle sequences
                result[elem.keyword] = [DicomClient._dataset_to_dict(item) for item in elem.value]
            else:
                # Handle regular elements
                if hasattr(elem, "keyword"):
                    try:
                        if elem.VM > 1:
                            # Multiple values
                            result[elem.keyword] = list(elem.value)
                        else:
                            # Single value
                            result[elem.keyword] = elem.value
                    except Exception:
                        # Fall back to string representation
                        result[elem.keyword] = str(elem.value)
        
        return result