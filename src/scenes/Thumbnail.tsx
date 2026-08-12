import React from 'react';
import {AbsoluteFill} from 'remotion';
import thumbData from '../scripts/thumbnail-data.json';

// A single static frame, designed specifically for click-through rate,
// not a random moment pulled from the video. Bold headline, big dramatic
// icon, high contrast. Rendered once via `remotion still`, then uploaded
// as the video's custom thumbnail.
export const Thumbnail: React.FC = () => {
  const {headline, icon} = thumbData;

  return (
    <AbsoluteFill style={{backgroundColor: '#1B1A2E'}}>
      <div
        style={{
          position: 'absolute',
          left: 60,
          top: 0,
          bottom: 0,
          width: '58%',
          display: 'flex',
          alignItems: 'center',
        }}
      >
        <div
          style={{
            fontFamily: 'Georgia, serif',
            fontWeight: 700,
            fontSize: 84,
            lineHeight: 1.08,
            color: '#FFFFFF',
          }}
        >
          {headline}
        </div>
      </div>

      <div
        style={{
          position: 'absolute',
          right: 40,
          top: 0,
          bottom: 0,
          width: '38%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <svg width="380" height="713" viewBox="0 -45 120 225">
          <circle cx="60" cy="30" r="20" fill="none" stroke="#5DCAA5" strokeWidth="7" />
          <line x1="60" y1="50" x2="60" y2="120" stroke="#5DCAA5" strokeWidth="7" />
          <line x1="60" y1="70" x2="20" y2="100" stroke="#5DCAA5" strokeWidth="7" />
          <line x1="60" y1="70" x2="100" y2="100" stroke="#5DCAA5" strokeWidth="7" />
          <line x1="60" y1="120" x2="30" y2="170" stroke="#5DCAA5" strokeWidth="7" />
          <line x1="60" y1="120" x2="90" y2="170" stroke="#5DCAA5" strokeWidth="7" />
          <text x="60" y="-14" fontSize="34" textAnchor="middle">{icon}</text>
        </svg>
      </div>

      <div
        style={{
          position: 'absolute',
          bottom: 28,
          left: 40,
          display: 'flex',
          alignItems: 'center',
          gap: 8,
        }}
      >
        <span style={{fontSize: 26}}>💡</span>
        <span style={{fontFamily: 'Inter, sans-serif', fontWeight: 600, fontSize: 26, color: '#9A98B5'}}>
          Wired Wrong
        </span>
      </div>
    </AbsoluteFill>
  );
};
