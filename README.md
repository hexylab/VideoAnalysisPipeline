
# Video Analytics Pipeline

## 概要
映像データに対して物体検出やトラッキングを行うためのパイプライン処理が記述できるフレームワークです。
処理タスクをDAGで記述することができ、簡単に動画に対する処理を記述することが可能です。
- DetectorやTracker、ユーティリティ（DataLoader、Visualizer、Exporterなど）を自由にカスタマイズ可能です。
- 複数のAIアルゴリズムを組み合わせて簡単に映像分析パイプラインを構築できます。

## 実装済みの機能
### Detector
- **YOLOX**: 物体検出アルゴリズム
  - 設定ファイル: `detectors/yolox/config.yaml`
  - モデル: `detectors/yolox/model/yolox_nano.pth`

### Tracker
- **ByteTrack**: マルチオブジェクトトラッキングアルゴリズム
  - 設定ファイル: `trackers/bytetrack/config.yaml`

### Utility
- **DataLoader**: データを効率的に読み込むためのモジュール。
- **Visualizer**: 検出結果やトラッキング結果を描画するツール。
- **Exporter**: 分析結果を保存するためのエクスポート機能。

## セットアップ
1. リポジトリをクローンします:
   ```bash
   git clone <repository-url>
   cd VideoAnalyticsPipeline
   ```
2. 仮想環境を作成し、アクティベートします:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
   ```
3. 依存関係をインストールします:
   ```bash
   pip install -r requirements.txt
   ```
   または、Condaを使用して環境をセットアップします:
   ```bash
   conda env create -f environment.yml
   conda activate video-analytics
   ```

## 使用方法
1. サンプルパイプラインを実行するには以下を実行します:
   ```bash
   python main.py
   ```
   - `main.py`はサンプルスクリプトであり、デフォルトのDAG（`pipeline_dag.png`）が生成されます。
   - 実際の用途に応じて、`pipeline/pipeline.py`を編集することでパイプラインをカスタマイズできます。


## ディレクトリ構造
```
VideoAnalyticsPipeline/
├── main.py                     # サンプルアプリ
├── pipeline/                   # パイプライン処理のコア実装
│   ├── __init__.py
│   ├── frame.py                # 処理間で受け渡すフレームクラス
│   └── pipeline.py             # パイプラインロジック
├── detectors/                  # 物体検出モジュール
│   ├── base_detector.py
│   └── yolox/
│       ├── yolox_detector.py
│       ├── config.yaml         # YOLOXの設定
│       └── model/              # 事前学習済みモデル
├── trackers/                   # トラッキングモジュール
│   ├── base_tracker.py
│   └── bytetrack/
│       ├── bytetrack_tracker.py
│       ├── config.yaml         # ByteTrackの設定
│       └── tracker/            
├── utils/                      # ユーティリティ関数
│   ├── data_loader.py
│   ├── exporter.py
│   └── visualizer.py
├── environment.yml             # Conda環境設定ファイル
├── LICENSE                     # ライセンス情報
└── README.md                   # プロジェクトドキュメント
```

## ライセンス
このプロジェクトは[LICENSE](LICENSE)に記載されている条件の下で提供されています。