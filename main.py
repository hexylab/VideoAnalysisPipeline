# main.py
import cv2
from pipeline.pipeline import Pipeline
from utils.data_loader import CameraDataLoader
from detectors.yolox.yolox_detector import YOLOXDetector
from trackers.bytetrack.bytetrack_tracker import ByteTrackTracker
from utils.visualizer import DetectTrackVisualizer
from utils.exporter import MP4Exporter


def main():
    pipeline = Pipeline(frame=None)

    # 処理タスクのインスタンスを作成
    camera_loader = CameraDataLoader(source=0)
    camerastream = camera_loader.stream 
    yolox_detector = YOLOXDetector().detect
    bytetrack_tracker = ByteTrackTracker().track
    draw_frame = DetectTrackVisualizer().draw_frame
    exporter = MP4Exporter()
    mp4_exporter = exporter.export

    # 処理パイプラインを作成
    pipeline.add_step(camerastream)
    pipeline.add_step(yolox_detector, dependencies=[camerastream])
    pipeline.add_step(bytetrack_tracker, dependencies=[yolox_detector])
    pipeline.add_step(draw_frame, dependencies=[bytetrack_tracker])
    pipeline.add_step(mp4_exporter, dependencies=[draw_frame])

    # 処理パイプラインのDAGを画像出力
    pipeline.save_dag_image("pipeline_dag.png")
    
    try:
        while True:
            pipeline.execute()

    except KeyboardInterrupt:
        print("処理が中断されました")

    finally:
        camera_loader.release()
        exporter.close()
        cv2.destroyAllWindows()
        print("終了しました")

if __name__ == "__main__":
    main()