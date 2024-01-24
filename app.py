from flask import Flask, request, jsonify
import marketscraper 

app = Flask(__name__)

@app.route('/api/solve_knapsack', methods=['POST'])
def solve_knapsack():
    data = request.json
    budget = data['budget']
    categories = data['categories']
    results = your_knapsack_script.process(budget, categories)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
