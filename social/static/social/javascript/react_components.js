class Post_generator extends React.Component {
 
  render() {
    return (
    <div className="new_post_div">
    <img className="post_author_pic" src={this.props.picture} alt="profile_pic" />
    <div>
      <textarea name="new_post_text" id="new_post_text" placeholder="Say something to your close friends"></textarea>
      <button onClick={() => this.props.onClick()} id='post_new_post_button' className='btn btn-primary'>&#10002;</button>
    </div>
  </div>
    )
  }
}


function Post_body(props) {
  var text = props.text
  let i = 0
  const new_text = text.split('\n')
  let result = []
  for(let i = 0; i < new_text.length; i++) {
    result.push(<p key={i} className='post_body'>{new_text[i]}</p>)
  }
    return result 
}



function Post_author(props) {
  const profile = '/profile/'
    return ( 
      <div className="author_info_div">
        <img className='post_author_pic' src={props.picture}/>
        <div className='post_info'>
          {props.current_user !== props.user ? (
            <a href={profile.concat(props.user)} className='post_author_user'>{props.user}</a>
            ) : <a href='/profile' className='post_author_user'>{props.user}</a>
          }    
          <p className='post_date'>{props.date}</p>
        </div>
      </div>
    )   
}


function Post_author_sandbox(props) {
  const profile = '/profile/'
    return ( 
      <div className="author_info_div">
        <img className='post_author_pic' src={props.picture}/>
        <div className='post_info'>
        <a onClick={(e) => props.friends_profile(e)} className='post_author_user'>{props.user}</a>   
          <p className='post_date'>{props.date}</p>
        </div>
      </div>
    )   
}


function Comment(props) {
  const current_user = props.current_user
  console.log('current user ', current_user)
  if (current_user === props.commentator){
    const profile = '/profile'
    return (
      <div className='comment'>
        <img className='image_in_comment' src={props.profile_pic} />
        <a href={profile} className="user_link_in_comment"> {props.commentator} </a>
        <p className='comment_text'>{props.text}</p>
      </div>
    )
  }
  else{
    const profile = '/profile/'.concat(props.commentator)
    return (
      <div className='comment'>
        <img className='image_in_comment' src={props.profile_pic} />
        <a href={profile} className="user_link_in_comment"> {props.commentator} </a>
        {props.text}
      </div>
    )
  }
  
 
}


function Comment_sandbox(props) {
  return(
    <div className='comment'>
        <img className='image_in_comment' src={props.profile_pic} />
        <a onClick={(e) => props.friends_profile(e)} className="user_link_in_comment">{props.commentator}</a>
        <p className='comment_text'>{props.text}</p>
      </div>
  )
}


class CreateComment extends React.Component {
  
  render() {
    return(
      <div className='create_comment'>
        <input className='comment_input' type='text' placeholder='Comment...' />
        <button onClick={(e) => this.props.add_comment(e.target.previousSibling)} className='submit_comment'>Comment</button>
      </div> 
    )
  }
}


class CommentSection extends React.Component {
  render() {
    return(
      <div className='comment_section'>
        
        {this.props.comments.map(comment => <Comment 
          commentator={comment.commentator}
          profile_pic={comment.profile_pic}
          text={comment.text}
          key={comment.id}
          id={comment.id}
          current_user={this.props.current_user}
        />)}
        
        <CreateComment
          add_comment={this.props.add_comment} 
        />
      </div>
    )
  }
}


class CommentSection_sandbox extends React.Component {
  render() {
    return(
      <div className='comment_section'>
        
        {this.props.comments.map(comment => <Comment_sandbox 
          commentator={comment.commentator}
          profile_pic={comment.profile_pic}
          text={comment.text}
          key={comment.id}
          id={comment.id}
          current_user={this.props.current_user}
          friends_profile={this.props.friends_profile}
        />)}
        
        <CreateComment
          add_comment={this.props.add_comment} 
        />
      </div>
    )
  }
}


class Feeling extends React.Component {
  render(){
    const profile = '/profile/'
    return (
      
      <div className='feeling'>
       
        <div className='like' onClick={() => this.props.like()} >👍</div>
        <div className='dislike' onClick={() => this.props.dislike()}>👎</div>
        <div className='likeNumber'  onClick={(e) => this.props.show(e.target.nextSibling.nextSibling)} title='who liked this post'>{this.props.likes.length}</div>
        <div className='dislikeNumber' onClick={(e) => this.props.show(e.target.nextSibling.nextSibling)}  title="who didn't like this post">{this.props.dislikes.length}</div>
        <div className='lovers'>
          <div className='close_lovers'><button onClick={(e) => this.props.hide(e.target.parentNode.parentNode)}>&#10006;</button></div>
          {this.props.likes.length > 0 ? this.props.likes.map(lover =>
            <div>
              <img src={lover.profile_pic} className='lover_picture' />
              {this.props.current_user !== lover.user ? 
                  <a href={profile.concat(lover.user)} className='lover_link'>{lover.user}</a>
                  :
                  <a href='/profile' className='lover_link'>{lover.user}</a>
                }
            </div>
            ):
            <p>No likes yet...</p>
          }
        </div>
        <div className='haters'>
          <div className='close_lovers'><button onClick={(e) => this.props.hide(e.target.parentNode.parentNode)}>&#10006;</button></div>
            {this.props.dislikes.length > 0 ? this.props.dislikes.map(lover =>
              <div>
                <img src={lover.profile_pic} className='lover_picture' />
                {this.props.current_user !== lover.user ? 
                  <a href={profile.concat(lover.user)} className='lover_link'>{lover.user}</a>
                  :
                  <a href='/profile' className='lover_link'>{lover.user}</a>
                }
                
              </div>
              ):
              <p>No hates yet...</p>
          }
        </div>
      </div>
    )
  }
}


