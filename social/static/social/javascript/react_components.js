class Post_generator extends React.Component {
 
  render() {
    return (
    <div className="new_post_div">
    <img className="post_author_pic" src={this.props.picture} alt="profile_pic" />
    <div>
      <textarea name="new_post_text" id="new_post_text" placeholder="Say something to your close friends"></textarea>
      <button onClick={() => this.props.onClick()} className='btn btn-primary'>&#10002;</button>
    </div>
  </div>
    )
  }
}


function Post_body(props) {
  var text = props.text
  let i = 0
  const new_text = text.split('\n')
  let result = []
  for(let i = 0; i < new_text.length; i++) {
    result.push(<p key={i} className='post_body'>{new_text[i]}</p>)
  }
    return result 
}


function Post_author(props) { 
  const profile = '/profile/'
    return ( 
      <div className="author_info_div">
        <img className='post_author_pic' src={props.picture}/>
        <div className='post_info'>
          {props.current_user !== props.user ? (
            <a href={profile.concat(props.user)} className='post_author_user'>{props.user}</a>
            ) : <a href='/profile' className='post_author_user'>{props.user}</a>
          }    
          <p className='post_date'>{props.date}</p>
        </div>
      </div>
    )
  
 
    
}


function Comment(props) {
  const profile = '/profile'
  return (
    <div className='comment'>
      <img className='image_in_comment' src={props.profile_pic} />
      <a href={profile} className="user_link_in_comment"> {props.commentator} </a>
      {props.text}
    </div>
  )
}


class CreateComment extends React.Component {
  
  render() {
    return(
      <div className='create_comment'>
        <input  type='text' placeholder='Comment...' />
        <button onClick={(e) => this.props.add_comment(e.target.previousSibling.value)}>Comment</button>
      </div> 
    )
  }
}


class CommentSection extends React.Component {
  render() {
    return(
      <div className='comment_section'>
        {this.props.comments.map(comment => <Comment 
          commentator={comment.commentator}
          profile_pic={comment.profile_pic}
          text={comment.text}
          key={comment.id}
        />)}
        
        <CreateComment
          add_comment={this.props.add_comment} 
        />
      </div>
    )
  }
}


class Feeling extends React.Component {
  render(){
    return (
      <div className='feeling'>
        <div className='like'>👍</div>
        <div className='dislike'>👎</div>
      </div>
    )
  }
}


class Post extends React.Component {
  constructor(props){
    super(props)
    this.state = {
      comments: this.props.comments,
      current_user: this.props.current_user,
      current_user_profile_pic: this.props.current_user_profile_pic,
      id: this.props.id
    }
    this.add_comment = this.add_comment.bind(this)
  }

  
  
  add_comment(text){
    const data = {'post_id': this.state.id, 'commentator': this.state.current_user, 'text': text}
    const csrftoken = Cookies.get('csrftoken');
    const request = new XMLHttpRequest()
    request.open('POST', '/comment', true)
    request.setRequestHeader('X-CSRFToken', csrftoken);
    request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
    request.onload = () => {
      const response = JSON.parse(request.responseText)
      console.log(response)
    }
    request.send(JSON.stringify(data))
    this.setState({
      comments: [...this.state.comments,{text: text, commentator: this.state.current_user, profile_pic: this.state.current_user_profile_pic}]
    })
    
  }

  render() {
    if (this.props.current_user === this.props.user){
      return (
        <div id={this.props.post_id} className="post">
          <button onClick={() => this.props.onClick()} className="delete_post_button">&#10006;</button>
          <Post_author 
            current_user={this.props.current_user}
            picture={this.props.profile_pic}
            user={this.props.user}
            date={this.props.date}
          />
          <Post_body text={this.props.text}/>
          <Feeling />
          <CommentSection
            comments={this.state.comments}
            add_comment={this.add_comment}  
          />
        </div>
      )
    }
    else {
      return (
        <div id={this.props.post_id} className="post">
          <button onClick={() => this.props.onClick()} className="delete_post_button">&#10006;</button>
          <Post_author 
            current_user={this.props.current_user}
            picture={this.props.profile_pic}
            user={this.props.user}
            date={this.props.date}
          />
          <Post_body text={this.props.text}/>
          <Feeling />
          <CommentSection
            add_comment={this.add_comment}
            comments={this.state.comments}
          />
        </div>
      )
    }
  }
}


