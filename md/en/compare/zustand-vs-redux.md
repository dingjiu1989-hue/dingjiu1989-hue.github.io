---
title: "Zustand vs Redux vs Jotai"
description: "Compare Zustand, Redux, and Jotai for React state management — API design, boilerplate, performance, and which state manager fits your project."
date: 2026-05-14
board: compare
url: https://dingjiu1989-hue.github.io/en/compare/zustand-vs-redux.html
---

# Zustand vs Redux vs Jotai

## Introduction

React state management has evolved significantly. Redux, once the default choice for complex applications, now competes with simpler alternatives like Zustand and Jotai. Each takes a different approach: Redux centralizes state with strict patterns, Zustand provides a minimal store with hooks, and Jotai offers atomic, Recoil-inspired state management. This comparison helps you choose the right state management approach.

## Redux Toolkit

Redux Toolkit (RTK) is Redux's modern incarnation, eliminating much of the boilerplate that plagued classic Redux.

**Philosophy:** Single centralized store with predictable updates through reducers and actions.

import { createSlice, configureStore } from "@reduxjs/toolkit";

const counterSlice = createSlice({

name: "counter",

initialState: { value: 0 },

reducers: {

increment: (state) => { state.value += 1; },

incrementBy: (state, action) => { state.value += action.payload; },

},

});

const store = configureStore({

reducer: { counter: counterSlice.reducer },

});

export const { increment, incrementBy } = counterSlice.actions;

export type RootState = ReturnType;

// In component:

function Counter() {

const count = useSelector((state: RootState) => state.counter.value);

const dispatch = useDispatch();

return (

{count}

dispatch(increment())}>+1

);

}

**Strengths:**

  * Mature ecosystem with middleware (Redux Thunk, Redux Saga)

  * DevTools with time-travel debugging

  * TypeScript integration is excellent with RTK

  * Clear patterns for large teams

  * Well-documented for complex async flows




**Weaknesses:**

  * Conceptual overhead (actions, reducers, dispatch, selectors)

  * More boilerplate than alternatives (even with RTK)

  * Selectors need memoization for performance

  * Centralized store can become a bottleneck in very large apps




## Zustand

Zustand provides a minimal store with React hooks, no providers needed.

**Philosophy:** A small, fast, and scalable state management solution with no boilerplate.

import { create } from "zustand";

interface CounterState {

count: number;

increment: () => void;

incrementBy: (amount: number) => void;

}

const useCounterStore = create((set) => ({

count: 0,

increment: () => set((state) => ({ count: state.count + 1 })),

incrementBy: (amount) => set((state) => ({ count: state.count + amount })),

}));

// In component — no Provider needed

function Counter() {

const count = useCounterStore((state) => state.count);

const increment = useCounterStore((state) => state.increment);

return (

{count}

+1

);

}

**Strengths:**

  * Minimal boilerplate — create a store, use it

  * No Provider wrapping needed

  * Subscription-based rendering (only re-renders on accessed state)

  * Simple async actions (no middleware needed)

  * Tiny bundle size (~1KB)

  * Works outside React (vanilla JS stores)




**Weaknesses:**

  * Fewer middleware options than Redux

  * Less structure for large teams (can lead to inconsistent patterns)

  * DevTools require additional setup

  * No built-in data fetching or caching (unlike RTK Query or TanStack Query)




## Jotai

Jotai takes an atomic approach — each piece of state is an independent atom.

**Philosophy:** Build state by composing primitive atoms, much like React's useState but shared.

import { atom, useAtom } from "jotai";

// Primitive atom

const countAtom = atom(0);

// Derived atom (computed state)

const doubleCountAtom = atom((get) => get(countAtom) * 2);

// Async atom

const userAtom = atom(async () => {

const response = await fetch("/api/user");

return response.json();

});

// In component

function Counter() {

const [count, setCount] = useAtom(countAtom);

const [doubleCount] = useAtom(doubleCountAtom);

return (

Count: {count}

Double: {doubleCount}

setCount((c) => c + 1)}>+1

);

}

**Strengths:**

  * Granular re-renders (only components using a specific atom re-render)

  * Built-in async atoms (no middleware for async)

  * Composable atoms for derived state

  * Tiny bundle size (~3KB)

  * No global store or Provider needed




**Weaknesses:**

  * Less mature ecosystem than Redux

  * Atomic approach can be unfamiliar to new team members

  * Debugging can be harder with many small atoms

  * SSR requires additional configuration




## Comparison Table

| Aspect | Redux Toolkit | Zustand | Jotai |

|--------|--------------|---------|-------|

| Architecture | Centralized store | Multiple stores | Atomic atoms |

| Boilerplate | Moderate | Minimal | Minimal |

| Bundle size | ~12KB | ~1KB | ~3KB |

| Learning curve | Steep | Gentle | Moderate |

| DevTools | Built-in | Add-on | Add-on |

| Middleware | Rich ecosystem | Immer, persist | None needed |

| Async support | Thunks/Sagas | Native in store | Native atoms |

| TypeScript | Excellent | Excellent | Good |

| Provider needed | Yes | No | No (optional) |

| External use | Yes (store) | Yes (store) | Limited |

## When to Choose What

**Choose Redux Toolkit when:**

  * You're building a large application with a big team

  * You need established patterns and clear structure

  * You want RTK Query for data fetching and caching

  * Your team already knows Redux patterns

  * You need time-travel debugging and rich middleware




**Choose Zustand when:**

  * You want minimal boilerplate and fast setup

  * You need a simple, performant store

  * You're building a medium-sized application

  * You want state management without Provider nesting

  * You need to access state outside React components