class Feeling_sandbox extends React.Component {
  render(){
    const profile = '/profile/'
    return (
      
      <div className='feeling'>
       
        <div className='like' onClick={() => this.props.like()} >👍</div>
        <div className='dislike' onClick={() => this.props.dislike()}>👎</div>
        <div className='likeNumber'  onClick={(e) => this.props.show(e.target.nextSibling.nextSibling)} title='who liked this post'>{this.props.likes.length}</div>
        <div className='dislikeNumber' onClick={(e) => this.props.show(e.target.nextSibling.nextSibling)}  title="who didn't like this post">{this.props.dislikes.length}</div>
        <div className='lovers'>
          <div className='close_lovers'><button onClick={(e) => this.props.hide(e.target.parentNode.parentNode)}>&#10006;</button></div>
          {this.props.likes.length > 0 ? this.props.likes.map(lover =>
            <div>
              <img src={lover.profile_pic} className='lover_picture' />
                <a onClick={(e) => this.props.friends_profile(e)} className='lover_link'>{lover.user}</a>
            </div>
            ):
            <p>No likes yet...</p>
          }
        </div>
        <div className='haters'>
          <div className='close_lovers'><button onClick={(e) => this.props.hide(e.target.parentNode.parentNode)}>&#10006;</button></div>
            {this.props.dislikes.length > 0 ? this.props.dislikes.map(lover =>
              <div>
                <img src={lover.profile_pic} className='lover_picture' />
                <a onClick={(e) => this.props.friends_profile(e)} className='lover_link'>{lover.user}</a>
              </div>
              ):
              <p>No hates yet...</p>
          }
        </div>
      </div>
    )
  }
}


function Friendship_request(props) {
  const profile = '/profile/'
  return (
    <div id={props.id} className='friendship_request'>
      <img src={props.img} className='friend_request_img'/>
      
      <a href={profile.concat(props.sender)} className="request_sender">{props.sender}</a>
      <button onClick={() => props.confirm(props.id)} className="accept_request_button">&#10004;</button>
      <button onClick={() => props.ignore(props.id)} className="ignore_request_button">&#10006;</button> 
    </div>
  )
}
  

function Message(props) {
  if (props.current_user === props.sender){
    return (
      <div className='user_message_div'>
        <p className='user_message'>{props.text}</p>
      </div>
    )
  }
  else {
    return (
      <div className='receiver_message_div'>
        <p className='receiver_message'>{props.text}</p>
      </div>
    )
  }
 
   
}

 
function Top_bar(props) {
  const profile = '/profile/'
  return(
    <div className='top_bar'>
      <div className='user_info_div'>
        <img className='profile_pic_in_top_bar' src={props.profile_pic}/>
        <a className="friend_link" onClick={(e) => props.friends_profile(e)}>{props.user}</a>
      </div>
      <button onClick={() => props.close()}>&#x2716;</button>
    </div>
  )
}


class  Message_screen extends React.Component {
  
  componentDidUpdate(){
    var screen = document.getElementById('message_screen')
    screen.scrollTop = screen.scrollHeight;
  }

  componentDidMount(){
    var screen = document.getElementById('message_screen')
    screen.scrollTop = screen.scrollHeight;
  }

  render() {
    return(
      <div id='message_screen' className='message_screen'>
        {this.props.messages.map(message =>
          <Message 
            key={message.id}
            text={message.text}
            sender={message.sender}
            receiver={message.receiver}
            current_user={this.props.current_user}
          />
          )}
      </div>
    )
  }
}


function Compose_message(props) {
  return(
    <div className='compose_message'>
      <div className='message_input_div'>
        <input id='message_text' type='text'></input>
      </div>
      <div className='send_message_div'>
        <button onClick={() => props.send()} id='send_message_button'><i className="fa fa-paper-plane"></i></button>
      </div>
    </div>
  )
}


class Navbar extends React.Component {
  
  render() {
    return(
      <nav id='navbar' className='main_nav'>
        <a href="#" onClick={() => this.props.main()} title='homepage'>DBSF</a>
        <form action="/find_friends" onSubmit={(e) => this.props.search_friends(e) } method="GET">
          <input   id='search_input' name='search_term' type='text' placeholder='Search for friends' />
          <input className='search_friends_button' type="submit" value='&#x1F50D;' />
        </form>
        <a href="#" onClick={() => this.props.profile()}>      
          <img className="profile_pic_small_icon" src={this.props.profile_pic} alt="profile_pic" />      
          {this.props.user}
        </a>
        <form className="logout_form" action='/logout' method="get">
          
          <a className='logout_a' href="/logout">Log out</a>
        </form>
      </nav>
    )
  }
}


