import base64
import os
from pathlib import Path

import requests
import streamlit as st


st.set_page_config(page_title="unikX | AI Studio", page_icon="✦", layout="wide")

UNIVERSE_IMAGE = "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?auto=format&fit=crop&w=2400&q=90"
LOGO_PATH = Path(__file__).with_name("logo.png")


def render_copy_button(message_id: int, text: str) -> None:
    encoded_text = base64.b64encode(text.encode("utf-8")).decode("ascii")
    st.html(
        f"""
        <button id="copy-reply-{message_id}" type="button" aria-label="Copy reply">Copy</button>
        <script>
        const button = document.getElementById("copy-reply-{message_id}");
        button.addEventListener("click", async () => {{
            const binary = atob("{encoded_text}");
            const bytes = Uint8Array.from(binary, character => character.charCodeAt(0));
            await navigator.clipboard.writeText(new TextDecoder().decode(bytes));
            button.textContent = "Copied";
            window.setTimeout(() => button.textContent = "Copy", 1400);
        }});
        </script>
        <style>
        button {{ color:#a8f0d1; background:rgba(9,14,22,.8); border:1px solid rgba(255,255,255,.2);
            border-radius:6px; padding:5px 12px; cursor:pointer; font:500 12px 'DM Mono',monospace; }}
        button:hover {{ border-color:#a8f0d1; }}
        </style>
        """,
        unsafe_allow_javascript=True,
        width="content",
    )


