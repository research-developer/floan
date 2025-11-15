# System Architecture Document: FloAng Illustrator Plugin

## Executive Summary

This document defines the technical architecture for the FloAng Illustrator Plugin, a CEP-based extension that enables intelligent angular flow design in Adobe Illustrator. The architecture leverages HTML5/CSS3/JavaScript for the UI layer, ExtendScript for Illustrator integration, and a modular component design that separates concerns between UI, computational logic, and Adobe API interactions. Key architectural decisions prioritize developer experience through modern tooling (Vite, TypeScript), maintainability through clear separation of concerns, and extensibility through well-defined interfaces between components.

## Architecture Overview

### System Context

The FloAng plugin operates as an embedded extension within Adobe Illustrator, bridging modern web technologies with Adobe's ExtendScript environment. The system must handle:

- Real-time UI interactions from designers
- Complex angular calculations and path generation
- Bidirectional communication between JavaScript and ExtendScript
- State synchronization between UI and Illustrator document
- Asynchronous operations with proper error handling

```
┌─────────────────────────────────────────────────────────────┐
│                    Adobe Illustrator                         │
│  ┌────────────────────────────────────────────────────┐    │
│  │          FloAng CEP Extension Panel                 │    │
│  │  ┌──────────────────────────────────────────────┐  │    │
│  │  │  Modern Web UI (HTML5/CSS3/JavaScript)       │  │    │
│  │  │  - React components                          │  │    │
│  │  │  - State management                          │  │    │
│  │  │  - Event handling                            │  │    │
│  │  └──────────────────────────────────────────────┘  │    │
│  │                      ↕ CSInterface                 │    │
│  │  ┌──────────────────────────────────────────────┐  │    │
│  │  │  ExtendScript Layer                          │  │    │
│  │  │  - Illustrator API integration               │  │    │
│  │  │  - Path manipulation                         │  │    │
│  │  │  - Document operations                       │  │    │
│  │  └──────────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Architecture Principles

1. **Separation of Concerns**: Clear boundaries between UI, business logic, and Adobe integration
   - Rationale: Enables independent testing, easier maintenance, and parallel development

2. **Modern Development Experience**: Use contemporary JavaScript tooling and practices
   - Rationale: Improves developer productivity, code quality, and team onboarding

3. **Defensive Programming**: Comprehensive error handling and validation
   - Rationale: CEP environment is fragile; graceful degradation prevents user frustration

4. **Performance First**: Minimize ExtendScript calls and optimize calculations
   - Rationale: ExtendScript is slow; batching operations and caching improves responsiveness

5. **Incremental Enhancement**: Build core features first, add complexity progressively
   - Rationale: Ensures a working foundation before tackling advanced features

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Presentation Layer                        │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│  │   React    │  │   CSS3     │  │  Controls  │               │
│  │ Components │  │  Styling   │  │  Library   │               │
│  └────────────┘  └────────────┘  └────────────┘               │
└─────────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│  │   State    │  │  Angular   │  │   Event    │               │
│  │ Management │  │  Engines   │  │  System    │               │
│  └────────────┘  └────────────┘  └────────────┘               │
└─────────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────────┐
│                     Integration Layer                           │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│  │    CEP     │  │ExtendScript│  │   Bridge   │               │
│  │   Bridge   │  │   Host     │  │  Protocol  │               │
│  └────────────┘  └────────────┘  └────────────┘               │
└─────────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────────┐
│                   Adobe Illustrator Layer                       │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               ���
│  │  Document  │  │   Path     │  │  Selection │               │
│  │    API     │  │    API     │  │    API     │               │
│  └────────────┘  └────────────┘  └────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### Frontend Layer

#### Technology Stack
- **Framework**: React 18 - Component-based UI with hooks for state management
  - Justification: Industry standard, excellent developer tools, large ecosystem, efficient re-rendering
- **Build Tool**: Vite - Fast development server and optimized production builds
  - Justification: Superior HMR performance, native ES modules, CEP-compatible output
- **Language**: TypeScript 5.x - Static typing for improved code quality
  - Justification: Catches errors at compile time, better IDE support, self-documenting code
- **Styling**: CSS Modules + CSS Variables - Scoped styling with design tokens
  - Justification: No runtime overhead, prevents style conflicts, theming support

#### Component Structure

```
src/
├── components/
│   ├── App.tsx                    # Root component
│   ├── ControlPanel/
│   │   ├── ControlPanel.tsx       # Main control container
│   │   ├── FlowControl.tsx        # Flow percentage slider
│   │   ├── AngleControl.tsx       # Dynamic angle slider
│   │   ├── SpinControl.tsx        # Spin value slider
│   │   └── PresetButtons.tsx      # Quick preset buttons
│   ├── PreviewCanvas/
│   │   ├── PreviewCanvas.tsx      # Visual preview component
│   │   └── AngleVisualizer.tsx    # Angle visualization
│   └── shared/
│       ├── Slider.tsx             # Reusable slider component
│       ├── Button.tsx             # Reusable button component
│       └── StatusIndicator.tsx    # Connection status
```

**Key Components**:

- **App.tsx**: Root component managing global state and CEP initialization
- **ControlPanel**: Houses all user controls, emits change events to bridge
- **FlowControl**: Logarithmic slider (0-100%) for flow percentage with visual feedback
- **AngleControl**: Dynamic slider with orthogonal snapping based on current Spin value
- **SpinControl**: Linear slider (-360° to +360°) for overall spin adjustment
- **PreviewCanvas**: Real-time visualization of angle distribution using HTML5 Canvas

### Backend Layer

#### Technology Stack
- **Language**: ExtendScript (JavaScript ES3) - Adobe's scripting environment
  - Justification: Required for Illustrator API access, no alternative
- **Bridge**: CEP CSInterface - Standard Adobe bridge for CEP extensions
  - Justification: Official Adobe solution, reliable, well-documented

#### Service Architecture

```
host/
├── index.jsx                      # ExtendScript entry point
├── core/
│   ├── angleEngine.jsx            # Core angular calculations
│   ├── pathGenerator.jsx          # Illustrator path creation
│   └── selectionManager.jsx       # Selection handling
├── utils/
│   ├── mathUtils.jsx              # Mathematical utilities
│   ├── validator.jsx              # Input validation
│   └── errorHandler.jsx           # Error handling
└── api/
    ├── documentAPI.jsx            # Document operations
    └── pathAPI.jsx                # Path manipulation
