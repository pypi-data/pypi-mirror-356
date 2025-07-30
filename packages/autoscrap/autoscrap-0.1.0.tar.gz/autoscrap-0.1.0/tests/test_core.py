import pytest
from autoscrap.core import get_text, extract_table
from unittest.mock import patch

EXAMPLE_HTML = '''
<html>
  <body>
    <h1>Title</h1>
    <p>First paragraph.</p>
    <p>Second paragraph.</p>
    <table>
      <tr><th>Name</th><th>Age</th></tr>
      <tr><td>Alice</td><td>30</td></tr>
      <tr><td>Bob</td><td>25</td></tr>
    </table>
  </body>
</html>
'''

class MockResponse:
    def __init__(self, text):
        self.text = text
    def raise_for_status(self):
        pass

@patch('requests.get', return_value=MockResponse(EXAMPLE_HTML))
def test_get_text(mock_get):
    result = get_text('http://fake.url', 'p')
    assert result == ['First paragraph.', 'Second paragraph.']

@patch('requests.get', return_value=MockResponse(EXAMPLE_HTML))
def test_extract_table_list(mock_get):
    table = extract_table('http://fake.url')
    assert table == [
        ['Name', 'Age'],
        ['Alice', '30'],
        ['Bob', '25']
    ]

@patch('requests.get', return_value=MockResponse(EXAMPLE_HTML))
def test_extract_table_dataframe(mock_get):
    try:
        import pandas as pd
    except ImportError:
        pytest.skip('pandas not installed')
    df = extract_table('http://fake.url', as_dataframe=True)
    assert list(df.columns) == ['Name', 'Age']
    assert df.iloc[0]['Name'] == 'Alice'
    assert df.iloc[1]['Age'] == '25' 