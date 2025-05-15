# cia_threat_model_example.md

## CIA Triad Definitions

- **Confidentiality**: Ensuring only authorized access to data.
- **Integrity**: Preventing unauthorized modifications to data.
- **Availability**: Ensuring systems and data are accessible when needed.

## Threat Example (Online Banking)

| Asset                | Threat                          | CIA Impact        | Mitigation                            |
|---------------------|----------------------------------|-------------------|----------------------------------------|
| Account credentials | Phishing email                   | Confidentiality   | MFA, user training                     |
| Transaction records | Database injection               | Integrity         | Input validation, WAF                  |
| Website login       | DDoS attack                      | Availability      | Load balancing, CDN, DDoS mitigation   |
