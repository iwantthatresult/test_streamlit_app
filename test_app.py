# Importing the required libraries
import streamlit as st
import pandas as pd
import os
import requests
from PIL import Image

# Defining the placeholders for the different sections of the app
placeholder_for_prompt = st.empty()
placeholder_for_text = st.empty()
placeholder_for_image = st.empty()
placeholder_for_past_posts = st.empty()

# Setting up the Streamlit app
st.set_page_config(page_title="LinkedIn Post Generator")
st.title("LinkedIn Post Generator")

# TODO: Add functionality to the different app components

# Defining the form where the user inputs the prompt for the LinkedIn post
prompt = placeholder_for_prompt.text_input("Enter a prompt for the LinkedIn post:")

# Generating the text for the post based on the prompt using GPT-3
if prompt:
    # TODO: Use OpenAI's GPT-3 to generate the text for the LinkedIn post
    generated_text = "This is the generated text for the LinkedIn post based on the prompt provided."
    
    # Displaying the generated text
    placeholder_for_text.write(generated_text)
    
    # Defining the form where the user inputs their email to receive the generated post
    email = placeholder_for_text.text_input("Enter your email to receive the generated LinkedIn post:")

    # TODO: Add functionality to send the generated post via email when the submit button is clicked.
    submit_button = placeholder_for_text.button("Submit")


# Importing the necessary modules for generating the image
import requests
import json

# Defining a function that generates an image using Stable Diffusion
def generate_image(prompt):
    # Defining the Stable Diffusion API endpoint and header
    url = "https://api.stdlib.com/diffusion-ai@2.0.0/image-generator/?"
    querystring = {"prompt": prompt}
    headers = {
        "Content-Type": "application/json"
    }
    
    # Sending the request to the API and extracting the image URL from the response
    response = requests.request("GET", url, headers=headers, params=querystring)
    image_url = json.loads(response.text)['link']
    
    return image_url

# Adding the image generation function to our Streamlit app
if prompt:
    # Generating the image
    image_url = generate_image(prompt)
    
    # Displaying the image and giving the user the option to attach it to their post
    placeholder_for_image.image(image_url)
    attach_image = placeholder_for_text.checkbox("Attach image to LinkedIn post")


# Importing the necessary modules for generating the post
import openai

# Defining the function that generates the LinkedIn post
def generate_post(prompt):
    # Setting up the OpenAI API
    openai.api_key = "YOUR_API_KEY_HERE"
    model_engine = "text-davinci-002"
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1500,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text.strip()
    
    return message

# Adding the post generation function to our Streamlit app
if prompt:
    # Generating the post
    generated_post = generate_post(prompt)
    
    # Displaying the generated post and giving the user the option to save it
    placeholder_for_text.write(generated_post)
    save_post = placeholder_for_text.checkbox("Save LinkedIn post")


# Adding a section to allow the user to input a prompt for their LinkedIn post
prompt = st.text_input("Enter a short prompt or message for your LinkedIn post:")

# Adding a placeholder to display the generated post
placeholder_for_text = st.empty()

# Adding functionality to generate the post when the user submits their prompt
if st.button("Generate LinkedIn post"):
    # Generating the post
    generated_post = generate_post(prompt)
    
    # Displaying the generated post and giving the user the option to save it
    placeholder_for_text.write(generated_post)
    save_post = placeholder_for_text.checkbox("Save LinkedIn post")


# Adding a section to allow the user to upload an image for their LinkedIn post
image_file = st.file_uploader("Upload an image for your LinkedIn post (JPG or PNG)", type=["jpg", "png"])

# Adding a placeholder to display the generated image
placeholder_for_image = st.empty()

# Adding functionality to generate the image when the user uploads it
if st.button("Generate LinkedIn post image") and image_file is not None:
    # Creating a temporary file to store the uploaded image
    with open("temp_image", "wb") as f:
        f.write(image_file.read())
        
    # Calling the script that will generate the image using Stable Diffusion
    os.system("python generate_image.py --prompt \"{}\" --infile temp_image --outfile generated_image.png".format(prompt))
    
    # Displaying the generated image and giving the user the option to save it
    placeholder_for_image.image("generated_image.png")
    save_image = placeholder_for_image.checkbox("Save LinkedIn post image")


