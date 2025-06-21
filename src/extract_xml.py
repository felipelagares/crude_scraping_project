import zipfile
import os

# override the contents if a .xml file with the same name already exists
def extract_xmls_from_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.lower().endswith('.xml'):
                zip_ref.extract(file, extract_to)

def extract_xmls():
    os.makedirs('xmls', exist_ok=True)
    for zip_filename in os.listdir('zips'):
        if zip_filename.lower().endswith('.zip'):
            zip_path = os.path.join('zips', zip_filename)
            extract_xmls_from_zip(zip_path, 'xmls')

if __name__ == "__main__":
    extract_xmls()
    print("Extração de XMLs concluída.")