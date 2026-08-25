"""Value Objects and Domain Enums for Gleam Pattern Detector."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class PatternCategory(str, Enum):
    """Categorical taxonomy for Gleam architectural patterns."""

    GLEAM_IDIOMATIC = "gleam_idiomatic"
    OTP_BEAM_CONCURRENCY = "otp_beam_concurrency"
    FUNCTIONAL_COMPOSITION = "functional_composition"
    CREATIONAL = "creational"
    STRUCTURAL = "structural"
    BEHAVIORAL = "behavioral"
    RESILIENCE = "resilience"
    PRINCIPLE = "principle"


class PatternType(str, Enum):
    """Concrete pattern identifiers for Gleam static analyzer (43 rules)."""

    # 1. Gleam Idiomatic & Functional Core
    CUSTOM_TYPE_ALGEBRAIC_DATA_TYPES = "custom_type_algebraic_data_types"
    EXHAUSTIVE_PATTERN_MATCHING = "exhaustive_pattern_matching"
    PIPE_OPERATOR_FLOW = "pipe_operator_flow"
    OPAQUE_TYPE_ENCAPSULATION = "opaque_type_encapsulation"
    RESULT_MONAD_RAILWAY = "result_monad_railway"
    USE_SYNTAX_CONTINUATION = "use_syntax_continuation"

    # 2. OTP & BEAM Concurrency
    GLEAM_OTP_ACTOR_PROCESS = "gleam_otp_actor_process"
    SUPERVISOR_TREE_SPEC = "supervisor_tree_spec"
    PROCESS_MESSAGE_PASSING = "process_message_passing"
    TASK_ASYNC_AWAIT = "task_async_await"

    # 3. Functional Composition
    HIGHER_ORDER_FUNCTION_PIPELINE = "higher_order_function_pipeline"
    CURRYING_PARTIAL_APPLICATION = "currying_partial_application"
    PURE_RECORD_UPDATE_SYNTAX = "pure_record_update_syntax"

    # 4. Creational Patterns (GoF 5/5)
    SINGLETON_PROCESS_REGISTRY = "singleton_process_registry"
    FACTORY_CONSTRUCTOR_FUNCTION = "factory_constructor_function"
    ABSTRACT_FACTORY_MODULE_SPEC = "abstract_factory_module_spec"
    BUILDER_RECORD_UPDATE_FLOW = "builder_record_update_flow"
    PROTOTYPE_IMMUTABLE_RECORD_CLONE = "prototype_immutable_record_clone"

    # 5. Structural Patterns (GoF 7/7)
    ADAPTER_NEWTYPE_WRAPPER = "adapter_newtype_wrapper"
    BRIDGE_TARGET_IMPLEMENTOR = "bridge_target_implementor"
    COMPOSITE_RECURSIVE_ADT_TREE = "composite_recursive_adt_tree"
    DECORATOR_MIDDLEWARE_INTERCEPTOR = "decorator_middleware_interceptor"
    FACADE_PUBLIC_MODULE_API = "facade_public_module_api"
    FLYWEIGHT_SHARED_ATOM_POOL = "flyweight_shared_atom_pool"
    PROXY_SUBJECT_GATEWAY = "proxy_subject_gateway"

    # 6. Behavioral Patterns (GoF 11/11)
    CHAIN_OF_RESPONSIBILITY_MIDDLEWARE = "chain_of_responsibility_middleware"
    COMMAND_MESSAGE_ACTION_PAYLOAD = "command_message_action_payload"
    INTERPRETER_CASE_AST_WALKER = "interpreter_case_ast_walker"
    ITERATOR_LAZY_STREAM = "iterator_lazy_stream"
    MEDIATOR_EVENT_COORDINATOR = "mediator_event_coordinator"
    MEMENTO_IMMUTABLE_STATE_SNAPSHOT = "memento_immutable_state_snapshot"
    OBSERVER_SUBJECT_PUBSUB_REGISTRY = "observer_subject_pubsub_registry"
    STATE_ACTOR_LOOP_FSM = "state_actor_loop_fsm"
    STRATEGY_INJECTED_FUNCTION = "strategy_injected_function"
    TEMPLATE_METHOD_SKELETON_PIPELINE = "template_method_skeleton_pipeline"
    VISITOR_ADT_PATTERN_MATCHER = "visitor_adt_pattern_matcher"

    # 7. Hazards & Safety
    UNHANDLED_RESULT_ERROR = "unhandled_result_error"
    INFINITE_ACTOR_LOOP = "infinite_actor_loop"
    TODO_PANIC_IN_PRODUCTION = "todo_panic_in_production"
    UNTYPED_DYNAMIC_DECODE_HAZARD = "untyped_dynamic_decode_hazard"
    SWALLOWED_PROCESS_TIMEOUT = "swallowed_process_timeout"

    # 8. SOLID & Clean Code Principles
    MONOLITHIC_CUSTOM_TYPE_SRP = "monolithic_custom_type_srp"
    FAT_MODULE_INTERFACE_ISP = "fat_module_interface_isp"
    DEEP_CASE_CASCADE_OCP = "deep_case_cascade_ocp"
    KISS_CYCLOMATIC_COMPLEXITY = "kiss_cyclomatic_complexity"
    KISS_LONG_PARAMETER_LIST = "kiss_long_parameter_list"
    DRY_DUPLICATE_LOGIC = "dry_duplicate_logic"
    DEMETER_LAW_TRAIN_WRECK = "demeter_law_train_wreck"


class ConfidenceLevel(str, Enum):
    """Categorized confidence rating."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


@dataclass(frozen=True)
class SourceLocation:
    """Source code coordinates in a Gleam file."""

    file_path: str
    line: int
    column: int = 1

    def __str__(self) -> str:
        return f"{self.file_path}:{self.line}:{self.column}"


@dataclass(frozen=True)
class Evidence:
    """Heuristic evidence item confirming pattern detection."""

    rule_code: str
    description: str
    weight: float
    location: SourceLocation | None = None


@dataclass
class Confidence:
    """Calculated confidence score with evidence traceability."""

    score: float  # 0.0 to 1.0
    evidences: list[Evidence] = field(default_factory=list)

    @property
    def level(self) -> ConfidenceLevel:
        if self.score >= 0.85:
            return ConfidenceLevel.VERY_HIGH
        if self.score >= 0.70:
            return ConfidenceLevel.HIGH
        if self.score >= 0.50:
            return ConfidenceLevel.MEDIUM
        return ConfidenceLevel.LOW

    @property
    def percentage_str(self) -> str:
        return f"{int(round(self.score * 100))}%"
