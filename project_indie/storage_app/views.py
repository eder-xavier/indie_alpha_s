from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Publication, UserProfile, Follow, Like, Attachment, Comment, Friendship
from .forms import PublicationForm, UserProfileForm, CommentForm, ReplyForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.utils.translation import activate
from django.contrib.humanize.templatetags.humanize import naturaltime


CustomUser = get_user_model()


#ADICiONAR PUBLICAÇÕES########################################################################
@login_required(login_url='indie_app:login')
def add_publication(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = PublicationForm(request.POST, request.FILES)
        if form.is_valid():
            publication = form.save(commit=False)
            publication.author = request.user
            #publication.is_public = not form.cleaned_data['is_public']
            publication.save()

            # Lidar com os anexos
            for uploaded_file in request.FILES.getlist('attachments'):
                if uploaded_file.content_type == 'application/x-directory':
                    # Trate como uma pasta (diretório)
                    attachment = Attachment(type=Attachment.PARENT_FOLDER, name=uploaded_file.name)
                else:
                    # Trate como um arquivo
                    attachment = Attachment(type=Attachment.FILE, name=uploaded_file.name, file=uploaded_file)

                attachment.save()
                publication.attachments.add(attachment)

            return redirect('indie_app:main')
    else:
        form = PublicationForm()

    context = {
        'user_profile': user_profile,
        'form': form
    }

    return render(request, 'main/add_publication.html', context)



# PROFILE ######################################################################################

@login_required(login_url='indie_app:login')
def user_profile(request, user_id):
    user_profile = UserProfile.objects.get(user_id=user_id)
    current_user = request.user

    # Verifique se o usuário atual está seguindo o perfil do usuário visitado
    is_following = False
    if current_user.is_authenticated:
        is_following = Follow.objects.filter(follower=current_user, followed=user_profile.user).exists()

    # Verifique se o usuário autenticado está visitando seu próprio perfil
    is_own_profile = current_user == user_profile.user if current_user.is_authenticated else False
    
    # Conte o número de seguidores do usuário visitado
    follower_count = Follow.objects.filter(followed=user_profile.user).count()

     # Conte o número de publicações públicas feitas pelo usuário
    public_posts_count = Publication.objects.filter(author=user_profile.user, is_public=True).count()

    # Obtenha as publicações públicas do usuário
    public_posts = Publication.objects.filter(author=user_profile.user, is_public=True).order_by('-created_at')


    context = {
        'current_user': current_user,
        'user_profile': user_profile,
        'is_following': is_following,
        'is_own_profile': is_own_profile,
        'follower_count': follower_count,  
        'public_posts_count': public_posts_count,
        'public_posts': public_posts,
    }

    return render(request, 'main/profile.html', context)



@login_required(login_url='indie_app:login')
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('storage_app:userprofile', user_id=user.id)

    else:
        form = UserProfileForm(instance=profile)

    context = {
        'user_profile': user_profile,
        'profile': profile,
        'form': form
    }

    return render(request, 'main/edit_profile.html', context)



#SEGUINDO #######################################################################
@login_required(login_url='indie_app:login')
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(CustomUser, id=user_id)

    if user_to_follow != request.user:
        Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)

    # Retorna um JSON
    return JsonResponse({'success': True})


@login_required(login_url='indie_app:login')
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
    Follow.objects.filter(follower=request.user, followed=user_to_unfollow).delete()

    # Retorna um JSON
    return JsonResponse({'success': True})    

@login_required(login_url='indie_app:login')
def toggle_follow(request, user_id):
    user_profile = UserProfile.objects.get(user_id=user_id)
    current_user = request.user

    # Verifique se o usuário atual está seguindo o perfil do usuário visitado
    is_following = Follow.objects.filter(follower=current_user, followed=user_profile.user).exists()

    if is_following:
        # Se o usuário já está seguindo, pare de seguir
        Follow.objects.filter(follower=current_user, followed=user_profile.user).delete()
        is_following = False
    else:
        # Caso contrário, comece a seguir
        Follow.objects.create(follower=current_user, followed=user_profile.user)
        is_following = True

    # Atualize o número de "seguindo" (following count)
    following_count = Follow.objects.filter(follower=current_user).count()

    response_data = {
        'is_following': is_following,
        'following_count': following_count,  # Atualize o número de "seguindo"
    }

    return JsonResponse(response_data)






#BIBLIOTECA#########################################################################

