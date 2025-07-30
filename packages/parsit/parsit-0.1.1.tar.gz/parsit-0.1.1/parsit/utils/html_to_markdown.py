import re
import logging
from typing import Optional, List, Tuple, Dict, Any
from bs4 import BeautifulSoup, Tag, Comment, NavigableString

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """Clean and normalize text from HTML cells."""
    if not text:
        return ""
    # Replace multiple whitespace with single space and strip
    return ' '.join(str(text).strip().split())

def extract_table_data(table: Tag) -> Tuple[List[str], List[List[str]]]:
    """Extract headers and rows from a BeautifulSoup table tag."""
    def clean_cell_text(cell) -> str:
        text = cell.get_text(' ', strip=True)
        return clean_text(text)
    
    headers = []
    rows = []
    
    # First, try to find thead and extract headers
    thead = table.find('thead')
    if thead:
        for row in thead.find_all('tr'):
            headers = [clean_cell_text(th) for th in row.find_all(['th', 'td']) if clean_cell_text(th)]
            if headers:
                break
    
    # If no headers in thead, check first row for th elements
    if not headers:
        first_row = table.find('tr')
        if first_row:
            th_cells = first_row.find_all(['th', 'td'])  # Be more lenient with cell types
            if any('th' in str(cell) for cell in th_cells):  # If any cell is a th, use as header
                headers = [clean_cell_text(th) for th in th_cells]
    
    # Determine the main body of the table
    tbody = table.find('tbody') or table
    
    # Process all rows in the table body
    for row in tbody.find_all('tr'):
        # Skip empty rows
        if not row.find(['td', 'th']):
            continue
            
        # Get all cells in the row
        cells = row.find_all(['td', 'th'])
        if not cells:
            continue
            
        # Skip header row if we already have headers
        if headers and row.find('th') and len(headers) > 0:
            continue
            
        # Process row data
        row_data = [clean_cell_text(cell) for cell in cells]
        if any(cell for cell in row_data):  # Only add non-empty rows
            rows.append(row_data)
    
    # If we still don't have headers but have rows, use the first row as headers
    if not headers and rows:
        headers = rows.pop(0)
    
    return headers, rows

def create_markdown_table(headers: List[str], rows: List[List[str]]) -> str:
    """
    Create a markdown table from headers and rows with improved formatting.
    
    Args:
        headers: List of header strings
        rows: List of rows, where each row is a list of strings
        
    Returns:
        str: Markdown formatted table
    """
    if not headers and not rows:
        return ""
        
    # If no headers but we have rows, use empty headers
    if not headers and rows:
        headers = [""] * len(rows[0])
    
    # Ensure all rows have the same number of columns as headers
    max_cols = len(headers)
    processed_rows = []
    
    # Process headers
    headers = [str(h) if h is not None else "" for h in headers]
    
    # Process each row
    for row in rows:
        # Skip empty rows
        if not row or not any(cell is not None and str(cell).strip() for cell in row):
            continue
            
        # Clean and normalize each cell
        cleaned_row = []
        for cell in row:
            # Convert to string, strip whitespace, and replace newlines with spaces
            cell_str = str(cell).strip() if cell is not None else ""
            cell_str = ' '.join(cell_str.split())  # Normalize whitespace
            cleaned_row.append(cell_str)
            
        # Pad or truncate row to match header length
        padded_row = (cleaned_row + [""] * max_cols)[:max_cols]
        processed_rows.append(padded_row)
    
    # If no valid rows after processing and no headers, return empty string
    if not processed_rows and not any(headers):
        return ""
    
    # Calculate column widths (minimum width of 3 for the separator)
    col_widths = [max(3, len(header)) for header in headers]
    for row in processed_rows:
        for i in range(len(col_widths)):
            if i < len(row):
                col_widths[i] = max(col_widths[i], len(row[i]))
    
    # Create the header row
    header_cells = []
    for i, header in enumerate(headers):
        if i < len(col_widths):
            header_cells.append(header.ljust(col_widths[i]))
    header_row = "| " + " | ".join(header_cells) + " |"
    
    # Create the separator row
    separator_parts = []
    for width in col_widths:
        separator_parts.append("-" * (width + 2))
    separator = "|" + "|".join(separator_parts) + "|"
    
    # Create data rows
    data_rows = []
    for row in processed_rows:
        row_cells = []
        for i in range(len(col_widths)):
            cell = row[i] if i < len(row) else ""
            row_cells.append(cell.ljust(col_widths[i]))
        data_rows.append("| " + " | ".join(row_cells) + " |")
    
    # Combine all parts
    table_parts = []
    if any(header.strip() for header in headers):  # Only add header if we have non-empty headers
        table_parts.append(header_row)
        table_parts.append(separator)
    table_parts.extend(data_rows)
    
    # Add an extra newline before and after the table for better readability
    if table_parts:
        return "\n" + "\n".join(table_parts) + "\n"
    return ""

