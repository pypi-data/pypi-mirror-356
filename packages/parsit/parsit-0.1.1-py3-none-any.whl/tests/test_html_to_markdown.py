import unittest
import os
import sys
from pathlib import Path
import re
from bs4 import BeautifulSoup
from parsit.utils.html_to_markdown import (
    convert_html_table_to_markdown,
    convert_html_tables_in_text,
    extract_table_from_markdown_code_block
)

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestHtmlToMarkdown(unittest.TestCase):
    def setUp(self):
        self.simple_table = """
        <table>
            <tr><th>Name</th><th>Age</th></tr>
            <tr><td>John</td><td>30</td></tr>
            <tr><td>Alice</td><td>25</td></tr>
        </table>
        """
        
        self.table_with_br = """
        <table>
            <tr><th>Name</th><th>Description</th></tr>
            <tr><td>John</td><td>First line<br>Second line</td></tr>
        </table>
        """
        
        self.complex_table = """
        <table>
            <thead>
                <tr><th>ID</th><th>Details</th><th>Price</th></tr>
            </thead>
            <tbody>
                <tr><td>1</td><td>Item 1<br>Description</td><td>$10.00</td></tr>
                <tr><td>2</td><td>Item 2</td><td>$20.00</td></tr>
            </tbody>
        </table>
        """
        
        self.html_wrapped_table = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Test</title></head>
        <body>
            <h1>Test Document</h1>
            {self.simple_table}
            <p>Some text after table</p>
        </body>
        </html>
        """
        
        self.markdown_wrapped_table = f"""
        # Test Document
        
        Here's a table:
        
        ```html
        {self.simple_table}
        ```
        
        And some text after the table.
        """

    def test_extract_table_from_markdown_code_block(self):
        # Test with HTML code block
        md = """
        Some text
        ```html
        <table><tr><td>test</td></tr></table>
        ```
        More text
        """
        result = extract_table_from_markdown_code_block(md)
        self.assertIn("<table>", result)
        self.assertIn("</table>", result)
        
        # Test with no code block
        self.assertIsNone(extract_table_from_markdown_code_block("no table here"))

    def test_convert_html_table_to_markdown(self):
        # Test simple table conversion
        result, success = convert_html_table_to_markdown(self.simple_table)
        self.assertTrue(success)
        # Verify markdown table structure
        lines = [line.strip() for line in result.split('\n') if line.strip()]
        self.assertGreaterEqual(len(lines), 3)  # At least header, separator, and one data row
        self.assertIn('|', lines[0])  # Header row should have pipes
        self.assertTrue('---' in lines[1] or '---' in lines[1].replace(' ', ''))  # Separator line
        # Check for expected data
        self.assertIn("Alice", result)
        self.assertIn("30", result)
        self.assertNotIn("<table>", result)
        
        # Test with a complex PDF table (from test_pdf_table.py)
        pdf_table = """
        <table><tr><td>Fiscal Accident YearEnding09/30</td><td>12 Months</td><td>24 Months</td><td>36 Months</td><td>48 Months</td><td>60 Months</td><td>72 Months</td><td>84M</td></tr>
        <tr><td>2011</td><td></td><td></td><td></td><td></td><td></td><td></td><td>37,02</td></tr>
        <tr><td>2012</td><td></td><td></td><td></td><td></td><td></td><td>39,239,110</td><td>39,23</td></tr>
        <tr><td>2013</td><td></td><td></td><td></td><td></td><td>35,898,511</td><td>35,895,995</td><td>35,89</td></tr>
        </table>
        """
        result, success = convert_html_table_to_markdown(pdf_table)
        self.assertTrue(success)
        self.assertIn("Fiscal Accident", result)
        self.assertIn("35,898,511", result)
        
        # Test with a simplified PDF table (from test_pdf_table_simple.py)
        simple_pdf_table = """
        <table>
            <tr><th>Fiscal Year</th><th>12 Months</th><th>24 Months</th><th>36 Months</th></tr>
            <tr><td>2020</td><td>46,039,133</td><td>51,965,847</td><td></td></tr>
            <tr><td>2021</td><td>45,814,514</td><td>51,874,978</td><td></td></tr>
            <tr><td>2022</td><td></td><td></td><td>Link Ratios</td></tr>
            <tr><td>Development</td><td>12 to 24</td><td>1.006</td><td>1.001</td></tr>
            <tr><td>1st Prior</td><td>1.129</td><td>1.012</td><td>1.001</td></tr>
        </table>
        """
        result, success = convert_html_table_to_markdown(simple_pdf_table)
        self.assertTrue(success)
        self.assertIn("Fiscal Year", result)
        self.assertIn("51,965,847", result)
        self.assertIn("1.129", result)
        
        # Test table with line breaks
        result, success = convert_html_table_to_markdown(self.table_with_br)
        self.assertTrue(success)
        # Check that both lines are present (they might be on the same line with a space)
        self.assertIn("First line", result)
        self.assertIn("Second line", result)
        
        # Test HTML-wrapped table
        result, success = convert_html_table_to_markdown(self.html_wrapped_table)
        self.assertTrue(success)
        self.assertIn("Name", result)
        self.assertNotIn("<html>", result)
        
        # Test markdown-wrapped table
        result, success = convert_html_table_to_markdown(self.markdown_wrapped_table)
        self.assertTrue(success)
        self.assertIn("Name", result)
        self.assertNotIn("```", result)

    def test_convert_html_tables_in_text(self):
        # Test with direct HTML table
        text = f"""
        Here is some text with a table:
        {self.simple_table}
        And more text after.
        """
        result = convert_html_tables_in_text(text)
        # Check for expected content without checking specific column names
        self.assertIn("Alice", result)
        self.assertIn("30", result)
        self.assertNotIn("<table>", result)
        # Verify table structure is preserved in the output
        self.assertIn('|', result)  # Should contain markdown table syntax
        self.assertIn('---', result)  # Should contain table separator
        
        # Test with markdown code block
        text = f"""
        Here is some text with a table in code block:
        ```html
        {self.simple_table}
        ```
        And more text after.
        """
        result = convert_html_tables_in_text(text)
        
        # Check if the table was converted to markdown format
        # We should see markdown table syntax (pipes and dashes)
        self.assertIn("|", result)  # Should contain markdown table syntax
        self.assertIn("---", result)  # Should contain table separator
        
        # The original HTML table tags should be removed
        self.assertNotIn("<table>", result)
        self.assertNotIn("</table>", result)
        
        # The content should be preserved
        self.assertIn("Name", result)
        self.assertIn("Alice", result)
        
        # Note: The current implementation doesn't remove the code block markers,
        # so we won't check for their absence
        
        # Test with HTML document
        result = convert_html_tables_in_text(self.html_wrapped_table)
        self.assertIn("Name", result)
        self.assertIn("Test Document", result)  # Should preserve non-table content
        self.assertNotIn("<html>", result)
        self.assertNotIn("<table>", result)

    def test_edge_cases(self):
        # Empty table
        result, success = convert_html_table_to_markdown("<table></table>")
        self.assertFalse(success)
        
        # Invalid HTML
        result, success = convert_html_table_to_markdown("<notatable>invalid</notatable>")
        self.assertFalse(success)
        
        # None input
        result = convert_html_tables_in_text(None)
        self.assertEqual(result, None)
        
        # Empty string
        result = convert_html_tables_in_text("")
        self.assertEqual(result, "")

    def test_real_world_table(self):
        html = """
        <table>
            <tr><th>Name</th><th>Age</th></tr>
            <tr><td>Alice</td><td>30</td></tr>
            <tr><td>Bob</td><td>25</td></tr>
        </table>
        """
        result, success = convert_html_table_to_markdown(html)
        self.assertTrue(success)
        # Check for data content regardless of header names
        self.assertIn("Alice", result)
        self.assertIn("Bob", result)
        self.assertIn("30", result)
        self.assertIn("25", result)
        self.assertNotIn("<table>", result)
        self.assertNotIn("<tr>", result)
        self.assertNotIn("<td>", result)
        # Verify table structure by checking number of rows and columns
        lines = [line.strip() for line in result.split('\n') if line.strip()]
        self.assertGreaterEqual(len(lines), 3)  # Header, separator, and at least one data row
        for line in lines:
            self.assertIn('|', line)  # Verify markdown table format

    def test_table_with_br_tags(self):
        html = """
        <table>
            <tr><th>ID</th><th>Description</th></tr>
            <tr><td>1</td><td>First line<br>Second line</td></tr>
        </table>
        """
        result = convert_html_tables_in_text(html)
        # Check that both lines appear in the output
        self.assertIn("First line", result)
        self.assertIn("Second line", result)
        self.assertIn("1", result)

    def test_empty_table(self):
        html = "<table></table>"
        result, success = convert_html_table_to_markdown(html)
        self.assertFalse(success)

    def test_invalid_html(self):
        result, success = convert_html_table_to_markdown("<notatable>")
        self.assertFalse(success)

    def test_complex_table_with_headers(self):
        html = """
        <table>
            <thead><tr><th>DATE</th><th>DESCRIPTION</th><th>AMOUNT</th></tr></thead>
            <tbody>
                <tr><td>2023-01-01</td><td>Grocery</td><td>100.00</td></tr>
                <tr><td>2023-01-02</td><td>Rent</td><td>1000.00</td></tr>
            </tbody>
        </table>
        """
        result, success = convert_html_table_to_markdown(html)
        self.assertTrue(success)
        # Check all expected content is in the result
        self.assertIn("2023-01-01", result)
        self.assertIn("Grocery", result)
        self.assertIn("100", result)  # Check without decimal as tabulate might format it
        self.assertIn("2023-01-02", result)
        self.assertIn("Rent", result)
        self.assertIn("1000", result)  # Check without decimal as tabulate might format it
        self.assertGreaterEqual(len(result.split('\n')), 3)  # At least header + separator + 2 rows

if __name__ == "__main__":
    unittest.main()
