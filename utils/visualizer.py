# utils/visualizer.py
from abc import ABC, abstractmethod
import cv2

class Visualizer(ABC):
    @abstractmethod
    def visualize(self, frame):
        pass

# YOLOXの認識結果を可視化する派生クラス
class YOLOXVisualizer(Visualizer):
    def visualize(self, frame):
        frame = self.draw_frame(frame)
        cv2.imshow("YOLOX Processed Frame", frame.vis_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False
        return True

    def get_id_color(self, index):
        temp_index = abs(int(index + 1)) * 3
        color = ((37 * temp_index) % 255, (17 * temp_index) % 255, (29 * temp_index) % 255)
        return color


    def draw_frame(self, frame):
        draw_img = frame.source_img
        for id, bbox, score, class_name in zip(frame.track_ids, frame.bboxes, frame.scores, frame.classes):
            x1, y1, x2, y2 = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
            color = self.get_id_color(int(id))
            # バウンディングボックス
            draw_img = cv2.rectangle(
                draw_img,
                (x1, y1),
                (x2, y2),
                color,
                thickness=2,
            )

            # トラックID、スコア
            score = '%.2f' % score
            text = 'TID:%s(%s)' % (str(int(id)), str(score))
            draw_img = cv2.putText(
                draw_img,
                text,
                (x1, y1 - 22),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                thickness=2,
            )

            # クラスID
            text = 'CID:%s' % (str(class_name))
            draw_img = cv2.putText(
                draw_img,
                text,
                (x1, y1 - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                thickness=2,
            )

        # 経過時間(キャプチャ、物体検出、トラッキング)
        cv2.putText(
            draw_img,
            "Elapsed Time : " + '{:.1f}'.format(frame.elapsed_time * 1000) + "ms",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            1,
            cv2.LINE_AA,
        )
        frame.vis_img = draw_img
        return frame