# Queens Puzzle Solver

Solusi untuk Queens Puzzle menggunakan algoritma Brute Force dengan Backtracking.

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
        -> True
    
    while (col <= n-1) and (not found) do
        if valid(row, col) then
            place_queen(row, col)
            if solve(row + 1):
                -> True
            remove_queen(row, col)
    
    -> False
```

**Kompleksitas:**
- Time: O(n!)
- Space: O(n²)

**Validasi:**
- Kolom unik
- Region unik
- Non-adjacent

## Testing

Test cases di folder `test/`:
- tes4.txt (easy, <1ms)
- tes6.txt (medium, ~10ms)
- tes8.txt (hard, ~100ms)

Run batch test:
```bash
uv run python main.py
# Pilih opsi 4
```

## Output

Console:
```
Solution found in 45.23ms
Iterations: 12,456
```

File txt:
```
Queens Puzzle Solution
====================

Board:

  A  A  Q  B  C
  A  B  B  Q  C
  ...

Statistics:
Time: 45.23ms
Iterations: 12,456
```

Image (PNG):
- Solution dengan queens
- Input vs output comparison

## Performa

| Board | Iterations | Time | Status |
|-------|-----------|------|--------|
| 4×4   | ~150      | 0.5ms | OK |
| 6×6   | ~3.4K     | 8ms | OK |
| 8×8   | ~45K      | 120ms | OK |
| 10×10 | ~1.2M     | 8.5s | OK |

*Test: Windows 11, Python 3.13, i5*

## Author

Nama: Zahran Alvan Putra Winarko  
NIM: 13524124  
Prodi: Teknik Informatika  
Institusi: ITB