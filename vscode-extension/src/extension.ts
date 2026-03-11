import * as vscode from "vscode";
import { runAgentCommand } from "./commands/runAgent";
import { scoreSelectionCommand } from "./commands/scoreSelection";
import { listAgentsCommand } from "./commands/listAgents";
import { updateDiagnostics } from "./diagnostics";

/** Debounce timer handle for auto-lint on document change. */
let lintTimer: ReturnType<typeof setTimeout> | undefined;

/** How long (ms) to wait after the last keystroke before linting. */
const LINT_DEBOUNCE_MS = 800;

/**
 * Called by VS Code when the extension is activated.
 *
 * Registers all commands, sets up the diagnostics collection for inline
 * content linting, and creates the status bar item.
 */
export function activate(context: vscode.ExtensionContext): void {
  // -----------------------------------------------------------------------
  // Diagnostics collection for inline content lint warnings
  // -----------------------------------------------------------------------
  const diagnosticCollection =
    vscode.languages.createDiagnosticCollection("cd-agency");
  context.subscriptions.push(diagnosticCollection);

  // -----------------------------------------------------------------------
  // Register commands
  // -----------------------------------------------------------------------
  context.subscriptions.push(
    vscode.commands.registerCommand(
      "cd-agency.runAgent",
      runAgentCommand
    )
  );

  context.subscriptions.push(
    vscode.commands.registerCommand(
      "cd-agency.scoreSelection",
      scoreSelectionCommand
    )
  );

  context.subscriptions.push(
    vscode.commands.registerCommand(
      "cd-agency.listAgents",
      listAgentsCommand
    )
  );

  context.subscriptions.push(
    vscode.commands.registerCommand("cd-agency.configure", () => {
      vscode.commands.executeCommand(
        "workbench.action.openSettings",
        "cdAgency"
      );
    })
  );

  // -----------------------------------------------------------------------
  // Status bar item — shows "CD Agency" and opens the agent picker on click
  // -----------------------------------------------------------------------
  const statusBarItem = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Right,
    100
  );
  statusBarItem.text = "$(edit) CD Agency";
  statusBarItem.tooltip = "CD Agency — Content Design Agents";
  statusBarItem.command = "cd-agency.listAgents";
  statusBarItem.show();
  context.subscriptions.push(statusBarItem);

  // -----------------------------------------------------------------------
  // Auto-lint on document change (if autoLint is enabled)
  // -----------------------------------------------------------------------

  // Lint the active document on activation so issues show immediately.
  if (vscode.window.activeTextEditor) {
    triggerLint(vscode.window.activeTextEditor.document, diagnosticCollection);
  }

  // Re-lint when the user switches to a different file.
  context.subscriptions.push(
    vscode.window.onDidChangeActiveTextEditor((editor) => {
      if (editor) {
        triggerLint(editor.document, diagnosticCollection);
      }
    })
  );

  // Re-lint (debounced) as the user types.
  context.subscriptions.push(
    vscode.workspace.onDidChangeTextDocument((event) => {
      if (event.document === vscode.window.activeTextEditor?.document) {
        debouncedLint(event.document, diagnosticCollection);
      }
    })
  );

  // Clear diagnostics for closed documents.
  context.subscriptions.push(
    vscode.workspace.onDidCloseTextDocument((document) => {
      diagnosticCollection.delete(document.uri);
    })
  );
}

/**
 * Called by VS Code when the extension is deactivated.
 */
export function deactivate(): void {
  if (lintTimer !== undefined) {
    clearTimeout(lintTimer);
    lintTimer = undefined;
  }
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Run lint immediately (used on activation and when switching editors).
 */
function triggerLint(
  document: vscode.TextDocument,
  diagnosticCollection: vscode.DiagnosticCollection
): void {
  const config = vscode.workspace.getConfiguration("cdAgency");
  if (!config.get<boolean>("autoLint", true)) {
    return;
  }

  updateDiagnostics(document, diagnosticCollection).catch(() => {
    // Silently ignore — the diagnostics module already handles errors.
  });
}

/**
 * Schedule a lint run after the debounce period. Resets the timer on every
 * call so that rapid typing does not trigger excessive API requests.
 */
function debouncedLint(
  document: vscode.TextDocument,
  diagnosticCollection: vscode.DiagnosticCollection
): void {
  if (lintTimer !== undefined) {
    clearTimeout(lintTimer);
  }

  lintTimer = setTimeout(() => {
    lintTimer = undefined;
    triggerLint(document, diagnosticCollection);
  }, LINT_DEBOUNCE_MS);
}
