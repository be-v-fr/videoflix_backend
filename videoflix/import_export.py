from videos_app.admin import VideoResource

def export_videos():
    dataset = VideoResource.export()
    with open("content.json", "w") as file:
        file.write(dataset.json)