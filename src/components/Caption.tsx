import React from 'react';
import {useCurrentFrame, interpolate} from 'remotion';

type Props = {
  text: string;
};

// A simple fade-in caption bar. This is what carries most of the
// "production value" in a CGP-Grey-style video — clean typography,
// consistent placement, readable at a glance on mobile.
export const Caption: React.FC<Props> = ({text}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 12], [0, 1], {
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        position: 'absolute',
        bottom: 80,
        left: '10%',
        width: '80%',
        textAlign: 'center',
        opacity,
      }}
    >
      <div
        style={{
          display: 'inline-block',
          background: 'rgba(255,255,255,0.92)',
          borderRadius: 12,
          padding: '16px 28px',
          fontFamily: 'Inter, sans-serif',
          fontSize: 32,
          fontWeight: 600,
          color: '#2B2D42',
          boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
        }}
      >
        {text}
      </div>
    </div>
  );
};
