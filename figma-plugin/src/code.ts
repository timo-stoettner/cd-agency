// CD Agency Figma Plugin — Main Thread (Figma Sandbox)
// This file runs in Figma's sandbox and has access to the Figma Plugin API.
// It communicates with the UI thread (iframe) via postMessage.

const PLUGIN_WIDTH = 360;
const PLUGIN_HEIGHT = 520;

// Show the plugin UI
figma.showUI(__html__, {
  width: PLUGIN_WIDTH,
  height: PLUGIN_HEIGHT,
  themeColors: true,
  title: "CD Agency",
});

// -------------------------------------------------------------------
// Helpers
// -------------------------------------------------------------------

interface SelectionInfo {
  type: "selection";
  text: string;
  nodeId: string;
  nodeName: string;
  layerContext: string; // parent frame name for contextual hints
}

interface NoSelectionInfo {
  type: "no-selection";
  reason: string;
}

function getSelectedTextInfo(): SelectionInfo | NoSelectionInfo {
  const selection = figma.currentPage.selection;

  if (selection.length === 0) {
    return { type: "no-selection", reason: "No layer selected. Select a text layer to get started." };
  }

  if (selection.length > 1) {
    return { type: "no-selection", reason: "Multiple layers selected. Please select a single text layer." };
  }

  const node = selection[0];

  if (node.type !== "TEXT") {
    return { type: "no-selection", reason: `Selected layer is a ${node.type}. Please select a text layer.` };
  }

  const textNode = node as TextNode;
  const parentName = textNode.parent && "name" in textNode.parent ? textNode.parent.name : "";

  return {
    type: "selection",
    text: textNode.characters,
    nodeId: textNode.id,
    nodeName: textNode.name,
    layerContext: parentName,
  };
}

// Send current selection to UI on launch
function sendSelectionToUI() {
  const info = getSelectedTextInfo();
  figma.ui.postMessage(info);
}

// -------------------------------------------------------------------
// Listen for selection changes
// -------------------------------------------------------------------

figma.on("selectionchange", () => {
  sendSelectionToUI();
});

// Send initial selection
sendSelectionToUI();

// -------------------------------------------------------------------
// Listen for messages from the UI
// -------------------------------------------------------------------

figma.ui.onmessage = async (msg: { type: string; [key: string]: any }) => {
  switch (msg.type) {
    case "get-selection": {
      sendSelectionToUI();
      break;
    }

    case "apply-text": {
      // Replace selected text node content with the new text
      const { text, nodeId } = msg;
      const node = figma.getNodeById(nodeId);

      if (!node || node.type !== "TEXT") {
        figma.ui.postMessage({
          type: "apply-error",
          error: "Original text layer no longer exists or is not a text node.",
        });
        return;
      }

      const textNode = node as TextNode;

      // Load all fonts used in the text node before modifying
      const fonts = textNode.getRangeAllFontNames(0, textNode.characters.length);
      for (const font of fonts) {
        await figma.loadFontAsync(font);
      }

      textNode.characters = text;

      figma.ui.postMessage({ type: "apply-success", text });
      figma.notify("Text updated successfully.");
      break;
    }

    case "resize": {
      const { width, height } = msg;
      figma.ui.resize(
        Math.max(300, Math.min(600, width)),
        Math.max(400, Math.min(800, height)),
      );
      break;
    }

    case "notify": {
      figma.notify(msg.message, { timeout: msg.timeout || 2000 });
      break;
    }

    case "close": {
      figma.closePlugin();
      break;
    }

    default:
      break;
  }
};
