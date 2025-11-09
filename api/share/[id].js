/**
 * GET /api/share/[id] - Load FlowAngle configuration from Vercel KV
 *
 * URL Parameters:
 *   id: The share ID (e.g., "abc12345")
 *
 * Response (Success):
 * {
 *   success: true,
 *   config: {
 *     sides: number,
 *     curveFactor: number,
 *     handleAngle: number,
 *     rotation: number,
 *     showGuides: boolean,
 *     keyframes: array
 *   },
 *   metadata: {
 *     createdAt: string,
 *     views: number
 *   }
 * }
 *
 * Response (Not Found):
 * {
 *   success: false,
 *   error: "Configuration not found or expired"
 * }
 */

import { kv } from '@vercel/kv';

export default async function handler(req, res) {
  // Only allow GET requests
  if (req.method !== 'GET') {
    return res.status(405).json({
      success: false,
      error: 'Method not allowed. Use GET.'
    });
  }

  try {
    // Extract share ID from query parameter
    const { id } = req.query;

    if (!id) {
      return res.status(400).json({
        success: false,
        error: 'Share ID is required'
      });
    }

    // Validate ID format (alphanumeric, 8 characters for nanoid)
    if (!/^[a-zA-Z0-9_-]{8}$/.test(id)) {
      return res.status(400).json({
        success: false,
        error: 'Invalid share ID format'
      });
    }

    // Retrieve configuration from Vercel KV
    const key = `share:${id}`;
    const data = await kv.get(key);

    if (!data) {
      return res.status(404).json({
        success: false,
        error: 'Configuration not found or expired',
        shareId: id
      });
    }

    // Increment view counter asynchronously (fire and forget)
    // We use a separate counter key to avoid race conditions
    kv.incr(`share:${id}:views`).catch(err => {
      console.error('Failed to increment view counter:', err);
    });

    // Update the views in the main data if it exists
    if (data.metadata) {
      const currentViews = await kv.get(`share:${id}:views`) || 0;
      data.metadata.views = currentViews;
    }

    // Return configuration with metadata
    return res.status(200).json({
      success: true,
      config: data.config,
      metadata: {
        createdAt: data.metadata?.createdAt,
        views: data.metadata?.views || 0
      }
    });

  } catch (error) {
    console.error('Error loading configuration:', error);

    return res.status(500).json({
      success: false,
      error: 'Failed to load configuration',
      message: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
}
