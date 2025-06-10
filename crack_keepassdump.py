import xml.etree.ElementTree as ET
from collections import defaultdict

def extract_keepass_credentials(xml_content):
    """
    Extract credentials from KeePass XML export
    Returns: list of dicts with 'title', 'username', 'password', 'url'
    """
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        print(f"XML parsing error: {e}")
        return []

    credentials = []
    ns = {'kp': 'http://keepass.info/whatever'}  # KeePass doesn't use namespaces in exports
    
    for entry in root.findall('.//Entry'):
        cred = defaultdict(str)
        
        # Extract basic entry info
        title = entry.find(".//String[Key='Title']/Value")
        if title is not None:
            cred['title'] = title.text
            
        username = entry.find(".//String[Key='UserName']/Value")
        if username is not None:
            cred['username'] = username.text
            
        password = entry.find(".//String[Key='Password']/Value")
        if password is not None:
            cred['password'] = password.text
            
        url = entry.find(".//String[Key='URL']/Value")
        if url is not None:
            cred['url'] = url.text
            
        # Only add if we have at least a title and password
        if cred.get('title') and cred.get('password'):
            credentials.append(dict(cred))
            
    return credentials

def print_credentials(credentials):
    """Print credentials in a readable format"""
    print("\nExtracted Credentials:")
    print("-" * 50)
    for i, cred in enumerate(credentials, 1):
        print(f"Entry {i}:")
        print(f"  Title:    {cred.get('title', 'N/A')}")
        print(f"  Username: {cred.get('username', 'N/A')}")
        print(f"  Password: {cred.get('password', 'N/A')}")
        print(f"  URL:      {cred.get('url', 'N/A')}")
        print("-" * 50)

if __name__ == "__main__":
    # Read XML file (replace with your filename)
    xml_file = "keepass_dump.xml" # ===============================> change this to your .xml file
    
    try:
        with open(xml_file, 'r', encoding='utf-8') as f:
            xml_content = f.read()
            
        credentials = extract_keepass_credentials(xml_content)
        
        if credentials:
            print_credentials(credentials)
            
            # Save to CSV for easy import
            import csv
            with open('extracted_credentials.csv', 'w', newline='') as csvfile:
                fieldnames = ['title', 'username', 'password', 'url']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(credentials)
            print("\nCredentials saved to 'extracted_credentials.csv'")
        else:
            print("No credentials found in the XML file.")
            
    except FileNotFoundError:
        print(f"Error: File '{xml_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
