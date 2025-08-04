from flask import Flask, render_template, request
from matcher_engine import ItemMatcher

app = Flask(__name__)

matcher = ItemMatcher(
    excel_path="SAPITEMCODEPYTHON.xlsx",
    cache_path="embeddings_cache.pkl",
    log_path="learning_log.pkl"
)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = ""
    feedback = ""
    if request.method == "POST":
        query = request.form["description"]
        results = matcher.search(query, top_k=5, min_score_threshold=0.3)
        feedback = request.form.get("feedback")
        if feedback:
            matcher.log_search_feedback(query, results, feedback)
    return render_template("index.html", query=query, results=results)

if __name__ == "__main__":
    app.run(debug=True)