class Main extends React.Component {

  render() {
    if (this.props.page === 'loading'){
      return(
        <div className='main_sandbox'>
          LOADING...
        </div>

      )
    }
    else if (this.props.page === 'main') {
      return (
        <div className='main_sandbox'>
        <Feed_sandbox
          user={this.props.user}
          posts={this.props.posts} 
          profile_pic={this.props.profile_pic}
          handleClick={this.props.handleClick}
          deletePost={this.props.deletePost}
          friends_profile={this.props.friends_profile}
          load_more_posts={this.props.load_more_posts}
        />
        </div>
        
      )
    }
    else if (this.props.page === 'profile') {

      return(
        <div className='main_sandbox'>
          <Profile 
            user={this.props.user}
            first={this.props.first}
            last={this.props.last}
            email={this.props.email}
            profile_pic={this.props.profile_pic}
            dob={this.props.dob}
            update_profile_pic={this.props.update_profile_pic}
            save_new_pic={this.props.save_new_pic}
            friends_profile={this.props.friends_profile}

          />
          <Feed_sandbox
            profile_pic={this.props.profile_pic}
            user={this.props.user}
            posts={this.props.posts}
            handleClick={this.props.handleClick}
            deletePost={this.props.deletePost}
            friends_profile={this.props.friends_profile}
            load_more_posts={this.props.load_more_posts}
            page={this.props.page}
            load_more_own_posts={this.props.load_more_own_posts}
            load_more_friends_posts={this.props.load_more_friends_posts}
          />
        </div>
      ) 
    }
    else if (this.props.page === 'search_results') {
     return (
      <div className='search_results'>  
        {this.props.results.map(user => 
        <div className='friend_box_div'>
          <img className='friend_img' src={user.profile_pic} />
          <a className="friend_link" onClick={(e) => this.props.friends_profile(e)} >{user.user}</a>
          <p className='name_in_result'>{user.first} {user.last}</p>  
        </div>
         )}
         <p className='load_more_posts_p' onClick={() => load_more_posts()}>Load more posts...</p>
      </div>
     )
    }
    else {
        return(
          <Friends_profile_sandbox 
            friend={this.props.friend}
            posts={this.props.posts}
            friends_profile={this.props.friends_profile}
            request_friendship={this.props.request_friendship}
            unfriend={this.props.unfriend}
            friends_profile={this.props.friends_profile}
            load_more_posts={this.props.load_more_posts}
            load_more_friends_posts={this.props.load_more_friends_posts}
          />
        )
    } 
  }
}


class Potential_friend_box extends React.Component {
  render() {
    return (
      <div>{this.props.user}</div>
    )
  }
}


class Profile extends React.Component {
   
  render() {
    const csrftoken = Cookies.get('csrftoken');
    return (
      <div className='profile_div'>
        <div className="profile_pic_div">     
          <img className='profile_pic' src={this.props.profile_pic} alt="profile_pic" onClick={() => document.querySelector('.upload_picture_div').style.display = 'block'}/>
        </div>
        <div className="user_info_div">
          <p id='profile_username'>{this.props.user}</p>
          <ul>
            <li>{this.props.first} {this.props.last}</li>
            <li>{this.props.dob}</li>
            <li>{this.props.email}</li>
          </ul>
        </div>
    <div className="upload_picture_div">
      <button id='close_button' type="button" name="button" onClick={(e) => e.target.parentNode.style.display = 'none'}>&#10006;</button>
      <h1>Upload a new Profile picture</h1>
      
      <div className="profile_pic_in_popup">
        <img src={this.props.profile_pic} alt="profile_pic" /> 
      </div>
     
      <form className="upload_profile_pic_form" action="change_profile_pic" method="post" encType="multipart/form-data">
          <input type='hidden' name='csrfmiddlewaretoken' value={csrftoken} />
          <p><label>Upload profile picture
          <input name='profile_pic' type="file" id="image_upload" onChange={(e) => this.props.update_profile_pic(e)} accept="image/gif, image/jpeg, image/png" />
          </label></p>        
      </form>
      <button onClick={(e) => this.props.save_new_pic(e)}  id='save_picture_button' type='submit'  className='btn btn-primary' name="button" >Save Picture</button>
    </div>
  </div>
  
    )
  }
}


class Feed extends React.Component {
  
  render() {  
    return (
      <div >
        <Post_generator 
          current_user={this.props.user}
          picture={this.props.profile_pic}
          onClick={() => this.props.handleClick()} />

        {this.props.posts.length ?  this.props.posts.map(post => <Post
          onClick={() => this.props.deletePost(post.id, post.author)} 
          key={post.id}
          id={post.id}
          post_id={post.id}
          current_user={this.props.user}
          user={post.author}
          profile_pic={post.author_picture}
          current_user_profile_pic={this.props.profile_pic}
          text={post.text}
          date={post.date}
          comments={post.comments}
          likes={post.likes}
          dislikes={post.dislikes}
          friends_profile={this.props.friends_profile}
        />): <p className="no_results_p">No posts here. Try to search for friends in the search box and add them as friends. You'll see posts appear over time!</p>}
      </div>
    ) 
  }
}


class Feed_sandbox extends React.Component {
  
