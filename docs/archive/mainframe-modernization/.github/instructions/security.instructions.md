---
description: "Use when implementing or reviewing authentication, authorization, crypto, secure configuration, secrets handling, and security-sensitive code."
applyTo: "backend/src/main/java/**/auth/**,backend/src/main/java/**/security/**,backend/src/main/java/**/config/**,backend/src/main/resources/**,frontend/**/auth/**,frontend/**/middleware.ts"
---

# Security Conventions — Auth, Secrets, and Injection

This file activates on security-sensitive code: `auth/`, `security/`, and `config/` packages, everything under `backend/src/main/resources/`, plus `frontend/**/auth/**` and `frontend/middleware.ts`. It teaches authentication, authorization, input validation, CORS, secret handling, and sensitive-data protection following the repo's OWASP Top 10 rules. Generic REST shape lives in [`backend.instructions.md`](backend.instructions.md); Terraform secret storage lives in [`infrastructure.instructions.md`](infrastructure.instructions.md).

## Authentication (OAuth2 / JWT)

The backend is a stateless OAuth2 resource server validating JWTs via Spring Security. Never hand-roll token parsing or crypto.

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
class SecurityConfig {

    @Bean
    SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/actuator/health").permitAll()
                .anyRequest().authenticated())
            .oauth2ResourceServer(oauth -> oauth.jwt(Customizer.withDefaults()))
            .cors(Customizer.withDefaults())
            .csrf(csrf -> csrf.disable()); // stateless token API; no session cookie
        return http.build();
    }
}
```

If passwords are ever stored, hash with argon2 or bcrypt (never a bare digest), rate-limit login, and require MFA for administrators.

## Authorization

Authorize every request, deny by default, and enforce the least privilege. Use method security for role checks and verify resource ownership explicitly.

```java
@PreAuthorize("hasRole('AUDITOR')")
public AuditReport generate(UUID resourceId, Authentication principal) {
    Resource resource = resourceService.getOwned(resourceId, principal.getName());
    // ownership is checked in the service; a role alone is not enough
    return AuditReport.of(resource);
}
```

## Input Validation and Injection

Validate at every boundary with `@Valid` (see [`backend.instructions.md`](backend.instructions.md)). Build queries only with JPA/JPQL bound parameters, escape HTML on output, and validate uploads by type and size.

> [!WARNING]
> Never concatenate user input into a query, a shell command, or markup. String-built SQL is the classic injection vector; parameter binding is not optional.

## CORS

Configure allowed origins explicitly. A `*` wildcard is forbidden in production.

```java
@Bean
CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration config = new CorsConfiguration();
    config.setAllowedOrigins(List.of("https://app.example.gov.br")); // never "*" in prod
    config.setAllowedMethods(List.of("GET", "POST", "PUT", "PATCH", "DELETE"));
    config.setAllowedHeaders(List.of("Authorization", "Content-Type"));
    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/api/**", config);
    return source;
}
```

## Secrets and Secure Config

No secret is hardcoded, committed, or logged. Read secrets from the environment or Key Vault; authenticate Azure service-to-service with Managed Identity. In the frontend, only non-secret values may use the `NEXT_PUBLIC_` prefix — anything prefixed is shipped to the browser.

## Sensitive Data (CPF, Amounts)

> [!IMPORTANT]
> Mask regulated fields (CPF, benefit amounts) in logs, error responses, and URLs. Never place them in query strings or unencrypted storage, and always transmit over TLS.

```java
// keep the first 3 and last 2 digits of an 11-digit CPF
String masked = cpf.replaceAll("(\\d{3})\\d{6}(\\d{2})", "$1******$2");
```

## Frontend Auth Boundary (`middleware.ts`)

Gate protected routes in middleware; never trust the client to enforce access. Keep tokens and secrets server-side.

```ts
import { NextResponse, type NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const session = request.cookies.get('session');
  if (!session) return NextResponse.redirect(new URL('/login', request.url));
  return NextResponse.next();
}

export const config = { matcher: ['/dashboard/:path*'] };
```

## Automation and Agent Boundaries

An AI agent or automation never grants itself new permissions and never touches a production database without explicit human approval. Changes to auth, roles, or secret handling require peer review before merge.

## Conventions

| Rule | Rationale |
|---|---|
| OAuth2/JWT via Spring Security | No custom, error-prone auth code |
| Authorize every request, deny by default | Least privilege at each boundary |
| JPA/JPQL bound parameters only | Eliminates SQL injection |
| Explicit CORS origins, no `*` in prod | Blocks cross-origin abuse |
| Secrets from env/Key Vault, Managed Identity | No credentials in code or logs |
| Mask CPF and amounts everywhere | Protects regulated data |

## Do / Do Not

| Do | Do not |
|---|---|
| Hash passwords with argon2/bcrypt | Store or log plaintext or a bare digest |
| Check role **and** resource ownership | Treat a role as sufficient authorization |
| Keep secrets server-side | Prefix a secret with `NEXT_PUBLIC_` |
| Mask sensitive fields before logging | Put CPF/amounts in logs or query strings |

## Checklist Before Opening a PR

- [ ] Endpoints authenticate via Spring Security; no custom token parsing
- [ ] Every request is authorized, denying by default, with ownership checks where relevant
- [ ] All queries use bound parameters; uploads and inputs are validated
- [ ] CORS lists explicit origins; no `*` in production configuration
- [ ] No secret is hardcoded, committed, or logged; Azure auth uses Managed Identity
- [ ] CPF, amounts, and tokens are masked in logs, errors, and URLs
