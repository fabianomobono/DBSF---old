// get the posts from server
const posts = new XMLHttpRequest()
posts.open('GET','/get_posts', true)
posts.onload = () => {
  const server_posts = JSON.parse(posts.responseText)
  console.log(server_posts)


  class Feed extends React.Component {
    constructor(props){
      super(props);
      this.state = {
        profile_pic: server_posts.profile_pic,
        user: server_posts.username,
        posts: server_posts.response
      }
    }
   
  
    handleClick() {
      const text = document.querySelector('#new_post_text').value;
      if (text.length > 1) {
        const data = {author: this.state.user, text: text}
        // send that post to the server to save it
        const csrftoken = Cookies.get('csrftoken');
        const request = new XMLHttpRequest();
        request.open('POST', '/create_new_post', true);
        request.setRequestHeader('X-CSRFToken', csrftoken);
        request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
        request.onload = () => {
          const response = JSON.parse(request.responseText)
          this.setState({
            posts : [{author: response.author, author_picture: this.state.profile_pic, text: response.text, date: response.date, id:response.id}, ...this.state.posts]
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
                              
        console.log(response)
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
  

}
posts.send()



