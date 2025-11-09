/**
 * Constraint Manager UI Component
 * Provides comprehensive UI for managing, visualizing, and switching between constraint modes
 *
 * @version 1.0.0
 * @author svGen Team 3 - Agent 4
 */

class ConstraintManagerUI {
    constructor(constraintManager) {
        this.manager = constraintManager;
        this.activeTab = 'current';
        this.currentMode = 'recommended';
        this.autoClampingEnabled = true;
        this.showRangeIndicators = true;
        this.strictness = 100;

        // Constraint mode definitions
        this.modes = {
            recommended: {
                name: 'Recommended',
                description: 'Tight, safe ranges proven to produce valid shapes',
                ranges: {
                    curveFactor: { 1: [-3, 1], 2: [-3, 1], 3: [-3, 1], 4: [-3, 1], 5: [-3, 1], 6: [-3, 1], 7: [-3, 1], 8: [-3, 1], 9: [-3, 1], 10: [-3, 1], 11: [-3, 1], 12: [-3, 1] },
                    handleAngle: { 1: [10, 170], 2: [10, 170], 3: [30, 90], 4: [20, 70], 5: [15, 55], 6: [12, 45], 7: [10, 40], 8: [10, 35], 9: [8, 30], 10: [8, 28], 11: [7, 25], 12: [7, 23] },
                    rotation: { 1: [0, 360], 2: [0, 360], 3: [0, 360], 4: [0, 360], 5: [0, 360], 6: [0, 360], 7: [0, 360], 8: [0, 360], 9: [0, 360], 10: [0, 360], 11: [0, 360], 12: [0, 360] }
                }
            },
            extended: {
                name: 'Extended',
                description: 'Wider valid ranges for more exploration',
                ranges: {
                    curveFactor: { 1: [-5, 3], 2: [-5, 3], 3: [-5, 3], 4: [-5, 3], 5: [-5, 3], 6: [-5, 3], 7: [-5, 3], 8: [-5, 3], 9: [-5, 3], 10: [-5, 3], 11: [-5, 3], 12: [-5, 3] },
                    handleAngle: { 1: [5, 175], 2: [5, 175], 3: [15, 120], 4: [10, 90], 5: [8, 70], 6: [7, 60], 7: [6, 50], 8: [5, 45], 9: [5, 40], 10: [4, 35], 11: [4, 32], 12: [3, 30] },
                    rotation: { 1: [0, 360], 2: [0, 360], 3: [0, 360], 4: [0, 360], 5: [0, 360], 6: [0, 360], 7: [0, 360], 8: [0, 360], 9: [0, 360], 10: [0, 360], 11: [0, 360], 12: [0, 360] }
                }
            },
            unlimited: {
                name: 'Unlimited',
                description: 'Full parameter exploration without limits',
                ranges: {
                    curveFactor: { 1: [-10, 10], 2: [-10, 10], 3: [-10, 10], 4: [-10, 10], 5: [-10, 10], 6: [-10, 10], 7: [-10, 10], 8: [-10, 10], 9: [-10, 10], 10: [-10, 10], 11: [-10, 10], 12: [-10, 10] },
                    handleAngle: { 1: [1, 179], 2: [1, 179], 3: [1, 179], 4: [1, 179], 5: [1, 179], 6: [1, 179], 7: [1, 179], 8: [1, 179], 9: [1, 179], 10: [1, 179], 11: [1, 179], 12: [1, 179] },
                    rotation: { 1: [0, 360], 2: [0, 360], 3: [0, 360], 4: [0, 360], 5: [0, 360], 6: [0, 360], 7: [0, 360], 8: [0, 360], 9: [0, 360], 10: [0, 360], 11: [0, 360], 12: [0, 360] }
                }
            },
            custom: {
                name: 'Custom',
                description: 'User-defined constraints',
                ranges: {} // Loaded from constraint manager
            }
        };

        this.init();
    }

    init() {
        this.createUI();
        this.attachEventListeners();
        this.loadSettings();
        this.applyMode(this.currentMode);
    }

