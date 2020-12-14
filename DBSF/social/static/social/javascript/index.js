class Post_generator extends React.Component {
  render() {
    return (
    <div className="new_post_div">
    <img className="post_author_pic" src={this.props.picture} alt="profile_pic" />
    
    <textarea name="new_post_text" id="new_post_text" placeholder="Say something to your close firends"></textarea>
    <button onClick={() => this.props.onClick()} className='btn btn-primary'>&#10002;</button>
    
  </div>
    )
  }
}



class Post_body extends React.Component {
  render() {
    return (
      <p className="post_body" >This is the body</p>
    )
  }
}

function Post_author(props) { 
    return (
      <div className="author_info_div">
        <img className='post_author_pic' src={props.picture}/>
        <p className='post_author_user'>{props.user}</p>
      </div>
    )
}



class Post extends React.Component {
  render() {
    return (
      <div className="post">
        <Post_author 
          picture={this.props.profile_pic}
          user={this.props.user}
        />
        <Post_body />
      </div>
    )
  }
}


class Feed extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      profile_pic: profile_pic_url,
      user: username,
      posts: []
    }
  }
  handleClick() {
    alert('is was clicked')
  }
  render() {
    return (
      <div>
        <Post_generator 
          picture={this.state.profile_pic}
          onClick={() => this.handleClick()} />

        {this.state.posts.map(post => <Post 
          user={this.state.user}
          profile_pic={this.state.profile_pic}  
        />)}
      </div>
    )
  }
}

// ========================================

ReactDOM.render(
  <Feed />,
  document.getElementById('feed')
);
