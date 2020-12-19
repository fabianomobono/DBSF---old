
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
