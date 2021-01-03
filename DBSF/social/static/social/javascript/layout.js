
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

      class Message_app extends React.Component {
        constructor(props) {
          super(props)
          this.state = {
            messages: [],
            receiver: friend,
            receiver_pic: profile_pic,
            user: response.user,
          }
        }
        
        componentDidMount() {
          const receiver = this.state.receiver
          const sender = this.state.user
          const chatSocket = new WebSocket(
             'ws://'
            + window.location.host
            + '/ws/chat/'
            + sender
            + '/'
            + receiver
            + '/'
          );
         
        }
        sendMessage() {
          const message = document.querySelector("#message_text").value;
          this.setState({
            messages: [...this.state.messages, {'message': message }]
          })
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
