from dicom_mcp.dicom_client import DicomClient
from dicom_mcp.config import load_config

def main():
    # Load the configuration
    try:
        config = load_config("configuration.yaml")
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return
    
    # Get the current node and calling AE title
    node = config.nodes[config.current_node]
    aet = config.calling_aet  # 这是一个字符串
    
    # Create client
    client = DicomClient(
        host=node.host,
        port=node.port,
        calling_aet=aet,  # 修复：直接使用aet
        called_aet=node.ae_title
    )
    
    print(f"Created DICOM client for {node.host}:{node.port}")
    print(f"Called AE: {node.ae_title}, Calling AE: {aet}")
    
    # Test connection
    success, message = client.verify_connection()
    if not success:
        print(f"Connection failed: {message}")
        return
    print(f"Connection successful: {message}")
    
    # Query for patients
    print("\nQuerying patients...")
    patients = client.query_patient()
    if not patients:
        print("No patients found")
        return
    
    print(f"Found {len(patients)} patients")
    for i, patient in enumerate(patients):
        print(f"  {i+1}. {patient.get('PatientName', 'Unknown')} (ID: {patient.get('PatientID', 'Unknown')})")

if __name__ == "__main__":
    main()