function Friendship_request(props) {
  const profile = '/profile/'
  return (
    <div id={props.id} className='friendship_request'>
      <img src={props.img} className='friend_request_img'/>
      
      <a href={profile.concat(props.sender)} className="request_sender">{props.sender}</a>
      <button onClick={() => props.confirm()} className="accept_request_button">&#10004;</button>
      <button onClick={() => props.ignore()} className="ignore_request_button">&#10006;</button> 
    </div>
  )
}


function Friend_box(props) {
  const profile = '/profile/'
  const date = new Date(props.last_contact)
  var now = new Date()
  now -= date
  console.log(now, props.name) 
  if (now > 10000 || isNaN(now)){
    return (
      <div className='friend_box_div'>
        <img className='friend_img' src={props.profile_pic} />
        <div className='DBSF_interaction'>
          <a className="friend_link" href={profile.concat(props.name)}>{props.name}</a>
          <p className='last_contacted'>Last contact:</p>
          {isNaN(now) ? <p className='last_contacted'>{props.last_contact}</p>:<p className='last_contacted'>{props.last_contact.substring(0, props.last_contact.length - 9)}</p>}
        </div>
        <button onClick={() => props.message(props.name, props.profile_pic)} id={props.friend} className="btn btn-primary"><i className="fa fa-paper-plane"></i></button>
    </div>
    ) 
  }
  else {
    return (
      <div className='friend_box_div'>
        <img className='friend_img' src={props.profile_pic} />
        <div className='interaction'>
          <a className="friend_link" href={profile.concat(props.name)}>{props.name}</a>
          <p className='last_contacted'>Last contact:</p>
          <p className='last_contacted'>{props.last_contact.substring(0, props.last_contact.length -9)}</p>
        </div>
        <button onClick={() => props.message(props.name, props.profile_pic)} id={props.friend} className="btn btn-primary"><i className="fa fa-paper-plane"></i></button>
    </div>
    ) 
  }
}
  


function Message(props) {
  if (props.current_user === props.sender){
    return (
      <div className='user_message_div'>
        <p className='user_message'>{props.text}</p>
      </div>
    )
  }
  else {
    return (
      <div className='receiver_message_div'>
        <p className='receiver_message'>{props.text}</p>
      </div>
    )
  }
 
   
}

 
function Top_bar(props) {
  const profile = '/profile/'
  return(
    <div className='top_bar'>
      <div className='user_info_div'>
        <img className='profile_pic_in_top_bar' src={props.profile_pic}/>
        <a href={profile.concat(props.user)}>{props.user}</a>
      </div>
      <button onClick={() => props.close()}>&#x2716;</button>
    </div>
  )
}


class  Message_screen extends React.Component {
  
  componentDidUpdate(){
    var screen = document.getElementById('message_screen')
    screen.scrollTop = screen.scrollHeight;
  }

  componentDidMount(){
    var screen = document.getElementById('message_screen')
    screen.scrollTop = screen.scrollHeight;
  }

  render() {
    return(
      <div id='message_screen' className='message_screen'>
        {this.props.messages.map(message =>
          <Message 
            key={message.id}
            text={message.text}
            sender={message.sender}
            receiver={message.receiver}
            current_user={this.props.current_user}
          />
          )}
      </div>
    )
  }
}


function Compose_message(props) {
  return(
    <div className='compose_message'>
      <div className='message_input_div'>
        <input id='message_text' type='text'></input>
      </div>
      <div className='send_message_div'>
        <button onClick={() => props.send()} id='send_message_button'><i className="fa fa-paper-plane"></i></button>
      </div>
    </div>
  )
}