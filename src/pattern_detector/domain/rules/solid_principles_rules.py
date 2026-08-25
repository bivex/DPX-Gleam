"""SOLID principles and clean code quality rules for Gleam."""

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


class MonolithicCustomTypeSrpRule(BaseRule):
    """Detects custom types with excessive fields violating SRP (>= 10 fields)."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for t in model.all_types:
            if t.total_fields_count >= 10:
                score = 0.90 if t.total_fields_count >= 12 else 0.82
                evidences = [
                    Evidence(
                        rule_code="SRP_MONOLITHIC_CUSTOM_TYPE",
                        description=f"Custom type '{t.name}' is a Monolithic Record declaring {t.total_fields_count} fields; consider decomposing into cohesive sub-records",
                        weight=score,
                        location=t.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.MONOLITHIC_CUSTOM_TYPE_SRP,
                        pattern_category=PatternCategory.PRINCIPLE,
                        target_name=t.name,
                        target_kind="type",
                        confidence=Confidence(score=score, evidences=evidences),
                        primary_location=t.location,
                        evidences=evidences,
                    )
                )
        return detections


class FatModuleInterfaceIspRule(BaseRule):
    """Detects fat modules exposing excessive public functions (>= 12)."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for f in model.files:
            pub_fns = [fn for fn in f.functions if fn.is_pub]
            if len(pub_fns) >= 12:
                module_name = f.file_path.split("/")[-1].replace(".gleam", "")
                evidences = [
                    Evidence(
                        rule_code="ISP_FAT_MODULE_INTERFACE",
                        description=f"Module '{module_name}' exposes {len(pub_fns)} public functions; consider decomposing into cohesive sub-modules",
                        weight=0.85,
                        location=pub_fns[0].location if pub_fns else None,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.FAT_MODULE_INTERFACE_ISP,
                        pattern_category=PatternCategory.PRINCIPLE,
                        target_name=module_name,
                        target_kind="module",
                        confidence=Confidence(score=0.85, evidences=evidences),
                        primary_location=pub_fns[0].location if pub_fns else None,
                        evidences=evidences,
                    )
                )
        return detections


class DeepCaseCascadeOcpRule(BaseRule):
    """Detects monolithic case branches (>= 8 branches) violating OCP."""

    BRANCH_PATTERN = re.compile(r"^\s*[a-zA-Z0-9_(),\s|]+\s*->\s*", re.MULTILINE)

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            matches = len(self.BRANCH_PATTERN.findall(fn.body or ""))
            if matches >= 8 and "case " in fn.body:
                evidences = [
                    Evidence(
                        rule_code="OCP_DEEP_CASE_CASCADE",
                        description=f"Function '{fn.name}' contains {matches} case branches; decompose into modular handlers to satisfy OCP",
                        weight=0.88,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.DEEP_CASE_CASCADE_OCP,
                        pattern_category=PatternCategory.PRINCIPLE,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class KissCyclomaticComplexityRule(BaseRule):
    """Detects functions with excessive cyclomatic complexity (> 8 branch points)."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.branch_count >= 9:
                evidences = [
                    Evidence(
                        rule_code="KISS_CYCLOMATIC_COMPLEXITY",
                        description=f"Function '{fn.name}' has high cyclomatic complexity ({fn.branch_count} branch points), violating KISS",
                        weight=0.88,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.KISS_CYCLOMATIC_COMPLEXITY,
                        pattern_category=PatternCategory.PRINCIPLE,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class KissLongParameterListRule(BaseRule):
    """Detects functions accepting excessive parameters (>= 6)."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if len(fn.parameters) >= 6:
                evidences = [
                    Evidence(
                        rule_code="KISS_LONG_PARAMETER_LIST",
                        description=f"Function '{fn.name}' accepts {len(fn.parameters)} parameters; bundle into a custom configuration record",
                        weight=0.85,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.KISS_LONG_PARAMETER_LIST,
                        pattern_category=PatternCategory.PRINCIPLE,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.85, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class DryDuplicateLogicRule(BaseRule):
    """Detects duplicated code blocks across functions."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        body_map: dict[str, list[str]] = {}
        for fn in model.all_functions:
            cleaned = re.sub(r"\s+", " ", fn.body).strip()
            if len(cleaned) >= 50:
                body_map.setdefault(cleaned, []).append(fn.name)

        for body, names in body_map.items():
            if len(names) >= 2:
                evidences = [
                    Evidence(
                        rule_code="DRY_DUPLICATE_CODE",
                        description=f"Identical logic duplicated across {len(names)} function(s): {', '.join(names[:3])}",
                        weight=0.80,
                        location=None,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.DRY_DUPLICATE_LOGIC,
                        pattern_category=PatternCategory.PRINCIPLE,
                        target_name=names[0],
                        target_kind="fn",
                        confidence=Confidence(score=0.80, evidences=evidences),
                        primary_location=None,
                        evidences=evidences,
                    )
                )
        return detections


class DemeterLawTrainWreckRule(BaseRule):
    """Detects Law of Demeter violations (deep record navigation 'a.b.c.d.e')."""

    DOT_CHAIN_PATTERN = re.compile(r"\b[a-zA-Z_]\w*\.[a-zA-Z_]\w*\.[a-zA-Z_]\w*\.[a-zA-Z_]\w*\.[a-zA-Z_]\w*\b")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            matches = self.DOT_CHAIN_PATTERN.findall(fn.body or "")
            if matches:
                evidences = [
                    Evidence(
                        rule_code="DEMETER_LAW_TRAIN_WRECK",
                        description=f"Function '{fn.name}' violates Law of Demeter with deep field access chain: '{matches[0]}'",
                        weight=0.80,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.DEMETER_LAW_TRAIN_WRECK,
                        pattern_category=PatternCategory.PRINCIPLE,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.80, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections
