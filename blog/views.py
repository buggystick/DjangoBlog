import boto3
from botocore.config import Config
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        return Post.objects.filter(published=True).order_by('-created_at')

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

def post_cover_redirect(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Check if user is authenticated or if post is public
    if not (request.user.is_authenticated or post.published):
        return HttpResponseForbidden("You do not have permission to access this media.")

    if not post.cover_image:
        return redirect('blog:post_list')

    # Generate presigned URL
    s3_client = boto3.client(
        's3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4', s3={'addressing_style': 'path'}),
        region_name=settings.AWS_S3_REGION_NAME
    )
    
    bucket = settings.MEDIA_BUCKET
    # The key in S3 includes the 'location' prefix from MediaStorage
    key = f"media/{post.cover_image.name}"
    
    presigned_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=300
    )
    return redirect(presigned_url)
