import csv
import os
import shutil
import argparse

def main():
    parser = argparse.ArgumentParser(description="Nettoyer le dataset a partir de review.csv")
    parser.add_argument("--review_csv", default="review.csv", help="Le fichier exporte par l'app de review")
    parser.add_argument("--out_csv", default="dataset_final/dataset_clean.csv", help="Le nouveau CSV propre")
    parser.add_argument("--move_bad_to", default="audios_mauvais", help="Dossier ou deplacer les mauvais audios")
    args = parser.parse_args()

    if not os.path.exists(args.review_csv):
        print(f"Erreur : Le fichier {args.review_csv} n'existe pas.")
        print("N'oublie pas de cliquer sur 'Exporter review.csv' dans l'application web !")
        return

    os.makedirs(os.path.dirname(args.out_csv), exist_ok=True)
    if args.move_bad_to:
        os.makedirs(args.move_bad_to, exist_ok=True)

    clean_rows = []
    bad_count = 0
    unseen_count = 0

    with open(args.review_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        for row in reader:
            status = row.get("status", "unseen")
            
            if status == "ok":
                # On garde les bons
                # On supprime la colonne status pour le dataset final
                clean_row = {k: v for k, v in row.items() if k != "status"}
                clean_rows.append(clean_row)
            
            elif status == "unseen":
                # On decide de garder les non-vus par defaut, ou tu peux changer la logique
                clean_row = {k: v for k, v in row.items() if k != "status"}
                clean_rows.append(clean_row)
                unseen_count += 1
                
            elif status == "bad":
                bad_count += 1
                if args.move_bad_to:
                    # Deplacer le fichier audio
                    old_path = os.path.join("audios", row["file_name"])
                    new_path = os.path.join(args.move_bad_to, os.path.basename(row["file_name"]))
                    if os.path.exists(old_path):
                        shutil.move(old_path, new_path)

    # Sauvegarder le nouveau CSV propre
    if clean_rows:
        out_fields = [f for f in fields if f != "status"]
        with open(args.out_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=out_fields)
            writer.writeheader()
            writer.writerows(clean_rows)

    print("\n=== Nettoyage termine ===")
    print(f"✅ Audios gardes : {len(clean_rows)} (dont {unseen_count} non-evalues)")
    print(f"❌ Audios mauvais : {bad_count} " + (f"(deplaces vers {args.move_bad_to}/)" if args.move_bad_to else "(ignores dans le CSV)"))
    print(f"📄 Nouveau dataset sauvegarde dans : {args.out_csv}")

if __name__ == "__main__":
    main()
