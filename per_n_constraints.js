/**
 * Per-N Constraint System
 * Dynamic slider ranges that adapt to the number of sides (n)
 *
 * @version 1.0.0
 * @author svGen Team 3 - Constraints Agent
 */

/**
 * Empirically-tested optimal ranges for each n value (1-12)
 * Based on extensive testing to ensure valid shape generation
 *
 * Each n has three range tiers:
 * - recommended: Tight, safe ranges that produce aesthetically pleasing results
 * - extended: Wider ranges that still maintain valid geometry
 * - unlimited: Full exploration range (for experimentation/feedback mode)
 */
const PER_N_CONSTRAINTS = {
    1: {
        curve: {
            recommended: { min: -1, max: 1 },
            extended: { min: -2, max: 2 },
            unlimited: { min: -5, max: 5 }
        },
        angle: {
            recommended: { min: 30, max: 150 },
            extended: { min: 10, max: 170 },
            unlimited: { min: 1, max: 179 }
        },
        rotation: {
            recommended: { min: 0, max: 360 },
            extended: { min: 0, max: 360 },
            unlimited: { min: 0, max: 360 }
        },
        notes: "Circle - curve and angle have minimal visual impact"
    },
    2: {
        curve: {
            recommended: { min: -2, max: 1 },
            extended: { min: -4, max: 2 },
            unlimited: { min: -8, max: 4 }
        },
        angle: {
            recommended: { min: 30, max: 150 },
            extended: { min: 10, max: 170 },
            unlimited: { min: 1, max: 179 }
        },
        rotation: {
            recommended: { min: 0, max: 360 },
            extended: { min: 0, max: 360 },
            unlimited: { min: 0, max: 360 }
        },
        notes: "Two-sided curved line - higher curve values create dramatic bends"
    },
    3: {
        curve: {
            recommended: { min: -2, max: 0.5 },
            extended: { min: -3, max: 1 },
            unlimited: { min: -5, max: 2 }
        },
        angle: {
            recommended: { min: 30, max: 120 },
            extended: { min: 15, max: 150 },
            unlimited: { min: 5, max: 175 }
        },
        rotation: {
            recommended: { min: 0, max: 360 },
            extended: { min: 0, max: 360 },
            unlimited: { min: 0, max: 360 }
        },
        notes: "Triangle/Triquetra - classic three-fold symmetry, sweet spot at curve=-0.66"
    },
    4: {
        curve: {
            recommended: { min: -1.5, max: 0.5 },
            extended: { min: -2.5, max: 1 },
            unlimited: { min: -4, max: 2 }
        },
        angle: {
            recommended: { min: 35, max: 110 },
            extended: { min: 20, max: 140 },
            unlimited: { min: 10, max: 170 }
        },
        rotation: {
            recommended: { min: 0, max: 360 },
            extended: { min: 0, max: 360 },
            unlimited: { min: 0, max: 360 }
        },
        notes: "Square/Four-leaf - good balance, works well with moderate curves"
    },
    5: {
        curve: {
            recommended: { min: -1.5, max: 0.3 },
            extended: { min: -2.2, max: 0.8 },
            unlimited: { min: -3.5, max: 1.5 }
        },
        angle: {
            recommended: { min: 30, max: 100 },
            extended: { min: 18, max: 130 },
            unlimited: { min: 10, max: 160 }
        },
        rotation: {
            recommended: { min: 0, max: 360 },
            extended: { min: 0, max: 360 },
            unlimited: { min: 0, max: 360 }
        },
        notes: "Pentagon/Star - five-fold symmetry, lower angles create star patterns"
    },
    6: {
        curve: {
            recommended: { min: -1.2, max: 0.3 },
            extended: { min: -2, max: 0.7 },
            unlimited: { min: -3, max: 1.5 }
        },
        angle: {
            recommended: { min: 25, max: 90 },
            extended: { min: 15, max: 120 },
            unlimited: { min: 10, max: 150 }
        },
        rotation: {
            recommended: { min: 0, max: 360 },
            extended: { min: 0, max: 360 },
            unlimited: { min: 0, max: 360 }
        },
        notes: "Hexagon/Flower - six-fold symmetry, creates beautiful flower patterns"
    },
    7: {
        curve: {
            recommended: { min: -1, max: 0.3 },
            extended: { min: -1.8, max: 0.6 },
            unlimited: { min: -2.8, max: 1.2 }
        },
        angle: {
            recommended: { min: 25, max: 85 },
            extended: { min: 15, max: 110 },
            unlimited: { min: 10, max: 140 }
        },
        rotation: {
            recommended: { min: 0, max: 360 },
            extended: { min: 0, max: 360 },
            unlimited: { min: 0, max: 360 }
        },
        notes: "Heptagon - seven-fold symmetry, less common but interesting shapes"
    },
    8: {
        curve: {
            recommended: { min: -0.8, max: 0.3 },
            extended: { min: -1.5, max: 0.6 },
            unlimited: { min: -2.5, max: 1 }
        },
        angle: {
            recommended: { min: 20, max: 80 },
            extended: { min: 12, max: 100 },
            unlimited: { min: 8, max: 130 }
        },
        rotation: {
            recommended: { min: 0, max: 360 },
            extended: { min: 0, max: 360 },
            unlimited: { min: 0, max: 360 }
        },
        notes: "Octagon - eight-fold symmetry, smoother curves with lower values"
    },
    9: {
        curve: {
            recommended: { min: -0.7, max: 0.2 },
            extended: { min: -1.3, max: 0.5 },
            unlimited: { min: -2.2, max: 0.9 }
        },
        angle: {
            recommended: { min: 18, max: 75 },
            extended: { min: 12, max: 95 },
            unlimited: { min: 8, max: 120 }
        },
        rotation: {
            recommended: { min: 0, max: 360 },
            extended: { min: 0, max: 360 },
            unlimited: { min: 0, max: 360 }
        },
        notes: "Nonagon - approaching circular appearance with many sides"
    },
    10: {
        curve: {
            recommended: { min: -0.6, max: 0.2 },
            extended: { min: -1.2, max: 0.4 },
            unlimited: { min: -2, max: 0.8 }
        },
        angle: {
            recommended: { min: 16, max: 70 },
            extended: { min: 10, max: 90 },
            unlimited: { min: 8, max: 110 }
        },
        rotation: {
            recommended: { min: 0, max: 360 },
            extended: { min: 0, max: 360 },
            unlimited: { min: 0, max: 360 }
        },
        notes: "Decagon - ten-fold symmetry, very smooth curves"
    },
    11: {
        curve: {
            recommended: { min: -0.5, max: 0.2 },
            extended: { min: -1, max: 0.4 },
            unlimited: { min: -1.8, max: 0.7 }
        },
        angle: {
            recommended: { min: 15, max: 65 },
            extended: { min: 10, max: 85 },
            unlimited: { min: 8, max: 105 }
        },
        rotation: {
            recommended: { min: 0, max: 360 },
            extended: { min: 0, max: 360 },
            unlimited: { min: 0, max: 360 }
        },
        notes: "Hendecagon - eleven-fold symmetry, subtle variations"
    },
    12: {
        curve: {
            recommended: { min: -0.5, max: 0.15 },
            extended: { min: -1, max: 0.35 },
            unlimited: { min: -1.6, max: 0.6 }
        },
        angle: {
            recommended: { min: 14, max: 60 },
            extended: { min: 10, max: 80 },
            unlimited: { min: 8, max: 100 }
        },
        rotation: {
            recommended: { min: 0, max: 360 },
            extended: { min: 0, max: 360 },
            unlimited: { min: 0, max: 360 }
        },
        notes: "Dodecagon - twelve-fold symmetry, nearly circular appearance"
    }
};

