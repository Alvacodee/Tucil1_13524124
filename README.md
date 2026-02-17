# Queens Puzzle Solver

Solusi untuk Queens Puzzle menggunakan algoritma Brute Force dengan Backtracking (Optimasi).

Tugas Kecil 1 - IF2211 Strategi Algoritma

## Deskripsi

Program ini menyelesaikan puzzle Queens, yaitu varian dari N-Queens dengan tambahan constraint berupa region berwarna.

Aturan:
- Setiap baris harus punya 1 queen
- Setiap kolom harus punya 1 queen
- Setiap region (warna) harus punya 1 queen
- Queens tidak boleh bersebelahan (8 arah)

## Fitur

**Core:**
- Algoritma brute force dengan backtracking
- Baca/tulis file
- Statistik (iterasi, waktu)
- Batch testing

**Bonus:**
- Live visualization
- GUI (Tkinter)
- Export ke PNG

## Struktur

```
Tucil1_NIM/
├── src/
│   ├── queenSolver.py
│   ├── queenIO.py
│   ├── queenVisualizer.py
│   ├── queensIamge.py
│   └── queenGUI.py
├── test/
│   ├── img/*.txt
│   ├── solutions/*.txt
│   └── *.txt (test files)
├── doc/
│   ├── Tucil1-IF2211-2026.pdf
│   └── Tucil1_13524124.pdf
│
├── main.py
├── QUICKSTART.md
├── README.md
└── SETUP_GUIDE.md
```

## Algoritma (Notasi Algoritmik)

Brute force dengan backtracking:

```python
function solve(row : integer) → boolean
{ Mengembalikan true jika penempatan ratu pada baris 'row' hingga 'n' berhasil dilakukan tanpa konflik }

Kamus
row : integer { Indeks baris }
col : integer { Indeks kolom untuk mencoba penempatan ratu }
found : boolean { Penanda jika solusi ditemukan di tingkat rekursi bawahnya }

    if row == n then
        -> Found
    
    while (col <= n-1) and (not found) do
        if is_valid(row, col) then
            place_queen(row, col)
            if solve(row + 1):
                -> Found
            remove_queen(row, col)
    
    -> not(Found)
```

**Kompleksitas:**
- Time: O(n!)
- Space: O(n²)

**Validasi:**
- Kolom unik
- Region unik
- Non-adjacent


## Requirement and Installation

Refer to SETUP_GUIDE.md

## Compilation and Running

Refer to SETUP_GUIDE.md

## Author

Nama: Zahran Alvan Putra Winarko  
NIM: 13524124  
Prodi: Teknik Informatika  
Institusi: ITB