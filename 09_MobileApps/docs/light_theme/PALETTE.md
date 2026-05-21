# Coral AI Color Palette

All colors used by the app, organized by semantic role. Status colors (Healthy / Bleached / Dead) and the primary aqua are identical across both themes — they carry meaning, not just style.

## Brand & status (shared across themes)

| Token | Hex | Notes |
|---|---|---|
| `primary` | `#00F5D4` | Aqua brand color |
| `primaryFixedDim` | `#00DFC1` (dark) / `#00A88E` (light) | Slightly darker variant — light theme uses much darker shade for AA contrast on white |
| `healthy` | `#4ADE80` | Healthy coral status |
| `bleached` | `#FBBF24` | Bleached coral status |
| `dead` | `#F87171` | Dead coral status |

## Dark theme (existing)

| Token | Hex |
|---|---|
| `background` | `#0E0E0E` |
| `surface` | `#1A1A1A` |
| `surfaceElevated` | `#2B2B2B` |
| `surfaceContainerLowest` | `#0E0E0E` |
| `surfaceContainer` | `#201F1F` |
| `surfaceContainerHigh` | `#2A2A2A` |
| `onBackground` | `#E5E2E1` |
| `onPrimary` | `#006C5C` |
| `textMuted` | `#A1A1AA` |
| `divider` | `#27272A` |
| `outline` | `#83948F` |

## Light theme (new, soft cream)

| Token | Hex |
|---|---|
| `background` | `#F8F9FA` |
| `surface` | `#FFFFFF` |
| `surfaceElevated` | `#F1F5F9` |
| `surfaceContainerLowest` | `#F8F9FA` |
| `surfaceContainer` | `#FFFFFF` |
| `surfaceContainerHigh` | `#E5E7EB` |
| `onBackground` | `#1A1A1A` |
| `onPrimary` | `#003D33` |
| `textMuted` | `#6B7280` |
| `divider` | `#E5E7EB` |
| `outline` | `#9CA3AF` |

## Glass / overlay tokens

These replace hardcoded `Colors.white.withValues(...)` and `Colors.black.withValues(...)` literals.

| Token | Dark | Light |
|---|---|---|
| `glassThin` | white 5% | black 4% |
| `glassMid` | white 10% | black 8% |
| `glassStrong` | white 20% | black 12% |
| `dim` | white 40% | black 40% |
| `bright` | white 80% | black 80% |

## Hero gradient & scrim

| Token | Dark | Light |
|---|---|---|
| `scrim` | `#CC000000` (80% black) | `#CC000000` (kept dark — hero photos need dark scrim for white text) |
| `heroGradientStart` | `transparent` | `transparent` |
| `heroGradientEnd` | `#FF0E0E0E` | `#F2F8F9FA` (matches cream background) |
