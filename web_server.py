from flask import Flask, render_template_string
from database import fetch_data
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>SC2 Map Score</title>
            <style>
                body { font-family: Arial, sans-serif; background-color: black; color: white; }
                #score { font-size: 24px; text-align: center; margin-top: 20px; }
            </style>
            <script>
                function updateScore() {
                    fetch('/get_score')
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById('score').innerHTML = `${data.opponent}: ${data.wins} - ${data.losses}`;
                        });
                    setTimeout(updateScore, 5000);  // Update every 5 seconds
                }
                window.onload = updateScore;
            </script>
        </head>
        <body>
            <div id="score">Waiting for game...</div>
        </body>
        </html>
    ''')

@app.route('/get_score')
def get_score():
    query = "SELECT opponent_name, SUM(wins) as wins, SUM(losses) as losses FROM matches GROUP BY opponent_name ORDER BY rowid DESC LIMIT 1"
    result = fetch_data(query)
    if result and len(result) > 0:
        opponent, wins, losses = result[0]
        return json.dumps({'opponent': opponent, 'wins': wins or 0, 'losses': losses or 0})
    return json.dumps({'opponent': 'Unknown', 'wins': 0, 'losses': 0})

def run_server():
    app.run(host='localhost', port=5000)

if __name__ == '__main__':
    run_server()