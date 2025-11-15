/**
 * FloAng Core Algorithm
 * Ported from FloAng.html generateFlowAngle() function
 *
 * Generates geometric patterns based on regular polygons with Bézier curve handles
 * Algorithm creates flowing shapes by manipulating control point positions
 *
 * Mathematical foundation:
 * - Orthogonal angle formula: (n-2) × 180 / n
 * - Bézier cubic curves connect vertices with precisely calculated control points
 * - Flow factor controls handle distance from vertices
 * - Handle angle determines curve character
 */

/**
 * Calculate orthogonal (natural centered) angle for a polygon
 * @param {number} sides - Number of polygon sides
 * @returns {number} Orthogonal angle in degrees
 */
export function calculateOrthogonalAngle(sides) {
    return ((sides - 2) * 180) / sides;
}

/**
 * Generate FlowAngle pattern data structure
 * @param {Object} params - Pattern parameters
 * @param {number} params.sides - Number of polygon sides (1-12)
 * @param {number} params.flowFactor - Handle distance multiplier (-3 to 1)
 * @param {number} params.handleAngle - Bézier handle angle in degrees
 * @param {number} params.rotation - Pattern rotation in degrees
 * @param {number} params.centerX - Center X coordinate
 * @param {number} params.centerY - Center Y coordinate
 * @param {number} params.radius - Pattern radius
 * @returns {Object} Pattern data with vertices, control points, and path segments
 */
export function generateFlowAngleData(params) {
    const {
        sides,
        flowFactor,
        handleAngle,
        rotation,
        centerX,
        centerY,
        radius
    } = params;

    // Calculate polygon vertices
    const vertices = [];
    const angleStep = (2 * Math.PI) / sides;
    const rotRad = (rotation * Math.PI) / 180;

    for (let i = 0; i < sides; i++) {
        const angle = rotRad + i * angleStep;
        vertices.push({
            x: centerX + radius * Math.cos(angle),
            y: centerY + radius * Math.sin(angle)
        });
    }

    // Special case: n=1 (circle)
    if (sides === 1) {
        return {
            type: 'circle',
            center: { x: centerX, y: centerY },
            radius: radius
        };
    }

    // Special case: n=2 (curved line)
    if (sides === 2) {
        const v1 = vertices[0];
        const v2 = vertices[1];
        const midX = (v1.x + v2.x) / 2;
        const midY = (v1.y + v2.y) / 2;

        // Calculate perpendicular offset for control point
        const dx = v2.x - v1.x;
        const dy = v2.y - v1.y;
        const perpX = dy;
        const perpY = -dx;
        const baseLength = Math.sqrt(dx * dx + dy * dy);
        const perpLength = Math.sqrt(perpX * perpX + perpY * perpY);
        const offset = (baseLength / 2) * flowFactor;

        const cpX = midX + (perpX / perpLength) * offset;
        const cpY = midY + (perpY / perpLength) * offset;

        return {
            type: 'quadratic',
            start: v1,
            end: v2,
            controlPoint: { x: cpX, y: cpY }
        };
    }

    // Standard case: n >= 3 (full algorithm)
    // Build triangles for each edge
    const triangles = [];
    const apexAngle = (handleAngle * Math.PI) / 180;

    for (let i = 0; i < sides; i++) {
        const v1 = vertices[i];
        const v2 = vertices[(i + 1) % sides];

        // Calculate midpoint
        const midX = (v1.x + v2.x) / 2;
        const midY = (v1.y + v2.y) / 2;

        // Calculate perpendicular direction
        const dx = v2.x - v1.x;
        const dy = v2.y - v1.y;
        const baseLength = Math.sqrt(dx * dx + dy * dy);

        // Perpendicular vector (rotated 90 degrees)
        const perpX = dy;
        const perpY = -dx;
        const perpLength = Math.sqrt(perpX * perpX + perpY * perpY);

        // Calculate triangle apex (third point) based on handle angle
        const height = (baseLength / 2) / Math.tan(apexAngle / 2);
        const thirdX = midX + (perpX / perpLength) * height;
        const thirdY = midY + (perpY / perpLength) * height;

        triangles.push({
            v1: v1,
            v2: v2,
            third: { x: thirdX, y: thirdY }
        });
    }

    // Calculate Bézier control points for each segment
    const segments = [];

    for (let i = 0; i < sides; i++) {
        const tri = triangles[i];
        const nextVertex = vertices[(i + 1) % sides];

        // Calculate control points using flow factor
        // Control points are positioned between vertex and triangle apex
        const cp1x = tri.v1.x + (tri.third.x - tri.v1.x) * flowFactor;
        const cp1y = tri.v1.y + (tri.third.y - tri.v1.y) * flowFactor;

        const cp2x = tri.v2.x + (tri.third.x - tri.v2.x) * flowFactor;
        const cp2y = tri.v2.y + (tri.third.y - tri.v2.y) * flowFactor;

        segments.push({
            start: tri.v1,
            end: nextVertex,
            controlPoint1: { x: cp1x, y: cp1y },
            controlPoint2: { x: cp2x, y: cp2y },
            triangle: tri
        });
    }

    return {
        type: 'bezier',
        vertices: vertices,
        triangles: triangles,
        segments: segments,
        center: { x: centerX, y: centerY },
        radius: radius
    };
}

/**
 * Calculate preset configurations
 * These are the proven parameter combinations from the web version
 */
export const PRESETS = {
    triquetra: {
        sides: 3,
        flowFactor: -0.66,
        handleAngle: 60,
        rotation: -30
    },
    flower: {
        sides: 6,
        flowFactor: -0.8,
        handleAngle: 30,
        rotation: 0
    },
    star: {
        sides: 5,
        flowFactor: -1.8,
        handleAngle: 72,
        rotation: -18
    },
    smooth: {
        sides: 6,
        flowFactor: 1.0,
        handleAngle: 120,
        rotation: 0
    }
};

/**
 * Validate pattern parameters
 * @param {Object} params - Parameters to validate
 * @returns {Object} { valid: boolean, errors: string[] }
 */
export function validateParameters(params) {
    const errors = [];

    if (params.sides < 1 || params.sides > 12) {
        errors.push('Sides must be between 1 and 12');
    }

    if (params.flowFactor < -3 || params.flowFactor > 1) {
        errors.push('Flow factor must be between -3 and 1');
    }

    if (params.handleAngle < 0 || params.handleAngle > 180) {
        errors.push('Handle angle must be between 0 and 180 degrees');
    }

    if (params.rotation < -360 || params.rotation > 360) {
        errors.push('Rotation must be between -360 and 360 degrees');
    }

    return {
        valid: errors.length === 0,
        errors: errors
    };
}
