# CD Agency Figma Plugin

A Figma plugin that connects text layers to the Content Design Agency, allowing designers to run agents directly on UI copy without leaving Figma.

## Features

- **Select & Run**: Select any text layer, pick an agent, get improved copy
- **Auto-suggest**: Plugin suggests the best agent based on your text content
- **Design System Presets**: Apply Material Design, Polaris, Atlassian, or Apple HIG voice guidelines
- **One-click Apply**: Replace text layer content with improved copy directly
- **Scoring**: See readability grade, a11y compliance, and lint results inline
- **History**: Recent runs saved per-file for reference

## Prerequisites

You need the CD Agency API backend running. See `api/` in the project root.

```bash
# Start the API server
pip install fastapi uvicorn
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

## Build & Install

```bash
cd figma-plugin
npm install
npm run build
```

Then in Figma:
1. Go to **Plugins > Development > Import plugin from manifest**
2. Select `figma-plugin/manifest.json`
3. The plugin appears under **Plugins > Development > CD Agency**

## Usage

1. Select a text layer in your Figma design
2. Right-click > **Plugins > CD Agency** (or use the keyboard shortcut)
3. Configure the API URL on first use (default: `http://localhost:8000`)
4. Choose an agent from the dropdown (or use the auto-suggestion)
5. Optionally select a design system preset
6. Click **Run Agent**
7. Review the suggestion, then **Apply** to update the text layer or **Copy** to clipboard

## Development

```bash
npm run watch    # Build + watch for changes
```

## Plugin Screens

### Agent Picker
- Shows detected text from selected layer
- Agent dropdown with auto-suggestion
- Design system preset selector

### Results
- Before/after comparison
- Score badges (readability grade, a11y pass/fail)
- Apply and Copy buttons
- Run Another Agent option
