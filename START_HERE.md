# 🚀 Start Here

## Quick Start (Choose One Method)

### Method 1: Simple & Reliable (Recommended)
```bash
python dev_simple.py
```
✅ Most reliable, output appears directly
✅ Best for beginners
✅ Auto-finds available port

### Method 2: Formatted Output
```bash
python dev.py
```
✅ Prefixed output ([Server], [Watcher])
✅ Slightly more complex
⚠️ May have buffering issues on some systems

### Method 3: Separate Windows
```bash
# Terminal 1
python dev_server.py

# Terminal 2 (separate window)
python watch.py
```
✅ Full control
✅ See each component's output clearly
⚠️ Requires two terminal windows

## What Happens

All methods start:
1. **HTTP Server** on http://localhost:8000 (or next available port)
2. **File Watcher** monitoring `examples/` and `templates/`

## Workflow

1. **Start dev environment** (pick a method above)
2. **Open browser** to `http://localhost:8000/viewer.html`
3. **Edit a Python file** in `examples/` or `templates/`
4. **Save file** → Script auto-runs
5. **Refresh browser** → See your SVG!

## Your First Edit

Try this:

1. Start dev environment:
   ```bash
   python dev_simple.py
   ```

2. Open `http://localhost:8000/viewer.html` in browser

3. Edit `templates/experiment_template.py`:
   ```python
   # Line 116: Change the fill color
   canvas.polygon(triangle, fill="purple", stroke="navy", stroke_width=3)
   ```

4. Save file → Watch terminal for "✓ Success"

5. Refresh browser → See purple triangle!

## Common Commands

```bash
# Generate all examples
python examples/advanced_examples.py
python examples/research_examples.py

# Run a single script
python templates/experiment_template.py

# Start dev environment (pick one)
python dev_simple.py      # Recommended
python dev.py             # Alternative
python dev_server.py      # Server only
python watch.py           # Watcher only

# Kill all processes on port 8000
lsof -ti:8000 | xargs kill -9
```

## Troubleshooting

**Server exits immediately?**
→ See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

**Port 8000 in use?**
→ Server auto-finds 8001-8010, or kill existing: `lsof -ti:8000 | xargs kill -9`

**Files don't auto-run?**
→ Make sure file is in `examples/` or `templates/` directory

**SVGs don't appear?**
→ Check `outputs/` folder exists and has `.svg` files

## Next Steps

- Read [DEVELOPMENT.md](docs/DEVELOPMENT.md) for full workflow guide
- Check [QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md) for API cheat sheet
- Explore `examples/advanced_examples.py` for inspiration
- Copy `templates/experiment_template.py` to start your own

## File Structure

```
svGen/
├── dev_simple.py          ← START WITH THIS
├── dev.py                 ← Or this (alternative)
├── dev_server.py          ← HTTP server only
├── watch.py               ← File watcher only
├── viewer.html            ← Open in browser
├── src/                   ← Core library
├── examples/              ← Built-in examples
├── templates/             ← Your starting point
└── outputs/               ← Generated SVGs
```

---

**Ready? Start with:**
```bash
python dev_simple.py
```

Then open: `http://localhost:8000/viewer.html` 🎨
