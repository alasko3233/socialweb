let loc = window.location;
console.log('je suis là');

let wsStar = 'ws://';
let input_message = $('#input-message');
let message_body = $('.msg_card_body');
let send_message_form = $('#send-message-form');
const USER_ID = $('#logged-in-user').val();
if (loc.protocol === 'https:') {
  wsStar = 'wss://';
}
let endpoint = wsStar + loc.host + loc.pathname;
var socket = new WebSocket(endpoint);

socket.onopen = async function(e){
    console.log('open', e);
    send_message_form.on('submit', function(e){
        e.preventDefault();
        let message = input_message.val();
        let send_to = get_active_other_user_id()
        let thread_id = get_active_thread_id()
      console.log('send_to : ', send_to);
      console.log('thread_id : ', thread_id);

        let data =  {
            'message':message,
            'sent_by': USER_ID,
            'sent_to':send_to,
            'thread_id': thread_id
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
    let sent_by_id = data['sent_by']
    let thread_id = data['thread_id']

    newMessage(message, sent_by_id,thread_id)
}
socket.onerror = async function(e){
    console.log('error', e);
}
socket.onclose = async function(e){
    console.log('close', e);
}



function newMessage(message, sent_by_id,thread_id ) {
    if ($.trim(message) === '') {
        return false;
    }
    let message_element;
	let chat_id = 'person' + thread_id
    console.log('bul : ',chat_id);
    if (sent_by_id == USER_ID){
        message_element = `
        <div class="bubble me">
          ${message}
          </div>

    `
    }else{
        message_element = `
        <div class="bubble you">
          ${message}
      </div>
    `
    }
let message_body = $('[data-chat="' + chat_id + '"] .msg_card_body')

message_body.append($(message_element))
message_body.animate({
    screenTop: $(document).height()
}, 500);
input_message.val(null);

}

///




// ///
// $('.msg').on('click', function (){
//   $('.msg .actiive').removeClass('active')
//   $(this).addClass('active')

//   // message wrappers
//   let chat_id = $(this).attr('chat-id')
//   $('.chat-area.is_active').removeClass('is_active')
//   $('.chat-area[chat-id="' + chat_id +'"]').addClass('is_active')

// })
 function get_active_other_user_id(){
   let other_user_id = $('.person.active').attr('other-user-id')
   other_user_id = $.trim(other_user_id)
   console.log('personne',other_user_id)
   return other_user_id
 }

 function get_active_thread_id(){
   let chat_id = $('.chat.active-chat').attr('data-chat')
   let thread_id = chat_id.replace('person', '')
   console.log('thread_id',thread_id)
   return thread_id
 }