// get all the necessasry info from the server 1) friend_requests 2) posts 3) friends

// create the App class 

const request = new XMLHttpRequest()
const csrftoken = Cookies.get('csrftoken');
const data = {'page_number': 1}
request.open('POST', '/sandbox', true)
request.setRequestHeader('X-CSRFToken', csrftoken);
request.setRequestHeader('Content-Type', "text/plain;charset=UTF-8");
request.onload = () => {
    const response = JSON.parse(request.responseText)
    console.log(response)

    // create the app component and put all the info into the state
    class App extends React.Component {
        constructor(props) {
            super(props)
            this.state = {
                user: response.user,
                profile_pic: response.profile_pic,
                posts: response.posts,
                friends: response.friends,
                friend_requests: response.friend_requests,
                first: response.first,
                last: response.last,
                dob: response.dob,
                email: response.email,
                page: 'main',
                friend: {},
                results: [],
                post_page : 1,
            }
        }

        main = () => {
            this.setState({
                page: 'loading',
                posts: []
            })        
            const request = new XMLHttpRequest()
            request.open("GET", '/get_posts', true)
            request.onload = () => {
                const response = JSON.parse(request.responseText)
                console.log(response)
                this.setState({
                    page: 'main',
                    posts: response.response
                })
            }
            request.send()    
        }

        profile = () => {
            this.setState({
                posts: [],
                page: 'loading',
                post_page: 1,
                friend : {},
            })  
            const request = new XMLHttpRequest()
            request.open("GET", '/get_own_posts?page_number=1' , true)
            request.onload = () => {
                const response = JSON.parse(request.responseText)
                console.log(response)
                this.setState({    
                    posts: response.response,
                    page: 'profile',
                    post_page: 1
                })
            }
            request.send()    
        }

        friends_profile = (e) => {
            const friend = e.target.innerHTML
            if (friend === this.state.user){
                this.setState({
                    page: 'loading',
                    post_page : 1,
                    posts: [],
                })  
                const request = new XMLHttpRequest()
                request.open("GET", '/get_own_posts?page_number=1')
                request.onload = () => {
                    const response = JSON.parse(request.responseText)
                    console.log(response)
                    this.setState({
                        page: 'profile',
                        posts: response.response,
                        post_page: 1
                    })
                }
                request.send()    
            }
            else {
                this.setState({
                    page: 'loading',
                    post_page : 1,
                    posts: [],
                }) 
                const request = new XMLHttpRequest()
                const csrftoken = Cookies.get('csrftoken');
                request.open('POST', '/friends_profile_sandbox', true)
                request.setRequestHeader('X-CSRFToken', csrftoken);
                request.setRequestHeader('Content-Type', "text/plain;charset=UTF-8");
                request.onload = () => {
                    const answer = JSON.parse(request.responseText)
                    console.log(answer)
                    this.setState({
                        page: friend,
                        friend: answer,
                        post_page: 1,
                        posts : answer.posts
                    })
                }
                request.send(JSON.stringify({'friend': friend, 'page_number': 1}))

               
            }
            
        }

        update_profile_pic = (e) => {
            document.querySelector(".profile_pic_in_popup").innerHTML = ''
            var image = document.createElement("IMG")
            image.width = 200
            image.src = URL.createObjectURL(e.target.files['0']);
            document.querySelector(".profile_pic_in_popup").appendChild(image)
            document.querySelector("#save_picture_button").style.display= 'inline-block';
        }

        save_new_pic  = (e) => {
            const profile_pic = e.target.previousSibling.childNodes[1].firstChild.childNodes[1].files[0]
            var formdata = new FormData()
            formdata.append('profile_pic', profile_pic)
            const request = new XMLHttpRequest()
            request.open('POST', 'change_profile_pic', true)
            const csrftoken = Cookies.get('csrftoken');
            request.setRequestHeader('X-CSRFToken', csrftoken);
            request.onload = () => {
                const answer = JSON.parse(request.responseText)

                //change the profile pic in the state
                this.setState({
                    profile_pic: answer.profile_pic
                })

                // change the proile in the author's posts
                var posts = []
                for(let i = 0 ; i < this.state.posts.length; i++) {
                    if (this.state.posts[i].author === this.state.user) {
                        posts.push(
                            {
                                'id': this.state.posts[i].id, 
                                'author': this.state.posts.author, 
                                'text': this.state.posts[i].text, 
                                'date': this.state.posts[i].date, 
                                'author_picture': answer.profile_pic,
                                'comments': this.state.posts[i].comments,
                                'likes': this.state.posts[i].likes,
                                'dislikes': this.state.posts[i].dislikes,
                            }
                        )
                    }
                    else {
                        posts.push(this.state.posts[i])
                    }
                }

                this.setState({
                    posts: posts
                })
                document.querySelector('.upload_picture_div').style.display = 'none';
            }
            request.send(formdata)   
        }

        handleClick = () => {
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
                console.log(response)
                
                this.setState({
                  posts : [{likes: [], dislikes: [], author: response.author, author_picture: this.state.profile_pic, text: response.text, date: response.date, id:response.id, comments: response.comments}, ...this.state.posts]
                })
                document.querySelector("#new_post_text").value = '';
                console.log(response)
              }
              request.send(JSON.stringify(data))
            }
        }
        
        deletePost = (post_id, author) => {
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

        request_friendship = () => {
            console.log('this is happening')
            const request = new XMLHttpRequest()
            const csrftoken = Cookies.get('csrftoken')
            request.open("POST", '/request_friendship', true)
            request.setRequestHeader('X-CSRFToken', csrftoken)
            request.setRequestHeader('COntent-Type', 'text/plain;charset=UTF8')
            request.onload = () => {
                const response = JSON.parse(request.responseText).response
                if (response === "Friendship requested"){
                    this.setState({
                        friend:  {dob: this.state.friend.dob,
                            email: this.state.friend.email,
                            first: this.state.friend.first,
                            friend: this.state.friend.friend,
                            last: this.state.friend.last,
                            posts: this.state.friend.posts,
                            profile_pic: this.state.friend.profile_pic,
                            status: "Pending",
                            user: this.state.friend.user
                        }
                    })
                }
            }
            request.send(this.state.page)   
        }

        unfriend = () => {
            console.log('starting to unfirnd')
            const request = new XMLHttpRequest()
            const csrftoken = Cookies.get('csrftoken')
            request.open("POST", '/unfriend', true)
            request.setRequestHeader('X-CSRFToken', csrftoken)
            request.setRequestHeader('COntent-Type', 'text/plain;charset=UTF8')
            request.onload = () => {
                const response = JSON.parse(request.responseText).response
                if (response === 'unfriended_sent' || response === 'unfriended_received'){
                    // change the friendship status
                    this.setState({
                        friend:  {dob: this.state.friend.dob,
                            email: this.state.friend.email,
                            first: this.state.friend.first,
                            friend: this.state.friend.friend,
                            last: this.state.friend.last,
                            posts: this.state.friend.posts,
                            profile_pic: this.state.friend.profile_pic,
                            status: "False",
                            user: this.state.friend.user
                        },
                        friends: this.state.friends.filter(f => f.user !== this.state.page),
                        posts: this.state.posts.filter(p => p.author !== this.state.page)
                    })
                    console.log('unfriended')
                }
            }
            request.send(this.state.page)   
        }

        confirm_request = (id) => {
            const confirm = new XMLHttpRequest()
            const csrftoken = Cookies.get('csrftoken');
            this.setState({
                posts: [],
                page: 'loading',
                post_page: 1,
            })
            confirm.open('POST', '/confirm_friend_request', true);
            confirm.setRequestHeader('X-CSRFToken', csrftoken);
            confirm.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
            confirm.onload = () => {
              const answer = JSON.parse(confirm.responseText)
              const response = answer['updated_info']
              const status = answer['response']
              console.log(response)
              
              if (status === 'friendship confirmed') {
                const box = document.getElementById(id)
                const message = document.createElement("P");
                message.setAttribute("class", "no_results_p");
                message.innerHTML = status
                box.innerHTML = ''
                box.appendChild(message)
                console.log(message)
                this.setState({
                    user: response.user,
                    profile_pic: response.profile_pic,
                    posts: response.posts,
                    friends: response.friends,
                    friend_requests: response.friend_requests,
                    first: response.first,
                    last: response.last,
                    dob: response.dob,
                    email: response.email,
                    page: 'main',
                    friend: {}
                })

              }
             
            }
            confirm.send(id)
          }
      
        ignore_request(id) {
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

        search_friends = (e) => { 
            e.preventDefault()
            this.setState({
                page: 'loading'
            })          
            const search_term = e.target.firstChild.value
            const request = new XMLHttpRequest()
            request.open("GET", '/find_friendss?search_term=' + search_term, true)
            request.onload = () => {
                const response = JSON.parse(request.responseText)
                console.log(response)
                this.setState({
                    page: 'search_results',
                    results: response.users,
                })
            }
            request.send()
        }
        
        load_more_posts = () => {
            document.querySelector('.load_more_posts_p').style.display = 'none';
            document.querySelector('.loader').style.display = 'block';
            const data = {page_number: this.state.post_page + 1}
            const csrftoken = Cookies.get('csrftoken')
            const request = new XMLHttpRequest()
            request.open('POST', '/sandbox', true)
            request.setRequestHeader('X-CSRFToken', csrftoken);
            request.setRequestHeader('Content-Type', "text/plain;charset=UTF-8");
            request.onload = () => {
                const response  =  JSON.parse(request.responseText)
                console.log(response.posts)
                if (response.posts === 'No more posts'){
                    document.querySelector('.load_more_posts_p').innerHTML = response.posts
                    document.querySelector('.load_more_posts_p').style.display = 'block';
                    document.querySelector('.loader').style.display = 'none';
                }
                else {
                    const more_posts = this.state.posts.concat(response.posts)
                    this.setState({
                    posts:more_posts,
                    post_page: this.state.post_page + 1,
                })
                console.log('line 364')
                console.log(typeof(response.posts))
                document.querySelector('.load_more_posts_p').style.display = 'block';
                document.querySelector('.loader').style.display = 'none';
                document.querySelector('.load_more_posts_p').innerHTML = 'Load even more posts'
                }
                
            }
            request.send(JSON.stringify(data))
        }
        
        load_more_friends_posts = () => {
            document.querySelector('.load_more_posts_p').style.display = 'none';
            document.querySelector('.loader').style.display = 'block';
            if (this.state.page === 'profile'){
                var dataa = {friend: this.state.user, page_number: this.state.post_page + 1}
            }
            else {
                var dataa = {friend: this.state.page, page_number: this.state.post_page + 1}
            }
            
            const csrftoken = Cookies.get('csrftoken')
            const request = new XMLHttpRequest()
            request.open('POST', '/friends_profile_sandbox', true)
            request.setRequestHeader('X-CSRFToken', csrftoken);
            request.setRequestHeader('Content-Type', "text/plain;charset=UTF-8");
            request.onload = () => {
                const response  =  JSON.parse(request.responseText)
                console.log(response.posts)
                if (response.posts === 'No more posts'){
                    document.querySelector('.load_more_posts_p').innerHTML = response.posts
                    document.querySelector('.load_more_posts_p').style.display = 'block';
                    document.querySelector('.loader').style.display = 'none';
                }
                else {
                    const more_posts = this.state.posts.concat(response.posts)
                    this.setState({
                        posts: more_posts,
                        post_page: this.state.post_page + 1,
                    })
                    console.log('line 364')
                    console.log(typeof(response.posts))
                    document.querySelector('.load_more_posts_p').style.display = 'block';
                    document.querySelector('.loader').style.display = 'none';
                    document.querySelector('.load_more_posts_p').innerHTML = 'Load even more posts'
                }   
            }
            request.send(JSON.stringify(dataa))
        }

        hello = (user) => {
            console.log('hello is being calleDDDDD')
            console.log('This is the user :', user)
            var now = new Date()
            now.setHours(now.getHours() + 5);
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

        render() {
            return (
                <div id='app'>
                    <Navbar
                        user={this.state.user}
                        profile_pic={this.state.profile_pic}
                        profile={this.profile}
                        main={this.main}
                        search_friends={this.search_friends}
                        
                    />
                    <Main
                        posts={this.state.posts}
                        profile_pic={this.state.profile_pic}
                        user={this.state.user}
                        page={this.state.page}
                        first={this.state.first}
                        last={this.state.last}
                        dob={this.state.dob}
                        email={this.state.email}
                        update_profile_pic={this.update_profile_pic}
                        save_new_pic={this.save_new_pic}
                        handleClick={this.handleClick}
                        deletePost={this.deletePost}
                        friends_profile={this.friends_profile}
                        friend={this.state.friend}
                        request_friendship={this.request_friendship}
                        unfriend={this.unfriend}
                        results={this.state.results}
                        load_more_posts={this.load_more_posts}
                        load_more_friends_posts={this.load_more_friends_posts}
                        load_more_own_posts={this.load_more_own_posts}
                    />
                    <h4 >Friends</h4>
                    <Friends_sandbox
                        friends={this.state.friends}
                        user={this.state.user}
                        friends_profile={this.friends_profile}
                        hello={this.hello}
                    />
                    <h4 id='friend_request_title'>Friend Requests</h4>
                    <Friendship_requests_div_sandbox 
                        friend_requests={this.state.friend_requests}
                        friends_profile={this.friends_profile}
                        ignore={this.ignore_request}
                        confirm={this.confirm_request}
                    />
                </div>
            )
        }
    }

    ReactDOM.render(
        <App />,
        document.getElementById('root')
    )
}
request.send(JSON.stringify(data))