  render() {  
    return (
      <div >
        <Post_generator 
          current_user={this.props.user}
          picture={this.props.profile_pic}
          onClick={() => this.props.handleClick()} />

        {this.props.posts.length ?  this.props.posts.map(post => <Post_sandbox
          onClick={() => this.props.deletePost(post.id, post.author)} 
          key={post.id}
          id={post.id}
          post_id={post.id}
          current_user={this.props.user}
          user={post.author}
          profile_pic={post.author_picture}
          current_user_profile_pic={this.props.profile_pic}
          text={post.text}
          date={post.date}
          comments={post.comments}
          likes={post.likes}
          dislikes={post.dislikes}
          friends_profile={this.props.friends_profile}
          load_more_posts={this.props.load_more_posts}
          />): <p className="no_results_p">No posts here. Try to search for friends in the search box and add them as friends. You'll see posts appear over time!</p>}
          {
            this.props.page === 'profile' ?<p className='load_more_posts_p' onClick={() => this.props.load_more_friends_posts()}>Load more posts </p>:
            <p className='load_more_posts_p' onClick={() => this.props.load_more_posts()}>Load more posts </p> 
          }
          
          <div className='loader'></div>       
      </div>
    ) 
  }
}


class Post extends React.Component {
  constructor(props){
    super(props)
    this.state = {
      comments: this.props.comments,
      current_user: this.props.current_user,
      current_user_profile_pic: this.props.current_user_profile_pic,
      id: this.props.id,
      likes: this.props.likes,
      dislikes: this.props.dislikes
    }
    
  }

  like_post = () => {
    const data = {post_id: this.state.id}
    const  csrftoken = Cookies.get('csrftoken');
    const request = new XMLHttpRequest();
    request.open('POST', '/like_a_post', true)
    request.setRequestHeader('X-CSRFToken', csrftoken);
    request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
    request.onload = () => {
      const response = JSON.parse(request.responseText)
      console.log(response)
      if (response['response'] !== 'you already liked this post'){
        this.setState({
          likes: [...this.state.likes, 
            {post_id: this.state.id, 
             user: this.state.current_user, 
             profile_pic: this.state.current_user_profile_pic
            }]
        })
      }
      else{
        alert(response['response'])
      }
      
    }
    request.send(JSON.stringify(data))
  }

  show = (div) => {
    div.style.display = 'block'
    
  }

  hide = (div) => {
    div.style.display = 'none'
  }

  dislike_post = () => {
    const data = {post_id: this.state.id}
    const  csrftoken = Cookies.get('csrftoken');
    const request = new XMLHttpRequest();
    request.open('POST', '/dislike_a_post', true)
    request.setRequestHeader('X-CSRFToken', csrftoken);
    request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
    request.onload = () => {
      const response = JSON.parse(request.responseText)
      console.log(response)
      if (response['response'] !== 'you already disliked this post'){
        this.setState({
          dislikes: [...this.state.dislikes, 
            {post_id: this.state.id, 
             user: this.state.current_user, 
             profile_pic: this.state.current_user_profile_pic
            }]
        })
      }
      else{
        alert(response['response'])
      }
    }
    request.send(JSON.stringify(data))
  }
  
  add_comment = (text) =>{
    console.log(this.state.id)
    const data = {'post_id': this.state.id, 'commentator': this.state.current_user, 'text': text.value}
    const csrftoken = Cookies.get('csrftoken');
    const request = new XMLHttpRequest()
    request.open('POST', '/comment', true)
    request.setRequestHeader('X-CSRFToken', csrftoken);
    request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
    request.onload = () => {
      const response = JSON.parse(request.responseText)
      console.log(response)
      this.setState({
        comments: [...this.state.comments, 
          {
            text: response.text, 
            commentator: response.commentator, 
            profile_pic: response.profile_pic, 
            id:response.id, 
            current_user: this.state.current_user}]
          }
      )
      text.value = ''
    }
    request.send(JSON.stringify(data))
   
    
  }

  render() {
    if (this.props.current_user === this.props.user){
      return (
        <div id={this.props.post_id} className="post">
          <button onClick={() => this.props.onClick()} className="delete_post_button">&#10006;</button>
          <Post_author 
            current_user={this.props.current_user}
            picture={this.props.profile_pic}
            user={this.props.user}
            date={this.props.date}
            friends_profile={this.props.friends_profile}
          />
          <Post_body text={this.props.text}/>
          <Feeling
            current_user={this.state.current_user}
            like={this.like_post}
            dislike={this.dislike_post}
            likes={this.state.likes}
            dislikes={this.state.dislikes}
            show={this.show}
            hide={this.hide}
           
          />
          <CommentSection
            current_user={this.state.current_user}
            comments={this.state.comments}
            add_comment={this.add_comment}
            friends_profile={this.friends_profile}  
          />
        </div>
      )
    }
    else {
      return (
        <div id={this.props.post_id} className="post">

          <Post_author 
            current_user={this.props.current_user}
            picture={this.props.profile_pic}
            user={this.props.user}
            date={this.props.date}
            friends_profile={this.props.friends_profile}
          />
          <Post_body text={this.props.text}/>
          <Feeling 
            current_user={this.state.current_user}
             like={this.like_post}
             dislike={this.dislike_post}
             likes={this.state.likes}
             dislikes={this.state.dislikes}
             show={this.show}            
             hide={this.hide}
             
          />
          <CommentSection
            current_user={this.state.current_user}
            add_comment={this.add_comment}
            comments={this.state.comments}
          />
        </div>
      )
    }
  }
}


class Post_sandbox extends React.Component {
  constructor(props){
    super(props)
    this.state = {
      comments: this.props.comments,
      current_user: this.props.current_user,
      current_user_profile_pic: this.props.current_user_profile_pic,
      id: this.props.id,
      likes: this.props.likes,
      dislikes: this.props.dislikes
    }
    
  }

