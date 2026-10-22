"""Exercise actual Streamlit UI without browser or external model calls."""
import tempfile
from pathlib import Path
import support
from streamlit.testing.v1 import AppTest

with tempfile.TemporaryDirectory() as folder:
    support.DB = Path(folder) / 'ui.db'
    app = AppTest.from_file('main.py', default_timeout=30).run()
    assert not app.exception
    app.chat_input[0].set_value('A1001退货运费').run()
    assert not app.exception
    assert '已签收' in app.session_state.messages[-1]['content']
    app.text_area[0].set_value('包装损坏')
    app.checkbox[0].check()
    app.button[1].click().run()
    assert not app.exception
    assert support.create_ticket('A1001', '包装损坏')['ticket_id'] == 1
    print('PASS: render, chat, confirmed ticket')
