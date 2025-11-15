/**
 * Coordinate Transformation Layer
 * Handles conversion between SVG coordinate system and Illustrator coordinate system
 *
 * SVG Coordinates:
 * - Origin: Top-left corner
 * - Y-axis: Grows downward
 * - Units: Pixels
 *
 * Illustrator Coordinates:
 * - Origin: Bottom-left corner of artboard
 * - Y-axis: Grows upward
 * - Units: Points (1 point = 1/72 inch)
 */

/**
 * Transform a single point from algorithm coordinates to Illustrator coordinates
 *
 * IMPORTANT: The FloAng algorithm generates points in mathematical coordinate space
 * with the center as origin. Since the algorithm receives Illustrator's centerX/centerY
 * directly, the generated coordinates are already in Illustrator's coordinate system.
 *
 * Coordinate System Analysis:
 * - Algorithm Input: Illustrator center coordinates (centerX, centerY) from artboard
 * - Algorithm Output: Points relative to that center in mathematical orientation
 * - Illustrator System: Bottom-left origin, Y increases upward (mathematical standard)
 * - Result: Direct 1:1 mapping, NO Y-axis inversion needed
 *
 * Previous Bug: The code incorrectly assumed algorithm output was in SVG screen space
 * (top-left origin, Y increases downward), causing vertical flip of all patterns.
 *
 * @param {Object} svgPoint - Point in algorithm/mathematical coordinates {x, y}
 * @param {number} artboardHeight - Height of the artboard (unused, kept for API compatibility)
 * @returns {Array} Illustrator coordinate pair [x, y]
 */
export function svgToIllustrator(svgPoint, artboardHeight) {
    // Direct mapping: algorithm coordinates are already in Illustrator space
    // No Y-axis transformation needed since both use mathematical orientation
    return [
        svgPoint.x,
        svgPoint.y  // Fixed: removed incorrect inversion (artboardHeight - svgPoint.y)
    ];
}

/**
 * Transform a single point from Illustrator to algorithm/mathematical coordinates
 *
 * Since the coordinate systems are now understood to be identical (both mathematical
 * orientation with Y increasing upward), this is also a direct 1:1 mapping.
 *
 * @param {Array} ilPoint - Illustrator coordinate pair [x, y]
 * @param {number} artboardHeight - Height of the artboard (unused, kept for API compatibility)
 * @returns {Object} Algorithm/mathematical coordinate {x, y}
 */
export function illustratorToSVG(ilPoint, artboardHeight) {
    // Direct mapping: Illustrator coordinates are already in mathematical orientation
    return {
        x: ilPoint[0],
        y: ilPoint[1]  // Fixed: removed incorrect inversion (artboardHeight - ilPoint[1])
    };
}

/**
 * Get artboard dimensions and center point
 * @param {Document} doc - Illustrator document
 * @returns {Object} { width, height, centerX, centerY, bounds }
 */
export function getArtboardInfo(doc) {
    if (!doc || doc.artboards.length === 0) {
        throw new Error('No artboards in document');
    }

    // Get active artboard
    const artboard = doc.artboards[doc.artboards.getActiveArtboardIndex()];
    const bounds = artboard.artboardRect; // [left, top, right, bottom]

    const left = bounds[0];
    const top = bounds[1];
    const right = bounds[2];
    const bottom = bounds[3];

    const width = right - left;
    const height = top - bottom; // Note: top > bottom in Illustrator

    return {
        width: width,
        height: height,
        centerX: left + (width / 2),
        centerY: bottom + (height / 2),
        bounds: {
            left: left,
            top: top,
            right: right,
            bottom: bottom
        }
    };
}

/**
 * Calculate appropriate radius for pattern based on artboard size
 * @param {Object} artboardInfo - Result from getArtboardInfo()
 * @param {number} scaleFactor - Scale factor (0-1, default 0.25)
 * @returns {number} Radius in points
 */
export function calculatePatternRadius(artboardInfo, scaleFactor = 0.25) {
    const minDimension = Math.min(artboardInfo.width, artboardInfo.height);
    return minDimension * scaleFactor;
}

/**
 * Convert pattern data from SVG space to Illustrator space
 * @param {Object} patternData - Output from generateFlowAngleData()
 * @param {Object} artboardInfo - Result from getArtboardInfo()
 * @returns {Object} Transformed pattern data
 */
export function transformPatternData(patternData, artboardInfo) {
    const { height: artboardHeight } = artboardInfo;

    // Handle circle case
    if (patternData.type === 'circle') {
        return {
            type: 'circle',
            center: svgToIllustrator(patternData.center, artboardHeight),
            radius: patternData.radius
        };
    }

    // Handle quadratic (n=2) case
    if (patternData.type === 'quadratic') {
        return {
            type: 'quadratic',
            start: svgToIllustrator(patternData.start, artboardHeight),
            end: svgToIllustrator(patternData.end, artboardHeight),
            controlPoint: svgToIllustrator(patternData.controlPoint, artboardHeight)
        };
    }

    // Handle bezier (n>=3) case
    if (patternData.type === 'bezier') {
        return {
            type: 'bezier',
            vertices: patternData.vertices.map(v => svgToIllustrator(v, artboardHeight)),
            segments: patternData.segments.map(seg => ({
                start: svgToIllustrator(seg.start, artboardHeight),
                end: svgToIllustrator(seg.end, artboardHeight),
                controlPoint1: svgToIllustrator(seg.controlPoint1, artboardHeight),
                controlPoint2: svgToIllustrator(seg.controlPoint2, artboardHeight)
            })),
            center: svgToIllustrator(patternData.center, artboardHeight),
            radius: patternData.radius
        };
    }

    throw new Error(`Unknown pattern type: ${patternData.type}`);
}
