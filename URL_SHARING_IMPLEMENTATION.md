# URL Sharing Implementation for FlowAngle Animation Studio

## Overview
A complete URL parameter system has been implemented for sharing FlowAngle configurations in `flowangle_animation.html`. This allows users to share and load specific configurations via URL.

## Features Implemented

### 1. State Serialization
- **Compact Parameter Names** for shorter URLs:
  - `s` = sides (number of sides)
  - `c` = curve factor
  - `a` = handle angle
  - `r` = rotation
  - `g` = show guides (1 or 0)
  - `kf` = keyframes (base64 encoded JSON)

- **Example URLs**:
  ```
  Basic configuration:
  http://localhost:8000/flowangle_animation.html#s=6&c=-0.800&a=30&r=0&g=0

  With keyframes:
  http://localhost:8000/flowangle_animation.html#s=3&c=-0.660&a=60&r=0&g=0&kf=W3sicz...
  ```

### 2. Share Button
- Added a green "Share Configuration" button in the controls panel
- Located after the "Show Guides" checkbox
- Styled with green background (`#4a4`) to distinguish from other buttons
- Visually consistent with existing design

### 3. Clipboard Functionality
- **Primary method**: Uses modern `navigator.clipboard.writeText()` API
- **Fallback method**: Uses legacy `document.execCommand('copy')` for older browsers
- **Manual fallback**: If all else fails, shows an alert with the URL to copy manually

### 4. Visual Feedback
- **Notification Element**: Centered modal-style notification
- **Animation**: Fades in when link is copied, auto-fades out after 2 seconds
- **Styling**:
  - Cyan border and text (#6cf)
  - Dark background (#2a2a2a)
  - Subtle glow shadow effect
  - Bold text: "Link copied to clipboard!"

### 5. URL Loading on Page Load
- **Automatic detection**: Checks for hash parameters on page initialization
- **Graceful fallback**: Uses defaults if no URL parameters present
- **Validation**: All parameters are validated before applying
  - Sides: 1-12
  - Handle Angle: 10-170 degrees
  - Rotation: Auto-normalized to 0-360 range
- **Keyframe support**: Decodes and loads keyframe animations if present

### 6. Auto-URL Updates
- **Debounced updates**: URL updates 500ms after last control change
- **Smart updates**: Doesn't update URL during animation playback
- **History-friendly**: Uses `history.replaceState()` to avoid polluting browser history

## Technical Implementation

### Functions

#### `encodeStateToURL(includeKeyframes = false)`
Encodes current state to URL hash parameters.
- Returns compact URL hash string
- Optionally includes keyframes (base64 encoded)
- Compresses numbers to 3 decimal places for curve factor

#### `loadFromURL()`
Decodes and applies URL parameters on page load.
- Returns `true` if state was loaded from URL
- Returns `false` if no parameters found
- Handles errors gracefully with console warnings

#### `updateURL()`
Updates browser URL without reloading (debounced).
- Called automatically after control changes
- Excluded during animations

#### `shareConfiguration()`
Main share function triggered by Share button.
- Generates full shareable URL
- Copies to clipboard
- Shows notification
- Updates browser URL
- Includes keyframes in share

#### `showShareNotification()`
Displays and hides the "Link copied!" message.
- 2-second display duration
- CSS transition for smooth fade

#### `fallbackCopyToClipboard(text)`
Legacy clipboard copy for older browsers.
- Creates temporary textarea
- Uses `document.execCommand('copy')`
- Shows alert if all methods fail

## Usage Examples

### Example 1: Share Basic Configuration
1. Adjust controls to desired settings (e.g., Flower preset)
2. Click "Share Configuration" button
3. URL is copied to clipboard automatically
4. Share the URL with others

### Example 2: Load Shared Configuration
1. Receive a shared URL like:
   ```
   http://localhost:8000/flowangle_animation.html#s=6&c=-0.800&a=30&r=0&g=0
   ```
2. Open the URL in browser
3. Configuration automatically loads with:
   - 6 sides
   - Curve factor: -0.8
   - Handle angle: 30°
   - Rotation: 0°
   - Guides: hidden

### Example 3: Share with Keyframes
1. Create multiple keyframes in the timeline
2. Click "Share Configuration"
3. URL includes base64-encoded keyframe data
4. Recipient gets full animation sequence

## URL Parameter Examples

### Triquetra (Default)
```
#s=3&c=-0.660&a=60&r=0&g=0
```

### Flower
```
#s=6&c=-0.800&a=30&r=0&g=1
```

### Star
```
#s=5&c=-1.200&a=36&r=18&g=0
```

### Smooth Circle
```
#s=8&c=-0.500&a=22.5&r=0&g=0
```

## File Changes

### Modified File
- `/Users/preston/research-developer/svGen/flowangle_animation.html`

### Key Changes
1. **CSS** (lines 300-331): Added styles for share button and notification
2. **HTML** (lines 389-395): Added Share button and notification element
3. **JavaScript** (line 554): Added `loadFromURL()` call on initialization
4. **JavaScript** (lines 898-1106): Added complete URL sharing functionality

## Browser Compatibility
- **Modern browsers**: Full clipboard API support
- **Older browsers**: Fallback to execCommand
- **All browsers**: Manual copy option as final fallback
- **URL parameters**: Supported in all modern browsers via URLSearchParams

## Security Considerations
- Uses URL hash (client-side only)
- No server requests for parameter handling
- Base64 encoding for keyframe data (not encryption)
- Input validation prevents invalid values

## Testing

### Manual Testing Steps
1. Open `flowangle_animation.html` in browser
2. Adjust any control (sides, curve, angle, rotation)
3. Click "Share Configuration" button
4. Verify "Link copied!" notification appears
5. Check URL in browser includes hash parameters
6. Copy URL and open in new tab
7. Verify configuration loads correctly
8. Test with keyframes:
   - Add 2-3 keyframes
   - Click "Share Configuration"
   - Open shared URL
   - Verify keyframes are restored

### Automated Testing (Future)
- Unit tests for encoding/decoding functions
- Integration tests for URL parameter parsing
- Cross-browser compatibility tests

## Future Enhancements
- Add URL compression for very long keyframe sequences
- Add preset sharing (named configurations)
- Add social media sharing buttons
- Add QR code generation for mobile sharing
- Add export/import JSON functionality
- Add permalink generation with shortened URLs

## Implementation Notes
- **Debouncing**: URL updates are debounced to 500ms to avoid excessive history entries
- **Animation handling**: URL doesn't update during animation playback
- **Keyframe compression**: Uses compact object keys (s, c, a, r, g) instead of full names
- **Decimal precision**: Curve factor limited to 3 decimal places for shorter URLs
- **Boolean encoding**: Uses 1/0 instead of true/false for compactness
