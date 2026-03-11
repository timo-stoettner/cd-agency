import * as vscode from "vscode";
import type { AgentResult, ScoreResult } from "./api";

/** Escape HTML entities to avoid XSS when injecting user content. */
function escapeHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

/**
 * Create a webview panel that shows agent results with a before/after
 * comparison and an "Apply" button that replaces the original selection.
 */
export function createResultPanel(
  result: AgentResult,
  editor: vscode.TextEditor,
  selection: vscode.Selection
): vscode.WebviewPanel {
  const panel = vscode.window.createWebviewPanel(
    "cdAgencyResult",
    `CD Agency: ${result.agent}`,
    vscode.ViewColumn.Beside,
    { enableScripts: true }
  );

  panel.webview.html = getResultHtml(result);

  // Handle messages from the webview (e.g. "Apply" button click).
  panel.webview.onDidReceiveMessage(async (message: { command: string }) => {
    if (message.command === "apply") {
      const success = await editor.edit((editBuilder) => {
        editBuilder.replace(selection, result.suggestion);
      });
      if (success) {
        vscode.window.showInformationMessage(
          "CD Agency: Suggestion applied."
        );
        panel.dispose();
      } else {
        vscode.window.showErrorMessage(
          "CD Agency: Could not apply suggestion — the editor may have changed."
        );
      }
    }
  });

  return panel;
}

/**
 * Create a webview panel that shows scoring results.
 */
export function createScorePanel(
  result: ScoreResult,
  originalText: string
): vscode.WebviewPanel {
  const panel = vscode.window.createWebviewPanel(
    "cdAgencyScore",
    "CD Agency: Score",
    vscode.ViewColumn.Beside,
    { enableScripts: false }
  );

  panel.webview.html = getScoreHtml(result, originalText);
  return panel;
}

// ---------------------------------------------------------------------------
// HTML generators
// ---------------------------------------------------------------------------

function getResultHtml(result: AgentResult): string {
  return /* html */ `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>CD Agency Result</title>
  <style>
    ${getBaseStyles()}
    .comparison {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin: 16px 0;
    }
    .panel {
      background: var(--vscode-editor-background, #1e1e1e);
      border: 1px solid var(--vscode-panel-border, #333);
      border-radius: 6px;
      padding: 12px;
    }
    .panel h3 {
      margin: 0 0 8px;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      opacity: 0.7;
    }
    .panel pre {
      white-space: pre-wrap;
      word-wrap: break-word;
      margin: 0;
      font-family: var(--vscode-editor-font-family, monospace);
      font-size: var(--vscode-editor-font-size, 13px);
      line-height: 1.5;
    }
    .explanation {
      margin: 16px 0;
      padding: 12px;
      background: var(--vscode-textBlockQuote-background, #222);
      border-left: 3px solid var(--vscode-textLink-foreground, #3794ff);
      border-radius: 0 6px 6px 0;
    }
    .actions {
      margin-top: 16px;
      display: flex;
      gap: 8px;
    }
    button {
      padding: 8px 16px;
      font-size: 13px;
      cursor: pointer;
      border: none;
      border-radius: 4px;
      font-family: var(--vscode-font-family, sans-serif);
    }
    button.primary {
      background: var(--vscode-button-background, #0e639c);
      color: var(--vscode-button-foreground, #fff);
    }
    button.primary:hover {
      background: var(--vscode-button-hoverBackground, #1177bb);
    }
  </style>
</head>
<body>
  <h2>Agent: ${escapeHtml(result.agent)}</h2>

  <div class="comparison">
    <div class="panel">
      <h3>Before</h3>
      <pre>${escapeHtml(result.original)}</pre>
    </div>
    <div class="panel">
      <h3>After</h3>
      <pre>${escapeHtml(result.suggestion)}</pre>
    </div>
  </div>

  <div class="explanation">
    <strong>Explanation:</strong> ${escapeHtml(result.explanation)}
  </div>

  <div class="actions">
    <button class="primary" id="applyBtn">Apply Suggestion</button>
  </div>

  <script>
    const vscode = acquireVsCodeApi();
    document.getElementById('applyBtn').addEventListener('click', () => {
      vscode.postMessage({ command: 'apply' });
    });
  </script>
</body>
</html>`;
}