@login_required(login_url='indie_app:login')
def library(request):
    user = request.user
    user_publications = Publication.objects.filter(author=user).order_by('-created_at')#[:10]
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Formatando a data e hora das publicações
    for publication in user_publications:
        natural_time = naturaltime(publication.created_at)

        if ',' in natural_time:
            # 'dia' por 'dia(s) atrás'
            natural_time = natural_time.replace(',', ' e')

        if 'hora' in natural_time:
            # Adicione um espaço entre "horas" e "atrás" para evitar "horaatrás"
            natural_time = natural_time.replace('horaatrás', 'hora atrás')

        if 'horas' in natural_time:
            # Adicione um espaço entre "horas" e "atrás" para evitar "horaatrás"
            natural_time = natural_time.replace('horasatrás', 'horas atrás')

        # Personalize a exibição para unidades maiores de tempo
        if 'dia' in natural_time:
            # 'dia' por 'dia(s) atrás'
            natural_time = natural_time.replace('diaatrás', 'dia atrás')
        if 'dia' in natural_time:
            #  'dia' por 'dia(s) atrás'
            natural_time = natural_time.replace('diasatrás', 'dias atrás')
        if 'semana' in natural_time:
            #  'semana' por 'semana(s) atrás'
            natural_time = natural_time.replace('semanaatrás', 'semana(s) atrás')
        if 'mês' in natural_time:
            #  'mês' por 'mês(es) atrás'
            natural_time = natural_time.replace('mêsatrás', 'mês(es) atrás')
        if 'ano' in natural_time:
            #  'ano' por 'ano(s) atrás'
            natural_time = natural_time.replace('anoatrás', 'ano(s) atrás')

        publication.formatted_created_at = natural_time

    for publication in user_publications:
        if publication.image:
            publication.media_type = 'image'
        elif publication.video:
            publication.media_type = 'video'
        else:
            publication.media_type = 'text'

    context = {
        'user_publications': user_publications,
        'user_profile': user_profile,
    }

    return render(request, 'main/library.html', context)



@login_required(login_url='indie_app:login')
def edit_post(request, post_id):
    post = get_object_or_404(Publication, id=post_id, author=request.user)
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = PublicationForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('storage_app:library')

    else:
        form = PublicationForm(instance=post)

    context = {
        'user_profile': user_profile,
        'form': form,
        'post': post,
    }

    return render(request, 'main/edit_post.html', context)


@login_required(login_url='indie_app:login')
def view_publication(request, post_id):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    post = get_object_or_404(Publication, id=post_id)
    natural_time = naturaltime(post.created_at)

    context = {
        'post': post,
        'user_profile': user_profile,
    }

    return render(request, 'main/view_publication.html', context)

#LIKES #############################################################################
@login_required(login_url='indie_app:login')
def like_post(request, post_id):
    post = get_object_or_404(Publication, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, publication=post)

    if not created:
        like.delete()

    return redirect('indie_app:main')

@login_required(login_url='indie_app:login')
def like_post_ajax(request, post_id):
    post = get_object_or_404(Publication, id=post_id)
    user = request.user

    if user not in post.likes.all():
        post.likes.add(user)
        liked = True
    else:
        post.likes.remove(user)
        liked = False

    likes_count = post.get_likes_count()

    # Renderize o contador de likes como uma string
    likes_count_html = render_to_string('main/likes_count.html', {'likes_count': likes_count})

    response_data = {
        'liked': liked,
        'likes_count': likes_count_html,  # Inclua o HTML renderizado do contador de likes
    }

    return JsonResponse(response_data)






