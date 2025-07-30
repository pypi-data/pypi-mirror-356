from streamlit.components.v1 import html


class UI:
    def navigateTo(self, target: str, id: str = None, query: str = None):
        # JS-safe fallback
        id_js = f"'{id}'" if id else "undefined"
        query_js = f"'{query}'" if query else "undefined"

        html(
            f"""
            <script>
                window.parent.navigateTo('{target}', {id_js}, {query_js});
            </script>
            """,
            height=0,
        )
