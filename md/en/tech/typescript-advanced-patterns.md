---
title: "Advanced TypeScript Patterns: Generics, Mapped Types, and Template Literals"
description: "Go beyond basic TypeScript with advanced patterns: conditional types, mapped types, template literal types, infer, and brand types. Real examples that make your code safer."
date: 2026-05-08
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/typescript-advanced-patterns.html
---

# Advanced TypeScript Patterns: Generics, Mapped Types, and Template Literals

TypeScript's type system is a programming language in its own right. Once you go beyond basic annotations, you can encode invariants into types that make entire categories of bugs impossible. Here are the advanced patterns that level up your TypeScript in 2026.

## 1\. Conditional Types

Conditional types select types based on a condition — like a ternary operator at the type level.

    type IsString<T> = T extends string ? true : false;

    type A = IsString<"hello">;  // true
    type B = IsString<number>;   // false

    // Real example: extract the array element type
    type ArrayElement<T> = T extends (infer U)[] ? U : never;
    type Item = ArrayElement<string[]>;  // string

## 2\. Mapped Types

Mapped types transform existing types by iterating over their keys.

    // Make all properties optional
    type Partial<T> = { [K in keyof T]?: T[K] };

    // Make all properties readonly
    type Readonly<T> = { readonly [K in keyof T]: T[K] };

    // Real example: pick nullable fields
    type Nullable<T> = { [K in keyof T]: T[K] | null };

## 3\. Template Literal Types

Construct types from string patterns — powerful for typed routing and event systems.

    type EventName = "click" | "focus" | "blur";
    type Handler = `on${Capitalize<EventName>}`;
    // "onClick" | "onFocus" | "onBlur"

    // Real example: typed API routes
    type Route = `/api/${string}`;
    type UserRoute = `/api/users/${number}`;
    const route: UserRoute = "/api/users/42"; // OK
    const bad: UserRoute = "/api/users/abc"; // Error

## 4\. The infer Keyword

Extract and capture types from other types during conditional type checks.

    // Extract return type of a function
    type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

    // Extract the promise resolved type
    type Awaited<T> = T extends Promise<infer U> ? U : T;

    // Real example: extract component props
    type Props<C> = C extends React.ComponentType<infer P> ? P : never;

## 5\. Branded Types (Nominal Typing)

TypeScript uses structural typing, but sometimes you want nominal types — two strings that are not interchangeable.

    type UserId = string & { readonly __brand: "UserId" };
    type OrderId = string & { readonly __brand: "OrderId" };

    function createUserId(id: string): UserId {
      return id as UserId;
    }

    function getUser(id: UserId) { /* ... */ }

    getUser(createUserId("abc")); // OK
    getUser("abc"); // Error — plain string is not a UserId

## 6\. Discriminated Unions

The most useful pattern in TypeScript. Model states exhaustively with a discriminator field.

    type RequestState<T> =
      | { status: "idle" }
      | { status: "loading" }
      | { status: "success"; data: T }
      | { status: "error"; error: Error };

    function render<T>(state: RequestState<T>) {
      switch (state.status) {
        case "idle": return "Ready";
        case "loading": return "Loading...";
        case "success": return state.data; // T — narrowed!
        case "error": return state.error.message; // Error — narrowed!
      }
    }

## 7\. Builder Pattern with Type Safety

    class QueryBuilder<
      T extends Record<string, unknown>,
      Selected extends keyof T | "*" = "*",
      WhereClause extends Partial<T> = {}
    > {
      select<K extends keyof T>(...cols: K[]): QueryBuilder<T, K, WhereClause> {
        return this as any;
      }
      where(conditions: Partial<T>): QueryBuilder<T, Selected, Partial<T>> {
        return this as any;
      }
    }

## Quick Reference: When to Use What

Pattern| Use Case  
---|---  
Conditional Types| Transform types based on conditions  
Mapped Types| Bulk-modify object property types  
Template Literal Types| String-pattern-based types (routes, events)  
infer| Extract embedded types  
Branded Types| Distinguish same-shape types semantically  
Discriminated Unions| Exhaustive state modeling (async, forms)  

**Bottom line:** Advanced TypeScript patterns let you catch bugs at compile time instead of runtime. Discriminated unions and branded types alone will eliminate entire categories of bugs. See also: [TypeScript ORM comparison](</en/compare/prisma-vs-drizzle-vs-typeorm.html>) and [tRPC for end-to-end types](</en/compare/trpc-vs-graphql-vs-rest.html>).