################## COMENTARIOS ################################################
@login_required(login_url='indie_app:login')
@csrf_exempt
def add_comment(request, publication_id):
    # Verifique se a publicação existe
    publication = get_object_or_404(Publication, id=publication_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.publication = publication
            comment.save()

            # Crie uma lista de dicionários com os comentários
            comments_data = [{'author': comment.author.username, 'text': comment.text}]

            return JsonResponse({'success': True, 'comments': comments_data})

    # Se o formulário não for válido ou a solicitação não for POST, retorne um JsonResponse com sucesso falso
    return JsonResponse({'success': False})

@login_required(login_url='indie_app:login')
def get_comment_count(request, publication_id):
    publication = get_object_or_404(Publication, id=publication_id)
    comment_count = publication.comments.count()

    return JsonResponse({'comment_count': comment_count})



@login_required(login_url='indie_app:login')
def view_comments(request, publication_id):
    publication = get_object_or_404(Publication, id=publication_id)
    comments = publication.comments.filter(parent=None)
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    for comment in comments:
        natural_time = naturaltime(comment.created_at)

        if ',' in natural_time:
            natural_time = natural_time.replace(',', ' e')

        if 'hora' in natural_time:
            natural_time = natural_time.replace('horaatrás', 'hora atrás')

        if 'horas' in natural_time:
            natural_time = natural_time.replace('horasatrás', 'horas atrás')

        if 'dia' in natural_time:
            natural_time = natural_time.replace('diaatrás', 'dia atrás')

        if 'dias' in natural_time:
            natural_time = natural_time.replace('diasatrás', 'dias atrás')

        if 'semana' in natural_time:
            natural_time = natural_time.replace('semanaatrás', 'semana(s) atrás')

        if 'mês' in natural_time:
            natural_time = natural_time.replace('mêsatrás', 'mês(es) atrás')

        if 'ano' in natural_time:
            natural_time = natural_time.replace('anoatrás', 'ano(s) atrás')

        comment.formatted_created_at = natural_time
        comment.replies_count = comment.replies.count()

        for reply in comment.replies.all():
            natural_time_reply = naturaltime(reply.created_at)

            if ',' in natural_time_reply:
                natural_time_reply = natural_time_reply.replace(',', ' e')

            if 'hora' in natural_time_reply:
                natural_time_reply = natural_time_reply.replace('horaatrás', 'hora atrás')

            if 'horas' in natural_time_reply:
                natural_time_reply = natural_time_reply.replace('horasatrás', 'horas atrás')

            if 'dia' in natural_time_reply:
                natural_time_reply = natural_time_reply.replace('diaatrás', 'dia atrás')

            if 'dias' in natural_time_reply:
                natural_time_reply = natural_time_reply.replace('diasatrás', 'dias atrás')

            if 'semana' in natural_time_reply:
                natural_time_reply = natural_time_reply.replace('semanaatrás', 'semana(s) atrás')

            if 'mês' in natural_time_reply:
                natural_time_reply = natural_time_reply.replace('mêsatrás', 'mês(es) atrás')

            if 'ano' in natural_time_reply:
                natural_time_reply = natural_time_reply.replace('anoatrás', 'ano(s) atrás')

            reply.formatted_created_at = natural_time_reply

    form = CommentForm()
    reply_form = ReplyForm() 

    context = {
        'user_profile': user_profile,
        'publication': publication,
        'comments': comments,
        'comment_form': form,
        'reply_form': reply_form,
    }

    return render(request, 'main/view_comments.html', context)



@login_required(login_url='indie_app:login')
@require_POST
def reply_to_comment(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent = parent_comment
            comment.publication = parent_comment.publication
            comment.save()
            return JsonResponse({
                'success': True,
                'reply_text': comment.text,
                'reply_author': comment.author.username,
                'replies_count': parent_comment.replies.count(),
                'formatted_created_at': naturaltime(comment.created_at)  # Formate a data com naturaltime
            })

    response_data = {
        'success': False,
    }

    return JsonResponse(response_data)

@login_required(login_url='indie_app:login')
@require_POST
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    if user not in comment.likes.all():
        comment.likes.add(user)
        liked = True
    else:
        comment.likes.remove(user)
        liked = False

    likes_count = comment.likes.count()

    response_data = {
        'liked': liked,
        'likes_count': likes_count,
    }

    return JsonResponse(response_data)

@login_required
def delete_comment(request, comment_id):
    # Verifique se o comentário existe e pertence ao usuário autenticado
    comment = get_object_or_404(Comment, pk=comment_id, author=request.user)

    # Exclua o comentário e todas as respostas associadas a ele
    comment.delete()

    # Responda com um JSON para indicar sucesso
    return JsonResponse({'deleted': True})


########### AMIZADE #############################################################
@login_required
def friend_requests(request):
    received_requests = Friendship.objects.filter(to_user=request.user, accepted=False)
    sent_requests = Friendship.objects.filter(from_user=request.user, accepted=False)
    
    context = {
        'received_requests': received_requests,
        'sent_requests': sent_requests,
    }
    
    return render(request, 'main/friend_requests.html', context)

@login_required
def send_friend_request(request, to_user_id):
    to_user = get_object_or_404(CustomUser, id=to_user_id)

    # Verifique se já existe uma solicitação de amizade pendente
    existing_request = Friendship.objects.filter(from_user=request.user, to_user=to_user, accepted=False).first()

    if not existing_request:
        Friendship.objects.create(from_user=request.user, to_user=to_user)
        response_data = {'status': 'success', 'message': 'Friend request sent successfully.'}
    else:
        response_data = {'status': 'error', 'message': 'Friend request already sent.'}

    return JsonResponse(response_data)
    
@login_required
def accept_friend_request(request, request_id):
    friendship_request = get_object_or_404(Friendship, id=request_id, to_user=request.user)
    friendship_request.accepted = True
    friendship_request.save()
    return redirect('friendship:friend_requests')

@login_required
def reject_friend_request(request, request_id):
    friendship_request = get_object_or_404(Friendship, id=request_id, to_user=request.user)
    friendship_request.delete()
    return redirect('friendship:friend_requests')

