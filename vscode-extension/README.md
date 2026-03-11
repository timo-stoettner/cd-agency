# CD Agency -- Content Design (VS Code Extension)

AI-powered content design agents for UX writing, inline linting, and content quality scoring -- right inside VS Code.

## Features

- **Inline Content Linting** -- Automatically detects UI strings in JS/TS/JSX/TSX/JSON files and shows lint warnings as squiggly underlines directly in the editor.
- **Run Agent on Selection** -- Select text, pick a content design agent (error messages, microcopy, CTAs, etc.), and see a before/after comparison in a side panel with one-click apply.
- **Score Selected Text** -- Get readability, accessibility, and lint scores for any selected text.
- **Agent Browser** -- Browse all 15 available content design agents with descriptions and tags.
- **Status Bar Integration** -- Quick access to the agent picker from the status bar.

## Requirements

- VS Code 1.85.0 or later
- The `cd-agency` Python package installed and its API server running (default: `http://localhost:8100`)

## Setup

1. Install the extension (see "Build from Source" below, or install from a `.vsix` file).
2. Start the CD Agency API server:
   ```bash
   cd-agency serve
   ```
3. Open a project in VS Code. The extension activates automatically for all languages.

## Commands

Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and type "CD Agency":

| Command | Description | Keybinding |
|---------|-------------|------------|
| **CD Agency: Run Agent on Selection** | Run a content design agent on selected text | `Ctrl+Shift+A` / `Cmd+Shift+A` |
| **CD Agency: Score Selected Text** | Show readability, a11y, and lint scores | -- |
| **CD Agency: List Available Agents** | Browse all agents in a QuickPick | -- |
| **CD Agency: Configure** | Open extension settings | -- |

## Configuration

Add these to your `settings.json` or configure via the Settings UI:

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `cdAgency.apiUrl` | `string` | `http://localhost:8100` | Base URL for the CD Agency API server |
| `cdAgency.defaultPreset` | `string` | `material-design` | Design system voice preset (`material-design`, `polaris`, `atlassian`, `apple-hig`) |
| `cdAgency.autoLint` | `boolean` | `true` | Automatically lint string literals as you type |

### Example

```json
{
  "cdAgency.apiUrl": "http://localhost:8100",
  "cdAgency.defaultPreset": "polaris",
  "cdAgency.autoLint": true
}
```

## How It Works

The extension communicates with the CD Agency API server over HTTP. It:

1. **Extracts string literals** from your code using lightweight regex-based heuristics.
2. **Sends them to the lint API** to check for common UX writing issues (passive voice, "click here", overly long button text, etc.).
3. **Displays diagnostics** as native VS Code warnings/errors with squiggly underlines.
4. **Runs agents** on demand, showing results in themed webview panels with before/after comparisons.

## Build from Source

```bash
# Navigate to the extension directory
cd vscode-extension

# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Package as .vsix
npm run package

# Install the packaged extension
code --install-extension cd-agency-0.1.0.vsix
```

### Development

```bash
# Watch mode (recompile on changes)
npm run watch

# To test: open this folder in VS Code, press F5 to launch Extension Development Host
```

## Architecture

```
src/
  extension.ts          Main entry point (activate/deactivate)
  api.ts                HTTP client for the CD Agency API
  diagnostics.ts        Inline linting via DiagnosticCollection
  webview.ts            Webview panels for agent results and scores
  commands/
    runAgent.ts         "Run Agent on Selection" command
    scoreSelection.ts   "Score Selected Text" command
    listAgents.ts       "List Available Agents" command
```

## License

MIT