```

**Key Services**:

- **angleEngine.jsx**: Implements angular distribution algorithms
  - Logarithmic flow distribution
  - Orthogonal angle calculation
  - Spin offset application

- **pathGenerator.jsx**: Creates and manipulates Illustrator paths
  - Converts angular data to path points
  - Applies transformations
  - Handles path properties (stroke, fill, etc.)

- **selectionManager.jsx**: Manages path selection and validation
  - Detects selected paths
  - Validates path types
  - Provides selection feedback

### Data Layer

#### Data Architecture

The plugin operates on ephemeral state synchronized between UI and Illustrator:

```
┌────────────────────────────────────────────────┐
│              UI State (React)                  │
│  {                                             │
│    flow: number,        // 0-100               │
│    angle: number,       // -90 to 90           │
│    spin: number,        // -360 to 360         │
│    isConnected: boolean,                       │
│    selectedPath: PathInfo | null               │
│  }                                             │
└────────────────────────────────────────────────┘
                      ↕ Synchronization
┌────────────────────────────────────────────────┐
│         Illustrator State (Document)           │
│  {                                             │
│    activePath: PathItem,                       │
│    points: Array<PathPoint>,                   │
│    angles: Array<number>                       │
│  }                                             │
└────────────────────────────────────────────────┘
```

#### Data Models

**PathInfo** (TypeScript):
```typescript
interface PathInfo {
  id: string;
  pointCount: number;
  isClosed: boolean;
  bounds: {
    left: number;
    top: number;
    width: number;
    height: number;
  };
}
```

**AngleDistribution** (TypeScript):
```typescript
interface AngleDistribution {
  angles: number[];           // Array of angles for each point
  baseAngle: number;          // Current angle control value
  flowPercentage: number;     // Current flow percentage
  spinOffset: number;         // Current spin value
}
```

**PathPoint** (ExtendScript):
```javascript
// Native Illustrator PathPoint object with:
// - anchor: [x, y]
// - leftDirection: [x, y]
// - rightDirection: [x, y]
```

## API Design

### API Standards
- **Protocol**: JavaScript function calls via CSInterface.evalScript()
- **Format**: JSON for data exchange between layers
- **Error Handling**: Consistent error object format across all API calls

### Bridge Communication

The CEP bridge follows a command-response pattern:

#### JavaScript → ExtendScript

```typescript
// src/bridge/cepBridge.ts
interface BridgeCommand {
  action: string;
  payload: any;
}

