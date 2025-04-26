from flask import Flask, jsonify
import sqlite3
import csv

app = Flask(__name__)

@app.route("/vindict/<name>")
def vindictive_wizards(name):
    wizards = []
    with open("you_know.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            wizards.append(row)

    target_wizard = None
    for wizard in wizards:
        if wizard["name"] == name:
            target_wizard = wizard
            break

    if not target_wizard:
        return jsonify({"error": "Wizard not found"}), 404

    # Вычисление могущества целевого волшебника
    conn = sqlite3.connect("info.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.power
        FROM Education e
        JOIN Universities u ON e.univer_id = u.id
        WHERE u.university = ? AND e.id = ?
    """, (target_wizard["university"], target_wizard["level_id"]))
    target_power = cursor.fetchone()
    target_power = target_power[0] if target_power else 0


    more_powerful_wizards = []
    for wizard in wizards:
        if wizard["name"] == name:
            continue
        cursor.execute("""
            SELECT e.power
            FROM Education e
            JOIN Universities u ON e.univer_id = u.id
            WHERE u.university = ? AND e.id = ?
        """, (wizard["university"], wizard["level_id"]))
        wizard_power = cursor.fetchone()
        wizard_power = wizard_power[0] if wizard_power else 0
        if wizard_power > target_power:
            more_powerful_wizards.append((wizard["name"], int(wizard["vindictiveness"]), wizard_power))

    conn.close()

    more_powerful_wizards.sort(key=lambda x: (-x[1], -x[2], x[0]))

    return jsonify([wizard[0] for wizard in more_powerful_wizards])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
