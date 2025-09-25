import os
import hashlib
import json

# ================================
# CONFIG
# ================================
BASE_DIR = "."   # Thư mục gốc local chứa ảnh
GITHUB_BASE_URL = "https://raw.githubusercontent.com/baohuavangia/AppBibleManifest/main"
OUTPUT_FILE = "manifest.json"


def file_hash(path):
    """Tính SHA256 hash của file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest().upper()


def generate_manifest():
    manifest = {"folders": []}

    for root, dirs, files in os.walk(BASE_DIR):
        if root == BASE_DIR:
            # bỏ qua thư mục gốc ".", chỉ lấy thư mục con
            continue

        folder_rel = os.path.relpath(root, BASE_DIR)  # VD: "ImageBackground" hoặc "ImageVerse"
        folder_entry = {"name": folder_rel, "images": []}

        for file_name in files:
            file_path = os.path.join(root, file_name)
            rel_path = os.path.relpath(file_path, BASE_DIR)  # VD: "ImageBackground/abc.png"
            url = f"{GITHUB_BASE_URL}/{rel_path.replace(os.sep, '/')}"
            hash_val = file_hash(file_path)

            folder_entry["images"].append({
                "name": file_name,
                "path": rel_path.replace(os.sep, "/"),  # để biết file nằm chỗ nào
                "url": url,
                "hash": hash_val
            })

        manifest["folders"].append(folder_entry)

    return manifest


if __name__ == "__main__":
    manifest = generate_manifest()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Manifest generated: {OUTPUT_FILE}")