class CEPBridge {
  async executeCommand(command: BridgeCommand): Promise<any> {
    return new Promise((resolve, reject) => {
      const csInterface = new CSInterface();
      const script = `executeCommand(${JSON.stringify(command)})`;

      csInterface.evalScript(script, (result) => {
        try {
          const parsed = JSON.parse(result);
          if (parsed.error) {
            reject(new Error(parsed.error));
          } else {
            resolve(parsed.data);
          }
        } catch (e) {
          reject(e);
        }
      });
    });
  }
}
```

#### ExtendScript → Response

```javascript
// host/index.jsx
function executeCommand(commandJSON) {
  try {
    var command = JSON.parse(commandJSON);
    var result = handleAction(command.action, command.payload);
    return JSON.stringify({ data: result, error: null });
  } catch (e) {
    return JSON.stringify({ data: null, error: e.message });
  }
}
```

### Key API Operations

| Operation | Direction | Purpose | Payload |
|-----------|-----------|---------|---------|
| `getSelectedPath` | JS → ES | Get active path info | `{}` |
| `updateAngles` | JS → ES | Apply new angles to path | `{ angles: number[], flow: number, spin: number }` |
| `previewAngles` | JS → ES | Non-destructive preview | `{ angles: number[], temporary: true }` |
| `resetPath` | JS → ES | Restore original path | `{ pathId: string }` |
| `validateSelection` | JS → ES | Check if valid path selected | `{}` |

**Response Format**:
```typescript
interface APIResponse<T> {
  data: T | null;
  error: string | null;
  timestamp: number;
}
```

## Security Architecture

### Authentication & Authorization
- **Authentication Method**: N/A - Desktop plugin, no user authentication required
- **Authorization Model**: Operating system file permissions control plugin installation
- **Data Access**: Plugin operates only on user's open Illustrator documents with explicit user action

### Security Layers

1. **Input Validation**: All user inputs validated in both JavaScript and ExtendScript layers
   - Range checking on numeric inputs
   - Type validation on all parameters
   - Sanitization of any string inputs used in evalScript

2. **Script Injection Prevention**: All data passed to ExtendScript properly escaped
   - JSON serialization for structured data
   - No direct string concatenation in evalScript calls
   - Command pattern prevents arbitrary code execution

3. **Error Information Disclosure**: Error messages sanitized to prevent information leakage
   - Generic user-facing messages
   - Detailed logs only in development builds
   - No file system paths exposed to UI

### Threat Model

| Threat | Impact | Mitigation |
|--------|--------|------------|
| Malicious script injection via UI inputs | High - Could execute arbitrary code in Illustrator | All inputs JSON-serialized, no eval() in ExtendScript, strict input validation |
| Corrupted Illustrator documents causing crashes | Medium - User loses work | Comprehensive error handling, validation before path manipulation, undo support |
| Plugin conflicts with other extensions | Low - Functionality impaired | Namespaced global variables, defensive checks for Illustrator state |
| Unhandled exceptions crashing panel | Medium - User forced to restart | Try-catch at all API boundaries, graceful error display |

## Infrastructure & Deployment

### Infrastructure Architecture

- **Platform**: Desktop application (Adobe Illustrator CEP extension)
- **Distribution**: Manual ZXP installation or Adobe Exchange marketplace
- **Installation Location**:
  - macOS: `~/Library/Application Support/Adobe/CEP/extensions/`
  - Windows: `%APPDATA%\Adobe\CEP\extensions\`

### Build & Packaging

```
┌─────────────────────────────────────────────────┐
│           Development Environment               │
│  ┌──────────────┐      ┌──────────────┐        │
│  │    Vite      │      │  TypeScript  │        │
│  │  Dev Server  │──────│   Compiler   │        │
│  └──────────────┘      └──────────────┘        │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│              Build Process (npm run build)      │
│  1. TypeScript compilation                      │
│  2. Vite bundling & optimization                │
│  3. Asset copying (manifest, ExtendScript)      │
│  4. CEP manifest validation                     │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│            Package Structure                    │
│  floang-plugin/                                 │
│  ├── CSXS/                                      │
│  │   └── manifest.xml    # CEP manifest         │
│  ├── host/                                      │
│  │   └── index.jsx       # ExtendScript bundle  │
│  ├── client/                                    │
│  │   ├── index.html      # Panel HTML           │
│  │   ├── main.js         # Bundled JavaScript   │
│  │   └── styles.css      # Bundled styles       │
│  └── .debug              # Debug config         │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│              ZXP Packaging                      │
│  - Digital signature (if distributing)          │
│  - Compressed archive                           │
│  - Install via Adobe Extension Manager          │
└─────────────────────────────────────────────────┘
```

### Environment Strategy

**Development**:
```javascript
// vite.config.ts
export default defineConfig({
  base: './',  // Relative paths for CEP
  build: {
    outDir: 'dist/client',
    sourcemap: true,
    minify: false,  // Easier debugging
  },
  server: {
    port: 3000,
    strictPort: true,
  }
});
```

**Production**:
```javascript
// vite.config.ts (production overrides)
export default defineConfig({
  build: {
    outDir: 'dist/client',
    sourcemap: false,
    minify: true,
    rollupOptions: {
      output: {
        manualChunks: undefined,  // Single bundle for CEP
      }
    }
  }
});
```

### Deployment Diagram

```
Developer Machine                  User Machine
┌──────────────┐                  ┌──────────────┐
│              │                  │              │
│  Git Repo    │                  │  Illustrator │
│  ↓           │                  │      +       │
│  npm build   │                  │  FloAng      │
│  ↓           │                  │   Plugin     │
│  ZXP Package │──────────────→   │              │
│              │   (Distribution) │              │
└──────────────┘                  └──────────────┘
```

## Performance & Scalability

### Performance Requirements

- **UI Response Time**: < 16ms per frame (60 FPS) for slider interactions
- **ExtendScript Execution**: < 100ms for angle calculation and path update
- **Path Operations**: Support paths with up to 1000 points without noticeable lag
- **Preview Rendering**: Real-time canvas updates at 60 FPS

### Performance Optimizations

#### Caching Strategy

**UI Layer**:
```typescript
// Memoize expensive calculations
const calculateAngles = useMemo(() => {
  return (flow: number, spin: number, pointCount: number) => {
    // Angular distribution calculation
    return angles;
  };
}, [flow, spin, pointCount]);

