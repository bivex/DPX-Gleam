"""Gleam Idiomatic and Functional Core rules."""

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


class CustomTypeAlgebraicDataTypesRule(BaseRule):
    """Detects Algebraic Data Types (ADTs / Sum Types) defining tagged variants."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for t in model.all_types:
            if t.is_sum_type:
                variant_names = [v.name for v in t.variants]
                evidences = [
                    Evidence(
                        rule_code="GLEAM_SUM_TYPE_ADT",
                        description=f"Custom type '{t.name}' defines an Algebraic Data Type with {len(t.variants)} variants: {', '.join(variant_names[:3])}",
                        weight=0.95,
                        location=t.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.CUSTOM_TYPE_ALGEBRAIC_DATA_TYPES,
                        pattern_category=PatternCategory.GLEAM_IDIOMATIC,
                        target_name=t.name,
                        target_kind="type",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=t.location,
                        evidences=evidences,
                    )
                )
        return detections


class ExhaustivePatternMatchingRule(BaseRule):
    """Detects compiler-verified exhaustive 'case' pattern matching."""

    CASE_PATTERN = re.compile(r"\bcase\s+.+\s*\{")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            cases_found = len(self.CASE_PATTERN.findall(fn.body or ""))
            if cases_found >= 1 or fn.cases_count >= 1:
                evidences = [
                    Evidence(
                        rule_code="GLEAM_EXHAUSTIVE_CASE_MATCH",
                        description=f"Function '{fn.name}' performs compiler-checked exhaustive pattern matching across domain data types",
                        weight=0.92,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.EXHAUSTIVE_PATTERN_MATCHING,
                        pattern_category=PatternCategory.GLEAM_IDIOMATIC,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.92, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class PipeOperatorFlowRule(BaseRule):
    """Detects linear data pipelines utilizing Gleam's pipe operator (|>)."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            pipes = fn.body.count("|>") if fn.body else fn.pipes_count
            if pipes >= 2:
                evidences = [
                    Evidence(
                        rule_code="GLEAM_PIPE_OPERATOR_FLOW",
                        description=f"Function '{fn.name}' chains {pipes} data transformations using linear pipe operator (|>) flow",
                        weight=0.95,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.PIPE_OPERATOR_FLOW,
                        pattern_category=PatternCategory.GLEAM_IDIOMATIC,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class OpaqueTypeEncapsulationRule(BaseRule):
    """Detects encapsulated types declared with 'pub opaque type'."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for t in model.all_types:
            if t.is_opaque:
                evidences = [
                    Evidence(
                        rule_code="GLEAM_OPAQUE_TYPE_ENCAPSULATION",
                        description=f"Type '{t.name}' is declared as 'pub opaque type', strictly hiding internal representation",
                        weight=0.95,
                        location=t.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.OPAQUE_TYPE_ENCAPSULATION,
                        pattern_category=PatternCategory.GLEAM_IDIOMATIC,
                        target_name=t.name,
                        target_kind="type",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=t.location,
                        evidences=evidences,
                    )
                )
        return detections


class ResultMonadRailwayRule(BaseRule):
    """Detects explicit Result(Ok(t), Error(e)) railway error propagation."""

    RESULT_PATTERN = re.compile(r"\b(Result\(|result\.try|result\.map|result\.unwrap|bool\.guard)\b")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if "Result(" in fn.return_type or self.RESULT_PATTERN.search(fn.body or ""):
                evidences = [
                    Evidence(
                        rule_code="GLEAM_RESULT_MONAD_RAILWAY",
                        description=f"Function '{fn.name}' implements Railway-Oriented error handling via Result(Ok, Error)",
                        weight=0.90,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.RESULT_MONAD_RAILWAY,
                        pattern_category=PatternCategory.GLEAM_IDIOMATIC,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.90, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class UseSyntaxContinuationRule(BaseRule):
    """Detects continuation sugar 'use <-' for monadic guards and early exits."""

    USE_PATTERN = re.compile(r"\buse\s+[a-zA-Z0-9_,\s()]+\s*<-\s*")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            matches = len(self.USE_PATTERN.findall(fn.body or ""))
            if matches >= 1 or fn.uses_count >= 1:
                evidences = [
                    Evidence(
                        rule_code="GLEAM_USE_SYNTAX_CONTINUATION",
                        description=f"Function '{fn.name}' adopts 'use <-' continuation sugar for linear higher-order callbacks",
                        weight=0.95,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.USE_SYNTAX_CONTINUATION,
                        pattern_category=PatternCategory.GLEAM_IDIOMATIC,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections
