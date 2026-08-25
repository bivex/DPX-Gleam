"""GoF Behavioral design pattern rules for Gleam (11/11)."""

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


class ChainOfResponsibilityMiddlewareRule(BaseRule):
    """Detects Chain of Responsibility middleware pipeline."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if "middleware" in fn.name.lower() or "pipeline" in fn.name.lower() or "handler" in fn.name.lower():
                takes_next = any(p.name in ("next", "handler", "cont") for p in fn.parameters)
                if takes_next:
                    evidences = [
                        Evidence(
                            rule_code="BEHAVIORAL_CHAIN_OF_RESPONSIBILITY",
                            description=f"Function '{fn.name}' implements Chain of Responsibility delegating request to next handler in pipeline",
                            weight=0.88,
                            location=fn.location,
                        )
                    ]
                    detections.append(
                        Detection(
                            pattern_type=PatternType.CHAIN_OF_RESPONSIBILITY_MIDDLEWARE,
                            pattern_category=PatternCategory.BEHAVIORAL,
                            target_name=fn.name,
                            target_kind="fn",
                            confidence=Confidence(score=0.88, evidences=evidences),
                            primary_location=fn.location,
                            evidences=evidences,
                        )
                    )
        return detections


class CommandMessageActionPayloadRule(BaseRule):
    """Detects Command message variants carrying action payload for actors."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for t in model.all_types:
            if "Message" in t.name or "Command" in t.name or "Action" in t.name:
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_COMMAND_MESSAGE",
                        description=f"Type '{t.name}' encapsulates actor executable instructions as Command message variants",
                        weight=0.90,
                        location=t.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.COMMAND_MESSAGE_ACTION_PAYLOAD,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=t.name,
                        target_kind="type",
                        confidence=Confidence(score=0.90, evidences=evidences),
                        primary_location=t.location,
                        evidences=evidences,
                    )
                )
        return detections


class InterpreterCaseAstWalkerRule(BaseRule):
    """Detects Interpreter pattern evaluating domain AST expressions."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.name in ("eval", "evaluate", "interpret", "walk", "execute_ast"):
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_INTERPRETER_AST",
                        description=f"Function '{fn.name}' evaluates domain AST grammar expressions as an Interpreter",
                        weight=0.92,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.INTERPRETER_CASE_AST_WALKER,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.92, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class IteratorLazyStreamRule(BaseRule):
    """Detects Iterator pattern utilizing 'gleam/iterator.Iterator(t)'."""

    ITER_PATTERN = re.compile(r"\b(iterator\.Iterator|iterator\.map|iterator\.filter|iterator\.fold|iterator\.from_list)\b")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if "Iterator(" in fn.return_type or self.ITER_PATTERN.search(fn.body or ""):
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_ITERATOR_STREAM",
                        description=f"Function '{fn.name}' processes sequences lazily using Gleam Iterator streams",
                        weight=0.95,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.ITERATOR_LAZY_STREAM,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class MediatorEventCoordinatorRule(BaseRule):
    """Detects Mediator coordinator routing events between processes."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for t in model.all_types:
            if "Mediator" in t.name or "Coordinator" in t.name or "Dispatcher" in t.name or "EventBus" in t.name:
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_MEDIATOR_COORDINATOR",
                        description=f"Type '{t.name}' coordinates decoupled communication between domain components as a Mediator",
                        weight=0.88,
                        location=t.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.MEDIATOR_EVENT_COORDINATOR,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=t.name,
                        target_kind="type",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=t.location,
                        evidences=evidences,
                    )
                )
        return detections


class MementoImmutableStateSnapshotRule(BaseRule):
    """Detects Memento immutable state records for snapshot checkpointing."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for t in model.all_types:
            if "Snapshot" in t.name or "Memento" in t.name or "Checkpoint" in t.name:
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_MEMENTO_SNAPSHOT",
                        description=f"Type '{t.name}' captures immutable state snapshot for Memento checkpointing",
                        weight=0.90,
                        location=t.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.MEMENTO_IMMUTABLE_STATE_SNAPSHOT,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=t.name,
                        target_kind="type",
                        confidence=Confidence(score=0.90, evidences=evidences),
                        primary_location=t.location,
                        evidences=evidences,
                    )
                )
        return detections


class ObserverSubjectPubSubRegistryRule(BaseRule):
    """Detects Observer PubSub registry holding subscriber Subject channels."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for t in model.all_types:
            has_subscribers = any(
                "subscribers" in f.name.lower() or "listeners" in f.name.lower() or "List(Subject" in f.type_name
                for v in t.variants
                for f in v.fields
            )
            if has_subscribers or "PubSub" in t.name or "Broadcaster" in t.name:
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_OBSERVER_PUBSUB",
                        description=f"Type '{t.name}' maintains subscriber channels for Observer event broadcasting",
                        weight=0.90,
                        location=t.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.OBSERVER_SUBJECT_PUBSUB_REGISTRY,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=t.name,
                        target_kind="type",
                        confidence=Confidence(score=0.90, evidences=evidences),
                        primary_location=t.location,
                        evidences=evidences,
                    )
                )
        return detections


class StateActorLoopFsmRule(BaseRule):
    """Detects Finite State Machine transitions in state custom types or actor loops."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for t in model.all_types:
            if ("State" in t.name or "Status" in t.name or "Phase" in t.name) and t.is_sum_type:
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_STATE_FSM",
                        description=f"Sum type '{t.name}' models Finite State Machine (FSM) states and phase transitions",
                        weight=0.92,
                        location=t.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.STATE_ACTOR_LOOP_FSM,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=t.name,
                        target_kind="type",
                        confidence=Confidence(score=0.92, evidences=evidences),
                        primary_location=t.location,
                        evidences=evidences,
                    )
                )
        return detections


class StrategyInjectedFunctionRule(BaseRule):
    """Detects Strategy pattern injecting interchangeable algorithm functions."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            strat_params = [p for p in fn.parameters if "strategy" in p.name.lower() or "algorithm" in p.name.lower() or "solver" in p.name.lower()]
            if strat_params:
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_STRATEGY_INJECTION",
                        description=f"Function '{fn.name}' injects interchangeable Strategy algorithm via '{strat_params[0].name}'",
                        weight=0.88,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.STRATEGY_INJECTED_FUNCTION,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class TemplateMethodSkeletonPipelineRule(BaseRule):
    """Detects Template Method pattern coordinating lifecycle hook callbacks."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            has_steps = any(kw in fn.body for kw in ("step1", "step2", "pre_process", "post_process", "hook", "before", "after"))
            if has_steps and ("process" in fn.name or "run" in fn.name or "execute" in fn.name):
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_TEMPLATE_METHOD",
                        description=f"Function '{fn.name}' coordinates a Template Method skeleton pipeline with configurable step hooks",
                        weight=0.85,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.TEMPLATE_METHOD_SKELETON_PIPELINE,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.85, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class VisitorAdtPatternMatcherRule(BaseRule):
    """Detects Visitor pattern decomposing heterogeneous ADT node variants."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.name.startswith("visit_") or fn.name in ("visit", "accept") or "visitor" in fn.name.lower():
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_VISITOR_MATCHER",
                        description=f"Function '{fn.name}' implements Visitor pattern matching over heterogeneous ADT node variants",
                        weight=0.90,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.VISITOR_ADT_PATTERN_MATCHER,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.90, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections
