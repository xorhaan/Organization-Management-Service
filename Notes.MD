# Architectural Review & Design Choices

## 1. Scalability Assessment
**Question:** *Do you think this is a good architecture with a scalable design?*

**Verdict:** While the requested "Collection-per-Tenant" architecture offers excellent data isolation, it is **not scalable** for a high-growth SaaS application.

### Why it limits scalability:
* **Resource Overhead:** MongoDB (WiredTiger engine) maintains open file descriptors and memory mappings for every active collection. Scaling to 10,000+ organizations would result in tens of thousands of collections, consuming massive amounts of RAM and potentially hitting OS file descriptor limits.
* **Infrastructure Complexity:** Managing indexes becomes a maintenance bottleneck. Adding a new index to a `Users` schema requires running a script to iterate through and update thousands of separate collections.
* **Analytics Barrier:** Running cross-tenant queries (e.g., *"What is the total user count across all organizations?"*) is computationally expensive, requiring scatter-gather queries across thousands of namespaces rather than a simple aggregation.

---

## 2. Tech Stack & Trade-offs
**Stack:** Python (FastAPI) + MongoDB (Pymongo)

### Trade-offs:
1.  **FastAPI (Async) vs. Pymongo (Sync):**
    * *Choice:* I used `pymongo` for reliability and simplicity given the scope.
    * *Trade-off:* Since FastAPI is asynchronous, using a blocking driver like `pymongo` forces the application to run database operations in a thread pool. For extreme high-concurrency (10k+ RPS), using an async driver like `Motor` would prevent blocking the event loop.

2.  **Schemaless Database (MongoDB):**
    * *Benefit:* Allows different organizations to potentially have custom fields in the future without complex migrations.
    * *Trade-off:* Lack of ACID transactions across collections (prior to v4.0) makes data integrity harder to guarantee. For example, creating an Organization and an Admin User involves writing to two different collections. If one fails, we risk "orphan" records unless complex Two-Phase Commits are implemented.

3.  **Physical Isolation (Collection-per-Tenant):**
    * *Benefit:* Security is enforced at the database namespace level. It is impossible to accidentally leak "Org A" data to "Org B" via a missing `WHERE` clause.
    * *Trade-off:* Operational agility is lost. Database migrations, backups, and monitoring become significantly harder as the tenant count grows.

---

## 3. A Better Scalable Design: The "Pool Model"
To design this system for high scalability (e.g., 100k+ tenants), I would choose the **Pool Architecture** (Shared Database, Shared Schema) with **Logical Isolation**.



### Proposed Architecture:
Instead of creating a new collection for every tenant, we use **one** massive collection for each resource type (e.g., `Users`, `Orders`) and partition data using an indexed `org_id`.

#### Key Changes:
1.  **Single Collection Pattern:**
    * **Old:** `db.org_tesla_users.find({})`
    * **New:** `db.users.find({ "org_id": "tesla_uuid" })`

2.  **Compound Indexing:**
    * Create a compound index `{ org_id: 1, email: 1 }`. This ensures queries are just as fast as separate collections because the database engine jumps directly to that tenant's data block.

3.  **Sharding (Horizontal Scaling):**
    * MongoDB excels at sharding based on a "Shard Key". By using `org_id` as the shard key, MongoDB can automatically distribute data across multiple servers (e.g., Tenants A-M on Server 1, N-Z on Server 2) without application-level complexity.

4.  **ID Strategy (Snowflake/ULID):**
    * Instead of random UUIDs, I would use **UUIDv7** or **ULID** (Time-Sortable IDs). This prevents index fragmentation and improves write performance by appending new data to the end of the B-Tree rather than inserting randomly.

### Summary Comparison
| Feature | Current (Collection-per-Tenant) | Proposed (Pool Model) |
| :--- | :--- | :--- |
| **Isolation** | Physical (High) | Logical (Medium) |
| **Max Tenants** | ~5,000 before degradation | Millions (limited only by disk) |
| **Analytics** | Very Hard | Very Easy (Standard Aggregations) |
| **Maintenance** | High Effort (Scripting required) | Low Effort (Standard Ops) |

---

## 4. Specific Design Decisions in This Implementation
Despite the limitations of the requested architecture, I implemented specific optimizations to maximize stability:

1.  **Atomic Renaming vs. Copying:**
    * The requirement suggested creating a new collection and moving data during updates. I rejected this in favor of `db.renameCollection()`.
    * *Reasoning:* Renaming is an atomic **O(1)** metadata operation. Copying data is **O(N)** and risks data corruption if the server crashes mid-transfer.

2.  **Dependency Injection:**
    * I refactored the codebase to use FastAPI's `Depends()` for service injection. This decouples business logic from the routing layer, making the system modular and significantly easier to unit test.

---

## 5. Load Testing with Locust

![alt text](<Screenshot 2025-12-12 at 3.14.52 PM.png>)
![alt text](<Screenshot 2025-12-12 at 3.14.09 PM.png>)
