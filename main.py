import os
import re
import sqlite3

from rich.console import Console
from rich.panel import Panel

console = Console()

# Define the paths to your Messages databases (current and backup)
DB_LOCATIONS = [
    os.path.expanduser("~/Library/Messages/chat.db"),
    os.path.expanduser(
        "~/Library/Containers/com.apple.iChat/Data/Library/Messages/chat.db"
    ),
]


def normalize_number(num):
    """Remove all non-digit characters from a phone number."""
    return re.sub(r"\D", "", num)


def get_normalized_handles(db_path, target_number):
    """
    Query all handles from the database and return those whose normalized form
    contains the normalized target number.
    """
    matching_handles = []
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT id FROM handle;")
        rows = cursor.fetchall()
        conn.close()
        target_norm = normalize_number(target_number)
        for row in rows:
            handle = row[0]
            norm_handle = normalize_number(handle)
            if target_norm in norm_handle:
                matching_handles.append(handle)
    except Exception as e:
        console.print(
            Panel(f"Error fetching handles from {db_path}:\n{e}", style="bold red")
        )
    return matching_handles


def get_first_message_for_handle(db_path, handle_id):
    """
    For a given handle, return the first message (raw date, formatted date, contact,
    sender, and message text) from the database.
    """
    first_msg = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = """
            SELECT
                m.date,
                datetime(m.date / 1000000000 + strftime('%s', '2001-01-01'), 'unixepoch') AS message_date,
                h.id AS contact,
                CASE m.is_from_me WHEN 1 THEN 'Me' ELSE 'Them' END AS sender,
                COALESCE(m.text, '') as message_text
            FROM message m
            JOIN handle h ON m.handle_id = h.rowid
            WHERE h.id = ?
            ORDER BY m.date ASC
            LIMIT 1;
        """
        cursor.execute(query, (handle_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            first_msg = row  # (raw_date, formatted_date, contact, sender, message_text)
    except Exception as e:
        console.print(
            Panel(
                f"Error reading first message from {db_path} for handle {handle_id}:\n{e}",
                style="bold red",
            )
        )
    return first_msg


def get_first_message(target_number: str):
    """
    Scan each database for handles matching the target number.
    For each matching handle, retrieve its earliest message.
    Then, return the overall earliest message among all candidates.
    """
    candidate_messages = []
    for db_path in DB_LOCATIONS:
        if not os.path.exists(db_path):
            continue
        handles = get_normalized_handles(db_path, target_number)
        for handle in handles:
            msg = get_first_message_for_handle(db_path, handle)
            if msg:
                # Append a tuple: (db_path, (raw_date, formatted_date, contact, sender, message_text))
                candidate_messages.append((db_path, msg))
    if not candidate_messages:
        return None
    # Sort by raw_date (the first element of msg tuple) to get the earliest message
    candidate_messages.sort(key=lambda item: item[1][0])
    return candidate_messages[0]


def display_first_message(target_number: str):
    result = get_first_message(target_number)
    if result is None:
        console.print(Panel("No messages found for this contact.", style="bold red"))
        return
    db_path, msg = result
    raw_date, formatted_date, contact, sender, message_text = msg

    panel_content = (
        f"[bold cyan]Date:[/bold cyan] {formatted_date}\n"
        f"[bold magenta]Contact:[/bold magenta] {contact}\n"
        f"[bold green]Sender:[/bold green] {sender}\n"
        f"[bold yellow]Message:[/bold yellow] {message_text}"
    )

    console.print(
        Panel(
            panel_content,
            title=f"First Message for {target_number}",
            border_style="bright_blue",
        )
    )


# Replace with the phone number (or fragment) you're targeting.
display_first_message("+123 456 7890")
