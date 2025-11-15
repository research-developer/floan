/**
 * FloAng UI Panel Controller
 * Handles user interactions and updates UI state
 */

import { calculateOrthogonalAngle } from '../flowangle-core.js';

// UI State
let currentParams = {
    sides: 3,
    flowFactor: -0.66,
    handleAngle: 60,
    rotation: -30
};

// Debug menu state
let debugMenuVisible = false;

/**
 * Initialize UI
 */
function initUI() {
    console.log('Initializing FloAng UI');

    // Set up event listeners
    setupPresetButtons();
    setupSliders();
    setupGenerateButton();
    setupDebugMenu();

    // Listen for events from main.js
    setupMainEventListeners();

    // Load saved parameters if available
    loadSavedParameters();
}

/**
 * Set up preset button handlers
 */
function setupPresetButtons() {
    const presetButtons = document.querySelectorAll('.preset-btn');

    presetButtons.forEach(button => {
        button.addEventListener('click', () => {
            const presetName = button.dataset.preset;

            // Remove active class from all buttons
            presetButtons.forEach(btn => btn.classList.remove('active'));

            // Add active class to clicked button
            button.classList.add('active');

            // Dispatch preset event
            window.dispatchEvent(new CustomEvent('floang:preset', {
                detail: { presetName }
            }));
        });
    });
}

/**
 * Set up slider event handlers
 */
function setupSliders() {
    // Sides slider
    const sidesSlider = document.getElementById('sides-slider');
    const sidesValue = document.getElementById('sides-value');

    sidesSlider.addEventListener('input', (e) => {
        const value = parseInt(e.target.value);
        sidesValue.textContent = value;
        updateParameter('sides', value);
    });

    // Flow slider
    const flowSlider = document.getElementById('flow-slider');
    const flowValue = document.getElementById('flow-value');

    flowSlider.addEventListener('input', (e) => {
        const value = parseFloat(e.target.value);
        flowValue.textContent = value.toFixed(2);
        updateParameter('flowFactor', value);
    });

    // Angle slider
    const angleSlider = document.getElementById('angle-slider');
    const angleValue = document.getElementById('angle-value');

    angleSlider.addEventListener('input', (e) => {
        const value = parseInt(e.target.value);
        angleValue.textContent = `${value}°`;
        updateParameter('handleAngle', value);
    });

    // Rotation slider
    const rotationSlider = document.getElementById('rotation-slider');
    const rotationValue = document.getElementById('rotation-value');

    rotationSlider.addEventListener('input', (e) => {
        const value = parseInt(e.target.value);
        rotationValue.textContent = `${value}°`;
        updateParameter('rotation', value);
    });
}

/**
 * Update a parameter and notify main.js
 * @param {string} parameter - Parameter name
 * @param {number} value - New value
 */
function updateParameter(parameter, value) {
    currentParams[parameter] = value;

    // Dispatch parameter change event
    window.dispatchEvent(new CustomEvent('floang:parameterChange', {
        detail: { parameter, value }
    }));

    // Update debug display
    updateDebugDisplay();
}

/**
 * Set up generate button handler
 */
function setupGenerateButton() {
    const generateBtn = document.getElementById('generate-btn');
    const statusMessage = document.getElementById('status-message');

    generateBtn.addEventListener('click', () => {
        // Disable button during generation
        generateBtn.disabled = true;
        generateBtn.classList.add('loading');
        statusMessage.textContent = 'Generating...';
        statusMessage.className = 'status-message info';

        // Dispatch generate event
        window.dispatchEvent(new CustomEvent('floang:generate'));
    });
}

/**
 * Set up debug menu handlers
 */
function setupDebugMenu() {
    const debugMenu = document.getElementById('debug-menu');
    const debugClose = document.getElementById('debug-close');

    // Keyboard shortcut: Cmd+Shift+D (Mac) or Ctrl+Shift+D (Windows)
    document.addEventListener('keydown', (e) => {
        if ((e.metaKey || e.ctrlKey) && e.shiftKey && e.key === 'D') {
            e.preventDefault();
            toggleDebugMenu();
        }
    });

    // Close button
    debugClose.addEventListener('click', () => {
        hideDebugMenu();
    });
}

/**
 * Toggle debug menu visibility
 */
function toggleDebugMenu() {
    debugMenuVisible = !debugMenuVisible;

    if (debugMenuVisible) {
        showDebugMenu();
    } else {
        hideDebugMenu();
    }
}

/**
 * Show debug menu
 */
function showDebugMenu() {
    const debugMenu = document.getElementById('debug-menu');
    debugMenu.style.display = 'block';
    debugMenuVisible = true;
    updateDebugDisplay();
}

