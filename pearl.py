import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

message = "Default message"
open_conn = []

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Text Share</title>
    </head>
    <body>
        <textarea oninput="sendMessage(event)" id="messageText" autocomplete="off" style="width:97vw;height:97vh"></textarea>
        <script>
        
            fetch('http://10.109.46.76:8000/current_msg').then(response => {
            return response.json()
            }).then(data => {
            document.getElementById('messageText').value = data.msg;
            })

            var ws = new WebSocket("ws://10.109.46.76:8000/ws");
            ws.onmessage = function(event) {
                document.getElementById('messageText').value = event.data
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    # with open("message.txt") as f:
    #     message = f.read()


    # print(message)
    # print("html = ", html)

    return HTMLResponse(html)

@app.get("/current_msg")
async def current_content():
    with open("message.txt") as f:
        data = f.read()
    return {"msg":data}    

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global message, open_conn
    print(message)
    await websocket.accept()
    open_conn.append(websocket)
    while True:
        data = await websocket.receive_text()
        with open('message.txt','w') as f:
            f.write(data)

        with open('message.txt','r') as f:
            message = f.read()

        for connections in open_conn:
            await connections.send_text(str(message))

if __name__ == "__main__":
    uvicorn.run(app, host="10.109.46.76", port=8000)
