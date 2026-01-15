import sqlite3
from datetime import datetime
from app.models import get_db_connection


def insert_message(message):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO messages (message_id, from_msisdn, to_msisdn, ts, text, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            message["message_id"],
            message["from"],
            message["to"],
            message["ts"],
            message.get("text"),
            datetime.utcnow().isoformat() + "Z"
        ))
        conn.commit()
        return "created"
    except sqlite3.IntegrityError:
        return "duplicate"
    finally:
        conn.close()


def get_messages(limit, offset, from_filter=None, since=None, q=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    conditions = []
    params = []

    if from_filter:
        conditions.append("from_msisdn = ?")
        params.append(from_filter)

    if since:
        conditions.append("ts >= ?")
        params.append(since)

    if q:
        conditions.append("LOWER(text) LIKE ?")
        params.append(f"%{q.lower()}%")

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    total_query = f"SELECT COUNT(*) FROM messages {where_clause}"
    total = cursor.execute(total_query, params).fetchone()[0]

    data_query = f"""
    SELECT message_id, from_msisdn as 'from', to_msisdn as 'to', ts, text
    FROM messages
    {where_clause}
    ORDER BY ts ASC, message_id ASC
    LIMIT ? OFFSET ?
    """

    rows = cursor.execute(data_query, params + [limit, offset]).fetchall()
    conn.close()

    return total, [dict(row) for row in rows]


def get_stats():
    conn = get_db_connection()
    cursor = conn.cursor()

    total_messages = cursor.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    senders_count = cursor.execute(
        "SELECT COUNT(DISTINCT from_msisdn) FROM messages"
    ).fetchone()[0]

    messages_per_sender = cursor.execute("""
        SELECT from_msisdn as 'from', COUNT(*) as count
        FROM messages
        GROUP BY from_msisdn
        ORDER BY count DESC
        LIMIT 10
    """).fetchall()

    first_ts = cursor.execute("SELECT MIN(ts) FROM messages").fetchone()[0]
    last_ts = cursor.execute("SELECT MAX(ts) FROM messages").fetchone()[0]

    conn.close()

    return {
        "total_messages": total_messages,
        "senders_count": senders_count,
        "messages_per_sender": [dict(row) for row in messages_per_sender],
        "first_message_ts": first_ts,
        "last_message_ts": last_ts
    }