import psycopg2
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
# --- Database Connection ---
DB_NAME = "ngo_db"
DB_USER = "postgres"
DB_PASS = "YOUR_DB_PASSWORD" # Get password from environment variable or set it here
DB_HOST = "localhost"
DB_PORT = "5432"

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        # This function now correctly uses the variables defined above.
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Could not connect to the database: {e}")
        return None

# --------------------------------------------------- API Endpoints for Donors -------------------------------------------------
# --------------------------------------------------- API Endpoints for Donors -------------------------------------------------
# --------------------------------------------------- API Endpoints for Donors -------------------------------------------------
# --------------------------------------------------- API Endpoints for Donors -------------------------------------------------

# CREATE a new donor
@app.route('/donors', methods=['POST'])
def add_donor():
    data = request.get_json()
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO Donors (donor_name, donor_type, email, phone_number, address) VALUES (%s, %s, %s, %s, %s) RETURNING donor_id;',
        (data['donor_name'], data['donor_type'], data['email'], data['phone_number'], data['address'])
    )
    new_donor_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": "Donor added successfully!", "donor_id": new_donor_id}), 201

# READ all donors
@app.route('/donors', methods=['GET'])
def get_all_donors():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
        
    cur = conn.cursor()
    cur.execute('SELECT donor_id, donor_name, email FROM Donors ORDER BY donor_name;')
    donors = cur.fetchall()
    cur.close()
    conn.close()
    
    donor_list = [{"donor_id": row[0], "donor_name": row[1], "email": row[2]} for row in donors]
    return jsonify(donor_list), 200

