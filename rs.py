import streamlit as st
import langchain_helper as lh
import re

# --- 1. SIDEBAR AND INPUT LOGIC ---
st.sidebar.title("Restaurant Menu Designer")
st.sidebar.write("Choose a cuisine to generate a printable menu.")

cuisine_bg_images = {
    "Italian": "https://images.unsplash.com/photo-1551183053-bf91a1d81141",
    "Chinese": "https://images.unsplash.com/photo-1585841773408-1146318370de",
    "Mexican": "https://images.unsplash.com/photo-1565299715636-c6b817b07436",
    "Indian": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8",
    "French": "https://images.unsplash.com/photo-1511920183863-9b8f36214311",
    "Japanese": "https://images.unsplash.com/photo-1569308027668-30948e5898d0",
    "Mediterranean": "https://images.unsplash.com/photo-1600326145550-2defda9789f2"
}
DEFAULT_BG_IMAGE = "https://images.unsplash.com/photo-1555396273-367ea4eb4db5"

cuisine_options = list(cuisine_bg_images.keys())
cuisine_select = st.sidebar.selectbox("Pick a Cuisine", cuisine_options)
cuisine_custom = st.sidebar.text_input("Or Enter a Custom Cuisine")
generate_button = st.sidebar.button("Generate Menu ✨")
st.sidebar.markdown("---")
st.sidebar.caption("Developed by Sohan Barik 🧑‍💻©")

if cuisine_custom:
    selected_cuisine = cuisine_custom
    bg_image_url = DEFAULT_BG_IMAGE
else:
    selected_cuisine = cuisine_select
    bg_image_url = cuisine_bg_images.get(selected_cuisine, DEFAULT_BG_IMAGE)

# --- 2. CSS FOR A4 MENU STYLE WITH BACKGROUND IMAGE ---
A4_BG_IMAGE = "https://media.istockphoto.com/id/522474608/photo/place-setting-shot-directly-above.jpg?s=612x612&w=0&k=20&c=ATOlj0zxYlFCJvLMhBawvAzdaJWuSl0WKPAU4V94JPc="  # Elegant restaurant background

st.markdown(
    f"""
    <style>
    body {{
        background: #222;
    }}
    .a4-menu {{
        background: url('{A4_BG_IMAGE}') center center/cover no-repeat;
        width: 21cm;
        height: 29.7cm;
        margin: 32px auto;
        box-shadow: 0 0 24px 4px rgba(0,0,0,0.15);
        border-radius: 12px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-family: 'Georgia', 'Times New Roman', Times, serif;
        position: relative;
        overflow: hidden;
    }}
    .menu-overlay {{
        background: rgba(255,255,255,0.7);
        width: 85%;
        border-radius: 14px;
        padding: 2.5cm 2cm 2cm 2cm;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 32px 0 rgba(0,0,0,0.12);
    }}
    .menu-title {{
        font-size: 2.7rem;
        font-family: 'Playfair Display', serif;
        font-weight: bold;
        letter-spacing: 2px;
        color: #2d2d2d;
        margin-bottom: 0.5em;
        text-align: center;
        border-bottom: 2px solid #e0c097;
        padding-bottom: 0.2em;
        width: 100%;
        background: none;
    }}
    .menu-section-title {{
        font-size: 1.3rem;
        color: #b48a3a;
        font-family: 'Playfair Display', serif;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
        letter-spacing: 1px;
        text-align: center;
        background: none;
    }}
    .menu-items {{
        width: 100%;
        display: flex;
        justify-content: space-between;
        gap: 2em;
        margin-bottom: 1.5em;
        background: none;
    }}
    .menu-column {{
        width: 48%;
        background: none;
    }}
    .menu-item {{
        font-size: 1.18rem;
        color: #333;
        margin-bottom: 0.7em;
        font-weight: bold;
        border-bottom: 1px dotted #e0c097;
        padding-bottom: 0.2em;
        background: none;
    }}
    .restaurant-footer {{
        margin-top: 2em;
        width: 100%;
        text-align: center;
        color: #b48a3a;
        font-size: 1.1rem;
        font-family: 'Playfair Display', serif;
        letter-spacing: 1px;
        background: none;
    }}
    @media print {{
        body, .stApp {{
            background: #fff !important;
        }}
        .a4-menu {{
            box-shadow: none !important;
            margin: 0 !important;
            border-radius: 0 !important;
            padding: 0 !important;
        }}
        .menu-overlay {{
            background: rgba(255,255,255,0.85) !important;
            padding: 1cm !important;
        }}
        .restaurant-footer {{
            position: static !important;
        }}
        header, footer, .stSidebar, .stToolbar, .stActionButton, .stDownloadButton, .stAlert {{
            display: none !important;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- 3. MENU RENDERING FUNCTION ---
def render_menu(name, items):
    """Render menu items sequentially with numbers."""
    # Clean and validate items
    items = [item.strip() for item in items if item.strip()]
    
    # Build HTML for menu items with numbers and line breaks
    menu_items_html = "".join(
        # f'<div class="menu-item"><{i+1}. {item}<br></div>' 
        f'<div class="menu-item">{i}.{item}</div>' 
        for i, item in enumerate(items)
    )

    # Update menu layout
    full_html = f"""
    <div class="a4-menu">
        <div class="menu-overlay">
            <div class="menu-title">{name}</div>
            <div class="menu-section-title">Menu Items</div>
            <div class="menu-items-container">
                {menu_items_html}
            </div>
            <div class="restaurant-footer">Bon Appétit! | Powered by Sohan Barik</div>
        </div>
    </div>
    """
    
    # Add new CSS for sequential layout
    st.markdown(
        """
        <style>
        .menu-items-container {
            width: 80%;
            margin: 0 auto;
            padding: 1em 2em;
        }
        .menu-item {
            font-size: 1.18rem;
            color: #333;
            margin-bottom: 1.2em;
            padding-bottom: 0.8em;
            border-bottom: 1px dotted #e0c097;
            line-height: 1.6;
            text-align: left;
            width: 100%;
            display: block; /* Ensures each is on a new line */
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(full_html, unsafe_allow_html=True)
    

# --- 4. MAIN APP LOGIC ---
if generate_button:
    if not selected_cuisine:
        st.sidebar.error("Please select or enter a cuisine.")
    else:
        with st.spinner(f"Creating a menu for a {selected_cuisine} restaurant..."):
            try:
                response = lh.generate_restaurant_name_and_items(selected_cuisine)
                name = response['restaurant_name'].strip()

                raw_items = response['menu_items'].strip()

                # Split items on "1. ", "2. ", etc.
                items = re.split(r'\d+\.\s*', raw_items)
                items = [item.strip() for item in items if item.strip()]

                render_menu(name, items)
            except Exception as e:
                st.error(f"An error occurred: {e}")

    # Always show the A4 menu container, even before generation
else:
    st.markdown(
        """
        <div class="a4-menu">
            <div class="menu-overlay">
                <div class="menu-title">Restaurant Menu</div>
                <div class="menu-section-title">Menu Items</div>
                <div style="text-align:center; color:#bbb; margin-top:3cm;">
                    <em>Select a cuisine and click 'Generate Menu' to see your menu here.</em>
                </div>
                <div class="restaurant-footer">Bon Appétit! | Powered by Sohan Barik</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

