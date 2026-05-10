import socket
import threading
import datetime
import random
import webbrowser
import urllib.parse

task_list = []

def get_time():
    now = datetime.datetime.now()
    return now.strftime("The current time is %H:%M.")

def google_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)
    return f"Searching for {query} on Google."

def get_weather(city):
    search_query = f"{city} weather"
    webbrowser.open(f"https://www.google.com/search?q={search_query}")
    return f"Showing weather for {city}."

def get_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't skeletons fight each other? They don't have the guts.",
        "What do you get if you cross a snowman and a vampire? Frostbite.",
        "Why was the math book sad? Because it had too many problems."
    ]
    return random.choice(jokes)

def get_fun_fact():
    facts = [
        "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still edible.",
        "A day on Venus is longer than a year on Venus.",
        "Bananas are berries, but strawberries aren't.",
        "There are more stars in the universe than grains of sand on all the world's beaches.",
        "A leap year is a year that has one extra day: February 29."
    ]
    return random.choice(facts)

def play_youtube(query=""):
    if query:
        search_query = query.replace("play", "").strip()
        youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
        webbrowser.open(youtube_url)
        return f"Playing {search_query} on YouTube."
    else:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."

def add_task(task):
    task_list.append(task)
    return f"Task '{task}' added to your list."

def view_tasks():
    if not task_list:
        return "Your task list is empty."
    return "Here are your tasks:\n" + "\n".join(f"{idx+1}. {task}" for idx, task in enumerate(task_list))

def remove_task(task_number):
    try:
        task_number = int(task_number)
        if 1 <= task_number <= len(task_list):
            removed_task = task_list.pop(task_number - 1)
            return f"Task '{removed_task}' removed from your list."
        else:
            return "Invalid task number."
    except ValueError:
        return "Please enter a valid number."

def calculate(expression):
    try:
        result = eval(expression)
        return f"The result is {result}"
    except Exception as e:
        return f"Error in calculation: {e}"

def translate(text, target_language="en"):
    encoded_text = urllib.parse.quote(text)
    translate_url = f"https://translate.google.com/?sl=auto&tl={target_language}&text={encoded_text}&op=translate"
    webbrowser.open(translate_url)
    return f"Translating '{text}' to {target_language}. Opening Google Translate."

def handle_command(command):
    if "time" in command:
        return get_time()
    elif "search" in command:
        query = command.replace("search", "").strip()
        return google_search(query)
    elif "weather" in command:
        city = command.replace("weather", "").strip()
        return get_weather(city)
    elif "add task" in command:
        task = command.replace("add task", "").strip()
        return add_task(task)
    elif "youtube" in command:
        query = command.replace("youtube", "").strip()
        return play_youtube(query)
    elif "view tasks" in command:
        return view_tasks()
    elif "remove task" in command:
        task_number = command.replace("remove task", "").strip()
        return remove_task(task_number)
    elif "joke" in command:
        return get_joke()
    elif "fun fact" in command:
        return get_fun_fact()
    elif "calculate" in command:
        expression = command.replace("calculate", "").strip()
        return calculate(expression)
    elif "translate" in command:
        parts = command.split("to")
        if len(parts) >= 2:
            text = parts[0].replace("translate", "").strip()
            target_language = parts[1].strip()
            return translate(text, target_language)
        else:
            return "Please specify the language to translate to, like 'translate hello to fr' for French."
    elif "exit" in command:
        return "Exiting. Have a great day!"
    else:
        return "Sorry, I don't know that command."

def client_handler(client_socket):
    while True:
        command = client_socket.recv(1024).decode()
        if not command or command.lower() == "exit":
            client_socket.send("Exiting. Have a great day!".encode())
            break
        
        response = handle_command(command)
        client_socket.send(response.encode())
    
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 12345))
    server.listen(5)
    print("Server started and listening for connections...")
    
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    main()







