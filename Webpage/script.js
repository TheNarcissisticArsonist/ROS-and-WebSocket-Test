//Create a WebSocket object, on localhost (127.0.0.1) port 12345
//The ws:// is just like http:// or file://
var ws = new WebSocket("ws://127.0.0.1:12345/");

//Define a function to be executed when a message is received
ws.onmessage = function (event) {
    var message = event.data; //Store the message data to a variable
    document.body.innerHTML = message + "<br>" + document.body.innerHTML; //Add it to the top of the webpage
};