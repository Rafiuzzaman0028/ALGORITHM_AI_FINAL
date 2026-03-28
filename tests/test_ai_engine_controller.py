from ai_engine.core.ai_engine import AIEngine


def test_ai_engine():

    engine = AIEngine()

#    prompt = "Build a travel website and create slides explaining the business"
#    prompt = "Design a mobile banking application interface"
#    prompt = "Create a startup pitch deck for an AI SaaS company"
#    prompt = "Research the impact of artificial intelligence on healthcare"
#    prompt = "Explain the difference between machine learning and deep learning"
#    prompt = "Build a python script that scrapes headlines from a news website and saves them to CSV"
#    prompt = "Build a python script that monitors a folder and logs new files"
#    prompt = "Build a python script that renames all files in a folder to lowercase"
#    prompt = "Build a python script that converts CSV to JSON"
#    prompt = "build a python script that downloads images from a website"
    prompt = "Explain the difference between machine learning and deep learning"
#    prompt = "Research the impact of artificial intelligence on healthcare and generate a detailed report"
#    prompt = "Build a python script that scrapes news headlines and saves them to a CSV. Split the logic into a main.py file and a scraper.py file."
#    prompt = "Build a node js website with a React frontend and Express backend. The website should have a homepage and an about page."
#    prompt = "Build a Python script that scrapes the latest news headlines from a website and saves them to a CSV file."
#  prompt = "Build a Python script that scrapes the latest news from a website and saves it to a CSV file."
#    prompt = "Build a python script that renames all files in a folder to lowercase"
#    prompt = "build a python script that reads a CSV file and calculates summary statistics"
#    prompt = "Create a startup pitch deck with 10 slides explaining an AI SaaS product."
    result = engine.run(prompt)

    print("\n--- FINAL RESULT ---\n")

    print(result)


if __name__ == "__main__":
    test_ai_engine()