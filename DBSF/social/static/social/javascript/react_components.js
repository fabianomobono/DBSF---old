class Post_generator extends React.Component {
  componentDidMount() {
    console.log('Post generator is mounted')
  }
  componentWillUnmount() {
    console.log('post generator  did unMount')
  }
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
    result.push(<p key={i}>{new_text[i]}</p>)
  }
    return result 
}


function Post_author(props) { 
  const profile = 'profile/'
    return ( 
      <div className="author_info_div">
        <img className='post_author_pic' src={props.picture}/>
        <div className='post_info'>
          {props.current_user !== props.user ? (
            <a href={profile.concat(props.user)} className='post_author_user'>{props.user}</a>
            ) : <a href='/profile' className='post_author_user'>{props.user}</a>
          }                    
          <small className="post_date">{props.date}</small>
        </div>
      </div>
    )
}


class Post extends React.Component {

  componentWillUnmount() {
    console.log('COMPONENT WILL UNMOUNT')
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
        </div>
      )
    }
    else {
      return (
        <div id={this.props.post_id} className="post">
          <Post_author 
            current_user={this.props.current_user}
            picture={this.props.profile_pic}
            user={this.props.user}
            date={this.props.date}
          />
          <Post_body text={this.props.text}/>
        </div>
      )
    }
  }
}


function Friendship_request(props) {
  const profile = 'profile/'
  return (
    <div className='friendship_request'>
      <img src={props.img} className='friend_request_img'/>
      <a href={profile.concat(props.sender)} className="request_sender">{props.sender}</a>
      <button onClick={() => props.confirm()} className="accept_request_button btn btn-primary">&#10004;</button>
      <button onClick={() => props.ignore()} className="ignore_request_button btn btn-secondary">&#10006;</button> 
    </div>
  )
}


function Friend_box(props) {
  const profile = 'profile/'
  return (
    <div className='friend_box_div'>
      <img className='friend_img' src={props.profile_pic} />
      <a className="friend_link" href={profile.concat(props.name)}>{props.name}</a>
      <button onClick={() => props.message(props.name, props.profile_pic)} id={props.friend} className="btn btn-primary"><i className="fa fa-paper-plane"></i></button>
  </div>
  ) 
}


function Message(props) {
  return(
    <div className='message'>
      <p>Hello</p>
    </div>
  )
}


function Top_bar(props) {
  const profile = 'profile/'
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

function Message_screen(props) {
  return(
    <div className='message_screen'>
      <Message />
    </div>
  )
}

function Compose_message(props) {
  return(
    <div className='compose_message'>
      <div className='message_input_div'>
        <input type='text'></input>
      </div>
      <div className='send_message_div'>
        <button id='send_message_button'><i className="fa fa-paper-plane"></i></button>
      </div>
    </div>
  )
}