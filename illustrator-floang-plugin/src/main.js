/**
 * FloAng Illustrator Plugin - Main Entry Point
 * Initializes plugin and handles communication between UI and Illustrator
 */

import { generatePatternSafe } from './illustrator-adapter.js';
import { PRESETS, calculateOrthogonalAngle } from './flowangle-core.js';

// Plugin state
let currentParams = {
    sides: 3,
    flowFactor: -0.66,
    handleAngle: 60,
    rotation: -30
};

/**
 * Initialize plugin
 */
export function initPlugin() {
    console.log('FloAng plugin initialized');

    // Set up event listeners from UI panel
    setupEventListeners();

    // Apply default preset (triquetra)
    applyPreset('triquetra');
}

/**
 * Set up event listeners for UI panel communication
 */
function setupEventListeners() {
    // Listen for parameter changes from UI
    window.addEventListener('floang:parameterChange', handleParameterChange);
    window.addEventListener('floang:generate', handleGenerate);
    window.addEventListener('floang:preset', handlePreset);
}

/**
 * Handle parameter change from UI
 * @param {CustomEvent} event - Event with parameter details
 */
function handleParameterChange(event) {
    const { parameter, value } = event.detail;

    currentParams[parameter] = value;

    // Update orthogonal angle range if sides changed
    if (parameter === 'sides') {
        const orthogonalAngle = calculateOrthogonalAngle(value);
        // Notify UI to update angle slider range
        window.dispatchEvent(new CustomEvent('floang:orthogonalUpdate', {
            detail: { orthogonalAngle }
        }));
    }

    // Persist parameters to localStorage
    saveParameters();

    console.log('Parameter updated:', parameter, '=', value);
}

/**
 * Handle generate button click
 * @param {CustomEvent} event - Generate event
 */
async function handleGenerate(event) {
    console.log('Generating pattern with params:', currentParams);

    // Notify UI that generation started
    window.dispatchEvent(new CustomEvent('floang:generationStart'));

    try {
        const result = await generatePatternSafe(currentParams);

        if (result.success) {
            // Notify UI of success
            window.dispatchEvent(new CustomEvent('floang:generationSuccess', {
                detail: { pathItem: result.pathItem }
            }));
            console.log('Pattern generated successfully');
        } else {
            // Notify UI of error
            window.dispatchEvent(new CustomEvent('floang:generationError', {
                detail: { error: result.error }
            }));
            console.error('Generation failed:', result.error);
        }
    } catch (error) {
        window.dispatchEvent(new CustomEvent('floang:generationError', {
            detail: { error: error.message }
        }));
        console.error('Generation error:', error);
    }
}

/**
 * Handle preset selection
 * @param {CustomEvent} event - Preset event with preset name
 */
function handlePreset(event) {
    const { presetName } = event.detail;
    applyPreset(presetName);
}

/**
 * Apply a preset configuration
 * @param {string} presetName - Name of preset (triquetra, flower, star, smooth)
 */
function applyPreset(presetName) {
    const preset = PRESETS[presetName];

    if (!preset) {
        console.error('Unknown preset:', presetName);
        return;
    }

    // Update current parameters
    currentParams = { ...preset };

    // Notify UI to update controls
    window.dispatchEvent(new CustomEvent('floang:presetApplied', {
        detail: { preset: currentParams, presetName }
    }));

    // Persist to localStorage
    saveParameters();

    console.log('Preset applied:', presetName, preset);
}

/**
 * Save current parameters to localStorage
 */
function saveParameters() {
    try {
        localStorage.setItem('floang:parameters', JSON.stringify(currentParams));
    } catch (error) {
        console.warn('Failed to save parameters:', error);
    }
}

/**
 * Load parameters from localStorage
 */
function loadParameters() {
    try {
        const saved = localStorage.getItem('floang:parameters');
        if (saved) {
            currentParams = JSON.parse(saved);
            console.log('Loaded saved parameters:', currentParams);
        }
    } catch (error) {
        console.warn('Failed to load parameters:', error);
    }
}

/**
 * Get current parameters
 * @returns {Object} Current parameters
 */
export function getCurrentParameters() {
    return { ...currentParams };
}

// Initialize on load
if (typeof window !== 'undefined') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initPlugin);
    } else {
        initPlugin();
    }
}
