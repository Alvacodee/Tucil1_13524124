import sys
import os
import time

# Tambahkan folder src ke path import
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.append(src_dir)

try:
    from queenSolver import QueenSolver
    import queenIO
    import queenGUI
    import queenImage
except ImportError as e:
    print(f"Error Import: {e}")
    sys.exit(1)

# Visualisasi CLI
def cli_callback(board, row, col, placed, is_trying):
    if not is_trying: return True 
    
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    n = len(placed)
    print(f"\n--- Cek Baris {row+1}, Kolom {col+1} ---")
    
    for r in range(n):
        line = ""
        for c in range(n):
            if placed[r][c]:
                line += " # "
            elif r == row and c == col:
                line += " ? " 
            else:
                # Tampilkan Huruf Wilayah
                line += f" {board[r][c]} "
        print(line)
        
    time.sleep(0.05) 
    return True

# Fungsi Helper Tampilan
def print_board_result(solver):
    print("\n" + "-"*30)
    print(f"HASIL AKHIR ({solver.n}x{solver.n})")
    print(f"Legenda: # = Ratu, Huruf = Wilayah")
    print("-"*30)
    
    for r in range(solver.n):
        line = ""
        for c in range(solver.n):
            if solver.solution[r][c]:
                line += " # " # REVISI: Pakai # untuk Ratu
            else:
                # Tampilkan Huruf Wilayah dari board asli
                line += f" {solver.board[r][c]} "
        print(line)
    print("-"*30)
    print(f"Durasi : {getattr(solver, 'duration', 0):.4f} detik")
    print(f"Iterasi: {solver.iterations}")
    print("-"*30 + "\n")

# Menu Functions 

def solve_file():
    print("\n--- SOLVE FROM FILE ---")
    fname = input("Masukkan nama file input: ").strip()
    board = queenIO.read_board(fname)
    
    if not board: 
        return

    print(f"Solving {len(board)}x{len(board)}...")
    solver = QueenSolver(board)
    found, dur = solver.start_solving()
    
    if found:
        # 1. Tampilkan dulu di CLI
        print_board_result(solver)
        
        # 2. Konfirmasi Save
        confirm = input("Apakah ingin menyimpan solusi ke file? (y/n): ").lower().strip()
        if confirm == 'y':
            out_name = input("Masukkan nama file output (contoh: hasil.txt): ").strip()
            if not out_name:
                print("Nama file kosong, batal simpan.")
            else:
                saved_path = queenIO.save_solution(solver, out_name)
                print(f"Berhasil disimpan di: {saved_path}")
    else:
        print("\nTidak ada solusi untuk konfigurasi ini.")

def solve_viz():
    print("\n--- SOLVE WITH VISUALIZATION ---")
    fname = input("Masukkan nama file input: ").strip()
    board = queenIO.read_board(fname)
    if not board: return

    if len(board) > 10:
        print("[Info] Ukuran board besar, animasi mungkin lambat.")
        input("Tekan Enter untuk lanjut...")

    solver = QueenSolver(board)
    
    # Hook animasi: Gunakan lambda untuk menyelipkan parameter 'board'
    solver.viz_function = lambda r, c, p, t: cli_callback(board, r, c, p, t)
    
    solver.start_solving()
    
    if solver.found:
        print_board_result(solver)
        
        if input("Simpan solusi? (y/n): ").lower() == 'y':
            out_name = input("Nama file output: ").strip()
            if out_name:
                saved = queenIO.save_solution(solver, out_name)
                print(f"Saved: {saved}")

def generate_test():
    print("\n--- GENERATE RANDOM TEST CASE ---")
    try:
        n_input = input("Masukkan ukuran N (misal 8): ").strip()
        if not n_input.isdigit():
            print("Harus angka.")
            return
        n = int(n_input)
        
        out_name = input("Masukkan nama file output (misal: soal_baru.txt): ").strip()
        if not out_name:
            out_name = f"test{n}x{n}.txt"
            print(f"Menggunakan nama default: {out_name}")
            
        path = queenIO.generate_random_case(n, out_name)
        
    except ValueError:
        print("Input error.")

def run_assignment():
    print("\nRunning Assignment 9x9...")
    data = [
        "AAABBCCCD", "ABBBBCECD", "ABBBDCECD", "AAABDCCCD", "BBBBDDDDD",
        "FGGGDDHDD", "FGIGDDHDD", "FGIGDDHDD", "FGGGDDHHH"
    ]
    path = "test/test9x9.txt"
    with open(path, "w") as f: f.write("\n".join(data))
    
    board = queenIO.read_board(path)
    solver = QueenSolver(board)
    solver.start_solving()
    
    if solver.found:
        print_board_result(solver)
        if input("Simpan? (y/n): ").lower() == 'y':
            queenIO.save_solution(solver, "test9x9_sol.txt")
            print("Saved test/solutions/test9x9_sol.txt")

def export_image():
    print("\n--- EXPORT IMAGE ---")
    fname = input("File input: ").strip()
    board = queenIO.read_board(fname)
    if not board: return
    
    solver = QueenSolver(board)
    found, _ = solver.start_solving(verbose=False)
    
    if found:
        print("Solusi ditemukan.")
        if input("Generate gambar? (y/n): ").lower() == 'y':
            out_name = input("Nama file gambar (misal: hasil.png): ").strip()
            path = queenImage.save_board_image(solver.board, solver.solution, out_name)
            print(f"Gambar saved: {path}")
    else:
        print("No solution.")

def print_menu():
    print("\n" + "="*40)
    print("   QUEENS SOLVER (Tucil 1 IF2211)")
    print("="*40)
    print("1. Solve File (CLI)")
    print("2. Solve with Animation (CLI)")
    print("3. Assignment Example (9x9)")
    print("4. Batch Test (All files)")
    print("5. Generate Random Test Case")
    print("6. Export Image")
    print("7. Launch GUI")
    print("0. Exit")

def main():
    while True:
        print_menu()
        choice = input("\n>> ").strip()
        
        if choice == '1':
            solve_file()
        elif choice == '2':
            solve_viz()
        elif choice == '3':
            run_assignment()
        elif choice == '4':
            queenIO.run_batch_tests(QueenSolver)
        elif choice == '5':
            generate_test()
        elif choice == '6':
            export_image()
        elif choice == '7':
            print("Launching GUI...")
            import tkinter as tk
            root = tk.Tk()
            app = queenGUI.QueensGUI(root)
            root.mainloop()
        elif choice == '0':
            print("Bye.")
            break
        else:
            print("Pilihan salah.")
        
        if choice != '7':
            input("\nPress Enter...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")