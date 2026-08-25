"""Resilience, Safety and Error Handling Hazards rules for Gleam."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BaseRule
from pattern_detector.domain.value_objects import (
    Confidence,
    Evidence,
    PatternCategory,
    PatternType,
)


class UnhandledResultErrorRule(BaseRule):
    """Detects Result(t, e) values that are dropped or ignored without handling."""

    RESULT_IGNORING_PATTERN = re.compile(r"\blet\s+_\s*=\s*[a-zA-Z0-9_.]+\s*\(")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            matches = self.RESULT_IGNORING_PATTERN.findall(fn.body or "")
            if matches and ("result" in fn.body or "Error" in fn.body):
                evidences = [
                    Evidence(
                        rule_code="HAZARD_UNHANDLED_RESULT_ERROR",
                        description=f"Function '{fn.name}' silently ignores return values via 'let _ = ...'; handle Result(Error) explicitly",
                        weight=0.88,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.UNHANDLED_RESULT_ERROR,
                        pattern_category=PatternCategory.RESILIENCE,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class InfiniteActorLoopRule(BaseRule):
    """Detects actor loops calling 'actor.continue' unconditionally without termination exit points."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if "actor.continue" in fn.body and "actor.Stop" not in fn.body and "Stop" not in fn.body:
                evidences = [
                    Evidence(
                        rule_code="HAZARD_INFINITE_ACTOR_LOOP",
                        description=f"Actor loop '{fn.name}' calls 'actor.continue' without any 'actor.Stop' exit branches",
                        weight=0.88,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.INFINITE_ACTOR_LOOP,
                        pattern_category=PatternCategory.RESILIENCE,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class TodoPanicInProductionRule(BaseRule):
    """Detects 'todo' or 'panic' in reachable production code."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.has_todo or fn.has_panic or re.search(r"\b(todo|panic)\b", fn.body or ""):
                kind = "todo" if (fn.has_todo or "todo" in fn.body) else "panic"
                evidences = [
                    Evidence(
                        rule_code="HAZARD_TODO_PANIC_PRODUCTION",
                        description=f"Function '{fn.name}' contains '{kind}' keyword; replace with explicit Result(Error(reason))",
                        weight=0.92,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.TODO_PANIC_IN_PRODUCTION,
                        pattern_category=PatternCategory.RESILIENCE,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.92, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class UntypedDynamicDecodeHazardRule(BaseRule):
    """Detects unvalidated dynamic decoders or raw FFI without type guards."""

    DYNAMIC_PATTERN = re.compile(r"\b(dynamic\.from|dynamic\.unsafe_coerce|@external)\b")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if self.DYNAMIC_PATTERN.search(fn.body or "") and "decode" not in fn.body and "Result" not in fn.return_type:
                evidences = [
                    Evidence(
                        rule_code="HAZARD_UNTYPED_DYNAMIC_DECODE",
                        description=f"Function '{fn.name}' performs unsafe dynamic coercion / external FFI without type-safe decoder validation",
                        weight=0.88,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.UNTYPED_DYNAMIC_DECODE_HAZARD,
                        pattern_category=PatternCategory.RESILIENCE,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class SwallowedProcessTimeoutRule(BaseRule):
    """Detects unchecked timeouts in 'process.receive'."""

    TIMEOUT_SWALLOW_PATTERN = re.compile(r"process\.receive\([^)]+\)\s*\|\s*Error\([^)]*\)\s*->\s*Nil")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if "process.receive" in fn.body and ("Error(_) -> Nil" in fn.body or "Error(_) -> nil" in fn.body):
                evidences = [
                    Evidence(
                        rule_code="HAZARD_SWALLOWED_PROCESS_TIMEOUT",
                        description=f"Function '{fn.name}' swallows process receive timeout without error handling, leading to silent loss",
                        weight=0.88,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.SWALLOWED_PROCESS_TIMEOUT,
                        pattern_category=PatternCategory.RESILIENCE,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections
