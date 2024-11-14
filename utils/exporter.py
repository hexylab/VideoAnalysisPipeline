# utils/exporter.py
from abc import ABC, abstractmethod
import os

class Exporter(ABC):
    @abstractmethod
    def export(self, frame, frame_number):
        pass

# テキストファイルに出力する派生クラス
class TextFileExporter(Exporter):
    def __init__(self, output_dir="output"):
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir

    def export(self, frame, frame_number):
        output_path = os.path.join(self.output_dir, f"frame_{frame_number}.txt")
        with open(output_path, "w") as f:
            f.write(str(frame))
        print(f"Saved: {output_path}")

# データベースに出力する派生クラス（例）
class DatabaseExporter(Exporter):
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def export(self, frame, frame_number):
        # データベースに保存する処理（例）
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO frames (frame_number, data) VALUES (?, ?)",
                       (frame_number, str(frame)))
        self.db_connection.commit()
        print(f"Frame {frame_number} saved to database.")