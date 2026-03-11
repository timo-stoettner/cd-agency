import * as vscode from "vscode";
import * as api from "../api";
import { createScorePanel } from "../webview";

/**
 * Command handler: Score the currently selected text for readability,
 * accessibility, and lint quality.
 */
export async function scoreSelectionCommand(): Promise<void> {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    vscode.window.showWarningMessage("CD Agency: No active editor found.");
    return;
  }

  const selection = editor.selection;
  const selectedText = editor.document.getText(selection);

  if (!selectedText.trim()) {
    vscode.window.showWarningMessage(
      "CD Agency: Select some text to score."
    );
    return;
  }

  const result = await vscode.window.withProgress(
    {
      location: vscode.ProgressLocation.Notification,
      title: "CD Agency: Scoring selection...",
      cancellable: false,
    },
    async () => {
      try {
        return await api.scoreText(selectedText);
      } catch (err) {
        const message = err instanceof Error ? err.message : String(err);
        vscode.window.showErrorMessage(message);
        return undefined;
      }
    }
  );

  if (!result) {
    return;
  }

  // For a brief result, use an information message; for detailed results, open
  // a webview panel.
  if (result.issues.length === 0 && result.scores.length <= 3) {
    const summary = result.scores
      .map((s) => `${s.name}: ${s.grade} (${s.score}/10)`)
      .join("  |  ");
    vscode.window.showInformationMessage(
      `CD Agency Score: ${result.overall}/10 — ${summary}`
    );
  } else {
    createScorePanel(result, selectedText);
  }
}
