from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.utils import timezone
from django.utils.html import mark_safe
import arrow
# Create your models here.

class Friends(models.Manager):
    def are_they_friends(self):
        self.hello = 'hello'
        return self.hello



class User(AbstractUser):
    dob = models.DateField(blank=True, default=timezone.now)
    friends = models.IntegerField(default=0)
    profile_pic = models.ImageField(blank=True, upload_to='profile_pictures', default='profile_pictures/no_profile_pic/no_image.jpg')


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.localtime)
    text = models.TextField()
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.author} posted: {self.text}'




class Comment(models.Model):
    commentator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='person_with_an_opinion')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='commented_post')
    text = models.TextField()
    likes = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.localtime)

    def __str__(self):
        return f"{self.commentator} commented on post number {self.post}: {self.text}"


class Friendship(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requesting_user')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="confirming_user")
    pending = models.BooleanField(default=True)
    rejected = models.BooleanField(default=False)
    are_they_friends = models.BooleanField(default=False)
    date_requested = models.DateTimeField(auto_now_add=True)
    date_confirmed = models.DateTimeField(blank=True, null=True)
    
    objects = models.Manager()
    buddies = Friends()

    def __str__(self):
        if self.are_they_friends:
            return f'Are {self.sender} and {self.receiver} friends? Yes' 
        else:
            return f'Are {self.sender} and {self.receiver} friends? No' 


class Message(models.Model):
    conversation = models.ForeignKey(Friendship, on_delete=models.CASCADE, related_name='between')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='starting_user')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiving_user')
    date_sent = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return f'{self.sender} to {self.receiver}: {self.text} at {self.date_sent}'



class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='what_was_liked')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='who_liked_it')
    

    def __str__(self):
        return f'{self.user} liked {self.post}'


class Dislike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='what_was_disliked')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='who_disliked_it')
    

    def __str__(self):
        return f'{self.user} disliked {self.post}'



class Get_info(models.Manager):
    def info(self, request):
        user = request.user

        # prepare respone object
        response = {
            'user': user.username,
            'profile_pic': user.profile_pic.url,
            'posts': [],
            'friend_requests':[],
            'friends': [],
            'first': user.first_name,
            'last': user.last_name,
            'email': user.email,
            'dob': user.dob
            }
        print(response)
        
        # get friends
        sent = Friendship.objects.filter(sender=request.user, pending=False, rejected=False)
        received = Friendship.objects.filter(receiver=request.user, pending=False, rejected=False)
        friends = []

        for f in received:
            friends.append({'user': f.sender.username, 'profile_pic': f.sender.profile_pic.url, 'id': f.id})
    
        for s in sent:
            friends.append({'user': s.receiver.username, 'profile_pic':s.receiver.profile_pic.url, 'id': s.id})

        # get the last message (if it exists) that was sent to each friend
        for f in friends:
            friendship = Friendship.objects.get(id=f['id']) 
            message = Message.objects.filter(conversation=friendship).order_by('-date_sent')
            if len(message) != 0:
                print(f)
                f['last_message_date'] = message[0].date_sent.strftime("%a %b %d, %Y %H:%M:%S")
            else:
                f['last_message_date'] = 'No message was sent yet'

        response['friends'] = friends

        # get all posts
        posts = []

        # get your own posts
        own_posts = Post.objects.filter(author=request.user)
        for o in own_posts:
            # if it is a post and not an empty Queryset
            if type(o) == Post:
                posts.append(o)

        # get posts from friendships you've sent
        for s in sent:
            post = Post.objects.filter(author=s.receiver)

            # if the QuerySet is not empty
            if len(post) != 0:
                for p in post:
                    posts.append(p)

        # get posts from  friendships you've received
        for r in received:
            post = Post.objects.filter(author=r.sender)

            # if the queryset is not empty
            if len(post) != 0:
                for p in post:
                    posts.append(p)
        
        for post in posts:
            # get the comments
            comments = Comment.objects.filter(post=post)
            c = []

            # for each comment
            for comment in comments:
                c.append({
                'commentator': comment.commentator.username,
                'profile_pic': comment.commentator.profile_pic.url, 
                'text': comment.text, 
                'date':comment.date, 
                'likes': comment.likes,
                'id': comment.id})
            
            # sort the comments by date
            c.sort(key = lambda x:x['date'])
                
            # humanize the date for each comment
            for comment in c:
                comment['date'] = arrow.get(comment['date']).humanize()
            

            # get all the likes for this post
            l = Like.objects.filter(post=post)
            likes = []
            for like in l:
                likes.append({
                    'post_id': like.post.id,
                    'user': like.user.username,
                    'profile_pic': like.user.profile_pic.url
                })

            # get all the dislikes for this post
            d = Dislike.objects.filter(post=post)
            dislikes = []
            for dislike in d: 
                dislikes.append({
                    'post_id': dislike.post.id,
                    'user': dislike.user.username,
                    'profile_pic': dislike.user.profile_pic.url
                })
            
            # store all the data necessary for the post in response['response']
            response['posts'].append({
                'id': post.id, 
                'author': post.author.username, 
                'text': post.text, 
                'date': post.date, 
                'author_picture': post.author.profile_pic.url,
                'comments': c,
                'likes': likes,
                'dislikes': dislikes,
                }) 
        
        # sort by -date
        response['posts'].sort(key = lambda x:x['date'])
        response['posts'].reverse()
        
        #humanize the date for each post
        for post in response['posts']:
            post['date'] = arrow.get(post['date']).humanize()

        # get friend requests
        requests = Friendship.objects.filter(receiver=request.user, pending=True)
       
        for request in requests:
            response['friend_requests'].append({'sender': request.sender.username, 'sender_profile_pic': request.sender.profile_pic.url, 'id': request.id})
        
        return response

