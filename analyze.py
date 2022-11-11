import os
import xml.etree.ElementTree as ET

# Unzip files
# fname = "../corenlp_plot_summaries/15401493.xml.gz"
# with gzip.open(fname, 'rb') as f_in:
#     xml_content = f_in.read().decode().strip()
# tree = ET.fromstring(xml_content)

# Father reference words
father_reference_words = ["father", "dad", "papa"]

# Store father related words in a set
father_related_words = set()

# Parse and print out father information
def get_father_info(root):
    for dep in root.iter('dep'):
        if dep.find("governor").text in father_reference_words:
            father_related_words.add(dep.find("dependent").text)
        if dep.find("dependent").text in father_reference_words:
            father_related_words.add(dep.find("governor").text)
    

# Find all the xml file names in the xmls directory
rootdir = '/home/anton/Desktop/ada/nlp/xmls'
xml_files = []
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file.endswith('.xml'):
            xml_files.append(os.path.join(subdir, file))


# Parse each xml file
for xml_file in xml_files:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    get_father_info(root)
    
# Print out the father related words
print(father_related_words)