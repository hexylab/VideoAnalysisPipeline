# Streaming Object Detection and Tracking Pipeline

## 概要
このプロジェクトは、Webカメラやビデオストリームから取得したフレームに対し、物体検出とトラッキングを行うパイプラインツールです。`YOLOX`などの認識エンジンを使用した物体検出や、`ByteTrack`などのトラッキングエンジンを組み合わせて、リアルタイムで処理を行うことができます。

## 主な機能
- **DataLoader**：Webカメラ、RTSPストリーム、MP4ファイルからのフレーム読み込み
- **Pipeline**：検出エンジン、トラッキングエンジンをDAG形式で構築し、フレーム単位で処理を実行
- **Exporter**：処理結果をテキストファイルやデータベース、HLSストリームなどに保存
- **Visualizer**：処理後のフレームに対し、物体検出やトラッキングの結果を可視化

## ディレクトリ構造
```
project_root/
├── detectors/
│   ├── base_detector.py         # Detector基底クラス
│   ├── yolox_detector.py        # YOLOXDetectorクラス
│   └── other_detector.py        # 他のDetectorクラス
│
├── trackers/
│   ├── base_tracker.py          # Tracker基底クラス
│   ├── bytetrack_tracker.py     # ByteTrackTrackerクラス
│   └── other_tracker.py         # 他のTrackerクラス
│
├── pipeline/
│   ├── frame.py                 # Frameクラス（フレームデータ管理）
│   └── pipeline.py              # Pipelineクラス（DAG形式のパイプライン処理）
│
├── utils/
│   ├── data_loader.py           # DataLoader基底クラスと派生クラス
│   ├── exporter.py              # Exporter基底クラスと派生クラス
│   └── visualizer.py            # Visualizer基底クラスと派生クラス
│
├── environment.yml              # conda環境設定ファイル
└── main.py                      # 実行スクリプト
```

## 環境構築

1. **Conda環境の作成**  
   プロジェクトの依存関係は`environment.yml`に記述されています。以下のコマンドでConda環境を作成してください。
   ```bash
   conda env create -f environment.yml
   ```

2. **環境のアクティベート**
   ```bash
   conda activate <環境名>
   ```

## 使い方

1. **main.pyの実行**  
   デフォルトの設定でWebカメラからデータを取得し、パイプライン処理を行います。
   ```bash
   python main.py
   ```

2. **DataLoaderのカスタマイズ**  
   `utils/data_loader.py`内でWebカメラ以外にRTSPストリームやMP4ファイルを読み込む`DataLoader`派生クラスを選択できます。

3. **Exporterの変更**  
   `utils/exporter.py`で、結果をテキストファイル以外にデータベースやHLSストリームなどに出力するように変更できます。

4. **Visualizerの設定**  
   `utils/visualizer.py`に記述されたクラスを使用して、検出結果やトラッキング結果をフレームに描画し、リアルタイムで表示します。

## 基本的なクラス構造

### Frameクラス
各フレームごとのデータを管理し、`Pipeline`クラスを通して`Detector`や`Tracker`で処理されるデータを格納します。

### Pipelineクラス
DAG形式で各処理をチェーンとして追加し、`execute()`メソッドで一連の処理を順次実行します。

### DataLoader基底クラスと派生クラス
- **CameraDataLoader**：Webカメラからフレームを取得します。
- **MP4DataLoader**：MP4ファイルからフレームを取得します。

### Exporter基底クラスと派生クラス
- **TextFileExporter**：処理結果をテキストファイルに出力します。
- **DatabaseExporter**：処理結果をデータベースに保存します。

### Visualizer基底クラスと派生クラス
- **YOLOXVisualizer**：YOLOXの検出結果を表示するためのビジュアライザです。  
  他のエンジン用のビジュアライザも同様に追加可能です。

## 注意事項
- `main.py`でパイプラインに組み込む`Detector`、`Tracker`、`Exporter`、`Visualizer`のクラスはプロジェクトの用途に合わせて適宜設定してください。
- カメラやストリーミングデータからの読み込みは、実行環境やデバイスに応じて調整が必要です。

## ライセンス
このプロジェクトはApache License 2.0のもとで公開されています。詳細はLICENSEファイルをご覧ください。