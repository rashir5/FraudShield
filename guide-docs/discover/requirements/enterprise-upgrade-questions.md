# enterprise-upgrade-questions.md

Please answer the following questions to help clarify the requirements for the Enterprise Upgrade.

## Question 1
For the **JWT-Based Authentication**, what is the preferred strategy for user management?

A) Simple single-user "Admin" account with hardcoded password in environment variables.
B) Full User Management system with registration, roles, and persistent database storage.
C) Integration with an external Identity Provider (Auth0, Firebase).
D) Other (please describe after [Answer]: tag below)

[Answer]: 

## Question 2
Regarding the **Real-time Alerting System** via WebSockets, how should the notification engine handle high-risk flags?

A) Push individual alerts instantly as they are processed in the batch.
B) Accumulate alerts and push a "Risk Summary" every N seconds.
C) Only push alerts for "HIGH" risk (score > 70), ignoring "MEDIUM" risk.
D) Other (please describe after [Answer]: tag below)

[Answer]: 

## Question 3
For the **Audit Logging & Trail**, what level of detail is required for the compliance reports?

A) Basic log: Action type, Timestamp, and User ID.
B) Detailed log: Component name, Old Value, New Value, Timestamp, and User ID.
C) Full Forensic log: Raw Request Body, Component State, User Session Details, and Outcome.
D) Other (please describe after [Answer]: tag below)

[Answer]: 

## Question 4
How should the **AI Explainability (XAI)** be triggered for high-risk flags?

A) Automatically for every "HIGH" risk detection during the batch process (increases API consumption).
B) Background task that processes flags asynchronously after the batch completes.
C) On-demand via the Dashboard (user clicks "Generate Explanation").
D) Other (please describe after [Answer]: tag below)

[Answer]: 