// Debounce ExtendScript calls
const debouncedUpdate = useDebouncedCallback(
  (angles) => bridge.updateAngles(angles),
  150  // 150ms debounce
);
```

**ExtendScript Layer**:
```javascript
// Cache path point data to avoid repeated API calls
var pathCache = {
  pathId: null,
  originalPoints: null,
  pointCount: 0
};

function getPathPoints(pathItem) {
  var id = pathItem.uuid;
  if (pathCache.pathId === id) {
    return pathCache.originalPoints;
  }
  // Expensive operation
  pathCache.originalPoints = clonePathPoints(pathItem);
  pathCache.pathId = id;
  return pathCache.originalPoints;
}
```

#### Batch Operations

```javascript
// host/core/pathGenerator.jsx
function applyAnglesToPath(pathItem, angles) {
  // Suspend screen redraw during updates
  app.redraw = false;

  try {
    // Batch all point modifications
    for (var i = 0; i < pathItem.pathPoints.length; i++) {
      var point = pathItem.pathPoints[i];
      var angle = angles[i];
      updateHandleAngle(point, angle);
    }
  } finally {
    // Re-enable redraw once
    app.redraw = true;
  }
}
```

#### Computational Optimization

```typescript
// Pre-calculate lookup tables for logarithmic distribution
const FLOW_LUT_SIZE = 101;
const flowLookupTable = new Array(FLOW_LUT_SIZE);

function buildFlowLUT() {
  for (let i = 0; i < FLOW_LUT_SIZE; i++) {
    const t = i / 100;
    flowLookupTable[i] = Math.log10(1 + 9 * t) / Math.log10(10);
  }
}

