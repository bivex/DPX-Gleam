"""Unit tests for all 23 GoF Creational, Structural, and Behavioral patterns in Gleam."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_gleam_parser import NativeGleamParserAdapter
from pattern_detector.domain.rules.behavioral_rules import (
    ChainOfResponsibilityMiddlewareRule,
    CommandMessageActionPayloadRule,
    InterpreterCaseAstWalkerRule,
    IteratorLazyStreamRule,
    MediatorEventCoordinatorRule,
    MementoImmutableStateSnapshotRule,
    ObserverSubjectPubSubRegistryRule,
    StateActorLoopFsmRule,
    StrategyInjectedFunctionRule,
    TemplateMethodSkeletonPipelineRule,
    VisitorAdtPatternMatcherRule,
)
from pattern_detector.domain.rules.creational_rules import (
    AbstractFactoryModuleSpecRule,
    BuilderRecordUpdateFlowRule,
    FactoryConstructorFunctionRule,
    PrototypeImmutableRecordCloneRule,
    SingletonProcessRegistryRule,
)
from pattern_detector.domain.rules.structural_rules import (
    AdapterNewtypeWrapperRule,
    BridgeTargetImplementorRule,
    CompositeRecursiveAdtTreeRule,
    DecoratorMiddlewareInterceptorRule,
    FacadePublicModuleApiRule,
    FlyweightSharedAtomPoolRule,
    ProxySubjectGatewayRule,
)
from pattern_detector.domain.value_objects import PatternType


# --- Creational (5/5) ---

def test_singleton_process_registry() -> None:
    code = """
pub type ProcessRegistry {
  ProcessRegistry
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("registry.gleam", code)])

    rule = SingletonProcessRegistryRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.SINGLETON_PROCESS_REGISTRY


def test_factory_constructor_function() -> None:
    code = """
pub fn new(name: String, age: Int) -> User {
  User(name: name, age: age)
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("factory.gleam", code)])

    rule = FactoryConstructorFunctionRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.FACTORY_CONSTRUCTOR_FUNCTION


def test_abstract_factory_module_spec() -> None:
    code = """
pub type GUIFactory {
  GUIFactory(
    create_button: fn() -> Button,
    create_dialog: fn() -> Dialog,
  )
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("abstract_factory.gleam", code)])

    rule = AbstractFactoryModuleSpecRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.ABSTRACT_FACTORY_MODULE_SPEC


def test_builder_record_update_flow() -> None:
    code = """
pub fn with_timeout(builder: ClientBuilder, timeout: Int) -> ClientBuilder {
  ClientBuilder(..builder, timeout: timeout)
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("builder.gleam", code)])

    rule = BuilderRecordUpdateFlowRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.BUILDER_RECORD_UPDATE_FLOW


def test_prototype_immutable_record_clone() -> None:
    code = """
pub fn clone(doc: Document) -> Document {
  Document(..doc, version: doc.version + 1)
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("proto.gleam", code)])

    rule = PrototypeImmutableRecordCloneRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.PROTOTYPE_IMMUTABLE_RECORD_CLONE


# --- Structural (7/7) ---

def test_adapter_newtype_wrapper() -> None:
    code = """
pub type JsonAdapter {
  JsonAdapter(raw: Dynamic)
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("adapter.gleam", code)])

    rule = AdapterNewtypeWrapperRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.ADAPTER_NEWTYPE_WRAPPER


def test_bridge_target_implementor() -> None:
    code = """
pub type DatabaseBridge {
  DatabaseBridge(backend: SqlBackend)
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("bridge.gleam", code)])

    rule = BridgeTargetImplementorRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.BRIDGE_TARGET_IMPLEMENTOR


def test_composite_recursive_adt_tree() -> None:
    code = """
pub type JSON {
  JsonNull
  JsonString(String)
  JsonArray(List(JSON))
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("json.gleam", code)])

    rule = CompositeRecursiveAdtTreeRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.COMPOSITE_RECURSIVE_ADT_TREE


def test_decorator_middleware_interceptor() -> None:
    code = """
pub fn logging_decorator(handler: fn(Request) -> Response) -> fn(Request) -> Response {
  fn(req) {
    log_request(req)
    handler(req)
  }
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("decorator.gleam", code)])

    rule = DecoratorMiddlewareInterceptorRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.DECORATOR_MIDDLEWARE_INTERCEPTOR


