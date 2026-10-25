# Agent Flow Diagram

Full flow of one event-planning request through the guarded, orchestrated, evaluated
multi-agent system (`Task3.ipynb` orchestrator + `Task4.ipynb` evaluator + `Task5.ipynb`
guardrails combined).

## ASCII

```
Raw user request
      │
      ▼
┌───────────────────────────┐
│   Input Guardrail          │  off_topic / harmful -> BLOCKED, no agent called
│   (on_topic? classifier)   │
└─────────────┬───────────────┘
              │ on_topic
              ▼
      ┌───────────────┐
      │ existing_venue │
      │   set?         │
      └───┬───────┬───┘
     yes  │        │ no
          ▼        ▼
     ┌─────────┐ ┌────────────┐          ┌───────────────────────────┐
     │  Skip    │ │ VenueAgent │          │  CateringLogisticsAgent   │ (independent -
     │ VenueAgent│ │(cost-capped)│         │      (cost-capped)        │  runs in parallel
     └────┬────┘ └─────┬──────┘          └─────────────┬─────────────┘  with venue/AV)
          │            │  ──────► Evaluator (score, retry once, else escalate) ─────┐
          └─────┬──────┘                                                            │
                ▼                                                                   │
      ┌───────────────────────────┐                                                 │
      │ AVVendorCoordinationAgent  │ ──────► Evaluator (score, retry once, else     │
      │       (cost-capped)        │          escalate)                             │
      └─────────────┬───────────────┘                                               │
                     │                                                              │
                     └───────────────────────────┬──────────────────────────────────┘
                                                  ▼
                                      ┌───────────────────────────┐
                                      │   AgendaAssemblyAgent      │ (join: venue + catering + av)
                                      │       (cost-capped)        │
                                      └─────────────┬───────────────┘
                                                    │ ──────► Evaluator (score, retry once,
                                                    │          else escalate)
                                                    ▼
                                      ┌───────────────────────────┐
                                      │    Output Guardrail        │
                                      │ (timeline feasibility +    │
                                      │  venue/location checks)    │
                                      └─────┬───────────────┬───────┘
                                       fail  │               │ pass
                                            ▼                ▼
                                  Flagged for human    Final RunOfShow
                                      review              returned

Cost-Cap Guard wraps every single LLM call above (venue/catering/AV/agenda/evaluator/
classifier) and aborts the whole pipeline BEFORE any call that would push estimated spend
over the configured cap, returning a graceful user-facing message instead.
```

## Mermaid

```mermaid
flowchart TD
    REQ[Raw user request] --> IG{Input Guardrail\non_topic?}
    IG -- off_topic / harmful --> BLOCK[Blocked - no agent called]
    IG -- on_topic --> COND{existing_venue set?}

    COND -- yes --> SKIP[Skip VenueAgent]
    COND -- no --> VENUE[VenueAgent]
    REQ -. parallel branch .-> CATER[CateringLogisticsAgent]

    SKIP --> EVALV[Evaluator]
    VENUE --> EVALV
    EVALV -- score below threshold --> RETRYV[Retry agent]
    RETRYV --> EVALV
    EVALV -- still failing --> ESCV[Escalate to human review]
    EVALV -- passed --> AV[AVVendorCoordinationAgent]

    AV --> EVALAV[Evaluator]
    CATER --> EVALC[Evaluator]

    EVALAV --> AGENDA[AgendaAssemblyAgent]
    EVALC --> AGENDA

    AGENDA --> EVALA[Evaluator]
    EVALA --> OG{Output Guardrail\ntimeline + venue/location checks}
    OG -- violation --> FLAG[Flagged for human review]
    OG -- pass --> PLAN[Final RunOfShow]

    CC[[CostCapGuard wraps every LLM call]] -. aborts before cap .-> VENUE
    CC -. aborts before cap .-> CATER
    CC -. aborts before cap .-> AV
    CC -. aborts before cap .-> AGENDA
```
