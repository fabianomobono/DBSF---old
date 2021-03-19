from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.utils import timezone
from django.utils.html import mark_safe
import arrow
from django.core.paginator import Paginator
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


# manager to get collect all the necessary info to display if the main page
class Get_info(models.Manager):
    def info(self, request, page_number):
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
        

        p = Paginator(response['posts'], 2)
        print('this is the page number')
        print(page_number)
        print(type(page_number))
        if page_number > p.num_pages:
            response['posts'] = 'No more posts'
        else:
            response['posts'] = p.page(page_number).object_list
       
        return response

# manager to get the data regarding one users post -- this is used when displaying a friends profile page or the users own 
# profile page
class Get_one_persons_posts(models.Manager):
    def posts(self, friend, request, page_number):
        friend_user = User.objects.get(username=friend)
        response = {'posts': []}
        # get all the users p osts 
        posts = Post.objects.filter(author=(User.objects.get(username=friend_user)))
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

        # humanize the date
        for p in response['posts']:
            p['date'] = arrow.get(p['date']).humanize()

        friendship_requested = Friendship.objects.filter(sender=request.user, receiver=friend_user)
        friendship_sent = Friendship.objects.filter(sender=friend_user, receiver=request.user)
        friendship_status = {'status': 'False'}
        
        # check the friendship status between the two users for button

        if friendship_requested.count() != 0:
            if friendship_requested[0].pending == True:            
                friendship_status['status'] = 'Pending'
            else:
                if friendship_requested[0].rejected == True:
                    friendship_status['status'] = 'Rejected'
                else: 
                    friendship_status['status'] = 'Friends'

        elif friendship_sent.count() != 0:
            if friendship_sent[0].pending == True:  
                friendship_status['status'] = 'Pending'
            else:
                if friendship_sent[0].rejected == True:
                    friendship_status['status'] = 'Rejected'
                else:
                    friendship_status['status'] = 'Friends'

        answer = {
            'posts': response['posts'],
            'user': request.user.username, 
            'profile_pic': friend_user.profile_pic.url, 
            'friend': friend_user.username, 
            'status': friendship_status['status'],
            'first': friend_user.first_name,
            'last': friend_user.last_name,
            'dob': friend_user.dob,
            'email': friend_user.email
            }
        
        # organize the posts using a pginator 
        p = Paginator(answer['posts'], 2)
        if page_number > p.num_pages:
            answer['posts'] = 'No more posts'
        else:
            answer['posts'] = p.page(page_number).object_list
        
        return answer