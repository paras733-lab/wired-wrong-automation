import React from 'react';
import {useCurrentFrame, spring, useVideoConfig} from 'remotion';

type Props = {
  label: string;
  x: number; // position as % of frame width
  color?: string;
  delayFrames?: number;
  icon?: string | null; // any emoji works, e.g. '👑' '📜' '⏳' '🧠' '⛓️'
};

// A simple stick figure drawn entirely in code — no image assets, no paid
// illustration packs. Swap the SVG paths here later if you want a fancier
// style once you're monetized; the animation logic stays the same.
export const StickFigure: React.FC<Props> = ({
  label,
  x,
  color = '#2B2D42',
  delayFrames = 0,
  icon = null,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const entrance = spring({
    frame: frame - delayFrames,
    fps,
    config: {damping: 12, stiffness: 120},
  });

  const translateY = (1 - entrance) * 60; // slides up into place
  const opacity = entrance;

  return (
    <div
      style={{
        position: 'absolute',
        left: `${x}%`,
        top: '14%',
        transform: `translate(-50%, ${translateY}px)`,
        opacity,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
      }}
    >
      <svg width="300" height="525" viewBox="0 -30 120 210">
        <circle cx="60" cy="30" r="20" fill="none" stroke={color} strokeWidth="6" />
        <line x1="60" y1="50" x2="60" y2="120" stroke={color} strokeWidth="6" />
        <line x1="60" y1="70" x2="20" y2="100" stroke={color} strokeWidth="6" />
        <line x1="60" y1="70" x2="100" y2="100" stroke={color} strokeWidth="6" />
        <line x1="60" y1="120" x2="30" y2="170" stroke={color} strokeWidth="6" />
        <line x1="60" y1="120" x2="90" y2="170" stroke={color} strokeWidth="6" />
        {icon && (
          <text x="60" y="-8" fontSize="26" textAnchor="middle">{icon}</text>
        )}
      </svg>
      <div
        style={{
          marginTop: 4,
          fontFamily: 'Inter, sans-serif',
          fontWeight: 600,
          fontSize: 40,
          color,
        }}
      >
        {label}
      </div>
    </div>
  );
};
