import * as vscode from "vscode";

/** Describes a single CD Agency agent. */
export interface Agent {
  name: string;
  description: string;
  tags: string[];
}

/** Result returned after running an agent on text. */
export interface AgentResult {
  agent: string;
  original: string;
  suggestion: string;
  explanation: string;
}

/** Individual score entry. */
export interface ScoreEntry {
  name: string;
  score: number;
  grade: string;
  details: string;
}

/** Full scoring result for a piece of text. */
export interface ScoreResult {
  overall: number;
  scores: ScoreEntry[];
  issues: LintIssue[];
}

/** A single lint issue found in content. */
export interface LintIssue {
  rule: string;
  message: string;
  severity: "error" | "warning" | "info";
  offset: number;
  length: number;
  suggestion?: string;
}

/** Design system preset definition. */
export interface Preset {
  name: string;
  displayName: string;
  description: string;
}

function getApiUrl(): string {
  const config = vscode.workspace.getConfiguration("cdAgency");
  return config.get<string>("apiUrl", "http://localhost:8100");
}

function getDefaultPreset(): string {
  const config = vscode.workspace.getConfiguration("cdAgency");
  return config.get<string>("defaultPreset", "material-design");
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const baseUrl = getApiUrl();
  const url = `${baseUrl}${path}`;

  let response: Response;
  try {
    response = await fetch(url, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
  } catch (err) {
    const message =
      err instanceof Error ? err.message : "Unknown network error";
    throw new Error(
      `Failed to connect to CD Agency API at ${baseUrl}. ` +
        `Ensure the server is running. (${message})`
    );
  }

  if (!response.ok) {
    let detail = "";
    try {
      const body = (await response.json()) as { error?: string };
      detail = body.error ?? "";
    } catch {
      // body wasn't JSON — ignore
    }
    throw new Error(
      `CD Agency API error ${response.status}: ${detail || response.statusText}`
    );
  }

  return (await response.json()) as T;
}

/** Fetch the list of available agents. */
export async function listAgents(): Promise<Agent[]> {
  return request<Agent[]>("/api/agents");
}

/** Run an agent on the given text. */
export async function runAgent(
  agentName: string,
  text: string
): Promise<AgentResult> {
  const preset = getDefaultPreset();
  return request<AgentResult>("/api/agents/run", {
    method: "POST",
    body: JSON.stringify({ agent: agentName, text, preset }),
  });
}

/** Score a piece of text (readability, a11y, lint). */
export async function scoreText(text: string): Promise<ScoreResult> {
  const preset = getDefaultPreset();
  return request<ScoreResult>("/api/score", {
    method: "POST",
    body: JSON.stringify({ text, preset }),
  });
}

/** Lint a piece of text and return issues. */
export async function lintText(text: string): Promise<LintIssue[]> {
  return request<LintIssue[]>("/api/lint", {
    method: "POST",
    body: JSON.stringify({ text }),
  });
}

/** Fetch available design system presets. */
export async function getPresets(): Promise<Preset[]> {
  return request<Preset[]>("/api/presets");
}
