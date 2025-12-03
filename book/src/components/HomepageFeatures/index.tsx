import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import { Bot, Cpu, Zap, Code, Brain, Rocket } from 'lucide-react';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Icon: any;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Physical AI Fundamentals',
    Icon: Bot,
    description: (
      <>
        Learn the core concepts of physical AI, robotics, and embodied intelligence
        through interactive lessons and hands-on examples.
      </>
    ),
  },
  {
    title: 'Hardware & Software Integration',
    Icon: Cpu,
    description: (
      <>
        Master the integration of sensors, actuators, and AI algorithms to build
        intelligent robotic systems.
      </>
    ),
  },
  {
    title: 'Real-World Applications',
    Icon: Rocket,
    description: (
      <>
        Explore practical applications in autonomous vehicles, industrial automation,
        and service robotics.
      </>
    ),
  },
  {
    title: 'Machine Learning for Robotics',
    Icon: Brain,
    description: (
      <>
        Apply deep learning, reinforcement learning, and computer vision to create
        adaptive robotic behaviors.
      </>
    ),
  },
  {
    title: 'Hands-On Projects',
    Icon: Code,
    description: (
      <>
        Build real projects with popular frameworks like ROS, PyTorch, and TensorFlow
        for robotics applications.
      </>
    ),
  },
  {
    title: 'Fast-Paced Learning',
    Icon: Zap,
    description: (
      <>
        Progress quickly with structured modules, code examples, and guided exercises
        designed for rapid skill development.
      </>
    ),
  },
];

function Feature({title, Icon, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4', styles.feature)}>
      <div className={styles.iconWrapper}>
        <Icon className={styles.featureIcon} size={32} />
      </div>
      <div className={styles.featureContent}>
        <Heading as="h3" className={styles.featureTitle}>{title}</Heading>
        <p className={styles.featureDescription}>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
