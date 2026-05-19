---
title: "Best Diagram as Code Tools"
description: "Compare diagram-as-code tools including Mermaid, PlantUML, Excalidraw, and Diagrams for creating technical diagrams."
date: 2025-12-09
board: tools
url: https://dingjiu1989-hue.github.io/en/tools/diagram-tools.html
---

# Best Diagram as Code Tools

Diagram-as-code tools let you create architecture diagrams, flowcharts, and sequence diagrams using text-based specifications. This approach offers version control, reproducibility, and seamless integration with documentation workflows.

## Why Diagram as Code

Traditional diagram tools (draw.io, LucidChart) produce binary files that are difficult to version control and review. Diagram-as-code tools:

  * Store diagrams as plain text (diffable, reviewable in PRs).

  * Integrate with Markdown documentation.

  * Generate consistent output from the same source.

  * Can be run in CI/CD pipelines.

  * Work in any editor with syntax highlighting.




## Mermaid

Mermaid is the most popular diagram-as-code tool, supported natively by GitHub, GitLab, and Notion. It renders diagrams from JavaScript-like syntax.

graph TD

A[Client] -->|HTTP| B[Load Balancer]

B --> C[Web Server 1]

B --> D[Web Server 2]

C --> E[(Database)]

D --> E

E --> F[Cache]

graph TD

A[Client] -->|HTTP| B[Load Balancer]

B --> C[Web Server 1]

B --> D[Web Server 2]

C --> E[(Database)]

D --> E

E --> F[Cache]

**Supported Diagram Types:**

  * Flowchart, Sequence diagram, Class diagram

  * State diagram, Entity Relationship diagram

  * Gantt chart, Pie chart, Git graph

  * User Journey, C4 diagram (decomposition)




sequenceDiagram

participant User

participant API

participant DB

User->>API: POST /login

API->>DB: SELECT user

DB-->>API: user data

API->>API: validate password

API-->>User: JWT token

**Pros** : Native GitHub/GitLab support, wide diagram type support, simple syntax, active development.

**Cons** : Complex diagrams can be slow to render, limited layout control, can look generic.

**Installation:**

npm install -g @mermaid-js/mermaid-cli

mmdc -i input.mmd -o output.png

## PlantUML

PlantUML is a mature diagram-as-code tool with Java-based rendering and extensive diagram type support.

@startuml

actor User

participant "API Gateway" as GW

participant "Auth Service" as Auth

database "User DB" as DB

User -> GW: POST /auth/login

GW -> Auth: validate credentials

Auth -> DB: query user

DB --> Auth: user record

Auth --> GW: JWT token

GW --> User: 200 OK

@enduml

**Supported Diagram Types:**

  * Sequence, Use Case, Class, Activity, Component

  * State, Deployment, Object, Timing, Wireframe

  * Archimate, Gantt, Mind Map, Work Breakdown

  * Network diagram, JSON/YAML visualization




**Pros** : Most comprehensive diagram type support, mature and stable, powerful layout engine.

**Cons** : Java dependency, syntax can be verbose, slower rendering than Mermaid.

**Installation:**

## Using Docker

docker run -it --rm -v $(pwd):/data plantuml/plantuml diagram.puml

## Or using the plantuml CLI with Java

java -jar plantuml.jar diagram.puml

## Excalidraw

Excalidraw is a whiteboard tool that produces hand-drawn style diagrams. It is not truly "diagram as code," but the .excalidraw format is JSON and can be version controlled.

**Pros** : Beautiful hand-drawn aesthetic, real-time collaboration, excellent for system design whiteboarding.

**Cons** : Not text-based, no code generation, manual placement.

Excalidraw has a CLI tool for embedding in workflows:

npx @excalidraw/cli export diagram.excalidraw --output diagram.png

## Diagrams (Python)

Diagrams is a Python library for creating cloud system architecture diagrams. It includes icons for AWS, GCP, Azure, Kubernetes, and more.

from diagrams import Diagram, Cluster

from diagrams.aws.compute import EC2

from diagrams.aws.database import RDS

from diagrams.aws.network import ELB

with Diagram("Web Service", show=False):

lb = ELB("Load Balancer")

web = EC2("Web Server")

db = RDS("Database")

lb >> web >> db

**Output Style:** Structured cloud architecture diagrams with official service icons.

**Pros** : Python-based, official AWS/GCP/Azure icons, programmatic control.

**Cons** : Limited to cloud architecture, not general-purpose diagramming.

**Installation:**

pip install diagrams

python diagram.py # Generates diagram.png

## D2

D2 is a newer diagram-as-code language by Terrastruct, designed to address Mermaid's layout limitations.

Client -> Load Balancer: HTTP

Load Balancer -> Web Server 1

Load Balancer -> Web Server 2

Web Server 1 -> Database: SQL

Web Server 2 -> Database: SQL

Database -> Redis Cache: Cache read/write

**Pros** : Better auto-layout than Mermaid, cleaner output, fast rendering, animated diagrams.

**Cons** : Newer = smaller community, fewer integrations, limited diagram types.

## Comparison Table

| Feature | Mermaid | PlantUML | Excalidraw | Diagrams | D2 |

|---------|---------|----------|------------|----------|-----|

| Language | JS-like | Java-like | JSON | Python | D2 DSL |

| Diagram types | 10+ | 20+ | Free-form | Cloud arch | 5+ |

| GitHub native | Yes | No | No | No | No |

| CI/CD support | CLI | CLI | CLI | Python | CLI |

| Layout quality | Good | Good | Manual | Algorithmic | Excellent |

| Speed | Fast | Medium | N/A | Fast | Fast |

| License | MIT | GPL | MIT | MIT | MPL |

## Integration with Documentation

**Mermaid in Markdown:**

graph LR

A --> B

B --> C

Rendered automatically on GitHub, GitLab, and with Markdown renderers that support Mermaid.

**In MkDocs with Material Theme:**

## mkdocs.yml

markdown_extensions:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- pymdownx.superfences:

custom_fences:

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\- name: mermaid

class: mermaid

**In VS Code:**

// Preview Mermaid in VS Code

"extensions": ["bierner.markdown-mermaid"]

## Recommendations

  * **For GitHub documentation** : Mermaid (native support, simplest syntax).

  * **For complex UML** : PlantUML (most diagram types, best UML support).

  * **For cloud architecture** : Diagrams (official icons, Python integration).

  * **For whiteboarding** : Excalidraw (best visual output for brainstorming).

  * **For polished output** : D2 (best auto-layout, modern tool).




## Summary

Diagram-as-code tools have made technical diagrams maintainable and version-controllable. Mermaid is the most accessible choice with native GitHub support. PlantUML offers the widest diagram type coverage. D2 provides the best layout quality for modern tools. The key principle is to choose a tool that integrates with your existing documentation workflow -- if you already use Markdown in GitHub, Mermaid is the natural choice.

**See also:** [Best Diagram and Architecture Tools 2026: Excalidraw vs Draw.io vs Mermaid vs Eraser](</en/tools/best-diagram-tools.html>), [API Testing Tools Comparison](</en/tools/api-testing-tools.html>), [Developer Note Taking Tools](</en/tools/note-taking-tools.html>).

**See also:** [Best Diagram and Architecture Tools 2026: Excalidraw vs Draw.io vs Mermaid vs Eraser](</en/tools/best-diagram-tools.html>), [API Testing Tools Comparison](</en/tools/api-testing-tools.html>), [Code Review Tools and Best Practices](</en/tools/code-review-tools.html>)

**See also:** [Best Diagram and Architecture Tools 2026: Excalidraw vs Draw.io vs Mermaid vs Eraser](</en/tools/best-diagram-tools.html>), [API Testing Tools Comparison](</en/tools/api-testing-tools.html>), [Code Review Tools and Best Practices](</en/tools/code-review-tools.html>)

**See also:** [Best Diagram and Architecture Tools 2026: Excalidraw vs Draw.io vs Mermaid vs Eraser](</en/tools/best-diagram-tools.html>), [API Testing Tools Comparison](</en/tools/api-testing-tools.html>), [Code Review Tools and Best Practices](</en/tools/code-review-tools.html>)

**See also:** [Best Diagram and Architecture Tools 2026: Excalidraw vs Draw.io vs Mermaid vs Eraser](</en/tools/best-diagram-tools.html>), [API Testing Tools Comparison](</en/tools/api-testing-tools.html>), [Code Review Tools and Best Practices](</en/tools/code-review-tools.html>)

**See also:** [Best Diagram and Architecture Tools 2026: Excalidraw vs Draw.io vs Mermaid vs Eraser](</en/tools/best-diagram-tools.html>), [API Testing Tools Comparison](</en/tools/api-testing-tools.html>), [Code Review Tools and Best Practices](</en/tools/code-review-tools.html>)

**See also:** [Project Management Tools for Developers](</en/tools/project-management-tools.html>), [Best Terminal Emulators 2026](</en/tools/terminal-emulators.html>), [Developer Collaboration Tools: Slack vs Discord vs Linear](</en/tools/collaboration-tools.html>)

**See also:** [Project Management Tools for Developers](</en/tools/project-management-tools.html>), [Best Terminal Emulators 2026](</en/tools/terminal-emulators.html>), [Developer Collaboration Tools: Slack vs Discord vs Linear](</en/tools/collaboration-tools.html>)

**See also:** [Project Management Tools for Developers](</en/tools/project-management-tools.html>), [Best Terminal Emulators 2026](</en/tools/terminal-emulators.html>), [Developer Collaboration Tools: Slack vs Discord vs Linear](</en/tools/collaboration-tools.html>)

**See also:** [Project Management Tools for Developers](</en/tools/project-management-tools.html>), [Best Terminal Emulators 2026](</en/tools/terminal-emulators.html>), [Developer Collaboration Tools: Slack vs Discord vs Linear](</en/tools/collaboration-tools.html>)

**See also:** [Project Management Tools for Developers](</en/tools/project-management-tools.html>), [Best Terminal Emulators 2026](</en/tools/terminal-emulators.html>), [Developer Collaboration Tools: Slack vs Discord vs Linear](</en/tools/collaboration-tools.html>)

**See also:** [Project Management Tools for Developers](</en/tools/project-management-tools.html>), [Best Terminal Emulators 2026](</en/tools/terminal-emulators.html>), [Developer Collaboration Tools: Slack vs Discord vs Linear](</en/tools/collaboration-tools.html>)
