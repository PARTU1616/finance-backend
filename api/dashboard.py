from flask import Blueprint, request, jsonify
from models.financial_record import FinancialRecord
from database import db
from utils.authorization import requires_auth
from datetime import datetime
from sqlalchemy import func, extract

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/summary/', methods=['GET'])
@requires_auth(roles=['Admin', 'Analyst'])
def get_summary():
    """
    Get financial summary with totals and recent activity.
    
    Query Params:
        start_date (str): Filter start date
        end_date (str): Filter end date
    
    Response:
        200: {
            ok: true,
            data: {
                total_income: 50000.00,
                total_expenses: 30000.00,
                net_balance: 20000.00,
                recent_transactions: [...]
            },
            msg: "Summary fetched"
        }
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = FinancialRecord.query
    
    # Apply date filters
    if start_date:
        query = query.filter(FinancialRecord.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    
    if end_date:
        query = query.filter(FinancialRecord.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    records = query.all()
    
    # Calculate totals
    total_income = sum(float(r.amount) for r in records if r.type == 'income')
    total_expenses = sum(float(r.amount) for r in records if r.type == 'expense')
    net_balance = total_income - total_expenses
    
    # Get recent transactions (last 10)
    recent_transactions = (
        FinancialRecord.query
        .order_by(FinancialRecord.date.desc())
        .limit(10)
        .all()
    )
    
    return jsonify(
        ok=True,
        data={
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_balance': net_balance,
            'recent_transactions': [txn.to_dict() for txn in recent_transactions]
        },
        msg="Summary fetched successfully"
    ), 200

@dashboard_bp.route('/category-breakdown/', methods=['GET'])
@requires_auth(roles=['Admin', 'Analyst'])
def get_category_breakdown():
    """
    Get totals grouped by category.
    
    Query Params:
        start_date (str): Filter start date
        end_date (str): Filter end date
    
    Response:
        200: {
            ok: true,
            data: {
                categories: [
                    {category: "Salary", total: 50000.00, type: "income"},
                    {category: "Rent", total: 15000.00, type: "expense"}
                ]
            },
            msg: "Category breakdown fetched"
        }
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = db.session.query(
        FinancialRecord.category,
        FinancialRecord.type,
        func.sum(FinancialRecord.amount).label('total')
    )
    
    # Apply date filters
    if start_date:
        query = query.filter(FinancialRecord.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    
    if end_date:
        query = query.filter(FinancialRecord.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    results = query.group_by(
        FinancialRecord.category,
        FinancialRecord.type
    ).all()
    
    categories = [
        {
            'category': r.category,
            'type': r.type,
            'total': float(r.total)
        }
        for r in results
    ]
    
    return jsonify(
        ok=True,
        data={'categories': categories},
        msg="Category breakdown fetched successfully"
    ), 200

@dashboard_bp.route('/trends/', methods=['GET'])
@requires_auth(roles=['Admin', 'Analyst'])
def get_trends():
    """
    Get time-series trend data.
    
    Query Params:
        period (str): 'monthly' or 'weekly'
        periods (int): Number of periods to return (default: 12)
    
    Response:
        200: {
            ok: true,
            data: {
                trends: [
                    {period: "2024-01", income: 50000, expenses: 30000},
                    {period: "2024-02", income: 52000, expenses: 28000}
                ]
            },
            msg: "Trends fetched"
        }
    """
    period_type = request.args.get('period', 'monthly')
    periods = request.args.get('periods', 12, type=int)
    
    if period_type == 'monthly':
        # Monthly aggregation
        results = db.session.query(
            func.to_char(FinancialRecord.date, 'YYYY-MM').label('period'),
            FinancialRecord.type,
            func.sum(FinancialRecord.amount).label('total')
        ).group_by(
            'period',
            FinancialRecord.type
        ).order_by('period').limit(periods * 2).all()  # *2 for income and expense
    else:
        # Weekly aggregation
        results = db.session.query(
            func.to_char(FinancialRecord.date, 'IYYY-IW').label('period'),
            FinancialRecord.type,
            func.sum(FinancialRecord.amount).label('total')
        ).group_by(
            'period',
            FinancialRecord.type
        ).order_by('period').limit(periods * 2).all()
    
    # Reshape data
    trends = {}
    for r in results:
        if r.period not in trends:
            trends[r.period] = {'period': r.period, 'income': 0, 'expenses': 0}
        
        if r.type == 'income':
            trends[r.period]['income'] = float(r.total)
        else:
            trends[r.period]['expenses'] = float(r.total)
    
    return jsonify(
        ok=True,
        data={'trends': list(trends.values())},
        msg="Trends fetched successfully"
    ), 200
