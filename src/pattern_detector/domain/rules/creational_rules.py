"""GoF Creational design pattern rules for Gleam (5/5)."""

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


class SingletonProcessRegistryRule(BaseRule):
    """Detects Singleton actors or globally registered coordinators."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for t in model.all_types:
            if "Registry" in t.name or "Config" in t.name or "Singleton" in t.name:
                evidences = [
                    Evidence(
                        rule_code="CREATIONAL_SINGLETON_PROCESS",
                        description=f"Type '{t.name}' represents a unique global Singleton actor or configuration registry",
                        weight=0.88,
                        location=t.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.SINGLETON_PROCESS_REGISTRY,
                        pattern_category=PatternCategory.CREATIONAL,
                        target_name=t.name,
                        target_kind="type",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=t.location,
                        evidences=evidences,
                    )
                )
        return detections


class FactoryConstructorFunctionRule(BaseRule):
    """Detects Factory Constructor functions ('new', 'from_string', 'init')."""

    FACTORY_NAME_PATTERN = re.compile(r"^(new|from_[a-z0-9_]+|create|init|build)$")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if self.FACTORY_NAME_PATTERN.match(fn.name) or "factory" in fn.name.lower():
                evidences = [
                    Evidence(
                        rule_code="CREATIONAL_FACTORY_CONSTRUCTOR",
                        description=f"Function '{fn.name}' acts as a pure Factory Constructor instantiating domain records",
                        weight=0.90,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.FACTORY_CONSTRUCTOR_FUNCTION,
                        pattern_category=PatternCategory.CREATIONAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.90, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class AbstractFactoryModuleSpecRule(BaseRule):
    """Detects Abstract Factory records defining constructor function contracts."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for t in model.all_types:
            has_fn_fields = any("fn(" in f.type_name for v in t.variants for f in v.fields)
            if (has_fn_fields and "Factory" in t.name) or "Provider" in t.name or "Factory" in t.name:
                evidences = [
                    Evidence(
                        rule_code="CREATIONAL_ABSTRACT_FACTORY",
                        description=f"Type '{t.name}' defines an Abstract Factory contract holding constructor functions",
                        weight=0.88,
                        location=t.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.ABSTRACT_FACTORY_MODULE_SPEC,
                        pattern_category=PatternCategory.CREATIONAL,
                        target_name=t.name,
                        target_kind="type",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=t.location,
                        evidences=evidences,
                    )
                )
        return detections


class BuilderRecordUpdateFlowRule(BaseRule):
    """Detects Builder pattern accumulating fields into a configuration record."""

    BUILDER_METHOD = re.compile(r"^(with_|set_|add_)")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if self.BUILDER_METHOD.match(fn.name) or "Builder" in fn.name:
                evidences = [
                    Evidence(
                        rule_code="CREATIONAL_BUILDER_FLOW",
                        description=f"Function '{fn.name}' implements Builder pattern fluent parameter accumulation",
                        weight=0.88,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.BUILDER_RECORD_UPDATE_FLOW,
                        pattern_category=PatternCategory.CREATIONAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class PrototypeImmutableRecordCloneRule(BaseRule):
    """Detects Prototype pattern duplicating records via functional updates."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.name in ("clone", "copy", "duplicate") or ("prototype" in fn.name.lower()):
                evidences = [
                    Evidence(
                        rule_code="CREATIONAL_PROTOTYPE_CLONE",
                        description=f"Function '{fn.name}' implements Prototype pattern for duplicating and updating immutable records",
                        weight=0.88,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.PROTOTYPE_IMMUTABLE_RECORD_CLONE,
                        pattern_category=PatternCategory.CREATIONAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections
