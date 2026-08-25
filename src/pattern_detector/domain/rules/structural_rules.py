"""GoF Structural design pattern rules for Gleam (7/7)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BaseRule
from pattern_detector.domain.value_objects import (
    Confidence,
    Evidence,
    PatternCategory,
    PatternType,
)


class AdapterNewtypeWrapperRule(BaseRule):
    """Detects Adapter pattern wrapping third-party or foreign types via newtype records."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for t in model.all_types:
            if "Adapter" in t.name or "Wrapper" in t.name:
                evidences = [
                    Evidence(
                        rule_code="STRUCTURAL_ADAPTER_NEWTYPE",
                        description=f"Type '{t.name}' adapts foreign or low-level types to domain interface contracts",
                        weight=0.88,
                        location=t.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.ADAPTER_NEWTYPE_WRAPPER,
                        pattern_category=PatternCategory.STRUCTURAL,
                        target_name=t.name,
                        target_kind="type",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=t.location,
                        evidences=evidences,
                    )
                )
        return detections


class BridgeTargetImplementorRule(BaseRule):
    """Detects Bridge pattern decoupling domain logic from target backend implementors."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for t in model.all_types:
            has_backend = any("Driver" in f.type_name or "Backend" in f.type_name or "Engine" in f.type_name for v in t.variants for f in v.fields)
            if has_backend or "Bridge" in t.name:
                evidences = [
                    Evidence(
                        rule_code="STRUCTURAL_BRIDGE_IMPLEMENTOR",
                        description=f"Type '{t.name}' decouples domain abstraction from target backend implementor",
                        weight=0.85,
                        location=t.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.BRIDGE_TARGET_IMPLEMENTOR,
                        pattern_category=PatternCategory.STRUCTURAL,
                        target_name=t.name,
                        target_kind="type",
                        confidence=Confidence(score=0.85, evidences=evidences),
                        primary_location=t.location,
                        evidences=evidences,
                    )
                )
        return detections


class CompositeRecursiveAdtTreeRule(BaseRule):
    """Detects Composite pattern modeling recursive AST or tree hierarchies in sum types."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for t in model.all_types:
            is_recursive = any(t.name in f.type_name or f"List({t.name})" in f.type_name for v in t.variants for f in v.fields)
            if (is_recursive and t.is_sum_type) or "Tree" in t.name or "Composite" in t.name:
                evidences = [
                    Evidence(
                        rule_code="STRUCTURAL_COMPOSITE_ADT",
                        description=f"Type '{t.name}' implements Composite pattern with recursive tree node variants",
                        weight=0.92,
                        location=t.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.COMPOSITE_RECURSIVE_ADT_TREE,
                        pattern_category=PatternCategory.STRUCTURAL,
                        target_name=t.name,
                        target_kind="type",
                        confidence=Confidence(score=0.92, evidences=evidences),
                        primary_location=t.location,
                        evidences=evidences,
                    )
                )
        return detections


class DecoratorMiddlewareInterceptorRule(BaseRule):
    """Detects Decorator pattern wrapping handler functions with cross-cutting behavior."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            takes_fn = any("fn(" in p.type_name for p in fn.parameters)
            returns_fn = "fn(" in fn.return_type
            if (takes_fn and returns_fn) or "decorator" in fn.name.lower() or "middleware" in fn.name.lower():
                evidences = [
                    Evidence(
                        rule_code="STRUCTURAL_DECORATOR_INTERCEPTOR",
                        description=f"Function '{fn.name}' decorates and augments inner handler functions as a Middleware Interceptor",
                        weight=0.90,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.DECORATOR_MIDDLEWARE_INTERCEPTOR,
                        pattern_category=PatternCategory.STRUCTURAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.90, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class FacadePublicModuleApiRule(BaseRule):
    """Detects Facade module APIs coordinating multiple internal subsystems."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for f in model.files:
            pub_fns = [fn for fn in f.functions if fn.is_pub]
            if len(pub_fns) >= 6 and len(f.types) >= 2:
                module_name = f.file_path.split("/")[-1].replace(".gleam", "")
                evidences = [
                    Evidence(
                        rule_code="STRUCTURAL_FACADE_MODULE",
                        description=f"Module '{module_name}' acts as a unified Facade API exposing {len(pub_fns)} entrypoints",
                        weight=0.82,
                        location=pub_fns[0].location if pub_fns else None,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.FACADE_PUBLIC_MODULE_API,
                        pattern_category=PatternCategory.STRUCTURAL,
                        target_name=module_name,
                        target_kind="module",
                        confidence=Confidence(score=0.82, evidences=evidences),
                        primary_location=pub_fns[0].location if pub_fns else None,
                        evidences=evidences,
                    )
                )
        return detections


class FlyweightSharedAtomPoolRule(BaseRule):
    """Detects Flyweight pattern sharing immutable terms, atom tables, or cached dicts."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for t in model.all_types:
            if "Pool" in t.name or "Cache" in t.name or "Flyweight" in t.name:
                evidences = [
                    Evidence(
                        rule_code="STRUCTURAL_FLYWEIGHT_POOL",
                        description=f"Type '{t.name}' implements Flyweight pool sharing immutable pre-allocated terms",
                        weight=0.88,
                        location=t.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.FLYWEIGHT_SHARED_ATOM_POOL,
                        pattern_category=PatternCategory.STRUCTURAL,
                        target_name=t.name,
                        target_kind="type",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=t.location,
                        evidences=evidences,
                    )
                )
        return detections


class ProxySubjectGatewayRule(BaseRule):
    """Detects Proxy pattern acting as a Subject gateway / surrogate for an OTP actor."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for t in model.all_types:
            has_subject = any("Subject(" in f.type_name for v in t.variants for f in v.fields)
            if (has_subject and "Gateway" in t.name) or "Proxy" in t.name or "Client" in t.name:
                evidences = [
                    Evidence(
                        rule_code="STRUCTURAL_PROXY_GATEWAY",
                        description=f"Type '{t.name}' acts as a Proxy Subject Gateway controlling access to underlying actors",
                        weight=0.88,
                        location=t.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.PROXY_SUBJECT_GATEWAY,
                        pattern_category=PatternCategory.STRUCTURAL,
                        target_name=t.name,
                        target_kind="type",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=t.location,
                        evidences=evidences,
                    )
                )
        return detections
