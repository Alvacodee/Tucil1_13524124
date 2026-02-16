import time

class QueenSolver:
    def __init__(self, board):
        self.board = board
        self.n = len(board)
        
        # Hasil
        self.solution = None
        self.found = False
        self.iterations = 0
        self.duration = 0
        
        # Fungsi visualisasi (diisi dari GUI/CLI)
        self.viz_function = None

        # Pre-processing warna agar validasi lebih cepat
        # Mapping: Warna -> List Koordinat [(r,c), ...]
        self.color_map = {}
        for r in range(self.n):
            for c in range(self.n):
                color = self.board[r][c]
                if color not in self.color_map:
                    self.color_map[color] = []
                self.color_map[color].append((r, c))

    def is_safe(self, row, col, placed):
        self.iterations += 1

        # 1. Cek Kolom (ke atas)
        for i in range(row):
            if placed[i][col]:
                return False

        # 2. Cek Warna (Region)
        current_color = self.board[row][col]
        for r, c in self.color_map[current_color]:
            # Jika ada ratu di warna sama, tapi bukan posisi kita sendiri
            if placed[r][c] and (r != row or c != col):
                return False

        # 3. Cek Tetangga (8 arah)
        moves = [(-1, -1), (-1, 0), (-1, 1), 
                 (0, -1),           (0, 1), 
                 (1, -1),  (1, 0),  (1, 1)]
        
        for dr, dc in moves:
            nr, nc = row + dr, col + dc
            # Pastikan koordinat valid (tidak keluar papan)
            if 0 <= nr < self.n and 0 <= nc < self.n:
                if placed[nr][nc]:
                    return False
        
        return True

    def solve_recursive(self, row, placed):
        # Base case: semua ratu berhasil dipasang
        if row == self.n:
            # Copy array 2D secara manual (tanpa library copy)
            self.solution = [r[:] for r in placed]
            self.found = True
            return True

        for col in range(self.n):
            # Update Visualisasi (Animasi "Mencoba" / Kuning)
            if self.viz_function:
                # Parameter terakhir True = sedang mencoba
                lanjut = self.viz_function(row, col, placed, True)
                if not lanjut: return False # Stop jika user menekan tombol stop

            if self.is_safe(row, col, placed):
                placed[row][col] = True # Pasang Ratu

                if self.solve_recursive(row + 1, placed):
                    return True
                
                placed[row][col] = False # Backtrack (Copot Ratu)
                
                # Update Visualisasi (Hapus Ratu dari layar)
                if self.viz_function:
                    self.viz_function(row, col, placed, False)
        
        return False

    def start_solving(self, verbose=True):
        if verbose:
            print(f"Solving {self.n}x{self.n} board...")
        
        self.found = False
        self.iterations = 0
        self.solution = None
        
        start = time.time()

        # Init papan kosong (False semua)
        empty_board = [[False for _ in range(self.n)] for _ in range(self.n)]
        
        self.solve_recursive(0, empty_board)
        
        self.duration = time.time() - start
        
        if verbose:
            if self.found:
                print(f"Ketemu! Waktu: {self.duration:.4f}s, Iterasi: {self.iterations}")
            else:
                print(f"Gagal. Waktu: {self.duration:.4f}s")
            
        return self.found, self.duration