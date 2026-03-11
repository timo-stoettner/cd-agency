"""Scoring endpoints — readability, linter, a11y, and combined."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from api.deps import verify_api_key
from api.models import (
    A11yIssueResponse,
    A11yResponse,
    CombinedScoreResponse,
    LintIssue,
    LintResponse,
    ReadabilityResponse,
    ScoreRequest,
)
from tools.a11y_checker import A11yChecker
from tools.linter import ContentLinter
from tools.scoring import ReadabilityScorer

router = APIRouter(prefix="/score", tags=["scoring"])

# Re-use scorer instances across requests (they are stateless).
_readability_scorer = ReadabilityScorer()
_content_linter = ContentLinter()
_a11y_checker = A11yChecker()


def _build_readability_response(text: str) -> ReadabilityResponse:
    result = _readability_scorer.score(text)
    return ReadabilityResponse(**result.to_dict())


def _build_lint_response(text: str) -> LintResponse:
    results = _content_linter.lint(text)
    issues = [
        LintIssue(
            rule=r.rule,
            passed=r.passed,
            severity=r.severity.value,
            message=r.message,
            suggestion=r.suggestion,
            matches=r.matches,
        )
        for r in results
    ]
    passed_count = sum(1 for i in issues if i.passed)
    failed_count = len(issues) - passed_count
    return LintResponse(
        issues=issues,
        passed_count=passed_count,
        failed_count=failed_count,
        total_rules=len(issues),
    )


def _build_a11y_response(text: str) -> A11yResponse:
    result = _a11y_checker.check(text)
    return A11yResponse(
        passed=result.passed,
        label=result.label,
        issue_count=result.issue_count,
        reading_grade=result.reading_grade,
        target_grade=result.target_grade,
        issues=[
            A11yIssueResponse(
                rule=i.rule,
                severity=i.severity.value,
                message=i.message,
                wcag_criterion=i.wcag_criterion,
                suggestion=i.suggestion,
                matches=i.matches,
            )
            for i in result.issues
        ],
    )


@router.post("/readability", response_model=ReadabilityResponse)
async def score_readability(
    body: ScoreRequest,
    _auth: Annotated[str | None, Depends(verify_api_key)] = None,
) -> ReadabilityResponse:
    """Score text for readability metrics."""
    return _build_readability_response(body.text)


@router.post("/lint", response_model=LintResponse)
async def score_lint(
    body: ScoreRequest,
    _auth: Annotated[str | None, Depends(verify_api_key)] = None,
) -> LintResponse:
    """Run the content linter on text."""
    return _build_lint_response(body.text)


@router.post("/a11y", response_model=A11yResponse)
async def score_a11y(
    body: ScoreRequest,
    _auth: Annotated[str | None, Depends(verify_api_key)] = None,
) -> A11yResponse:
    """Run accessibility checks on text."""
    return _build_a11y_response(body.text)


@router.post("/all", response_model=CombinedScoreResponse)
async def score_all(
    body: ScoreRequest,
    _auth: Annotated[str | None, Depends(verify_api_key)] = None,
) -> CombinedScoreResponse:
    """Run all scoring tools and return a combined result."""
    return CombinedScoreResponse(
        readability=_build_readability_response(body.text),
        lint=_build_lint_response(body.text),
        a11y=_build_a11y_response(body.text),
    )
