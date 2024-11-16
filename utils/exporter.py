# utils/exporter.py
from abc import ABC, abstractmethod
import os
import cv2
import threading
import subprocess
import time

class Exporter(ABC):
    @abstractmethod
    def export(self, frame, frame_number):
        pass

# テキストファイルに出力する派生クラス
class TextFileExporter(Exporter):
    def __init__(self, output_dir="output"):
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir

    def export(self, frame):
        output_path = os.path.join(self.output_dir, f"frame.txt")
        with open(output_path, "w") as f:
            f.write(str(frame))
        print(f"Saved: {output_path}")
        return frame

# MP4に出力する派生クラス
class MP4Exporter:
    def __init__(self, output_file="output/video.mp4", frame_size=(640, 480), fps=30):
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        self.output_file = output_file
        self.frame_size = frame_size
        self.fps = fps
        self.writer = None
        # 初期化時にVideoWriterを作成
        self._start_writer()

    def _start_writer(self):
        """VideoWriterを初期化または再初期化します。"""
        if self.writer:
            self.writer.release()

        self.writer = cv2.VideoWriter(
            self.output_file,
            cv2.VideoWriter_fourcc(*'mp4v'),
            self.fps,
            self.frame_size
        )

    def export(self, frame):
        """フレームを動画に書き込みます。"""
        # フレームのFPSや解像度が現在の設定と異なる場合に再初期化
        if frame.fps != self.fps or (frame.width, frame.height) != self.frame_size:
            print(f"MP4 Stream: FPS={frame.fps}, サイズ=({frame.width}, {frame.height})")
            self.fps = frame.fps
            self.frame_size = (frame.width, frame.height)
            self._start_writer()

        if frame.vis_img is not None:
            # フレームをリサイズして書き込み
            resized_frame = cv2.resize(frame.vis_img, self.frame_size)
            self.writer.write(resized_frame)
        return frame

    def close(self):
        """VideoWriterを解放します。"""
        if self.writer:
            self.writer.release()
            self.writer = None
            print(f"Video saved: {self.output_file}")


# HLSに出力する派生クラス
class HLSExporter:
    def __init__(self, output_dir="output/hls", frame_size=(640, 480), fps=30):
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir
        self.frame_size = frame_size
        self.fps = fps
        self.pipe = None
        self.hls_segment_filename = os.path.join(self.output_dir, "segment_%03d.ts")
        self.hls_playlist_filename = os.path.join(self.output_dir, "playlist.m3u8")
        
        # 初期化時にFFmpegプロセスを開始
        self._start_ffmpeg()

    def _start_ffmpeg(self):
        """FFmpegプロセスを開始または再起動します。"""
        if self.pipe:
            # 既存のFFmpegプロセスを停止
            self.close()
        
        self.pipe = subprocess.Popen(
            [
                'ffmpeg',
                '-y',  # Overwrite output files
                '-f', 'rawvideo',
                '-vcodec', 'rawvideo',
                '-pix_fmt', 'bgr24',
                '-s', f"{self.frame_size[0]}x{self.frame_size[1]}",
                '-r', str(self.fps),
                '-i', '-',  # Input from pipe
                '-c:v', 'libx264',
                '-preset', 'veryfast',
                '-f', 'hls',
                '-hls_time', '1',
                '-hls_list_size', '5',
                '-hls_segment_filename', self.hls_segment_filename,
                self.hls_playlist_filename
            ],
            stdin=subprocess.PIPE
        )

    def export(self, frame):
        """フレームをFFmpegプロセスに送信します。"""
        # フレームのFPSや解像度が異なる場合にプロセスを再起動
        if frame.fps != self.fps or (frame.width, frame.height) != self.frame_size:
            print(f"HLS Stream: FPS={frame.fps}, サイズ=({frame.width}, {frame.height})")
            self.fps = frame.fps
            self.frame_size = (frame.width, frame.height)
            self._start_ffmpeg()

        if frame.vis_img is not None and self.pipe and self.pipe.stdin:
            # フレームをリサイズして送信
            resized_frame = cv2.resize(frame.vis_img, self.frame_size)
            self.pipe.stdin.write(resized_frame.tobytes())
        return frame

    def close(self):
        """FFmpegプロセスを終了します。"""
        if self.pipe:
            self.pipe.stdin.close()
            self.pipe.wait()
            self.pipe = None
            print(f"HLS stream saved: {self.hls_playlist_filename}")