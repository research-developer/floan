# Development Guide

This guide explains how to work with the svGen framework in a live development environment.

## Quick Start

```bash
# Start the development environment
python dev.py
```

Then open `http://localhost:8000/viewer.html` in your browser.

## What You Get

The development environment provides three key features:

### 1. HTTP Server (Port 8000)
- Serves `viewer.html` and all generated SVGs
- Properly handles CORS for local development
- No caching, always serves fresh files

### 2. File Watcher
- Monitors `examples/`, `templates/`, and `src/` directories
- Automatically runs scripts when you save changes
- Shows output and errors in terminal

### 3. Visual Feedback Loop
Edit → Save → Auto-generate → Refresh browser → See results

## Development Workflows

### Interactive Experimentation

**Best for:** Trying out ideas, tweaking parameters, exploring patterns

1. Start dev environment: `python dev.py`
2. Open browser to `http://localhost:8000/viewer.html`
3. Open `templates/experiment_template.py` in your editor
4. Make changes (e.g., adjust fractal depth, colors, sizes)
5. Save file
6. Watch terminal for "✓ Success" message
7. Refresh browser to see results

### Creating New Examples

**Best for:** Building complete, reusable patterns

1. Copy template: `cp templates/experiment_template.py examples/my_pattern.py`
2. Edit `examples/my_pattern.py`
3. Dev environment auto-runs on save
4. View results in browser

### Debugging

**Best for:** Understanding why something doesn't work

The file watcher shows:
- Script output (print statements)
- Errors and stack traces
- Success/failure status
- Timestamps

Add debug visualizations:
```python
# Mark important points in red
canvas.circle(center, 5, fill="red")

# Draw construction lines
canvas.line(p1, p2, stroke="red", stroke_width=0.5)

# Print coordinates
print(f"Center: ({center.x}, {center.y})")
```

## Development Tools

### dev.py - Full Development Environment
Runs both server and watcher together.

```bash
python dev.py
```

**Use when:** You want the complete live-reload experience

### dev_server.py - HTTP Server Only
Just serves files, no auto-regeneration.

```bash
python dev_server.py
```

**Use when:**
- You want to manually control when scripts run
- You're working on documentation or viewer.html
- You want to review existing outputs

### watch.py - File Watcher Only
Monitors and auto-runs scripts, but doesn't serve files.

```bash
python watch.py
```

**Use when:**
- You're viewing SVGs in a different way (e.g., directly in Finder/Explorer)
- You have a different server running
- You want to see script output without browser overhead

## Tips & Tricks

### Rapid Iteration
1. Keep browser window visible next to editor
2. Use `Cmd/Ctrl + R` for quick refresh
3. Use smaller canvas sizes during development (faster rendering)
4. Start with low recursion depth, increase when pattern looks right

### Performance
- Scripts timeout after 30 seconds (configurable in `watch.py`)
- Large recursion depths can be slow - test with depth 3-4 first
- Complex patterns: break into smaller functions

### Multiple Experiments
The watcher monitors all files in `examples/` and `templates/`:
- Edit multiple files
- Each auto-runs independently
- All outputs visible in viewer

### Browser Auto-Refresh (Optional)

For true live-reload without manual refresh, use browser extensions:
- **Chrome/Edge:** Live Server or Auto Refresh
- **Firefox:** Auto Reload
- **Safari:** Live Reload

Configure to watch: `http://localhost:8000/viewer.html`

## Common Patterns

### Quick Color Test
```python
# Test different color schemes quickly
for i, hue in enumerate([0, 60, 120, 180, 240, 300]):
    color = f"hsl({hue}, 70%, 60%)"
    # ... use color in your pattern
```

### Parameter Sweep
```python
# Generate multiple variations
for depth in range(3, 7):
    canvas = SVGCanvas(400, 400)
    my_fractal(canvas, Point(200, 200), 100, depth)
    canvas.save(os.path.join(output_dir, f'fractal_depth_{depth}.svg'))
```

### Composition Testing
```python
# Build up complexity incrementally
def test_pattern(canvas, center, size):
    # Step 1: Basic shape
    pts = equilateral_triangle(center, size)
    canvas.polygon(pts, fill="lightblue")

    # Step 2: Add rotation
    # pts = rotate_points(pts, math.pi/6, center)
    # canvas.polygon(pts, fill="none", stroke="blue")

    # Step 3: Add recursion
    # ... add more as you verify each step works
```

## Troubleshooting

### "Address already in use" Error
Another process is using port 8000.

**Solutions:**
1. Stop the other process
2. Edit `dev_server.py`, change `PORT = 8000` to another port
3. Kill the process: `lsof -ti:8000 | xargs kill`

### Script Doesn't Auto-Run
Check that:
1. File is in `examples/` or `templates/` directory
2. File ends with `.py`
3. No syntax errors (watcher shows errors in terminal)
4. Watcher is running (look for "Watching N files..." message)

### SVGs Don't Appear in Viewer
Check that:
1. Script ran successfully (green ✓ in terminal)
2. SVG file exists in `outputs/` directory
3. Filename is listed in `viewer.html` (edit the `svgFiles` array)
4. Browser cache cleared (try hard refresh: `Cmd/Ctrl + Shift + R`)

### Slow Performance
- Reduce recursion depth
- Use smaller canvas size during development
- Simplify pattern temporarily
- Check for infinite loops

## Next Steps

- Check out `examples/advanced_examples.py` for inspiration
- Read `QUICK_REFERENCE.md` for API documentation
- Explore `research_examples.py` for advanced patterns
- Join the community (if available) to share your creations!
