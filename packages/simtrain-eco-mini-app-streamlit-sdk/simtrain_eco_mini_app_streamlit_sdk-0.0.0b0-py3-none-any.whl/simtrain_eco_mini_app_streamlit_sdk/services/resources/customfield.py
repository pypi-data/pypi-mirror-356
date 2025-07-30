from streamlit_javascript import st_javascript
from ..helper import Helper
from typing import Optional
from ..api_option import ApiOption
from streamlit.components.v1 import html
import json


class Customfield:
    _resource_name = "customfield"

    def response(self, action: str, options: Optional[ApiOption] = {}):
        return Helper.get_api_response(
            resource=self._resource_name, action=action, options=options
        )

    def openOnScreenForm(self, id: Optional[str] = None):
        id_js = f"'{id}'" if id else "undefined"

        html(
            f"""
          <script>
              window.parent.openOnScreenResourceForm('{self._resource_name}', {{
                  id: {id_js}
              }});
          </script>
          """,
            height=0,
        )
