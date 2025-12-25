# Analisis Kompleksitas Algoritma (Iteratif vs Rekursif)

Aplikasi web sederhana untuk **membandingkan waktu eksekusi** dan **estimasi penggunaan memori** pada proses **konversi huruf besar-kecil** di sebuah string, dengan pilihan algoritma **iteratif** dan **rekursif**.  
Frontend dibuat dengan HTML/CSS/JS, backend menggunakan **Flask** yang menyediakan API untuk generate string dan analisis.

## Fitur

- Generate string acak dengan panjang `n`.
- Pilih pola string:
  - `lower` (huruf kecil saja) → dikonversi ke UPPERCASE
  - `upper` (huruf besar saja) → dikonversi ke lowercase
  - `mixed` (campuran) → bisa:
    - `to_upper` (jadi besar semua)
    - `to_lower` (jadi kecil semua)
    - `swap` (tukar besar↔kecil)
- Menampilkan:
  - waktu eksekusi (ms) dari backend
  - estimasi memori (KB) (estimasi sederhana berbasis ukuran bytes string)

## Struktur Proyek

- `templates/index.html` — tampilan utama aplikasi
- `templates/style.css` — styling UI
- `templates/script.js` — logic frontend, memanggil API backend
- `app.py` — backend Flask + endpoint API
- `requirements.txt` — dependensi Python

## Prasyarat

- Python 3.9+ (disarankan)
- Browser modern (Chrome/Firefox/Edge)

## Cara Menjalankan (Backend / API)

1. Buat virtual environment:

   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

2. Install dependensi:

   ```bash
   pip install -r requirements.txt
   ```

3. Jalankan server Flask:

   ```bash
   python app.py
   ```

4. Pastikan API hidup:
   - Buka `http://localhost:5000/api/test`  
     Harusnya mengembalikan JSON status `ok`.
