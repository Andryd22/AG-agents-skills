---
name: typescript-expert
description: Advanced TypeScript patterns. Type-level programming, generics, infer, conditional types, template literals, mapped types, and strict configurations.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# TypeScript Expert

> Advanced type-level programming. Strict mode. Zero `any`. Type-driven development.

## Configuration

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "exactOptionalPropertyTypes": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

## Type Patterns

### Discriminated Unions
```typescript
type ApiState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: string };

function renderState(state: ApiState<User>) {
  switch (state.status) {
    case 'idle': return 'Ready.';
    case 'loading': return 'Loading...';
    case 'success': return `Hi ${state.data.name}`; // T inferred
    case 'error': return `Error: ${state.error}`;
  }
}
```

### Branded Types
```typescript
type UserId = string & { __brand: 'UserId' };
type PostId = string & { __brand: 'PostId' };

function getUser(id: UserId) { /* ... */ }

const userId = 'abc' as UserId;
getUser(userId); // ✅
getUser('abc'); // ❌ Type error
```

### Template Literal Types
```typescript
type EventName = `user.${'created' | 'updated' | 'deleted'}`;
// "user.created" | "user.updated" | "user.deleted"

type Route = `/${string}`;
type ApiRoute = `/api/${string}`;
```

### Conditional + Infer
```typescript
type PromiseValue<T> = T extends Promise<infer V> ? V : T;
type Unwrapped = PromiseValue<Promise<string>>; // string

type ArrayElement<T> = T extends (infer U)[] ? U : T;
type Item = ArrayElement<User[]>; // User
```

### Mapped Types
```typescript
type ReadonlyDeep<T> = {
  readonly [K in keyof T]: T[K] extends object ? ReadonlyDeep<T[K]> : T[K];
};

type PickByValue<T, V> = {
  [K in keyof T as T[K] extends V ? K : never]: T[K];
};
```

## Derive Types from Runtime

```typescript
const ROLES = ['admin', 'user', 'moderator'] as const;
type Role = (typeof ROLES)[number]; // "admin" | "user" | "moderator"

const config = { api: 'https://api.example.com', timeout: 5000 } as const;
```

## Type Guards

```typescript
function isUser(obj: unknown): obj is User {
  return typeof obj === 'object' && obj !== null && 'email' in obj && 'id' in obj;
}

const data: unknown = fetchData();
if (isUser(data)) {
  console.log(data.email); // data is User
}
```

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| `any` | `unknown` + type guard |
| Type assertion `as` everywhere | Proper inference or type guard |
| `@ts-ignore` | Fix the type error |
| `object` type | `Record<string, unknown>` or interface |
| `Function` type | Specific function signature |
| Enums with numbers | `as const` objects or string unions |

## Checklist

- [ ] `strict: true` in tsconfig
- [ ] Zero `any` types (use `unknown` with guards)
- [ ] Discriminated unions for state machines
- [ ] Return types explicit on public API functions
- [ ] Generic constraints (`extends`) used appropriately
- [ ] `noUncheckedIndexedAccess` enabled
