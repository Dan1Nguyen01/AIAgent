from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha



#speech engine initialisation
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) # 0 = male , 1 = female
activationWord = 'computer' 
#configure browser
#set the path
chrome_path ="C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

appId = 'GT4ETY-Q5PW84LWW3'
wolframClient = wolframalpha.Client(appId)
def speak(text, rate =120) :
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

def parseCommand():
    listener = sr.Recognizer()
    print ("Lising for a command")

    with sr.Microphone() as source:
        listener.pause_threshhold = 2
        input_speech = listener.listen(source)

    try:
        print("Regconizing speech...")
        query = listener.recognize_google(input_speech, language='en_gb')
        print (f'The input speech was: {query}')
    except Exception as exception:
        print('I did not quite catch that')
        speak('I did not quite catch that')
        print(exception)
        return 'None'
    return query


def search_wikipedia(query = ''):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print("No wikipedia result")
        return 'No result received'
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary

def listOrDict(var) :
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']

def search_wolframAlpha (query = ''):
    response = wolframClient.query(query)

    # @success : Wolfram Alpha was able to resolve the query
    # @numpods :Number of results returned
    # @pod : List of results. This can also contain subpods
    if response['@success'] == 'false':
        return 'Could not computer'
    #query resolved
    else: 
        result = ""
        #Question
        pod0 = response['pod'][0]

        pod1 = response['pod'][1]
        # May contain the answer, has the highest confidence value
        # If it's primary, or has the title of result or definition, then it's the official result
        if (('result')in pod1['@title'].lower()) or (pod1.get('@primary','false')== 'true') or ('definition'in pod1['@title'].lower()):
            #Get result
            result =  listOrDict(pod1['subpod'])
            #remove the bracketed section
            return result.split('(')[0]
        else:
            question = listOrDict(pod0['subpod'])
            #remove the bracketed section
            return result.split('(')[0]
            speak('Computation failed. Querying universal data')
            return search_wikipedia(question)
#main loop

if  __name__  == '__main__' :
    speak('All systems nomninal.')
    while True :
        #Parse a list
        query = parseCommand().lower().split()

        if query[0] == activationWord and len(query) >1:
            query.pop(0)

            #list commads
            if query[0] == 'say':
                if 'hello' in query:
                    speak('Greetings, all.')
                else:
                    query.pop(0)
                    speech = ' '.join(query)
                    speak(speech)

            #Navigation
                
            if query[0] == 'go' and query [1] == 'to' :
                speak("Opening...")
                query = ' '.join(query[2:])
                webbrowser.get('chrome').open_new(query)
            #Wikipedia
            if query[0] == 'wikipedia' :
                query = " ".join(query[1:])
                speak("Querying the universal databank.")
                speak(search_wikipedia(query))
            #wolfram alpha
            if query[0] =='compute' or query[0] == 'computer':
                query = ' '.join(query[1:])
                speak("Computings")
                try:
                    result = search_wolframAlpha(query)
                    speak(result)

                except:
                    speak("Unable to compute.")

            #Note taking
            if query [0] == 'note' :
                speak('Ready to record your note')
                newNote = parseCommand().lower()
                now = datetime.now().strftime('%Y-%m-%d-%h-%M-%S')
                with open('note_%s.txt' % now, 'w') as newFile:
                    newFile.write(newNote)
                speak('Note Written')

            if query[0] == "exit":
                speak('Goodbye')
                break

