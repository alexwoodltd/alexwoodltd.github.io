# utils.py
from string import Template
from datetime import datetime
import re
import shutil
import os

# Function to clear and recreate a directory
def clear_directory(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)  # Remove the directory and its contents
    os.makedirs(directory_path, exist_ok=True)  # Recreate the directory

# Function to parse tab-separated strings and return a list of dictionaries
def parse_tab_separated_strings(data):
    keys = data[0]  # First row contains keys
    result = []
    for row in data[1:]:
        stripped_row = [col.strip() for col in row]
        result.append(dict(zip(keys, stripped_row)))  # Create dictionary for each row
    return result

# Function to create a sorted dictionary by date
def create_sorted_dict(data):
    for trade in data:
        dt = datetime.strptime(trade['date'], '%m/%d/%Y')
        trade['sort_date'] = dt
        trade['title'] = f"Trades for {dt.date()}"
        trade['categories'] = generate_categories(trade)
    
    sorted_data = sorted(data, key=lambda x: x['sort_date'])
    
    sorted_trades_dict = {}
    for trade in sorted_data:
        date_key = trade['sort_date'].date()
        if date_key not in sorted_trades_dict:
            sorted_trades_dict[date_key] = []
        sorted_trades_dict[date_key].append(trade)
    
    return sorted_trades_dict

# Function to generate HTML trade rows based on type (PUT or CALL)
def gen_trade_row(trade, put_row_template, call_row_template, PUT, CALL):
    row_template = put_row_template if trade.get('type').lower() == PUT else call_row_template
    return row_template.safe_substitute(trade)

# Function to extract the first date from a string
def extract_first_date(input_string):
    date_pattern = r'\b(\d{1,2}/\d{1,2}/\d{4})\b'
    match = re.search(date_pattern, input_string)
    if match:
        return datetime.strptime(match.group(1), "%m/%d/%Y").date()
    return None

# Function to write the HTML content to a markdown file
def write_post_to_file(date, content):
    relative_directory = '_posts'
    file_name = f'{date}-trades-for-{date}.md'
    file_path = os.path.join(relative_directory, file_name)
    os.makedirs(relative_directory, exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(content)

def generate_blog_headline(trades):
  # List to hold individual trade summaries
  trade_summaries = []

  # Iterate over each trade and extract the key information
  for trade in trades:
      trade_date = trade['date']
      account_type = trade['account'].strip().upper()
      ticker = trade['ticker'].strip()
      strategy = trade['strategy'].strip()
      trade_type = trade['type'].strip().upper()
      contract_count = trade['contract_cnt']
      
      # Create a summary for this trade
      summary = f"{account_type} {strategy} on {ticker} with {contract_count} {trade_type} Contract(s)"
      trade_summaries.append(f"{trade_date}: {summary}")

  # Join all trade summaries with a separator, such as a new line or a semicolon
  full_summary = " | ".join(trade_summaries)
  
  return full_summary
  
  return headline

def generate_categories(trade):
    # Extract key information from the first trade to use in the headline
    # Extract details from the first trade
    categories = [trade['account'].strip().upper(),
    trade['ticker'].strip().upper(),
    trade['strategy'].strip().upper(),
    trade['type'].strip().upper()]

    return ' '.join(map(str, categories))

def create_markdown_bulleted_list(items):
    """
    Create a Markdown bulleted list from an array of strings.

    Parameters:
    items (list): A list of strings to convert into a bulleted list.

    Returns:
    str: A Markdown formatted bulleted list.
    """
    # Using list comprehension to format each item with a bullet point
    bulleted_list = '\n'.join(f'* {item}' for item in items)
    return bulleted_list
    