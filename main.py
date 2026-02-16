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

# Fungsi Visualisasi CLI
def cli_callback(row, col, placed, is_trying):
    if not is_trying: return True 
    
    # Clear screen (Windows/Linux compatible)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    n = len(placed)
    print(f"\n--- Cek Baris {row+1}, Kolom {col+1} ---")
    
    for r in range(n):
        line = ""
        for c in range(n):
            if placed[r][c]:
                line += " Q "
            elif r == row and c == col:
                line += " ? " 
            else:
                line += " . "
        print(line)
        
    time.sleep(0.05) 
    return True

# Menu Functions

def print_menu():
    print("\n" + "="*50)
    print("      QUEENS PUZZLE SOLVER (Tucil 1 IF2211)")
    print("="*50)
    print("1. Solve from File")
    print("2. Solve with CLI Visualization")
    print("3. Run Assignment Example (9x9)")
    print("4. Batch Testing (All files in test/)")
    print("5. Generate Random Test Case")
    print("6. Export Solution as Image")
    print("7. Launch GUI")
    print("8. Help")
    print("0. Exit")

def show_help():
    print("\n" + "="*40)
    print("           BANTUAN PENGGUNAAN")
    print("="*40)
    print("\n FORMAT INPUT FILE (.txt)")
    print("   Gunakan huruf untuk mewakili warna wilayah.")
    print("   Contoh (4x4):")
    print("     AABB")
    print("     AACC")
    print("     DDEE")
    print("     DDEE")
    print("\n ATURAN PERMAINAN")
    print("   - Satu Ratu per Baris")
    print("   - Satu Ratu per Kolom")
    print("   - Satu Ratu per Warna Wilayah")
    print("   - Tidak boleh bersentuhan (8 arah mata angin)")
 

def solve_file():
    fname = input("Filename (contoh: test4x4.txt): ").strip()
    board = queenIO.read_board(fname)
    if not board: return

    solver = QueenSolver(board)
    found, dur = solver.start_solving()
    
    if found:
        # Auto save: namafile_sol.txt
        base = os.path.basename(fname)
        out_name = base.replace('.txt', '_sol.txt') if base.endswith('.txt') else base + "_sol.txt"
        
        saved = queenIO.save_solution(solver, out_name)
        print(f"Saved: {saved}")

def solve_viz():
    fname = input("Filename: ").strip()
    board = queenIO.read_board(fname)
    if not board: return

    if len(board) > 10:
        print("Warning: Board besar mungkin lambat di terminal.")
        input("Press Enter...")

    solver = QueenSolver(board)
    # Hook callback visualisasi baru
    solver.viz_function = cli_callback
    
    solver.start_solving()
    
    if solver.found:
        print("\nSolusi Akhir:")
        for r in solver.solution:
            print(" ".join([" Q " if c else " . " for c in r]))

def run_assignment():
    print("\nRunning Assignment 9x9 Case...")
    # Data dari gambar soal
    data = [
        "AAABBCCCD", "ABBBBCECD", "ABBBDCECD", "AAABDCCCD", "BBBBDDDDD",
        "FGGGDDHDD", "FGIGDDHDD", "FGIGDDHDD", "FGGGDDHHH"
    ]
    
    path = "test/test9x9.txt"
    # Tulis file sementara
    with open(path, "w") as f:
        f.write("\n".join(data))
    
    board = queenIO.read_board(path)
    solver = QueenSolver(board)
    solver.start_solving()
    
    if solver.found:
        saved = queenIO.save_solution(solver, "test9x9_sol.txt")
        print(f"Solusi tersimpan: {saved}")

def export_image():
    fname = input("Filename: ").strip()
    board = queenIO.read_board(fname)
    if not board: return
    
    print("Solving...")
    solver = QueenSolver(board)
    found, _ = solver.start_solving(verbose=False)
    
    if found:
        base = os.path.basename(fname).replace('.txt', '')
        
        # 1. Save TXT
        txt_out = f"{base}_sol.txt"
        path_txt = queenIO.save_solution(solver, txt_out)
        print(f"[1] Text saved: {path_txt}")
        
        # 2. Save PNG
        img_out = f"{base}_sol.png"
        path_img = queenImage.save_board_image(solver.board, solver.solution, img_out)
        print(f"[2] Image saved: {path_img}")
    else:
        print("No solution found, cannot export image.")

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
            try:
                n_input = input("Size (N): ").strip()
                if n_input.isdigit():
                    queenIO.generate_random_case(int(n_input))
                else:
                    print("Masukkan angka yang benar.")
            except ValueError:
                print("Error input.")
        elif choice == '6':
            export_image()
        elif choice == '7':
            print("Launching GUI...")
            # Import tk lokal agar tidak mengganggu jika user cuma mau CLI
            import tkinter as tk
            root = tk.Tk()
            app = queenGUI.QueensGUI(root)
            root.mainloop()
        elif choice == '8':
            show_help()
        elif choice == '0':
            print("Bye.")
            break
        else:
            print("Pilihan tidak valid.")
        
        if choice != '7':
            input("\nPress Enter...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")