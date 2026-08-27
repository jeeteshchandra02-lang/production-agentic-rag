# Enterprise security overview

The platform supports SSO using SAML 2.0 and OpenID Connect for enterprise
customers.

Customer data is encrypted in transit using TLS 1.2 or later and encrypted at
rest using AES-256.

Administrative actions are written to an audit log. Audit records include the
actor, action, target resource and timestamp.

Enterprise customers can configure role-based access control. Access policies
should follow least privilege and are evaluated before protected resources are
returned.
