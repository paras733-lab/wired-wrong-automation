import React from 'react';
import {AbsoluteFill} from 'remotion';
import {StickFigure} from '../components/StickFigure';
import {Caption} from '../components/Caption';

type Beat =
  | {type: 'singleFigure'; label: string; icon?: string; animation?: string}
  | {type: 'twoFigures'; leftLabel: string; rightLabel: string; leftIcon?: string; rightIcon?: string; animation?: string}
  | {type: 'arrow'; fromLabel: string; toLabel: string; arrowText?: string; animation?: string};

type SceneData = {
  id: string;
  durationInSeconds: number;
  caption: string;
  beat: Beat;
};

// This is the piece you extend over time: every new "beat.type" you invent
// (a chart, a map, a timeline) just needs one new case here. The script
// JSON never needs to know any React — it only speaks in beat types.
export const Scene: React.FC<{scene: SceneData}> = ({scene}) => {
  const {beat, caption} = scene;

  return (
    <AbsoluteFill style={{backgroundColor: '#FDFDFD'}}>
      {beat.type === 'singleFigure' && (
        <StickFigure label={beat.label} x={50} icon={beat.icon ?? null} />
      )}

      {beat.type === 'twoFigures' && (
        <>
          <StickFigure label={beat.leftLabel} x={30} icon={beat.leftIcon} />
          <StickFigure label={beat.rightLabel} x={70} delayFrames={10} icon={beat.rightIcon} />
        </>
      )}

      {beat.type === 'arrow' && (
        <>
          <StickFigure label={beat.fromLabel} x={30} />
          <StickFigure label={beat.toLabel} x={70} delayFrames={10} />
          <div
            style={{
              position: 'absolute',
              top: '38%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              fontSize: 40,
            }}
          >
            {beat.arrowText ?? '→'}
          </div>
        </>
      )}

      <Caption text={caption} />
    </AbsoluteFill>
  );
};
