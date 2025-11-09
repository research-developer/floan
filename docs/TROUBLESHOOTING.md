# Troubleshooting Guide

## Development Server Issues

### "Address already in use" Error

**Problem:** Port 8000 (or 8001-8010) is already taken.

**Solutions:**

1. **Kill the existing process:**
   ```bash
   # macOS/Linux
   lsof -ti:8000 | xargs kill -9

   # Or find and kill manually
   lsof -i:8000
   kill <PID>
   ```

2. **The server will auto-find an available port** from 8000-8010
   - Check the startup message to see which port it's using
   - Update your browser URL if it's not on port 8000

3. **Change the default port:**
   Edit `dev_server.py` and change:
   ```python
   PORT = 8000  # Change to 8080, 3000, or any available port
   ```

### Server Exits Immediately

**Possible causes:**

1. **Port conflict** - See above
2. **Wrong directory** - Must run from repository root
3. **Python version** - Requires Python 3.7+

**Debug steps:**
```bash
# Run server directly to see error messages
python dev_server.py

# Check Python version
python --version  # Should be 3.7 or higher
```

### Files Not Appearing in Viewer

**Check:**

1. **Server is running:**
   ```bash
   curl http://localhost:8000/viewer.html
   ```

2. **SVG files exist:**
   ```bash
   ls -la outputs/
   ```

3. **Correct URL:**
   - Should be `http://localhost:PORT/viewer.html`
   - Not `file:///...viewer.html`

4. **Filename in viewer.html:**
   ```javascript
   // Edit viewer.html and check the svgFiles array
   const svgFiles = [
       'your_file.svg',  // Add your file here
       ...
   ];
   ```

5. **Browser cache:**
   - Try hard refresh: `Cmd/Ctrl + Shift + R`
   - Or clear cache

## File Watcher Issues

### Scripts Don't Auto-Run

**Check:**

1. **Watcher is running:**
   Look for "Watching N files..." message in terminal

2. **File is in watched directory:**
   - Must be in `examples/`, `templates/`, or `src/`
   - Check with: `ls examples/your_file.py`

3. **File has .py extension:**
   - Only `.py` files are watched

4. **No syntax errors:**
   ```bash
   python -m py_compile your_file.py
   ```

### Watcher Exits Unexpectedly

**Possible causes:**

1. **Script timeout** (30 seconds)
   - Reduce recursion depth during development
   - Increase timeout in `watch.py` if needed

2. **Infinite loop in script**
   - Check for missing base cases in recursion

**Debug:**
```bash
# Run watcher directly to see errors
python watch.py

# Or run script manually
python examples/your_script.py
```

## Combined Dev Environment Issues

### dev.py Exits Immediately

**Try the simple version:**
```bash
python dev_simple.py
```

This version is more robust and doesn't try to capture output.

**Or run components separately:**
```bash
# Terminal 1
python dev_server.py

# Terminal 2
python watch.py
```

### Can't See Output

**Use simple version:**
```bash
python dev_simple.py
```

This shows output directly without buffering.

## Script Errors

### Import Error: "No module named 'svg_generator'"

**Problem:** Script can't find the svg_generator module.

**Solution:** Check the import path at top of file:
```python
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from svg_generator import *
```

### File Not Found Error

**Problem:** Output path is incorrect.

**Solution:** Use relative paths:
```python
output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
os.makedirs(output_dir, exist_ok=True)
canvas.save(os.path.join(output_dir, 'my_file.svg'))
```

### RecursionError: maximum recursion depth exceeded

**Problem:** Recursion is too deep or missing base case.

**Solutions:**

1. **Reduce depth:**
   ```python
   # Instead of depth=10
   fractal(canvas, center, size, depth=5)  # Start smaller
   ```

2. **Check base case:**
   ```python
   def my_fractal(canvas, center, size, depth):
       if depth == 0:  # MUST have this
           return
       # ... recursive calls
   ```

3. **Increase Python recursion limit** (use with caution):
   ```python
   import sys
   sys.setrecursionlimit(3000)  # Default is 1000
   ```

## Performance Issues

### Slow Script Execution

**Solutions:**

1. **Reduce recursion depth** during development
2. **Use smaller canvas size:**
   ```python
   canvas = SVGCanvas(400, 400)  # Instead of 1000, 1000
   ```

3. **Simplify pattern temporarily**
4. **Check for O(n²) or worse complexity**

### Slow Browser Rendering

**Solutions:**

1. **Reduce number of elements:**
   - Lower recursion depth
   - Fewer iterations
   - Simpler shapes

2. **Optimize SVG:**
   - Combine paths where possible
   - Remove unnecessary elements

3. **View individual SVGs:**
   - Open single `.svg` file instead of viewer.html
   - Comment out large examples in viewer.html

## Common Mistakes

### Forgetting to Create Output Directory

**Error:** `FileNotFoundError: [Errno 2] No such file or directory: 'outputs/...'`

**Fix:** Always include:
```python
os.makedirs(output_dir, exist_ok=True)
```

### Hardcoded Absolute Paths

**Bad:**
```python
canvas.save("/mnt/user-data/outputs/file.svg")
```

**Good:**
```python
output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
canvas.save(os.path.join(output_dir, 'file.svg'))
```

### Missing Math Import

**Error:** `NameError: name 'math' is not defined`

**Fix:**
```python
import math
```

### Modifying Points In-Place

**Bad:**
```python
point.x += 10  # Point is immutable!
```

**Good:**
```python
point = Point(point.x + 10, point.y)
# Or
point = point + Point(10, 0)
```

## Getting Help

1. **Check error messages carefully** - they usually tell you what's wrong
2. **Run scripts directly** to see full output: `python examples/your_script.py`
3. **Add debug prints:**
   ```python
   print(f"Point: ({p.x}, {p.y})")
   print(f"Depth: {depth}")
   ```
4. **Visualize construction:**
   ```python
   # Mark important points
   canvas.circle(center, 5, fill="red")
   ```
5. **Check generated SVG** - open it in a text editor to inspect

## Still Having Issues?

1. **Verify Python version:** `python --version` (need 3.7+)
2. **Check file structure:**
   ```bash
   ls -la
   # Should see: src/, examples/, templates/, outputs/, viewer.html
   ```
3. **Try a fresh start:**
   ```bash
   # Regenerate all examples
   python examples/advanced_examples.py

   # Start simple dev server
   python dev_simple.py
   ```

4. **Test with minimal script:**
   ```python
   import os
   import sys
   sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
   from svg_generator import *

   canvas = SVGCanvas(400, 400)
   canvas.circle(Point(200, 200), 50, fill="blue")

   output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
   os.makedirs(output_dir, exist_ok=True)
   canvas.save(os.path.join(output_dir, 'test.svg'))
   print("✓ Success!")
   ```
