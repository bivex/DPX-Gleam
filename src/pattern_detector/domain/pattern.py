"""Pattern metadata catalog and definitions for Gleam static analyzer."""

from __future__ import annotations

from dataclasses import dataclass
from pattern_detector.domain.value_objects import PatternCategory, PatternType


@dataclass(frozen=True)
class PatternDefinition:
    """Detailed architectural definition for a Gleam design pattern."""

    type: PatternType
    name: str
    category: PatternCategory
    description: str
    gleam_version: str = "1.0 - 1.8+"
    recommendation: str | None = None


PATTERN_CATALOG: dict[PatternType, PatternDefinition] = {
    # 1. Gleam Idiomatic & Functional Core
    PatternType.CUSTOM_TYPE_ALGEBRAIC_DATA_TYPES: PatternDefinition(
        type=PatternType.CUSTOM_TYPE_ALGEBRAIC_DATA_TYPES,
        name="Custom Type (ADT / Sum Type)",
        category=PatternCategory.GLEAM_IDIOMATIC,
        description="Algebraic Data Type (ADT) defining tagged union variants or structured product records.",
        recommendation="Model business domain states as explicit Custom Types to leverage compiler exhaustiveness.",
    ),
    PatternType.EXHAUSTIVE_PATTERN_MATCHING: PatternDefinition(
        type=PatternType.EXHAUSTIVE_PATTERN_MATCHING,
        name="Exhaustive Pattern Matching",
        category=PatternCategory.GLEAM_IDIOMATIC,
        description="Compiler-verified exhaustive 'case' expression decomposing custom types without runtime misses.",
        recommendation="Rely on Gleam's exhaustive case matching rather than catch-all wildcard '_' branches.",
    ),
    PatternType.PIPE_OPERATOR_FLOW: PatternDefinition(
        type=PatternType.PIPE_OPERATOR_FLOW,
        name="Pipe Operator Flow (|>)",
        category=PatternCategory.GLEAM_IDIOMATIC,
        description="Linear data pipeline transformation passing output into the first argument of the next function.",
        recommendation="Use |> pipelines for multi-step data transformations to enhance readability.",
    ),
    PatternType.OPAQUE_TYPE_ENCAPSULATION: PatternDefinition(
        type=PatternType.OPAQUE_TYPE_ENCAPSULATION,
        name="Opaque Type Encapsulation",
        category=PatternCategory.GLEAM_IDIOMATIC,
        description="Encapsulated internal representation via 'pub opaque type' restricting construction to module constructors.",
        recommendation="Expose opaque types when domain invariants must be strictly enforced via constructor functions.",
    ),
    PatternType.RESULT_MONAD_RAILWAY: PatternDefinition(
        type=PatternType.RESULT_MONAD_RAILWAY,
        name="Result Monad Railway (Result(t, e))",
        category=PatternCategory.GLEAM_IDIOMATIC,
        description="Explicit error handling with Result(Ok(t), Error(e)) and 'result.try' monadic chaining.",
        recommendation="Propagate errors explicitly using Result and 'use <- result.try' instead of panicking.",
    ),
    PatternType.USE_SYNTAX_CONTINUATION: PatternDefinition(
        type=PatternType.USE_SYNTAX_CONTINUATION,
        name="Use Syntax Continuation",
        category=PatternCategory.GLEAM_IDIOMATIC,
        description="'use' syntactic sugar transforming callback hell into clean, linear continuation pipelines.",
        recommendation="Adopt 'use <-' for guards, resource management, and monadic early exits.",
    ),

    # 2. OTP & BEAM Concurrency
    PatternType.GLEAM_OTP_ACTOR_PROCESS: PatternDefinition(
        type=PatternType.GLEAM_OTP_ACTOR_PROCESS,
        name="Gleam OTP Actor Process",
        category=PatternCategory.OTP_BEAM_CONCURRENCY,
        description="Fault-tolerant BEAM lightweight process managed via 'gleam/otp/actor.start' or 'actor.Spec'.",
        recommendation="Use OTP Actors for stateful concurrent components and isolated failure domains.",
    ),
    PatternType.SUPERVISOR_TREE_SPEC: PatternDefinition(
        type=PatternType.SUPERVISOR_TREE_SPEC,
        name="Supervisor Tree Spec",
        category=PatternCategory.OTP_BEAM_CONCURRENCY,
        description="Erlang/BEAM supervision hierarchy coordinating child worker restarts and fault tolerance.",
        recommendation="Place all long-running actors under a Supervisor with defined restart strategies.",
    ),
    PatternType.PROCESS_MESSAGE_PASSING: PatternDefinition(
        type=PatternType.PROCESS_MESSAGE_PASSING,
        name="Process Message Passing",
        category=PatternCategory.OTP_BEAM_CONCURRENCY,
        description="Type-safe inter-process communication using 'process.Subject(msg)', 'send', and 'receive'.",
        recommendation="Use typed Subjects to prevent dynamic runtime message deserialization errors.",
    ),
    PatternType.TASK_ASYNC_AWAIT: PatternDefinition(
        type=PatternType.TASK_ASYNC_AWAIT,
        name="Task Async / Await",
        category=PatternCategory.OTP_BEAM_CONCURRENCY,
        description="Asynchronous parallel job execution via 'task.async' and 'task.await'.",
        recommendation="Parallelize independent I/O and compute jobs across BEAM cores using Tasks.",
    ),

    # 3. Functional Composition
    PatternType.HIGHER_ORDER_FUNCTION_PIPELINE: PatternDefinition(
        type=PatternType.HIGHER_ORDER_FUNCTION_PIPELINE,
        name="Higher-Order Function Pipeline",
        category=PatternCategory.FUNCTIONAL_COMPOSITION,
        description="First-class functions passed as arguments to 'list.map', 'list.fold', or custom combinators.",
    ),
    PatternType.CURRYING_PARTIAL_APPLICATION: PatternDefinition(
        type=PatternType.CURRYING_PARTIAL_APPLICATION,
        name="Currying & Partial Application",
        category=PatternCategory.FUNCTIONAL_COMPOSITION,
        description="Function parameter binding via anonymous closures or partial application.",
    ),
    PatternType.PURE_RECORD_UPDATE_SYNTAX: PatternDefinition(
        type=PatternType.PURE_RECORD_UPDATE_SYNTAX,
        name="Pure Record Update Syntax",
        category=PatternCategory.FUNCTIONAL_COMPOSITION,
        description="Non-mutating record copy with updated fields using '{ ..base, field: value }'.",
    ),

    # 4. Creational Patterns (GoF 5/5)
    PatternType.SINGLETON_PROCESS_REGISTRY: PatternDefinition(
        type=PatternType.SINGLETON_PROCESS_REGISTRY,
        name="Singleton Process Registry",
        category=PatternCategory.CREATIONAL,
        description="Single global actor registered via process name registry or top-level supervisor.",
    ),
    PatternType.FACTORY_CONSTRUCTOR_FUNCTION: PatternDefinition(
        type=PatternType.FACTORY_CONSTRUCTOR_FUNCTION,
        name="Factory Constructor Function",
        category=PatternCategory.CREATIONAL,
        description="Pure factory constructor ('new', 'from_string', 'init') instantiating valid records.",
    ),
    PatternType.ABSTRACT_FACTORY_MODULE_SPEC: PatternDefinition(
        type=PatternType.ABSTRACT_FACTORY_MODULE_SPEC,
        name="Abstract Factory Module Spec",
        category=PatternCategory.CREATIONAL,
        description="Record of constructor functions representing an abstract factory provider contract.",
    ),
    PatternType.BUILDER_RECORD_UPDATE_FLOW: PatternDefinition(
        type=PatternType.BUILDER_RECORD_UPDATE_FLOW,
        name="Builder Record Update Flow",
        category=PatternCategory.CREATIONAL,
        description="Method chaining or pipe flow accumulating configuration fields into a record.",
    ),
    PatternType.PROTOTYPE_IMMUTABLE_RECORD_CLONE: PatternDefinition(
        type=PatternType.PROTOTYPE_IMMUTABLE_RECORD_CLONE,
        name="Prototype Immutable Clone",
        category=PatternCategory.CREATIONAL,
        description="Duplicating prototype records with field modifications via record update syntax.",
    ),

    # 5. Structural Patterns (GoF 7/7)
    PatternType.ADAPTER_NEWTYPE_WRAPPER: PatternDefinition(
        type=PatternType.ADAPTER_NEWTYPE_WRAPPER,
        name="Adapter Newtype Wrapper",
        category=PatternCategory.STRUCTURAL,
        description="Newtype custom type wrapping external or foreign types to conform to domain contracts.",
    ),
    PatternType.BRIDGE_TARGET_IMPLEMENTOR: PatternDefinition(
        type=PatternType.BRIDGE_TARGET_IMPLEMENTOR,
        name="Bridge Target Implementor",
        category=PatternCategory.STRUCTURAL,
        description="Decoupling domain logic from target backend implementors (Erlang BEAM FFI vs JS FFI).",
    ),
    PatternType.COMPOSITE_RECURSIVE_ADT_TREE: PatternDefinition(
        type=PatternType.COMPOSITE_RECURSIVE_ADT_TREE,
        name="Composite Recursive ADT Tree",
        category=PatternCategory.STRUCTURAL,
        description="Recursive sum type hierarchy modeling abstract syntax trees or nested data structures.",
    ),
    PatternType.DECORATOR_MIDDLEWARE_INTERCEPTOR: PatternDefinition(
        type=PatternType.DECORATOR_MIDDLEWARE_INTERCEPTOR,
        name="Decorator Middleware Interceptor",
        category=PatternCategory.STRUCTURAL,
        description="Higher-order function wrapping an inner handler to augment behavior (logging, metrics).",
    ),
    PatternType.FACADE_PUBLIC_MODULE_API: PatternDefinition(
        type=PatternType.FACADE_PUBLIC_MODULE_API,
        name="Facade Public Module API",
        category=PatternCategory.STRUCTURAL,
        description="Unified module API orchestrating and hiding complex internal sub-module interactions.",
    ),
    PatternType.FLYWEIGHT_SHARED_ATOM_POOL: PatternDefinition(
        type=PatternType.FLYWEIGHT_SHARED_ATOM_POOL,
        name="Flyweight Shared Atom / Term Pool",
        category=PatternCategory.STRUCTURAL,
        description="Sharing immutable atoms, pre-allocated terms, or ETS table entries to conserve memory.",
    ),
    PatternType.PROXY_SUBJECT_GATEWAY: PatternDefinition(
        type=PatternType.PROXY_SUBJECT_GATEWAY,
        name="Proxy Subject Gateway",
        category=PatternCategory.STRUCTURAL,
        description="Subject wrapper controlling message access or buffering requests before the target actor.",
    ),

    # 6. Behavioral Patterns (GoF 11/11)
    PatternType.CHAIN_OF_RESPONSIBILITY_MIDDLEWARE: PatternDefinition(
        type=PatternType.CHAIN_OF_RESPONSIBILITY_MIDDLEWARE,
        name="Chain of Responsibility Middleware",
        category=PatternCategory.BEHAVIORAL,
        description="List of middleware functions sequentially handling or forwarding requests.",
    ),
    PatternType.COMMAND_MESSAGE_ACTION_PAYLOAD: PatternDefinition(
        type=PatternType.COMMAND_MESSAGE_ACTION_PAYLOAD,
        name="Command Message Action Payload",
        category=PatternCategory.BEHAVIORAL,
        description="Actor message variants encapsulating action intent and execution arguments.",
    ),
    PatternType.INTERPRETER_CASE_AST_WALKER: PatternDefinition(
        type=PatternType.INTERPRETER_CASE_AST_WALKER,
        name="Interpreter Case AST Walker",
        category=PatternCategory.BEHAVIORAL,
        description="Recursive case evaluation function traversing domain AST expressions.",
    ),
    PatternType.ITERATOR_LAZY_STREAM: PatternDefinition(
        type=PatternType.ITERATOR_LAZY_STREAM,
        name="Iterator Lazy Stream",
        category=PatternCategory.BEHAVIORAL,
        description="Lazy sequence traversal using 'gleam/iterator.Iterator(t)' streams.",
    ),
    PatternType.MEDIATOR_EVENT_COORDINATOR: PatternDefinition(
        type=PatternType.MEDIATOR_EVENT_COORDINATOR,
        name="Mediator Event Coordinator",
        category=PatternCategory.BEHAVIORAL,
        description="Central coordinator actor routing events between independent processes.",
    ),
    PatternType.MEMENTO_IMMUTABLE_STATE_SNAPSHOT: PatternDefinition(
        type=PatternType.MEMENTO_IMMUTABLE_STATE_SNAPSHOT,
        name="Memento State Snapshot",
        category=PatternCategory.BEHAVIORAL,
        description="Immutable state record captured for time-travel debugging or rollback.",
    ),
    PatternType.OBSERVER_SUBJECT_PUBSUB_REGISTRY: PatternDefinition(
        type=PatternType.OBSERVER_SUBJECT_PUBSUB_REGISTRY,
        name="Observer PubSub Registry",
        category=PatternCategory.BEHAVIORAL,
        description="Broadcasting events to a collection of subscriber Subject channels.",
    ),
    PatternType.STATE_ACTOR_LOOP_FSM: PatternDefinition(
        type=PatternType.STATE_ACTOR_LOOP_FSM,
        name="State Actor Loop FSM",
        category=PatternCategory.BEHAVIORAL,
        description="Finite State Machine where state transitions occur inside an OTP actor loop.",
    ),
    PatternType.STRATEGY_INJECTED_FUNCTION: PatternDefinition(
        type=PatternType.STRATEGY_INJECTED_FUNCTION,
        name="Strategy Injected Function",
        category=PatternCategory.BEHAVIORAL,
        description="Interchangeable algorithm passed as a first-class function parameter.",
    ),
    PatternType.TEMPLATE_METHOD_SKELETON_PIPELINE: PatternDefinition(
        type=PatternType.TEMPLATE_METHOD_SKELETON_PIPELINE,
        name="Template Method Skeleton Pipeline",
        category=PatternCategory.BEHAVIORAL,
        description="Pipeline skeleton coordinating configurable step hooks passed as functions.",
    ),
    PatternType.VISITOR_ADT_PATTERN_MATCHER: PatternDefinition(
        type=PatternType.VISITOR_ADT_PATTERN_MATCHER,
        name="Visitor ADT Pattern Matcher",
        category=PatternCategory.BEHAVIORAL,
        description="Pattern matching functions decomposing heterogeneous sum type variants.",
    ),

    # 7. Hazards & Safety
    PatternType.UNHANDLED_RESULT_ERROR: PatternDefinition(
        type=PatternType.UNHANDLED_RESULT_ERROR,
        name="Unhandled Result Error",
        category=PatternCategory.RESILIENCE,
        description="Result(t, e) dropped or ignored without pattern matching or monadic propagation.",
        recommendation="Handle Result variants explicitly or use 'use <- result.try' to propagate errors.",
    ),
    PatternType.INFINITE_ACTOR_LOOP: PatternDefinition(
        type=PatternType.INFINITE_ACTOR_LOOP,
        name="Infinite Actor Loop",
        category=PatternCategory.RESILIENCE,
        description="Actor loop calling 'actor.continue' unconditionally without termination handling.",
        recommendation="Provide 'actor.Stop' exit branches for clean process shutdown.",
    ),
    PatternType.TODO_PANIC_IN_PRODUCTION: PatternDefinition(
        type=PatternType.TODO_PANIC_IN_PRODUCTION,
        name="Todo / Panic in Production Code",
        category=PatternCategory.RESILIENCE,
        description="'todo' or 'panic' keyword present in reachable production code.",
        recommendation="Replace 'panic' and 'todo' with explicit Result(Error(reason)) return types.",
    ),
    PatternType.UNTYPED_DYNAMIC_DECODE_HAZARD: PatternDefinition(
        type=PatternType.UNTYPED_DYNAMIC_DECODE_HAZARD,
        name="Untyped Dynamic Decode Hazard",
        category=PatternCategory.RESILIENCE,
        description="Unvalidated dynamic decode or FFI call without decoder error guards.",
        recommendation="Use type-safe decoders ('decode.into', 'dynamic.field') with explicit error checking.",
    ),
    PatternType.SWALLOWED_PROCESS_TIMEOUT: PatternDefinition(
        type=PatternType.SWALLOWED_PROCESS_TIMEOUT,
        name="Swallowed Process Timeout",
        category=PatternCategory.RESILIENCE,
        description="Unchecked timeout in 'process.receive' leading to silent data loss or stale state.",
        recommendation="Handle timeout cases explicitly in process receive loops.",
    ),

    # 8. SOLID Principles
    PatternType.MONOLITHIC_CUSTOM_TYPE_SRP: PatternDefinition(
        type=PatternType.MONOLITHIC_CUSTOM_TYPE_SRP,
        name="Monolithic Custom Type (SRP)",
        category=PatternCategory.PRINCIPLE,
        description="Record type declaring excessive fields (>= 10), violating Single Responsibility.",
    ),
    PatternType.FAT_MODULE_INTERFACE_ISP: PatternDefinition(
        type=PatternType.FAT_MODULE_INTERFACE_ISP,
        name="Fat Module Interface (ISP)",
        category=PatternCategory.PRINCIPLE,
        description="Module exposing excessive public functions (>= 15), violating Interface Segregation.",
    ),
    PatternType.DEEP_CASE_CASCADE_OCP: PatternDefinition(
        type=PatternType.DEEP_CASE_CASCADE_OCP,
        name="Deep Case Cascade (OCP)",
        category=PatternCategory.PRINCIPLE,
        description="Case expression with >= 8 branches; consider decomposing into sub-modules or dispatch tables.",
    ),
    PatternType.KISS_CYCLOMATIC_COMPLEXITY: PatternDefinition(
        type=PatternType.KISS_CYCLOMATIC_COMPLEXITY,
        name="High Cyclomatic Complexity",
        category=PatternCategory.PRINCIPLE,
        description="Function containing excessive decision branch points (> 8).",
    ),
    PatternType.KISS_LONG_PARAMETER_LIST: PatternDefinition(
        type=PatternType.KISS_LONG_PARAMETER_LIST,
        name="Long Parameter List",
        category=PatternCategory.PRINCIPLE,
        description="Function accepting >= 6 positional parameters.",
    ),
    PatternType.DRY_DUPLICATE_LOGIC: PatternDefinition(
        type=PatternType.DRY_DUPLICATE_LOGIC,
        name="Duplicate Logic (DRY)",
        category=PatternCategory.PRINCIPLE,
        description="Duplicated algorithmic sequences across multiple functions.",
    ),
    PatternType.DEMETER_LAW_TRAIN_WRECK: PatternDefinition(
        type=PatternType.DEMETER_LAW_TRAIN_WRECK,
        name="Law of Demeter Violation",
        category=PatternCategory.PRINCIPLE,
        description="Deep record navigation chains ('a.b.c.d.e').",
    ),
}
