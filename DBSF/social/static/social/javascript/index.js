


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
          posts : [{author: response.author, author_picture: profile_pic_url, text: response.text, date: response.date}, ...this.state.posts]
        })
        document.querySelector("#new_post_text").value = '';
        console.log(response)
      }
      request.send(JSON.stringify(data))
    }
  }

  deletePost(post_id, author) {
    const post = document.getElementById(post_id)
    post.style.animationPlayState = 'running';
    setTimeout(() =>{
      this.setState({
        posts: this.state.posts.filter(post => post.id != post_id)
      })
    }, 1000)

    // delete the post from the server
    const data = {'post_author': author, 'id': post_id}
    const csrftoken = Cookies.get('csrftoken');
    const request = new XMLHttpRequest();
    request.open('POST', '/delete_post', true);
    request.setRequestHeader('X-CSRFToken', csrftoken);
    request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
    request.onload = () => {
      const response = JSON.parse(request.responseText);
                            
      console.log('loaded')
    }
    request.send(JSON.stringify(data))
    }

  
  render() {
    return (
      <div>
        <Post_generator 
          current_user={this.state.user}
          picture={this.state.profile_pic}
          onClick={() => this.handleClick()} />

        {this.state.posts.map(post => <Post
          onClick={() => this.deletePost(post.id, post.author)} 
          key={post.id}
          post_id={post.id}
          current_user={this.state.user}
          user={post.author}
          profile_pic={post.author_picture}
          text={post.text}
          date={post.date}  
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


