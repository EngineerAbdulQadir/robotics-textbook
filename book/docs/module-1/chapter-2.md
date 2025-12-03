---
title: "Chapter 2: ROS 2 Fundamentals - Nodes, Topics, and Services"
---

# Chapter 2: ROS 2 Fundamentals: Nodes, Topics, and Services

**Description**: Master the core architecture of ROS 2, the middleware that powers modern robotics.

---

## Topics

### ROS 2 Architecture and Design Principles

Understanding the distributed architecture of ROS 2:
- Decentralized communication
- Language-agnostic design
- Real-time capabilities
- Security features

### Nodes: The Building Blocks of Robot Systems

Nodes are independent processes that perform specific tasks:
- Sensor nodes
- Processing nodes
- Control nodes
- Visualization nodes

### Topics: Publish-Subscribe Communication

Asynchronous communication pattern:
- Publishers send messages
- Subscribers receive messages
- Many-to-many communication
- Message types and interfaces

### Services: Request-Response Patterns

Synchronous communication for specific tasks:
- Client-server model
- Request and response messages
- Use cases for services
- Service definitions

### Actions: Long-Running Tasks

For tasks that take time to complete:
- Goal, feedback, and result
- Preemptable operations
- Progress monitoring
- Navigation and manipulation examples

---

## Hands-on

Create your first ROS 2 node, publish sensor data, and call services.

**Example**: Building a simple publisher-subscriber system for robot telemetry.

---

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand ROS 2 architecture and communication patterns
- Create and manage ROS 2 nodes
- Implement publish-subscribe communication with topics
- Use services for request-response patterns
- Understand when to use actions for long-running tasks

---

## Key Takeaways

- ROS 2 uses a distributed architecture for robot systems
- Nodes are independent processes that communicate via topics and services
- Topics enable asynchronous many-to-many communication
- Services provide synchronous request-response patterns
- Actions handle long-running, preemptable tasks

---

## Next Steps

Continue to [Chapter 3: ROS 2 Tools](./chapter-3.md) to learn visualization and simulation tools.
