from flask import Blueprint, request, jsonify, session
from models.financial_record import FinancialRecord
from database import db
from utils.authorization import requires_auth
from datetime import datetime
from decimal import Decimal

transactions_bp = Blueprint('transactions', __name__, url_prefix='/api/transactions')

@transactions_bp.route('/list/', methods=['GET'])
@requires_auth()
def list_transactions():
    """
    List financial transactions with filtering and pagination.
    
    Query Params:
        page (int): Page number
        limit (int): Records per page
        start_date (str): Filter by start date (YYYY-MM-DD)
        end_date (str): Filter by end date (YYYY-MM-DD)
        category (str): Filter by category
        type (str): Filter by type (income/expense)
    
    Response:
        200: {ok: true, records: [...], total_count: int, msg: "Transactions fetched"}
    """
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    category = request.args.get('category')
    txn_type = request.args.get('type')
    
    query = FinancialRecord.query
    
    # Apply filters
    if start_date:
        query = query.filter(FinancialRecord.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    
    if end_date:
        query = query.filter(FinancialRecord.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    if category:
        query = query.filter(FinancialRecord.category == category)
    
    if txn_type:
        query = query.filter(FinancialRecord.type == txn_type)
    
    # Default ordering: date descending
    query = query.order_by(FinancialRecord.date.desc())
    
    total_count = query.count()
    offset = (page - 1) * limit
    transactions = query.offset(offset).limit(limit).all()
    
    return jsonify(
        ok=True,
        records=[txn.to_dict() for txn in transactions],
        total_count=total_count,
        page=page,
        limit=limit,
        msg="Transactions fetched successfully"
    ), 200

@transactions_bp.route('/create/', methods=['POST'])
@requires_auth(roles=['Admin'])
def create_transaction():
    """
    Create a new financial transaction.
    
    Request Body:
        {
            "amount": 1500.50,
            "type": "income|expense",
            "category": "Salary",
            "date": "2024-01-15",
            "notes": "Monthly salary"
        }
    
    Response:
        200: {ok: true, data: {transaction}, msg: "Transaction created"}
        400: {ok: false, error: "Validation error"}
    """
    data = request.json
    
    if not data:
        return jsonify(ok=False, error="No data provided", msg="Request body is required"), 400
    
    amount = data.get('amount')
    txn_type = data.get('type')
    category = data.get('category')
    date_str = data.get('date')
    notes = data.get('notes', '')
    
    # Validation
    if not amount or not txn_type or not category or not date_str:
        return jsonify(ok=False, error="Missing required fields", msg="Amount, type, category, and date are required"), 400
    
    try:
        amount = Decimal(str(amount))
        if amount <= 0:
            return jsonify(ok=False, error="Invalid amount", msg="Amount must be greater than zero"), 400
    except:
        return jsonify(ok=False, error="Invalid amount", msg="Amount must be a valid number"), 400
    
    if txn_type not in ['income', 'expense']:
        return jsonify(ok=False, error="Invalid type", msg="Type must be 'income' or 'expense'"), 400
    
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        return jsonify(ok=False, error="Invalid date format", msg="Date must be in YYYY-MM-DD format"), 400
    
    # Create transaction
    transaction = FinancialRecord(
        amount=amount,
        type=txn_type,
        category=category,
        date=date_obj,
        notes=notes,
        created_by=session.get('user_id')
    )
    
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify(
        ok=True,
        data=transaction.to_dict(),
        msg="Transaction created successfully"
    ), 200

@transactions_bp.route('/update/<int:transaction_id>/', methods=['POST'])
@requires_auth(roles=['Admin'])
def update_transaction(transaction_id):
    """
    Update a financial transaction.
    
    Request Body: Same as create (partial updates allowed)
    
    Response:
        200: {ok: true, data: {updated transaction}, msg: "Transaction updated"}
        404: {ok: false, error: "Transaction not found"}
    """
    transaction = FinancialRecord.query.get(transaction_id)
    
    if not transaction:
        return jsonify(ok=False, error="Transaction not found", msg="The requested transaction does not exist"), 404
    
    data = request.json
    
    if not data:
        return jsonify(ok=False, error="No data provided", msg="Request body is required"), 400
    
    # Update fields if provided
    if 'amount' in data:
        try:
            amount = Decimal(str(data['amount']))
            if amount <= 0:
                return jsonify(ok=False, error="Invalid amount", msg="Amount must be greater than zero"), 400
            transaction.amount = amount
        except:
            return jsonify(ok=False, error="Invalid amount", msg="Amount must be a valid number"), 400
    
    if 'type' in data:
        txn_type = data['type']
        if txn_type not in ['income', 'expense']:
            return jsonify(ok=False, error="Invalid type", msg="Type must be 'income' or 'expense'"), 400
        transaction.type = txn_type
    
    if 'category' in data:
        transaction.category = data['category']
    
    if 'date' in data:
        try:
            transaction.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except:
            return jsonify(ok=False, error="Invalid date format", msg="Date must be in YYYY-MM-DD format"), 400
    
    if 'notes' in data:
        transaction.notes = data['notes']
    
    transaction.updated_by = session.get('user_id')
    db.session.commit()
    
    return jsonify(
        ok=True,
        data=transaction.to_dict(),
        msg="Transaction updated successfully"
    ), 200

@transactions_bp.route('/delete/<int:transaction_id>/', methods=['POST'])
@requires_auth(roles=['Admin'])
def delete_transaction(transaction_id):
    """
    Delete a financial transaction.
    
    Response:
        200: {ok: true, msg: "Transaction deleted"}
        404: {ok: false, error: "Transaction not found"}
    """
    transaction = FinancialRecord.query.get(transaction_id)
    
    if not transaction:
        return jsonify(ok=False, error="Transaction not found", msg="The requested transaction does not exist"), 404
    
    db.session.delete(transaction)
    db.session.commit()
    
    return jsonify(ok=True, msg="Transaction deleted successfully"), 200
