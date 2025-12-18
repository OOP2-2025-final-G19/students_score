from flask import Flask, render_template
from models import initialize_database, Score, Subject
from routes import blueprints
from collections import defaultdict

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# ホームページのルート
@app.route('/')
def index():
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

    labels = [f"{i}–{i+9}" for i in range(0, 100, 10)]

    return render_template(
        'index.html',
        labels=labels,
        histograms=histograms
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
