// get all the necessasry info from the server 1) friend_requests 2) posts 3) friends

// create the App class 

const request = new XMLHttpRequest()
const csrftoken = Cookies.get('csrftoken');
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
                page: 'main'
            }
        }

        main = () => {          
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
            const request = new XMLHttpRequest()
            request.open("GET", '/get_own_posts', true)
            request.onload = () => {
                const response = JSON.parse(request.responseText)
                console.log(response)
                this.setState({
                    page: 'profile',
                    posts: response.response
                })
            }
            request.send()    
        }

        update_profile_pic = (e) => {
            document.querySelector(".profile_pic_in_popup").innerHTML = ''
            var image = document.createElement("IMG")
            image.width = 200
            image.src = URL.createObjectURL(e.target.files['0']);
            document.querySelector(".profile_pic_in_popup").appendChild(image)
            document.querySelector("#save_picture_button").style.display= 'inline-block';
        }

        save_new_pic  = () => {
            console.log('hello')
        }

        render() {
            return (
                <div id='app'>
                    <Navbar
                        user={this.state.user}
                        profile_pic={this.state.profile_pic}
                        profile={this.profile}
                        main={this.main}
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
                    />
                    <h4 >Friends</h4>
                    <Friends 
                        friends={this.state.friends}
                        user={this.state.user}
                    />
                    <h4 id='friend_request_title'>Friend Requests</h4>
                    <Friendship_requests_div 
                        friend_requests={this.state.friend_requests}
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
request.send()