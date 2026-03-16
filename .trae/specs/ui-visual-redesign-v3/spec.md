# UI Visual Redesign V3 Spec

## Why
User feedback indicates a need for a "beautiful, simple, and pretty" interface with a strong emphasis on user experience. The current UI, while functional, lacks the high-end polish and cohesive aesthetic of modern consumer apps (e.g., iOS Shortcuts, Linear, or high-quality Fintech apps).

## What Changes
- **Visual Language Overhaul**:
  - **Style**: Adoption of a "Soft Minimalist" aesthetic with subtle glassmorphism (blur effects), mesh gradients, and generous whitespace.
  - **Typography**: Refined type scale using Inter with tighter tracking for headings and improved readability for data.
  - **Color**: Refined Indigo/Violet palette to be softer (pastel tones for backgrounds) yet vibrant for actions.
  - **Radius**: Increased border-radius (24px for cards, full pill shape for buttons) for a friendlier feel.

- **Login/Auth Experience**:
  - **Redesign**: Move from a simple centered card to a **Split Layout** (Desktop) or **Immersive Gradient** (Mobile).
  - **Details**: Animated entrance, floating labels, and brand illustration placeholder.

- **Component Redesign**:
  - **Navigation**:
    - **Sidebar**: Floating glass effect, detached from the edge (Desktop).
    - **Bottom Bar**: Blur background (`backdrop-filter: blur(20px)`), removing solid borders.
  - **Cards**: Remove visible borders, rely on soft shadows (`box-shadow`) and surface colors.
  - **Lists**: "Inset Grouped" style (like iOS Settings) for all lists (Transactions, Settings, Family).
  - **Inputs**: Modern "Filled" or "Soft Outline" style with floating focus states.

- **Feature-Specific UI Updates**:
  - **Dashboard**: "Overview Card" gets a mesh gradient background. Stats are presented in a clean grid without heavy borders.
  - **Transactions**: Category icons get distinct colorful backgrounds (squircle shape). Amount display emphasizes legibility.
  - **Budget**: Progress bars become thicker, rounder, and use gradient fills.

## Impact
- Affected specs: `ui-optimization-frontend` (superseded).
- Affected code: `frontend/index.html` (CSS & HTML structure).

## ADDED Requirements
### Requirement: Glassmorphism Navigation
Navigation bars SHALL use `backdrop-filter: blur()` to provide context of content scrolling underneath.

### Requirement: Immersive Auth Page
The login page SHALL feature a rich visual background (gradient/pattern) and a polished form container with high elevation.

### Requirement: Micro-interactions
Interactive elements (Buttons, Cards, List Items) SHALL have distinct hover (lift) and active (scale down) states.

## MODIFIED Requirements
### Requirement: Refined Color System
Replace current utility colors with a semantic "Surface System" (Surface 1, Surface 2, Surface 3) to handle depth and hierarchy better than simple borders.

## REMOVED Requirements
### Requirement: Solid Borders
**Reason**: Heavy borders create visual noise.
**Migration**: Replace with shadows and background color differentiation.