function getScoreHtml(result: ScoreResult, originalText: string): string {
  const scoreRows = result.scores
    .map(
      (s) => /* html */ `
      <tr>
        <td><strong>${escapeHtml(s.name)}</strong></td>
        <td>${s.score}/10</td>
        <td>${escapeHtml(s.grade)}</td>
        <td>${escapeHtml(s.details)}</td>
      </tr>`
    )
    .join("");

  const issueRows = result.issues
    .map(
      (i) => /* html */ `
      <tr>
        <td class="severity-${i.severity}">${i.severity}</td>
        <td>${escapeHtml(i.rule)}</td>
        <td>${escapeHtml(i.message)}</td>
        <td>${i.suggestion ? escapeHtml(i.suggestion) : "—"}</td>
      </tr>`
    )
    .join("");

  const overallPercent = Math.round(result.overall * 10);

  return /* html */ `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>CD Agency Score</title>
  <style>
    ${getBaseStyles()}
    .overall {
      font-size: 28px;
      font-weight: bold;
      margin: 16px 0;
    }
    .bar {
      height: 10px;
      background: var(--vscode-panel-border, #333);
      border-radius: 5px;
      overflow: hidden;
      margin-bottom: 24px;
    }
    .bar-fill {
      height: 100%;
      border-radius: 5px;
      background: var(--vscode-charts-green, #4caf50);
      width: ${overallPercent}%;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 12px 0;
    }
    th, td {
      text-align: left;
      padding: 6px 10px;
      border-bottom: 1px solid var(--vscode-panel-border, #333);
      font-size: 13px;
    }
    th { opacity: 0.7; font-weight: 600; }
    .severity-error { color: var(--vscode-errorForeground, #f44); }
    .severity-warning { color: var(--vscode-editorWarning-foreground, #fa4); }
    .severity-info { color: var(--vscode-editorInfo-foreground, #3af); }
    .text-preview {
      background: var(--vscode-editor-background, #1e1e1e);
      border: 1px solid var(--vscode-panel-border, #333);
      border-radius: 6px;
      padding: 12px;
      white-space: pre-wrap;
      font-family: var(--vscode-editor-font-family, monospace);
      font-size: var(--vscode-editor-font-size, 13px);
      margin-bottom: 16px;
    }
  </style>
</head>
<body>
  <h2>Content Score</h2>

  <div class="text-preview">${escapeHtml(originalText)}</div>

  <div class="overall">${result.overall}/10</div>
  <div class="bar"><div class="bar-fill"></div></div>

  <h3>Scores</h3>
  <table>
    <thead>
      <tr><th>Metric</th><th>Score</th><th>Grade</th><th>Details</th></tr>
    </thead>
    <tbody>${scoreRows}</tbody>
  </table>

  ${
    result.issues.length > 0
      ? /* html */ `
  <h3>Issues (${result.issues.length})</h3>
  <table>
    <thead>
      <tr><th>Severity</th><th>Rule</th><th>Message</th><th>Suggestion</th></tr>
    </thead>
    <tbody>${issueRows}</tbody>
  </table>`
      : "<p>No issues found.</p>"
  }
</body>
</html>`;
}

/** Shared CSS that picks up VS Code theme variables. */
function getBaseStyles(): string {
  return `
    body {
      font-family: var(--vscode-font-family, -apple-system, BlinkMacSystemFont, sans-serif);
      font-size: var(--vscode-font-size, 13px);
      color: var(--vscode-foreground, #ccc);
      background: var(--vscode-editor-background, #1e1e1e);
      padding: 16px;
      margin: 0;
    }
    h2 {
      margin: 0 0 12px;
      font-size: 18px;
      font-weight: 600;
    }
    h3 {
      margin: 20px 0 8px;
      font-size: 14px;
      font-weight: 600;
    }
  `;
}
