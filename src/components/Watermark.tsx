import React from 'react';
import {useVideoConfig} from 'remotion';

// A small, unobtrusive channel mark, present in every frame. On landscape
// (long-form) it sits bottom-right, out of the way. On vertical (Shorts),
// bottom-right is exactly where YouTube's own like/comment/share buttons
// live, and the bottom strip is covered by the title/channel bar - so on
// vertical we move it to the top instead, which stays clear on Shorts.
export const Watermark: React.FC = () => {
  const {width, height} = useVideoConfig();
  const isVertical = height > width;

  const style: React.CSSProperties = isVertical
    ? {
        position: 'absolute',
        top: 50,
        left: 0,
        right: 0,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        gap: 8,
        opacity: 0.6,
        zIndex: 100,
      }
    : {
        position: 'absolute',
        bottom: 24,
        right: 28,
        display: 'flex',
        alignItems: 'center',
        gap: 8,
        opacity: 0.55,
        zIndex: 100,
      };

  return (
    <div style={style}>
      <span style={{fontSize: isVertical ? 26 : 22}}>💡</span>
      <span
        style={{
          fontFamily: 'Inter, sans-serif',
          fontWeight: 600,
          fontSize: isVertical ? 26 : 22,
          color: '#2B2D42',
        }}
      >
        Wired Wrong
      </span>
    </div>
  );
};
