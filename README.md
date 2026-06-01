# ETL Pipeline Fashion Studio

Project ini merupakan submission untuk kelas **Belajar Fundamental Pemrosesan Data**.  
Tujuan project ini adalah membangun **ETL pipeline sederhana** untuk mengambil data produk dari website **Fashion Studio**, membersihkan data, lalu menyimpannya ke dalam file **CSV**.

## Dataset Source

Website sumber data:

`https://fashion-studio.dicoding.dev`

Data yang diambil meliputi:
- Title
- Price
- Rating
- Colors
- Size
- Gender

## Project Structure

```bash
submission-pemda/
├── tests/
│   ├── test_extract.py
│   ├── test_load.py
│   └── test_transform.py
├── utils/
│   ├── extract.py
│   ├── load.py
│   └── transform.py
├── main.py
├── products.csv
├── requirements.txt
└── submission.txt
```

## ETL Process

### 1. Extract
Tahap extract mengambil data produk dari seluruh halaman website Fashion Studio, mulai dari halaman 1 sampai 50.

Data mentah yang diambil terdiri dari:
- Title
- Price
- Rating
- Colors
- Size
- Gender
- timestamp

### 2. Transform
Tahap transform melakukan pembersihan data dengan aturan berikut:
- Menghapus data invalid seperti `Unknown Product`
- Menghapus data dengan harga invalid seperti `Price Unavailable`
- Menghapus data rating invalid seperti `Invalid Rating / 5` dan `Not Rated`
- Mengubah nilai `Price` dari dolar ke rupiah dengan kurs `Rp16.000`
- Mengubah `Rating` menjadi tipe `float`
- Mengubah `Colors` menjadi tipe `int`
- Membersihkan prefix pada kolom `Size` dan `Gender`
- Menghapus data `null`
- Menghapus data duplikat

### 3. Load
Tahap load menyimpan data yang sudah bersih ke dalam file `products.csv`.

## Installation

```bash
pip install -r requirements.txt
```

## How to Run

```bash
python main.py
```

## How to Run Unit Test

```bash
python -m pytest tests -v
```

## How to Run Test Coverage

```bash
python -m coverage run -m pytest tests
python -m coverage report -m
```

## Output
Hasil akhir ETL pipeline akan disimpan dalam file `products.csv`.

## Notes
Project ini menggunakan repositori data berupa **CSV**
