# Orchestration Patterns

| Situation | Pattern | Example |
|---|---|---|
| One transformation, no collaboration | Single agent | `atomic-examples/quickstart/` |
| Stages where each refines the last | Sequential pipeline | `atomic-examples/deep-research/` |
| Independent lookups, run at the same time | Parallel fan-out | see parallel-models.md |
| Classify request, then route | Router | `atomic-examples/orchestration-agent/` |
| Quality gate / iterative refinement | Supervisor | — |
| Large tool catalog (dozens+) | Search + execute | `atomic-examples/progressive-disclosure/` |

Start minimal; compose only when the simpler shape stops working.

## Sequential pipeline

Each stage's output is the next stage's input. Use typed adapters when shapes don't align.
```python
extracted = extractor.run(RawDoc(text=doc))
scored    = scorer.run(ScoreQuery(entities=extracted.entities))
summary   = summarizer.run(SummaryReq(scored=scored))
```

## Parallel fan-out

```python
import asyncio
docs, users = await asyncio.gather(
    doc_agent.run_async(DocLookup(q=query)),
    user_agent.run_async(UserLookup(q=query)),
)
return await summary_agent.run_async(Summary(docs=docs.items, users=users.items))
```

Each concurrent agent gets its **own** `ChatHistory` (or none). Sharing one corrupts state.

## Router

```python
from typing import Literal, Union
class BillingRoute(BaseIOSchema):
    """Route to the billing agent."""
    topic: Literal["billing"] = "billing"
    normalized_question: str = Field(..., description="Rewritten for the billing agent.")

class Routing(BaseIOSchema):
    """Routing decision."""
    choice: Union[BillingRoute, TechRoute] = Field(..., description="Routed agent and payload.")

decision = router.run(query)
reply = billing_agent.run(...) if isinstance(decision.choice, BillingRoute) else tech_agent.run(...)
```

## Supervisor / validate-and-retry

```python
draft = writer.run(DraftRequest(topic="X"))
for _ in range(3):                       # cap the loop — bad prompts oscillate
    verdict = reviewer.run(ReviewReq(draft=draft.text))
    if verdict.accept: break
    draft = writer.run(DraftRequest(topic="X", revise_notes=verdict.notes))
```

## Shared context between agents

Register the **same** provider instance on multiple agents; updates propagate. Cheaper
than threading session state through every schema.

## Common mistakes

- Sharing `ChatHistory` between parallel agents.
- Hidden coupling via globals/files — use a context provider or explicit schema.
- Router returning free-text "topic" instead of a discriminated union.
- Unbounded supervisor loops.
- Pipelines silently dropping fields between stages.
