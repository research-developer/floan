# Vercel KV Setup Guide

This guide explains how to set up Vercel KV (Redis) for the FlowAngle Studio sharing feature.

## Overview

The FlowAngle Studio uses Vercel KV to store and retrieve shared configurations via short URLs like `/share/abc12345`. This replaces the long hash-based URLs with a cleaner database-backed approach.

## Prerequisites

- Vercel account
- Project deployed to Vercel (or ready to deploy)
- Node.js installed (for local development)

## Setup Steps

### 1. Create a Vercel KV Database

1. Go to your [Vercel Dashboard](https://vercel.com/dashboard)
2. Navigate to the **Storage** tab
3. Click **Create Database**
4. Select **KV** (Redis-compatible key-value store)
5. Choose a name (e.g., `flowangle-kv`)
6. Select a region close to your users
7. Click **Create**

### 2. Link Database to Your Project

1. In your Vercel project settings, go to **Storage**
2. Click **Connect Store**
3. Select the KV database you just created
4. Click **Connect**

This automatically adds the following environment variables to your project:
- `KV_URL`
- `KV_REST_API_URL`
- `KV_REST_API_TOKEN`
- `KV_REST_API_READ_ONLY_TOKEN`

### 3. Local Development Setup

For local development, you'll need to pull the environment variables:

```bash
# Install Vercel CLI if not already installed
npm install -g vercel

# Login to Vercel
vercel login

# Link your project
vercel link

# Pull environment variables
vercel env pull .env.local
```

This creates a `.env.local` file with your KV credentials.

### 4. Install Dependencies

```bash
npm install
```

This installs:
- `@vercel/kv` - Official Vercel KV client
- `nanoid` - For generating short, collision-resistant IDs

### 5. Deploy

```bash
# Deploy to production
vercel --prod

# Or deploy to preview
vercel
```

## API Endpoints

### POST /api/share

Save a FlowAngle configuration to the database.

**Request:**
```json
{
  "sides": 3,
  "curveFactor": -0.66,
  "handleAngle": 60,
  "rotation": 0,
  "showGuides": false,
  "keyframes": [...]  // Optional
}
```

**Response:**
```json
{
  "success": true,
  "shareId": "abc12345",
  "url": "/share/abc12345",
  "fullUrl": "https://your-domain.com/share/abc12345",
  "expiresIn": "90 days"
}
```

### GET /api/share/[id]

Load a shared configuration from the database.

**Response:**
```json
{
  "success": true,
  "config": {
    "sides": 3,
    "curveFactor": -0.66,
    "handleAngle": 60,
    "rotation": 0,
    "showGuides": false,
    "keyframes": [...]
  },
  "metadata": {
    "createdAt": "2024-01-01T00:00:00.000Z",
    "views": 42
  }
}
```

## Features

### Rate Limiting

The API includes built-in rate limiting to prevent abuse:
- **Limit:** 10 shares per minute per IP address
- **Window:** 60 seconds
- **Response:** 429 Too Many Requests with `retryAfter` header

### Data Expiration

Shared configurations automatically expire after **90 days** to prevent database bloat.

### View Tracking

Each time a shared link is loaded, the view counter increments (analytics feature).

### Validation

All configurations are validated before storage:
- `sides`: 1-12
- `curveFactor`: -3 to 1
- `handleAngle`: 10-170 degrees
- `rotation`: any number
- `keyframes`: max 50 frames

### Short IDs

Share IDs are generated using `nanoid` with 8 characters:
- ~13 billion years to have 1% collision probability at 1000 IDs/hour
- URL-safe characters (A-Za-z0-9_-)

## Architecture

```
User clicks "Share"
    ↓
Frontend sends POST /api/share
    ↓
API validates config
    ↓
Generate unique ID with nanoid(8)
    ↓
Store in KV: key="share:abc12345"
    ↓
Return short URL: /share/abc12345
    ↓
Copy to clipboard
```

```
User visits /share/abc12345
    ↓
Frontend detects /share/ route
    ↓
Call GET /api/share/abc12345
    ↓
KV returns configuration
    ↓
Apply to UI controls
    ↓
Increment view counter
```

## Database Schema

### Keys

```
share:{shareId}          # Main configuration data
share:{shareId}:views    # View counter (separate for race condition safety)
ratelimit:{ip}           # Rate limit counter
```

### Data Structure

```typescript
{
  config: {
    sides: number,
    curveFactor: number,
    handleAngle: number,
    rotation: number,
    showGuides: boolean,
    keyframes?: Array<{
      sides: number,
      curveFactor: number,
      handleAngle: number,
      rotation: number,
      showGuides: boolean
    }>
  },
  metadata: {
    createdAt: string,  // ISO 8601 timestamp
    createdBy: string,  // IP address (hashed for privacy)
    views: number
  }
}
```

## Troubleshooting

### "Failed to create share link"

1. Check Vercel deployment logs for errors
2. Verify KV database is connected to your project
3. Ensure environment variables are set correctly
4. Check rate limit hasn't been exceeded

### "Configuration not found or expired"

- The share link may have expired (90 days)
- The share ID may be invalid
- Check the share ID in the URL is exactly 8 characters

### Local Development Issues

If the API doesn't work locally:

```bash
# Make sure you've pulled environment variables
vercel env pull .env.local

# Start local dev server
vercel dev
```

## Cost Considerations

Vercel KV pricing (as of 2024):
- **Hobby Plan:** 256 MB storage, 3k commands/day - FREE
- **Pro Plan:** 512 MB storage, 10k commands/month, then $0.25/100k
- **Enterprise:** Custom pricing

With 90-day expiration and typical usage:
- ~1000 shares/month ≈ 500KB storage
- Well within free tier limits

## Security

- Rate limiting prevents abuse
- Input validation prevents injection attacks
- No sensitive user data is stored
- Share IDs are cryptographically random
- HTTPS enforced by Vercel

## Monitoring

To monitor your KV database:
1. Go to Vercel Dashboard → Storage → Your KV Database
2. View metrics: storage used, commands, latency
3. Check logs in Vercel project → Logs tab

## Fallback Mode

If the database is unavailable, the app automatically falls back to hash-based URL sharing (the old method). This ensures the app remains functional even if KV has issues.

## Next Steps

- [ ] Set up alerts for rate limit violations
- [ ] Add analytics dashboard for share metrics
- [ ] Implement share link preview images (Open Graph)
- [ ] Add user authentication for private shares

---

## Support

For issues or questions:
- Check Vercel KV documentation: https://vercel.com/docs/storage/vercel-kv
- Review API logs in Vercel dashboard
- Contact support@vercel.com for KV-specific issues
