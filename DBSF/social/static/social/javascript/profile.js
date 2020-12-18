
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
          posts: posts_from_server
      }
  }
  render() {
      return (
          <div>
              {this.state.posts.map(post => <Post
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