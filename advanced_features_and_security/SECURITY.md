# Security Configuration – LibraryProject

## HTTPS Enforcement
- `SECURE_SSL_REDIRECT = True` ensures all traffic is redirected to HTTPS.
- HSTS is enabled (`SECURE_HSTS_SECONDS = 31536000`, `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`, `SECURE_HSTS_PRELOAD = True`) to instruct browsers to only use HTTPS.

## Secure Cookies
- `SESSION_COOKIE_SECURE = True` and `CSRF_COOKIE_SECURE = True` enforce cookies over HTTPS only.

## Security Headers
- `X_FRAME_OPTIONS = "DENY"` prevents clickjacking.
- `SECURE_CONTENT_TYPE_NOSNIFF = True` blocks MIME-type sniffing.
- `SECURE_BROWSER_XSS_FILTER = True` enables browser-side XSS protection.

## Deployment
- Configured SSL/TLS certificates (via Let’s Encrypt) in Nginx.
- HTTP traffic is redirected to HTTPS.

## Review
These settings ensure:
- Encrypted client-server communication.
- Mitigation of clickjacking, XSS, and MIME-type attacks.
- Strict HTTPS-only access via HSTS.

Potential Improvements:
- Implement Content Security Policy (CSP) headers for stronger XSS mitigation.
- Use security monitoring tools (e.g., Mozilla Observatory, OWASP ZAP).
