import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        #Read  the file and convert it to into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type, # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
def click_image_setup(img_file_buffer):
    # Check if image has been clicked
    if img_file_buffer is not None:
    # To read image file buffer as bytes:
        bytes_data = img_file_buffer.getvalue()
        image_parts = [
                {
                    "mime_type": img_file_buffer.type, # Get the mime type of the uploaded file
                    "data": bytes_data
                }
            ]
        return image_parts
    else:
        raise FileNotFoundError("No Picture clicked")

    
## Initialize our streamlit app frontend
st.set_page_config(page_title="Calories Advisor App")
st.header("Calories Advisor App")

# Use st.image directly for camera input
img_file_buffer = st.camera_input("Take a picture")

# Use st.file uploader to upload a file
uploaded_file = st.file_uploader("Choose an image....", type = ["jpg", "jpeg", "png"])
image = None
image_data = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
    image_data = input_image_setup(uploaded_file)
elif img_file_buffer is not None:
    image = Image.open(img_file_buffer)
    st.image(image, caption = "Uploaded Image.", use_column_width=True)
    image_data = click_image_setup(img_file_buffer)

submit = st.button("Tell me about the total calories")

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 : no of calories
               2. Item 2 : no of calories
               ----
               ----
        Finally you can also mention whether the food us healthy or not and also mention the
        percentage split of the ratio of carbohydrates ,fats ,vitamin ,sugar ,protein and  
        other important things required in our diet
        """

# Check if the button is clicked and image_data is not None
if submit and image_data is not None:
    # Execute the following block only if no exception is raised and image_data is not None
    response = get_gemini_response(input_prompt, image_data)
    st.header("The Response is")
    st.write(response)
elif submit and image_data is None:
    # Print an error message if no input is provided
    st.error("No input provided. Upload an image or take a picture.")