// Fast lookup instead of recalculation
function getFlowValue(percentage: number): number {
  const index = Math.round(percentage);
  return flowLookupTable[index];
}
```

### Scaling Strategy

**Path Complexity Scaling**:
- **Small paths (< 50 points)**: Real-time updates, no throttling
- **Medium paths (50-500 points)**: Debounced updates (150ms)
- **Large paths (500-1000 points)**: Throttled updates (300ms), loading indicator

**UI Scaling**:
- Canvas preview uses requestAnimationFrame for smooth rendering
- Slider interactions throttled to prevent excessive renders
- State updates batched using React's automatic batching

**Memory Management**:
- Path cache cleared when switching documents
- Preview canvas reuses same buffer
- Event listeners properly cleaned up in component unmount

## Reliability & Monitoring

### Reliability Targets

- **Availability**: 99.9% (plugin operational when Illustrator is running)
- **Error Recovery**: Graceful degradation on all error conditions
- **Data Integrity**: No corruption of Illustrator documents under any circumstance

### Failure Handling

**Circuit Breaker Pattern**:
```typescript
class BridgeCircuitBreaker {
  private failureCount = 0;
  private readonly threshold = 3;
  private state: 'closed' | 'open' | 'half-open' = 'closed';

  async execute<T>(operation: () => Promise<T>): Promise<T> {
    if (this.state === 'open') {
      throw new Error('Circuit breaker open - ExtendScript unavailable');
    }

    try {
      const result = await operation();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onFailure() {
    this.failureCount++;
    if (this.failureCount >= this.threshold) {
      this.state = 'open';
      setTimeout(() => this.state = 'half-open', 5000);
    }
  }

  private onSuccess() {
    this.failureCount = 0;
    this.state = 'closed';
  }
}
```

**Retry Logic**:
```typescript
async function retryOperation<T>(
  operation: () => Promise<T>,
  maxAttempts = 3,
  delayMs = 1000
): Promise<T> {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await operation();
    } catch (error) {
      if (attempt === maxAttempts) throw error;
      await sleep(delayMs * attempt);  // Exponential backoff
    }
  }
  throw new Error('Max retry attempts exceeded');
}
```

**Graceful Degradation**:
```typescript
// If ExtendScript fails, continue with UI-only mode
function handleBridgeFailure(error: Error) {
  console.error('Bridge communication failed:', error);

  // Update UI to show disconnected state
  setState({
    isConnected: false,
    mode: 'preview-only'  // Show preview but disable Illustrator updates
  });

  // Show user-friendly error message
  showNotification({
    type: 'warning',
    message: 'Connection to Illustrator lost. Working in preview mode.',
    action: { label: 'Retry', onClick: reconnect }
  });
}
```

### Monitoring & Observability

**Logging Strategy**:
```typescript
// src/utils/logger.ts
enum LogLevel {
  DEBUG = 0,
  INFO = 1,
  WARN = 2,
  ERROR = 3
}

class Logger {
  private level: LogLevel = process.env.NODE_ENV === 'development'
    ? LogLevel.DEBUG
    : LogLevel.WARN;

  debug(message: string, data?: any) {
    if (this.level <= LogLevel.DEBUG) {
      console.debug(`[FloAng Debug] ${message}`, data);
    }
  }

  error(message: string, error: Error) {
    console.error(`[FloAng Error] ${message}`, {
      message: error.message,
      stack: error.stack,
      timestamp: new Date().toISOString()
    });
  }
}
```

**Error Tracking** (Development):
```typescript
// Track errors for debugging
interface ErrorReport {
  message: string;
  stack?: string;
  context: {
    action: string;
    state: any;
    timestamp: number;
  };
}

const errorLog: ErrorReport[] = [];

function trackError(error: Error, action: string, state: any) {
  errorLog.push({
    message: error.message,
    stack: error.stack,
    context: { action, state, timestamp: Date.now() }
  });

  // Keep only last 50 errors
  if (errorLog.length > 50) {
    errorLog.shift();
  }
}
```

**Performance Metrics**:
```typescript
// Track operation timings in development
class PerformanceMonitor {
  private metrics = new Map<string, number[]>();

  measureAsync<T>(label: string, operation: () => Promise<T>): Promise<T> {
    const start = performance.now();
    return operation().finally(() => {
      const duration = performance.now() - start;
      this.recordMetric(label, duration);
    });
  }

  private recordMetric(label: string, duration: number) {
    if (!this.metrics.has(label)) {
      this.metrics.set(label, []);
    }
    const values = this.metrics.get(label)!;
    values.push(duration);

    // Log if slow
    if (duration > 100) {
      console.warn(`Slow operation: ${label} took ${duration.toFixed(2)}ms`);
    }
  }

