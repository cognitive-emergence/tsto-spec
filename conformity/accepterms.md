# Accepterms 2027

| Code | Judge | Determinability | Silence after the agreed window |
|---|---|---|---|
| SA | First party, subject to second-party objection | All | DEEMED_CONFORM |
| BD | Second party | All | DEEMED_CONFORM |
| MV | Third party | MACHINE or MEASURED | Not applicable; immediate judgment |
| TI | Third party | All | ESCALATE |
| BE | Second party | All | ESCALATE; remains open for explicit action |
| BR | Second party | All | DEEMED_NONCONFORM |

All except MV use judgmentWindow and defectNotificationPeriod. MV uses
defectNotificationPeriod. Durations are ISO 8601 elapsed durations. Days contain
86,400 seconds; calendar months and years do not have an implicit elapsed value.
The absolute deadline, when separately agreed and signed, prevails over a
derived duration. The source absolute deadline must be retained by its profile.

Rejections list defects together; a later unlisted defect cannot be asserted
under the same rejection, subject to the agreed defect-notification terms.
A deemed outcome requires a separate signed expiry event and an explicit claim
that the recorder holds the complete transaction log. It is never a fabricated
party J. The initial explicit-judgment producer uses BE and emits no expiry event.
