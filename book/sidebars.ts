import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

/**
 * Physical AI & Humanoid Robotics Textbook
 * Complete 4-Module Curriculum Structure
 */

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'introduction',
      label: 'Introduction',
    },
    
    // Module 1
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      collapsed: false,
      collapsible: true,
      link: {
        type: 'doc',
        id: 'module-1/index',
      },
      items: [
        {
          type: 'doc',
          id: 'module-1/chapter-1',
          label: 'Chapter 1: Introduction to Embodied AI and Robotics',
        },
        {
          type: 'doc',
          id: 'module-1/chapter-2',
          label: 'Chapter 2: ROS 2 Fundamentals: Nodes, Topics, and Services',
        },
        {
          type: 'doc',
          id: 'module-1/chapter-3',
          label: 'Chapter 3: ROS 2 Tools: RViz, Gazebo, and the CLI',
        },
      ],
    },
    
    // Module 2
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      collapsed: true,
      link: {
        type: 'doc',
        id: 'module-2/index',
      },
      items: [
        {
          type: 'doc',
          id: 'module-2/chapter-4',
          label: 'Chapter 4: Camera Systems and Image Processing in ROS 2',
        },
        {
          type: 'doc',
          id: 'module-2/chapter-5',
          label: 'Chapter 5: Lidar and Depth Sensing: Building Point Clouds',
        },
        {
          type: 'doc',
          id: 'module-2/chapter-6',
          label: 'Chapter 6: Sensor Fusion: Combining Data for Robust Perception',
        },
      ],
    },
    
    // Module 3
    {
      type: 'category',
      label: 'Module 3: Motion, Control, and Navigation',
      collapsed: true,
      link: {
        type: 'doc',
        id: 'module-3/index',
      },
      items: [
        {
          type: 'doc',
          id: 'module-3/chapter-7',
          label: 'Chapter 7: Inverse Kinematics for Humanoid Arms',
        },
        {
          type: 'doc',
          id: 'module-3/chapter-8',
          label: 'Chapter 8: Bipedal Locomotion: Walking and Balance',
        },
        {
          type: 'doc',
          id: 'module-3/chapter-9',
          label: 'Chapter 9: Navigation Stack: From A to B Autonomously',
        },
      ],
    },
    
    // Module 4
    {
      type: 'category',
      label: 'Module 4: Advanced Topics and Real-World Deployment',
      collapsed: true,
      link: {
        type: 'doc',
        id: 'module-4/index',
      },
      items: [
        {
          type: 'doc',
          id: 'module-4/chapter-10',
          label: 'Chapter 10: NVIDIA Isaac Sim and Omniverse',
        },
        {
          type: 'doc',
          id: 'module-4/chapter-11',
          label: 'Chapter 11: Vision-Language-Action (VLA) Models',
        },
        {
          type: 'doc',
          id: 'module-4/chapter-12',
          label: 'Chapter 12: Deploying to Real Hardware',
        },
      ],
    },
    
    // Module 5
    {
      type: 'category',
      label: 'Module 5: Capstone Projects',
      collapsed: true,
      link: {
        type: 'doc',
        id: 'module-5/index',
      },
      items: [
        {
          type: 'doc',
          id: 'module-5/capstone',
          label: 'Capstone Project: The Autonomous Humanoid',
        },
      ],
    },
  ],
};

export default sidebars;
