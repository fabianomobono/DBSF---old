class Post_generator extends React.Component {
  render() {
    return (
    <div className="new_post_div">
    <img className="post_author_pic" src={this.props.picture} alt="profile_pic" />
    <div>
      <textarea name="new_post_text" id="new_post_text" placeholder="Say something to your close firends"></textarea>
      <button onClick={() => this.props.onClick()} className='btn btn-primary'>&#10002;</button>
    </div>
  </div>
    )
  }
}



class Post_body extends React.Component {
  render() {
    return (
      <p className="post_body" >{this.props.text}</p>
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
        <Post_body text={this.props.text}/>
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
      posts: posts_from_server,
    }
  }
  handleClick() {
    const text = document.querySelector('#new_post_text').value;
    if (text.length > 1) {
      const data = {author: username, text: text}
      // send that post to the server to save it
      const csrftoken = Cookies.get('csrftoken');
      const request = new XMLHttpRequest();
      request.open('POST', '/create_new_post', true);
      request.setRequestHeader('X-CSRFToken', csrftoken);
      request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
      request.onload = () => {
        const response = JSON.parse(request.responseText)
        this.setState({
          posts : [{author: response.author, author_picture: profile_pic_url, text: response.text}, ...this.state.posts]
        })
        document.querySelector("#new_post_text").value = '';
        console.log(response)
      }
      request.send(JSON.stringify(data))
    }
  }
  render() {
    return (
      <div>
        <Post_generator 
          picture={this.state.profile_pic}
          onClick={() => this.handleClick()} />

        {this.state.posts.map(post => <Post 
          user={post.author}
          profile_pic={post.author_picture}
          text={post.text}  
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