def convert_html_table_to_markdown(html_table: str) -> Tuple[str, bool]:
    """
    Convert an HTML table to Markdown format with improved handling for complex tables.
    
    Args:
        html_table: HTML table as string, can be wrapped in HTML/body or markdown code blocks
        
    Returns:
        tuple: (converted_markdown, success)
    """
    def extract_table_from_html(html: str) -> str:
        # Try to find a complete table structure
        table_match = re.search(r'(<table[^>]*>.*?</table>)', html, re.DOTALL | re.IGNORECASE)
        if table_match:
            return table_match.group(1)
        return html
    
    def clean_html(html: str) -> str:
        # Remove script and style tags
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        # Remove HTML comments
        html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
        # Remove extra whitespace but preserve newlines for table structure
        html = re.sub(r'[\t\r\f\v ]+', ' ', html)
        html = re.sub(r'\s*\n\s*', '\n', html)
        return html.strip()
    
    def extract_table_data(table: Tag) -> Tuple[List[str], List[List[str]]]:
        headers = []
        rows = []
        
        # Extract headers from thead or first row with th
        thead = table.find('thead')
        if thead:
            for row in thead.find_all('tr'):
                headers = [clean_text(th.get_text()) for th in row.find_all(['th', 'td'])]
                if headers:
                    break
        
        # If no headers in thead, check first row for th elements
        if not headers:
            first_row = table.find('tr')
            if first_row:
                th_cells = first_row.find_all(['th', 'td'])
                if any('th' in str(cell) for cell in th_cells):
                    headers = [clean_text(th.get_text()) for th in th_cells]
        
        # Get all data rows
        tbody = table.find('tbody') or table
        for row in tbody.find_all('tr'):
            # Skip header row if we already have headers
            if headers and row.find('th'):
                continue
                
            cells = row.find_all(['td', 'th'])
            if cells:  # Only add non-empty rows
                row_data = [clean_text(cell.get_text()) for cell in cells]
                rows.append(row_data)
        
        # If we still don't have headers but have rows, use first row as headers
        if not headers and rows:
            headers = rows.pop(0)
        
        return headers, rows
    
    def clean_text(text: str) -> str:
        if not text:
            return ""
        # Replace multiple whitespace with single space and strip
        return ' '.join(str(text).strip().split())
    
    try:
        # Clean up the input HTML first
        html_table = html_table.strip()
        if not html_table:
            return "", False
        
        # Handle markdown code blocks
        code_block_match = re.search(r'```(?:html)?\s*\n(<table[\s\S]*?</table>)\s*```', html_table, re.IGNORECASE)
        if code_block_match:
            html_table = code_block_match.group(1)
        
        # Extract table HTML
        table_html = extract_table_from_html(html_table)
        if not table_html:
            return html_table, False
            
        # Clean HTML
        table_html = clean_html(table_html)
        
        # Parse the HTML
        soup = BeautifulSoup(table_html, 'html.parser')
        
        # Find the first table
        table = soup.find('table')
        if not table:
            return html_table, False
        
        # Extract table data
        headers, rows = extract_table_data(table)
        
        # If we couldn't extract any data, return the original
        if not headers and not rows:
            return html_table, False
            
        # Create markdown table
        markdown_table = create_markdown_table(headers, rows)
        
        # If the markdown table is empty or too small, return the original
        if not markdown_table or len(markdown_table.strip().split('\n')) < 2:
            return html_table, False
            
        return markdown_table, True
        
    except Exception as e:
        logger.error(f"Error converting table: {str(e)}")
        return html_table, False

def extract_table_from_markdown_code_block(markdown_text: str) -> Optional[str]:
    """
    Extract HTML table from markdown code block.
    
    Args:
        markdown_text: Markdown text containing an HTML table in a code block
        
    Returns:
        Extracted HTML table as string, or None if no table found
    """
    # Look for HTML code blocks that contain tables
    pattern = r'```(?:html)?\s*<table[\s\S]*?</table>\s*```'
    match = re.search(pattern, markdown_text, re.IGNORECASE | re.DOTALL)
    if match:
        # Extract just the table HTML without the code block markers
        table_html = match.group(0)
        # Remove the code block markers
        table_html = re.sub(r'^```(?:html)?\s*', '', table_html, flags=re.IGNORECASE)
        table_html = re.sub(r'\s*```$', '', table_html, flags=re.IGNORECASE)
        return table_html.strip()
    return None

