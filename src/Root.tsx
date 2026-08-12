import React from 'react';
import {Composition} from 'remotion';
import {ExplainerVideo, getTotalDurationInFrames} from './scenes/ExplainerVideo';
import {ShortVideo, getShortDurationInFrames} from './scenes/ShortVideo';
import {Thumbnail} from './scenes/Thumbnail';
import script from './scripts/example-script.json';
import shortScript from './scripts/short-script.json';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Explainer"
        component={ExplainerVideo}
        durationInFrames={getTotalDurationInFrames()}
        fps={script.fps}
        width={1920}
        height={1080}
      />
      <Composition
        id="Short"
        component={ShortVideo}
        durationInFrames={getShortDurationInFrames()}
        fps={shortScript.fps}
        width={1080}
        height={1920}
      />
      <Composition
        id="Thumbnail"
        component={Thumbnail}
        durationInFrames={1}
        fps={30}
        width={1280}
        height={720}
      />
    </>
  );
};