# READ a single donor by ID
@app.route('/donors/<int:donor_id>', methods=['GET'])
def get_donor(donor_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute('SELECT * FROM Donors WHERE donor_id = %s;', (donor_id,))
    donor = cur.fetchone()
    cur.close()
    conn.close()

    if donor:
        donor_data = {
            "donor_id": donor[0],
            "donor_name": donor[1],
            "donor_type": donor[2],
            "email": donor[3],
            "phone_number": donor[4],
            "address": donor[5],
            "registration_date": donor[6].strftime('%Y-%m-%d')
        }
        return jsonify(donor_data), 200
    else:
        return jsonify({"message": "Donor not found"}), 404

# UPDATE a donor's information
@app.route('/donors/<int:donor_id>', methods=['PUT'])
def update_donor(donor_id):
    data = request.get_json()
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute(
        'UPDATE Donors SET donor_name = %s, donor_type = %s, email = %s, phone_number = %s, address = %s WHERE donor_id = %s;',
        (data['donor_name'], data['donor_type'], data['email'], data['phone_number'], data['address'], donor_id)
    )
    conn.commit()
    
    updated_rows = cur.rowcount
    cur.close()
    conn.close()
    
    if updated_rows > 0:
        return jsonify({"message": f"Donor {donor_id} updated successfully!"}), 200
    else:
        return jsonify({"message": "Donor not found"}), 404

# DELETE a donor
@app.route('/donors/<int:donor_id>', methods=['DELETE'])
def delete_donor(donor_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute('DELETE FROM Donors WHERE donor_id = %s;', (donor_id,))
    conn.commit()
    
    deleted_rows = cur.rowcount
    cur.close()
    conn.close()
    
    if deleted_rows > 0:
        return jsonify({"message": f"Donor {donor_id} deleted successfully."}), 200
    else:
        return jsonify({"message": "Donor not found"}), 404

# Main entry point to run the app
if __name__ == '__main__':
    app.run(debug=True)
# ------------------------------------------------------ API Endpoints for Campaigns -----------------------------------------------------------
# ------------------------------------------------------ API Endpoints for Campaigns -----------------------------------------------------------
# ------------------------------------------------------ API Endpoints for Campaigns -----------------------------------------------------------
# ------------------------------------------------------ API Endpoints for Campaigns -----------------------------------------------------------
# CREATE a new campaign
@app.route('/campaigns', methods=['POST'])
def add_campaign():
    data = request.get_json()
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO Campaigns (campaign_name, description, start_date, end_date, goal_amount, status) VALUES (%s, %s, %s, %s, %s, %s) RETURNING campaign_id;',
        (data['campaign_name'], data['description'], data['start_date'], data['end_date'], data['goal_amount'], data['status'])
    )
    new_campaign_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": "Campaign added successfully!", "campaign_id": new_campaign_id}), 201

# READ all campaigns
@app.route('/campaigns', methods=['GET'])
def get_all_campaigns():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
        
    cur = conn.cursor()
    cur.execute('SELECT campaign_id, campaign_name, status, goal_amount FROM Campaigns ORDER BY start_date DESC;')
    campaigns = cur.fetchall()
    cur.close()
    conn.close()
    
    campaign_list = [{"campaign_id": row[0], "campaign_name": row[1], "status": row[2], "goal_amount": float(row[3])} for row in campaigns]
    return jsonify(campaign_list), 200

# READ a single campaign by ID
@app.route('/campaigns/<int:campaign_id>', methods=['GET'])
def get_campaign(campaign_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute('SELECT * FROM Campaigns WHERE campaign_id = %s;', (campaign_id,))
    campaign = cur.fetchone()
    cur.close()
    conn.close()

    if campaign:
        campaign_data = {
            "campaign_id": campaign[0],
            "campaign_name": campaign[1],
            "description": campaign[2],
            "start_date": campaign[3].strftime('%Y-%m-%d') if campaign[3] else None,
            "end_date": campaign[4].strftime('%Y-%m-%d') if campaign[4] else None,
            "goal_amount": float(campaign[5]) if campaign[5] else None,
            "status": campaign[6]
        }
        return jsonify(campaign_data), 200
    else:
        return jsonify({"message": "Campaign not found"}), 404

# UPDATE a campaign's information
@app.route('/campaigns/<int:campaign_id>', methods=['PUT'])
def update_campaign(campaign_id):
    data = request.get_json()
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute(
        'UPDATE Campaigns SET campaign_name = %s, description = %s, start_date = %s, end_date = %s, goal_amount = %s, status = %s WHERE campaign_id = %s;',
        (data['campaign_name'], data['description'], data['start_date'], data['end_date'], data['goal_amount'], data['status'], campaign_id)
    )
    conn.commit()
    
    updated_rows = cur.rowcount
    cur.close()
    conn.close()
    
    if updated_rows > 0:
        return jsonify({"message": f"Campaign {campaign_id} updated successfully!"}), 200
    else:
        return jsonify({"message": "Campaign not found"}), 404

# DELETE a campaign
@app.route('/campaigns/<int:campaign_id>', methods=['DELETE'])
def delete_campaign(campaign_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute('DELETE FROM Campaigns WHERE campaign_id = %s;', (campaign_id,))
    conn.commit()
    
    deleted_rows = cur.rowcount
    cur.close()
    conn.close()
    
    if deleted_rows > 0:
        return jsonify({"message": f"Campaign {campaign_id} deleted successfully."}), 200
    else:
        return jsonify({"message": "Campaign not found"}), 404
    

# -------------------------------------------------- API Endpoints for Volunteers ------------------------------------------------
# -------------------------------------------------- API Endpoints for Volunteers ------------------------------------------------
# -------------------------------------------------- API Endpoints for Volunteers ------------------------------------------------
# -------------------------------------------------- API Endpoints for Volunteers ------------------------------------------------

# CREATE a new volunteer
@app.route('/volunteers', methods=['POST'])
def add_volunteer():
    data = request.get_json()
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO Volunteers (volunteer_name, email, phone_number, skills) VALUES (%s, %s, %s, %s) RETURNING volunteer_id;',
        (data['volunteer_name'], data['email'], data['phone_number'], data['skills'])
    )
    new_volunteer_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": "Volunteer added successfully!", "volunteer_id": new_volunteer_id}), 201

# READ all volunteers
@app.route('/volunteers', methods=['GET'])
def get_all_volunteers():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
        
    cur = conn.cursor()
    cur.execute('SELECT volunteer_id, volunteer_name, email, skills FROM Volunteers ORDER BY volunteer_name;')
    volunteers = cur.fetchall()
    cur.close()
    conn.close()
    
    volunteer_list = [{"volunteer_id": row[0], "volunteer_name": row[1], "email": row[2], "skills": row[3]} for row in volunteers]
    return jsonify(volunteer_list), 200

# READ a single volunteer by ID
@app.route('/volunteers/<int:volunteer_id>', methods=['GET'])
def get_volunteer(volunteer_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute('SELECT * FROM Volunteers WHERE volunteer_id = %s;', (volunteer_id,))
    volunteer = cur.fetchone()
    cur.close()
    conn.close()

    if volunteer:
        volunteer_data = {
            "volunteer_id": volunteer[0],
            "volunteer_name": volunteer[1],
            "email": volunteer[2],
            "phone_number": volunteer[3],
            "skills": volunteer[4],
            "join_date": volunteer[5].strftime('%Y-%m-%d') if volunteer[5] else None,
            "user_id": volunteer[6]
        }
        return jsonify(volunteer_data), 200
    else:
        return jsonify({"message": "Volunteer not found"}), 404

# UPDATE a volunteer's information
@app.route('/volunteers/<int:volunteer_id>', methods=['PUT'])
def update_volunteer(volunteer_id):
    data = request.get_json()
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute(
        'UPDATE Volunteers SET volunteer_name = %s, email = %s, phone_number = %s, skills = %s WHERE volunteer_id = %s;',
        (data['volunteer_name'], data['email'], data['phone_number'], data['skills'], volunteer_id)
    )
    conn.commit()
    
    updated_rows = cur.rowcount
    cur.close()
    conn.close()
    
    if updated_rows > 0:
        return jsonify({"message": f"Volunteer {volunteer_id} updated successfully!"}), 200
    else:
        return jsonify({"message": "Volunteer not found"}), 404

# DELETE a volunteer
@app.route('/volunteers/<int:volunteer_id>', methods=['DELETE'])
def delete_volunteer(volunteer_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute('DELETE FROM Volunteers WHERE volunteer_id = %s;', (volunteer_id,))
    conn.commit()
    
    deleted_rows = cur.rowcount
    cur.close()
    conn.close()
    
    if deleted_rows > 0:
        return jsonify({"message": f"Volunteer {volunteer_id} deleted successfully."}), 200
    else:
        return jsonify({"message": "Volunteer not found"}), 404
    

# -------------------------------------------------------- API Endpoints for Donations -------------------------------
# -------------------------------------------------------- API Endpoints for Donations -------------------------------
# -------------------------------------------------------- API Endpoints for Donations -------------------------------
# -------------------------------------------------------- API Endpoints for Donations -------------------------------

# CREATE a new donation
@app.route('/donations', methods=['POST'])
def add_donation():
    data = request.get_json()
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO Donations (donor_id, campaign_id, donation_date, donation_type, cash_amount, notes) VALUES (%s, %s, %s, %s, %s, %s) RETURNING donation_id;',
        (data['donor_id'], data['campaign_id'], data['donation_date'], data['donation_type'], data['cash_amount'], data['notes'])
    )
    new_donation_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": "Donation recorded successfully!", "donation_id": new_donation_id}), 201

# READ all donations
@app.route('/donations', methods=['GET'])
def get_all_donations():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
        
    cur = conn.cursor()
    # This query JOINS tables to get the actual names, not just IDs
    cur.execute('''
        SELECT d.donation_id, dn.donor_name, c.campaign_name, d.donation_date, d.donation_type, d.cash_amount
        FROM Donations d
        JOIN Donors dn ON d.donor_id = dn.donor_id
        JOIN Campaigns c ON d.campaign_id = c.campaign_id
        ORDER BY d.donation_date DESC;
    ''')
    donations = cur.fetchall()
    cur.close()
    conn.close()
    
    donation_list = []
    for row in donations:
        donation_list.append({
            "donation_id": row[0],
            "donor_name": row[1],
            "campaign_name": row[2],
            "donation_date": row[3].strftime('%Y-%m-%d'),
            "donation_type": row[4],
            "cash_amount": float(row[5]) if row[5] else None
        })
    return jsonify(donation_list), 200

# READ all donations for a specific campaign
@app.route('/campaigns/<int:campaign_id>/donations', methods=['GET'])
def get_donations_for_campaign(campaign_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
        
    cur = conn.cursor()
    cur.execute(
        'SELECT d.donation_id, dn.donor_name, d.donation_date, d.cash_amount FROM Donations d JOIN Donors dn ON d.donor_id = dn.donor_id WHERE d.campaign_id = %s ORDER BY d.donation_date DESC;', 
        (campaign_id,)
    )
    donations = cur.fetchall()
    cur.close()
    conn.close()
    
    donation_list = []
    for row in donations:
        donation_list.append({
            "donation_id": row[0],
            "donor_name": row[1],
            "donation_date": row[2].strftime('%Y-%m-%d'),
            "cash_amount": float(row[3]) if row[3] else None
        })
    return jsonify(donation_list), 200

# ------------------------------------------------------ API Endpoints for Donation Items -------------------------------------------
# ------------------------------------------------------ API Endpoints for Donation Items -------------------------------------------
# ------------------------------------------------------ API Endpoints for Donation Items -------------------------------------------
# ------------------------------------------------------ API Endpoints for Donation Items -------------------------------------------

# CREATE (Add) an item to a specific donation
@app.route('/donations/<int:donation_id>/items', methods=['POST'])
def add_donation_item(donation_id):
    data = request.get_json()
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO Donation_Items (donation_id, item_name, item_category, quantity, unit) VALUES (%s, %s, %s, %s, %s) RETURNING item_id;',
        (donation_id, data['item_name'], data['item_category'], data['quantity'], data['unit'])
    )
    new_item_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": "Item added to donation successfully!", "item_id": new_item_id}), 201

# READ all items for a specific donation
@app.route('/donations/<int:donation_id>/items', methods=['GET'])
def get_items_for_donation(donation_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
        
    cur = conn.cursor()
    cur.execute('SELECT item_id, item_name, item_category, quantity, unit FROM Donation_Items WHERE donation_id = %s;', (donation_id,))
    items = cur.fetchall()
    cur.close()
    conn.close()
    
    item_list = []
    for row in items:
        item_list.append({
            "item_id": row[0],
            "item_name": row[1],
            "item_category": row[2],
            "quantity": row[3],
            "unit": row[4]
        })
    return jsonify(item_list), 200

# ------------------------------------------ API Endpoints for Users (Registration & Login) --------------------------------------
# ------------------------------------------ API Endpoints for Users (Registration & Login) --------------------------------------
# ------------------------------------------ API Endpoints for Users (Registration & Login) --------------------------------------
# ------------------------------------------ API Endpoints for Users (Registration & Login) --------------------------------------

# CREATE (Register) a new user
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    email = data['email']
    password = data['password']
    role = data['role'] # 'Donor', 'Volunteer', 'Worker', 'Owner'

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(
            'INSERT INTO Users (email, password_hash, role) VALUES (%s, %s, %s) RETURNING user_id;',
            (email, hashed_password, role)
        )
        new_user_id = cur.fetchone()[0]
        conn.commit()
    except psycopg2.IntegrityError: # This catches duplicate emails
        conn.rollback()
        return jsonify({"message": "Error: Email already registered."}), 409
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "User registered successfully!", "user_id": new_user_id}), 201

# LOGIN a user
@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data['email']
    password_candidate = data['password'] # The password the user typed in

    conn = get_db_connection()
    cur = conn.cursor()
    
    # First, find the user by email
    cur.execute('SELECT user_id, password_hash, role FROM Users WHERE email = %s;', (email,))
    user = cur.fetchone()
    
    cur.close()
    conn.close()

    if user:
        # User was found. Now check the password.
        password_hash_from_db = user[1]
        if bcrypt.check_password_hash(password_hash_from_db, password_candidate):
            # Password is correct!
            return jsonify({
                "message": "Login successful!",
                "user_id": user[0],
                "role": user[2]
            }), 200
        else:
            # Password was incorrect
            return jsonify({"message": "Invalid email or password."}), 401
    else:
        # No user found with that email
        return jsonify({"message": "Invalid email or password."}), 401
    

# --------------------------------------------- API Endpoints for Beneficiaries ---
# --------------------------------------------- API Endpoints for Beneficiaries ---
# --------------------------------------------- API Endpoints for Beneficiaries ---
# --------------------------------------------- API Endpoints for Beneficiaries ---

# CREATE a new beneficiary
@app.route('/beneficiaries', methods=['POST'])
def add_beneficiary():
    data = request.get_json()
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO Beneficiaries (beneficiary_name, beneficiary_type, contact_info, description) VALUES (%s, %s, %s, %s) RETURNING beneficiary_id;',
        (data['beneficiary_name'], data['beneficiary_type'], data['contact_info'], data['description'])
    )
    new_beneficiary_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": "Beneficiary added successfully!", "beneficiary_id": new_beneficiary_id}), 201

# READ all beneficiaries
@app.route('/beneficiaries', methods=['GET'])
def get_all_beneficiaries():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
        
    cur = conn.cursor()
    cur.execute('SELECT beneficiary_id, beneficiary_name, beneficiary_type, contact_info FROM Beneficiaries ORDER BY beneficiary_name;')
    beneficiaries = cur.fetchall()
    cur.close()
    conn.close()
    
    beneficiary_list = []
    for row in beneficiaries:
        beneficiary_list.append({
            "beneficiary_id": row[0],
            "beneficiary_name": row[1],
            "beneficiary_type": row[2],
            "contact_info": row[3]
        })
    return jsonify(beneficiary_list), 200

# READ a single beneficiary by ID
@app.route('/beneficiaries/<int:beneficiary_id>', methods=['GET'])
def get_beneficiary(beneficiary_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute('SELECT * FROM Beneficiaries WHERE beneficiary_id = %s;', (beneficiary_id,))
    beneficiary = cur.fetchone()
    cur.close()
    conn.close()

    if beneficiary:
        beneficiary_data = {
            "beneficiary_id": beneficiary[0],
            "beneficiary_name": beneficiary[1],
            "beneficiary_type": beneficiary[2],
            "contact_info": beneficiary[3],
            "description": beneficiary[4]
        }
        return jsonify(beneficiary_data), 200
    else:
        return jsonify({"message": "Beneficiary not found"}), 404

# ------------------------------------------------ API Endpoints for Distributions --------------------------
# ------------------------------------------------ API Endpoints for Distributions --------------------------
# ------------------------------------------------ API Endpoints for Distributions --------------------------
# ------------------------------------------------ API Endpoints for Distributions --------------------------

# CREATE a new distribution record
@app.route('/distributions', methods=['POST'])
def add_distribution():
    data = request.get_json()
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO Distributions (beneficiary_id, item_name, quantity_distributed, distribution_date) VALUES (%s, %s, %s, %s) RETURNING distribution_id;',
        (data['beneficiary_id'], data['item_name'], data['quantity_distributed'], data['distribution_date'])
    )
    new_distribution_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": "Distribution recorded successfully!", "distribution_id": new_distribution_id}), 201

# READ all distributions for a specific beneficiary
@app.route('/beneficiaries/<int:beneficiary_id>/distributions', methods=['GET'])
def get_distributions_for_beneficiary(beneficiary_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
        
    cur = conn.cursor()
    cur.execute(
        'SELECT distribution_id, item_name, quantity_distributed, distribution_date FROM Distributions WHERE beneficiary_id = %s ORDER BY distribution_date DESC;',
        (beneficiary_id,)
    )
    distributions = cur.fetchall()
    cur.close()
    conn.close()
    
    distribution_list = []
    for row in distributions:
        distribution_list.append({
            "distribution_id": row[0],
            "item_name": row[1],
            "quantity_distributed": row[2],
            "distribution_date": row[3].strftime('%Y-%m-%d')
        })
    return jsonify(distribution_list), 200

# ------------------------------------------------- API Endpoints for Expenses ----------------------------------
# ------------------------------------------------- API Endpoints for Expenses ----------------------------------
# ------------------------------------------------- API Endpoints for Expenses ----------------------------------
# ------------------------------------------------- API Endpoints for Expenses ----------------------------------

# CREATE a new expense record
@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.get_json()
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO Expenses (campaign_id, expense_category, description, amount, expense_date, receipt_url) VALUES (%s, %s, %s, %s, %s, %s) RETURNING expense_id;',
        (data.get('campaign_id'), data['expense_category'], data['description'], data['amount'], data['expense_date'], data.get('receipt_url'))
    )
    new_expense_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": "Expense recorded successfully!", "expense_id": new_expense_id}), 201

# READ all expenses
@app.route('/expenses', methods=['GET'])
def get_all_expenses():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
        
    cur = conn.cursor()
    # This query JOINS with Campaigns to show which campaign the expense was for
    cur.execute('''
        SELECT e.expense_id, c.campaign_name, e.expense_category, e.description, e.amount, e.expense_date
        FROM Expenses e
        LEFT JOIN Campaigns c ON e.campaign_id = c.campaign_id
        ORDER BY e.expense_date DESC;
    ''')
    expenses = cur.fetchall()
    cur.close()
    conn.close()
    
    expense_list = []
    for row in expenses:
        expense_list.append({
            "expense_id": row[0],
            "campaign_name": row[1] if row[1] else "General Expense",
            "expense_category": row[2],
            "description": row[3],
            "amount": float(row[4]),
            "expense_date": row[5].strftime('%Y-%m-%d')
        })
    return jsonify(expense_list), 200

# ---------------------------------------------------- API Endpoints for Events ---
# ---------------------------------------------------- API Endpoints for Events ---
# ---------------------------------------------------- API Endpoints for Events ---
# ---------------------------------------------------- API Endpoints for Events ---

# CREATE a new event
@app.route('/events', methods=['POST'])
def add_event():
    data = request.get_json()
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO Events (event_name, description, location, event_date) VALUES (%s, %s, %s, %s) RETURNING event_id;',
        (data['event_name'], data['description'], data['location'], data['event_date'])
    )
    new_event_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": "Event created successfully!", "event_id": new_event_id}), 201