def convert_html_tables_in_text(text: str) -> str:
    """
    Convert all HTML tables in the given text to Markdown tables.
    
    Args:
        text: Text containing HTML tables
        
    Returns:
        Text with HTML tables converted to Markdown
    """
    if not text or '<table' not in text.lower():
        return text
    
    # First handle markdown code blocks with tables
    code_block_pattern = r'```(?:html)?\s*\n(<table[\s\S]*?</table>)\s*```'
    
    def replace_code_block(match):
        table_html = match.group(1)
        markdown_table, success = convert_html_table_to_markdown(table_html)
        return f"\n\n{markdown_table}\n\n" if success else match.group(0)
    
    # Process markdown code blocks first
    result = re.sub(code_block_pattern, replace_code_block, text, flags=re.IGNORECASE)
    
    # Then handle direct HTML tables
    html_table_pattern = r'(<table[\s\S]*?</table>)'
    
    def replace_html_table(match):
        table_html = match.group(1)
        markdown_table, success = convert_html_table_to_markdown(table_html)
        return f"\n\n{markdown_table}\n\n" if success else table_html
    
    # Process direct HTML tables
    result = re.sub(html_table_pattern, replace_html_table, result, flags=re.IGNORECASE)
    
    # Clean up any remaining HTML tags
    soup = BeautifulSoup(result, 'html.parser')
    
    # Remove script and style elements
    for element in soup(['script', 'style']):
        element.decompose()
    
    # Get text and clean up whitespace
    result = soup.get_text()
    result = '\n'.join(line.strip() for line in result.split('\n') if line.strip())
    
    # Clean up excessive newlines
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    return result.strip()

if __name__ == "__main__":
    # Install required packages if not already installed
    import sys
    import subprocess
    import pkg_resources
    
    required = {'beautifulsoup4', 'tabulate'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    
    if missing:
        print(f"Installing missing packages: {', '.join(missing)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
    
    # Import after ensuring packages are installed
    from bs4 import BeautifulSoup
    from tabulate import tabulate
    
    # Test with the table from table1.html
    html = """
    <table><thead><tr><th>DATE</th><th>DESCRIPTION</th><th>WITHDRAWAL</th><th>DEPOSIT</th><th>BALANCE</th></tr></thead><tbody><tr><td></td><td>Previous Balance</td><td></td><td></td><td>34,572.23</td></tr><tr><td>06/01</td><td>Rent Bill</td><td>670.00</td><td></td><td>33,902.23</td></tr><tr><td>06/03</td><td>Check No. 3456<br/>Payment from Nala Spencer</td><td></td><td>740.00</td><td>34,642.23</td></tr><tr><td>06/08</td><td>Electric Bill</td><td>347.85</td><td></td><td>34,294.38</td></tr><tr><td>06/13</td><td>Phone Bill</td><td>75.45</td><td></td><td>34,218.93</td></tr><tr><td>06/15</td><td>Deposit</td><td></td><td>7,245.00</td><td>41,463.93</td></tr><tr><td>06/18</td><td>Debit Transaction<br/>Photography Tools Warehouse</td><td>339.96</td><td></td><td>41,123.97</td></tr><tr><td>06/24</td><td>Deposit</td><td></td><td>3,255.00</td><td>44,378.97</td></tr><tr><td>06/25</td><td>Internet Bill</td><td>88.88</td><td></td><td>44,290.09</td></tr><tr><td>06/28</td><td>Check No. 0231<br/>Payment from Kyubi Tayler</td><td></td><td>935.00</td><td>45,225.09</td></tr><tr><td>06/29</td><td>Payroll Run</td><td>6,493.65</td><td></td><td>38,731.44</td></tr><tr><td>06/30</td><td>Debit Transaction<br/>Picture Perfect Equipments</td><td>1,234.98</td><td></td><td>37,496.46</td></tr><tr><td>06/30</td><td>Interest Earned</td><td></td><td>18.75</td><td>37,515.21</td></tr><tr><td>06/30</td><td>Withholding Tax</td><td>3.75</td><td></td><td>37,511.46</td></tr><tr><td></td><td>Ending Balance</td><td></td><td></td><td>37,511.46</td></tr></tbody></table>
    """

    markdown = html_table_to_markdown(html)
    print("\nConverted Markdown:")
    print(markdown)
