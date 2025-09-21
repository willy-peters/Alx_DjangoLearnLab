# Security Summary — LibraryProject (bookshelf)

## High-level measures implemented
- DEBUG set to False in production.
- CSRF and session cookies marked secure (CSRF_COOKIE_SECURE, SESSION_COOKIE_SECURE).
- Security-related headers set:
  - X-Frame-Options: DENY
  - X-Content-Type-Options: nosniff
  - X-XSS-Protection: enabled
  - Content-Security-Policy header via custom middleware (bookshelf.middleware.ContentSecurityPolicyMiddleware)
- All forms use CSRF tokens. Use `{% csrf_token %}` in templates.
- All user input validated via Django Forms (`bookshelf/forms.py`) and ORM queries are used (no raw SQL).
- Use Django auto-escaping in templates; avoid `|safe` unless input is sanitized.

## Testing checklist (manual)
1. Start the site with HTTPS locally (use mkcert / dev certs) and verify:
   - Cookies have `Secure` flag.
   - `Content-Security-Policy` header is present.
   - `X-Frame-Options` header equals `DENY`.
2. Forms:
   - Submit a form without CSRF token and verify the server rejects it (403).
   - Submit a search with SQL-like payloads (e.g., `'; DROP TABLE books; --`) — should not succeed or crash.
3. XSS:
   - Attempt to inject `<script>alert(1)</script>` into form fields — content should be escaped in output and not executed.
4. HSTS:
   - Confirm `Strict-Transport-Security` header is present when HTTPS is used.
5. CSRF/Session:
   - Confirm cookies are not exposed over HTTP and cannot be read by JS (Session cookie is HttpOnly).

## Notes
- `DEBUG=False` requires proper `ALLOWED_HOSTS`.
- When using third-party services (Google Fonts, analytics), update the CSP middleware to allow those hosts explicitly.
