import zipfile
import xml.etree.ElementTree as ET
import sys
import os

def extract_text_from_docx(docx_path):
    if not os.path.exists(docx_path):
        return f"File not found: {docx_path}"
    
    try:
        with zipfile.ZipFile(docx_path) as zf:
            # Debug: List files
            # print("Files in zip:", zf.namelist())
            
            if 'word/document.xml' not in zf.namelist():
                return "Error: word/document.xml not found in zip"
                
            xml_content = zf.read('word/document.xml')
            
        tree = ET.fromstring(xml_content)
        
        # XML Namespace usually: {http://schemas.openxmlformats.org/wordprocessingml/2006/main}
        # We will iterate and find all text
        
        full_text = []
        for elem in tree.iter():
            # w:t is text, w:br and w:cr are breaks, w:p is paragraph
            tag_name = elem.tag.split('}')[-1] # Remove namespace
            
            if tag_name == 't':
                if elem.text:
                    full_text.append(elem.text)
            elif tag_name == 'p':
                full_text.append('\n')
            elif tag_name == 'br':
                full_text.append('\n')
            elif tag_name == 'tab':
                full_text.append('\t')
                
        return "".join(full_text)

    except zipfile.BadZipFile:
        return "Error: Not a valid docx/zip file"
    except Exception as e:
        return f"Error reading docx: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_docx.py <path_to_docx> [output_file]")
    else:
        text = extract_text_from_docx(sys.argv[1])
        if len(sys.argv) >= 3:
            with open(sys.argv[2], 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Successfully extracted to {sys.argv[2]}")
        else:
            # Safe print for console
            try:
                print(text)
            except UnicodeEncodeError:
                print(text.encode('utf-8', errors='ignore').decode('utf-8'))
