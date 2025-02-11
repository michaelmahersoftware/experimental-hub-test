import { AlertColor } from "@mui/material/Alert";
import { SnackbarOrigin } from "@mui/material/Snackbar";

export type Session = {
  id: string;
  title: string;
  date: number;
  record: boolean;
  time_limit: number;
  description: string;
  creation_time: number;
  end_time: number;
  start_time: number;
  notes: Note[];
  participants: Participant[];
  log: [];
};

export type Note = {
  time: number;
  speakers: string[];
  content: string;
};

export type Participant = {
  id: string;
  participant_name: string;
  banned: boolean;
  size: { width: number; height: number };
  muted_video: boolean;
  muted_audio: boolean;
  position: { x: number; y: number; z: number };
  chat: ChatMessage[];
  audio_filters: AudioFilter[];
  video_filters: VideoFilter[];
};

export type Box = {
  x: number;
  y: number;
  width: number;
  height: number;
};

export type Shape = {
  x: number;
  y: number;
  fill: string;
  participant_name: string;
};

export type Group = {
  x: number;
  y: number;
  width: number;
  height: number;
};

type VideoFilter = {
  id: string;
  type: string;
};

type AudioFilter = {
  id: string;
  type: string;
  size?: number;
};

export type ChatMessage = {
  message: string;
  time: number;
  author: string;
  target: string;
};

export type Filter = {
  type: string;
  id: string;
  size?: number;
};

export type Snackbar = {
  open: boolean;
  text: string;
  severity: AlertColor;
  autoHideDuration?: number;
  anchorOrigin?: SnackbarOrigin;
};
