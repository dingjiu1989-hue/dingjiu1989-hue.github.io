---
title: "TypeScript实践：类型体操、泛型、装饰器高级用法"
description: "深入讲解TypeScript的高级特性，包括条件类型、映射类型等类型体操技巧，泛型的进阶用法以及装饰器的实际应用场景。"
date: 2026-05-12
board: tech
url: https://dingjiu1989-hue.github.io/zh/tech/typescript-shijian.html
---

## 超越基础类型

TypeScript的类型系统远比表面上看起来更强大。掌握高级类型技巧能让代码更加安全和优雅。

## 类型体操

### 条件类型

根据条件选择不同的类型：

```typescript
type IsString<T> = T extends string ? true : false;
type Result1 = IsString<"hello">;  // true
type Result2 = IsString<42>;       // false
```

### 映射类型

对已有类型的属性进行变换：

```typescript
type Readonly<T> = {
    readonly [P in keyof T]: T[P];
};

type Partial<T> = {
    [P in keyof T]?: T[P];
};

type Pick<T, K extends keyof T> = {
    [P in K]: T[P];
};
```

### 递归类型

处理嵌套结构的类型：

```typescript
type DeepPartial<T> = {
    [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

type DeepReadonly<T> = {
    readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};
```

### infer关键字

从类型中提取子类型：

```typescript
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
type ArrayItem<T> = T extends (infer U)[] ? U : never;
type PromiseValue<T> = T extends Promise<infer U> ? U : T;
```

## 泛型进阶

### 泛型约束

使用extends约束泛型参数的范围：

```typescript
interface HasId {
    id: number;
}

function getById<T extends HasId>(items: T[], id: number): T | undefined {
    return items.find(item => item.id === id);
}
```

### 泛型工具类型

TypeScript内置了大量有用的工具类型，需要深入理解其使用场景：

- `Partial<T>`：所有属性变为可选
- `Required<T>`：所有属性变为必选
- `Readonly<T>`：所有属性变为只读
- `Pick<T, K>`：从T中选取部分属性
- `Omit<T, K>`：从T中排除部分属性
- `Record<K, V>`：构造一个键值类型
- `Exclude<T, U>`：从联合类型中排除某些类型

### 模板字面量类型

TypeScript 4.1+支持的模板字面量类型：

```typescript
type EventName = `on${Capitalize<string>}`;
type CSSProperty = `--${string}`;
```

## 装饰器

### 类装饰器

修改类的行为和结构：

```typescript
function LogClass<T extends { new (...args: any[]): {} }>(constructor: T) {
    return class extends constructor {
        createdAt = new Date();
    };
}
```

### 方法装饰器

拦截方法调用，实现日志、缓存等功能：

```typescript
function Log(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const original = descriptor.value;
    descriptor.value = function(...args: any[]) {
        console.log(`Calling ${propertyKey} with`, args);
        return original.apply(this, args);
    };
}
```

## 实践建议

1. **优先使用interface定义公共API的类型**
2. **使用type定义联合类型和工具类型**
3. **避免过度抽象**：复杂的类型体操可能降低代码可读性
4. **善用satisfies操作符**（TypeScript 4.9+）进行类型验证
5. **使用ts-reset等工具库增强类型安全**

掌握TypeScript的高级类型系统，能够写出更具表达力和安全性的代码。
