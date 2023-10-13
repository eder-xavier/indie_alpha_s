import uuid
import asyncio
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Contact, Message, Group, GroupMessage
from storage_app.models import UserProfile
from .forms import MessageForm, GroupForm, GroupEditForm, ProfileForm, UserProfileForm
from django.conf import settings
from indie_app.models import CustomUser
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.db.models import F


@login_required
def inbox(request):
    contacts = Contact.objects.filter(user=request.user)
    friend_requests = Contact.objects.filter(contact=request.user, requested_by__isnull=False)
    user_profile = UserProfile.objects.get(user=request.user)
    contact_profiles = UserProfile.objects.filter(user__in=contacts.values_list('contact', flat=True))

    # Lista de grupos do usuário logado
    groups = Group.objects.filter(members=request.user)

    # Se o usuário enviou o formulário de criação de grupo
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.admins.add(request.user)
            group.save()
    else:
        form = GroupForm()

    context = {
        'contacts': contacts,
        'friend_requests': friend_requests,
        'user_profile': user_profile,
        'contact_profiles': contact_profiles,
        'groups': groups,
        'form': form,
    }
    return render(request, 'chat/inbox.html', context)

@login_required
def conversation(request, contact_username):
    contact_user = get_object_or_404(CustomUser, username=contact_username)
    conversation = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=contact_user )) | (Q(sender=contact_user) & Q(receiver=request.user))
    ).order_by('-timestamp')

    contacts = Contact.objects.filter(user=request.user)
    friend_requests = Contact.objects.filter(contact=request.user, requested_by__isnull=False)
    user_profile = UserProfile.objects.get(user=request.user)

    context = {
        'contact_username': contact_username,
        'conversation': conversation,
        'contacts': contacts,
        'friend_requests': friend_requests,
        'user_profile': user_profile,
    }
    return render(request, 'chat/conversation.html', context)

@login_required
def add_contact(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        username = request.POST['username']
        try:
            contact_user = CustomUser.objects.get(username=username)
            if contact_user == request.user:
                messages.error(request, 'Você não pode adicionar a si mesmo como contato.')
            elif Contact.objects.filter(user=request.user, contact=contact_user).exists():
                messages.error(request, 'Esse usuário já está na sua lista de contatos.')
            else:
                contact = Contact(user=request.user, contact=contact_user, requested_by=request.user)
                contact.save()
                messages.success(request, 'Solicitação de contato enviada com sucesso.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')
    #return redirect('letter_app:inbox')
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'chat/add_contact.html', context)

@login_required
def accept_friend_request(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, contact=request.user, requested_by__isnull=False)
    contact_user = contact.requested_by

    contact1 = Contact(user=request.user, contact=contact_user)
    contact1.save()

    contact2 = Contact(user=contact_user, contact=request.user)
    contact2.save()

    contact.delete()

    return redirect('letter_app:inbox')


async def send_message_via_websocket(sender, receiver, content):
    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()

    # Montar a mensagem a ser enviada
    message_data = {
        "type": "chat.message",
        "message": content,
        "sender": sender,
        "timestamp": timezone.now().isoformat(),
    }
    
    # Enviar a mensagem para o grupo de chat do destinatário
    await channel_layer.group_add(f"chat_{receiver}", sender)
    await channel_layer.group_send(f"chat_{receiver}", message_data)
    await channel_layer.group_discard(f"chat_{receiver}", sender)

@login_required
def send_message(request, contact_username):
    contact_user = get_object_or_404(CustomUser, username=contact_username)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            sender = request.user
            receiver = contact_user

            message = Message.objects.create(content=content, sender=sender, receiver=receiver)

            # Enviar a mensagem via WebSocket para atualização em tempo real
            send_message_via_websocket(sender.username, receiver.username, content)

            return redirect('letter_app:conversation', contact_username=contact_username)
    else:
        form = MessageForm()

    context = {
        'form': form,
        'contact_username': contact_username,
    }
    return render(request, 'chat/conversation.html', context)



