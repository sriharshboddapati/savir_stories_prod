from azure.cosmos import CosmosClient, PartitionKey
from datetime import datetime
import os
import json
import streamlit as st
import openai
import base64
import uuid
from dotenv import load_dotenv
#import pdb; pdb.set_trace()
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")
DATABASE_NAME = 'savirstoriesmain'
CONTAINER_NAME = 'savir1'
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
database = client.create_database_if_not_exists(id=DATABASE_NAME)
container = database.create_container_if_not_exists(
        id=CONTAINER_NAME,
        partition_key=PartitionKey(path="/date"),
        offer_throughput=400
    )

def save_milestone(milestone_date, photo):
    # Structure the milestone entry
    milestone = {
        "date": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "image_path": None
    }

    # Save photo to the media folder
    if photo:
        filename = f"{milestone_date}.jpg"
        filepath = os.path.join("media", filename)
        with open(filepath, "wb") as f:
            f.write(photo.getbuffer())
        milestone["image_path"] = filepath

    # Make sure the data file exists
    os.makedirs("data", exist_ok=True)
    if not os.path.exists("data/milestones.json"):
        with open("data/milestones.json", "w") as f:
            json.dump([], f)

    # Read current data
    with open("data/milestones.json", "r+") as f:
        data = json.load(f)
        data.append(milestone)
        f.seek(0)
        json.dump(data, f, indent=2)

def show_milestones():
    # Load milestones from the data file
    if not os.path.exists("data/milestones.json"):
        return []

    with open("data/milestones.json", "r") as f:
        milestones = json.load(f)
    return milestones

    st.markdown('<div class="timeline">', unsafe_allow_html=True)
    for m in milestones:
        html = f"""
        <div class="timeline-item">
            <div class="timeline-content">
                <div class="timeline-date">{m['date']} –</div>
                <div>{m['description']}</div>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
        st.image(m["image_path"])  # This ensures the image loads correctly
    st.markdown('</div>', unsafe_allow_html=True)

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

#generate title from image meta data
def generate_title_from_photo(milestone):
    client = openai.OpenAI()
    base64_image = encode_image(milestone["image_path"])
    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "user",
                "content": [
                    { "type": "input_text", "text": "See this image and write exactly 1 line title about what this baby milestone is?" },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ],
    )
    #print(response.output_text)
    return response.output_text

def categorize_and_make_timeline(milestone):
    client = openai.OpenAI()
    # Path to your image
    #image_path = "path_to_your_image.jpg"
    # Getting the Base64 string
    base64_image = encode_image(milestone["image_path"])
    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "user",
                "content": [
                    { "type": "input_text", "text": "See this image and write exactly 2 lines about what this baby milestone is?" },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ],
    )
    #print(response.output_text)
    return response.output_text

def add_timeline_styles():
    st.markdown("""
    <style>
    .timeline {
        position: relative;
        margin: 0 auto;
        padding: 2rem 0;
        max-width: 800px;
    }
    .timeline::after {
        content: '';
        position: absolute;
        width: 4px;
        background-color: #E0E0E0;
        top: 0;
        bottom: 0;
        left: 50%;
        margin-left: -2px;
    }
    .timeline-item {
        position: relative;
        margin: 1rem 0;
        width: 50%;
        padding: 1rem;
    }
    .timeline-item.left {
        left: 0;
        text-align: right;
    }
    .timeline-item.right {
        left: 50%;
        text-align: left;
    }
    .timeline-item::before {
        content: '';
        position: absolute;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background-color: #4A90E2;
        top: 20px;
        z-index: 1;
    }
    .timeline-item.left::before {
        right: -8px;
    }
    .timeline-item.right::before {
        left: -8px;
    }
    .timeline-content {
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        position: relative;
    }
    .timeline-date {
        font-weight: bold;
        color: #4A4A4A;
        margin-bottom: 0.5rem;
    }
    .timeline-image {
        max-width: 100%;
        height: auto;
        border-radius: 6px;
        margin-top: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

def render_timeline(milestones):
    st.markdown('<div class="timeline">', unsafe_allow_html=True)
    for index, m in enumerate(milestones):
        alignment_class = "left" if index % 2 == 0 else "right"
        image_html = ""
        if m["image_path"]:
            # Encode the image to Base64
            base64_image = encode_image(m["image_path"])
            image_html = f'<img class="timeline-image" src="data:image/jpeg;base64,{base64_image}" alt="Milestone Image">'
        
        # Get the categorized description from categorize_and_make_timeline
        categorized_description = categorize_and_make_timeline(m)
        categorized_title = generate_title_from_photo(m)

        html = f"""
        <div class="timeline-item {alignment_class}">
            <div class="timeline-content">
                <div class="timeline-date">{m['date']} – </div>
                <div style="font-weight: bold; color: #333;">Description</div>
                <div style="font-style: italic; color: #6c757d;">{categorized_description}</div>
                <div style="font-weight: bold; color: #333;">Title</div>
                <div style="font-style: italic; color: #6c757d;">{categorized_title}</div>
                {image_html}
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def save_timeline():
    #Get current milestones from the JSON, store in a fast read database
    #Current flow is to store uploaded images into JSON, encode it and pass it to the API. 
    # Instead after initial upload store the title and description into database
    #Do not generate title and description on every render. Retrieve from DB and send only for new Images
    #step 1: Read from JSON file, see date updated, store older than datatime Now into DB 
    with open("data/milestones.json", "r") as f:
        milestones = json.load(f)
    #step 2: Store into DB
    for m in milestones:
        # Create a unique ID based on title and date
        m['id'] = str(uuid.uuid4()) 
        container.upsert_item(m)  # Insert or update the item
    print(f"Milestone saved: {m['date']}")

def show_timeline_from_db():
    query = "SELECT * FROM c"
    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    return items