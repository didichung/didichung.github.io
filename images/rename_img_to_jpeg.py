import os
from PIL import Image

current_folder = os.getcwd()

print(f"Mulai memproses, mengonversi, dan mengoptimasi semua gambar di: {current_folder}\n")
count = 0

# Daftar ekstensi yang didukung (ditulis lowercase untuk dicocokkan nanti)
SUPPORTED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.gif']

for filename in os.listdir(current_folder):
    # Lewati file script itu sendiri
    if filename == os.path.basename(__file__):
        continue

    name, ext = os.path.splitext(filename)
    
    # Menghilangkan spasi gaib dan mengubah ke huruf kecil semua (.PNG -> .png)
    ext_clean = ext.strip().lower()

    if ext_clean in SUPPORTED_EXTENSIONS:
        old_file = os.path.join(current_folder, filename)
        new_file = os.path.join(current_folder, name + ".jpeg")

        try:
            with Image.open(old_file) as img:
                # Handling khusus untuk PNG/WebP transparan agar tidak rusak saat ke JPEG
                if img.mode in ("RGBA", "P", "LA") or (img.mode == "CMYK"):
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    # Jika ada channel alpha (transparansi), gunakan sebagai mask
                    if img.mode in ("RGBA", "LA"):
                        background.paste(img, mask=img.split()[-1])
                    else:
                        background.paste(img)
                    img = background
                elif img.mode != "RGB":
                    img = img.convert("RGB")

                temp_file = new_file + ".tmp"
                img.save(temp_file, "JPEG", optimize=True, quality=85)

            # Hapus file lama jika eksetensinya bukan .jpeg (termasuk .png, .png, dll)
            if old_file != new_file and os.path.exists(old_file):
                os.remove(old_file)

            # Jika file .jpeg tujuan sudah ada, hapus dulu sebelum ditimpa yang baru
            if os.path.exists(new_file):
                os.remove(new_file)

            os.rename(temp_file, new_file)
            print(f"Sukses Konversi & Optimasi: {filename} -> {name}.jpeg")
            count += 1

        except Exception as e:
            print(f"Gagal memproses file {filename}: {e}")

print(f"\nSelesai! Berhasil mengoptimasi total {count} gambar ke format .jpeg.")