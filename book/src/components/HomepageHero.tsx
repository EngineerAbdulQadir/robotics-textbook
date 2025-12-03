import React from 'react';
import Link from '@docusaurus/Link';
import '../css/homepage.css';

export default function HomepageHero() {
  return (
    <div className="hero">
      <div className="hero-content">
        {/* Left: Hero Visual */}
        <div className="hero-visual">
          <div className="hero-visual-image">
            🤖🦾
          </div>
        </div>

        {/* Right: Hero Text & CTA */}
        <div className="hero-text">
          <div className="hero-badge">PHYSICAL AI LEARNING</div>

          <h1>
            Physical AI &<br />
            Humanoid Robotics
          </h1>

          <p>
            Master ROS 2, robot control, and simulation through hands-on learning.
            From ROS 2 fundamentals to autonomous robot behavior—build the complete
            pipeline for physical AI systems.
          </p>

          <div className="hero-buttons">
            <Link
              href="/docs/module-1/"
              className="btn btn-primary"
            >
              ▶ Start Learning
            </Link>
            <a
              href="https://github.com/92Bilal26/physical-ai-textbook"
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-secondary"
            >
              ⭐ GitHub
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
