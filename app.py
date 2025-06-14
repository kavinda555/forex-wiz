import streamlit as st
from PIL import Image
import openai
import io
import os

st.set_page_config(page_title="🧠 Forex Vision Wizard", layout="centered")
st.title("📊 Forex Vision Wizard – AI Chart Analyzer")

# Set your API key here (IMPORTANT: Keep this secret in production!)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Read from system environment variable

uploaded_file = st.file_uploader("🖼️ Upload chart screenshot (JPG/PNG)", type=["jpg", "png", "jpeg"])
prompt = st.text_area("✍️ Enter your strategy prompt (e.g., 'Should I buy or sell using support and resistance?')")

if st.button("🔍 Analyze Now"):
    if not uploaded_file or not prompt.strip():
        st.error("Please upload a chart and enter your strategy question.")
    else:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Chart", use_column_width=True)

        with st.spinner("Analyzing with AI..."):
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_bytes = buffered.getvalue()

            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional forex analyst. Analyze the chart using support and resistance, trend, and advanced strategies. Give clear entry, TP (1000–5000 pips), SL, and reasoning."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.4,
                n=1,
                tools=[{
                    "type": "image",
                    "data": img_bytes
                }]
            )

        result = response.choices[0].message.content
        st.markdown("## 🧠 AI Output")
        st.markdown(result)