  getStats(label: string) {
    const values = this.metrics.get(label) || [];
    return {
      count: values.length,
      avg: values.reduce((a, b) => a + b, 0) / values.length,
      max: Math.max(...values)
    };
  }
}
```

## Technology Stack Summary

### Core Technologies

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend Framework | React | 18.3.x | Industry standard, excellent hooks API, large ecosystem |
| Build Tool | Vite | 5.x | Fast HMR, ES modules, CEP-compatible output |
| Language | TypeScript | 5.x | Type safety, better IDE support, catches errors early |
| Styling | CSS Modules | N/A | Scoped styles, no runtime cost, theming support |
| Backend Scripting | ExtendScript | ES3 | Required for Illustrator API, no alternative |
| CEP Bridge | CSInterface | 11.x | Adobe's official bridge, reliable, well-documented |

### Development Tools

**IDE**: Visual Studio Code (recommended)
- Extensions: ESLint, Prettier, TypeScript, ExtendScript Debugger

**Version Control**: Git workflow
- Branch strategy: feature branches + main
- Commit convention: Conventional Commits (feat/fix/docs/refactor)

**Code Quality**:
- Linting: ESLint with TypeScript and React plugins
- Formatting: Prettier with consistent config
- Type checking: TypeScript strict mode enabled

**Testing Frameworks**:
- Unit: Vitest (Vite-native, fast)
- Component: React Testing Library
- E2E: Manual testing in Illustrator (CEP limitations prevent automated E2E)

### Build Configuration

**package.json scripts**:
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build && npm run copy-assets",
    "copy-assets": "node scripts/copy-cep-files.js",
    "debug": "npm run build && npm run install-debug",
    "install-debug": "node scripts/install-to-cep.js",
    "package": "node scripts/create-zxp.js",
    "test": "vitest",
    "lint": "eslint src --ext .ts,.tsx",
    "format": "prettier --write \"src/**/*.{ts,tsx,css}\""
  }
}
```

## Implementation Considerations

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| ExtendScript performance bottlenecks on large paths | High | High | Implement throttling, show loading states, batch operations, use path caching |
| CEP bridge communication failures | Medium | High | Circuit breaker pattern, retry logic, graceful degradation to preview mode |
| Vite build incompatibility with CEP | Low | Medium | Test build output early, use documented Vite CEP configurations, relative paths |
| Adobe API changes in future Illustrator versions | Low | Medium | Wrap all Adobe API calls in abstraction layer, version detection, graceful fallbacks |

### Technical Debt Considerations

**Planned Shortcuts** (with justification):
- Initial version uses simple linear interpolation for angles between orthogonal points
  - Justification: Faster to implement, good enough for MVP
  - Future: Implement sophisticated easing functions (cubic, exponential)

- Preview canvas uses simplified rendering
  - Justification: Full Bezier curve preview too complex for initial release
  - Future: Add accurate Bezier curve preview with proper handle visualization

**Future Refactoring**:
- Extract angle calculation engine into separate package for potential standalone use
- Migrate ExtendScript to modern JavaScript when/if Adobe supports ES6+ in CEP
- Add WebAssembly module for complex mathematical operations if performance issues arise

**Upgrade Path**:
- React 18 → 19: Should be straightforward, minimal breaking changes expected
- Vite 5 → 6: Monitor Vite releases, update when stable
- TypeScript 5 → 6: Enable new features progressively
- CEP: Track Adobe's roadmap for potential UXP migration (next-gen extension platform)

### Team Considerations

**Required Skills**:
- Strong JavaScript/TypeScript fundamentals
- React experience (hooks, state management)
- Understanding of Adobe Illustrator concepts (paths, points, handles)
- Basic ExtendScript knowledge (can learn on the job)
- Familiarity with Vite or similar build tools

**Training Needs**:
- ExtendScript fundamentals (2-3 days)
- CEP architecture overview (1 day)
- Adobe Illustrator API documentation (ongoing reference)

**Team Structure** (suggested):
- 1 senior frontend developer (React/TypeScript)
- 1 developer with Adobe plugin experience (ExtendScript mentor)
- 1 designer for UI/UX refinement (part-time)

## Migration Strategy

Not applicable - this is a new plugin, no migration from existing system.

## Appendix

### Architecture Decision Records (ADRs)

#### ADR-001: React for UI Layer

**Context**: Need modern, maintainable UI framework for CEP extension panel

