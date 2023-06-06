let loc = window.location
console.log('je suis la');

let wsStar =  'ws://'
let input_message = $('#input-message')
let message_body = $('.msg_card_body')
let send_message_form = $('#send-message-form')
if (loc.protocol === 'https'){
let wsStar =  'wss://'
} 
let endpoint = wsStar + loc.host + loc.pathname
var socket = new WebSocket(endpoint)

socket.onopen = async function(e){
    console.log('open', e);
    send_message_form.on('submit', function(e){
        e.preventDefault();
        let message = input_message.val();
        let data =  {
            'message':message,
        }
        data = JSON.stringify(data)
        socket.send(data);
        $(this)[0].reset()
    })
}

socket.onmessage = async function(e){
    console.log('message', e);
    let data = JSON.parse(e.data)
    let message = data['message']
    newMessage(message)
}
socket.onerror = async function(e){
    console.log('error', e);
}
socket.onclose = async function(e){
    console.log('close', e);
}



function newMessage(message) {
    if ($.trim(message) === '') {
        return false;
    }
    let message_element = `
    <div class="chat-msg owner">
    <div class="chat-msg-profile">
      <img
        class="chat-msg-img"
        src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/3364143/download+%282%29.png"
        alt=""
      />
      <div class="chat-msg-date">Message seen 2.50pm</div>
    </div>
    <div class="chat-msg-content">
      <div class="chat-msg-text">
      ${message}
      </div>
    </div>
  </div>
`
message_body.append($(message_element))
message_body.animate({
    scrollTop: $(document).height()
}, 500);
input_message.val(null);

}

