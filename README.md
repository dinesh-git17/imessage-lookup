# iMessage First Message Extractor

This Python project extracts the earliest message for a given phone number from your iMessage chat database. It uses SQLite to query Apple's Messages database and leverages the `rich` library to output results in a formatted, easy-to-read panel.

## Features

- **Database Scanning:** Checks multiple potential locations for the iMessage database on macOS.
- **Phone Number Normalization:** Strips non-digit characters to correctly match phone numbers.
- **Message Retrieval:** Retrieves the first (earliest) message associated with a contact.
- **Formatted Output:** Uses the `rich` library to display the message details in a visually appealing way.

## Prerequisites

- Python 3.x
- [rich](https://github.com/Textualize/rich) package
- Access to your iMessage `chat.db` file. The script assumes default macOS locations:
  - `~/Library/Messages/chat.db`
  - `~/Library/Containers/com.apple.iChat/Data/Library/Messages/chat.db`

## Installation

1. **Clone or Download the Project Files**

2. **Install Dependencies**

   Run the following command in the project directory:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Open the `script.py` file and update the target phone number if needed (the default is `+123 456 7890`):
   ```python
   display_first_message("+123 456 7890")
   ```

2. Run the script:
   ```bash
   python script.py
   ```

3. The script will display the first message details in a formatted panel if found, or it will print an error message if no messages are found.

## Files

- **`script.py`**: The main Python script that extracts and displays the first message.
- **`README.md`**: This documentation file.
- **`requirements.txt`**: Lists the project dependencies.

## License

This project is open source. Feel free to use and modify it as needed.