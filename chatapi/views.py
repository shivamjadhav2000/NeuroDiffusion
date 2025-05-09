from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from datetime import datetime
from .models import PromptHistory

HISTORY_JSON_PATH = os.path.join("media", "history.json")

def append_to_json_file(record):
    if os.path.exists(HISTORY_JSON_PATH):
        with open(HISTORY_JSON_PATH, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.insert(0, record)  # newest first
    with open(HISTORY_JSON_PATH, "w") as f:
        json.dump(data[:100], f, indent=2)  # keep latest 100 entries

@csrf_exempt
def generate_image_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        prompt = data.get("prompt", "")

        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        safe_prompt = "".join(c if c.isalnum() else "_" for c in prompt[:30])
        filename = f"{safe_prompt}_{timestamp}.png"
        save_path = os.path.join("media", filename)

        from stable_diff import generate_image
        generate_image(prompt, save_path)

        image_url = f"/media/{filename}"
        PromptHistory.objects.create(prompt=prompt, image_url=image_url)

        append_to_json_file({
            "prompt": prompt,
            "image_url": image_url,
            "timestamp": timestamp
        })

        return JsonResponse({"image_url": image_url})


@csrf_exempt
def get_history(request):
    # You can switch between DB and JSON here
    if os.path.exists(HISTORY_JSON_PATH):
        with open(HISTORY_JSON_PATH, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    return JsonResponse({"history": data})
