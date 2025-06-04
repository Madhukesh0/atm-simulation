from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS  # <-- Add this line

app = Flask(__name__)
CORS(app) 

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Use your MySQL root password here
    database="atm_db"
)
cursor = db.cursor()




@app.route('/login', methods=['POST'])
def login():
    data = request.json
    account_number = data['account_number']
    pin = data['pin']
    
    cursor.execute("""
        SELECT a.account_id, a.balance, u.pin 
        FROM accounts a
        JOIN users u ON a.user_id = u.user_id
        WHERE a.account_number = %s
    """, (account_number,))
    
    account = cursor.fetchone()
    
    if account and account[2] == pin:  # Check PIN
        return jsonify({
            "status": "success", 
            "account_id": account[0],
            "balance": float(account[1])
        })
    else:
        return jsonify({"status": "failed"})

@app.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.json
    account_id = data['account_id']
    amount = data['amount']
    
    cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
    balance = cursor.fetchone()[0]
    
    if balance >= amount:
        new_balance = balance - amount
        # Update account balance
        cursor.execute("UPDATE accounts SET balance = %s WHERE account_id = %s", (new_balance, account_id))
        # Record transaction
        cursor.execute("""
            INSERT INTO transactions (account_id, type, amount)
            VALUES (%s, 'WITHDRAW', %s)
        """, (account_id, amount))
        db.commit()
        return jsonify({
            "status": "success", 
            "new_balance": float(new_balance)
        })
    else:
        return jsonify({
            "status": "failed", 
            "message": "Insufficient funds"
        })

@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.json
    account_id = data['account_id']
    amount = data['amount']
    
    cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
    balance = cursor.fetchone()[0]
    
    new_balance = balance + amount
    # Update account balance
    cursor.execute("UPDATE accounts SET balance = %s WHERE account_id = %s", (new_balance, account_id))
    # Record transaction
    cursor.execute("""
        INSERT INTO transactions (account_id, type, amount)
        VALUES (%s, 'DEPOSIT', %s)
    """, (account_id, amount))
    db.commit()
    return jsonify({
        "status": "success", 
        "new_balance": float(new_balance)
    })

@app.route('/balance', methods=['POST'])
def balance():
    data = request.json
    account_id = data['account_id']
    
    cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
    balance = cursor.fetchone()[0]
    
    return jsonify({
        "status": "success", 
        "balance": float(balance)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
