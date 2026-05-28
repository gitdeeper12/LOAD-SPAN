# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**Please DO NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: **gitdeeper@gmail.com**

You should receive a response within 48 hours. If the issue is confirmed, we will release a patch as soon as possible.

## Security Features

LOAD-SPAN implements several security measures:

### Data Integrity
- SHA-256 checksums for all archival data
- Append-only record writing (no in-place modification)
- Tamper-evidence logging

### AI Output Safety
- Physics-constrained outputs (enforced bounds)
- Mandatory engineering verification requirement
- Uncertainty quantification for all AI predictions

### Access Control
- Environment-based configuration (no hardcoded secrets)
- JWT authentication for API endpoints
- Role-based access for dashboard features

### Code Security
- Regular dependency scanning (Dependabot)
- Pre-commit hooks for secret detection
- Static type checking with mypy

## Best Practices for Users

1. Never commit `.env` files to version control
2. Use strong, unique secrets in production
3. Keep the system updated to the latest version
4. Validate all AI outputs against physics-based analysis
5. Maintain regular backups of archival data

## Disclosure Policy

- Security vulnerabilities will be disclosed after a patch is available
- Credit will be given to reporters (unless anonymity requested)
- Full disclosure occurs 30 days after patch release

## Contact

Security Coordinator: Samir Baladi (gitdeeper@gmail.com)
