# Simtrain Eco Mini App Streamlit SDK

## Installation

1. Install dependencies:

```sh
pip install streamlit
pip install git+https://github.com/jhyong94/streamlit-javascript.git
```

2. Install this SDK:

```sh
pip install simtrain-eco-mini-app-streamlit-sdk
```

---

## Usage

### Get Student List

```python
import streamlit as st
from simtrain_eco_mini_app_streamlit_sdk.sdk import SimtrainEcoMiniAppStreamlitSdk
import pandas as pd

sdk = SimtrainEcoMiniAppStreamlitSdk()

if st.button("Get Students"):
    sdk.student.list()

students = sdk.student.response("list")
if students:
    df = pd.DataFrame(students)[
        ["_id", "studentCode", "studentName", "alternateName", "gender"]
    ]
    st.table(df)
else:
    st.info("No found students.")
```

### Get Student Detail (with Dynamic State)

Use the `options={"api_key": "your_custom_key"}` parameter to manage state separately for different students. This allows you to call the same API action (`detail`) multiple times while maintaining distinct responses.

> **NOTE**: By passing a custom api_key inside options, you isolate the request/response state — allowing multiple calls to the same action (e.g. detail) without conflict. This is especially useful in Streamlit apps where multiple buttons trigger the same backend logic.

```python

# ==================================== Student 1 ====================================

if st.button("Get Student 1"):
    sdk.student.detail(
        id="a2278689-7812-425d-a604-de27322cc2c1",
        options={"api_key": "student1"},
    )

student = sdk.student.response(
    action="detail",
    options={"api_key": "student1"},
)
if student:
    st.write(student)

# ==================================== Student 2 ====================================

if st.button("Get Student 2"):
    sdk.student.detail(
        id="da3b5fad-898e-45c1-a689-05585ebaac72",
        options={"api_key": "student2"},
    )

student = sdk.student.response(
    action="detail",
    options={"api_key": "student2"},
)
if student:
    st.write(student)
```

### Navigate

```python
if st.button("Go to Student Page"):
    sdk.ui.navigate_to("managestudents")
```

### Open On Screen Form

```python
if st.button("Open Student On Screen Add New Form"):
    sdk.student.openOnScreenForm()
```
