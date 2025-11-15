/**
 * Illustrator Adapter
 * Creates native Illustrator PathItems from transformed pattern data
 * Handles Bézier curve construction and path properties
 */

import { getArtboardInfo, calculatePatternRadius, transformPatternData } from './coordinate-transform.js';

/**
 * Create a PathItem from Bézier pattern data
 * @param {Document} doc - Illustrator document
 * @param {Object} transformedData - Pattern data in Illustrator coordinates
 * @returns {PathItem} Created path item
 */
function createBezierPath(doc, transformedData) {
    const layer = doc.activeLayer;
    const pathItem = layer.pathItems.add();

    // Build path points array for Illustrator
    // Illustrator expects: [[x, y], [x, y], ...]
    const anchorPoints = transformedData.vertices;

    // Set entire path at once
    pathItem.setEntirePath(anchorPoints);

    // Set Bézier control handles for each point
    for (let i = 0; i < transformedData.segments.length; i++) {
        const segment = transformedData.segments[i];
        const pathPoint = pathItem.pathPoints[i];

        // Set control handles (direction points)
        // rightDirection: handle going to next point
        // leftDirection: handle coming from previous point

        // Current point's outgoing handle (right direction)
        pathPoint.rightDirection = segment.controlPoint1;

        // Next point's incoming handle (left direction)
        const nextIndex = (i + 1) % pathItem.pathPoints.length;
        pathItem.pathPoints[nextIndex].leftDirection = segment.controlPoint2;

        // Set point type to SMOOTH for continuous curves
        pathPoint.pointType = PointType.SMOOTH;
    }

    // Close the path
    pathItem.closed = true;

    // Set default appearance
    pathItem.stroked = true;
    pathItem.filled = false;
    pathItem.strokeWidth = 2;

    // Set stroke color to black
    const strokeColor = new RGBColor();
    strokeColor.red = 0;
    strokeColor.green = 0;
    strokeColor.blue = 0;
    pathItem.strokeColor = strokeColor;

    return pathItem;
}

/**
 * Create a circle PathItem
 * @param {Document} doc - Illustrator document
 * @param {Object} transformedData - Circle data in Illustrator coordinates
 * @returns {PathItem} Created ellipse
 */
function createCirclePath(doc, transformedData) {
    const layer = doc.activeLayer;

    // Illustrator ellipse creation
    // ellipse(top, left, width, height)
    const centerX = transformedData.center[0];
    const centerY = transformedData.center[1];
    const radius = transformedData.radius;

    const ellipse = layer.pathItems.ellipse(
        centerY + radius,  // top
        centerX - radius,  // left
        radius * 2,        // width
        radius * 2         // height
    );

    // Set default appearance
    ellipse.stroked = true;
    ellipse.filled = false;
    ellipse.strokeWidth = 2;

    const strokeColor = new RGBColor();
    strokeColor.red = 70;
    strokeColor.green = 130;
    strokeColor.blue = 180;
    ellipse.strokeColor = strokeColor;

    return ellipse;
}

/**
 * Create a quadratic curve PathItem (n=2 case)
 * @param {Document} doc - Illustrator document
 * @param {Object} transformedData - Quadratic curve data
 * @returns {PathItem} Created path item
 */
function createQuadraticPath(doc, transformedData) {
    const layer = doc.activeLayer;
    const pathItem = layer.pathItems.add();

    // Set two anchor points
    pathItem.setEntirePath([
        transformedData.start,
        transformedData.end
    ]);

    // Quadratic curve: convert to cubic Bézier
    // Quadratic: start, control, end
    // Cubic: start, cp1, cp2, end
    // cp1 = start + 2/3 * (control - start)
    // cp2 = end + 2/3 * (control - end)

    const control = transformedData.controlPoint;
    const start = transformedData.start;
    const end = transformedData.end;

    const cp1 = [
        start[0] + (2/3) * (control[0] - start[0]),
        start[1] + (2/3) * (control[1] - start[1])
    ];

    const cp2 = [
        end[0] + (2/3) * (control[0] - end[0]),
        end[1] + (2/3) * (control[1] - end[1])
    ];

    // Set control handles
    pathItem.pathPoints[0].rightDirection = cp1;
    pathItem.pathPoints[1].leftDirection = cp2;
    pathItem.pathPoints[0].pointType = PointType.SMOOTH;
    pathItem.pathPoints[1].pointType = PointType.SMOOTH;

    // Open path for n=2 case
    pathItem.closed = false;
    pathItem.stroked = true;
    pathItem.filled = false;
    pathItem.strokeWidth = 3;

    const strokeColor = new RGBColor();
    strokeColor.red = 70;
    strokeColor.green = 130;
    strokeColor.blue = 180;
    pathItem.strokeColor = strokeColor;

    return pathItem;
}

/**
 * Main function: Generate FloAng pattern in Illustrator
 * @param {Object} params - Pattern parameters
 * @param {number} params.sides - Number of sides
 * @param {number} params.flowFactor - Flow factor
 * @param {number} params.handleAngle - Handle angle in degrees
 * @param {number} params.rotation - Rotation in degrees
 * @returns {PathItem} Created path item
 */
export async function generatePattern(params) {
    const app = require('illustrator').app;

    // Check if document exists
    if (app.documents.length === 0) {
        throw new Error('No document open. Please create or open a document.');
    }

    const doc = app.activeDocument;

    // Check if layer is locked
    if (doc.activeLayer.locked) {
        throw new Error('Active layer is locked. Please unlock the layer to generate patterns.');
    }

    // Get artboard information
    const artboardInfo = getArtboardInfo(doc);

    // Calculate pattern center and radius
    const centerX = artboardInfo.centerX;
    const centerY = artboardInfo.centerY;
    const radius = calculatePatternRadius(artboardInfo);

    // Import core algorithm
    const { generateFlowAngleData } = await import('./flowangle-core.js');

    // Generate pattern data in SVG space
    const patternData = generateFlowAngleData({
        ...params,
        centerX: centerX,
        centerY: centerY,
        radius: radius
    });

    // Transform to Illustrator coordinates
    const transformedData = transformPatternData(patternData, artboardInfo);

    // Create appropriate PathItem based on type
    let pathItem;

    if (transformedData.type === 'circle') {
        pathItem = createCirclePath(doc, transformedData);
    } else if (transformedData.type === 'quadratic') {
        pathItem = createQuadraticPath(doc, transformedData);
    } else if (transformedData.type === 'bezier') {
        pathItem = createBezierPath(doc, transformedData);
    } else {
        throw new Error(`Unknown pattern type: ${transformedData.type}`);
    }

    // Set descriptive name
    pathItem.name = `FloAng Pattern [n=${params.sides}]`;

    // Select the created path
    doc.selection = [pathItem];

    return pathItem;
}

/**
 * Error handling wrapper for pattern generation
 * @param {Object} params - Pattern parameters
 * @returns {Object} { success: boolean, pathItem?: PathItem, error?: string }
 */
export async function generatePatternSafe(params) {
    try {
        const pathItem = await generatePattern(params);
        return {
            success: true,
            pathItem: pathItem
        };
    } catch (error) {
        return {
            success: false,
            error: error.message
        };
    }
}
