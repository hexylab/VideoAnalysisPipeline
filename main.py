import cv2

from detectors.yolox.yolox_detector import YOLOXDetector
from trackers.bytetrack.bytetrack_tracker import ByteTrackTracker
from pipeline.pipeline import Pipeline
from pipeline.frame import Frame
from utils.data_loader import CameraDataLoader
from utils.exporter import TextFileExporter
from utils.visualizer import YOLOXVisualizer

# 必要なインスタンスを作成
detector = YOLOXDetector()
tracker = ByteTrackTracker()
data_loader = CameraDataLoader()
exporter = TextFileExporter()
visualizer = YOLOXVisualizer()

# フレームごとにパイプライン処理を実行
for frame_number, frame_data in enumerate(data_loader):
    frame = Frame(frame_data)

    # パイプラインにデータを流す
    pipeline = Pipeline(frame)
    processed_frame = (
        pipeline
        .add_step(detector.detect)
        .add_step(tracker.track, dependencies=[detector.detect])
        .execute()
    )

    # 処理結果をエクスポート
    exporter.export(processed_frame, frame_number)

    # 可視化
    if not visualizer.visualize(processed_frame):
        break  # 'q'キーで終了

# リソースの解放
data_loader.release()
cv2.destroyAllWindows()