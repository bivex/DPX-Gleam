"""Unit tests for CLI commands and formatters/exporters in DPX-Gleam."""

from __future__ import annotations

from typer.testing import CliRunner
from pattern_detector.adapters.inbound.cli.main import app
from pattern_detector.adapters.outbound.persistence import (
    HtmlReportFormatter,
    JsonReportFormatter,
    LlmReportFormatter,
    MarkdownReportFormatter,
    SarifReportFormatter,
)
from pattern_detector.domain.detection import Detection, DetectionReport
from pattern_detector.domain.value_objects import (
    Confidence,
    Evidence,
    PatternCategory,
    PatternType,
    SourceLocation,
)

runner = CliRunner()


def _create_sample_report() -> DetectionReport:
    loc = SourceLocation(file_path="src/actor.gleam", line=10, column=1)
    ev = Evidence(rule_code="OTP_ACTOR_PROCESS", description="Stateful OTP actor process", weight=0.95, location=loc)
    det = Detection(
        pattern_type=PatternType.GLEAM_OTP_ACTOR_PROCESS,
        pattern_category=PatternCategory.OTP_BEAM_CONCURRENCY,
        target_name="start_actor",
        target_kind="actor",
        confidence=Confidence(score=0.95, evidences=[ev]),
        primary_location=loc,
        evidences=[ev],
    )
    return DetectionReport(
        project_path="src",
        scanned_files_count=1,
        detections=[det],
        elapsed_seconds=0.012,
    )


def test_cli_rules_command() -> None:
    result = runner.invoke(app, ["rules"])
    assert result.exit_code == 0
    assert "DPX-Gleam" in result.stdout
    assert "GLEAM_IDIOMATIC" in result.stdout


def test_cli_info_command() -> None:
    result = runner.invoke(app, ["info", "gleam_otp_actor_process"])
    assert result.exit_code == 0
    assert "Gleam OTP Actor Process" in result.stdout


def test_exporters_format() -> None:
    report = _create_sample_report()

    html_out = HtmlReportFormatter().format(report)
    assert "<!DOCTYPE html>" in html_out
    assert "Pattern Scanner Report" in html_out
    assert "start_actor" in html_out
    assert "Copy AI Context Prompt" in html_out

    md_out = MarkdownReportFormatter().format(report)
    assert "# ⭐ DPX-Gleam" in md_out
    assert "start_actor" in md_out

    json_out = JsonReportFormatter().format(report)
    assert '"total_detections_count": 1' in json_out

    sarif_out = SarifReportFormatter().format(report)
    assert '"$schema"' in sarif_out

    llm_out = LlmReportFormatter().format_scan_report(report)
    assert '<codebase_architecture_analysis language="gleam">' in llm_out