  like_post = () => {
    const data = {post_id: this.state.id}
    const  csrftoken = Cookies.get('csrftoken');
    const request = new XMLHttpRequest();
    request.open('POST', '/like_a_post', true)
    request.setRequestHeader('X-CSRFToken', csrftoken);
    request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
    request.onload = () => {
      const response = JSON.parse(request.responseText)
      console.log(response)
      if (response['response'] !== 'you already liked this post'){
        this.setState({
          likes: [...this.state.likes, 
            {post_id: this.state.id, 
             user: this.state.current_user, 
             profile_pic: this.state.current_user_profile_pic
            }]
        })
      }
      else{
        alert(response['response'])
      }
      
    }
    request.send(JSON.stringify(data))
  }

  show = (div) => {
    div.style.display = 'block'
    
  }

  hide = (div) => {
    div.style.display = 'none'
  }

  dislike_post = () => {
    const data = {post_id: this.state.id}
    const  csrftoken = Cookies.get('csrftoken');
    const request = new XMLHttpRequest();
    request.open('POST', '/dislike_a_post', true)
    request.setRequestHeader('X-CSRFToken', csrftoken);
    request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
    request.onload = () => {
      const response = JSON.parse(request.responseText)
      console.log(response)
      if (response['response'] !== 'you already disliked this post'){
        
        this.setState({
          dislikes: [...this.state.dislikes, 
            {post_id: this.state.id, 
             user: this.state.current_user, 
             profile_pic: this.state.current_user_profile_pic
            }]
            
        })
        
      }
      else{
        alert(response['response'])
      }
    }
    request.send(JSON.stringify(data))
  }
  
  add_comment = (text) =>{
    console.log(this.state.id)
    const data = {'post_id': this.state.id, 'commentator': this.state.current_user, 'text': text.value}
    const csrftoken = Cookies.get('csrftoken');
    const request = new XMLHttpRequest()
    request.open('POST', '/comment', true)
    request.setRequestHeader('X-CSRFToken', csrftoken);
    request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
    request.onload = () => {
      const response = JSON.parse(request.responseText)
      console.log(response)
      this.setState({
        comments: [...this.state.comments, 
          {
            text: response.text, 
            commentator: response.commentator, 
            profile_pic: response.profile_pic, 
            id:response.id, 
            current_user: this.state.current_user}]
          }
      )
      text.value = ''
    }
    request.send(JSON.stringify(data))
   
    
  }

  render() {
    if (this.props.current_user === this.props.user){
      return (
        <div id={this.props.post_id} className="post">
          <button onClick={() => this.props.onClick()} className="delete_post_button">&#10006;</button>
          <Post_author_sandbox 
            current_user={this.props.current_user}
            picture={this.props.profile_pic}
            user={this.props.user}
            date={this.props.date}
            friends_profile={this.props.friends_profile}
          />
          <Post_body text={this.props.text}/>
          <Feeling_sandbox
            current_user={this.props.current_user}
            like={this.like_post}
            dislike={this.dislike_post}
            likes={this.state.likes}
            dislikes={this.state.dislikes}
            show={this.show}
            hide={this.hide}
            friends_profile={this.props.friends_profile}
           
          />
          <CommentSection_sandbox
            current_user={this.props.current_user}
            comments={this.state.comments}
            add_comment={this.add_comment}
            friends_profile={this.props.friends_profile}
             
          />
        </div>
      )
    }
    else {
      return (
        <div id={this.props.post_id} className="post">

          <Post_author_sandbox 
            current_user={this.props.current_user}
            picture={this.props.profile_pic}
            user={this.props.user}
            date={this.props.date}
            friends_profile={this.props.friends_profile}
          />
          <Post_body text={this.props.text}/>
          <Feeling_sandbox 
            current_user={this.state.current_user}
             like={this.like_post}
             dislike={this.dislike_post}
             likes={this.state.likes}
             dislikes={this.state.dislikes}
             show={this.show}            
             hide={this.hide}
             friends_profile={this.props.friends_profile}
             
          />
          <CommentSection_sandbox
            current_user={this.state.current_user}
            add_comment={this.add_comment}
            comments={this.state.comments}
            friends_profile={this.props.friends_profile}
          />
        </div>
      )
    }
  }
}


class Friends extends React.Component {
  constructor(props){
    super(props)
    this.state = {
      friends: this.props.friends,
      user: this.props.user
    }
    
  }

  hello = (user) => {
    var now = new Date()
    now.toUTCString()
    now = now.toString()
    now = now.substring(0, now.length -33)
    var friends = this.state.friends
    for (let i = 0; i < friends.length; i ++){
      if (friends[i]['user'] === user){
        friends[i].last_message_date = now
      }
    }
    this.setState({friends: friends})
    console.log(now)
  }

