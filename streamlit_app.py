import streamlit as st
import openai
# Uncomment the following lines to enable the API key input form
# Initialize
st.cache_data.clear()
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ""

openai.api_key = st.session_state.openai_api_key

if "text_error" not in st.session_state:
    st.session_state.text_error = None

if "text" not in st.session_state:
    st.session_state.text = None

if "n_requests" not in st.session_state:
    st.session_state.n_requests = 0

with st.sidebar:
    api_key_form = st.form(key="api_key_form")
    openai_api_key = api_key_form.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    api_key_form_submitted = api_key_form.form_submit_button("Submit")

    if api_key_form_submitted:
        st.session_state.openai_api_key = openai_api_key
        openai.api_key = st.session_state.openai_api_key
        st.success("Your OpenAI API key was saved successfully!")


def generate_cuisine_recommendation(cuisine, meal_type, flavor_preferred):
    # Customize the prompt based on your requirements
    prompt = f"I feel like having {meal_type} {cuisine} food with a {flavor_preferred} flavor. What dish do you recommend?. and write 3 notes for me why I chose this cuisine for this {meal_type}."

    # Call OpenAI API for recommendation
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.7,
        top_p=0.7,
        max_tokens=450,
        messages=[
            {"role": "system", "content": "You are a cuisine recommendation bot. You will help users find the best dishes for their meal."},
            {"role": "user", "content": f"You will help users find the best dishes and make notes from the context:{prompt}."},
        ]
    )
    
    return response.choices[0].message.content

st.title("Dish For Today")
st.markdown("<h2 style = 'font-size: 1.8rem'>🍜 Dish For Today 🍚</h2>",unsafe_allow_html=True)




# User input
meal_type = st.text_input("Meal Type:")
cuisune = st.text_input("Cuisine:")
flavor_preferred = st.text_input("Flavor:")

# Generate recommendation
if st.button("Generate Recommendation"):
    if meal_type and cuisune and flavor_preferred:
        recommendation = generate_cuisine_recommendation(
            meal_type, cuisune, flavor_preferred
        )
        st.success(f"Recommended Dish: {recommendation}")
    else:
        st.warning("Please fill in all fields.")