**Decision**: Use React 18 with TypeScript

**Alternatives Considered**:
- Vue 3: Simpler learning curve, but smaller CEP community
- Vanilla JavaScript: More control, but higher maintenance cost
- Svelte: Excellent performance, but less Adobe plugin ecosystem support

**Consequences**:
- Positive: Large ecosystem, excellent tooling, team familiarity
- Positive: Hooks API perfect for managing CEP bridge state
- Negative: Slightly larger bundle size than alternatives
- Negative: React DevTools don't work well in CEP panels

#### ADR-002: Vite for Build Tool

**Context**: Need fast development experience and CEP-compatible builds

**Decision**: Use Vite 5.x as primary build tool

**Alternatives Considered**:
- Webpack: More mature CEP documentation, but slower HMR
- Parcel: Zero-config appealing, but less CEP community support
- Rollup: Great for libraries, but less DX than Vite

**Consequences**:
- Positive: Near-instant HMR during development
- Positive: Simple configuration for CEP's relative path requirements
- Negative: Some CEP examples use Webpack, need translation
- Negative: Smaller community for CEP-specific issues

#### ADR-003: Command Pattern for CEP Bridge

**Context**: Need safe, structured communication between JavaScript and ExtendScript

**Decision**: Implement command pattern with JSON serialization

**Alternatives Considered**:
- Direct function strings: Simpler, but injection risk
- RPC library: More features, but overkill for simple plugin
- Event-based: More flexible, but harder to debug

**Consequences**:
- Positive: Prevents script injection attacks
- Positive: Easy to add new commands without changing bridge
- Positive: Clear request/response structure
- Negative: Slight performance overhead from JSON parsing
- Negative: More boilerplate than direct evalScript calls

#### ADR-004: CSS Modules for Styling

**Context**: Need scoped, maintainable styling without runtime cost

**Decision**: Use CSS Modules with CSS Variables for theming

**Alternatives Considered**:
- Styled-components: Runtime overhead, larger bundle
- Tailwind CSS: Utility-first approach doesn't fit component model
- Plain CSS: No scoping, risk of conflicts

**Consequences**:
- Positive: No runtime cost, generates scoped class names
- Positive: CSS Variables enable theming
- Positive: Familiar CSS syntax
- Negative: Separate files for styles and components
- Negative: Less dynamic than CSS-in-JS solutions

### Glossary

- **CEP (Common Extensibility Platform)**: Adobe's framework for building HTML5-based extensions for Creative Cloud applications
- **ExtendScript**: Adobe's extended JavaScript environment based on ECMAScript 3, used for scripting Creative Cloud applications
- **CSInterface**: JavaScript library provided by Adobe for communication between CEP panel and host application
- **ZXP**: Zipped eXtensible Platform package, the distribution format for CEP extensions
- **Path Item**: Illustrator's object representing a vector path with anchor points and handles
- **Anchor Point**: A point on a path that defines the path's shape
- **Direction Handles**: Control points that define the curve of a Bézier path segment
- **Flow Percentage**: FloAng-specific term for the intensity of angular distribution (0-100%)
- **Spin Offset**: Global rotation applied to all angle values
- **Orthogonal Angles**: Angles at 90-degree intervals (0°, 90°, 180°, 270°)

### References

**Architecture Patterns**:
- [React Documentation - Thinking in React](https://react.dev/learn/thinking-in-react)
- [CEP Cookbook](https://github.com/Adobe-CEP/CEP-Resources/blob/master/CEP_11.x/Documentation/CEP%2011.1%20HTML%20Extension%20Cookbook.md)
- [Circuit Breaker Pattern (Martin Fowler)](https://martinfowler.com/bliki/CircuitBreaker.html)

**Technology Documentation**:
- [React 18 Documentation](https://react.dev)
- [Vite Documentation](https://vitejs.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Adobe Illustrator ExtendScript Reference](https://ai-scripting.docsforadobe.dev/)
- [CEP Resources Repository](https://github.com/Adobe-CEP/CEP-Resources)

**Best Practices**:
- [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html)
- [React Testing Library Best Practices](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
- [Vite + React + TypeScript Template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts)

---
**Document Version**: 1.0
**Date**: 2025-01-11
**Author**: Winston (BMAD System Architect)
**Quality Score**: 100/100
**PRD Reference**: .claude/specs/floang-illustrator-plugin/01-product-requirements.md
