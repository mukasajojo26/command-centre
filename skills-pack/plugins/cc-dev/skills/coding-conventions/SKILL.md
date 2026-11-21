---
name: coding-conventions
description: Opinionated conventions for JavaScript and TypeScript projects (pnpm, ESLint flat config, Vitest, ESM, tsconfig, monorepos, library publishing, Vue and Vite). Use when scaffolding a new JS/TS app or library, setting up linting and tests, choosing tooling, or reviewing a repo's setup for consistency.
---

# Coding Conventions (JS/TS)

A fixed set of defaults so every new project starts the same way. Deviate only when the repo already uses something else: match the existing repo first.

## Defaults

| Area | Default | Why |
|---|---|---|
| Package manager | pnpm (pin with `"packageManager"` in package.json) | Fast, strict, good workspaces |
| Module format | ESM only (`"type": "module"`) | One format, fewer edge cases |
| Language | TypeScript, `strict: true` | Catch errors before runtime |
| Lint + format | ESLint flat config (`eslint.config.js`), no separate Prettier | One tool, one config |
| Tests | Vitest | Vite-native, Jest-compatible API |
| Build (libs) | tsdown or unbuild | Zero-config dual output when needed |
| Build (apps) | Vite | Fast dev server, sane defaults |
| Node | Current LTS, set in `.nvmrc` and `engines` | Reproducible |
| Releases | `bumpp` + changelog from conventional commits | Simple, auditable |

## New project checklist

1. `pnpm init`, set `"type": "module"`, `"packageManager": "pnpm@<version>"`, `"engines": { "node": ">=20" }`.
2. `tsconfig.json`:
   ```json
   {
     "compilerOptions": {
       "target": "ES2022", "module": "ESNext", "moduleResolution": "Bundler",
       "strict": true, "noUncheckedIndexedAccess": true, "skipLibCheck": true,
       "esModuleInterop": true, "resolveJsonModule": true, "verbatimModuleSyntax": true
     }
   }
   ```
3. `eslint.config.js` with a shared config (for example `@antfu/eslint-config`) or a minimal typescript-eslint setup. Scripts: `"lint": "eslint ."`, `"lint:fix": "eslint . --fix"`.
4. Vitest: `"test": "vitest"`. Test files sit beside source as `*.test.ts`.
5. `.gitignore`: `node_modules`, `dist`, `coverage`, `.env*` (but commit `.env.example`).
6. CI (GitHub Actions): install with `pnpm install --frozen-lockfile`, then `lint`, `typecheck` (`tsc --noEmit`), `test --run`.
7. Add `README.md` with: what it does, install, one usage example, scripts.

## Code style rules

- Named exports over default exports (easier refactors and grep).
- Small pure functions. Side effects at the edges.
- `const` by default. No `var`.
- Prefer `unknown` over `any`. Narrow with type guards.
- Errors: throw `Error` subclasses with a clear message. Never swallow errors silently.
- File names: `kebab-case.ts`. Types and classes: `PascalCase`. Functions and variables: `camelCase`. Constants: `UPPER_SNAKE` only for true constants.
- Imports ordered: node built-ins, external, internal, relative. Let the linter sort them.
- Comments explain why, not what.

## Security defaults (always apply)

- Never commit secrets. Read from env, validate at startup (zod or valibot schema).
- `pnpm audit` in CI. Pin GitHub Actions to a commit SHA, not a tag.
- Sanitize any HTML you render from user input. No `innerHTML` with untrusted data.
- Lockfile committed. Review new dependencies: weekly downloads, maintainer count, last publish date, install scripts.

## Monorepo

- `pnpm-workspace.yaml` with `packages/*`.
- Shared configs in the root. Each package has its own `package.json` scripts.
- Use `workspace:*` for internal deps.

## Review mode

When asked to review a repo's setup, output a table: Area, Current, Recommended, Effort (S/M/L), Risk if ignored. Then the top 3 changes to make first.
