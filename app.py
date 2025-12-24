from flask import Flask, render_template
from models import initialize_database, Score, Subject
from routes import blueprints
from collections import defaultdict
from peewee import fn

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# ホームページのルート
@app.route('/')
def index():
    # 成績分布（ヒストグラム）用データ
    histograms = {}
    for subject in Subject.select():
        bins = defaultdict(int)

        for s in Score.select().where(Score.subject == subject):
            bucket = (s.value // 10) * 10
            if bucket >= 100:
                bucket = 90
            bins[bucket] += 1

        # 0,10,20,...,90 の順に並べる
        histograms[subject.name] = [bins[i] for i in range(0, 100, 10)]

    # ヒストグラム用のラベル
    labels = [f"{i}–{i+9}" for i in range(0, 100, 10)]

    # 平均点 推移折れ線グラフ用データ（科目ごと）
    linegraphs = {}
    for subject in Subject.select():
        monthly_totals = defaultdict(int)
        monthly_counts = defaultdict(int)

        for s in Score.select().where(Score.subject == subject):
            monthly_totals[s.month] += s.value
            monthly_counts[s.month] += 1

        average_scores = []
        for month in range(1, 13):
            if monthly_counts[month] > 0:
                average = monthly_totals[month] / monthly_counts[month]
            else:
                average = 0
            average_scores.append(average)

        # 各科目ごとに「ラベルと値」のセットを持たせる
        linegraphs[subject.name] = {
            "labels": [f"{m}月" for m in range(1, 13)],
            "values": average_scores,
        }

    return render_template(
        'index.html',
        labels=labels,
        histograms=histograms,
        linegraphs=linegraphs,
    )

@app.route('/partials/linegraph')
def linegraph():
    # index() と同じ形式の linegraphs を返すAPI的なルート（必要なら利用）
    linegraphs = {}
    for subject in Subject.select():
        monthly_totals = defaultdict(int)
        monthly_counts = defaultdict(int)

        for s in Score.select().where(Score.subject == subject):
            monthly_totals[s.month] += s.value
            monthly_counts[s.month] += 1

        average_scores = []
        for month in range(1, 13):
            if monthly_counts[month] > 0:
                average = monthly_totals[month] / monthly_counts[month]
            else:
                average = 0
            average_scores.append(average)

        linegraphs[subject.name] = {
            "labels": [f"{m}月" for m in range(1, 13)],
            "values": average_scores,
        }

    return render_template(
        'index.html',
        labels=[],
        histograms={},
        linegraphs=linegraphs,
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
