# Component Methods

## Dashboard UI
- `render_transaction_table()`: Displays the local ₹ transactions using Streamlit dataframe widgets.
- `trigger_ai_analysis(tx_id)`: Pushes a request to analyze a specific row and expand the results in an alert panel.
- `update_rule_weights(weights)`: Form payload sent to backend API to modify fraud parameters.

## Backend API
- `POST /api/v1/analyze_transaction`: Routes individual transaction context data to Gemini proxy.
- `POST /api/v1/generate_synthetic_data`: Triggers the Core Logic synthetic database populator.
- `PUT /api/v1/rules`: Updates SQLite configuration payload.

## Core Logic Engine
- `calculate_risk_score(transaction, rules)`: Outputs 0-100 weighted average score.
- `evaluate_velocity(tx_history, new_tx, threshold)`: Evaluates time-bound frequency rules.
- `generate_transactions(count)`: Emits synthetic payloads inside ₹ context.
