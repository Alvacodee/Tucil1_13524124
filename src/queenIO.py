import os
import random
import string

# Setup folder default
TEST_DIR = "test"
SOL_DIR = "test/solutions"
IMG_DIR = "test/img"

# Buat folder jika belum ada (setup awal)
for d in [TEST_DIR, SOL_DIR, IMG_DIR]:
    if not os.path.exists(d):
        os.makedirs(d)

def read_board(filename):
    # Cek file di root, jika tidak ada cek di folder test
    if not os.path.exists(filename):
        if os.path.exists(os.path.join(TEST_DIR, filename)):
            filename = os.path.join(TEST_DIR, filename)
        else:
            print(f"File tidak ditemukan: {filename}")
            return None

    try:
        board = []
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip baris kosong atau komentar
                if not line or line.startswith('#'): 
                    continue
                # Support format "A B C" atau "ABC"
                row = list(line.replace(" ", ""))
                board.append(row)
        return board
    except Exception:
        print("Gagal membaca file (cek format).")
        return None

def save_solution(solver, filename=None):
    # Default nama file output
    if not filename:
        filename = f"test{solver.n}x{solver.n}_sol.txt"

    # Jika tidak ada path spesifik, masukkan ke folder solutions
    if not os.path.dirname(filename):
        filename = os.path.join(SOL_DIR, filename)

    # Tulis laporan solusi
    with open(filename, 'w') as f:
        f.write("Queens Puzzle Solution\n")
        f.write("=" * 40 + "\n\n")

        if not solver.found:
            f.write("No solution found.\n")
        else:
            f.write(f"Solved Board ({solver.n}x{solver.n}):\n\n")
            for r in range(solver.n):
                line = "  "
                for c in range(solver.n):
                    if solver.solution[r][c]:
                        line += " Q "
                    else:
                        line += f" {solver.board[r][c]} "
                f.write(line + "\n")
            
            f.write("\nQueen Positions:\n")
            count = 1
            for r in range(solver.n):
                for c in range(solver.n):
                    if solver.solution[r][c]:
                        f.write(f"  {count}. Baris {r+1}, Kolom {c+1} ({solver.board[r][c]})\n")
                        count += 1

        f.write("\n" + "=" * 40 + "\n")
        f.write(f"Iterations : {solver.iterations}\n")
        # Ambil durasi jika ada (handle attribute error manual jika perlu)
        dur = getattr(solver, 'duration', 0)
        f.write(f"Time       : {dur*1000:.2f} ms\n")
        f.write(f"Status     : {'SOLVED' if solver.found else 'FAIL'}\n")
    
    return filename

def generate_random_case(n, filename=None):
    if not filename:
        filename = f"test{n}x{n}.txt"
    
    # Default ke folder test jika path tidak ada
    if not os.path.dirname(filename):
        filename = os.path.join(TEST_DIR, filename)
        
    chars = string.ascii_uppercase
    
    with open(filename, 'w') as f:
        for _ in range(n):
            # Ambil warna random (max 26 huruf)
            pool = chars[:min(n, 26)]
            row = [random.choice(pool) for _ in range(n)]
            f.write(" ".join(row) + "\n")
            
    print(f"Test case created: {filename}")
    return filename

def run_batch_tests(solver_class):
    print("\nBATCH TESTING")
    print("="*60)
    
    # Ambil file .txt di folder test
    files = [f for f in os.listdir(TEST_DIR) if f.endswith('.txt')]
    files.sort()
    
    if not files:
        print("Folder test kosong.")
        return

    print(f"{'File':<20} | {'Size':<5} | {'Status':<8} | {'Time(ms)':<10} | {'Iters'}")
    print("-" * 60)

    count = 0
    for fname in files:
        path = os.path.join(TEST_DIR, fname)
        board = read_board(path)
        if not board: continue
        
        # Run solver (verbose=False agar terminal bersih)
        s = solver_class(board)
        found, dur = s.start_solving(verbose=False)
        
        # Auto save
        out = fname.replace('.txt', '_sol.txt')
        save_solution(s, out)
        
        status = "SOLVED" if found else "FAIL"
        print(f"{fname:<20} | {s.n:<5} | {status:<8} | {dur*1000:<10.2f} | {s.iterations}")
        if found: count += 1
        
    print("-" * 60)
    print(f"Total: {count}/{len(files)} solved.\n")