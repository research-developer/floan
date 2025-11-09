/**
 * Constraint Management Functions for FlowAngle Studio
 * To be inserted after the parameter mapping and before URL sharing functions
 */

// ===== CONSTRAINT MANAGEMENT FUNCTIONS =====

/**
 * Initialize Constraint Manager
 */
function initConstraintManager() {
    constraintManager = new ConstraintManager('flowangle_constraints');

    // Add event listeners
    constraintManager.addListener((event, data) => {
        console.log('Constraint event:', event, data);

        if (event === 'constraint-set' || event === 'constraint-cleared' ||
            event === 'constraints-cleared' || event === 'import-success') {
            updateRangeIndicators();
            refreshConstraintTable();
        }

        if (event === 'export-success') {
            showNotification('Constraints copied to clipboard!', 'success');
        }

        if (event === 'import-success') {
            showNotification('Constraints imported successfully!', 'success');
        }

        if (event === 'import-error' || event === 'export-error') {
            showNotification('Error: ' + data.error, 'error');
        }
    });

    updateRangeIndicators();
}

/**
 * Toggle Feedback Mode
 */
function toggleFeedbackMode() {
    feedbackMode = document.getElementById('feedback-mode').checked;
    constraintManager.setFeedbackMode(feedbackMode);

    const container = document.getElementById('feedback-mode-container');
    container.classList.toggle('active', feedbackMode);

    // Show/hide constraint capture buttons
    const constraintButtons = document.querySelectorAll('.constraint-buttons');
    constraintButtons.forEach(btn => {
        btn.style.display = feedbackMode ? 'flex' : 'none';
    });

    // Update slider ranges with animation
    updateSliderRanges(true);
    updateRangeIndicators();

    showNotification(
        feedbackMode ? 'Feedback Mode Enabled - Explore freely!' : 'Feedback Mode Disabled',
        feedbackMode ? 'success' : 'info'
    );
}

/**
 * Update slider ranges based on current mode and constraints
 */
function updateSliderRanges(animate = false) {
    const n = parseInt(document.getElementById('sides').value);

    // Update each parameter
    Object.entries(paramMap).forEach(([param, config]) => {
        const slider = document.getElementById(config.id);
        const range = constraintManager.getEffectiveRange(n, param);

        if (range) {
            const oldMin = parseFloat(slider.min);
            const oldMax = parseFloat(slider.max);
            const currentValue = parseFloat(slider.value);

            // Update range
            slider.min = range.min;
            slider.max = range.max;
            slider.step = range.step;

            // Clamp current value if needed
            if (currentValue < range.min) {
                slider.value = range.min;
            } else if (currentValue > range.max) {
                slider.value = range.max;
            }

            // Visual feedback for range change
            if (animate && (oldMin !== range.min || oldMax !== range.max)) {
                slider.style.transition = 'opacity 0.3s';
                slider.style.opacity = '0.5';
                setTimeout(() => {
                    slider.style.opacity = '1';
                    slider.style.transition = '';
                }, 300);
            }
        }
    });

    updatePreview();
}

/**
 * Update range indicators below sliders
 */
function updateRangeIndicators() {
    const n = parseInt(document.getElementById('sides').value);

    Object.entries(paramMap).forEach(([param, config]) => {
        const range = constraintManager.getEffectiveRange(n, param);
        const indicator = document.getElementById(param === 'curveFactor' ? 'curve-range-indicator' :
                                                 param === 'handleAngle' ? 'angle-range-indicator' :
                                                 'rotation-range-indicator');

        if (range && indicator) {
            const minStr = config.decimals > 0 ? range.min.toFixed(config.decimals) : range.min;
            const maxStr = config.decimals > 0 ? range.max.toFixed(config.decimals) : range.max;
            indicator.textContent = `[${minStr}${config.unit} to ${maxStr}${config.unit}]`;
            indicator.classList.toggle('feedback-active', feedbackMode);
        }
    });
}

/**
 * Capture constraint for current parameter and n value
 */
