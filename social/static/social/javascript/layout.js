
//logout logic
document.querySelector(".logout_a").addEventListener('click', (e) =>{

  e.preventDefault()
  document.querySelector('.logout_form').submit()
})


//displays all pending friend requests
const f_requests = new XMLHttpRequest()
f_requests.open('GET', '/get_f_requests', true)
f_requests.onload = () => {
  const requests = JSON.parse(f_requests.responseText)

  class Friendship_requests_div extends React.Component {
    constructor(props){
      super(props);
      this.state = {
       pending: requests.requests
      }
    }

    confirm_request(id) {
      const confirm = new XMLHttpRequest()
      const csrftoken = Cookies.get('csrftoken');
      
      confirm.open('POST', '/confirm_friend_request', true);
      confirm.setRequestHeader('X-CSRFToken', csrftoken);
      confirm.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
      confirm.onload = () => {
        const response = JSON.parse(confirm.responseText)
       
      }
      confirm.send(id)
    }

    ignore_request(id) {
      const ignore = new XMLHttpRequest();
      const csrftoken = Cookies.get('csrftoken');
      ignore.open('POST', '/ignore_friend_request', true);
      ignore.setRequestHeader('X-CSRFToken',csrftoken);
      ignore.setRequestHeader('Content-Type', "text/plain;charset=UTF-8");
      ignore.onload = () => {
        const response = JSON.parse(ignore.responseText)
        
      }
      ignore.send(id)
    }
    render() {
      return (
        <div>
          {this.state.pending.map(x => <Friendship_request
            key={x.id}
            img={x.sender_profile_pic}
            sender={x.sender}
            ignore={() => this.ignore_request(x.id)}
            confirm={() => this.confirm_request(x.id)}
            />
          )}
        </div>
      );
    }
  }


  ReactDOM.render(
    <Friendship_requests_div />, 
    document.getElementById("friendship_request_div")
  )
}
f_requests.send()


// displays all of the users friends
const friends = new XMLHttpRequest()
friends.open('GET', '/get_friends', true)
friends.onload = () => {
  const response = JSON.parse(friends.responseText)
  
  class Friends extends React.Component {
    constructor(props){
      super(props)
      this.state = {
        friends: response.response
      }
    }

    message(friend, profile_pic) {
      document.getElementById('message_box').style.display = 'block';
      
      // get friendship id for chatSocket
      const data = {sender: response.user, receiver: friend}
      const friendship = new XMLHttpRequest()
      const csrftoken = Cookies.get('csrftoken');
      friendship.open("POST", "/friendship_id", true)
      friendship.setRequestHeader('X-CSRFToken',csrftoken);
      friendship.setRequestHeader('Content-Type', "text/plain;charset=UTF-8");
      friendship.onload = () => {
        const answer = JSON.parse(friendship.responseText)
        const friendship_id = answer.id
        const messages_from_server = answer.messages
        console.log(answer.id)
        console.log(messages_from_server)

        // create messaging appnew ReconnectingWebSocket
      var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
      const chatSocket = new WebSocket(
        ws_scheme
        + '://'
        + window.location.host
        + '/wss/chat/'
        + friendship_id
        + '/'
      );
      console.log(chatSocket)
      

      class Message_app extends React.Component {
        constructor(props) {
          super(props)
          this.state = {
            messages: messages_from_server,
            receiver: friend,
            receiver_pic: profile_pic,
            user: response.user,
          }
        }
        
        componentDidMount() {
          chatSocket.onmessage = (e) => {
            const data = JSON.parse(e.data)
            console.log(data)
            this.setState({
              messages: [...this.state.messages, {'text': data.message, 'sender': data.sender, 'receiver':data.receiver, 'id': data.id}]
            })
          }  
        }
        
        sendMessage() {
          
          const message = document.querySelector("#message_text").value;
          //send the message via the chatsocket
          chatSocket.send(JSON.stringify({
            message: message,
            sender: this.state.user,
            receiver: this.state.receiver
          }));

          
          document.querySelector("#message_text").value = '';
        }

        close() {
          document.getElementById('message_box').style.display = 'none';
        }

        render() {
          return(
            <div>
            <Top_bar
              user={this.state.receiver}
              profile_pic={this.state.receiver_pic}
              close={() => this.close()}
            />
            <Message_screen 
              messages={this.state.messages}
              current_user={this.state.user}
            />
            <Compose_message 
              send={() => this.sendMessage()}
            />
            </div>
          )
        }
      }
      ReactDOM.render(
        <Message_app />, document.getElementById('message_box')

      )


      }
      friendship.send(JSON.stringify(data))

      
    }
    render() {
      return (
        <div>
          {this.state.friends.map(friend => <Friend_box
            key={friend.id}
            name={friend.user}
            profile_pic={friend.profile_pic}
            friend={friend.id}
            message={() => this.message(friend.user, friend.profile_pic)}
          />)}
        </div>
        )
      }
    }

  ReactDOM.render(
    <Friends />, 
    document.getElementById('friendship_div')
  )
}
friends.send()


//open message box
