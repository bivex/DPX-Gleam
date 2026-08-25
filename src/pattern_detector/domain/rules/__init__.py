"""Rules registry and aggregation factory for Gleam pattern detector."""

from __future__ import annotations

from pattern_detector.domain.rules.base import BaseRule
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
from pattern_detector.domain.rules.functional_rules import (
    CurryingPartialApplicationRule,
    HigherOrderFunctionPipelineRule,
    PureRecordUpdateSyntaxRule,
)
from pattern_detector.domain.rules.idiomatic_rules import (
    CustomTypeAlgebraicDataTypesRule,
    ExhaustivePatternMatchingRule,
    OpaqueTypeEncapsulationRule,
    PipeOperatorFlowRule,
    ResultMonadRailwayRule,
    UseSyntaxContinuationRule,
)
from pattern_detector.domain.rules.otp_beam_rules import (
    GleamOtpActorProcessRule,
    ProcessMessagePassingRule,
    SupervisorTreeSpecRule,
    TaskAsyncAwaitRule,
)
from pattern_detector.domain.rules.resilience_hazards_rules import (
    InfiniteActorLoopRule,
    SwallowedProcessTimeoutRule,
    TodoPanicInProductionRule,
    UnhandledResultErrorRule,
    UntypedDynamicDecodeHazardRule,
)
from pattern_detector.domain.rules.solid_principles_rules import (
    DeepCaseCascadeOcpRule,
    DemeterLawTrainWreckRule,
    DryDuplicateLogicRule,
    FatModuleInterfaceIspRule,
    KissCyclomaticComplexityRule,
    KissLongParameterListRule,
    MonolithicCustomTypeSrpRule,
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

DEFAULT_RULES: list[type[BaseRule]] = [
    # 1. Gleam Idiomatic & Functional Core (6)
    CustomTypeAlgebraicDataTypesRule,
    ExhaustivePatternMatchingRule,
    PipeOperatorFlowRule,
    OpaqueTypeEncapsulationRule,
    ResultMonadRailwayRule,
    UseSyntaxContinuationRule,

    # 2. OTP & BEAM Concurrency (4)
    GleamOtpActorProcessRule,
    SupervisorTreeSpecRule,
    ProcessMessagePassingRule,
    TaskAsyncAwaitRule,

    # 3. Functional Composition (3)
    HigherOrderFunctionPipelineRule,
    CurryingPartialApplicationRule,
    PureRecordUpdateSyntaxRule,

    # 4. Creational GoF (5/5)
    SingletonProcessRegistryRule,
    FactoryConstructorFunctionRule,
    AbstractFactoryModuleSpecRule,
    BuilderRecordUpdateFlowRule,
    PrototypeImmutableRecordCloneRule,

    # 5. Structural GoF (7/7)
    AdapterNewtypeWrapperRule,
    BridgeTargetImplementorRule,
    CompositeRecursiveAdtTreeRule,
    DecoratorMiddlewareInterceptorRule,
    FacadePublicModuleApiRule,
    FlyweightSharedAtomPoolRule,
    ProxySubjectGatewayRule,

    # 6. Behavioral GoF (11/11)
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

    # 7. Hazards & Safety (5)
    UnhandledResultErrorRule,
    InfiniteActorLoopRule,
    TodoPanicInProductionRule,
    UntypedDynamicDecodeHazardRule,
    SwallowedProcessTimeoutRule,

    # 8. SOLID & Clean Code (7)
    MonolithicCustomTypeSrpRule,
    FatModuleInterfaceIspRule,
    DeepCaseCascadeOcpRule,
    KissCyclomaticComplexityRule,
    KissLongParameterListRule,
    DryDuplicateLogicRule,
    DemeterLawTrainWreckRule,
]


def get_default_rules() -> list[BaseRule]:
    """Instantiate and return full suite of default Gleam rules."""
    return [
        # 1. Idiomatic
        CustomTypeAlgebraicDataTypesRule(),
        ExhaustivePatternMatchingRule(),
        PipeOperatorFlowRule(),
        OpaqueTypeEncapsulationRule(),
        ResultMonadRailwayRule(),
        UseSyntaxContinuationRule(),

        # 2. OTP & BEAM
        GleamOtpActorProcessRule(),
        SupervisorTreeSpecRule(),
        ProcessMessagePassingRule(),
        TaskAsyncAwaitRule(),

        # 3. Functional Composition
        HigherOrderFunctionPipelineRule(),
        CurryingPartialApplicationRule(),
        PureRecordUpdateSyntaxRule(),

        # 4. Creational (5/5)
        SingletonProcessRegistryRule(),
        FactoryConstructorFunctionRule(),
        AbstractFactoryModuleSpecRule(),
        BuilderRecordUpdateFlowRule(),
        PrototypeImmutableRecordCloneRule(),

        # 5. Structural (7/7)
        AdapterNewtypeWrapperRule(),
        BridgeTargetImplementorRule(),
        CompositeRecursiveAdtTreeRule(),
        DecoratorMiddlewareInterceptorRule(),
        FacadePublicModuleApiRule(),
        FlyweightSharedAtomPoolRule(),
        ProxySubjectGatewayRule(),

        # 6. Behavioral (11/11)
        ChainOfResponsibilityMiddlewareRule(),
        CommandMessageActionPayloadRule(),
        InterpreterCaseAstWalkerRule(),
        IteratorLazyStreamRule(),
        MediatorEventCoordinatorRule(),
        MementoImmutableStateSnapshotRule(),
        ObserverSubjectPubSubRegistryRule(),
        StateActorLoopFsmRule(),
        StrategyInjectedFunctionRule(),
        TemplateMethodSkeletonPipelineRule(),
        VisitorAdtPatternMatcherRule(),

        # 7. Hazards & Safety
        UnhandledResultErrorRule(),
        InfiniteActorLoopRule(),
        TodoPanicInProductionRule(),
        UntypedDynamicDecodeHazardRule(),
        SwallowedProcessTimeoutRule(),

        # 8. SOLID & Clean Code
        MonolithicCustomTypeSrpRule(),
        FatModuleInterfaceIspRule(),
        DeepCaseCascadeOcpRule(),
        KissCyclomaticComplexityRule(),
        KissLongParameterListRule(),
        DryDuplicateLogicRule(),
        DemeterLawTrainWreckRule(),
    ]