    createUI() {
        // Create main panel
        const panel = document.createElement('div');
        panel.id = 'constraints-panel';
        panel.className = 'collapsed';
        panel.innerHTML = `
            <div id="constraints-header">
                <h2>Parameter Constraints</h2>
                <button id="constraints-collapse-btn" class="constraint-reset-btn">Hide</button>
            </div>

            <div class="constraint-tabs">
                <button class="constraint-tab active" data-tab="current">Current</button>
                <button class="constraint-tab" data-tab="all">All Constraints</button>
                <button class="constraint-tab" data-tab="settings">Settings</button>
            </div>

            <div class="constraint-tab-content active" id="tab-current">
                <div id="current-constraints-container"></div>
            </div>

            <div class="constraint-tab-content" id="tab-all">
                <div class="table-actions">
                    <button class="table-action-btn" onclick="constraintManagerUI.resetAllConstraints()">Reset All</button>
                    <button class="table-action-btn" onclick="constraintManagerUI.exportConstraints()">Export</button>
                    <button class="table-action-btn" onclick="constraintManagerUI.importConstraints()">Import</button>
                </div>
                <div class="constraints-table-wrapper">
                    <table class="constraints-table" id="constraints-table"></table>
                </div>
            </div>

            <div class="constraint-tab-content" id="tab-settings">
                <div class="settings-section">
                    <h3>Constraint Mode</h3>
                    <div class="settings-mode-selector" id="mode-selector"></div>
                </div>

                <div class="settings-section">
                    <h3>Preferences</h3>
                    <div class="settings-checkbox-group">
                        <label class="settings-checkbox-option">
                            <input type="checkbox" id="auto-clamping" checked>
                            <span class="settings-checkbox-label">Enable Auto-Clamping</span>
                        </label>
                        <label class="settings-checkbox-option">
                            <input type="checkbox" id="show-range-indicators" checked>
                            <span class="settings-checkbox-label">Show Range Indicators</span>
                        </label>
                    </div>

                    <div class="settings-slider-group">
                        <div class="settings-slider-label">
                            <span>Constraint Strictness</span>
                            <span class="settings-slider-value" id="strictness-value">100%</span>
                        </div>
                        <input type="range" id="strictness-slider" min="0" max="100" value="100" step="1">
                    </div>
                </div>

                <div class="settings-section">
                    <h3>Preset Profiles</h3>
                    <div class="preset-profiles">
                        <button class="preset-profile-btn" data-profile="conservative">Conservative</button>
                        <button class="preset-profile-btn" data-profile="artistic">Artistic</button>
                        <button class="preset-profile-btn" data-profile="experimental">Experimental</button>
                        <button class="preset-profile-btn" data-profile="precise">Precise</button>
                    </div>
                </div>

                <div id="constraint-status" class="constraint-status"></div>
            </div>
        `;

        // Insert into main content area
        const mainContent = document.getElementById('main-content');
        if (mainContent) {
            mainContent.appendChild(panel);
        }

        // Create toggle button
        const toggleBtn = document.createElement('button');
        toggleBtn.id = 'constraints-toggle-btn';
        toggleBtn.textContent = '◀';
        toggleBtn.onclick = () => this.togglePanel();
        document.getElementById('canvas-area').appendChild(toggleBtn);

        // Create mode selector
        this.renderModeSelector();
    }

    renderModeSelector() {
        const container = document.getElementById('mode-selector');
        if (!container) return;

        container.innerHTML = '';

        Object.keys(this.modes).forEach(mode => {
            const modeData = this.modes[mode];
            const option = document.createElement('div');
            option.className = 'settings-mode-option' + (this.currentMode === mode ? ' active' : '');
            option.innerHTML = `
                <input type="radio" name="constraint-mode" value="${mode}" ${this.currentMode === mode ? 'checked' : ''} class="settings-mode-radio">
                <div class="settings-mode-label">
                    <div class="settings-mode-title">${modeData.name}</div>
                    <div class="settings-mode-description">${modeData.description}</div>
                </div>
            `;
            option.onclick = () => this.setMode(mode);
            container.appendChild(option);
        });
    }

