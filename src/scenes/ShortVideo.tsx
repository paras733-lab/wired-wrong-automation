import React from 'react';
import {Series, Audio, staticFile, AbsoluteFill} from 'remotion';
import {Scene} from './Scene';
import {Watermark} from '../components/Watermark';
import script from '../scripts/short-script.json';

export const ShortVideo: React.FC = () => {
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
      <Watermark />
    </AbsoluteFill>
  );
};

export const getShortDurationInFrames = () => {
  return script.scenes.reduce(
    (sum, s) => sum + Math.round(s.durationInSeconds * script.fps),
    0
  );
};
