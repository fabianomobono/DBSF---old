class Post_body extends React.Component {
  render() {
    return (
      <p className="post_body" >This is the body</p>
    )
  }
}

class Post_author extends React.Component {
  render() {
    return (
      <img className='post_author_pic' src="static/social/core_images/coglioni.jpg"  />
    )
  }
}



class Post extends React.Component {
  render() {
    return (
      <div className="post">
        <Post_author />
        <Post_body />
      </div>
    )
  }
}


// ========================================

ReactDOM.render(
  <Post />,
  document.getElementById('feed')
);
