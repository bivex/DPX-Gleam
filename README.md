# ⭐ DPX-Gleam: Type-Safe OTP Actors, Algebraic Data Types, Railway Monads, GoF 23 & BEAM Concurrency Architectural Pattern Detector

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Gleam Version](https://img.shields.io/badge/Gleam-1.0%20--%201.8+-FFAFF3?logo=gleam&logoColor=black)](https://gleam.run)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Architecture: Hexagonal DDD](https://img.shields.io/badge/Architecture-Hexagonal%20DDD-blueviolet)](https://alistair.cockburn.us/hexagonal-architecture/)
[![CLI: Typer & Rich](https://img.shields.io/badge/CLI-Typer%20%26%20Rich-009688)](https://typer.tiangolo.com)
[![SARIF OASIS v2.1.0](https://img.shields.io/badge/SARIF-OASIS%20v2.1.0-blue)](https://sarifweb.azurewebsites.net)

**DPX-Gleam** is an enterprise-grade static analysis engine and architectural pattern detector for Gleam codebases. Designed for **Type-Safe Functional Systems, Erlang/BEAM OTP Actors, Fault-Tolerant Distributed Services, and Fullstack Web Platforms (Lustre / Wisp)**, it analyzes **Custom Types (Sum Types / ADTs), Exhaustive Pattern Matching, Pipe Operator Flow (`|>`), Opaque Types, Railway-Oriented Error Handling (`Result(t, e)`), `use <-` Syntactic Sugar, BEAM OTP Processes (`actor.start`, `supervisor.start`, `task.async`), all 23 GoF Design Patterns**, and **Gleam Safety Hazards (Unhandled Results, Infinite Actor Loops, Production Panics, Dynamic Decode Hazards)**.

[Features](#-key-features) • [Installation](#-installation) • [CLI Usage](#-cli-usage) • [Supported Rules](#-supported-pattern-rules--checks) • [The DPX Suite Family](#-the-dpx-suite-family)

</div>

---

## 🌟 Key Features

- 🎭 **Type-Safe OTP Actors & BEAM Concurrency:** Audits stateful OTP actors (`gleam/otp/actor.start`, `actor.Spec`), Erlang supervision trees (`supervisor.start`, `supervisor.worker`), process message channels (`process.Subject`, `process.send`), and asynchronous background tasks (`task.async`).
- 💎 **Gleam Functional Idioms & Custom Types:** Analyzes Algebraic Data Types (Sum types / tagged variants), compiler-checked exhaustive `case` expressions, linear pipeline transformations (`|>`), opaque type encapsulation (`pub opaque type`), and `use <-` continuation pipelines.
- 🚂 **Railway-Oriented Programming (ROP):** Inspects explicit monadic error propagation with `Result(Ok(t), Error(e))`, `result.try`, and `bool.guard`.
- 🏛️ **100% Complete Gang of Four (GoF 23/23):** Comprehensive detection of all 23 classic Creational, Structural, and Behavioral patterns adapted for Gleam's algebraic type and actor-message paradigm.
- 🚨 **Safety, Concurrency & Resilience Hazard Detection:** Identifies dropped `Result(Error)` values, infinite actor loops without `actor.Stop` termination, unhandled `todo` and `panic` statements in production, and unsafe dynamic decoders.
- 📊 **Interactive Architecture Observability HUD:** Zero-dependency interactive HTML dashboard with instant search, KPI breakdown, and built-in **`🤖 Copy AI Context Prompt`** generator for LLMs (Claude, GPT-4, Gemini).
- 🔒 **CI/CD & GitHub Security Ready:** Standardized **OASIS SARIF v2.1.0**, JSON, and Markdown reports.

---

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/bivex/DPX-Gleam.git
cd DPX-Gleam

# Install dependencies using uv or pip
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

---

## 💻 CLI Usage

### 1. Scan a Gleam Project or Package
```bash
# Terminal scan with Rich formatting
dpx-gleam scan /path/to/gleam/project

# Export Interactive HTML Observability HUD
dpx-gleam scan src/ -H reports/gleam_hud.html

# Generate AI Context Prompt for LLMs
dpx-gleam scan src/ --llm

# Filter for specific OTP or ADT rules
dpx-gleam scan src/ -p gleam_otp_actor_process -p result_monad_railway

# Export SARIF for GitHub Code Scanning
dpx-gleam scan src/ -S reports/results.sarif
```

### 2. Inspect Supported Architectural Rules
```bash
dpx-gleam rules
```

### 3. Query Deep Pattern Documentation
```bash
dpx-gleam info gleam_otp_actor_process
dpx-gleam info result_monad_railway
```

---

## 📋 Supported Pattern Rules & Checks

### 1. 💎 Gleam Idiomatic & Functional Core
- `custom_type_algebraic_data_types`: Algebraic Data Types (Sum types / tagged union variants).
- `exhaustive_pattern_matching`: Compiler-checked exhaustive `case` pattern matching.
- `pipe_operator_flow`: Linear data pipelines using pipe operator (`|>`).
- `opaque_type_encapsulation`: Encapsulation via `pub opaque type`.
- `result_monad_railway`: Railway-Oriented error handling with `Result(Ok, Error)` and `result.try`.
- `use_syntax_continuation`: `use <-` continuation sugar for linear higher-order callbacks.

### 2. 🎭 OTP & BEAM Concurrency
- `gleam_otp_actor_process`: Stateful OTP actor process (`actor.start`, `actor.Spec`).
- `supervisor_tree_spec`: Supervision trees coordinating child worker fault tolerance.
- `process_message_passing`: Type-safe message channels with `process.Subject`.
- `task_async_await`: Asynchronous background task execution with `task.async`/`task.await`.

### 3. 🧩 Functional Composition
- `higher_order_function_pipeline`: Higher-order functions passed as arguments (`list.map`, `list.fold`).
- `currying_partial_application`: Anonymous closures and partial application.
- `pure_record_update_syntax`: Non-mutating record copy updates (`{ ..base, field: val }`).

### 4. 🏛️ GoF Creational Patterns (5/5)
- `singleton_process_registry`: Unique global actor registry or single state coordinator.
- `factory_constructor_function`: Pure factory constructor functions (`new`, `from_string`, `init`).
- `abstract_factory_module_spec`: Record defining constructor function contracts.
- `builder_record_update_flow`: Functional builder accumulating configuration options.
- `prototype_immutable_record_clone`: Prototype duplication via record updates.

### 5. 🧱 GoF Structural Patterns (7/7)
- `adapter_newtype_wrapper`: Newtype record adapting external or foreign types.
- `bridge_target_implementor`: Decoupling domain logic from target backend implementors (BEAM vs JS).
- `composite_recursive_adt_tree`: Recursive sum type tree structures.
- `decorator_middleware_interceptor`: Higher-order middleware wrapping handler functions.
- `facade_public_module_api`: Unified module API coordinating internal subsystems.
- `flyweight_shared_atom_pool`: Sharing immutable terms or atom tables.
- `proxy_subject_gateway`: Subject gateway controlling access or buffering requests for actors.

### 6. 🎯 GoF Behavioral Patterns (11/11)
- `chain_of_responsibility_middleware`: Middleware functions sequentially forwarding requests.
- `command_message_action_payload`: Actor message variants carrying executable action intent.
- `interpreter_case_ast_walker`: Domain AST expression evaluator.
- `iterator_lazy_stream`: Lazy sequence traversal with `gleam/iterator.Iterator(t)`.
- `mediator_event_coordinator`: Central event coordinator routing messages between processes.
- `memento_immutable_state_snapshot`: Immutable state snapshot for checkpointing and rollback.
- `observer_subject_pubsub_registry`: Broadcasting events to subscriber Subject channels.
- `state_actor_loop_fsm`: Finite state machine dispatching transitions inside an actor loop.
- `strategy_injected_function`: Interchangeable algorithm passed as a first-class function.
- `template_method_skeleton_pipeline`: Algorithm skeleton coordinating configurable step hooks.
- `visitor_adt_pattern_matcher`: Pattern matching traversing heterogeneous ADT variants.

### 7. 🛡️ Safety, Concurrency & Resilience Hazards
- `unhandled_result_error`: Dropped or ignored `Result(Error)` return values.
- `infinite_actor_loop`: Actor loop calling `actor.continue` without `actor.Stop` exit branches.
- `todo_panic_in_production`: Unimplemented `todo` or `panic` statements in production code.
- `untyped_dynamic_decode_hazard`: Unchecked dynamic coercion without decoder error guards.
- `swallowed_process_timeout`: Swallowed timeouts in `process.receive`.

### 8. 📐 SOLID & Clean Code Principles
- `monolithic_custom_type_srp`: Record declaring excessive fields (>= 10), violating SRP.
- `fat_module_interface_isp`: Module exposing excessive public functions (>= 12), violating ISP.
- `deep_case_cascade_ocp`: Case expression with >= 8 branches; consider sub-module decomposition.
- `kiss_cyclomatic_complexity`: High cyclomatic complexity (> 8 branch points).
- `kiss_long_parameter_list`: Functions accepting >= 6 parameters.
- `dry_duplicate_logic`: Duplicated algorithmic code blocks across functions.
- `demeter_law_train_wreck`: Deep record field chaining (`a.b.c.d.e`).

---

---

## 🌐 The DPX Multi-Language Static Analysis Family (33 Languages)

| # | Language | Repository | Ecosystem & Focus |
|:---:|---|---|---|
| 1 | **Ada** | [`bivex/DPX-Ada`](https://github.com/bivex/DPX-Ada) | Ada 2012/2022, SPARK Contracts, Ravenscar Tasking, DO-178C Safety |
| 2 | **Clojure** | [`bivex/DPX`](https://github.com/bivex/DPX) | Lisp S-Expressions, Protocols, Multimethods |
| 3 | **C** | [`bivex/DPX-C`](https://github.com/bivex/DPX-C) | Memory Safety, Struct VTables, Idiomatic C11/C23 |
| 4 | **Cairo** | [`bivex/DPX-Cairo`](https://github.com/bivex/DPX-Cairo) | Starknet Smart Contracts, ZK-Rollup Invariants |
| 5 | **C++** | [`bivex/DPX-Cpp`](https://github.com/bivex/DPX-Cpp) | RAII, CRTP, Concepts, Modern C++20/23 |
| 6 | **C#** | [`bivex/DPX-CSharp`](https://github.com/bivex/DPX-CSharp) | .NET 9, Roslyn AST, Linq, Records |
| 7 | **Dart** | [`bivex/DPX-Dart`](https://github.com/bivex/DPX-Dart) | Dart 3.x, Flutter, BLoC, Riverpod, Isolates |
| 8 | **Elixir** | [`bivex/DPX-Elixir`](https://github.com/bivex/DPX-Elixir) | BEAM OTP, GenServer, Supervisors |
| 9 | **Erlang** | [`bivex/DPX-Erlang`](https://github.com/bivex/DPX-Erlang) | Fault Tolerance, Actor Model, OTP Behaviors |
| 10 | **Gleam** | [`bivex/DPX-Gleam`](https://github.com/bivex/DPX-Gleam) | Type-Safe BEAM, Actor Concurrency |
| 11 | **Go** | [`bivex/DPX-Go`](https://github.com/bivex/DPX-Go) | Goroutines, Channels, Composition, Interfaces |
| 12 | **Haskell** | [`bivex/DPX-Haskell`](https://github.com/bivex/DPX-Haskell) | Pure Functional, Monads, Typeclasses, Arrows |
| 13 | **Huff** | [`bivex/DPX-Huff`](https://github.com/bivex/DPX-Huff) | Low-Level EVM Bytecode & Opcodes |
| 14 | **Idris 2** | [`bivex/DPX-Idris2`](https://github.com/bivex/DPX-Idris2) | Dependent Types, QTT Linear Protocols, Totality, Proofs |
| 15 | **Java** | [`bivex/DPX-Java`](https://github.com/bivex/DPX-Java) | Spring Boot, Enterprise Java, JVM Invariants |
| 16 | **Julia** | [`bivex/DPX-Julia`](https://github.com/bivex/DPX-Julia) | Multiple Dispatch, Scientific Computing |
| 17 | **Kotlin** | [`bivex/DPX-Kotlin`](https://github.com/bivex/DPX-Kotlin) | Coroutines, Multiplatform, Functional DSLs |
| 18 | **Lua** | [`bivex/DPX-Lua`](https://github.com/bivex/DPX-Lua) | Metatables, Coroutines, LuaJIT, Neovim |
| 19 | **Mojo** | [`bivex/DPX-Mojo`](https://github.com/bivex/DPX-Mojo) | SIMD Hardware, Memory Lifetimes, AI Systems |
| 20 | **Move** | [`bivex/DPX-Move`](https://github.com/bivex/DPX-Move) | Aptos & Sui Resource Safety, Linear Types |
| 21 | **OCaml** | [`bivex/DPX-OCaml`](https://github.com/bivex/DPX-OCaml) | Algebraic Data Types, Functors, Polymorphism |
| 22 | **PHP** | [`bivex/DPX-Php`](https://github.com/bivex/DPX-Php) | Modern PHP 8.4, Attributes, Traits, Laravel |
| 23 | **Prolog** | [`bivex/DPX-Prolog`](https://github.com/bivex/DPX-Prolog) | ISO Prolog, SWI-Prolog, DCG, CLP(FD/R/Q), CHR, Meta-Interpreters |
| 24 | **Puppet** | [`bivex/DPX-Puppet`](https://github.com/bivex/DPX-Puppet) | Puppet DSL, Roles/Profiles, IaC Security, Hiera |
| 25 | **Python** | [`bivex/DPX-Py`](https://github.com/bivex/DPX-Py) | Metaprogramming, Protocols, Hexagonal DDD |
| 26 | **Ruby** | [`bivex/DPX-Ruby`](https://github.com/bivex/DPX-Ruby) | Ruby 3.x, Rails, Metaprogramming, Dry-RB, Security |
| 27 | **Rust** | [`bivex/DPX-Rust`](https://github.com/bivex/DPX-Rust) | Zero-Cost Abstractions, Borrow Checker, Traits |
| 28 | **Solidity** | [`bivex/DPX-Solidity`](https://github.com/bivex/DPX-Solidity) | DeFi Security, Reentrancy, EVM Yul/Assembly |
| 29 | **SQL** | [`bivex/DPX-SQL`](https://github.com/bivex/DPX-SQL) | PostgreSQL, MySQL, SQLite, T-SQL, PL/SQL |
| 30 | **Swift** | [`bivex/DPX-Swift`](https://github.com/bivex/DPX-Swift) | Protocol-Oriented Programming, Actors |
| 31 | **TypeScript** | [`bivex/DPX-TypeScript`](https://github.com/bivex/DPX-TypeScript) | Generics, Conditional Types, Clean Architecture |
| 32 | **Yul** | [`bivex/DPX-Yul`](https://github.com/bivex/DPX-Yul) | EVM Intermediate Representation Optimization |
| 33 | **Zig** | [`bivex/DPX-Zig`](https://github.com/bivex/DPX-Zig) | Comptime, Manual Memory Allocators, C ABI |

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
