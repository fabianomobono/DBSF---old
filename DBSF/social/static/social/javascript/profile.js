
document.querySelector('.profile_pic').addEventListener('click', () => {
  document.querySelector(".upload_picture_div").style.display = 'block';
})


function closeElement(element) {
  element.parentElement.style.display = 'none';
}


var loadFile = function(event){
  document.querySelector(".profile_pic_in_popup").innerHTML = ''
  var files = event.target.files['0']
  var image = document.createElement("IMG")
  image.width = 200
  image.src = URL.createObjectURL(event.target.files['0']);
  document.querySelector(".profile_pic_in_popup").appendChild(image)
  document.querySelector("#save_picture_button").removeAttribute('disabled');
}


class Post_list extends React.Component {
  constructor(props) {
      super(props);
      this.state = {
          posts: posts_from_server,
          user: username,
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
       response = JSON.parse(request.responseText);
       console.log(response)
     }
     request.send(JSON.stringify(data))

    }

  render() {
      return (
          <div>
              {this.state.posts.map(post => <Post
              delete={() => this.deletePost(post.id, post.author)}
              current_user={this.state.user}
              key={post.id}
              post_id={post.id}
              user={post.author}
              profile_pic={post.author_picture}
              text={post.text}
              date={post.date}
              />)}
          </div>
      )
  }
}


ReactDOM.render(
  <Post_list />,
  document.getElementById('friends_posts_div')
);