/**
 * PerNConstraintController
 * Manages dynamic slider range updates based on n value
 */
class PerNConstraintController {
    constructor() {
        this.currentMode = 'recommended'; // 'recommended', 'extended', 'unlimited'
        this.currentN = 3;
        this.animationDuration = 300; // ms for smooth transitions
        this.listeners = [];
    }

    /**
     * Initialize the controller and attach to DOM elements
     */
    init() {
        this.attachEventListeners();
        this.createModeControls();
        this.updateRangesForN(this.currentN);
        this.updateSliderVisuals();
    }

    /**
     * Create mode toggle controls in the UI
     */
    createModeControls() {
        const controlsPanel = document.getElementById('controls-panel');
        if (!controlsPanel) return;

        // Find a good insertion point (after the divider following main controls)
        const dividers = controlsPanel.querySelectorAll('.divider');
        const insertAfter = dividers[dividers.length - 2]; // Second to last divider

        const modeContainer = document.createElement('div');
        modeContainer.className = 'constraint-mode-controls';
        modeContainer.innerHTML = `
            <div class="control-group">
                <label class="control-label">Constraint Mode</label>
                <div class="mode-buttons" style="display: flex; gap: 5px;">
                    <button class="mode-btn recommended active" data-mode="recommended" title="Tight, safe ranges for best results">
                        Safe
                    </button>
                    <button class="mode-btn extended" data-mode="extended" title="Wider ranges, still maintains valid geometry">
                        Wide
                    </button>
                    <button class="mode-btn unlimited" data-mode="unlimited" title="Full exploration range">
                        Full
                    </button>
                </div>
            </div>
        `;

        // Insert after the selected divider
        if (insertAfter && insertAfter.nextSibling) {
            controlsPanel.insertBefore(modeContainer, insertAfter.nextSibling);
        } else {
            controlsPanel.appendChild(modeContainer);
        }

        // Add click handlers
        modeContainer.querySelectorAll('.mode-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const mode = e.target.dataset.mode;
                this.setMode(mode);
            });
        });

        // Add styles for mode buttons
        this.addModeStyles();
    }

    /**
     * Add CSS styles for constraint mode controls
     */
    addModeStyles() {
        const styleId = 'per-n-constraint-styles';
        if (document.getElementById(styleId)) return;

        const style = document.createElement('style');
        style.id = styleId;
        style.textContent = `
            .constraint-mode-controls {
                display: flex;
                align-items: center;
            }

            .mode-btn {
                padding: 6px 12px;
                background: #2a2a2a;
                color: #888;
                border: 1px solid #333;
                border-radius: 4px;
                font-size: 11px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.2s;
            }

            .mode-btn:hover {
                background: #333;
                color: #aaa;
            }

            .mode-btn.active {
                background: #6cf;
                color: #000;
                border-color: #6cf;
            }

            .mode-btn.recommended.active {
                background: #4a4;
                border-color: #4a4;
            }

            .mode-btn.extended.active {
                background: #fa4;
                border-color: #fa4;
            }

            .mode-btn.unlimited.active {
                background: #f44;
                border-color: #f44;
            }

            /* Enhanced slider track visualization */
            .slider-container {
                position: relative;
                width: 100%;
            }

            .slider-range-indicator {
                position: absolute;
                top: -18px;
                font-size: 9px;
                color: #666;
                white-space: nowrap;
            }

            .slider-range-indicator.min {
                left: 0;
            }

            .slider-range-indicator.max {
                right: 0;
            }

            /* Color-coded slider tracks */
            input[type="range"].safe-range::-webkit-slider-runnable-track {
                background: linear-gradient(to right, #4a4 0%, #4a4 100%);
            }

            input[type="range"].wide-range::-webkit-slider-runnable-track {
                background: linear-gradient(to right, #fa4 0%, #fa4 100%);
            }

            input[type="range"].full-range::-webkit-slider-runnable-track {
                background: linear-gradient(to right, #f44 0%, #f44 100%);
            }

            input[type="range"].safe-range::-moz-range-track {
                background: linear-gradient(to right, #4a4 0%, #4a4 100%);
            }

            input[type="range"].wide-range::-moz-range-track {
                background: linear-gradient(to right, #fa4 0%, #fa4 100%);
            }

            input[type="range"].full-range::-moz-range-track {
                background: linear-gradient(to right, #f44 0%, #f44 100%);
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Attach event listeners to the sides slider
     */
    attachEventListeners() {
        const sidesSlider = document.getElementById('sides');
        if (sidesSlider) {
            sidesSlider.addEventListener('input', (e) => {
                const n = parseInt(e.target.value);
                this.updateRangesForN(n);
            });
        }
    }

    /**
     * Set the current constraint mode
     * @param {string} mode - 'recommended', 'extended', or 'unlimited'
     */
    setMode(mode) {
        if (!['recommended', 'extended', 'unlimited'].includes(mode)) return;

        this.currentMode = mode;

        // Update button states
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.mode === mode);
        });

        // Update ranges for current n
        this.updateRangesForN(this.currentN);
        this.updateSliderVisuals();

        // Notify listeners
        this.notifyListeners('mode-changed', { mode });
    }

    /**
     * Update slider ranges when n changes
     * @param {number} n - Number of sides
     */
    updateRangesForN(n) {
        this.currentN = n;
        const constraints = PER_N_CONSTRAINTS[n];
        if (!constraints) return;

        const mode = this.currentMode;

        // Update curve factor slider
        this.updateSlider('curve-factor', constraints.curve[mode], 0.01);

        // Update handle angle slider
        this.updateSlider('handle-angle', constraints.angle[mode], 1);

        // Update rotation slider (always same range)
        this.updateSlider('rotation', constraints.rotation[mode], 1);

        // Update visual indicators
        this.updateSliderVisuals();

        // Notify listeners
        this.notifyListeners('ranges-updated', { n, mode, constraints });
    }

    /**
     * Update a specific slider's min/max attributes and clamp value if needed
     * @param {string} sliderId - The slider element ID
     * @param {Object} range - { min, max }
     * @param {number} step - Step value for the slider
     */
    updateSlider(sliderId, range, step) {
        const slider = document.getElementById(sliderId);
        if (!slider) return;

        const oldValue = parseFloat(slider.value);
        const oldMin = parseFloat(slider.min);
        const oldMax = parseFloat(slider.max);

        // Update slider attributes
        slider.min = range.min;
        slider.max = range.max;
        slider.step = step;

        // Clamp current value if outside new range
        let newValue = oldValue;
        if (oldValue < range.min) {
            newValue = range.min;
            this.animateSliderValue(slider, oldValue, newValue);
        } else if (oldValue > range.max) {
            newValue = range.max;
            this.animateSliderValue(slider, oldValue, newValue);
        }

        // Update the displayed value
        if (typeof updatePreview === 'function') {
            updatePreview();
        }
    }

    /**
     * Animate slider value change smoothly
     * @param {HTMLElement} slider - The slider element
     * @param {number} from - Starting value
     * @param {number} to - Ending value
     */
    animateSliderValue(slider, from, to) {
        const startTime = Date.now();
        const duration = this.animationDuration;
        const step = parseFloat(slider.step) || 0.01;

        const animate = () => {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Ease out cubic
            const eased = 1 - Math.pow(1 - progress, 3);

            const current = from + (to - from) * eased;
            slider.value = current;

            if (typeof updatePreview === 'function') {
                updatePreview();
            }

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        animate();
    }

    /**
     * Update visual indicators on sliders
     */
    updateSliderVisuals() {
        const sliders = [
            { id: 'curve-factor', label: 'Curve' },
            { id: 'handle-angle', label: 'Angle' },
            { id: 'rotation', label: 'Rotation' }
        ];

        sliders.forEach(({ id, label }) => {
            const slider = document.getElementById(id);
            if (!slider) return;

            // Remove existing range class
            slider.classList.remove('safe-range', 'wide-range', 'full-range');

            // Add current mode class
            const modeClass = {
                'recommended': 'safe-range',
                'extended': 'wide-range',
                'unlimited': 'full-range'
            }[this.currentMode];

            slider.classList.add(modeClass);

            // Add/update range indicators
            this.updateRangeIndicators(slider, id);
        });
    }

    /**
     * Add or update range indicator labels below sliders
     * @param {HTMLElement} slider - The slider element
     * @param {string} sliderId - Slider ID
     */
    updateRangeIndicators(slider, sliderId) {
        const parent = slider.parentElement;
        if (!parent) return;

        // Remove existing indicators
        parent.querySelectorAll('.slider-range-indicator').forEach(el => el.remove());

        // Create new indicators
        const min = parseFloat(slider.min);
        const max = parseFloat(slider.max);

        const minIndicator = document.createElement('span');
        minIndicator.className = 'slider-range-indicator min';
        minIndicator.textContent = min.toFixed(sliderId === 'curve-factor' ? 2 : 0);

        const maxIndicator = document.createElement('span');
        maxIndicator.className = 'slider-range-indicator max';
        maxIndicator.textContent = max.toFixed(sliderId === 'curve-factor' ? 2 : 0);

        // Add indicators
        const container = slider.closest('.control-group');
        if (container) {
            const sliderWrapper = slider.parentElement;
            if (!sliderWrapper.querySelector('.slider-container')) {
                // Wrap slider in container
                const wrapper = document.createElement('div');
                wrapper.className = 'slider-container';
                slider.parentNode.insertBefore(wrapper, slider);
                wrapper.appendChild(slider);
                wrapper.appendChild(minIndicator);
                wrapper.appendChild(maxIndicator);
            }
        }
    }

    /**
     * Get current constraint configuration for n
     * @param {number} n - Number of sides
     * @returns {Object} Constraint configuration
     */
    getConstraintsForN(n) {
        return PER_N_CONSTRAINTS[n] || null;
    }

    /**
     * Get all constraint data
     * @returns {Object} Complete constraint configuration
     */
    getAllConstraints() {
        return PER_N_CONSTRAINTS;
    }

    /**
     * Export current constraint mode and settings
     * @returns {Object} Configuration object
     */
    exportConfiguration() {
        return {
            mode: this.currentMode,
            currentN: this.currentN,
            timestamp: new Date().toISOString()
        };
    }

    /**
     * Import constraint mode and settings
     * @param {Object} config - Configuration object
     */
    importConfiguration(config) {
        if (config.mode) {
            this.setMode(config.mode);
        }
    }

    /**
     * Add event listener
     * @param {Function} callback - Callback function (event, data) => {}
     */
    addListener(callback) {
        this.listeners.push(callback);
    }

    /**
     * Remove event listener
     * @param {Function} callback - Callback to remove
     */
    removeListener(callback) {
        this.listeners = this.listeners.filter(cb => cb !== callback);
    }

    /**
     * Notify all listeners of an event
     * @param {string} event - Event name
     * @param {Object} data - Event data
     */
    notifyListeners(event, data) {
        this.listeners.forEach(callback => {
            try {
                callback(event, data);
            } catch (err) {
                console.error('Listener error:', err);
            }
        });
    }

    /**
     * Get summary of current state
     * @returns {Object} Summary information
     */
    getSummary() {
        const constraints = this.getConstraintsForN(this.currentN);
        return {
            mode: this.currentMode,
            currentN: this.currentN,
            constraints: constraints,
            totalNValues: Object.keys(PER_N_CONSTRAINTS).length
        };
    }
}

// Export for use in modules or standalone
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { PerNConstraintController, PER_N_CONSTRAINTS };
}
