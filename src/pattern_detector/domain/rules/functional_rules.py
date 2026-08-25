"""Functional composition and transformation rules for Gleam."""

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


class HigherOrderFunctionPipelineRule(BaseRule):
    """Detects higher-order function composition ('list.map', 'list.fold', 'fn(...) -> ...')."""

    HOF_PATTERN = re.compile(r"\b(list\.map|list\.filter|list\.fold|list\.each|result\.map|option\.map)\b")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            fn_param_count = sum(1 for p in fn.parameters if "fn(" in p.type_name)
            if self.HOF_PATTERN.search(fn.body or "") or fn_param_count >= 1:
                evidences = [
                    Evidence(
                        rule_code="FUNCTIONAL_HOF_PIPELINE",
                        description=f"Function '{fn.name}' composes higher-order functions as first-class citizens",
                        weight=0.90,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.HIGHER_ORDER_FUNCTION_PIPELINE,
                        pattern_category=PatternCategory.FUNCTIONAL_COMPOSITION,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.90, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class CurryingPartialApplicationRule(BaseRule):
    """Detects anonymous closures and partial application."""

    CLOSURE_PATTERN = re.compile(r"\bfn\s*\([^)]*\)\s*\{")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            closures = len(self.CLOSURE_PATTERN.findall(fn.body or ""))
            if closures >= 2:
                evidences = [
                    Evidence(
                        rule_code="FUNCTIONAL_CLOSURE_CURRYING",
                        description=f"Function '{fn.name}' defines {closures} anonymous closures for partial application and currying",
                        weight=0.88,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.CURRYING_PARTIAL_APPLICATION,
                        pattern_category=PatternCategory.FUNCTIONAL_COMPOSITION,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class PureRecordUpdateSyntaxRule(BaseRule):
    """Detects immutable record copy updates ('Type(..base, field: value)')."""

    UPDATE_PATTERN = re.compile(r"\(\s*\.\.[a-zA-Z0-9_]+,\s*[a-zA-Z0-9_]+:")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if self.UPDATE_PATTERN.search(fn.body or ""):
                evidences = [
                    Evidence(
                        rule_code="FUNCTIONAL_RECORD_UPDATE",
                        description=f"Function '{fn.name}' creates immutable record copies using record update syntax (Type(..base, field: val))",
                        weight=0.92,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.PURE_RECORD_UPDATE_SYNTAX,
                        pattern_category=PatternCategory.FUNCTIONAL_COMPOSITION,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.92, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections
