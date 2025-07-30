# Simtrain Eco Mini App Streamlit SDK

## Installation

1. Install dependencies:

```sh
pip install streamlit
pip install git+https://github.com/thunderbug1/streamlit-javascript.git@1.42.0
```

2. Install this SDK:

```sh
pip install git+https://github.com/yourusername/yourrepo.git
```

3. Copy the missing frontend folder into the streamlit_javascript package:

```sh
cp -r missing_streamlit_javascript/frontend $(python -c "import streamlit_javascript; import os; print(os.path.dirname(streamlit_javascript.__file__))")/
```

---

Update the URL above to your actual repository if needed.
