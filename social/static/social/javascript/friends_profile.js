document.querySelector('#friend_request_button').addEventListener('click', () => {
    const button_text = document.querySelector('#friend_request_button').innerHTML
    const  csrftoken = Cookies.get('csrftoken');
    const request = new XMLHttpRequest();
    if (button_text === 'Unfriend') {
      request.open('POST', '/unfriend', true)
      request.setRequestHeader('X-CSRFToken', csrftoken);
      request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");

      request.onload = () => {
        const response = JSON.parse(request.responseText)
        console.log(response)
        alert("Unfriended")
        document.querySelector('#friend_request_button').innerHTML = '<i class="fa fa-user-plus"> Add';
        
    }
    request.send(username);
    }
    else {
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
    }
    
})


// get the friend posts and load them
const  csrftoken = Cookies.get('csrftoken');
const request = new XMLHttpRequest();
request.open('POST', '/friends_posts', true)
request.setRequestHeader('X-CSRFToken', csrftoken);
request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
request.onload = () => {
    const answer = JSON.parse(request.responseText)
    console.log(answer)
    class Post_list extends React.Component {
        constructor(props) {
            super(props);
            this.state = {
                posts: answer.response,
                user: answer.username,
                profile_pic: answer.profile_pic
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
                    {this.state.posts.map(post => <Post
                    onClick={() => this.deletePost(post.id, post.author)}
                    current_user={this.state.user}
                    key={post.id}
                    id={post.id}
                    user={post.author}
                    current_user_profile_pic={this.state.profile_pic}
                    profile_pic={post.author_picture}
                    text={post.text}
                    date={post.date}
                    comments={post.comments}
                    likes={post.likes}
                    dislikes={post.dislikes}
                    />)}
                </div>
            )
        }
      }
      
      ReactDOM.render(
        <Post_list />,
        document.getElementById('friends_posts_div')
      );

    // load the posts with react
}
request.send(username)