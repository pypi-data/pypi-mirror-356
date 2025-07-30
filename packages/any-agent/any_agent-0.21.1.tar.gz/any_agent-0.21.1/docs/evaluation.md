# Agent Evaluation

!!! warning

    The codebase for evaluation is under development and is not yet stable. Use with caution,
    we welcome contributions.

Evaluation using any_agent.evaluation is designed to be a "trace-first" evaluation. The evaluation of a trace
is not designed to be pass/fail, but is rather a score based on the achievement of user-defined criteria for
each example. Agent systems are hyper-specific to each use case, and it's difficult to provide a single set of metrics
that would reliably provide the insight needed to make a decision about the effectiveness of an agent.

Using any-agent evaluation, you can specify any criteria you wish, and through the LLM-as-a-judge technique, any-agent will
evaluate which criteria are satisfied.

## Example

Using the unified tracing format provided by any-agent's [tracing functionality](./tracing.md), the trace can be evaluated
with user defined criteria. The steps for evaluating an agent are as follows:

### Run an agent using any-agent, which will produce a trace. For example

```python
from any_agent import AgentConfig, AnyAgent
from any_agent.tools import search_web

agent = AnyAgent.create(
    "langchain",
    AgentConfig(
        model_id="gpt-4o-mini",
        tools=[search_web]
    ),
)

agent_trace = agent.run("How many seconds would it take for a leopard at full speed to run through Pont des Arts?")
```


### Define an evaluation case either in a yaml file or in python:

=== "YAML"
    ~~~yaml
    {% include "./examples/evaluation_case.yaml" %}
    ~~~
    Then in python
    ```python
    from any_agent.evaluation.evaluation_case import EvaluationCase
    evaluation_case = EvaluationCase.from_yaml(evaluation_case_path)
    ```

=== "Python"
    ```python
    from any_agent.evaluation.evaluation_case import EvaluationCase
    evaluation_case = EvaluationCase(
            ground_truth={ "value": "9", "points": 1.0},
            checkpoints=[
                {"criteria": "Did the agent run a calculation", "points": 1},
                {"criteria": "Did the agent use fewer than 5 steps", "points": 4},
            ],
            llm_judge="gpt-4o-mini",
    )
    ```

### Run the evaluation using the test case and trace

=== "Python"
    ```python
    from any_agent.evaluation.evaluate import evaluate
    eval_result = evaluate(
        evaluation_case=evaluation_case,
        trace=agent_trace
    )
    print(f"Final score: {eval_result.score}")
    print(f"Checkpoint scores: {eval_result.checkpoint_results}")
    ```

=== "CLI"
    ```bash
    any-agent-evaluate \
        --evaluation_case_path "docs/examples/evaluation_case.yaml" \
        --trace_path "tests/assets/OPENAI_trace.json"
    ```