# READ all events
@app.route('/events', methods=['GET'])
def get_all_events():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
        
    cur = conn.cursor()
    cur.execute('SELECT event_id, event_name, location, event_date FROM Events ORDER BY event_date DESC;')
    events = cur.fetchall()
    cur.close()
    conn.close()
    
    event_list = []
    for row in events:
        event_list.append({
            "event_id": row[0],
            "event_name": row[1],
            "location": row[2],
            "event_date": row[3].strftime('%Y-%m-%d %H:%M:%S') if row[3] else None
        })
    return jsonify(event_list), 200

# --- --------------------------------------------------API Endpoints for Tasks ---
# --- --------------------------------------------------API Endpoints for Tasks ---
# --- --------------------------------------------------API Endpoints for Tasks ---
# --- --------------------------------------------------API Endpoints for Tasks ---

# CREATE a new task for a specific event
@app.route('/events/<int:event_id>/tasks', methods=['POST'])
def add_task(event_id):
    data = request.get_json()
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO Tasks (event_id, task_name, description, status) VALUES (%s, %s, %s, %s) RETURNING task_id;',
        (event_id, data['task_name'], data['description'], data.get('status', 'To Do')) # 'To Do' is a default value
    )
    new_task_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": "Task created successfully!", "task_id": new_task_id}), 201

