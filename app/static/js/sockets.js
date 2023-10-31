const messages = document.getElementById('messageFeed');
const message = document.getElementById("message");
const messageBtn = document.getElementById("messageBtn");






message.addEventListener("keypress", function(event) {
  // If the user presses the "Enter" key on the keyboard
  if (event.key === "Enter") {
    // Cancel the default action, if needed
    event.preventDefault();
    // Trigger the button element with a click
    messageBtn.click();
  }
});


var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {
    var cnt = 0
    if (xhr.readyState == XMLHttpRequest.DONE) {
        const data = JSON.parse(xhr.responseText)
        console.log(data);
        console.log(`Статус ${xhr.status}`);
        console.log(`Получено байт ${xhr.response.length}`);
        const userName = xhr.getResponseHeader('User-InfoName');
        console.log(userName);
        console.log(`Статус ${xhr.status}`);
        window.senderUsername = userName
        data.forEach((mesStr) =>{
        createMessege(mesStr.name, mesStr.message, mesStr.timestamp, senderUsername)

    })
    }

}
xhr.open('POST', '/chat/messenger');
xhr.send();






const createMessege = (name, message, time, sender) =>{
    moment.locale('ru')
	if (name == sender) {
                content =`<div class="message my-message">`+
`<img alt="" class="img-circle medium-image" src="/static/img/def-ava.png">`+
` <div class="message-body"><div class="message-body-inner">`+
`<div class="message-info"><h4> ${name}</h4><h5> <i class="fa fa-clock-o" ></i>${moment(time).local().format()}</h5></div><hr>`+
            `<div class="message-text text-break">${message}</div>`+
           `</div>`+
        `</div>`+
            `<br>`+
        `</div>`;

	} else{
                content = `<div class="message info">`+
       ` <img alt="" class="img-circle medium-image" src="/static/img/def-ava.png">`+
        `<div class="message-body"><div class="message-info"><h4> ${name}</h4><h5> <i class="fa fa-clock-o"></i>${moment(time).local().format()}</h5></div><hr>`+
            `<div class="message-text text-break"> ${message}</div>`+
        `</div> <br>`+
    `</div>`;

  	}
	messages.innerHTML+=content;
    messages.scrollTop = messages.scrollHeight - messages.clientHeight;

};


const memberJoin = (name, message, time) =>{
	content =  `<div class="my-2 text-center">` +
    `<p>${name} ${message} ${time}</p>` +
    `</div>`;

    messages.innerHTML+=content
    messages.scrollTop = messages.scrollHeight - messages.clientHeight;

};




  const sendMessage = (senderUsername) => {
    console.log('sendMessage')
    console.log(message.value)
    if (message.value.trim() == "") return;
    sio.emit("message", { data: message.value });
    message.value = "";
  };




// POST запрос контента для чата
const sio = io();
console.log('Сокет подключился')






// sio.on("allMesseges", (data) => {
// 	console.log('allMessages')
// 	console.log(data)
// 	data.forEach((mesStr) =>{
// 		createMessege(mesStr.name, mesStr.message, mesStr.timestamp)
// 	})
// });

sio.on("connect", (data) => {
	console.log('connect');
	console.log(data.name);
	if (data){
		memberJoin(data.name, data.message, data.timestamp);
	}

});





sio.on('disconnect', (data) =>{
	console.log('disconnected');
        if (data.name){
        memberJoin(data.name, data.message, data.timestamp);
    }

});


sio.on("message", (data) => {
	console.log('message')
    console.log(senderUsername)
        if (data){
            createMessege(data.name, data.message, data.timestamp, senderUsername)
    }

})