from g4f.client import Client
from g4f.Provider import Liaobots
import g4f.debug

def GetRandomTwit():
    g4f.debug.logging = True

    client = Client(
        provider=Liaobots
    )
    
    response = client.chat.completions.create(
        model="",
        messages=[{"role": "user", "content": "Write a random post for Twitter without any emoji"}],
    )
    
    return response.choices[0].message.content