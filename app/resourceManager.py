import os
import streamlit as st
import base64
from PIL import Image

WD = os.path.dirname(os.path.abspath(__file__))


@st.cache_data
def get_path(folder, filename):
    return os.path.join(WD, folder, filename)


@st.cache_data
def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    return html


@st.cache_data
def load_svg(path):
    with open(path) as f:
        logo_string = f.read()

    logo = render_svg(logo_string)

    return logo


@st.cache_data
def load_image(image_path) -> Image:
    img = Image.open(image_path)
    return img
