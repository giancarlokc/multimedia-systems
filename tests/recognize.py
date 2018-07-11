import sys
import speech_recognition as sr
from os import path

# Get list of speech samples from command arguments
files = sys.argv[1:]

# Prepare recognizer
r = sr.Recognizer()

# For each file run all speech recognition methods and output recognized speech
for file in files:
    print('\n\n######################')
    print('Running tests for file: ' + file)

    # Load speech sample into memory
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), file)
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)

    # Recognize speech using Google Speech Recognition
    try:
        print("Google Speech Recognition Recognized:\n[\n" + r.recognize_google(audio) + '\n]')
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("\Could not request results from Google Speech Recognition service; {0}".format(e))

    # Recognize speech using Sphinx
    try:
        print("Sphinx Recognized:\n[\n" + r.recognize_sphinx(audio) + '\n]')
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

    # Recognize speech using Wit.ai
    WIT_AI_KEY = "JV35JQMK2Y3W6EWX3CBQTQWAVTQWJSSI"  # Wit.ai keys are 32-character uppercase alphanumeric strings
    try:
        print("Wit.ai Recognized:\n[\n" + r.recognize_wit(audio, key=WIT_AI_KEY, show_all=True)['_text'] + '\n]')
    except sr.UnknownValueError:
        print("Wit.ai could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Wit.ai service; {0}".format(e))

    # Recognize speech using Sphinx
    try:
        print("Sphinx Recognized:\n[\n" + r.recognize_sphinx(audio) + '\n]')
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

    # Recognize speech using Houndify
    HOUNDIFY_CLIENT_ID = "6V5XSPsUA3_10FoBNRBDlg=="
    HOUNDIFY_CLIENT_KEY = "QWUKG1FYB5nLrKsGq69aH5298Y1g-0f8pPbi2_jwm-kUct5SZueCBTXVAMooXB8DMwob9NbqReUj5JR_X852YQ=="
    try:
        print("Houndify Recognized:\n[\n", r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY, show_all=True) + '\n]')
    except sr.UnknownValueError:
        print("Houndify could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Houndify service; {0}".format(e))