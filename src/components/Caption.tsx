import React from 'react';
import {useCurrentFrame, useVideoConfig, interpolate} from 'remotion';

type Props = {
  text: string;
};

// A simple fade-in caption bar. Automatically repositions for vertical
// (Shorts) vs landscape (long-form) - Shorts have YouTube's own UI
// overlaying the bottom (title/channel bar) and right edge (like/share
// buttons), so the caption needs to sit higher and narrower to stay
// clear of both on a vertical canvas.
export const Caption: React.FC<Props> = ({text}) => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const isVertical = height > width;

  const opacity = interpolate(frame, [0, 12], [0, 1], {
    extrapolateRight: 'clamp',
  });

  const containerStyle: React.CSSProperties = isVertical
    ? {
        position: 'absolute',
        bottom: '22%',
        left: '10%',
        right: '10%',
        textAlign: 'center',
        opacity,
      }
    : {
        position: 'absolute',
        bottom: 80,
        left: '10%',
        width: '80%',
        textAlign: 'center',
        opacity,
      };

  return (
    <div style={containerStyle}>
      <div
        style={{
          display: 'inline-block',
          background: 'rgba(255,255,255,0.92)',
          borderRadius: 12,
          padding: isVertical ? '14px 22px' : '16px 28px',
          fontFamily: 'Inter, sans-serif',
          fontSize: isVertical ? 30 : 32,
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