@login_required
def group_list(request):
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Obter todos os grupos criados pelo usuário atual
    #groups_created_by_user = Group.objects.filter(creator=request.user)
    

    # Obter todos os grupos em que o usuário atual é membro
    #groups_user_is_member = Group.objects.filter(members=request.user)
    groups = Group.objects.filter(members=request.user)

    # Combina as duas listas em uma única lista
    #groups = list(groups_created_by_user) + list(groups_user_is_member)

    context = {
        'groups': groups,
        'user_profile': user_profile,
    }
    return render(request, 'chat/group_list.html', context)

@login_required
def group_detail(request, group_id):
    user_profile = UserProfile.objects.get(user=request.user)
    user_contacts = Contact.objects.filter(user=request.user)
    group = get_object_or_404(Group, id=group_id)

    groups = Group.objects.filter(members=request.user)

    is_admin = request.user in group.admins.all()
    is_member = request.user in group.members.all()

 # Obter os usernames dos membros do grupo
    member_usernames = [member.username for member in group.members.all()]

    # Obter os usernames dos administradores do grupo
    admin_usernames = [admin.username for admin in group.admins.all()]

    if request.method == 'POST':
        if 'add_member' in request.POST:
            member_id = request.POST['member_id']
            member = get_object_or_404(CustomUser, id=member_id)
            group.members.add(member)
        elif 'remove_member' in request.POST:
            member_id = request.POST['member_id']
            member = get_object_or_404(CustomUser, id=member_id)
            group.members.remove(member)
        elif 'add_admin' in request.POST:
            admin_id = request.POST['admin_id']
            admin = get_object_or_404(CustomUser, id=admin_id)
            group.admins.add(admin)
        elif 'remove_admin' in request.POST:
            admin_id = request.POST['admin_id']
            admin = get_object_or_404(CustomUser, id=admin_id)
            group.admins.remove(admin)

        group.save()
        
    
    context = {
        'group': group,
        'groups': groups,
        'user_profile': user_profile,
        'is_admin': is_admin,
        'is_member': is_member,
        'member_usernames': member_usernames,
        'admin_usernames': admin_usernames,
        'user_contacts': user_contacts,
    }
    return render(request, 'chat/group_detail.html', context)

@login_required
def create_group(request):
    user_profile = UserProfile.objects.get(user=request.user)
    groups = Group.objects.filter(members=request.user)

    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            # Salvar o grupo e seus membros (ajustar isso com base no modelo de Grupo)
            group = form.save(commit=False)
            group.creator = request.user
            group.save()
            form.save_m2m()  # Salvar os membros do grupo (usuários adicionados ao grupo)
            
            # Adicionar o usuário criador às listas de admins e members
            group.admins.add(request.user)
            group.members.add(request.user)
            return redirect('letter_app:inbox')

    else:
        form = GroupForm()

    context = {
        'groups': groups,
        'form': form,
        'user_profile': user_profile,
    }
    return render(request, 'chat/create_group.html', context )

@login_required
def group_chat(request, group_id):
    user_profile = UserProfile.objects.get(user=request.user)
    groups = Group.objects.filter(members=request.user)

    # Obtém o objeto do grupo com base no group_id
    group = get_object_or_404(Group, id=group_id)

    # Obtém todas as mensagens para este grupo
    messages = GroupMessage.objects.filter(group=group).order_by('-timestamp')

    context = {
        'group': group,
        'groups': groups,
        'messages': messages,
        'user_profile': user_profile,
    }

    return render(request, 'chat/group_chat.html', context)

@login_required
def send_group_message(request, group_id):
    if request.method == 'POST':
        content = request.POST['content']
        sender = request.user
        group = Group.objects.get(id=group_id)
        GroupMessage.objects.create(group=group, sender=sender, content=content)
    return redirect('letter_app:group_chat', group_id=group_id)


# View para adicionar um membro ao grupo
def add_contacts_to_group(request, group_id):
    if request.method == 'POST':
        group = get_object_or_404(Group, id=group_id)
        contact_ids = request.POST.getlist('selected_contacts')  # Obtenha a lista de IDs dos contatos selecionados

        # Adicione os contatos selecionados ao grupo
        for contact_id in contact_ids:
            contact = get_object_or_404(CustomUser, id=contact_id)
            group.members.add(contact)

        return redirect('letter_app:group_detail', group_id=group.id)
    