  message(friend, profile_pic) {
    document.getElementById('message_box').style.display = 'block';
   
    // get friendship id for chatSocket
    const data = {sender: this.state.user, receiver: friend}
    const friendship = new XMLHttpRequest()
    const csrftoken = Cookies.get('csrftoken');
    friendship.open("POST", "/friendship_id", true)
    friendship.setRequestHeader('X-CSRFToken',csrftoken);
    friendship.setRequestHeader('Content-Type', "text/plain;charset=UTF-8");
    friendship.onload = () => {
      const answer = JSON.parse(friendship.responseText)
      const friendship_id = answer.id
      const messages_from_server = answer.messages
      console.log(answer.id)
      console.log(messages_from_server)

    // create messaging appnew ReconnectingWebSocket
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    const chatSocket = new WebSocket(
      ws_scheme
      + '://'
      + window.location.host
      + '/wss/chat/'
      + friendship_id
      + '/'
    );
    console.log(chatSocket)
    

    class Message_app extends React.Component {
      constructor(props) {
        super(props)
        this.state = {
          messages: messages_from_server,
          receiver: friend,
          receiver_pic: profile_pic,
          user: this.props.user,
        }
      }
      
      componentDidMount() {
       
        chatSocket.onmessage = (e) => {
          const data = JSON.parse(e.data)
          console.log(data)
          this.setState({
            messages: [...this.state.messages, {'text': data.message, 'sender': data.sender, 'receiver':data.receiver, 'id': data.id}]
          })
        }
        document.querySelector('#message_text').onkeyup = function (e) {
          if (e.keyCode === 13) {
            document.querySelector("#send_message_button").click() 
          }
        }  
      }

      // close the websocket connection when the close button is clicked
      componentWillUnmount() {
       
      }

      
      sendMessage() {
        
        const message = document.querySelector("#message_text").value;
        //send the message via the chatsocket
        if (message.length > 0){
          chatSocket.send(JSON.stringify({
            text: message,
            sender: this.state.user,
            receiver: this.state.receiver
          }));
          document.querySelector("#message_text").value = '';

          this.props.greet(this.state.receiver)
        }
      }

      close() {
        document.getElementById('message_box').style.display = 'none';
        chatSocket.close()
        console.log('closed chatSocket')
      }

      render() {
        return(
          <div className='inner_container'>
          <Top_bar
            user={this.state.receiver}
            profile_pic={this.state.receiver_pic}
            close={() => this.close()}
            friends_profile={this.props.friends_profile}
          />
          <Message_screen 
            messages={this.state.messages}
            current_user={this.state.user}
          />
          <Compose_message 
            send={() => this.sendMessage()}
          />
          </div>
        )
      }
    }
    ReactDOM.render(
      <Message_app 
      user={this.state.user}
      greet={(user) => this.hello(user)}
      friends_profile={this.props.friends_profile}
      />, document.getElementById('message_box')
      
    )

    }
    friendship.send(JSON.stringify(data))

    
  }

  render() {
    return (
      <div className="friends_sandbox">
        
        {this.props.friends.length ? this.props.friends.map(friend => <Friend_box
          key={friend.id}
          name={friend.user}
          profile_pic={friend.profile_pic}
          friend={friend.id}
          message={() => this.message(friend.user, friend.profile_pic)}
          last_contact={friend.last_message_date}
          friends_profile={this.props.friends_profile}
        />): <p className='no_results_p'>Uh Oh! You don't have any Friends yet.
        Try to add them via the search box and they will appear here when they accept your friend request.</p>}
      </div>
      )
  }
}


function Friend_box_sandbox(props) {
  const profile = '/profile/'
  const date = new Date(props.last_contact)
  
  var now = new Date()
  now.setHours(now.getHours() + 5);
  console.log(now)
  console.log(date)
  now -= date
  console.log(now, props.name)

  // if you contacted the person in the last 10 seconds(low timeframe for testing) 
  if (now > 10000 || isNaN(now)){
    return (
      <div className='friend_box_div'>
        <img className='friend_img' src={props.profile_pic} />
        <div className='DBSF_interaction'>
          <a className="friend_link" onClick={(e) => props.friends_profile(e)}>{props.name}</a>
          <p className='last_contacted'>Last contact:</p>
          {isNaN(now) ? <p className='last_contacted'>{props.last_contact}</p>:<p className='last_contacted'>{props.last_contact.substring(0, props.last_contact.length - 9)}</p>}
        </div>
        <button onClick={() => props.message(props.name, props.profile_pic)} id={props.friend} className="btn btn-primary"><i className="fa fa-paper-plane"></i></button>
    </div>
    ) 
  }

  // if you talked recently....
  else {
    return (
      <div className='friend_box_div'>
        <img className='friend_img' src={props.profile_pic} />
        <div className='interaction'>
          <a className="friend_link" onClick={(e) => props.friends_profile(e)}>{props.name}</a>
          <p className='last_contacted'>Last contact:</p>
          <p className='last_contacted'>{props.last_contact.substring(0, props.last_contact.length -9)}</p>
        </div>
        <button onClick={() => props.message(props.name, props.profile_pic)} id={props.friend} className="btn btn-primary"><i className="fa fa-paper-plane"></i></button>
    </div>
    ) 
  }
}


function Friend_box(props) {
  const profile = '/profile/'
  const date = new Date(props.last_contact)
  var now = new Date()
  now -= date
  console.log(now, props.name) 
  if (now > 10000 || isNaN(now)){
    return (
      <div className='friend_box_div'>
        <img className='friend_img' src={props.profile_pic} />
        <div className='DBSF_interaction'>
          <a className="friend_link" href={profile.concat(props.name)}>{props.name}</a>
          <p className='last_contacted'>Last contact:</p>
          {isNaN(now) ? <p className='last_contacted'>{props.last_contact}</p>:<p className='last_contacted'>{props.last_contact.substring(0, props.last_contact.length - 9)}</p>}
        </div>
        <button onClick={() => props.message(props.name, props.profile_pic)} id={props.friend} className="btn btn-primary"><i className="fa fa-paper-plane"></i></button>
    </div>
    ) 
  }
  else {
    return (
      <div className='friend_box_div'>
        <img className='friend_img' src={props.profile_pic} />
        <div className='interaction'>
          <a className="friend_link" href={profile.concat(props.name)}>{props.name}</a>
          <p className='last_contacted'>Last contact:</p>
          <p className='last_contacted'>{props.last_contact.substring(0, props.last_contact.length -9)}</p>
        </div>
        <button onClick={() => props.message(props.name, props.profile_pic)} id={props.friend} className="btn btn-primary"><i className="fa fa-paper-plane"></i></button>
    </div>
    ) 
  }
}


class Friendship_requests_div extends React.Component {
  constructor(props){
    super(props);
    this.state = {
     pending: this.props.friend_requests
    }
  }

