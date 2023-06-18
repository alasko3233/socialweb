// Récupérer l'objet de localisation
let loc = window.location;

// Afficher un message dans la console
console.log('je suis là');

// Préfixe du protocole pour la connexion WebSocket
let wsStar = 'ws://';

// Sélectionner des éléments du DOM
let input_message = $('#input-message');
let message_body = $('.msg_card_body');
let send_message_form = $('#send-message-form');

// Récupérer l'ID de l'utilisateur connecté
const USER_ID = $('#logged-in-user').val();

// Vérifier si le protocole est HTTPS et mettre à jour le préfixe du protocole si nécessaire
if (loc.protocol === 'https:') {
  wsStar = 'wss://';
}

// Construire l'URL de l'endpoint WebSocket
let endpoint = wsStar + loc.host + loc.pathname;

// Créer une instance de WebSocket avec l'endpoint
var socket = new WebSocket(endpoint);

// Gérer l'événement d'ouverture de la connexion WebSocket
socket.onopen = async function(e){
    console.log('open', e);

    // Gérer l'événement de soumission du formulaire d'envoi de message
    send_message_form.on('submit', function(e){
        e.preventDefault();
        let message = input_message.val();
        let send_to = get_active_other_user_id();
        let thread_id = get_active_thread_id();
        console.log('send_to : ', send_to);
        console.log('thread_id : ', thread_id);

        // Construire l'objet de données à envoyer via WebSocket
        let data =  {
            'message': message,
            'sent_by': USER_ID,
            'sent_to': send_to,
            'thread_id': thread_id
        };

        // Convertir l'objet de données en JSON
        data = JSON.stringify(data);

        // Envoyer les données via WebSocket
        socket.send(data);

        // Réinitialiser le formulaire
        $(this)[0].reset();
    });
};

// Gérer l'événement de réception d'un message via WebSocket
socket.onmessage = async function(e){
    console.log('message', e);

    // Parser les données JSON reçues
    let data = JSON.parse(e.data);
    let message = data['message'];
    let sent_by_id = data['sent_by'];
    let thread_id = data['thread_id'];

    // Appeler la fonction newMessage pour traiter le nouveau message reçu
    newMessage(message, sent_by_id, thread_id);
};

// Gérer l'événement d'erreur de la connexion WebSocket
socket.onerror = async function(e){
    console.log('error', e);
};

// Gérer l'événement de fermeture de la connexion WebSocket
socket.onclose = async function(e){
    console.log('close', e);
};

// Fonction pour traiter un nouveau message
function newMessage(message, sent_by_id, thread_id) {
    // Vérifier si le message est vide
    if ($.trim(message) === '') {
        return false;
    }

    let message_element;
    let chat_id = 'person' + thread_id;
    console.log('bul : ', chat_id);

    // Construire l'élément HTML du message en fonction de l'auteur du message
    if (sent_by_id == USER_ID) {
        message_element = `
        <div class="bubble me">
          ${message}
        </div>
    `;
    } else {
        message_element = `
        <div class="bubble you">
          ${message}
        </div>
    `;
    }

    // Sélectionner le corps du chat correspondant au thread
    let message_body = $('[data-chat="' + chat_id + '"] .msg_card_body');

    // Ajouter l'élément du message au corps du chat
    message_body.append($(message_element));

    // Animer le défilement vers le bas pour afficher le nouveau message
    message_body.animate({
        scrollTop: $(document).height()
    }, 500);

    // Réinitialiser le champ de saisie du message
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
// Fonction pour obtenir l'ID de l'autre utilisateur actif
function get_active_other_user_id(){
    // Récupérer l'attribut 'other-user-id' de l'élément '.person.active'
    let other_user_id = $('.person.active').attr('other-user-id');
    
    // Supprimer les espaces en début et en fin de chaîne
    other_user_id = $.trim(other_user_id);
    
    // Afficher l'ID de l'autre utilisateur dans la console
    console.log('personne', other_user_id);
    
    // Retourner l'ID de l'autre utilisateur
    return other_user_id;
 }
 
 // Fonction pour obtenir l'ID du thread actif
 function get_active_thread_id(){
    // Récupérer l'attribut 'data-chat' de l'élément '.chat.active-chat'
    let chat_id = $('.chat.active-chat').attr('data-chat');
    
    // Remplacer la partie 'person' par une chaîne vide pour obtenir l'ID du thread
    let thread_id = chat_id.replace('person', '');
    
    // Afficher l'ID du thread dans la console
    console.log('thread_id', thread_id);
     
    // Retourner l'ID du thread
    return thread_id;
 }
 