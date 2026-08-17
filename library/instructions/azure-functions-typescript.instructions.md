---
applyTo: '**/*.ts,**/*.js,**/host.json,**/local.settings.json,**/function.json,**/package.json'
description: 'Conventions for Azure Functions apps in TypeScript and JavaScript, including async Node.js patterns, dependency choices, and function configuration.'
---

# Azure Functions TypeScript Conventions

- Generate modern TypeScript code for Node.js
- Use `async/await` for asynchronous code
- Whenever possible, use Node.js v22 LTS built-in modules instead of external packages
- Always use Node.js async functions, like `node:fs/promises` instead of `fs` to avoid blocking the event loop
- Ask before adding any extra dependencies to the project
- The API is built using Azure Functions using `@azure/functions@4` package.
- Each endpoint should have its own function file, and use the following naming convention: `src/functions/<resource-name>-<http-verb>.ts`
- When making changes to the API, make sure to update the OpenAPI schema (if it exists) and `README.md` file accordingly.
