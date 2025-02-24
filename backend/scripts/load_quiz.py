import json
from main.models import Quiz

def run():
    print("📂 JSON dosyası açılıyor...")
    with open("quiz_data.json", "r", encoding="utf-8") as file:
        quiz_list = json.load(file)
        print(f"📜 {len(quiz_list)} quiz bulundu!")

        for quiz_data in quiz_list:
            quiz, created = Quiz.objects.get_or_create(
                title=quiz_data["title"],
                defaults={
                    "description": quiz_data["description"],
                    "questions": quiz_data["questions"]
                }
            )
            if created:
                print(f"✅ Quiz Eklendi: {quiz.title}")
            else:
                print(f"⚠️ Quiz Zaten Var: {quiz.title}")

    print("✅ Quiz yükleme işlemi tamamlandı!")
