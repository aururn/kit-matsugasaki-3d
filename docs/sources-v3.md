# 出典と観察記録

## キャンパス配置

- 京都工芸繊維大学 [公式キャンパスマップ](https://www.kit.ac.jp/uni_index/campus-map/)：2026年6月1日版。東西の建物名、4・5号館の接続、D-lab、運動施設、北側歴史建築の区画を照合。
- [OpenStreetMap API](https://api.openstreetmap.org/api/0.6/map?bbox=135.779,35.046,135.787,35.054)：建物輪郭、道路、駐車場、運動施設。元データは `references/osm.xml`。© OpenStreetMap contributors。[著作権・ODbL](https://www.openstreetmap.org/copyright)。建物の階数や最新の外観まで確認できるデータではない。
- `prepare_site.py` で大学境界内を抽出し、`prepare_catalog.py` で公式図に合わせて複数号館の輪郭を分割。全体モデルは建築測量ではない。

## 3号館

- [徳岡設計・京都工芸繊維大学3号館改修](https://www.tokuoka-ao.co.jp/works/educational/kosen_3/)：2・3階の薄い張り出しと連続窓、改修後のサッシ、玄関庇を確認。細部が不鮮明な部分の寸法は推定。
- [大学公式・3号館](https://www.kit.ac.jp/2018/06/k-n_sangoukan/)：正面玄関、扉、階段。
- [文化庁・本館及び講堂](https://kunishitei.bunka.go.jp/bsys/maindetails/101/00006970)：3階建、E字形、スクラッチタイル、南北面の連続窓。
- v2の詳しい参考写真・カメラ推定記録は `historic-research.md`。今回の側面・背面の扉には、位置・形状を推定した部分がある。

## 他の主な建物

- [公式・キャンパス＆周辺散策](https://www.kit.ac.jp/uni_index/principle/campus/)：美術工芸資料館、KIT HOUSE、虹の塔、プラザKITの外観写真。
- [大学の教育研究施設紹介](https://www.kit.ac.jp/wp/wp-content/uploads/2025/11/sisetsusyoukai_leaflet.pdf)：2025年7月31日施設環境安全課資料。耐震補強、和楽庵、KIT HOUSEのガラス面とテラス。元PDFを観察用に保存。
- [1号館の写真](https://commons.wikimedia.org/wiki/File:Kyoto_Institute_of_Technology140524NI3.JPG)：Atelier Verde、2014年5月24日、[CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)。赤褐色タイル、突出した階段室、開放的な入口、横長窓を参考にした。写真はモデルへ貼り付けていない。
- [木村博昭＋ケイズアーキテクツ・60周年記念館](https://www.ks-architects.com/ja/works/p.php?id=89)：白い上階外装、下階のガラス、屋根、縦の突出部。モデルの複雑な曲面と内装は簡略化されている。
- [図書館自身による2025年の紹介](https://www.libraryfair.jp/poster/2025/230)：3階構成、改修後のガラス張り入口、茶色の外壁。
- [大学・センターホール改修報告](https://www.kit.ac.jp/2025/08/news0805/)：2025年に改修。模型の屋根・立面はまだ追加照合が必要。
- [岸和郎＋K.ASSOCIATES・KIT HOUSE](https://k-associates.com/works/kit-house/)：4つの切妻屋根、東向きの屋根採光、透かし積みの外壁、ガラス張りの下階、外階段・テラスを参考に個別形状を作成。
- [大学公式オープンキャンパス案内](https://www.kit.ac.jp/ouw-index/)から紹介される[学生制作3Dマップ](https://kitmap.jp)：公開写真でセンターホールの段状の外観、東1号館の5階構成、15号館の確認できる部分の3階構成を照合。東2号館と14号館は隣接棟から推定した階数。公開GLBは調査用に保存したが、本モデルにそのメッシュを取り込んでいない。
- 虹の塔は公式散策写真の縦方向の色変化と横長パネルを反映。記念館との位置関係は設計者の外観写真に基づく概略配置。

設計事務所・大学の写真の権利は各権利者に帰属する。ダウンロードした資料はこの作業での観察用で、自由利用の写真集としての配布を意図しない。

## 材質と手法

- [Poly Haven Asphalt 01](https://polyhaven.com/a/asphalt_01)、[Kloofendal Overcast Pure Sky](https://polyhaven.com/a/kloofendal_overcast_puresky)：CC0。Blenderに格納。
- [fSpyのカメラ推定の原理](https://fspy.io/basics/)：3号館のv2カメラ推定の参考。fSpyアプリそのものを使用したわけではない。
- 連続窓は実開口、ガラス、共通枠をそれぞれメッシュとして作成。全体の一般校舎も壁を窓周囲で分割し、ガラスの手前を壁が塞がない形状にした。
- 校舎のメッシュを棟単位にまとめ、同じ樹木形状を共有し、全体でも編集できる構成にしている。
