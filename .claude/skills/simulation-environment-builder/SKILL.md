---
name: simulation-environment-builder
category: "robotics-development"
applies_to: ["simulation-chapters", "gazebo-tutorials", "isaac-sim-content"]
required_for: ["content-implementer", "exercise-designer"]
description: |
  Design and configure realistic simulation environments for robotics education using Gazebo, Isaac Sim, and
  Unity. This skill helps create worlds, configure physics, add sensors, and ensure sim-to-real transferability.
  Use when building simulation scenarios for learning, testing robot algorithms, or demonstrating concepts
  without physical hardware. Ensures simulations are educationally valuable while maintaining physical accuracy.
  Aligned with Constitution v4.0.1.
version: "1.0.0"
dependencies: ["constitution:v4.0.1"]
---

# Simulation Environment Builder

## Purpose

Create realistic, educational simulation environments that accurately represent physical robotics systems. This skill helps:
- Design Gazebo worlds for ROS 2 robot simulation
- Configure Isaac Sim environments for advanced AI training
- Set up Unity scenes for human-robot interaction studies
- Implement realistic physics and sensor models
- Balance simulation fidelity with computational performance
- Ensure sim-to-real transferability
- Create progressive learning scenarios (simple → complex)
- Document known simulation limitations

## When to Activate

Use this skill when:
- Creating Gazebo worlds for robot navigation
- Building Isaac Sim environments for manipulation tasks
- Designing Unity scenes for HRI research
- Configuring physics engines and parameters
- Adding sensors (cameras, lidar, IMU) to simulations
- Creating test scenarios for robot algorithms
- Developing educational simulation exercises
- Troubleshooting simulation instabilities
- Educators ask about "simulation setup", "Gazebo worlds", "physics configuration"

## Process

### Step 1: Define Simulation Requirements

When a request comes in for simulation environment, first clarify:
- **What is the learning objective?** (Navigation, manipulation, perception, control)
- **What robot platform?** (Mobile robot, manipulator, humanoid, aerial)
- **What sensors are needed?** (Camera, lidar, depth, IMU, GPS)
- **What complexity level?** (Empty world, structured environment, complex scene)
- **What performance constraints?** (Real-time required, acceptable lag)
- **What sim-to-real gap is acceptable?** (Educational vs. deployment-ready)

### Step 2: Choose Simulation Platform

Select appropriate simulator based on requirements:

#### Gazebo (ROS 2 Integration)
**Best for**:
- Mobile robot navigation
- ROS 2 learning and development
- Multi-robot systems
- Sensor simulation (lidar, cameras)

**Strengths**:
- Native ROS 2 integration
- Good physics simulation
- Large community and resources
- Free and open-source

**Limitations**:
- Limited photorealism
- Basic rendering
- Can be computationally intensive

#### Isaac Sim (NVIDIA)
**Best for**:
- Manipulation tasks
- AI/ML training with synthetic data
- Photorealistic rendering
- Large-scale simulation

**Strengths**:
- Photorealistic graphics
- GPU-accelerated physics
- Domain randomization
- Synthetic data generation

**Limitations**:
- Requires NVIDIA GPU
- Steeper learning curve
- Resource intensive

#### Unity (Custom Integration)
**Best for**:
- Human-robot interaction
- Custom visualizations
- Game-like scenarios
- Cross-platform deployment

**Strengths**:
- Excellent graphics
- Flexible scripting
- Asset store
- Multi-platform

**Limitations**:
- Requires custom ROS integration
- Physics less accurate than Gazebo
- More development overhead

### Step 3: Design World Structure

Create world layout based on learning objectives:

**Progressive Complexity Approach**:

**Level 1: Empty World**
- Flat ground plane
- Simple lighting
- No obstacles
- Use for: Basic movement, sensor testing

**Level 2: Structured Environment**
- Walls and boundaries
- Simple obstacles (boxes, cylinders)
- Landmarks for navigation
- Use for: Obstacle avoidance, path planning

**Level 3: Realistic Environment**
- Furniture and objects
- Textured surfaces
- Complex geometry
- Use for: Advanced navigation, manipulation

**Level 4: Dynamic Environment**
- Moving obstacles
- Changing lighting
- Interactive objects
- Use for: Adaptive behaviors, robust algorithms

### Step 4: Configure Physics Parameters

Set realistic physics for educational value:

