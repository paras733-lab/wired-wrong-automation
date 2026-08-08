import React from 'react';
import {Composition} from 'remotion';
import {ExplainerVideo, getTotalDurationInFrames} from './scenes/ExplainerVideo';
import {TestComposition} from './scenes/TestComposition';
import script from './scripts/example-script.json';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Test"
        component={TestComposition}
        durationInFrames={90}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="Explainer"
        component={ExplainerVideo}
        durationInFrames={getTotalDurationInFrames()}
        fps={script.fps}
        width={1920}
        height={1080}
      />
    </>
  );
};