/**
 * Hide debug menu
 */
function hideDebugMenu() {
    const debugMenu = document.getElementById('debug-menu');
    debugMenu.style.display = 'none';
    debugMenuVisible = false;
}

/**
 * Update debug display with current parameters
 */
function updateDebugDisplay() {
    const debugParams = document.getElementById('debug-params');
    if (debugParams && debugMenuVisible) {
        const orthogonalAngle = calculateOrthogonalAngle(currentParams.sides);
        debugParams.textContent = JSON.stringify({
            ...currentParams,
            orthogonalAngle: `${orthogonalAngle.toFixed(2)}°`
        }, null, 2);
    }
}

/**
 * Set up event listeners for main.js events
 */
function setupMainEventListeners() {
    // Listen for preset applied
    window.addEventListener('floang:presetApplied', (e) => {
        const { preset } = e.detail;
        updateUIFromPreset(preset);
    });

    // Listen for orthogonal angle update
    window.addEventListener('floang:orthogonalUpdate', (e) => {
        const { orthogonalAngle } = e.detail;
        updateAngleSliderRange(orthogonalAngle);
    });

    // Listen for generation start
    window.addEventListener('floang:generationStart', () => {
        showStatus('Generating pattern...', 'info');
    });

    // Listen for generation success
    window.addEventListener('floang:generationSuccess', () => {
        showStatus('Pattern generated successfully!', 'success');
        enableGenerateButton();
    });

    // Listen for generation error
    window.addEventListener('floang:generationError', (e) => {
        const { error } = e.detail;
        showStatus(`Error: ${error}`, 'error');
        enableGenerateButton();
    });
}

/**
 * Update UI controls from preset values
 * @param {Object} preset - Preset parameters
 */
function updateUIFromPreset(preset) {
    currentParams = { ...preset };

    // Update sliders and values
    document.getElementById('sides-slider').value = preset.sides;
    document.getElementById('sides-value').textContent = preset.sides;

    document.getElementById('flow-slider').value = preset.flowFactor;
    document.getElementById('flow-value').textContent = preset.flowFactor.toFixed(2);

    document.getElementById('angle-slider').value = preset.handleAngle;
    document.getElementById('angle-value').textContent = `${preset.handleAngle}°`;

    document.getElementById('rotation-slider').value = preset.rotation;
    document.getElementById('rotation-value').textContent = `${preset.rotation}°`;

    // Update angle slider range based on sides
    const orthogonalAngle = calculateOrthogonalAngle(preset.sides);
    updateAngleSliderRange(orthogonalAngle);

    // Update debug display
    updateDebugDisplay();
}

/**
 * Update angle slider range based on orthogonal angle
 * @param {number} orthogonalAngle - Orthogonal angle in degrees
 */
function updateAngleSliderRange(orthogonalAngle) {
    const angleSlider = document.getElementById('angle-slider');
    const minAngle = Math.max(10, orthogonalAngle - 50);
    const maxAngle = Math.min(170, orthogonalAngle + 50);

    angleSlider.min = minAngle;
    angleSlider.max = maxAngle;

    // Update markers
    document.getElementById('angle-min').textContent = `${Math.round(minAngle)}°`;
    document.getElementById('angle-max').textContent = `${Math.round(maxAngle)}°`;
    document.getElementById('angle-ortho').textContent = `${Math.round(orthogonalAngle)}°`;

    // Highlight orthogonal marker
    document.getElementById('angle-ortho').style.color = '#4CAF50';
    document.getElementById('angle-ortho').style.fontWeight = 'bold';
}

/**
 * Show status message
 * @param {string} message - Message text
 * @param {string} type - Message type (info, success, error)
 */
function showStatus(message, type) {
    const statusMessage = document.getElementById('status-message');
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;

    // Auto-hide success messages after 3 seconds
    if (type === 'success') {
        setTimeout(() => {
            statusMessage.textContent = '';
            statusMessage.className = 'status-message';
        }, 3000);
    }
}

/**
 * Enable generate button after generation completes
 */
function enableGenerateButton() {
    const generateBtn = document.getElementById('generate-btn');
    generateBtn.disabled = false;
    generateBtn.classList.remove('loading');
}

/**
 * Load saved parameters from localStorage
 */
function loadSavedParameters() {
    try {
        const saved = localStorage.getItem('floang:parameters');
        if (saved) {
            const params = JSON.parse(saved);
            updateUIFromPreset(params);
        }
    } catch (error) {
        console.warn('Failed to load saved parameters:', error);
    }
}

// Initialize on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initUI);
} else {
    initUI();
}
