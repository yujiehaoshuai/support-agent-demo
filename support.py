"""Small, auditable support tools. All records are synthetic demo data."""
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB = Path(__file__).with_name('support.db')

@contextmanager
def connection():
    conn = sqlite3.connect(DB)
    try:
        with conn:
            yield conn
    finally:
        conn.close()
POLICIES = {
    '退货': '签收后7天内，商品未使用且包装完整可申请退货；定制商品除外。',
    '运费': '质量问题由商家承担退货运费，个人原因由买家承担。',
    '发货': '付款后48小时内发货，预售商品按商品页约定。',
}

def init_db():
    with connection() as conn:
        conn.executescript('''
        CREATE TABLE IF NOT EXISTS orders(id TEXT PRIMARY KEY, owner TEXT, status TEXT);
        CREATE TABLE IF NOT EXISTS tickets(id INTEGER PRIMARY KEY, owner TEXT, order_id TEXT, reason TEXT, UNIQUE(owner, order_id, reason));
        INSERT OR IGNORE INTO orders VALUES ('A1001','demo','已签收'),('A1002','other','运输中');
        ''')

def search_policy(query: str) -> dict:
    """按关键词检索售后规则，返回可追溯来源；没有结果时不编造。"""
    hits = [{'source': f'policy/{key}', 'text': value} for key, value in POLICIES.items() if key in query]
    return {'results': hits, 'found': bool(hits)}

def lookup_order(order_id: str, owner: str = 'demo') -> dict:
    """只允许查询当前演示账户拥有的订单。"""
    with connection() as conn:
        row = conn.execute('SELECT id,status FROM orders WHERE id=? AND owner=?', (order_id, owner)).fetchone()
    return {'id': row[0], 'status': row[1]} if row else {'error': '订单不存在或无权访问'}

def create_ticket(order_id: str, reason: str, owner: str = 'demo') -> dict:
    """仅由界面明确确认后调用；重复提交返回同一工单。"""
    if 'error' in lookup_order(order_id, owner):
        return {'error': '订单不存在或无权访问'}
    reason = reason.strip()
    if not 2 <= len(reason) <= 500:
        return {'error': '原因长度须为2到500字'}
    with connection() as conn:
        conn.execute('INSERT OR IGNORE INTO tickets(owner,order_id,reason) VALUES (?,?,?)', (owner, order_id, reason))
        ticket = conn.execute('SELECT id FROM tickets WHERE owner=? AND order_id=? AND reason=?', (owner, order_id, reason)).fetchone()[0]
    return {'ticket_id': ticket, 'status': '待人工处理'}

def demo_answer(query):
    """确定性演示路径，不代表模型推理能力。"""
    import re
    order = re.search(r'A\d+', query)
    trace = []
    if order:
        trace.append({'tool': 'lookup_order', 'result': lookup_order(order.group())})
    trace.append({'tool': 'search_policy', 'result': search_policy(query)})
    return trace
