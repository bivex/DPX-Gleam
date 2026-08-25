"""OTP and BEAM concurrency pattern detection rules for Gleam."""

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


class GleamOtpActorProcessRule(BaseRule):
    """Detects stateful OTP actors managed via 'gleam/otp/actor'."""

    ACTOR_PATTERN = re.compile(r"\b(actor\.start|actor\.Spec|actor\.continue|actor\.Stop|actor\.call|actor\.send)\b")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if self.ACTOR_PATTERN.search(fn.body or "") or fn.is_actor_loop:
                evidences = [
                    Evidence(
                        rule_code="OTP_ACTOR_PROCESS",
                        description=f"Function '{fn.name}' coordinates a stateful, fault-tolerant Gleam OTP Actor process",
                        weight=0.95,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.GLEAM_OTP_ACTOR_PROCESS,
                        pattern_category=PatternCategory.OTP_BEAM_CONCURRENCY,
                        target_name=fn.name,
                        target_kind="actor",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class SupervisorTreeSpecRule(BaseRule):
    """Detects BEAM supervision trees coordinating child worker restarts."""

    SUPERVISOR_PATTERN = re.compile(r"\b(supervisor\.start|supervisor\.add|supervisor\.worker|supervisor\.Spec)\b")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if self.SUPERVISOR_PATTERN.search(fn.body or "") or "supervisor" in fn.name.lower():
                evidences = [
                    Evidence(
                        rule_code="OTP_SUPERVISOR_SPEC",
                        description=f"Function '{fn.name}' defines an Erlang/BEAM Supervisor tree spec coordinating child fault tolerance",
                        weight=0.95,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.SUPERVISOR_TREE_SPEC,
                        pattern_category=PatternCategory.OTP_BEAM_CONCURRENCY,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class ProcessMessagePassingRule(BaseRule):
    """Detects type-safe process communication via 'process.Subject' and message channels."""

    PROCESS_PATTERN = re.compile(r"\b(process\.Subject|process\.send|process\.receive|process\.new_subject|process\.spawn)\b")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if self.PROCESS_PATTERN.search(fn.body or "") or any("Subject(" in p.type_name for p in fn.parameters):
                evidences = [
                    Evidence(
                        rule_code="OTP_PROCESS_MESSAGE_PASSING",
                        description=f"Function '{fn.name}' performs type-safe message passing via process Subject channels",
                        weight=0.92,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.PROCESS_MESSAGE_PASSING,
                        pattern_category=PatternCategory.OTP_BEAM_CONCURRENCY,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.92, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class TaskAsyncAwaitRule(BaseRule):
    """Detects asynchronous job execution with 'task.async' and 'task.await'."""

    TASK_PATTERN = re.compile(r"\b(task\.async|task\.await|task\.try_await)\b")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if self.TASK_PATTERN.search(fn.body or ""):
                evidences = [
                    Evidence(
                        rule_code="OTP_TASK_ASYNC_AWAIT",
                        description=f"Function '{fn.name}' spawns parallel background jobs via Task async/await",
                        weight=0.95,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.TASK_ASYNC_AWAIT,
                        pattern_category=PatternCategory.OTP_BEAM_CONCURRENCY,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections
