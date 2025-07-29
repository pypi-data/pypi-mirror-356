import streamlit as st
from streamlit_template import Template

st.set_page_config(layout="wide")

style = """
.card {
  /* Add shadows to create the "card" effect */
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
  transition: all 0.2s ease;
  background-color: #ffb6c1;
  border-radius: 15px;
}

/* On mouse-over, add a deeper shadow */
.card:hover {
  box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
}

.card:active {
  transform: scale(.98);
}

/* Add some padding inside the card container */
.container {
  padding: 2px 16px;
}
"""

template = Template(
    """
<div class="card">
  <div class="container">
    <h4><b>{{name}}</b></h4>
    <dl>
        <dt>Job Title</dt>
        <dd>{{job}}</dd>
        <dt>Birthday</dt>
        <dd>{{birthday}}</dd>
        <dt>Residence</dt>
        <dd>{{residence}}</dd>
    </dl>
  </div>
</div>
""",
    style=style,
)

left, right, pvv = st.columns(3)

with left:
    template.render(
        name="Hans Then",
        job="Software Developer",
        birthday="26-03-1972",
        residence="Schiedam",
    )
    template.render(
        name="Ling Then",
        job="Software Developer",
        birthday="26-03-1972",
        residence="Schiedam",
    )
    template.render(
        name="Willem Then",
        job="Software Developer",
        birthday="26-03-1972",
        residence="Schiedam",
    )

with right:
    template.render(
        name="Richard Then",
        job="Software Developer",
        birthday="26-03-1972",
        residence="Schiedam",
    )
    template.render(
        name="Linda Then",
        job="Software Developer",
        birthday="26-03-1972",
        residence="Schiedam",
    )