    attachEventListeners() {
        // Tab switching
        document.querySelectorAll('.constraint-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.switchTab(e.target.dataset.tab);
            });
        });

        // Collapse button
        const collapseBtn = document.getElementById('constraints-collapse-btn');
        if (collapseBtn) {
            collapseBtn.addEventListener('click', () => this.togglePanel());
        }

        // Preferences
        const autoClamp = document.getElementById('auto-clamping');
        if (autoClamp) {
            autoClamp.addEventListener('change', (e) => {
                this.autoClampingEnabled = e.target.checked;
                this.saveSettings();
            });
        }

        const showRanges = document.getElementById('show-range-indicators');
        if (showRanges) {
            showRanges.addEventListener('change', (e) => {
                this.showRangeIndicators = e.target.checked;
                this.saveSettings();
                this.updateRangeIndicators();
            });
        }

        const strictness = document.getElementById('strictness-slider');
        if (strictness) {
            strictness.addEventListener('input', (e) => {
                this.strictness = parseInt(e.target.value);
                document.getElementById('strictness-value').textContent = this.strictness + '%';
                this.saveSettings();
            });
        }

        // Preset profiles
        document.querySelectorAll('.preset-profile-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.loadPresetProfile(e.target.dataset.profile);
            });
        });
    }

    switchTab(tabName) {
        this.activeTab = tabName;

        // Update tab buttons
        document.querySelectorAll('.constraint-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.tab === tabName);
        });

        // Update tab content
        document.querySelectorAll('.constraint-tab-content').forEach(content => {
            content.classList.toggle('active', content.id === `tab-${tabName}`);
        });

        // Render content based on active tab
        if (tabName === 'current') {
            this.renderCurrentConstraints();
        } else if (tabName === 'all') {
            this.renderAllConstraintsTable();
        }
    }

    renderCurrentConstraints() {
        const container = document.getElementById('current-constraints-container');
        if (!container) return;

        const n = this.getCurrentN();
        const params = ['curveFactor', 'handleAngle', 'rotation'];
        const paramNames = {
            curveFactor: 'Curve Factor',
            handleAngle: 'Handle Angle',
            rotation: 'Rotation'
        };

        container.innerHTML = '';

        params.forEach(param => {
            const range = this.getEffectiveRangeForParam(n, param);
            const currentValue = this.getCurrentValue(param);

            const item = document.createElement('div');
            item.className = 'constraint-item';
            item.innerHTML = `
                <div class="constraint-item-header">
                    <span class="constraint-item-title">${paramNames[param]}</span>
                    <button class="constraint-reset-btn" onclick="constraintManagerUI.resetConstraint(${n}, '${param}')">Reset</button>
                </div>

                <div class="constraint-range-display">
                    <div class="constraint-range-bar">
                        <div class="constraint-range-fill" style="left: 0%; width: 100%;"></div>
                        <div class="constraint-range-current" style="left: ${this.calculatePercentage(currentValue, range.min, range.max)}%;"></div>
                    </div>
                    <div class="constraint-range-labels">
                        <span>Min: ${range.min}</span>
                        <span>Max: ${range.max}</span>
                    </div>
                    <div class="constraint-range-current-value">${this.formatValue(currentValue, param)}</div>
                </div>

                <div class="constraint-quick-edit">
                    <input type="number" placeholder="Min" value="${range.min}" step="${range.step}"
                        onchange="constraintManagerUI.updateConstraint(${n}, '${param}', parseFloat(this.value), 'min')">
                    <input type="number" placeholder="Max" value="${range.max}" step="${range.step}"
                        onchange="constraintManagerUI.updateConstraint(${n}, '${param}', parseFloat(this.value), 'max')">
                </div>
            `;

            container.appendChild(item);
        });
    }

    renderAllConstraintsTable() {
        const table = document.getElementById('constraints-table');
        if (!table) return;

        let html = `
            <thead>
                <tr>
                    <th>n</th>
                    <th colspan="2">Curve Factor</th>
                    <th colspan="2">Handle Angle</th>
                    <th colspan="2">Rotation</th>
                </tr>
                <tr>
                    <th></th>
                    <th>Min</th>
                    <th>Max</th>
                    <th>Min</th>
                    <th>Max</th>
                    <th>Min</th>
                    <th>Max</th>
                </tr>
            </thead>
            <tbody>
        `;

        for (let n = 1; n <= 12; n++) {
            html += `<tr>`;
            html += `<td style="font-weight: bold; background: #2a2a2a;">${n}</td>`;

            ['curveFactor', 'handleAngle', 'rotation'].forEach(param => {
                const range = this.getEffectiveRangeForParam(n, param);
                const isModified = this.isConstraintModified(n, param);
                const cellClass = isModified ? 'modified editable' : 'default editable';

                html += `
                    <td class="${cellClass}" onclick="constraintManagerUI.editCell(this, ${n}, '${param}', 'min')">
                        ${range.min}
                    </td>
                    <td class="${cellClass}" onclick="constraintManagerUI.editCell(this, ${n}, '${param}', 'max')">
                        ${range.max}
                    </td>
                `;
            });

            html += `</tr>`;
        }

        html += `</tbody>`;
        table.innerHTML = html;
    }

    editCell(cell, n, param, type) {
        if (cell.querySelector('input')) return; // Already editing

        const currentValue = cell.textContent.trim();
        const input = document.createElement('input');
        input.type = 'number';
        input.value = currentValue;
        input.step = param === 'curveFactor' ? '0.01' : '1';

        input.onblur = () => {
            const newValue = parseFloat(input.value);
            if (!isNaN(newValue)) {
                this.updateConstraint(n, param, newValue, type);
                cell.textContent = newValue;
                cell.classList.add('modified');
            } else {
                cell.textContent = currentValue;
            }
        };

        input.onkeydown = (e) => {
            if (e.key === 'Enter') {
                input.blur();
            } else if (e.key === 'Escape') {
                cell.textContent = currentValue;
            }
        };

        cell.textContent = '';
        cell.appendChild(input);
        input.focus();
        input.select();
    }

    setMode(mode) {
        this.currentMode = mode;
        this.applyMode(mode);
        this.renderModeSelector();
        this.saveSettings();
        this.showStatus('Constraint mode changed to: ' + this.modes[mode].name, 'success');
    }

    applyMode(mode) {
        if (mode === 'custom') return; // Custom mode doesn't override constraints

        const modeData = this.modes[mode];
        const ranges = modeData.ranges;

        // Apply mode ranges to constraint manager
        for (let n = 1; n <= 12; n++) {
            Object.keys(ranges).forEach(param => {
                if (ranges[param][n]) {
                    const [min, max] = ranges[param][n];
                    this.manager.setConstraint(n, param, min, 'min');
                    this.manager.setConstraint(n, param, max, 'max');
                }
            });
        }

        // Update sliders if current n is visible
        this.updateSliderLimits();
        this.renderCurrentConstraints();
        this.renderAllConstraintsTable();
    }

    updateSliderLimits() {
        const n = this.getCurrentN();

        const curveRange = this.getEffectiveRangeForParam(n, 'curveFactor');
        const angleRange = this.getEffectiveRangeForParam(n, 'handleAngle');
        const rotationRange = this.getEffectiveRangeForParam(n, 'rotation');

        const curveSlider = document.getElementById('curve-factor');
        const angleSlider = document.getElementById('handle-angle');
        const rotationSlider = document.getElementById('rotation');

        if (curveSlider) {
            curveSlider.min = curveRange.min;
            curveSlider.max = curveRange.max;
            curveSlider.step = curveRange.step;
            // Clamp current value if auto-clamping is enabled
            if (this.autoClampingEnabled) {
                const currentValue = parseFloat(curveSlider.value);
                if (currentValue < curveRange.min) curveSlider.value = curveRange.min;
                if (currentValue > curveRange.max) curveSlider.value = curveRange.max;
            }
        }

        if (angleSlider) {
            angleSlider.min = angleRange.min;
            angleSlider.max = angleRange.max;
            angleSlider.step = angleRange.step;
            if (this.autoClampingEnabled) {
                const currentValue = parseFloat(angleSlider.value);
                if (currentValue < angleRange.min) angleSlider.value = angleRange.min;
                if (currentValue > angleRange.max) angleSlider.value = angleRange.max;
            }
        }

        if (rotationSlider) {
            rotationSlider.min = rotationRange.min;
            rotationSlider.max = rotationRange.max;
            rotationSlider.step = rotationRange.step;
        }

        // Trigger preview update if a function exists
        if (typeof updatePreview === 'function') {
            updatePreview();
        }
    }

    updateConstraint(n, param, value, type) {
        this.manager.setConstraint(n, param, value, type);
        this.currentMode = 'custom'; // Switch to custom mode when user edits
        this.renderModeSelector();
        this.updateSliderLimits();
        this.renderCurrentConstraints();
        this.saveSettings();
    }

    resetConstraint(n, param) {
        this.manager.clearConstraint(n, param);
        this.applyMode(this.currentMode === 'custom' ? 'recommended' : this.currentMode);
        this.showStatus(`Reset constraints for ${param} at n=${n}`, 'success');
    }

    resetAllConstraints() {
        if (confirm('Reset all constraints to default values?')) {
            this.manager.resetToDefaults();
            this.currentMode = 'recommended';
            this.applyMode('recommended');
            this.showStatus('All constraints reset to recommended defaults', 'success');
        }
    }

    exportConstraints() {
        const json = this.manager.exportToJSON();

        // Create download link
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `flowangle-constraints-${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);

        this.showStatus('Constraints exported successfully', 'success');
    }

    importConstraints() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'application/json';

        input.onchange = (e) => {
            const file = e.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = (event) => {
                try {
                    const success = this.manager.importFromJSON(event.target.result);
                    if (success) {
                        this.currentMode = 'custom';
                        this.renderModeSelector();
                        this.updateSliderLimits();
                        this.renderAllConstraintsTable();
                        this.showStatus('Constraints imported successfully', 'success');
                    } else {
                        this.showStatus('Failed to import constraints', 'error');
                    }
                } catch (err) {
                    this.showStatus('Invalid constraint file: ' + err.message, 'error');
                }
            };
            reader.readAsText(file);
        };

        input.click();
    }

    loadPresetProfile(profile) {
        const profiles = {
            conservative: 'recommended',
            artistic: 'extended',
            experimental: 'unlimited',
            precise: 'recommended'
        };

        const mode = profiles[profile] || 'recommended';
        this.setMode(mode);

        // Update active button
        document.querySelectorAll('.preset-profile-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.profile === profile);
        });
    }

    togglePanel() {
        const panel = document.getElementById('constraints-panel');
        const btn = document.getElementById('constraints-toggle-btn');

        if (panel.classList.contains('collapsed')) {
            panel.classList.remove('collapsed');
            btn.textContent = '▶';
            btn.style.right = '400px';
        } else {
            panel.classList.add('collapsed');
            btn.textContent = '◀';
            btn.style.right = '0';
        }
    }

    showStatus(message, type = 'info') {
        const status = document.getElementById('constraint-status');
        if (!status) return;

        status.textContent = message;
        status.className = 'constraint-status ' + type;

        setTimeout(() => {
            status.className = 'constraint-status';
        }, 3000);
    }

    // Helper methods
    getCurrentN() {
        const sidesSlider = document.getElementById('sides');
        return sidesSlider ? parseInt(sidesSlider.value) : 3;
    }

    getCurrentValue(param) {
        const paramMap = {
            curveFactor: 'curve-factor',
            handleAngle: 'handle-angle',
            rotation: 'rotation'
        };

        const slider = document.getElementById(paramMap[param]);
        return slider ? parseFloat(slider.value) : 0;
    }

    getEffectiveRangeForParam(n, param) {
        // Get from constraint manager
        const constraints = this.manager.getConstraints(n);
        const paramConstraints = constraints[param];

        // Default ranges
        const defaults = {
            curveFactor: { min: -3, max: 1, step: 0.01 },
            handleAngle: { min: 10, max: 170, step: 1 },
            rotation: { min: 0, max: 360, step: 1 }
        };

        const baseRange = defaults[param] || { min: 0, max: 100, step: 1 };

        if (!paramConstraints || (paramConstraints[0] === null && paramConstraints[1] === null)) {
            return { ...baseRange };
        }

        return {
            min: paramConstraints[0] !== null ? paramConstraints[0] : baseRange.min,
            max: paramConstraints[1] !== null ? paramConstraints[1] : baseRange.max,
            step: baseRange.step
        };
    }

    isConstraintModified(n, param) {
        const constraints = this.manager.getConstraints(n);
        return constraints[param] !== undefined;
    }

    calculatePercentage(value, min, max) {
        if (max === min) return 50;
        return ((value - min) / (max - min)) * 100;
    }

    formatValue(value, param) {
        if (param === 'handleAngle' || param === 'rotation') {
            return value.toFixed(0) + '°';
        }
        return value.toFixed(2);
    }

    updateRangeIndicators() {
        // Update range indicators on sliders if needed
        // This can be expanded to show visual indicators on the main sliders
    }

    saveSettings() {
        const settings = {
            mode: this.currentMode,
            autoClampingEnabled: this.autoClampingEnabled,
            showRangeIndicators: this.showRangeIndicators,
            strictness: this.strictness
        };

        localStorage.setItem('svgen_constraint_ui_settings', JSON.stringify(settings));
    }

    loadSettings() {
        try {
            const stored = localStorage.getItem('svgen_constraint_ui_settings');
            if (stored) {
                const settings = JSON.parse(stored);
                this.currentMode = settings.mode || 'recommended';
                this.autoClampingEnabled = settings.autoClampingEnabled !== undefined ? settings.autoClampingEnabled : true;
                this.showRangeIndicators = settings.showRangeIndicators !== undefined ? settings.showRangeIndicators : true;
                this.strictness = settings.strictness || 100;

                // Update UI elements
                const autoClamp = document.getElementById('auto-clamping');
                if (autoClamp) autoClamp.checked = this.autoClampingEnabled;

                const showRanges = document.getElementById('show-range-indicators');
                if (showRanges) showRanges.checked = this.showRangeIndicators;

                const strictnessSlider = document.getElementById('strictness-slider');
                if (strictnessSlider) strictnessSlider.value = this.strictness;

                const strictnessValue = document.getElementById('strictness-value');
                if (strictnessValue) strictnessValue.textContent = this.strictness + '%';
            }
        } catch (err) {
            console.error('Failed to load UI settings:', err);
        }
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ConstraintManagerUI;
}
