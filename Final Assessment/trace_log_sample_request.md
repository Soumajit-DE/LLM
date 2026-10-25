# End-to-End Trace Log - Sample Event Request

Source: `Task3.ipynb`, Section 6 ("Demo run 1 - full DAG, parallel venue/AV + catering
branches"). This is the full `EventPlanningOrchestrator` trace for one complete event request -
a 200-person product launch with no pre-booked venue, so all four agents are invoked, with the
catering branch running in parallel with the venue → AV branch.

## Request

```json
{
  "event_name": "Nova Product Launch",
  "event_type": "product_launch",
  "headcount": 200,
  "budget_usd": 250000,
  "location": "Austin",
  "event_date": "2026-11-18",
  "start_time": "09:00",
  "end_time": "14:00",
  "meal_period": "lunch",
  "dietary_restrictions": ["vegan", "gluten-free"],
  "special_requirements": ["livestream"]
}
```

## Trace log

```
Wall-clock time: 0.92s  (naive sequential estimate: 1.20s)

=== Trace log ===
[t= 0.000s] orchestrator   received request for 'Nova Product Launch'
[t= 0.001s] venue_agent    invoked
[t= 0.002s] catering_agent invoked (parallel branch)
[t= 0.309s] catering_agent completed (parallel branch)
[t= 0.311s] venue_agent    completed
[t= 0.311s] av_agent       invoked (routed venue choice 'Riverside Conference Center' / area 'ballroom')
[t= 0.613s] av_agent       completed
[t= 0.614s] agenda_agent   invoked (joins venue + catering + av)
[t= 0.916s] agenda_agent   completed
[t= 0.916s] orchestrator   final event plan assembled
```

The timestamps prove the parallel branch actually overlaps: `catering_agent` is invoked at
`t=0.002s` and completes at `t=0.309s`, entirely while `venue_agent` (invoked at `t=0.001s`) is
still running (it doesn't complete until `t=0.311s`) - the wall-clock time (0.92s) is
correspondingly faster than the naive sequential estimate (1.20s) of running all four agents
back-to-back.

## Final assembled plan

```json
{
  "event_name": "Nova Product Launch",
  "event_date": "2026-11-18",
  "selected_venue": "Riverside Conference Center",
  "run_of_show": [
    {
      "start_time": "07:00",
      "end_time": "09:00",
      "activity": "AV setup & sound check",
      "owner": "AV crew",
      "location": "Ballroom",
      "notes": null
    },
    {
      "start_time": "09:00",
      "end_time": "09:30",
      "activity": "Registration & welcome coffee",
      "owner": "Host",
      "location": "Foyer",
      "notes": null
    },
    {
      "start_time": "09:30",
      "end_time": "11:30",
      "activity": "Keynote & product reveal",
      "owner": "Host",
      "location": "Ballroom",
      "notes": "Livestreamed"
    },
    {
      "start_time": "11:30",
      "end_time": "13:00",
      "activity": "Plated lunch service",
      "owner": "Catering team",
      "location": "Ballroom",
      "notes": null
    },
    {
      "start_time": "13:00",
      "end_time": "14:00",
      "activity": "Teardown",
      "owner": "AV crew",
      "location": "Ballroom",
      "notes": null
    }
  ],
  "overall_notes": [
    "Vegan and gluten-free plated options confirmed with catering."
  ]
}
```
