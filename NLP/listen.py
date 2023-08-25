import speech_recognition as listen

def Listen():
    r = listen.Recognizer()

    with listen.Microphone() as source:
        print("Listening")
        r.pause_threshold = 1
        audio = r.listen(source,0,2)

    try:
        print("recognisation")
        query = r.recognize_google(audio, language='en-in')
        print(f"User: {query}")
    except:
        return ""
    
    query = str(query)
    return query.lower()

Listen()