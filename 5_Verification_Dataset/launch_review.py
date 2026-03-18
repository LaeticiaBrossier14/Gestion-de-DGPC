"""
Lance le serveur de review dataset avec sauvegarde automatique.
Double-clique sur ce fichier ou lance : python launch_review.py
"""
import http.server
import os
import threading
import webbrowser
import json
import csv

PORT = 8787
DIR  = os.path.dirname(os.path.abspath(__file__))

os.chdir(DIR)

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_): pass  # silencieux
    
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_POST(self):
        if self.path == '/save_status':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                file_name = data.get('file_name')
                status = data.get('status')
                
                if file_name and status:
                    dataset_path = os.path.join('dataset_final', 'dataset.csv')
                    if os.path.exists(dataset_path):
                        # Mettre à jour le CSV
                        rows = []
                        with open(dataset_path, 'r', encoding='utf-8') as f:
                            reader = csv.DictReader(f)
                            fieldnames = list(reader.fieldnames)
                            if 'status' not in fieldnames:
                                fieldnames.append('status')
                            for row in reader:
                                if row['file_name'] == file_name:
                                    row['status'] = status
                                rows.append(row)
                        
                        with open(dataset_path, 'w', encoding='utf-8', newline='') as f:
                            writer = csv.DictWriter(f, fieldnames=fieldnames)
                            writer.writeheader()
                            writer.writerows(rows)
                            
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status": "ok"}')
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def open_browser():
    webbrowser.open(f"http://localhost:{PORT}/review_dataset.html")

print(f"Serveur lance sur http://localhost:{PORT}")
print("Mode Sauvegarde Automatique ACTIVE (Chaque clic met a jour le CSV en direct)")
print("Ferme cette fenetre (ou Ctrl+C) pour arreter.")

threading.Timer(0.8, open_browser).start()

with http.server.HTTPServer(("", PORT), Handler) as srv:
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
