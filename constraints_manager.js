/**
 * ConstraintManager - Modular constraint management system
 * Handles dynamic range limits with localStorage persistence and JSON import/export
 *
 * @version 1.0.0
 * @author svGen Team 3
 */

class ConstraintManager {
    constructor(storageKey = 'svgen_constraints') {
        this.storageKey = storageKey;
        this.constraints = this.loadFromLocalStorage() || {};
        this.feedbackMode = false;
        this.listeners = [];

        // Default expanded ranges for feedback mode
        this.defaultRanges = {
            curveFactor: { min: -10, max: 10, step: 0.01 },
            handleAngle: { min: 1, max: 179, step: 1 },
            size: { min: 10, max: 500, step: 1 },
            rotation: { min: 0, max: 360, step: 1 }
        };

        // Normal (safe) ranges
        this.normalRanges = {
            curveFactor: { min: -3, max: 1, step: 0.01 },
            handleAngle: { min: 10, max: 170, step: 1 },
            size: { min: 20, max: 300, step: 1 },
            rotation: { min: 0, max: 360, step: 1 }
        };
    }

    /**
     * Set a constraint for a specific n value and parameter
     * @param {number} n - Number of sides
     * @param {string} param - Parameter name (e.g., 'curveFactor', 'handleAngle')
     * @param {number} value - The constraint value
     * @param {string} type - 'min' or 'max'
     */
    setConstraint(n, param, value, type) {
        if (!this.constraints[n]) {
            this.constraints[n] = {};
        }
        if (!this.constraints[n][param]) {
            this.constraints[n][param] = [null, null];
        }

        const index = type === 'min' ? 0 : 1;
        this.constraints[n][param][index] = value;

        this.saveToLocalStorage();
        this.notifyListeners('constraint-set', { n, param, value, type });
    }

    /**
     * Get constraints for a specific n value
     * @param {number} n - Number of sides
     * @returns {Object} Constraint object for the given n
     */
    getConstraints(n) {
        return this.constraints[n] || {};
    }

    /**
     * Get the effective range for a parameter (respects constraints and mode)
     * @param {number} n - Number of sides
     * @param {string} param - Parameter name
     * @returns {Object} Range object with min, max, step
     */
    getEffectiveRange(n, param) {
        const baseRange = this.feedbackMode
            ? this.defaultRanges[param]
            : this.normalRanges[param];

        if (!baseRange) return null;

        const constraints = this.getConstraints(n);
        const paramConstraints = constraints[param];

        if (!paramConstraints) {
            return { ...baseRange };
        }

        return {
            min: paramConstraints[0] !== null ? paramConstraints[0] : baseRange.min,
            max: paramConstraints[1] !== null ? paramConstraints[1] : baseRange.max,
            step: baseRange.step
        };
    }

    /**
     * Clear a specific constraint
     * @param {number} n - Number of sides
     * @param {string} param - Parameter name
     * @param {string} type - 'min', 'max', or 'both'
     */
    clearConstraint(n, param, type = 'both') {
        if (!this.constraints[n] || !this.constraints[n][param]) return;

        if (type === 'both') {
            delete this.constraints[n][param];
        } else {
            const index = type === 'min' ? 0 : 1;
            this.constraints[n][param][index] = null;
        }

        // Clean up empty objects
        if (Object.keys(this.constraints[n]).length === 0) {
            delete this.constraints[n];
        }

        this.saveToLocalStorage();
        this.notifyListeners('constraint-cleared', { n, param, type });
    }

    /**
     * Clear all constraints for a specific n value
     * @param {number} n - Number of sides
     */
    clearAllConstraints(n) {
        if (this.constraints[n]) {
            delete this.constraints[n];
            this.saveToLocalStorage();
            this.notifyListeners('constraints-cleared', { n });
        }
    }

    /**
     * Toggle feedback mode
     * @param {boolean} enabled - Enable/disable feedback mode
     */
    setFeedbackMode(enabled) {
        this.feedbackMode = enabled;
        this.notifyListeners('feedback-mode-changed', { enabled });
    }

