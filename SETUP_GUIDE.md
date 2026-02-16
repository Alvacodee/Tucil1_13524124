# Setup Guide

Panduan setup Queens Puzzle Solver dengan UV.

## Requirements

- Python 3.13
- UV (package manager)
- Pillow (untuk export image)
- Tkinter (untuk GUI)

## Installation

### 1. Check Python

```bash
python --version
# atau
python3 --version
```

### 2. Install UV

Jika belum punya UV:

```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/Mac
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify:
```bash
uv --version
```

### 3. Setup Project

```bash
# Clone Repository
git clone https://github.com/Alvacodee/Tucil1_13524124.git

# Change Directory
cd Tucil1_13524124

# Initialize (jika belum)
uv init

# Sync dependencies dari pyproject.toml
uv sync

# Add Pillow
uv add pillow
```

### 4. Check Tkinter

```bash
python -m tkinter
```

Kalau muncul window kecil → OK  

## Verification

```bash
uv --version
python --version
python -c "from PIL import Image; print('Pillow OK')"
python -m tkinter
```

Kalau semua OK, siap running.

## First Run

```bash
uv run python main.py
atau
python main.py # pastikan interpreter yang menggunakan UV telah di aplikasikan
```

## Common Issues

| Problem | Fix |
|---------|-----|
| No module PIL | `uv add pillow && uv sync` |
| No tkinter | Check SETUP_GUIDE.md |
| Import error | Run with `uv run python main.py` |
| UV command not found | Install UV first |

## Common UV Commands

UV secara otomatis manage virtual environment. Tidak perlu aktivasi manual.

Commands yang sering dipakai:
```bash
uv sync           # Sync dependencies
uv add <package>  # Add package
uv remove <package>   # Remove package
uv run <command>  # Run command in venv
uv --version      # Check UV version
```

## Tips

- Board >10x10 akan lambat karena brute force
- Gunakan ≤8x8 untuk testing
- GUI freeze/hang jika boardnya besar karena algoritma brute (memerlukan waktu yang cukup lama) membuatnya tidak responsif