# READ all tasks for a specific event
@app.route('/events/<int:event_id>/tasks', methods=['GET'])
def get_tasks_for_event(event_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
        
    cur = conn.cursor()
    cur.execute('SELECT task_id, task_name, description, status FROM Tasks WHERE event_id = %s ORDER BY task_id;', (event_id,))
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    
    task_list = []
    for row in tasks:
        task_list.append({
            "task_id": row[0],
            "task_name": row[1],
            "description": row[2],
            "status": row[3]
        })
    return jsonify(task_list), 200

# ---------------------------------------------- API Endpoints for Volunteer Assignments ---
# ---------------------------------------------- API Endpoints for Volunteer Assignments ---
# ---------------------------------------------- API Endpoints for Volunteer Assignments ---
# ---------------------------------------------- API Endpoints for Volunteer Assignments ---

# CREATE a new volunteer assignment (assign a volunteer to a task)
@app.route('/assignments', methods=['POST'])
def add_volunteer_assignment():
    data = request.get_json()
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    cur = conn.cursor()
    try:
        cur.execute(
            'INSERT INTO Volunteer_Assignments (volunteer_id, task_id, assignment_date, notes) VALUES (%s, %s, %s, %s) RETURNING assignment_id;',
            (data['volunteer_id'], data['task_id'], data.get('assignment_date'), data.get('notes'))
        )
        new_assignment_id = cur.fetchone()[0]
        conn.commit()
    except psycopg2.IntegrityError as e:
        conn.rollback()
        # This will catch if volunteer_id or task_id does not exist
        return jsonify({"message": f"Error creating assignment: {e.diag.message_detail}"}), 400
    finally:
        cur.close()
        conn.close()
    
    return jsonify({"message": "Volunteer assigned to task successfully!", "assignment_id": new_assignment_id}), 201

# READ all assignments for a specific volunteer
@app.route('/volunteers/<int:volunteer_id>/assignments', methods=['GET'])
def get_assignments_for_volunteer(volunteer_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
        
    cur = conn.cursor()
    cur.execute('''
        SELECT va.assignment_id, t.task_name, e.event_name, va.assignment_date, va.notes
        FROM Volunteer_Assignments va
        JOIN Tasks t ON va.task_id = t.task_id
        JOIN Events e ON t.event_id = e.event_id
        WHERE va.volunteer_id = %s
        ORDER BY va.assignment_date DESC;
    ''', (volunteer_id,))
    assignments = cur.fetchall()
    cur.close()
    conn.close()
    
    assignment_list = []
    for row in assignments:
        assignment_list.append({
            "assignment_id": row[0],
            "task_name": row[1],
            "event_name": row[2],
            "assignment_date": row[3].strftime('%Y-%m-%d') if row[3] else None,
            "notes": row[4]
        })
    return jsonify(assignment_list), 200

# READ all volunteers assigned to a specific task
@app.route('/tasks/<int:task_id>/volunteers', methods=['GET'])
def get_volunteers_for_task(task_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
        
    cur = conn.cursor()
    cur.execute('''
        SELECT va.assignment_id, v.volunteer_name, v.email, va.assignment_date, va.notes
        FROM Volunteer_Assignments va
        JOIN Volunteers v ON va.volunteer_id = v.volunteer_id
        WHERE va.task_id = %s
        ORDER BY v.volunteer_name;
    ''', (task_id,))
    volunteers = cur.fetchall()
    cur.close()
    conn.close()
    
    volunteer_list = []
    for row in volunteers:
        volunteer_list.append({
            "assignment_id": row[0],
            "volunteer_name": row[1],
            "email": row[2],
            "assignment_date": row[3].strftime('%Y-%m-%d') if row[3] else None,
            "notes": row[4]
        })
    return jsonify(volunteer_list), 200

# ------------------------------------------------ API Endpoints for Public Stats ---
# ------------------------------------------------ API Endpoints for Public Stats ---
# ------------------------------------------------ API Endpoints for Public Stats ---
# ------------------------------------------------ API Endpoints for Public Stats ---

@app.route('/api/public-stats', methods=['GET'])
def get_public_stats():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
        
    cur = conn.cursor()
    
    # 1. Get Total Donations Raised
    cur.execute('SELECT SUM(cash_amount) FROM Donations;')
    total_raised = cur.fetchone()[0] or 0 # Use 'or 0' in case the table is empty

    # 2. Get Total Volunteers
    cur.execute('SELECT COUNT(*) FROM Volunteers;')
    total_volunteers = cur.fetchone()[0] or 0
    
    # 3. Get Active Campaigns
    cur.execute("SELECT COUNT(*) FROM Campaigns WHERE status = 'Active';")
    active_campaigns = cur.fetchone()[0] or 0
    
    cur.close()
    conn.close()
    
    # Return all stats in a single JSON object
    return jsonify({
        "total_raised": float(total_raised),
        "total_volunteers": total_volunteers,
        "active_campaigns": active_campaigns
    }), 200

# ------------------------ API Endpoints for Admin Management ---
# ------------------------ API Endpoints for Admin Management ---
# ------------------------ API Endpoints for Admin Management ---
# ------------------------ API Endpoints for Admin Management ---

# READ all users (for Admin Dashboard)
@app.route('/api/users', methods=['GET'])
def get_all_users():
    # TODO: Add authentication to make sure only an 'Owner' can access this!

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute('SELECT user_id, email, role, created_at FROM Users ORDER BY user_id;')
    users = cur.fetchall()
    cur.close()
    conn.close()

    user_list = []
    for row in users:
        user_list.append({
            "user_id": row[0],
            "email": row[1],
            "role": row[2],
            "created_at": row[3].strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify(user_list), 200