function captureConstraint(param, type) {
    const n = parseInt(document.getElementById('sides').value);
    const config = paramMap[param];
    const slider = document.getElementById(config.id);
    const value = parseFloat(slider.value);

    constraintManager.setConstraint(n, param, value, type);

    showNotification(
        `${type === 'min' ? 'Minimum' : 'Maximum'} set for ${config.display} at n=${n}: ${value.toFixed(config.decimals)}${config.unit}`,
        'success'
    );

    // Visual feedback on button
    const buttonContainerId = param === 'curveFactor' ? 'curve-constraints' :
                              param === 'handleAngle' ? 'angle-constraints' :
                              'rotation-constraints';
    const buttons = document.querySelectorAll(`#${buttonContainerId} .constraint-btn`);
    const btnIndex = type === 'min' ? 0 : 1;
    if (buttons[btnIndex]) {
        buttons[btnIndex].classList.add('active');
        setTimeout(() => buttons[btnIndex].classList.remove('active'), 1000);
    }
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = 'notification show ' + type;

    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

/**
 * Open Constraint Manager
 */
function openConstraintManager() {
    document.getElementById('constraint-manager').classList.add('visible');
    document.getElementById('overlay').classList.add('visible');
    refreshConstraintTable();
}

/**
 * Close Constraint Manager
 */
function closeConstraintManager() {
    document.getElementById('constraint-manager').classList.remove('visible');
    document.getElementById('overlay').classList.remove('visible');
    document.getElementById('import-dialog').style.display = 'none';
}

/**
 * Refresh constraint table
 */
function refreshConstraintTable() {
    const container = document.getElementById('constraints-table-container');
    const summary = constraintManager.getSummary();

    // Update statistics
    document.getElementById('stat-n-values').textContent = summary.totalNValues;
    document.getElementById('stat-constraints').textContent = summary.totalConstraints;
    document.getElementById('stat-mode').textContent = feedbackMode ? 'Feedback' : 'Normal';

    // Build table
    if (summary.totalConstraints === 0) {
        container.innerHTML = '<div class="empty-state">No constraints defined yet.<br>Enable Feedback Mode and use "Set Min/Max" buttons to create constraints.</div>';
        return;
    }

    let tableHTML = '<table class="constraint-table"><thead><tr><th>N</th><th>Parameter</th><th>Min</th><th>Max</th><th>Actions</th></tr></thead><tbody>';

    summary.nValues.forEach(n => {
        const constraints = constraintManager.getConstraints(n);

        Object.entries(constraints).forEach(([param, values]) => {
            const config = paramMap[param];
            const minVal = values[0] !== null ? values[0].toFixed(config.decimals) + config.unit : '-';
            const maxVal = values[1] !== null ? values[1].toFixed(config.decimals) + config.unit : '-';

            tableHTML += `
                <tr>
                    <td><strong>n=${n}</strong></td>
                    <td>${config.display}</td>
                    <td class="constraint-value">${minVal}</td>
                    <td class="constraint-value">${maxVal}</td>
                    <td>
                        <button class="action-btn" onclick="clearConstraint(${n}, '${param}', 'min')">Clear Min</button>
                        <button class="action-btn" onclick="clearConstraint(${n}, '${param}', 'max')">Clear Max</button>
                        <button class="action-btn delete" onclick="clearConstraint(${n}, '${param}', 'both')">Delete</button>
                    </td>
                </tr>
            `;
        });
    });

    tableHTML += '</tbody></table>';
    container.innerHTML = tableHTML;
}

/**
 * Clear specific constraint
 */
function clearConstraint(n, param, type) {
    constraintManager.clearConstraint(n, param, type);
    const typeStr = type === 'both' ? 'constraint' : type + ' value';
    showNotification(`Cleared ${typeStr} for ${paramMap[param].display} at n=${n}`, 'success');
}

/**
 * Clear all constraints
 */
function clearAllConstraints() {
    if (confirm('Are you sure you want to clear all constraints?')) {
        Object.keys(constraintManager.constraints).forEach(n => {
            constraintManager.clearAllConstraints(parseInt(n));
        });
        showNotification('All constraints cleared', 'success');
    }
}

/**
 * Reset to defaults
 */
function resetConstraints() {
    if (confirm('This will reset all constraints and disable feedback mode. Continue?')) {
        constraintManager.resetToDefaults();
        feedbackMode = false;
        document.getElementById('feedback-mode').checked = false;
        toggleFeedbackMode();
        showNotification('Reset to defaults', 'success');
    }
}

/**
 * Export constraints
 */
async function exportConstraints() {
    await constraintManager.exportToClipboard();
}

/**
 * Import from clipboard
 */
async function importFromClipboard() {
    const success = await constraintManager.importFromClipboard();
    if (success) {
        updateSliderRanges(true);
    }
}

/**
 * Toggle import dialog
 */
function toggleImportDialog() {
    const dialog = document.getElementById('import-dialog');
    dialog.style.display = dialog.style.display === 'none' ? 'block' : 'none';
}

/**
 * Import from textarea
 */
function importFromTextarea() {
    const textarea = document.getElementById('import-textarea');
    const success = constraintManager.importFromJSON(textarea.value);
    if (success) {
        updateSliderRanges(true);
        textarea.value = '';
        toggleImportDialog();
    }
}

// ===== END CONSTRAINT MANAGEMENT =====
