import streamlit as st
import pickle
import numpy as np
from PIL import Image

# Load the model
rfc = pickle.load(open('rfc.pkl', 'rb'))

# Forest-themed CSS styles
forest_css = """
<style>
body {
    background-color: #f0f3f5; /* Light blue-grey background */
    color: #333333; /* Dark grey text */
    font-family: Arial, sans-serif; /* Font style */
}
.nav-button {
    padding: 10px;
    background-color: #4CAF50; /* Green button */
    color: white;
    border: none;
    border-radius: 5px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
}
.nav-button:hover {
    background-color: #45a049; /* Darker green on hover */
}
h1 {
    color: #004d00; /* Dark green heading */
}
.cover-type {
    margin-top: 20px;
    padding: 10px;
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.cover-type-title {
    font-size: 24px;
    font-weight: bold;
    color: #004d00;
    margin-bottom: 10px;
}
.cover-type-description {
    margin-bottom: 10px;
}
.cover-type-image {
    margin-top: 10px;
    border-radius: 5px;
}
</style>
"""

# Apply forest theme
st.markdown(forest_css, unsafe_allow_html=True)

# Function to show falling leaves animation
def show_falling_leaves_animation():
    animated_leaves = Image.open('falling_fox.gif')
    st.image(animated_leaves, caption='Thanks Anurag for giving your concern on our homes', use_column_width=True)

# Create the web app
st.title('Forest Cover Type Classification')

# Add back navigation button at the top corner
st.markdown("""
    <div style='display: flex; justify-content: flex-end; align-items: center; padding-top: 10px;'>
        <a href="/" class="nav-button">Back</a>
    </div>
    """, unsafe_allow_html=True)

image = Image.open('classify.png')
st.image(image, caption='Forest Cover Type', use_column_width=True)

# Input fields for Id, Elevation, Aspect
st.subheader('Input Features')
Id = st.number_input('Id', value=0, step=1)
Elevation = st.number_input('Elevation', value=0, step=1)
Aspect = st.number_input('Aspect', value=0, step=1)

# Single input box for all other features
input_features_str = st.text_input('Input Features (comma separated integers)')

# Cover type dictionary
cover_type_dict = {
    1: {
        "name": "Spruce/Fir",
        "description": "Spruce and Fir forests are found in high elevation areas with cool, moist climates. They are known for their dense canopy and needle-like leaves.",
        "image_path": "img_1.png",
        "location": "High elevation areas"
    },
    2: {
        "name": "Lodgepole Pine",
        "description": "Lodgepole Pine forests are typically found in mountainous regions and are known for their straight, tall trees. They have long needles and produce cones.",
        "image_path": "img_2.png",
        "location": "Mountainous regions"
    },
    3: {
        "name": "Ponderosa Pine",
        "description": "Ponderosa Pine forests are characterized by large, open stands of tall trees, usually found in lower elevations. They have distinctive large pine cones.",
        "image_path": "img_3.png",
        "location": "Lower elevation areas"
    },
    4: {
        "name": "Cottonwood/Willow",
        "description": "Cottonwood and Willow forests are commonly found along streams and rivers in lowland areas. They have broad leaves and provide habitat for diverse wildlife.",
        "image_path": "img_4.png",
        "location": "Lowland areas near streams and rivers"
    },
    5: {
        "name": "Aspen",
        "description": "Aspen forests are known for their beautiful fall colors and are often found in mountainous regions. They are deciduous trees with rounded leaves that tremble in the wind.",
        "image_path": "img_5.png",
        "location": "Mountainous regions"
    },
    6: {
        "name": "Douglas-fir",
        "description": "Douglas-fir forests are one of the most productive timber regions and are commonly found in the Pacific Northwest. They have distinctive cone shapes and soft needles.",
        "image_path": "img_6.png",
        "location": "Pacific Northwest"
    },
    7: {
        "name": "Krummholz",
        "description": "Krummholz, meaning 'crooked wood', refers to stunted forests found in subalpine areas where harsh conditions limit growth. They have twisted branches and sparse foliage.",
        "image_path": "img_7.png",
        "location": "Subalpine areas"
    }
}

# Function to preprocess input and make prediction
def preprocess_input(Id, Elevation, Aspect, input_features_str):
    # Split input_features_str into a list
    input_features_list = input_features_str.split(',')
    
    # Convert to integers
    try:
        input_features_list = [int(feature.strip()) for feature in input_features_list]
    except ValueError:
        st.warning('Please enter integer values separated by commas.')
        return None
    
    # Add Id, Elevation, Aspect to the beginning of the list
    input_features_list.insert(0, Id)
    input_features_list.insert(1, Elevation)
    input_features_list.insert(2, Aspect)
    
    # Convert to numpy array
    input_features = np.array([input_features_list])
    
    return input_features

# Function to predict cover type
def predict_cover_type(input_features):
    output = rfc.predict(input_features).reshape(1, -1)
    predicted_cover_type = int(output[0])
    return predicted_cover_type

# Submit button
if st.button("Submit"):
    input_features = preprocess_input(Id, Elevation, Aspect, input_features_str)
    
    if input_features is not None:
        predicted_cover_type = predict_cover_type(input_features)
        
        if predicted_cover_type in cover_type_dict:
            # Display cover type information
            st.subheader('Predicted Cover Type Information')
            
            cover_type_info = cover_type_dict[predicted_cover_type]
            
            # Left side: Cover type details (name, description, soil types, location)
            st.markdown(f"<h2 class='cover-type-title'>{cover_type_info['name']}</h2>", unsafe_allow_html=True)
            
            st.write(f"<p class='cover-type-description'>{cover_type_info['description']}</p>", unsafe_allow_html=True)
            
            st.write(f"<b>Location:</b> {cover_type_info['location']}<br>", unsafe_allow_html=True)
            
            # Right side: Cover type image
            cover_type_image = Image.open(cover_type_info['image_path'])
            st.image(cover_type_image, caption=cover_type_info['name'], use_column_width=True)
            
            # Show falling leaves animation
            show_falling_leaves_animation()
        else:
            st.warning('Failed to predict cover type. Please check input values.')
    else:
        st.warning('Please enter valid input values.')
