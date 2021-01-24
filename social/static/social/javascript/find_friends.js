// function add friend
function add_friend(button){
    var name = button.getAttribute('data-name')  
    request = new XMLHttpRequest()
    request.open("POST" ,'/request_friendship', true )
    const csrftoken = Cookies.get('csrftoken');
    request.setRequestHeader('X-CSRFToken', csrftoken);
    request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
    request.onload = () => {
        const response = JSON.parse(request.responseText)
        console.log(response)
        button.innerHTML = 'Pending'
        button.setAttribute('disabled', 'true')
    }
    request.send(name)
}
    

    //figure out which button was pressed

    // send XML request

    // when it comes back change the button

// send the request


function unfriend(button) {
    var name = button.getAttribute('data-name')  
    request = new XMLHttpRequest()
    request.open("POST" ,'/unfriend', true )
    const csrftoken = Cookies.get('csrftoken');
    request.setRequestHeader('X-CSRFToken', csrftoken);
    request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
    request.onload = () => {
        const response = JSON.parse(request.responseText)
        console.log(response)
        button.innerHTML = '<i class="fa fa-user-plus"></i>'
        button.setAttribute('onclick', 'add_friend(this)')
    }
    request.send(name)
}