# Adding code to create and display the DataFrame of generated LinkedIn posts
if 'generated_posts' not in st.session_state:
    st.session_state['generated_posts'] = pd.DataFrame(columns=['Date', 'Prompt', 'Post', 'Image filename'])

st.write(st.session_state['generated_posts'])

# Adding code to append each new post to the DataFrame
if st.button("Generate LinkedIn post"):
    # Generating the LinkedIn post
    generated_post = message_agent(1, prompt)
    
    # Saving the generated image with a unique filename
    if image_file is not None:
        image_filename = "generated_images/{}-{}.png".format(prompt,datetime.now().strftime("%Y%m%d%H%M%S"))
        with open("generated_images/temp_image.png", "wb") as f:
            f.write(image_file.read())
        os.rename("generated_images/temp_image.png", image_filename)
    else:
        image_filename = None
        
    # Adding the post and associated metadata to the DataFrame
    st.session_state['generated_posts'] = st.session_state['generated_posts'].append({'Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'Prompt': prompt, 'Post': generated_post, 'Image filename': image_filename}, ignore_index=True)
# Adding code to generate a LinkedIn post with attached image
if st.button('Generate LinkedIn post'):
    # Generating the LinkedIn post
    generated_post = message_agent(<your_agent_key>, prompt)['message']
    # Generating and attaching the image
     image_file = generate_image(prompt)['image']
     # If an image was generated, attach it to the LinkedIn post
     if image_file is not None:
        image_filename = f'generated_images/{prompt}.jpg'
        with open(image_filename, 'wb') as f:
            f.write(image_file)
            # Attaching the image to the LinkedIn post
            generated_post += f'\\n\\n![a generated image]({image_filename})'
        # Adding the post and associated metadata to the DataFrame
        if 'generated_posts' not in st.session_state:
            st.session_state['generated_posts'] = pd.DataFrame(columns=['Date', 'Prompt', 'Post', 'Image filename'])\
            st.session_state['generated_posts'] = st.session_state['generated_posts'].append({'Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Prompt': prompt, 'Post': generated_post, 'Image filename': image_filename}, ignore_index=True)
            # Previewing the generated LinkedIn post
            st.write(generated_post)
        
# Adding code to send generated LinkedIn post to email
# Define the function that sends the email
def send_email(post, email_address):
    try:
        # Setting up the email message
        message = EmailMessage()
        message['To'] = email_address
        message['Subject'] = 'Generated LinkedIn Post'
        message.set_content(post)
        # Adding the attached image to the email message
        with open(image_filename, 'rb') as f:
            image_data = f.read()
            message.add_attachment(image_data, maintype='image', subtype=imghdr.what(None, image_data), filename=os.path.basename(image_filename))
            # Sending the email message
            with smtplib.SMTP('smtp.gmail.com', port=587) as smtp_server:
                smtp_server.ehlo()
                smtp_server.starttls()
                smtp_server.login(<your_email_address>, <your_email_password>)
                smtp_server.send_message(message)   
                st.write(f'Email sent to {email_address}!')
    except Exception as e:
        st.write(f'Error sending email to {email_address}: {e}')
        # Adding the email address form and callback function
    
email_address = st.text_input('Enter your email address')
if st.button('Send email') and email_address != '':
    send_email(generated_post, email_address)    
# Adding code to save generated LinkedIn post
# Define the function that saves the data to a CSV file
def save_post_to_csv(post, filename):
        try:
            # Creating a pandas DataFrame with the generated post data
            data = {'post': [post], 'image_filename': [image_filename]}
            df = pd.DataFrame(data)
        # Saving DataFrame to CSV
        df.to_csv(filename, index=False)
        st.write(f'Post saved to {filename}!')
        except Exception as e:
            st.write(f'Error saving post to {filename}: {e}')
# Adding the save button
if st.button('Save post'):
    filename = st.text_input('Enter the filename to save the post to (without extension)')
    if filename != '':
        filename += '.csv'
        save_post_to_csv(generated_post, filename)