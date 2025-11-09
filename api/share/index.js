/**
 * POST /api/share - Save FlowAngle configuration to Vercel KV
 *
 * Request Body:
 * {
 *   sides: number,
 *   curveFactor: number,
 *   handleAngle: number,
 *   rotation: number,
 *   showGuides: boolean,
 *   keyframes?: array
 * }
 *
 * Response:
 * {
 *   success: true,
 *   shareId: "abc12345",
 *   url: "/share/abc12345",
 *   fullUrl: "https://domain.com/share/abc12345"
 * }
 */

import { kv } from '@vercel/kv';
import { nanoid } from 'nanoid';

// Rate limiting configuration
const RATE_LIMIT_MAX_REQUESTS = 10; // Max requests per time window
const RATE_LIMIT_WINDOW_MS = 60000; // 1 minute window
const SHARE_EXPIRY_SECONDS = 90 * 24 * 60 * 60; // 90 days

/**
 * Check rate limit for an IP address
 */
async function checkRateLimit(ip) {
  const key = `ratelimit:${ip}`;
  const current = await kv.get(key);

  if (current && current >= RATE_LIMIT_MAX_REQUESTS) {
    return false;
  }

  // Increment counter
  const pipe = kv.pipeline();
  pipe.incr(key);

  if (!current) {
    // Set expiry only on first request
    pipe.expire(key, Math.ceil(RATE_LIMIT_WINDOW_MS / 1000));
  }

  await pipe.exec();
  return true;
}

/**
 * Validate configuration data
 */
function validateConfig(config) {
  const errors = [];

  // Required fields
  if (typeof config.sides !== 'number' || config.sides < 1 || config.sides > 12) {
    errors.push('sides must be a number between 1 and 12');
  }

  if (typeof config.curveFactor !== 'number' || config.curveFactor < -3 || config.curveFactor > 1) {
    errors.push('curveFactor must be a number between -3 and 1');
  }

  if (typeof config.handleAngle !== 'number' || config.handleAngle < 10 || config.handleAngle > 170) {
    errors.push('handleAngle must be a number between 10 and 170');
  }

  if (typeof config.rotation !== 'number') {
    errors.push('rotation must be a number');
  }

  if (typeof config.showGuides !== 'boolean') {
    errors.push('showGuides must be a boolean');
  }

  // Optional keyframes validation
  if (config.keyframes !== undefined) {
    if (!Array.isArray(config.keyframes)) {
      errors.push('keyframes must be an array');
    } else if (config.keyframes.length > 50) {
      errors.push('maximum 50 keyframes allowed');
    } else {
      // Validate each keyframe has same structure
      config.keyframes.forEach((kf, index) => {
        if (typeof kf.sides !== 'number' || kf.sides < 1 || kf.sides > 12) {
          errors.push(`keyframe ${index}: invalid sides`);
        }
        if (typeof kf.curveFactor !== 'number') {
          errors.push(`keyframe ${index}: invalid curveFactor`);
        }
        if (typeof kf.handleAngle !== 'number') {
          errors.push(`keyframe ${index}: invalid handleAngle`);
        }
        if (typeof kf.rotation !== 'number') {
          errors.push(`keyframe ${index}: invalid rotation`);
        }
      });
    }
  }

  return errors;
}

export default async function handler(req, res) {
  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({
      success: false,
      error: 'Method not allowed. Use POST.'
    });
  }

  try {
    // Get client IP for rate limiting
    const ip = req.headers['x-forwarded-for']?.split(',')[0] ||
               req.headers['x-real-ip'] ||
               req.socket?.remoteAddress ||
               'unknown';

    // Check rate limit
    const allowed = await checkRateLimit(ip);
    if (!allowed) {
      return res.status(429).json({
        success: false,
        error: 'Rate limit exceeded. Please try again later.',
        retryAfter: 60
      });
    }

    // Parse and validate request body
    const config = req.body;

    if (!config) {
      return res.status(400).json({
        success: false,
        error: 'Request body is required'
      });
    }

    // Validate configuration
    const validationErrors = validateConfig(config);
    if (validationErrors.length > 0) {
      return res.status(400).json({
        success: false,
        error: 'Invalid configuration',
        details: validationErrors
      });
    }

    // Generate unique short ID (8 characters for good collision resistance)
    const shareId = nanoid(8);

    // Store configuration in Vercel KV with metadata
    const dataToStore = {
      config: {
        sides: config.sides,
        curveFactor: config.curveFactor,
        handleAngle: config.handleAngle,
        rotation: config.rotation,
        showGuides: config.showGuides,
        keyframes: config.keyframes || []
      },
      metadata: {
        createdAt: new Date().toISOString(),
        createdBy: ip,
        views: 0
      }
    };

    // Store with 90-day expiry
    await kv.set(`share:${shareId}`, dataToStore, {
      ex: SHARE_EXPIRY_SECONDS
    });

    // Construct URLs
    const protocol = req.headers['x-forwarded-proto'] || 'http';
    const host = req.headers['x-forwarded-host'] || req.headers.host;
    const baseUrl = `${protocol}://${host}`;
    const sharePath = `/share/${shareId}`;
    const fullUrl = `${baseUrl}${sharePath}`;

    // Return success response
    return res.status(200).json({
      success: true,
      shareId: shareId,
      url: sharePath,
      fullUrl: fullUrl,
      expiresIn: `${SHARE_EXPIRY_SECONDS / (24 * 60 * 60)} days`
    });

  } catch (error) {
    console.error('Error saving configuration:', error);

    return res.status(500).json({
      success: false,
      error: 'Failed to save configuration',
      message: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
}
