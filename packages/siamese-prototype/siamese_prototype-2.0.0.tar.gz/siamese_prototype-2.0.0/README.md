# Siamese Prototype v2.0: Production-Ready Async Rule Engine

siamese-prototypeis a high-performance, asynchronous backward-chaining rule engine in Python. It is designed for production environments where logic-based decisions may need to interact with external, non-blocking I/O resources like web APIs or databases.

```mermaid
sequenceDiagram
    participant App as User Application
    participant Engine as RuleEngine (Facade)
    participant Resolver as Async Resolver
    participant KB as KnowledgeBase
    participant Unificator
    participant Builtin as Async Built-in (e.g., http_get_json)

    App->>+Engine: await query("sibling", "john", "?S")
    Engine->>Engine: _to_internal() converts args
    Engine->>+Resolver: new Resolver(kb, builtins)
    Resolver-->>-Engine: resolver_instance
    Engine->>+Resolver: prove([goal], max_depth)
    note right of Resolver: Stack created with initial goal: [sibling(john, ?S)]

    loop Proof Search
        Resolver->>Resolver: Pop goal from stack
        Resolver->>Engine: yield TraceEvent("CALL", ...)
        Engine->>Engine: logger.trace(...)

        %% First, try matching a rule %%
        Resolver->>+KB: find_rules(sibling/2)
        KB-->>-Resolver: Return sibling rule
        Resolver->>Resolver: _rename_rule()
        Resolver->>+Unificator: unify(goal, rule.head)
        Unificator-->>-Resolver: new_bindings

        %% Rule head matches, add body to stack %%
        Resolver->>Resolver: Push rule body to stack: [parent(?P, john), parent(?P, mary), neq(john, mary)]
        Resolver->>Engine: yield TraceEvent("EXIT", ...)
        Engine->>Engine: logger.success(...)

        %% Next iteration of the loop for the 'parent' goal %%
        Resolver->>Resolver: Pop goal from stack: [parent(?P, john)]
        Resolver->>+KB: find_facts(parent/2)
        KB-->>-Resolver: Return parent(david, john)
        Resolver->>+Unificator: unify(...)
        Unificator-->>-Resolver: new_bindings {?P: david}

        %% ... continues similarly for the second 'parent' goal ... %%

        %% Finally, process the 'neq' built-in goal %%
        Resolver->>Resolver: Pop goal from stack: [neq(john, mary)]
        Resolver->>+Builtin: neq_builtin(goal, bindings)
        note right of Builtin: Performs synchronous check
        Builtin-->>-Resolver: yield new_bindings

        %% All goals in rule body are satisfied. The original goal list is now empty %%
        Resolver->>Resolver: Pop empty goal list from stack
        Resolver->>Engine: yield final_bindings

    end

    Engine->>Engine: Format solution, check for uniqueness
    Engine-->>-App: async for sol in solutions: yield solution_dict

    %% Example of an async built-in call
    loop Another Query
        App->>Engine: await query("http_get_json", url, "?R")
        %% ... setup is similar ... %%
        Resolver->>Resolver: Pop goal: [http_get_json(...)]
        Resolver->>+Builtin: await http_get_json(goal, bindings)
        note over Builtin: Makes async HTTP call via aiohttp. <br/> Event loop is free to run other tasks.
        Builtin-->>-Resolver: yield new_bindings_with_json_data
        %% ... proof continues ... %%
    end
```

## Key Features

-   😎**Fully Asynchronous**: Built on `asyncio` to handle I/O-bound tasks without blocking.
-   👀**Structured Logging**: Integrated with `loguru` for powerful and configurable tracing and debugging.
-   ⚙️**External Configuration**: Load facts and rules from human-readable YAML files.
-   🪜**Extensible Async Built-ins**: Easily write custom Python `async` functions to extend the engine's logic (e.g., for database access, API calls).
-   🚀**Robust and Thread-Safe**: The query resolution process is stateless, allowing for safe concurrent querying from multiple async tasks.
-   🧰**Control & Safety**: Prevents infinite loops with configurable search depth and limits the number of solutions.

## Installation

To install the library and its dependencies from the project root, run:
```bash
uv sync
```

## Quick Start

1.  **Define your knowledge in a YAML file (`knowledge.yaml`):**

    ```yaml
    facts:
      - [parent, david, john]
      - [parent, john, mary]

    rules:
      - head: [grandparent, '?GP', '?GC']
        body:
          - [parent, '?GP', '?P']
          - [parent, '?P', '?GC']
    ```

2.  **Write your async Python script:**

    ```python
    import asyncio
    from siamese import RuleEngine

    async def main():
        # Initialize the engine
        engine = RuleEngine()

        # Load knowledge from the file
        engine.load_from_file("knowledge.yaml")
        print("Knowledge base loaded.")

        # Asynchronously query the engine
        print("Query: Who is David's grandchild?")
        solutions = await engine.query("grandparent", "david", "?GC")
        
        async for sol in solutions:
            print(f"  - Solution: {sol}")

    if __name__ == "__main__":
        asyncio.run(main())
    ```

## Advanced Features

### Async Built-ins

The engine supports custom async built-in functions for external I/O operations:

```python
async def my_custom_builtin(goal, bindings):
    # Perform async operations like database queries or API calls
    result = await some_async_operation()
    if result:
        new_bindings = bindings.copy()
        new_bindings[goal.args[0]] = result
        yield new_bindings

# Register your custom built-in
engine = RuleEngine(builtins={"my_builtin": my_custom_builtin})
```

### Structured Logging

Configure detailed tracing of the engine's reasoning process:

```python
engine.configure_logging(level="TRACE")  # For detailed tracing
engine.configure_logging(level="INFO")   # For production use
```

### External Knowledge Bases

Load complex knowledge bases from YAML files:

```yaml
facts:
  - [person, alice]
  - [person, bob]
  - [parent, alice, bob]

rules:
  - head: [ancestor, '?A', '?D']
    body:
      - [parent, '?A', '?D']
  - head: [ancestor, '?A', '?D']
    body:
      - [parent, '?A', '?P']
      - [ancestor, '?P', '?D']
```

## License

MIT License - see LICENSE file for details. 