    /**
     * Export constraints to JSON string
     * @returns {string} JSON representation of constraints
     */
    exportToJSON() {
        return JSON.stringify(this.constraints, null, 2);
    }

    /**
     * Export constraints to clipboard
     * @returns {Promise<boolean>} Success status
     */
    async exportToClipboard() {
        try {
            const json = this.exportToJSON();
            await navigator.clipboard.writeText(json);
            this.notifyListeners('export-success', { method: 'clipboard' });
            return true;
        } catch (err) {
            console.error('Failed to copy to clipboard:', err);
            this.notifyListeners('export-error', { error: err.message });
            return false;
        }
    }

    /**
     * Import constraints from JSON string
     * @param {string} json - JSON string containing constraints
     * @returns {boolean} Success status
     */
    importFromJSON(json) {
        try {
            const parsed = JSON.parse(json);

            // Validate structure
            if (typeof parsed !== 'object') {
                throw new Error('Invalid constraint format: must be an object');
            }

            // Validate each constraint
            for (const [n, params] of Object.entries(parsed)) {
                if (isNaN(parseInt(n))) {
                    throw new Error(`Invalid n value: ${n}`);
                }

                for (const [param, values] of Object.entries(params)) {
                    if (!Array.isArray(values) || values.length !== 2) {
                        throw new Error(`Invalid constraint for ${param}: must be [min, max] array`);
                    }
                }
            }

            this.constraints = parsed;
            this.saveToLocalStorage();
            this.notifyListeners('import-success', { source: 'json' });
            return true;
        } catch (err) {
            console.error('Failed to import constraints:', err);
            this.notifyListeners('import-error', { error: err.message });
            return false;
        }
    }

    /**
     * Import constraints from clipboard
     * @returns {Promise<boolean>} Success status
     */
    async importFromClipboard() {
        try {
            const text = await navigator.clipboard.readText();
            return this.importFromJSON(text);
        } catch (err) {
            console.error('Failed to read from clipboard:', err);
            this.notifyListeners('import-error', { error: err.message });
            return false;
        }
    }

    /**
     * Save constraints to localStorage
     */
    saveToLocalStorage() {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(this.constraints));
        } catch (err) {
            console.error('Failed to save to localStorage:', err);
        }
    }

    /**
     * Load constraints from localStorage
     * @returns {Object|null} Loaded constraints or null if not found
     */
    loadFromLocalStorage() {
        try {
            const stored = localStorage.getItem(this.storageKey);
            return stored ? JSON.parse(stored) : null;
        } catch (err) {
            console.error('Failed to load from localStorage:', err);
            return null;
        }
    }

    /**
     * Reset all constraints to defaults
     */
    resetToDefaults() {
        this.constraints = {};
        this.feedbackMode = false;
        this.saveToLocalStorage();
        this.notifyListeners('reset-complete', {});
    }

    /**
     * Register event listener
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
     * Get summary statistics
     * @returns {Object} Summary statistics
     */
    getSummary() {
        const nValues = Object.keys(this.constraints).map(n => parseInt(n));
        let totalConstraints = 0;

        for (const params of Object.values(this.constraints)) {
            totalConstraints += Object.keys(params).length;
        }

        return {
            totalNValues: nValues.length,
            nValues: nValues.sort((a, b) => a - b),
            totalConstraints,
            feedbackMode: this.feedbackMode,
            storageSize: JSON.stringify(this.constraints).length
        };
    }

    /**
     * Check if a value is within constraints
     * @param {number} n - Number of sides
     * @param {string} param - Parameter name
     * @param {number} value - Value to check
     * @returns {Object} { valid: boolean, min: number, max: number }
     */
    validateValue(n, param, value) {
        const range = this.getEffectiveRange(n, param);
        if (!range) {
            return { valid: true, min: null, max: null };
        }

        const valid = value >= range.min && value <= range.max;
        return { valid, min: range.min, max: range.max };
    }
}

// Export for use in modules or standalone
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ConstraintManager;
}