  confirm_request = (id) => {
    const confirm = new XMLHttpRequest()
    const csrftoken = Cookies.get('csrftoken');
    
    confirm.open('POST', '/confirm_friend_request', true);
    confirm.setRequestHeader('X-CSRFToken', csrftoken);
    confirm.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
    confirm.onload = () => {
      const response = JSON.parse(confirm.responseText)
      console.log(response)
      if (response.response === 'friendship confirmed'){
        const box = document.getElementById(id)
        const message = document.createElement("P");
        message.setAttribute("class", "no_results_p");
        message.innerHTML = response.response
        box.innerHTML = ''
        box.appendChild(message)
        console.log(message)
      }
     
    }
    confirm.send(id)
  }

  ignore_request = (id) => {
    const ignore = new XMLHttpRequest();
    const csrftoken = Cookies.get('csrftoken');
    ignore.open('POST', '/ignore_friend_request', true);
    ignore.setRequestHeader('X-CSRFToken',csrftoken);
    ignore.setRequestHeader('Content-Type', "text/plain;charset=UTF-8");
    ignore.onload = () => {
      const response = JSON.parse(ignore.responseText)
      if (response.response === 'request ignored'){
        const box = document.getElementById(id)
        const message = document.createElement("P");
        message.setAttribute("class", "no_results_p");
        message.innerHTML = response.response
        box.innerHTML = ''
        box.appendChild(message)
        console.log(message)
      }
    }
    ignore.send(id)
  }

  render() {
    return (
      <div className='f_requests_sandbox'>
        {this.state.pending.length ? this.state.pending.map(x => <Friendship_request
          key={x.id}
          img={x.sender_profile_pic}
          sender={x.sender}
          id={x.id}
          ignore={this.ignore_request()}
          confirm={this.confirm_request()}
          />
        ): <p className='no_results_p'>No pending Friendship requests.</p>}
        
      </div>
    );
  }
}


class Friends_profile_sandbox extends React.Component { 
  render() {

    return(
      <div className='main_sandbox'>
         <div className="profile_div">
          <div className="profile_pic_div">
            <img className='profile_pic' src={this.props.friend.profile_pic} alt="profile_pic"/>  
          </div>
          <div className="user_info_div">
          <div className="friendship_div">
            <p id='profile_friendname'>{this.props.friend.friend}</p>
            {this.props.friend.status === 'False' ? <button onClick={() => this.props.request_friendship()} id='friend_request_button'><i className="fa fa-user-plus"></i> Add</button>:
             this.props.friend.status === 'Pending' || this.props.friend.status === 'Rejected' ? <button  id='friend_request_button' disabled>Request is pending</button>:
             <button onClick={() => this.props.unfriend()} id='friend_request_button'>Unfriend</button> }

          </div>
            <ul>
              <li>{this.props.friend.first} {this.props.friend.last}</li>
              <li>{this.props.friend.dob}</li>
              <li>{this.props.friend.email}</li>
            </ul>
          </div>
        </div>
        <Post_list_sandbox
          posts={this.props.posts}
          friends_profile={this.props.friends_profile}
          load_more_friends_posts={this.props.load_more_friends_posts}
        />   
      </div>
    )
  }
}


class Post_list extends React.Component {
  render() {
    return (
    <div className="postlist">
      {this.props.posts.map(post => <Post 
         onClick={() => this.props.deletePost(post.id, post.author)} 
         key={post.id}
         id={post.id}
         post_id={post.id}
         current_user={this.props.user}
         user={post.author}
         profile_pic={post.author_picture}
         current_user_profile_pic={this.props.profile_pic}
         text={post.text}
         date={post.date}
         comments={post.comments}
         likes={post.likes}
         dislikes={post.dislikes}
         friends_profile={this.props.friends_profile}
      />)}
    </div>
     
    )
  }
}


class Post_list_sandbox extends React.Component {
  render() {
    return (
    <div className="postlist">
      {this.props.posts.map(post => <Post_sandbox 
         onClick={() => this.props.deletePost(post.id, post.author)} 
         key={post.id}
         id={post.id}
         post_id={post.id}
         current_user={this.props.user}
         user={post.author}
         profile_pic={post.author_picture}
         current_user_profile_pic={this.props.profile_pic}
         text={post.text}
         date={post.date}
         comments={post.comments}
         likes={post.likes}
         dislikes={post.dislikes}
         friends_profile={this.props.friends_profile}
      />)}
          <p className='load_more_posts_p' onClick={() => this.props.load_more_friends_posts()}>Load more posts </p>
          <div className='loader'></div>
    </div>
     
    )
  }
}


class Friendship_requests_div_sandbox extends React.Component {

