"""Preset endpoints — list and detail for design system voice profiles."""

from __future__ import annotations

from typing import Annotated

import yaml
from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import PRESETS_DIR, verify_api_key
from api.models import PresetDetail, PresetSummary

router = APIRouter(prefix="/presets", tags=["presets"])


def _load_preset_files() -> dict[str, dict]:
    """Load all YAML preset files from the presets/ directory."""
    presets: dict[str, dict] = {}
    if not PRESETS_DIR.is_dir():
        return presets

    for path in sorted(PRESETS_DIR.glob("*.yaml")):
        with open(path) as f:
            data = yaml.safe_load(f) or {}
        data["_filename"] = path.stem
        name = data.get("name", path.stem)
        presets[path.stem] = data
    return presets


@router.get("", response_model=list[PresetSummary])
async def list_presets(
    _auth: Annotated[str | None, Depends(verify_api_key)] = None,
) -> list[PresetSummary]:
    """List all available design system presets."""
    presets = _load_preset_files()
    return [
        PresetSummary(
            name=data.get("name", filename),
            filename=filename,
        )
        for filename, data in presets.items()
    ]


@router.get("/{name}", response_model=PresetDetail)
async def get_preset(
    name: str,
    _auth: Annotated[str | None, Depends(verify_api_key)] = None,
) -> PresetDetail:
    """Get full details for a design system preset by filename stem."""
    presets = _load_preset_files()

    # Look up by filename stem first, then by display name
    data = presets.get(name)
    if data is None:
        for _filename, pdata in presets.items():
            if pdata.get("name", "").lower() == name.lower():
                data = pdata
                break

    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Preset '{name}' not found",
        )

    return PresetDetail(
        name=data.get("name", data.get("_filename", name)),
        filename=data.get("_filename", name),
        tone_descriptors=data.get("tone_descriptors", []),
        do_rules=data.get("do", []),
        dont_rules=data.get("dont", []),
        sample_content=data.get("sample_content", []),
        character_limits=data.get("character_limits", {}),
        terminology=data.get("terminology", {}),
    )
