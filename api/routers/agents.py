"""Agent endpoints — list, detail, search, and run."""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.deps import get_registry, get_runner, verify_api_key
from api.models import AgentDetail, AgentInputSchema, AgentOutputSchema, AgentRunRequest, AgentRunResponse, AgentSummary
from runtime.registry import AgentRegistry
from runtime.runner import AgentRunner

router = APIRouter(prefix="/agents", tags=["agents"])


def _agent_to_summary(agent: Any) -> AgentSummary:
    return AgentSummary(
        slug=agent.slug,
        name=agent.name,
        description=agent.description,
        tags=agent.tags,
    )


def _agent_to_detail(agent: Any) -> AgentDetail:
    return AgentDetail(
        slug=agent.slug,
        name=agent.name,
        description=agent.description,
        tags=agent.tags,
        inputs=[
            AgentInputSchema(
                name=i.name,
                type=i.type,
                required=i.required,
                description=i.description,
            )
            for i in agent.inputs
        ],
        outputs=[
            AgentOutputSchema(
                name=o.name,
                type=o.type,
                description=o.description,
            )
            for o in agent.outputs
        ],
        related_agents=agent.related_agents,
        version=agent.version,
        difficulty_level=agent.difficulty_level,
    )


@router.get("/search", response_model=list[AgentSummary])
async def search_agents(
    q: Annotated[str, Query(min_length=1, description="Search query")],
    registry: Annotated[AgentRegistry, Depends(get_registry)],
    _auth: Annotated[str | None, Depends(verify_api_key)] = None,
) -> list[AgentSummary]:
    """Search agents by name, description, or tags."""
    results = registry.search(q)
    return [_agent_to_summary(a) for a in results]


@router.get("", response_model=list[AgentSummary])
async def list_agents(
    registry: Annotated[AgentRegistry, Depends(get_registry)],
    _auth: Annotated[str | None, Depends(verify_api_key)] = None,
) -> list[AgentSummary]:
    """List all available agents."""
    agents = registry.list_all()
    return [_agent_to_summary(a) for a in agents]


@router.get("/{slug}", response_model=AgentDetail)
async def get_agent(
    slug: str,
    registry: Annotated[AgentRegistry, Depends(get_registry)],
    _auth: Annotated[str | None, Depends(verify_api_key)] = None,
) -> AgentDetail:
    """Get full details for a single agent by slug."""
    agent = registry.get(slug)
    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{slug}' not found",
        )
    return _agent_to_detail(agent)


@router.post("/{slug}/run", response_model=AgentRunResponse)
async def run_agent(
    slug: str,
    body: AgentRunRequest,
    registry: Annotated[AgentRegistry, Depends(get_registry)],
    runner: Annotated[AgentRunner, Depends(get_runner)],
    _auth: Annotated[str | None, Depends(verify_api_key)] = None,
) -> AgentRunResponse:
    """Run an agent with the provided input."""
    agent = registry.get(slug)
    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{slug}' not found",
        )

    try:
        output = runner.run(agent, body.input)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent execution failed: {exc}",
        )

    return AgentRunResponse(
        content=output.content,
        agent_name=output.agent_name,
        model=output.model,
        input_tokens=output.input_tokens,
        output_tokens=output.output_tokens,
        latency_ms=output.latency_ms,
    )