  render() {
    return (
      <div className='f_requests_sandbox'>
        {this.props.friend_requests.length ? this.props.friend_requests.map(x => <Friendship_request
          key={x.id}
          img={x.sender_profile_pic}
          sender={x.sender}
          id={x.id}
          ignore={this.props.ignore}
          confirm={this.props.confirm}
          />
        ): <p className='no_results_p'>No pending Friendship requests.</p>}
        
      </div>
    );
  }
}


class Friends_sandbox extends React.Component {
  constructor(props){
    super(props)
    this.state = {
      friends: this.props.friends,
      user: this.props.user
    }
    
  }

  // update the last interaction display
  

  message(friend, profile_pic) {
    document.getElementById('message_box').style.display = 'block';
   
    // get friendship id for chatSocket
    const data = {sender: this.state.user, receiver: friend}
    const friendship = new XMLHttpRequest()
    const csrftoken = Cookies.get('csrftoken');
    friendship.open("POST", "/friendship_id", true)
    friendship.setRequestHeader('X-CSRFToken',csrftoken);
    friendship.setRequestHeader('Content-Type', "text/plain;charset=UTF-8");
    friendship.onload = () => {
      const answer = JSON.parse(friendship.responseText)
      const friendship_id = answer.id
      const messages_from_server = answer.messages
      console.log(answer.id)
      console.log(messages_from_server)

    // create messaging websocket
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    const chatSocket = new WebSocket(
      ws_scheme
      + '://'
      + window.location.host
      + '/wss/chat/'
      + friendship_id
      + '/'
    );
    console.log(chatSocket)
    

    class Message_app extends React.Component {
      constructor(props) {
        super(props)
        this.state = {
          messages: messages_from_server,
          receiver: friend,
          receiver_pic: profile_pic,
          user: this.props.user,
        }
      }
      
      componentDidMount() {
       
        chatSocket.onmessage = (e) => {
          const data = JSON.parse(e.data)
          console.log(data)
          this.setState({
            messages: [...this.state.messages, {'text': data.message, 'sender': data.sender, 'receiver':data.receiver, 'id': data.id}]
          })
        }
        document.querySelector('#message_text').onkeyup = function (e) {
          if (e.keyCode === 13) {
            document.querySelector("#send_message_button").click() 
          }
        }  
      }
      
      sendMessage() {
        
        const message = document.querySelector("#message_text").value;
        //send the message via the chatsocket
        if (message.length > 0){
          chatSocket.send(JSON.stringify({
            message: message,
            sender: this.state.user,
            receiver: this.state.receiver
          }));
          document.querySelector("#message_text").value = '';
          this.props.greet(this.state.receiver)
        }
      }

      close() {
        document.getElementById('message_box').style.display = 'none';
      }

      render() {
        return(
          <div className='inner_container'>
          <Top_bar
            user={this.state.receiver}
            profile_pic={this.state.receiver_pic}
            close={() => this.close()}
            friends_profile={this.props.friends_profile}
          />
          <Message_screen 
            messages={this.state.messages}
            current_user={this.state.user}
          />
          <Compose_message 
            send={() => this.sendMessage()}
          />
          </div>
        )
      }
    }
    ReactDOM.render(
      <Message_app 
      user={this.state.user}
      greet={(user) => this.props.hello(user)}
      friends_profile={this.props.friends_profile}
      />, document.getElementById('message_box')
      
    )

    }
    friendship.send(JSON.stringify(data))

    
  }

  render() {
    return (
      <div className="friends_sandbox">        
        {this.props.friends.length ? this.props.friends.map(friend => <Friend_box_sandbox
          key={friend.id}
          name={friend.user}
          profile_pic={friend.profile_pic}
          friend={friend.id}
          message={() => this.message(friend.user, friend.profile_pic)}
          last_contact={friend.last_message_date}
          friends_profile={this.props.friends_profile}
        />): <p className='no_results_p'>Uh Oh! You don't have any Friends yet.
        Try to add them via the search box and they will appear here when they accept your friend request.</p>}
      </div>
      )
  }
}