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
  if(props.current_user !== props.user){
    return ( 
      <div className="author_info_div">
        <img className='post_author_pic' src={props.picture}/>
        <div className='post_info'>
          <a href={profile.concat(props.user)} className='post_author_user'>{props.user}</a>           
          <small className="post_date">{props.date}</small>
        </div>
      </div>
    )
  }
  else {
    return (
      <div className="author_info_div">
        <img className='post_author_pic' src={props.picture}/>
        <div className='post_info'>
          <a href='/profile' className='post_author_user'>{props.user}</a>           
          <small className="post_date">{props.date}</small>
        </div>
      </div>
    )
  }    
}


class Post extends React.Component {
  
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
