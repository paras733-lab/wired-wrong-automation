import React from 'react';
import {Series, Audio, staticFile, AbsoluteFill} from 'remotion';
import {Scene} from './Scene';
import script from '../scripts/example-script.json';

// This component never changes between videos. To make a new video, you
// only ever touch the script JSON (and record/generate a new voiceover).
// Same philosophy as your Shorts channel: content changes, pipeline doesn't.
export const ExplainerVideo: React.FC = () => {
  const fps = script.fps;

  return (
    <AbsoluteFill>
      {script.voiceoverFile && (
        <Audio src={staticFile(script.voiceoverFile)} />
      )}
      <Series>
        {script.scenes.map((scene) => (
          <Series.Sequence
            key={scene.id}
            durationInFrames={Math.round(scene.durationInSeconds * fps)}
          >
            <Scene scene={scene as any} />
          </Series.Sequence>
        ))}
      </Series>
    </AbsoluteFill>
  );
};

// Total duration in frames, used by Root.tsx to configure the composition.
export const getTotalDurationInFrames = () => {
  return script.scenes.reduce(
    (sum, s) => sum + Math.round(s.durationInSeconds * script.fps),
    0
  );
};
