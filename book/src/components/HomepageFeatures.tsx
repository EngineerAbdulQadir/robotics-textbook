import React from 'react';
import { Bot, Cpu, Zap, Code, Brain, Rocket } from 'lucide-react';
import '../css/homepage.css';

interface Feature {
  Icon: any;
  title: string;
  description: string;
}

const features: Feature[] = [
  {
    Icon: Bot,
    title: 'Physical AI Fundamentals',
    description: 'Learn the core concepts of physical AI, robotics, and embodied intelligence through interactive lessons and hands-on examples.',
  },
  {
    Icon: Cpu,
    title: 'Hardware & Software Integration',
    description: 'Master the integration of sensors, actuators, and AI algorithms to build intelligent robotic systems.',
  },
  {
    Icon: Rocket,
    title: 'Real-World Applications',
    description: 'Explore practical applications in autonomous vehicles, industrial automation, and service robotics.',
  },
  {
    Icon: Brain,
    title: 'Machine Learning for Robotics',
    description: 'Apply deep learning, reinforcement learning, and computer vision to create adaptive robotic behaviors.',
  },
  {
    Icon: Code,
    title: 'Hands-On Projects',
    description: 'Build real projects with popular frameworks like ROS, PyTorch, and TensorFlow for robotics applications.',
  },
  {
    Icon: Zap,
    title: 'Fast-Paced Learning',
    description: 'Progress quickly with structured modules, code examples, and guided exercises designed for rapid skill development.',
  },
];

export default function HomepageFeatures() {
  return (
    <section className="features">
      <div className="features-grid">
        {features.map((feature, idx) => (
          <div key={idx} className="feature-card">
            <div className="feature-icon-wrapper">
              <feature.Icon className="feature-icon-svg" size={32} />
            </div>
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
