import React from 'react';
import {AbsoluteFill} from 'remotion';

// This bypasses your script/scenes entirely - just a solid red box with
// text, no animation, no JSON, no audio. If THIS renders blank too, the
// problem is environmental (something about your machine/render setup),
// not your actual video content. If this renders correctly, the problem
// is specifically in the scenes/script pipeline, and we know where to look.
export const TestComposition: React.FC = () => {
  return (
    <AbsoluteFill style={{backgroundColor: '#FF0000'}}>
      <div
        style={{
          color: 'white',
          fontSize: 80,
          fontFamily: 'Arial, sans-serif',
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
        }}
      >
        TEST OK
      </div>
    </AbsoluteFill>
  );
};