**Gazebo Physics Configuration**:
```xml
<world name="robot_world">
  <physics type="ode">
    <!-- Time step: smaller = more accurate but slower -->
    <max_step_size>0.001</max_step_size>
    
    <!-- Real-time factor: 1.0 = real-time -->
    <real_time_factor>1.0</real_time_factor>
    
    <!-- Solver iterations: higher = more stable -->
    <ode>
      <solver>
        <type>quick</type>
        <iters>50</iters>
        <sor>1.3</sor>
      </solver>
      <constraints>
        <cfm>0.0</cfm>
        <erp>0.2</erp>
        <contact_max_correcting_vel>100.0</contact_max_correcting_vel>
        <contact_surface_layer>0.001</contact_surface_layer>
      </constraints>
    </ode>
  </physics>
  
  <!-- Gravity -->
  <gravity>0 0 -9.81</gravity>
  
  <!-- Magnetic field (for IMU simulation) -->
  <magnetic_field>6e-06 2.3e-05 -4.2e-05</magnetic_field>
</world>
```

**Key Parameters**:
- **max_step_size**: Smaller values (0.001s) = more accurate, slower
- **real_time_factor**: Target speed (1.0 = real-time)
- **solver iterations**: More iterations = more stable contacts
- **gravity**: Always use 9.81 m/s² for Earth

### Step 5: Add Realistic Sensors

Configure sensors with realistic characteristics:

**Lidar Sensor Example**:
```xml
<sensor name="lidar" type="ray">
  <pose>0 0 0.2 0 0 0</pose>
  <update_rate>10</update_rate>
  <ray>
    <scan>
      <horizontal>
        <samples>360</samples>
        <resolution>1</resolution>
        <min_angle>-3.14159</min_angle>
        <max_angle>3.14159</max_angle>
      </horizontal>
    </scan>
    <range>
      <min>0.12</min>
      <max>30.0</max>
      <resolution>0.01</resolution>
    </range>
    <!-- Add realistic noise -->
    <noise>
      <type>gaussian</type>
      <mean>0.0</mean>
      <stddev>0.01</stddev>
    </noise>
  </ray>
  <plugin name="lidar_plugin" filename="libgazebo_ros_ray_sensor.so">
    <ros>
      <namespace>/robot</namespace>
      <remapping>~/out:=scan</remapping>
    </ros>
    <output_type>sensor_msgs/LaserScan</output_type>
  </plugin>
</sensor>
```

**Camera Sensor Example**:
```xml
<sensor name="camera" type="camera">
  <pose>0.05 0 0.1 0 0 0</pose>
  <update_rate>30</update_rate>
  <camera>
    <horizontal_fov>1.3962634</horizontal_fov>
    <image>
      <width>640</width>
      <height>480</height>
      <format>R8G8B8</format>
    </image>
    <clip>
      <near>0.02</near>
      <far>300</far>
    </clip>
    <!-- Add realistic noise -->
    <noise>
      <type>gaussian</type>
      <mean>0.0</mean>
      <stddev>0.007</stddev>
    </noise>
  </camera>
  <plugin name="camera_plugin" filename="libgazebo_ros_camera.so">
    <ros>
      <namespace>/robot</namespace>
      <remapping>~/image_raw:=camera/image_raw</remapping>
      <remapping>~/camera_info:=camera/camera_info</remapping>
    </ros>
  </plugin>
</sensor>
```

**Sensor Configuration Checklist**:
- [ ] Update rate matches real sensor
- [ ] Noise model included
- [ ] Range limits realistic
- [ ] Resolution appropriate
- [ ] Field of view correct

### Step 6: Implement Realistic Materials

Configure surface properties for accurate physics:

**Material Properties**:
```xml
<gazebo reference="wheel_link">
  <material>Gazebo/Black</material>
  <mu1>1.0</mu1>  <!-- Friction coefficient 1 -->
  <mu2>1.0</mu2>  <!-- Friction coefficient 2 -->
  <kp>1000000.0</kp>  <!-- Contact stiffness -->
  <kd>100.0</kd>  <!-- Contact damping -->
  <minDepth>0.001</minDepth>
  <maxVel>1.0</maxVel>
</gazebo>

<gazebo reference="floor">
  <material>Gazebo/Wood</material>
  <mu1>0.8</mu1>
  <mu2>0.8</mu2>
</gazebo>
```

**Common Material Friction Values**:
- Rubber on concrete: 0.7-1.5
- Metal on metal: 0.15-0.25
- Wood on wood: 0.25-0.5
- Plastic on plastic: 0.2-0.4

### Step 7: Create Progressive Scenarios