st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {{
        --ink: #f5f4f2;
        --muted: #a7adb9;
        --line: rgba(255,255,255,.13);
        --panel: rgba(11, 16, 26, .78);
        --mint: #a8f0d1;
        --coral: #ffae91;
    }}
    html, body, [class*="css"] {{ font-family: 'Manrope', sans-serif; }}
    .stApp {{
        color: var(--ink);
        background-image: linear-gradient(90deg, rgba(6,10,17,.91), rgba(7,12,22,.72) 56%, rgba(6,10,17,.82)),
            linear-gradient(0deg, rgba(6,10,17,.9), transparent 54%),
            url('{UNIVERSE_IMAGE}');
        background-size: cover;
        background-position: center 43%;
        background-attachment: fixed;
    }}
    .stApp [data-testid="stAppViewContainer"] {{ position: relative; z-index: 1; background: transparent; }}
    .stApp [data-testid="stSidebar"] {{ z-index: 5; }}
    #unikx-three-root {{ position: fixed; inset: 0; z-index: 0; overflow: hidden; pointer-events: none; }}
    #unikx-three-root canvas {{ display: block; width: 100%; height: 100%; opacity: .64; }}
    [data-testid="stHeader"] {{ background: transparent; }}
    [data-testid="stSidebar"] {{
        background: rgba(7, 11, 19, .91);
        border-right: 1px solid rgba(255,255,255,.1);
        border-radius: 0 28px 28px 0;
        overflow: hidden;
        box-shadow: 14px 0 44px rgba(0,0,0,.16);
        transform-origin: 100% 50%;
        animation: sidebar-sway 11s ease-in-out infinite;
    }}
    [data-testid="stSidebar"] > div:first-child {{ padding-top: 1.4rem; }}
    [data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"],
    button[data-testid="stExpandSidebarButton"] {{
        width: 38px;
        height: 38px;
        min-height: 38px;
        padding: 0;
        border: 1px solid rgba(168,240,209,.35) !important;
        border-radius: 50% !important;
        background: rgba(12,22,29,.9) !important;
        box-shadow: 0 4px 18px rgba(0,0,0,.28), inset 0 0 12px rgba(168,240,209,.06);
        transition: transform .2s ease, border-color .2s ease, box-shadow .2s ease;
    }}
    [data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"] [data-testid="stIconMaterial"],
    button[data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"] {{
        color: var(--mint) !important;
        font-size: 1.15rem !important;
    }}
    [data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"]:hover,
    button[data-testid="stExpandSidebarButton"]:hover {{
        transform: scale(1.06);
        border-color: var(--mint) !important;
        box-shadow: 0 0 18px rgba(168,240,209,.18);
    }}
    [data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"]:focus-visible,
    button[data-testid="stExpandSidebarButton"]:focus-visible {{
        outline: 2px solid var(--mint);
        outline-offset: 3px;
    }}
    .block-container {{ max-width: 1120px; padding-top: 2.4rem; padding-bottom: 7rem; }}
    h1, h2, h3, p, label {{ color: var(--ink); }}
    .brand-lockup {{ display:flex; align-items:center; gap:13px; margin: 0 0 2.3rem; }}
    .brand-name {{ font-size: 1.16rem; font-weight: 800; letter-spacing: 0; }}
    .brand-name span {{ color: var(--mint); }}
    .brand-kicker, .eyebrow {{ color: var(--muted); font: 500 .68rem 'DM Mono', monospace; letter-spacing: 0; text-transform: uppercase; }}
    .hero {{ max-width: 800px; padding: 1rem 0 1.45rem; animation: rise .55s ease-out both; }}
    .eyebrow {{ color: var(--mint); margin: 0 0 .85rem; }}
    .hero h1 {{ font-size: 3.4rem; line-height: 1.05; font-weight: 700; margin: 0; }}
    .hero h1 em {{ color: var(--mint); font-style: normal; }}
    .hero p {{ color: #c1c5cd; font-size: .98rem; line-height: 1.7; margin: .95rem 0 0; max-width: 600px; }}
    .section-label {{ color: #d9dce2; font: 500 .7rem 'DM Mono', monospace; text-transform: uppercase; margin: .9rem 0 .65rem; }}
    [data-testid="stChatMessage"] {{
        background: rgba(10, 15, 24, .76);
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 1rem 1.15rem;
        backdrop-filter: blur(12px);
    }}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p {{ line-height: 1.72; }}
    [data-testid="stChatInput"] {{
        background: rgba(9, 14, 22, .92);
        border: 1px solid rgba(168,240,209,.43);
        border-radius: 8px;
        box-shadow: 0 12px 45px rgba(0,0,0,.3);
    }}
    [data-testid="stChatInput"] textarea {{ color: var(--ink); }}
    [data-testid="stChatInput"] textarea::placeholder {{ color: #9ba2ae; }}
    [data-testid="stChatInput"] button {{ color: var(--mint); }}
    .stButton > button {{
        width: 100%; min-height: 76px; text-align: left; white-space: normal;
        color: #e8e9ec; background: rgba(13, 19, 29, .74);
        border: 1px solid var(--line); border-radius: 7px;
        transition: border-color .18s ease, background .18s ease, transform .18s ease;
    }}
    .stButton > button p {{ white-space: normal; overflow-wrap: anywhere; line-height: 1.45; }}
    .stButton > button:hover {{ border-color: var(--mint); background: rgba(19, 31, 38, .88); transform: translateY(-2px); color: white; }}
    [data-testid="stExpander"] {{ border: 1px solid var(--line); border-radius: 7px; background: rgba(12,17,26,.62); }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{ color: #c2c7d0; }}
    [data-testid="stSidebar"] hr {{ border-color: var(--line); }}
    .key-note {{ color: #9ca4b1; font-size: .76rem; line-height: 1.55; }}
    .status-line {{ color: var(--mint); font: 500 .68rem 'DM Mono', monospace; text-transform: uppercase; }}
    @keyframes rise {{ from {{ opacity:0; transform:translateY(10px); }} to {{ opacity:1; transform:translateY(0); }} }}
    @keyframes sidebar-sway {{
        0%, 100% {{ transform: perspective(1400px) rotateY(-.65deg); }}
        50% {{ transform: perspective(1400px) rotateY(.65deg); }}
    }}
    @media (prefers-reduced-motion: reduce) {{
        [data-testid="stSidebar"] {{ animation: none; }}
    }}
    @media (max-width: 700px) {{
        .block-container {{ padding: 1.4rem 1rem 6rem; }}
        .hero {{ padding-top: .25rem; }}
        .hero h1 {{ font-size: 2.25rem; }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.html(
    """
    <div id="unikx-three-root" aria-hidden="true"></div>
    <script>
    (() => {
        const root = document.getElementById("unikx-three-root");
        if (!root) return;
        if (window.__unikxThreeScene) window.__unikxThreeScene.dispose();
        root.replaceChildren();

        const startScene = () => {
            if (!window.THREE || !root.isConnected) return;
            const THREE = window.THREE;
            const scene = new THREE.Scene();
            const aspect = window.innerWidth / Math.max(window.innerHeight, 1);
            const camera = new THREE.OrthographicCamera(-5 * aspect, 5 * aspect, 5, -5, 0.1, 60);
            camera.position.z = 24;

            let renderer;
            try {
                renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true, powerPreference: "low-power", preserveDrawingBuffer: true });
            } catch (error) {
                return;
            }
            renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.65));
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setClearColor(0x000000, 0);
            renderer.toneMapping = THREE.ACESFilmicToneMapping;
            renderer.toneMappingExposure = .9;
            root.appendChild(renderer.domElement);

            const planet = new THREE.Group();
            const radius = aspect < 0.8 ? .72 : aspect < 1.15 ? 1.0 : 1.35;
            const planetXFactor = aspect < 0.8 ? 1.14 : aspect < 1.15 ? 1.0 : .78;
            let planetBaseY = aspect < 0.8 ? 1.55 : aspect < 1.15 ? 2.4 : 2.65;
            planet.position.set(5 * aspect * planetXFactor, planetBaseY, -1.1);
            scene.add(planet);

            const textureCanvas = document.createElement("canvas");
            textureCanvas.width = 1024;
            textureCanvas.height = 512;
            const context = textureCanvas.getContext("2d");
            const base = context.createLinearGradient(0, 0, 0, 512);
            base.addColorStop(0, "#163b46");
            base.addColorStop(.3, "#579985");
            base.addColorStop(.53, "#18313d");
            base.addColorStop(.72, "#a66c56");
            base.addColorStop(1, "#132835");
            context.fillStyle = base;
            context.fillRect(0, 0, 1024, 512);
            for (let band = 0; band < 95; band += 1) {
                const y = band * 5.5;
                const height = 1 + Math.random() * 9;
                const wave = Math.random() * 20;
                context.beginPath();
                context.moveTo(0, y);
                for (let x = 0; x <= 1024; x += 32) {
                    context.lineTo(x, y + Math.sin(x * .009 + band) * wave);
                }
                context.lineTo(1024, y + height + 14);
                context.lineTo(0, y + height);
                context.closePath();
                context.fillStyle = band % 4 === 0
                    ? `rgba(182, 236, 206, ${.025 + Math.random() * .075})`
                    : `rgba(5, 17, 28, ${Math.random() * .12})`;
                context.fill();
            }
            const surfaceTexture = new THREE.CanvasTexture(textureCanvas);
            surfaceTexture.colorSpace = THREE.SRGBColorSpace;

            scene.add(new THREE.AmbientLight(0x9db9b2, .62));
            const keyLight = new THREE.DirectionalLight(0xd6fff0, 1.8);
            keyLight.position.set(-5, 6, 9);
            scene.add(keyLight);
            const warmLight = new THREE.PointLight(0xff987e, 3.8, 18);
            warmLight.position.set(5, -2, 4);
            scene.add(warmLight);

            const globe = new THREE.Mesh(
                new THREE.SphereGeometry(radius, 96, 72),
                new THREE.MeshStandardMaterial({
                    map: surfaceTexture,
                    roughness: .78,
                    metalness: .08,
                    transparent: true,
                    opacity: .9,
                }),
            );
            planet.add(globe);

            const atmosphere = new THREE.Mesh(
                new THREE.SphereGeometry(radius * 1.09, 64, 48),
                new THREE.ShaderMaterial({
                    uniforms: {
                        glowColor: { value: new THREE.Color(0x92efd0) },
                        warmColor: { value: new THREE.Color(0xffa78d) },
                    },
                    vertexShader: `
                        varying vec3 vNormal;
                        varying vec3 vViewPosition;
                        void main() {
                            vec4 viewPosition = modelViewMatrix * vec4(position, 1.0);
                            vViewPosition = -viewPosition.xyz;
                            vNormal = normalize(normalMatrix * normal);
                            gl_Position = projectionMatrix * viewPosition;
                        }
                    `,
                    fragmentShader: `
                        uniform vec3 glowColor;
                        uniform vec3 warmColor;
                        varying vec3 vNormal;
                        varying vec3 vViewPosition;
                        void main() {
                            float rim = pow(1.0 - max(dot(normalize(vNormal), normalize(vViewPosition)), 0.0), 3.0);
                            vec3 color = mix(glowColor, warmColor, smoothstep(-0.5, 0.8, vNormal.y));
                            gl_FragColor = vec4(color, rim * 0.48);
                        }
                    `,
                    side: THREE.BackSide,
                    blending: THREE.AdditiveBlending,
                    transparent: true,
                    depthWrite: false,
                }),
            );
            planet.add(atmosphere);

            const rings = new THREE.Group();
            rings.rotation.set(1.18, -.24, -.16);
            planet.add(rings);
            const ringMaterial = new THREE.MeshBasicMaterial({
                color: 0xa4ead2,
                transparent: true,
                opacity: .42,
                side: THREE.DoubleSide,
                depthWrite: false,
            });
            rings.add(new THREE.Mesh(new THREE.TorusGeometry(radius * 1.48, .035, 8, 180), ringMaterial));
            rings.add(new THREE.Mesh(
                new THREE.TorusGeometry(radius * 1.72, .012, 6, 180),
                new THREE.MeshBasicMaterial({ color: 0xffb398, transparent: true, opacity: .3, side: THREE.DoubleSide }),
            ));

            const cometOrbit = new THREE.Group();
            cometOrbit.rotation.set(1.15, .22, -.34);
            planet.add(cometOrbit);
            const cometPath = new THREE.EllipseCurve(0, 0, radius * 2.15, radius * 1.12, 0, Math.PI * 2, false, 0);
            const orbitPoints = cometPath.getPoints(180).map((point) => new THREE.Vector3(point.x, point.y, 0));
            cometOrbit.add(new THREE.Line(
                new THREE.BufferGeometry().setFromPoints(orbitPoints),
                new THREE.LineBasicMaterial({ color: 0xa8f0d1, transparent: true, opacity: .13 }),
            ));
            const comet = new THREE.Group();
            const cometHead = new THREE.Mesh(
                new THREE.SphereGeometry(radius * .045, 20, 16),
                new THREE.MeshBasicMaterial({ color: 0xffd7b6, toneMapped: false }),
            );
            comet.add(cometHead);
            const cometTrailPositions = new Float32Array(36 * 3);
            const cometTrailGeometry = new THREE.BufferGeometry();
            cometTrailGeometry.setAttribute("position", new THREE.BufferAttribute(cometTrailPositions, 3));
            const cometTrail = new THREE.Line(
                cometTrailGeometry,
                new THREE.LineBasicMaterial({ color: 0xffb398, transparent: true, opacity: .8 }),
            );
            cometOrbit.add(cometTrail);
            cometOrbit.add(comet);

            const moonOrbit = new THREE.Group();
            planet.add(moonOrbit);
            const moon = new THREE.Mesh(
                new THREE.SphereGeometry(radius * .12, 32, 24),
                new THREE.MeshStandardMaterial({ color: 0xe5c9ab, roughness: .9, metalness: .04 }),
            );
            moon.position.set(radius * 2.15, radius * .88, .3);
            moonOrbit.add(moon);

            const starCount = window.innerWidth < 700 ? 280 : 640;
            const starPositions = new Float32Array(starCount * 3);
            const starColors = new Float32Array(starCount * 3);
            const mint = new THREE.Color(0xa8f0d1);
            const coral = new THREE.Color(0xffae91);
            for (let index = 0; index < starCount; index += 1) {
                starPositions[index * 3] = (Math.random() * 2 - 1) * 5 * aspect;
                starPositions[index * 3 + 1] = (Math.random() * 2 - 1) * 5;
                starPositions[index * 3 + 2] = -4 - Math.random() * 12;
                const tint = Math.random() > .82 ? coral : mint;
                starColors[index * 3] = tint.r;
                starColors[index * 3 + 1] = tint.g;
                starColors[index * 3 + 2] = tint.b;
            }
            const starGeometry = new THREE.BufferGeometry();
            starGeometry.setAttribute("position", new THREE.BufferAttribute(starPositions, 3));
            starGeometry.setAttribute("color", new THREE.BufferAttribute(starColors, 3));
            const stars = new THREE.Points(
                starGeometry,
                new THREE.PointsMaterial({ size: .035, vertexColors: true, transparent: true, opacity: .65, sizeAttenuation: false }),
            );
            scene.add(stars);
            const starMaterial = stars.material;

            const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
            const clock = new THREE.Clock();
            let animationFrame = 0;
            const render = () => {
                const elapsed = clock.getElapsedTime();
                if (!reducedMotion) {
                    planet.position.y = planetBaseY + Math.sin(elapsed * .32) * .09;
                    planet.rotation.y = elapsed * .035;
                    globe.rotation.y = elapsed * .045;
                    rings.rotation.z = Math.sin(elapsed * .24) * .045;
                    moonOrbit.rotation.y = elapsed * .16;
                    const cometAngle = elapsed * .34;
                    const positions = cometTrailGeometry.attributes.position.array;
                    for (let index = 0; index < 36; index += 1) {
                        const trailAngle = cometAngle - index * .022;
                        const point = cometPath.getPointAt(((trailAngle / (Math.PI * 2)) % 1 + 1) % 1);
                        positions[index * 3] = point.x;
                        positions[index * 3 + 1] = point.y;
                        positions[index * 3 + 2] = Math.sin(trailAngle * 2) * radius * .16;
                    }
                    cometTrailGeometry.attributes.position.needsUpdate = true;
                    const cometPoint = cometPath.getPointAt(((cometAngle / (Math.PI * 2)) % 1 + 1) % 1);
                    comet.position.set(cometPoint.x, cometPoint.y, Math.sin(cometAngle * 2) * radius * .16);
                    cometHead.scale.setScalar(.82 + (Math.sin(elapsed * 2.8) + 1) * .16);
                    starMaterial.opacity = .52 + Math.sin(elapsed * .8) * .08;
                    stars.rotation.z = elapsed * .002;
                }
                renderer.render(scene, camera);
                if (!reducedMotion) animationFrame = window.requestAnimationFrame(render);
            };

            const resize = () => {
                const width = window.innerWidth;
                const height = window.innerHeight;
                const nextAspect = width / Math.max(height, 1);
                camera.left = -5 * nextAspect;
                camera.right = 5 * nextAspect;
                camera.updateProjectionMatrix();
                planet.position.x = 5 * nextAspect * (nextAspect < .8 ? 1.14 : nextAspect < 1.15 ? 1.0 : .78);
                planetBaseY = nextAspect < .8 ? 1.55 : nextAspect < 1.15 ? 2.4 : 2.65;
                planet.position.y = planetBaseY;
                renderer.setSize(width, height);
                render();
            };
            window.addEventListener("resize", resize);
            render();

            window.__unikxThreeScene = {
                dispose() {
                    window.cancelAnimationFrame(animationFrame);
                    window.removeEventListener("resize", resize);
                    scene.traverse((object) => {
                        object.geometry?.dispose();
                        if (Array.isArray(object.material)) object.material.forEach((material) => material.dispose());
                        else object.material?.dispose();
                    });
                    surfaceTexture.dispose();
                    renderer.dispose();
                    renderer.domElement.remove();
                },
            };
        };

        if (window.THREE) {
            startScene();
        } else {
            const loader = document.createElement("script");
            loader.src = "https://cdn.jsdelivr.net/npm/three@0.149.0/build/three.min.js";
            loader.onload = startScene;
            loader.onerror = () => root.remove();
            document.head.appendChild(loader);
        }
    })();
    </script>
    """,
    unsafe_allow_javascript=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

api_key = os.environ.get("GROQ_API_KEY", "")
try:
    api_key = st.secrets.get("GROQ_API_KEY", api_key)
except Exception:
    pass

with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=200)
    st.markdown('<div class="brand-lockup"><div><div class="brand-name">unik<span>X</span></div><div class="brand-kicker">intelligence, in orbit</div></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Workspace</div>', unsafe_allow_html=True)
    model = st.selectbox(
        "Model",
        options=["openai/gpt-oss-20b", "openai/gpt-oss-120b", "qwen/qwen3.8-27b"],
        format_func=lambda value: {
            "openai/gpt-oss-20b": "GPT-OSS 20B",
            "openai/gpt-oss-120b": "GPT-OSS 120B",
            "qwen/qwen3.8-27b": "Qwen 3.8 27B · photo",
        }[value],
        label_visibility="collapsed",
    )
    if api_key:
        st.markdown('<div class="status-line">● &nbsp;unikX / Groq ready</div>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="key-note">The assistant is temporarily unavailable. Please try again later.</p>', unsafe_allow_html=True)
    st.divider()
    with st.expander("Advanced controls"):
        temperature = st.slider("Creativity", min_value=0.0, max_value=1.0, value=0.65, step=0.05)
        system_instruction = st.text_area(
            "System instruction",
            value="You are unikX, a thoughtful and capable AI assistant. Be accurate, clear, and useful.",
            height=120,
        )
    st.divider()
    st.markdown('<div class="status-line">● &nbsp;Secure session</div>', unsafe_allow_html=True)
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown(
    '<div class="hero"><div class="eyebrow">unikX / personal intelligence</div><h1>Think beyond<br><em>the expected.</em></h1><p>A focused space for ideas, research, and the questions worth following further.</p></div>',
    unsafe_allow_html=True,
)

if not st.session_state.messages:
    st.markdown('<div class="section-label">A place to begin</div>', unsafe_allow_html=True)
    suggestions = [
        "Help me untangle a difficult idea",
        "Turn these notes into a clear plan",
        "Explore a fresh perspective on my project",
    ]
    suggestion_columns = st.columns(3)
    selected_prompt = None
    for column, suggestion in zip(suggestion_columns, suggestions):
        with column:
            if st.button(f"↗  {suggestion}", key=f"suggestion-{suggestion}"):
                selected_prompt = suggestion
else:
    selected_prompt = None

for message_index, message in enumerate(st.session_state.messages):
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role, avatar="✨" if role == "assistant" else "👤"):
        st.markdown(message["content"])
        images = message.get("images", [])
        if message.get("image_bytes"):
            images = [*images, {"bytes": message["image_bytes"], "type": message["image_type"]}]
        for image in images:
            st.image(image["bytes"], width=360)
        if role == "assistant":
            render_copy_button(message_index, message["content"])

chat_submission = st.chat_input(
    "Message unikX..." if api_key else "unikX is temporarily unavailable",
    accept_file="multiple",
    file_type=["image/*", "audio/*"],
    accept_audio=True,
    max_upload_size=25,
    disabled=not api_key,
)
typed_prompt = chat_submission.text.strip() if chat_submission is not None else ""
submitted_files = chat_submission.files if chat_submission is not None else []
voice_recording = chat_submission.audio if chat_submission is not None else None
uploaded_images = [file for file in submitted_files if file.type.startswith("image/")]
uploaded_audio = [file for file in submitted_files if file.type.startswith("audio/")]
if voice_recording is not None:
    uploaded_audio.append(voice_recording)

media_prompt = "Please analyze the attached media."
if not uploaded_images and uploaded_audio:
    media_prompt = "Please transcribe and respond to the attached voice recording."
prompt = typed_prompt or selected_prompt or (
    media_prompt if uploaded_images or uploaded_audio else None
)

if prompt and api_key:
    try:
        user_content = prompt
        transcripts = []
        for audio_file in uploaded_audio:
            audio_bytes = audio_file.getvalue()
            with st.spinner("Transcribing your voice recording..."):
                transcription_response = requests.post(
                    "https://api.groq.com/openai/v1/audio/transcriptions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    files={"file": (audio_file.name, audio_bytes, audio_file.type)},
                    data={"model": "whisper-large-v3-turbo", "response_format": "json"},
                    timeout=120,
                )
                transcription_response.raise_for_status()
                transcript = transcription_response.json().get("text", "").strip()
            if transcript:
                transcripts.append(transcript)
        if uploaded_audio and not transcripts:
            raise ValueError("No speech could be transcribed from the recording.")
        if transcripts:
            transcript = "\n".join(transcripts)
            user_content += f"\n\nVoice transcript: {transcript}"

        user_message = {"role": "user", "content": user_content}
        if uploaded_images:
            user_message_images = []
            for image_file in uploaded_images:
                image_bytes = image_file.getvalue()
                if len(image_bytes) > 20 * 1024 * 1024:
                    raise ValueError("Each photo must be 20 MB or smaller.")
                user_message_images.append({"bytes": image_bytes, "type": image_file.type})
            user_message["images"] = user_message_images
        st.session_state.messages.append(user_message)

        with st.chat_message("user", avatar="👤"):
            st.markdown(user_content)
            for image in user_message.get("images", []):
                st.image(image["bytes"], width=360)

        with st.chat_message("assistant", avatar="✨"):
            with st.spinner("unikX is thinking..."):
                chat_messages = [{"role": "system", "content": system_instruction}]
                for message in st.session_state.messages:
                    role = "assistant" if message["role"] == "model" else message["role"]
                    content = message["content"]
                    images = message.get("images", [])
                    if message.get("image_bytes"):
                        images = [*images, {"bytes": message["image_bytes"], "type": message["image_type"]}]
                    if images:
                        content = [{"type": "text", "text": message["content"]}]
                        for image in images:
                            encoded_image = base64.b64encode(image["bytes"]).decode("ascii")
                            content.append(
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:{image['type']};base64,{encoded_image}"
                                    },
                                }
                            )
                    chat_messages.append({"role": role, "content": content})
                request_model = (
                    "qwen/qwen3.8-27b"
                    if any(message.get("images") or message.get("image_bytes") for message in st.session_state.messages)
                    else model
                )
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "model": request_model,
                        "messages": chat_messages,
                        "temperature": temperature,
                    },
                    timeout=90,
                )
                response.raise_for_status()
                answer = response.json()["choices"][0]["message"]["content"]
                if not answer:
                    answer = "I couldn't produce a text response for that request."
                st.markdown(answer)
                st.session_state.messages.append({"role": "model", "content": answer})
                render_copy_button(len(st.session_state.messages) - 1, answer)
    except Exception as error:
        st.error(f"Groq request failed: {error}")