# View para editar informações do grupo
@login_required
def edit_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    
    if request.method == 'POST':
        # Obtenha os dados do formulário para editar o grupo e, em seguida, salve o grupo
        group.name = request.POST.get('name')
        group.description = request.POST.get('description')
        group.save()
    
    return redirect('letter_app:group_detail', group_id=group_id)

@login_required
def generate_invite_link(group):
    unique_code = str(uuid.uuid4())
    link = f"{settings.SITE_URL}/msg/join_group/{unique_code}/"
    return link

@login_required
def join_group(request, unique_code):
    group = Group.objects.get(invite_code=unique_code)
    group.members.add(request.user)
    return redirect('letter_app:group_detail', group_id=group.id)

@login_required
def edit_group(request, group_id):
    user_profile = UserProfile.objects.get(user=request.user)
    groups = Group.objects.filter(members=request.user)
    group = get_object_or_404(Group, id=group_id)
    

    if request.method == 'POST':
        form = GroupEditForm(request.POST, request.FILES, instance=group)
        if form.is_valid():
            form.save()
            return redirect('letter_app:group_detail', group_id=group.id)

    form = GroupEditForm(instance=group)

    context = {
        'group': group,
        'groups': groups,
        'user_profile': user_profile,
        'form': form,
    }
    return render(request, 'chat/edit_group.html', context)

@login_required
def promote_member(request, group_id, member_id):
    # Verifique se o usuário atual é um administrador do grupo
    group = Group.objects.get(id=group_id)
    if request.user not in group.admins.all():
        # Se o usuário não for um administrador, você pode retornar uma resposta de erro ou redirecioná-lo para algum lugar
        return redirect('letter_app:group_detail', group_id=group_id)

    # Obtenha o membro a ser promovido a administrador
    member = CustomUser.objects.get(id=member_id)

    # Adicione o membro à lista de administradores do grupo
    group.admins.add(member)
    group.save()

    return redirect('letter_app:group_detail', group_id=group_id)

@login_required
def remove_member(request, group_id, member_id):
    # Verifique se o usuário atual é um administrador do grupo
    group = Group.objects.get(id=group_id)
    if request.user not in group.admins.all():
        # Se o usuário não for um administrador, você pode retornar uma resposta de erro ou redirecioná-lo para algum lugar
        return redirect('letter_app:group_detail', group_id=group_id)

    # Obtenha o membro a ser removido do grupo
    member = CustomUser.objects.get(id=member_id)

    # Remova o membro do grupo
    group.members.remove(member)
    group.save()

    return redirect('letter_app:group_detail', group_id=group_id)

@login_required
def remove_admin(request, group_id, member_id):
    # Verifique se o usuário atual é um administrador do grupo
    group = Group.objects.get(id=group_id)
    if request.user not in group.admins.all():
        # Se o usuário não for um administrador, você pode retornar uma resposta de erro ou redirecioná-lo para algum lugar
        return redirect('letter_app:group_detail', group_id=group_id)

    # Obtenha o membro cuja função de admin será removida
    member = CustomUser.objects.get(id=member_id)

    # Remova o membro da lista de administradores do grupo
    group.admins.remove(member)
    group.save()

    return redirect('letter_app:group_detail', group_id=group_id)

@login_required
def leave_group(request, group_id):
    # Obtenha o grupo e o usuário atual
    group = Group.objects.get(id=group_id)
    user = request.user

    # Verifique se o usuário atual é um membro do grupo
    if user in group.members.all():
        # Remova o usuário do grupo
        group.members.remove(user)
        group.save()

    return redirect('letter_app:inbox')


@login_required
def delete_group(request, group_id):
    group = Group.objects.get(id=group_id)

    # Verifique se o usuário atual é o último administrador do grupo
    if request.user in group.admins.all() and group.admins.count() == 1:
        # Se o usuário atual é o último administrador, você pode apagar o grupo
        group.delete()
        return redirect('letter_app:inbox')
    else:
        # Caso contrário, retorne uma resposta proibida (403)
        return HttpResponseForbidden("Você não tem permissão para apagar este grupo.")