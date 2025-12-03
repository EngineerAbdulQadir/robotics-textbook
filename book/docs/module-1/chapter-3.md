---
title: "Chapter 3: ROS 2 Tools - RViz, Gazebo, and the CLI"
---

# Chapter 3: ROS 2 Tools: RViz, Gazebo, and the CLI

**Description**: Learn the essential tools for visualizing, simulating, and debugging robot systems.

---

## Topics

### RViz: 3D Visualization of Robot State

RViz is the primary visualization tool for ROS 2:
- Visualizing robot models (URDF)
- Displaying sensor data (cameras, lidar, point clouds)
- Showing transforms and coordinate frames
- Interactive markers for robot control

### Gazebo: Physics-Based Simulation

Gazebo provides realistic physics simulation:
- Simulating gravity, friction, and collisions
- Sensor simulation (cameras, lidar, IMU)
- World building and environment design
- Plugin system for custom behaviors

### Command-Line Tools for Introspection

Essential CLI tools for debugging:
- `ros2 node list` - List active nodes
- `ros2 topic list/echo` - Inspect topics
- `ros2 service list/call` - Work with services
- `ros2 bag` - Record and replay data

### Launch Files for Complex Systems

Managing multiple nodes:
- Python launch files
- XML launch files
- Parameter configuration
- Node composition

---

## Hands-on

Visualize a robot in RViz and simulate it in Gazebo.

**Example**: Loading a humanoid robot model and controlling it in simulation.

---

## Learning Objectives

By the end of this chapter, you will be able to:

- Use RViz to visualize robot state and sensor data
- Simulate robots in Gazebo with realistic physics
- Debug robot systems using command-line tools
- Create launch files to manage complex robot systems

---

## Key Takeaways

- RViz provides powerful 3D visualization for robot development
- Gazebo enables realistic physics simulation before hardware deployment
- Command-line tools are essential for debugging
- Launch files simplify managing multi-node systems

---

## Module Complete

You have completed Module 1! Continue to [Module 2: The Digital Twin](../module-2/index.md) to learn about advanced simulation.
