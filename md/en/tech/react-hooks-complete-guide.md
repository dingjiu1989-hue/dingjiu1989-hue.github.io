---
title: "React Hooks Complete Guide 2026: From useState to useOptimistic"
description: "Every React hook explained with real examples: useState, useEffect, useContext, useReducer, useMemo, useCallback, useRef, useTransition, useDeferredValue, and the new useOptimistic hook."
date: 2025-10-13
board: tech
url: https://aidev.fit/en/tech/react-hooks-complete-guide.html
---

# React Hooks Complete Guide 2026: From useState to useOptimistic

React Hooks have been the primary way to add state and logic to React components since 2019, but their surface area keeps growing. React 19 and React 20 (2026) introduced hooks like useOptimistic and useFormStatus that change how we handle optimistic updates and form state. This guide covers every built-in React hook, when to use each, and the most common pitfalls.

## All React Hooks at a Glance

Hook| Purpose| When to Use| Introduced  
---|---|---|---  
useState| Component-level state| Any mutable value in a component| React 16.8  
useEffect| Synchronize with external systems| API calls, subscriptions, DOM mutations| React 16.8  
useContext| Read a context value| Theme, auth, locale — any global-ish state| React 16.8  
useReducer| Complex state logic| State with multiple sub-values, state machines| React 16.8  
useCallback| Memoize a function reference| Stable callbacks passed to memoized children| React 16.8  
useMemo| Memoize a computed value| Expensive calculations, stable object references| React 16.8  
useRef| Mutable reference that persists| DOM access, storing previous values, interval IDs| React 16.8  
useId| Unique ID for accessibility| Linking label's htmlFor to input's id| React 18  
useTransition| Mark a state update as non-urgent| UI that updates slower than user input (tabs, filters)| React 18  
useDeferredValue| Defer re-rendering a value| Showing stale content while new content loads| React 18  
useSyncExternalStore| Subscribe to an external store| Integrating non-React state libraries (Redux, Zustand)| React 18  
useInsertionEffect| CSS-in-JS library hook| Inject styles before layout effects fire (rarely used directly)| React 18  
useOptimistic| Optimistic UI updates| Show a value before the server confirms it| React 19/20  
useFormStatus| Form submission status| Disable submit button while form is submitting| React 19/20  
useActionState| Form action with state| Server Action form handling with error states| React 19/20  
  
## useState: The Foundation

**Best for:** Simple values that change over time — form inputs, toggle states, counters. **Key rule:** Never call setState during render (except for derived state with useMemo or useReducer).
    
    
    // Basic usage
    const [count, setCount] = useState(0);
    
    // Functional update (when new state depends on old)
    setCount(prev => prev + 1);
    
    // Lazy initializer (expensive computation, runs once)
    const [data, setData] = useState(() => expensiveComputation());

## useEffect: The Most Misused Hook

**Best for:** Synchronizing with external systems (browser APIs, third-party libraries, network). **Common mistake:** Using useEffect for derived state or event handling, which should be done in event handlers or during render.
    
    
    // Good: connect to external system
    useEffect(() => {
      const connection = createConnection(serverUrl);
      connection.connect();
      return () => connection.disconnect();
    }, [serverUrl]);
    
    // Bad: setting state from props (do this during render instead)
    useEffect(() => {
      setFullName(firstName + ' ' + lastName); // Unnecessary!
    }, [firstName, lastName]);

## useMemo and useCallback: Performance Hooks

**Best for:** Preventing unnecessary re-renders of memoized child components. **Key rule:** Do not wrap everything in useMemo/useCallback — only use them when you have measured a performance problem.
    
    
    // useMemo: cache an expensive computed value
    const sortedList = useMemo(() => {
      return items.sort((a, b) => a.name.localeCompare(b.name));
    }, [items]);
    
    // useCallback: stabilize a function reference
    const handleClick = useCallback((id: string) => {
      setSelectedId(id);
    }, []); // Stable reference across re-renders

## useOptimistic: Optimistic UI in 2026

**Best for:** Instant UI feedback while a server action is in flight — like liking a post, toggling a todo, or sending a message.
    
    
    const [optimisticMessages, addOptimisticMessage] = useOptimistic(
      messages,
      (state, newMessage) => [...state, { ...newMessage, sending: true }]
    );
    
    async function sendMessage(formData: FormData) {
      const message = formData.get('message');
      addOptimisticMessage({ text: message, id: crypto.randomUUID() });
      await sendMessageToServer(message); // Revalidates messages on success
    }

**Bottom line:** React Hooks are not just for state — they are the primitive for composing behavior in React. The newer hooks (useOptimistic, useFormStatus, useTransition) show React's direction: tighter integration with server actions and optimistic UI. See also: [React vs Vue vs Angular vs Svelte](</en/compare/react-vs-vue-vs-angular-vs-svelte.html>) and [Next.js vs Nuxt vs SvelteKit](</en/compare/nextjs-vs-nuxt-vs-sveltekit.html>).

**See also:** [API Security Best Practices 2026: JWT, Rate Limiting, Input Validation, and OWASP for APIs](</en/tech/api-security-best-practices.html>), [Responsive CSS in 2026: Container Queries, Grid, and Modern Layout Patterns](</en/tech/css-responsive-design-guide.html>), [Node.js Streams: Complete Guide to Efficient Data Processing](</en/tech/nodejs-streams-guide.html>)
