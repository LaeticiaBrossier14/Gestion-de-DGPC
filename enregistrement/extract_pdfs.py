import fitz  # PyMuPDF
import os

pdf_files = [
    "MEMOIRE.pdf",
    "Memoire final.pdf",
    "Memoire corrige a imprimer.pdf",
    "The_End__Version_corrigée_.pdf",
    "Gestion_des_interventions_de_protection.pdf",
]

base_dir = r"g:\AZ\Documents\gestion des appelles telephoniques\enregistrement"

for pdf_file in pdf_files:
    pdf_path = os.path.join(base_dir, pdf_file)
    txt_name = os.path.splitext(pdf_file)[0] + ".txt"
    txt_path = os.path.join(base_dir, txt_name)
    
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        print(f"\n{'='*60}")
        print(f"File: {pdf_file}")
        print(f"Pages: {total_pages}")
        
        full_text = []
        for page_num, page in enumerate(doc):
            text = page.get_text()
            full_text.append(f"--- PAGE {page_num+1} ---\n{text}")
        
        all_text = "\n".join(full_text)
        
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(all_text)
        
        print(f"Extracted to: {txt_name}")
        print(f"Total chars: {len(all_text)}")
        
        # Print first 500 chars for preview
        print(f"Preview:\n{all_text[:500]}")
        print(f"{'='*60}")
        
        doc.close()
    except Exception as e:
        print(f"ERROR with {pdf_file}: {e}")