Design scenarios that build complexity:

**Scenario 1: Basic Movement**
```xml
<world name="empty_world">
  <include>
    <uri>model://ground_plane</uri>
  </include>
  <include>
    <uri>model://sun</uri>
  </include>
  <!-- Just robot and flat ground -->
</world>
```
**Learning Goal**: Test basic movement commands

**Scenario 2: Obstacle Avoidance**
```xml
<world name="obstacle_world">
  <include>
    <uri>model://ground_plane</uri>
  </include>
  <include>
    <uri>model://sun</uri>
  </include>
  
  <!-- Add obstacles -->
  <model name="obstacle_1">
    <pose>2 0 0.5 0 0 0</pose>
    <link name="link">
      <collision name="collision">
        <geometry>
          <box><size>0.5 0.5 1.0</size></box>
        </geometry>
      </collision>
      <visual name="visual">
        <geometry>
          <box><size>0.5 0.5 1.0</size></box>
        </geometry>
      </visual>
    </link>
  </model>
</world>
```
**Learning Goal**: Implement obstacle detection and avoidance

**Scenario 3: Navigation Challenge**
```xml
<world name="maze_world">
  <!-- Complex environment with walls, corridors, rooms -->
  <!-- Multiple goal locations -->
  <!-- Dynamic obstacles -->
</world>
```
**Learning Goal**: Advanced path planning and navigation

### Step 8: Add Educational Features

Include features that enhance learning:

**Visual Debugging Aids**:
```xml
<!-- Show coordinate frames -->
<plugin name="tf_visualizer" filename="libgazebo_ros_tf.so"/>

<!-- Show sensor rays -->
<visualize>true</visualize>

<!-- Show contact points -->
<plugin name="contact_visualizer" filename="libgazebo_ros_contact.so"/>
```

**Data Logging**:
```xml
<plugin name="data_logger" filename="libgazebo_ros_state_logger.so">
  <update_rate>100</update_rate>
  <log_file>simulation_data.csv</log_file>
</plugin>
```

**Performance Monitoring**:
```xml
<plugin name="performance_monitor" filename="libgazebo_ros_performance.so">
  <update_rate>1</update_rate>
  <publish_stats>true</publish_stats>
</plugin>
```

### Step 9: Document Sim-to-Real Gaps

Clearly document simulation limitations:

**Documentation Template**:
```markdown
## Simulation Limitations

### Known Sim-to-Real Gaps

#### 1. Perfect Odometry
**Simulation**: Wheel encoders provide perfect position tracking
**Reality**: Wheel slip, encoder quantization, drift accumulation
**Impact**: Students may over-rely on odometry
**Mitigation**: Add Gaussian noise (σ=0.01m) to odometry

#### 2. Instantaneous Sensor Updates
**Simulation**: Sensors update with zero latency
**Reality**: 10-100ms sensor latency, variable delays
**Impact**: Control loops may be too aggressive
**Mitigation**: Add 50ms delay to sensor data

#### 3. Simplified Friction
**Simulation**: Constant friction coefficients
**Reality**: Friction varies with speed, temperature, surface condition
**Impact**: Turning behavior differs from real robot
**Mitigation**: Document expected differences, test on real hardware

#### 4. Perfect Lighting
**Simulation**: Consistent, ideal lighting
**Reality**: Shadows, glare, varying illumination
**Impact**: Vision algorithms may fail in real conditions
**Mitigation**: Add lighting variations, test with real images

### Recommended Validation
1. Test algorithms in simulation first
2. Validate key assumptions on real hardware
3. Iterate between sim and real
4. Document all differences observed
```

### Step 10: Optimize Performance

Ensure simulation runs efficiently:

**Performance Optimization Checklist**:
- [ ] Use simplified collision meshes
- [ ] Reduce polygon count on visual meshes
- [ ] Limit sensor update rates to necessary values
- [ ] Use appropriate physics step size
- [ ] Disable unused plugins
- [ ] Optimize world complexity
- [ ] Monitor real-time factor

**Performance Tuning**:
```xml
<!-- Reduce visual quality for performance -->
<scene>
  <ambient>0.4 0.4 0.4 1</ambient>
  <background>0.7 0.7 0.7 1</background>
  <shadows>false</shadows>  <!-- Disable for performance -->
</scene>

<!-- Use simpler collision shapes -->
<collision name="collision">
  <geometry>
    <!-- Use box instead of mesh when possible -->
    <box><size>1 1 1</size></box>
  </geometry>
</collision>
```

