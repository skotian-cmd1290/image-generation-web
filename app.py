import streamlit as st
import requests
import base64

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Image Generation • Luxury AI",
    page_icon="🎬",
    layout="centered"
)

HF_TOKEN = st.secrets["HF_TOKEN"]
API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# ---------------- LUXURY CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

body {
    background: linear-gradient(135deg, #e6f2ff 0%, #f8fbff 50%, #eef6ff 100%);
}

.main-card {
    background: linear-gradient(145deg, #0b2c45, #0e3a5f);
    padding: 2.8rem;
    border-radius: 24px;
    box-shadow: 0 30px 80px rgba(0,0,0,0.15);
    color: white;
}

.title {
    font-size: 2.6rem;
    font-weight: 700;
    letter-spacing: -0.03em;
}

.subtitle {
    font-size: 1.05rem;
    color: #b6d6ff;
    margin-top: 0.4rem;
}

.section {
    margin-top: 2rem;
}

label {
    font-weight: 600 !important;
    color: #0b2c45 !important;
}

textarea {
    border-radius: 16px !important;
    padding: 1rem !important;
}

.stButton > button {
    background: linear-gradient(135deg, #4da3ff, #2f80ed);
    color: white;
    border-radius: 14px;
    font-size: 1rem;
    padding: 0.7rem 2rem;
    border: none;
    box-shadow: 0 10px 30px rgba(77,163,255,0.4);
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 14px 40px rgba(77,163,255,0.55);
}

.preset-box {
    background: white;
    padding: 1.6rem;
    border-radius: 18px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.08);
}

.error-box {
    background: #ffe8e8;
    padding: 1rem;
    border-radius: 12px;
    color: #b00020;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="main-card">
    <div class="title">🎬 Image Generation with Pre-trained Models</div>
    <div class="subtitle">
        Artistic text-to-image generation using Stable Diffusion XL (API-based)
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- PRESETS ----------------
st.markdown('<div class="section preset-box">', unsafe_allow_html=True)

preset = st.selectbox(
    "🎯 Prompt Presets",
    [
        "— Select a preset —",
        "🌅 Cinematic Sunset Scene",
        "🎥 Neo-Noir City Night",
        "🧘 Minimal Luxury Interior",
        "🌊 Ocean Fantasy Artwork",
        "🦸 Hero Portrait (Film Still)"
    ]
)

preset_prompts = {
    "🌅 Cinematic Sunset Scene":
        "cinematic sunset scene, warm light, soft clouds, shallow depth of field, film still, ultra detailed",
    "🎥 Neo-Noir City Night":
        "neo noir city at night, rain reflections, neon lights, cinematic lighting, 35mm film",
    "🧘 Minimal Luxury Interior":
        "minimal luxury interior, ocean blue palette, natural light, modern design, architectural photography",
    "🌊 Ocean Fantasy Artwork":
        "fantasy ocean scene, glowing water, deep blues, ethereal lighting, digital art",
    "🦸 Hero Portrait (Film Still)":
        "cinematic hero portrait, dramatic lighting, dark blue tones, ultra detailed film still"
}

prompt = st.text_area(
    "✍️ Describe your image",
    height=120,
    placeholder="Describe the image you want to generate…"
)

if preset in preset_prompts:
    prompt = preset_prompts[preset]
    st.info("Preset applied. You can edit it further ✨")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- GENERATE ----------------
if st.button("✨ Generate Image"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Creating art… this may take 10–20 seconds"):
            payload = {
                "inputs": prompt,
                "parameters": {
                    "width": 768,
                    "height": 768,
                    "guidance_scale": 7.5,
                    "num_inference_steps": 30
                }
            }

            response = requests.post(API_URL, headers=HEADERS, json=payload)

            if response.status_code == 200:
                image_bytes = response.content
                st.image(image_bytes, caption="Generated Image", use_container_width=True)
            else:
                st.markdown(
                    '<div class="error-box">Image generation failed. Please wait 15 seconds and try again.</div>',
                    unsafe_allow_html=True
                )
