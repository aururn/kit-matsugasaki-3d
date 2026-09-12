# KIT Matsugasaki 3D

[日本語](#kit-matsugasaki-3d) | [English](#english)

京都工芸繊維大学・松ヶ崎キャンパス（東西両地区）の非公式3Dモデルです。Blenderで制作しています。

**Work in progress / 制作途中。** 建物の形状・寸法・入口には推定を含みます。測量モデルではありません。

![キャンパス全景](previews/campus-overview.png)

## ダウンロード

[v0.1.0 制作途中版のダウンロード](https://github.com/aururn/kit-matsugasaki-3d/releases/tag/v0.1.0)

| ファイル | 内容 |
| --- | --- |
| `kit_matsugasaki_campus_v5.blend` | 東西キャンパス全体。建物、道路、植栽、校門、大学の塔 |
| `kit_building_studies_v5.blend` | 建物別75シーン・校門などの7シーンを切り替えて閲覧 |
| `SHA256SUMS.txt` | ダウンロードファイルの整合性確認用 |

`.blend` はReleasesのAssetsから取得してください。GitHubの「Code → Download ZIP」にはモデル本体は含まれません。ファイル内に必要なテクスチャ・フォントを格納しています。

## Blenderで見る

制作・検証環境は **Blender 5.2.0 LTS**。開くだけでスクリプトを実行する必要はありません。

- 中央ボタンドラッグ：回転、ホイール：拡大縮小、Shift＋中央ボタン：移動。
- テンキー0：カメラ表示。建物を選択してテンキーの小数点：選択対象へ移動。
- 建物別版は上部のシーン選択で建物を切り替えます。`Access |` は校門・塔などの視点です。
- 全体版のコレクション `09` に校門・塔・入口をまとめています。

![中央東門と大学の塔](previews/access-central-east-tower.png)

![旧正門](previews/access-historic-east-gate.png)

## 収録範囲と精度

東西両地区、3号館の歴史建築、主要な校舎・施設、8か所の門、大学の塔、資料で位置を整理した48棟・65か所の入口を収録。75のカタログ項目には付属部分や分割部分が含まれ、大学の正式な建物数とは異なります。

建物輪郭はOpenStreetMap、建物名や入口は大学公開資料、外観は公開写真を照合しています。高さ、背面、屋上設備、細部寸法には推定が残ります。塔の高さ17 mは写真からの推定、位置は約5 mの不確かさを見込んでいます。全室の内装は作成していません。

[詳細な制作状況](docs/model-notes.md) / [出典](SOURCES.md) / [入口・門・塔の根拠データ](data/access-survey.json)

## 再生成

Blenderの実行ファイルをPATHへ追加し、リポジトリのルートで順に実行します。Windows PowerShellでも同じコマンドを使えます。Blender同梱のPython・NumPyを使用し、ビルド時に外部データを取得する必要はありません。

```sh
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python scripts/historic/build_historic.py -- --build-only
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python scripts/build_campus.py -- --build-only
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python scripts/create_building_studies.py
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python scripts/validate_v5.py
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python scripts/validate_studies.py
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python scripts/validate_public_assets.py
```

モデルは `build/`、検証結果は `reports/` に出力されます。検証はファイル整合性、配置、入口の開口を確認するもので、実測精度を保証しません。生成スクリプトは `data/` の生成済みカタログ・調査結果も更新します。

v0.1.0の配布モデルは制作版v5を `scripts/export_public.py` で梱包したものです。形状を保持し、日本語フォントと出典の埋め込みを公開用に整理しています。再生成手順もBlender 5.2.0で動作確認済みです。[公開時の検証結果](docs/validation/public-assets-validation.json)を収録しています。

静止画は `scripts/render_access.py`、入口配置図は `scripts/make_access_plan.py`（通常のPythonとPillowが必要）で作成できます。Cyclesレンダリングは対応GPUがあればOptiXを使用し、それ以外はCPUを使います。大きなモデルのため生成・レンダリングには時間とメモリを要します。

## ファイル構成

- `scripts/`：生成・描画・検証スクリプト。
- `data/`：建物輪郭、入口、配置、カメラ推定値。
- `assets/`：再配布可能な環境画像・路面画像・日本語フォント。
- `previews/`：モデルのレンダリングと配置図。
- `docs/`：調査記録・制作状況。
- `LICENSES/`：同梱素材と地理データのライセンス情報。

地理データ：© OpenStreetMap contributors、ODbL 1.0。独自部分の利用許諾は現時点で未設定です。[ライセンスの適用範囲](LICENSES/README.md)を参照してください。

---

## English

An unofficial 3D model of Kyoto Institute of Technology's Matsugasaki Campus, covering both the east and west areas. Created with Blender.

**Work in progress.** Building geometry, dimensions, and entrances include estimates. This is not a measured survey model.

![Campus overview](previews/campus-overview.png)

### Download

[Download v0.1.0 — work-in-progress release](https://github.com/aururn/kit-matsugasaki-3d/releases/tag/v0.1.0)

| File | Contents |
| --- | --- |
| `kit_matsugasaki_campus_v5.blend` | The east and west campus areas, including buildings, roads, planting, gates, and the university tower |
| `kit_building_studies_v5.blend` | 75 building scenes and 7 scenes for gates and other access views |
| `SHA256SUMS.txt` | Checksums for verifying downloaded files |

Download the `.blend` files from the release's **Assets** section. GitHub's **Code → Download ZIP** does not include the models themselves. Required textures and fonts are packed into the Blender files.

### Viewing in Blender

Created and validated with **Blender 5.2.0 LTS**. You do not need to run any scripts to open the models.

- Drag with the middle mouse button to orbit, scroll to zoom, and Shift + middle mouse button to pan.
- Press Numpad 0 for the camera view. Select a building and press Numpad Decimal to frame it.
- In the building studies file, use the scene selector at the top to switch buildings. Scenes starting with `Access |` provide views of gates, the tower, and other access points.
- In the campus file, collection `09` groups the gates, tower, and entrances.

![Central east gate and university tower](previews/access-central-east-tower.png)

![Historic main gate](previews/access-historic-east-gate.png)

### Coverage and accuracy

The model includes the east and west campus areas, the historic Building 3, major academic buildings and facilities, 8 gates, the university tower, and 65 entrances across 48 buildings located using reference documents. The 75 catalog entries include annexes and subdivided building sections; they do not represent the university's official building count.

Building footprints are based on OpenStreetMap. Building names and entrances were cross-checked against university publications, and exteriors against publicly available photographs. Heights, rear facades, rooftop equipment, and detailed dimensions still include estimates. The tower's height of 17 m is estimated from photographs, and its position has an estimated uncertainty of approximately 5 m. Complete interiors have not been modeled.

[Detailed modeling notes (Japanese)](docs/model-notes.md) / [Sources](SOURCES.md) / [Entrance, gate, and tower evidence data](data/access-survey.json)

### Rebuilding the models

Add the Blender executable to your PATH, then run these commands in order from the repository root. The same commands work in Windows PowerShell. The build uses Python and NumPy bundled with Blender and does not need to download external data.

```sh
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python scripts/historic/build_historic.py -- --build-only
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python scripts/build_campus.py -- --build-only
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python scripts/create_building_studies.py
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python scripts/validate_v5.py
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python scripts/validate_studies.py
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python scripts/validate_public_assets.py
```

Models are written to `build/`, and validation reports to `reports/`. Validation checks file integrity, placement, and physical entrance openings; it does not guarantee real-world dimensional accuracy. The generation scripts also update generated catalog and survey data in `data/`.

The v0.1.0 release models were packaged from modeling revision v5 using `scripts/export_public.py`. This preserves the geometry while preparing the Japanese font and embedded source information for distribution. The rebuild procedure has also been verified with Blender 5.2.0. [Validation results from publication](docs/validation/public-assets-validation.json) are included.

Use `scripts/render_access.py` to render still images and `scripts/make_access_plan.py` to generate the entrance plan (the latter requires a standalone Python installation and Pillow). Cycles rendering uses OptiX when a compatible GPU is available and falls back to the CPU otherwise. Generating and rendering this large model requires time and memory.

### Repository structure

- `scripts/`: Model generation, rendering, and validation scripts.
- `data/`: Building footprints, entrances, placement data, and camera estimates.
- `assets/`: Redistributable environment and road textures, and a Japanese font.
- `previews/`: Model renders and a site access plan.
- `docs/`: Research records and modeling notes.
- `LICENSES/`: License information for bundled assets and geographic data.

Geographic data: © OpenStreetMap contributors, ODbL 1.0. No reuse license has been specified for this project's original content at this stage. See the [license scope](LICENSES/README.md).