## Output Format

Present simulation environments with complete documentation:

### For Gazebo World:
```xml
<?xml version="1.0"?>
<sdf version="1.6">
  <world name="educational_world">
    <!-- Physics configuration -->
    <physics type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
      <ode>
        <solver>
          <type>quick</type>
          <iters>50</iters>
        </solver>
      </ode>
    </physics>
    
    <!-- Lighting -->
    <include>
      <uri>model://sun</uri>
    </include>
    
    <!-- Ground -->
    <include>
      <uri>model://ground_plane</uri>
    </include>
    
    <!-- Environment objects -->
    <!-- ... -->
    
    <!-- Plugins -->
    <!-- ... -->
  </world>
</sdf>
```

### With README:
```markdown
# Simulation Environment: [Name]

## Purpose
Brief description of what this environment is for

## Learning Objectives
- Objective 1
- Objective 2

## Environment Description
- Size: 10m x 10m
- Obstacles: 5 static boxes
- Sensors: Lidar, Camera, IMU
- Complexity: Medium

## Running the Simulation
```bash
ros2 launch package_name world.launch.py
```

## Known Limitations
- List sim-to-real gaps
- Document workarounds

## Performance
- Expected real-time factor: 1.0
- CPU usage: ~40%
- GPU usage: ~20%

## Troubleshooting
Common issues and solutions
```

## Common Patterns

### Pattern 1: Progressive World Series

Create series of worlds with increasing complexity:

```
worlds/
├── 01_empty.world          # Flat ground only
├── 02_simple_obstacles.world  # Few boxes
├── 03_structured.world     # Walls and corridors
├── 04_realistic.world      # Furniture and objects
└── 05_dynamic.world        # Moving obstacles
```

### Pattern 2: Modular Environment

Build reusable components:

```
models/
├── obstacles/
│   ├── box_small/
│   ├── box_large/
│   └── cylinder/
├── furniture/
│   ├── table/
│   ├── chair/
│   └── shelf/
└── sensors/
    ├── lidar_2d/
    ├── camera_rgb/
    └── depth_camera/
```

### Pattern 3: Scenario-Based Learning

Create specific scenarios for learning objectives:

```
scenarios/
├── navigation_basics/
│   ├── straight_line.world
│   ├── simple_turn.world
│   └── figure_eight.world
├── obstacle_avoidance/
│   ├── static_obstacles.world
│   ├── narrow_passage.world
│   └── dynamic_obstacles.world
└── manipulation/
    ├── pick_and_place.world
    ├── stacking.world
    └── assembly.world
```

## Troubleshooting

### Simulation Runs Too Slow

**Problem**: Real-time factor < 0.5

**Solutions**:
1. Increase physics step size (0.001 → 0.002)
2. Reduce sensor update rates
3. Simplify collision meshes
4. Disable shadows and reflections
5. Reduce world complexity
6. Use faster physics solver

### Physics Explosions

**Problem**: Objects fly apart or behave erratically

**Solutions**:
1. Decrease physics step size
2. Increase solver iterations
3. Check for overlapping geometries
4. Verify mass and inertia values
5. Adjust contact parameters (kp, kd)
6. Check joint limits and constraints

### Sensor Data Unrealistic

**Problem**: Sensor readings don't match expectations

**Solutions**:
1. Add noise models to sensors
2. Verify sensor placement and orientation
3. Check update rates
4. Validate range limits
5. Test with known objects/distances
6. Compare with real sensor specifications

## Integration with Other Skills

This skill works well with:

**→ robotics-content-creator**: Create content using simulation environments
**→ practical-exercise-builder**: Design exercises with simulation scenarios
**→ technical-documentation-writer**: Document simulation setup and usage

## Tips for Success

1. **Start Simple**: Begin with empty world, add complexity gradually
2. **Match Real Hardware**: Use actual sensor specifications
3. **Add Noise**: Perfect sensors teach wrong intuitions
4. **Document Gaps**: Be explicit about sim-to-real differences
5. **Test Performance**: Ensure real-time operation
6. **Validate Physics**: Check against known physical behaviors
7. **Provide Variants**: Offer multiple difficulty levels
8. **Include Debugging**: Add visualization aids
9. **Optimize Meshes**: Use simple collision geometry
10. **Version Control**: Track world files with git

---

**Ready to build simulation environment?** Provide:
- Learning objective
- Robot platform
- Required sensors
- Complexity level
- Performance constraints
- Target simulator (Gazebo/Isaac/Unity)
