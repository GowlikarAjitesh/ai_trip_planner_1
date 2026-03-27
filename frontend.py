import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/generate_itinerary"

def generate_itinerary(destination, startDate, endDate, travelers, interests):
    payload = {
        "destination": destination,
        "startDate": startDate,
        "endDate": endDate,
        "travelers": travelers,
        "interests": interests
    }
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            result = f"🧾 **Trip Summary:** {data['summary']}\n\n"
            for day in data["dailyPlans"]:
                result += f"### 🗓️ Day {day['day']} - {day['theme']} ({day['date']})\n"
                for act in day["activities"]:
                    result += f"- 🕒 {act['time']} — {act['description']}\n"
            return result
        else:
            return f"❌ Error: {response.text}"
    except Exception as e:
        return f"⚠️ Connection error: {e}"

ui = gr.Interface(
    fn=generate_itinerary,
    inputs=[
        gr.Textbox(label="Destination"),
        gr.Textbox(label="Start Date (YYYY-MM-DD)"),
        gr.Textbox(label="End Date (YYYY-MM-DD)"),
        gr.Textbox(label="Travelers"),
        gr.Textbox(label="Interests"),
    ],
    outputs="markdown",
    title="🌍 AI Travel Itinerary Generator",
    description="Enter your trip details to get an AI-generated itinerary using LangChain + Gemini"
)

ui.launch(share=True)