**Choose Jotai when:**

  * You want React-idiomatic state (atoms = useState + useContext)

  * You need fine-grained re-renders

  * You want built-in async support

  * You're building an app with many small, independent state pieces

  * You want composeable state without a global store




## Conclusion

The state management landscape in 2026 has moved beyond "one size fits all." Redux Toolkit remains the right choice for large applications that need structure and a rich ecosystem. Zustand has become the default recommendation for most new React projects due to its simplicity and performance. Jotai offers the most React-idiomatic experience for applications with highly granular state needs. Consider your team size, application complexity, and whether you need data fetching (RTK Query) or async workflows (Jotai's async atoms) when making your choice.

**See also:** [GraphQL vs REST API](</en/compare/graphql-vs-rest.html>), [Linear vs Jira vs GitHub Issues: Project Management, Workflows, Integrations, and Team Size Fit](</en/compare/linear-vs-jira.html>), [Playwright vs Cypress](</en/compare/playwright-vs-cypress.html>).

**See also:** [GraphQL vs REST API](</en/compare/graphql-vs-rest.html>), [Playwright vs Cypress](</en/compare/playwright-vs-cypress.html>), [Turbopack vs Vite](</en/compare/turbopack-vs-vite.html>)

**See also:** [GraphQL vs REST API](</en/compare/graphql-vs-rest.html>), [Playwright vs Cypress](</en/compare/playwright-vs-cypress.html>), [Turbopack vs Vite](</en/compare/turbopack-vs-vite.html>)

**See also:** [GraphQL vs REST API](</en/compare/graphql-vs-rest.html>), [Playwright vs Cypress](</en/compare/playwright-vs-cypress.html>), [Turbopack vs Vite](</en/compare/turbopack-vs-vite.html>)

**See also:** [GraphQL vs REST API](</en/compare/graphql-vs-rest.html>), [Playwright vs Cypress](</en/compare/playwright-vs-cypress.html>), [Turbopack vs Vite](</en/compare/turbopack-vs-vite.html>)

**See also:** [GraphQL vs REST API](</en/compare/graphql-vs-rest.html>), [Playwright vs Cypress](</en/compare/playwright-vs-cypress.html>), [Turbopack vs Vite](</en/compare/turbopack-vs-vite.html>)

**See also:** [AWS vs Azure vs GCP 2026](</en/compare/aws-vs-azure-vs-gcp-2026.html>), [Zustand vs Redux vs Jotai: Best React State Management in 2026?](</en/compare/zustand-vs-redux-vs-jotai.html>), [Terraform vs Pulumi: Infrastructure as Code Compared](</en/compare/terraform-vs-pulumi.html>)

**See also:** [AWS vs Azure vs GCP 2026](</en/compare/aws-vs-azure-vs-gcp-2026.html>), [Zustand vs Redux vs Jotai: Best React State Management in 2026?](</en/compare/zustand-vs-redux-vs-jotai.html>), [Terraform vs Pulumi: Infrastructure as Code Compared](</en/compare/terraform-vs-pulumi.html>)

**See also:** [AWS vs Azure vs GCP 2026](</en/compare/aws-vs-azure-vs-gcp-2026.html>), [Zustand vs Redux vs Jotai: Best React State Management in 2026?](</en/compare/zustand-vs-redux-vs-jotai.html>), [Terraform vs Pulumi: Infrastructure as Code Compared](</en/compare/terraform-vs-pulumi.html>)

**See also:** [AWS vs Azure vs GCP 2026](</en/compare/aws-vs-azure-vs-gcp-2026.html>), [Zustand vs Redux vs Jotai: Best React State Management in 2026?](</en/compare/zustand-vs-redux-vs-jotai.html>), [Terraform vs Pulumi: Infrastructure as Code Compared](</en/compare/terraform-vs-pulumi.html>)

**See also:** [AWS vs Azure vs GCP 2026](</en/compare/aws-vs-azure-vs-gcp-2026.html>), [Zustand vs Redux vs Jotai: Best React State Management in 2026?](</en/compare/zustand-vs-redux-vs-jotai.html>), [Terraform vs Pulumi: Infrastructure as Code Compared](</en/compare/terraform-vs-pulumi.html>)

**See also:** [AWS vs Azure vs GCP 2026](</en/compare/aws-vs-azure-vs-gcp-2026.html>), [Zustand vs Redux vs Jotai: Best React State Management in 2026?](</en/compare/zustand-vs-redux-vs-jotai.html>), [Terraform vs Pulumi: Infrastructure as Code Compared](</en/compare/terraform-vs-pulumi.html>)

**See also:** [AWS vs Azure vs GCP 2026](</en/compare/aws-vs-azure-vs-gcp-2026.html>), [Zustand vs Redux vs Jotai: Best React State Management in 2026?](</en/compare/zustand-vs-redux-vs-jotai.html>), [Terraform vs Pulumi: Infrastructure as Code Compared](</en/compare/terraform-vs-pulumi.html>)

**See also:** [AWS vs Azure vs GCP 2026](</en/compare/aws-vs-azure-vs-gcp-2026.html>), [Zustand vs Redux vs Jotai: Best React State Management in 2026?](</en/compare/zustand-vs-redux-vs-jotai.html>), [Terraform vs Pulumi: Infrastructure as Code Compared](</en/compare/terraform-vs-pulumi.html>)

**See also:** [AWS vs Azure vs GCP 2026](</en/compare/aws-vs-azure-vs-gcp-2026.html>), [Zustand vs Redux vs Jotai: Best React State Management in 2026?](</en/compare/zustand-vs-redux-vs-jotai.html>), [Terraform vs Pulumi: Infrastructure as Code Compared](</en/compare/terraform-vs-pulumi.html>)
