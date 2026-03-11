import * as vscode from "vscode";
import * as api from "../api";

/**
 * Command handler: List all available CD Agency agents in a QuickPick.
 * Selecting an agent copies its name to the clipboard for convenience.
 */
export async function listAgentsCommand(): Promise<void> {
  let agents: api.Agent[];
  try {
    agents = await api.listAgents();
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    vscode.window.showErrorMessage(message);
    return;
  }

  if (agents.length === 0) {
    vscode.window.showInformationMessage("CD Agency: No agents available.");
    return;
  }

  const picked = await vscode.window.showQuickPick(
    agents.map((a) => ({
      label: a.name,
      description: a.description,
      detail: `Tags: ${a.tags.join(", ")}`,
    })),
    {
      placeHolder: `${agents.length} agents available — select to copy name`,
      matchOnDescription: true,
      matchOnDetail: true,
    }
  );

  if (picked) {
    await vscode.env.clipboard.writeText(picked.label);
    vscode.window.showInformationMessage(
      `CD Agency: Copied "${picked.label}" to clipboard.`
    );
  }
}