def test_facade_public_module_api() -> None:
    code = """
pub type Config { Config }
pub type State { State }

pub fn start() { Nil }
pub fn stop() { Nil }
pub fn restart() { Nil }
pub fn get_status() { Nil }
pub fn update_config() { Nil }
pub fn export_metrics() { Nil }
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("facade.gleam", code)])

    rule = FacadePublicModuleApiRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.FACADE_PUBLIC_MODULE_API


def test_flyweight_shared_atom_pool() -> None:
    code = """
pub type AtomPool {
  AtomPool(atoms: Dict(String, Int))
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("pool.gleam", code)])

    rule = FlyweightSharedAtomPoolRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.FLYWEIGHT_SHARED_ATOM_POOL


def test_proxy_subject_gateway() -> None:
    code = """
pub type AuthGateway {
  AuthGateway(target: process.Subject(Message))
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("proxy.gleam", code)])

    rule = ProxySubjectGatewayRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.PROXY_SUBJECT_GATEWAY


# --- Behavioral (11/11) ---

def test_chain_of_responsibility_middleware() -> None:
    code = """
pub fn auth_middleware(req: Request, next: fn(Request) -> Response) -> Response {
  next(req)
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("chain.gleam", code)])

    rule = ChainOfResponsibilityMiddlewareRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.CHAIN_OF_RESPONSIBILITY_MIDDLEWARE


def test_command_message_action_payload() -> None:
    code = """
pub type ActorMessage {
  Increment(amount: Int)
  Decrement(amount: Int)
  Reset
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("msg.gleam", code)])

    rule = CommandMessageActionPayloadRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.COMMAND_MESSAGE_ACTION_PAYLOAD


def test_interpreter_case_ast_walker() -> None:
    code = """
pub fn eval(expr: Expr) -> Int {
  case expr {
    Num(n) -> n
    Add(a, b) -> eval(a) + eval(b)
  }
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("eval.gleam", code)])

    rule = InterpreterCaseAstWalkerRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.INTERPRETER_CASE_AST_WALKER


def test_iterator_lazy_stream() -> None:
    code = """
pub fn stream_fibonacci() -> iterator.Iterator(Int) {
  iterator.unfold(from: #(0, 1), with: fn(pair) {
    let #(a, b) = pair
    iterator.Next(element: a, accumulator: #(b, a + b))
  })
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("fib.gleam", code)])

    rule = IteratorLazyStreamRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.ITERATOR_LAZY_STREAM


def test_mediator_event_coordinator() -> None:
    code = """
pub type EventCoordinator {
  EventCoordinator(channel: Int)
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("mediator.gleam", code)])

    rule = MediatorEventCoordinatorRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.MEDIATOR_EVENT_COORDINATOR


def test_memento_immutable_state_snapshot() -> None:
    code = """
pub type StateSnapshot {
  StateSnapshot(step: Int, value: Float)
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("snapshot.gleam", code)])

    rule = MementoImmutableStateSnapshotRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.MEMENTO_IMMUTABLE_STATE_SNAPSHOT


def test_observer_subject_pubsub_registry() -> None:
    code = """
pub type PubSubRegistry {
  PubSubRegistry(subscribers: List(process.Subject(Event)))
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("pubsub.gleam", code)])

    rule = ObserverSubjectPubSubRegistryRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.OBSERVER_SUBJECT_PUBSUB_REGISTRY


def test_state_actor_loop_fsm() -> None:
    code = """
pub type ConnectionState {
  Disconnected
  Connecting
  Connected(session_id: String)
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("state.gleam", code)])

    rule = StateActorLoopFsmRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.STATE_ACTOR_LOOP_FSM


def test_strategy_injected_function() -> None:
    code = """
pub fn sort_items(items: List(Item), sort_strategy: fn(Item, Item) -> Order) -> List(Item) {
  list.sort(items, sort_strategy)
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("strategy.gleam", code)])

    rule = StrategyInjectedFunctionRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.STRATEGY_INJECTED_FUNCTION


def test_template_method_skeleton_pipeline() -> None:
    code = """
pub fn process_order(order: Order) {
  step1_validate(order)
  step2_charge(order)
  step3_ship(order)
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("pipeline.gleam", code)])

    rule = TemplateMethodSkeletonPipelineRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.TEMPLATE_METHOD_SKELETON_PIPELINE


def test_visitor_adt_pattern_matcher() -> None:
    code = """
pub fn visit_node(node: ASTNode, visitor: Visitor) {
  case node {
    Leaf(val) -> visitor.on_leaf(val)
    Branch(l, r) -> visitor.on_branch(l, r)
  }
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("visitor.gleam", code)])

    rule = VisitorAdtPatternMatcherRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.VISITOR_ADT_PATTERN_MATCHER
