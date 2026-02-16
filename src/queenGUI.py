import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog
import threading
import time
import os
from queenSolver import QueenSolver
import queenIO
import queenImage

class QueensGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tucil 1 - Queens Solver (GUI)")
        self.root.geometry("1100x750")
        
        self.board = None
        self.n = 0
        self.solver = None
        self.stop_requested = False
        self.current_filename = "custom"
        
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#2c3e50", height=60, pady=10)
        header.pack(fill=tk.X)
        tk.Label(header, text="Queens Puzzle Solver", font=("Segoe UI", 18, "bold"), bg="#2c3e50", fg="white").pack()
        tk.Label(header, text="Brute Force Algorithm Visualization", font=("Segoe UI", 10), bg="#2c3e50", fg="#bdc3c7").pack()

        # Main Layout (Split Pane)
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_panel = tk.Frame(main_frame, width=300, relief=tk.RIDGE, borderwidth=1, padx=10, pady=10)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        right_panel = tk.Frame(main_frame, bg="white", relief=tk.SUNKEN, borderwidth=1)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.setup_controls(left_panel)
        self.setup_canvas(right_panel)

    def setup_controls(self, parent):
        # 1. Input Data
        lbl_input = tk.LabelFrame(parent, text="1. Input Data", font=("Arial", 10, "bold"), padx=5, pady=5)
        lbl_input.pack(fill=tk.X, pady=5)
        
        self.btn_load = ttk.Button(lbl_input, text="📂 Load File (.txt)", command=self.load_file)
        self.btn_load.pack(fill=tk.X, pady=2)
        
        self.btn_rand = ttk.Button(lbl_input, text="🎲 Generate Random Case", command=self.generate_random)
        self.btn_rand.pack(fill=tk.X, pady=2)

        self.lbl_file_status = tk.Label(lbl_input, text="No file loaded", fg="gray", wraplength=200)
        self.lbl_file_status.pack(pady=2)

        # 2. Solver Control
        lbl_solver = tk.LabelFrame(parent, text="2. Solver Control", font=("Arial", 10, "bold"), padx=5, pady=5)
        lbl_solver.pack(fill=tk.X, pady=10)

        self.var_animate = tk.BooleanVar(value=True)
        tk.Checkbutton(lbl_solver, text="Tampilkan Animasi", variable=self.var_animate).pack(anchor="w")

        tk.Label(lbl_solver, text="Speed Delay (detik):").pack(anchor="w", pady=(5,0))
        self.scale_speed = tk.Scale(lbl_solver, from_=0.01, to=1.0, resolution=0.01, orient=tk.HORIZONTAL)
        self.scale_speed.set(0.1) 
        self.scale_speed.pack(fill=tk.X)

        self.btn_solve = ttk.Button(lbl_solver, text="▶ START SOLVING", command=self.start_thread, state=tk.DISABLED)
        self.btn_solve.pack(fill=tk.X, pady=5)
        
        self.btn_stop = ttk.Button(lbl_solver, text="⏹ STOP", command=self.stop_solving, state=tk.DISABLED)
        self.btn_stop.pack(fill=tk.X)

        # 3. Export
        lbl_export = tk.LabelFrame(parent, text="3. Export Result", font=("Arial", 10, "bold"), padx=5, pady=5)
        lbl_export.pack(fill=tk.X, pady=10)
        
        self.btn_save_txt = ttk.Button(lbl_export, text="💾 Save Solution (.txt)", command=self.save_txt, state=tk.DISABLED)
        self.btn_save_txt.pack(fill=tk.X, pady=2)
        
        self.btn_save_img = ttk.Button(lbl_export, text="🖼️ Save Image (.png)", command=self.save_img, state=tk.DISABLED)
        self.btn_save_img.pack(fill=tk.X, pady=2)

        # Log Box
        lbl_log = tk.LabelFrame(parent, text="Log Aktivitas", padx=5, pady=5)
        lbl_log.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.txt_log = scrolledtext.ScrolledText(lbl_log, height=5, font=("Consolas", 9), state='disabled')
        self.txt_log.pack(fill=tk.BOTH, expand=True)

    def setup_canvas(self, parent):
        self.canvas = tk.Canvas(parent, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.lbl_status = tk.Label(parent, text="Ready.", bg="#ecf0f1", anchor="w", padx=5)
        self.lbl_status.pack(fill=tk.X, side=tk.BOTTOM)

    # LOGIC

    def log(self, msg):
        self.txt_log.config(state='normal')
        self.txt_log.insert(tk.END, f"> {msg}\n")
        self.txt_log.see(tk.END)
        self.txt_log.config(state='disabled')

    def load_file(self):
        fname = filedialog.askopenfilename(initialdir="test", title="Pilih File", filetypes=[("Text Files", "*.txt")])
        if not fname: return
        
        base = os.path.basename(fname)
        self.current_filename = os.path.splitext(base)[0]
        self.load_board_from_path(fname)

    def generate_random(self):
        n = simpledialog.askinteger("Input", "Masukkan Ukuran Board (N):", minvalue=4, maxvalue=15)
        if n:
            filename = f"test{n}x{n}.txt"
            self.current_filename = f"test{n}x{n}"
            try:
                fullpath = queenIO.generate_random_case(n, filename)
                self.log(f"Generated: {filename}")
                self.load_board_from_path(fullpath)
            except Exception as e:
                messagebox.showerror("Error", f"Gagal generate: {e}")

    def load_board_from_path(self, filepath):
        self.board = queenIO.read_board(filepath)
        if self.board:
            self.n = len(self.board)
            self.lbl_file_status.config(text=os.path.basename(filepath), fg="blue")
            self.log(f"Loaded Board: {self.n}x{self.n}")
            
            # Reset UI
            self.canvas.delete("all")
            self.btn_solve.config(state=tk.NORMAL)
            self.btn_save_txt.config(state=tk.DISABLED)
            self.btn_save_img.config(state=tk.DISABLED)
            self.lbl_status.config(text="Ready to solve.")
            
            self.draw_board()
        else:
            messagebox.showerror("Error", "Gagal membaca file board.")

    def save_txt(self):
        if self.solver and self.solver.found:
            default_name = f"{self.current_filename}_sol.txt"
            fname = filedialog.asksaveasfilename(
                defaultextension=".txt", 
                initialdir="test/solutions", 
                initialfile=default_name,
                filetypes=[("Text", "*.txt")]
            )
            if fname:
                queenIO.save_solution(self.solver, fname)
                self.log(f"Saved TXT: {os.path.basename(fname)}")

    def save_img(self):
        if self.solver and self.solver.found:
            default_name = f"{self.current_filename}_sol.png"
            fname = filedialog.asksaveasfilename(
                defaultextension=".png", 
                initialdir="test/img", 
                initialfile=default_name,
                filetypes=[("PNG Image", "*.png")]
            )
            if fname:
                try:
                    queenImage.save_board_image(self.solver.board, self.solver.solution, fname)
                    self.log(f"Saved Image: {os.path.basename(fname)}")
                    messagebox.showinfo("Sukses", "Gambar berhasil disimpan!")
                except Exception as e:
                    messagebox.showerror("Error", f"Gagal simpan gambar: {e}")

    # DRAWING

    def get_color(self, char_code):
        colors = {
            'A': '#FFB7B2', 'B': '#A2E1DB', 'C': '#C3B1E1', 'D': '#FDFD96',
            'E': '#F8C8DC', 'F': '#B5EAD7', 'G': '#FFDAC1', 'H': '#E2F0CB',
            'I': '#DEC4D6', 'J': '#9BB7D4', 'K': '#E7949A', 'L': '#C7CEEA',
            'M': '#FF9AA2', 'N': '#E2F0CB', 'O': '#B5EAD7', 'P': '#C7CEEA'
        }
        return colors.get(char_code, "#E0E0E0") 

    def draw_board(self, solution_mask=None, trying_pos=None):
        self.canvas.delete("all")
        if not self.board: return

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        size = min(w, h) - 40
        cell_size = size // self.n
        offset_x = (w - (self.n * cell_size)) // 2
        offset_y = (h - (self.n * cell_size)) // 2

        for r in range(self.n):
            for c in range(self.n):
                x1 = offset_x + c * cell_size
                y1 = offset_y + r * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                # Background
                color = self.get_color(self.board[r][c])
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#7f8c8d")
                self.canvas.create_text(x1+10, y1+10, text=self.board[r][c], font=("Arial", 8))

                # Ratu / Animasi
                if solution_mask and solution_mask[r][c]:
                    pad = cell_size * 0.15
                    self.canvas.create_oval(x1+pad, y1+pad, x2-pad, y2-pad, fill="#e74c3c", outline="white", width=2)
                    self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text="Q", fill="white", font=("Times New Roman", int(cell_size/2), "bold"))
                elif trying_pos and trying_pos == (r, c):
                    pad = cell_size * 0.2
                    self.canvas.create_oval(x1+pad, y1+pad, x2-pad, y2-pad, fill="#f1c40f", outline="black")
                    self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text="?", fill="black", font=("Arial", int(cell_size/2), "bold"))

    # SOLVER THREAD

    def start_thread(self):
        self.stop_requested = False
        self.btn_solve.config(state=tk.DISABLED)
        self.btn_load.config(state=tk.DISABLED)
        self.btn_rand.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.lbl_status.config(text="Solving...", fg="blue")
        
        threading.Thread(target=self.run_solver_logic, daemon=True).start()

    def stop_solving(self):
        self.stop_requested = True
        self.log("Stopping process...")
        self.lbl_status.config(text="Stopping...", fg="red")

    def viz_callback(self, row, col, mask, is_trying):
        if self.stop_requested: return False
        
        if self.var_animate.get():
            self.root.after_idle(lambda: self.draw_board(mask, trying_pos=(row, col) if is_trying else None))
            time.sleep(self.scale_speed.get())
        return True

    def run_solver_logic(self):
        try:
            self.log("Solver started...")
            self.solver = QueenSolver(self.board)
            # Hubungkan callback visualisasi (nama disesuaikan dengan solver baru)
            self.solver.viz_function = self.viz_callback
            
            start_time = time.time()
            self.solver.start_solving()
            duration = time.time() - start_time
            
            self.root.after(0, lambda: self.on_finish(duration))
        except Exception as e:
            self.log(f"Error Solver: {e}")
            self.root.after(0, lambda: self.reset_buttons())

    def on_finish(self, duration):
        self.reset_buttons()
        if self.solver.found:
            msg = f"SOLVED! ({duration:.4f}s, {self.solver.iterations} iterasi)"
            self.log(msg)
            self.lbl_status.config(text=msg, fg="green")
            self.draw_board(self.solver.solution) 
            self.btn_save_txt.config(state=tk.NORMAL)
            self.btn_save_img.config(state=tk.NORMAL)
            messagebox.showinfo("Berhasil", "Solusi ditemukan!")
        else:
            msg = f"TIDAK ADA SOLUSI. ({duration:.4f}s)"
            self.log(msg)
            self.lbl_status.config(text=msg, fg="red")
            messagebox.showwarning("Selesai", "Tidak ada konfigurasi yang valid.")

    def reset_buttons(self):
        self.btn_solve.config(state=tk.NORMAL)
        self.btn_load.config(state=tk.NORMAL)
        self.btn_rand.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = QueensGUI(root)
    root.mainloop()