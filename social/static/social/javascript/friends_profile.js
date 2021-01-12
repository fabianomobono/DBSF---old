document.querySelector('#friend_request_button').addEventListener('click', () =>{
    const  csrftoken = Cookies.get('csrftoken');
    const request = new XMLHttpRequest();
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
})

// React components to render the post list
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
                key={post.id}
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
