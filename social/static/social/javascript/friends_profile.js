document.querySelector('#friend_request_button').addEventListener('click', () =>{
    const  csrftoken = Cookies.get('csrftoken');
    const request = new XMLHttpRequest();
    request.open('POST', '/request_friendship', true)
    request.setRequestHeader('X-CSRFToken', csrftoken);
    request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");

    request.onload = () => {
        const response = JSON.parse(request.responseText)
        console.log(response)
        document.querySelector('#friend_request_button').innerHTML = 'Request Sent';
        document.querySelector('#friend_request_button').setAttribute('disabled', 'true');
    }
    request.send(username);
})

// React components to render the post list
