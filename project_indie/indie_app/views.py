from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Cripyto
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from storage_app.models import Publication, Like, UserProfile
from storage_app.forms import PublicationForm, CommentForm
from django.db.models import Count, OuterRef, Subquery, Q
from django.contrib.auth import get_user_model
from django.utils.translation import activate
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

User = get_user_model()

# Create your views here.

def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')

def services(request):
    return render(request, 'home/services.html')

def contact(request):
    return render(request, 'home/contact.html')



@login_required(login_url='indie_app:login')
def mainPage(request):
    activate('pt-br')
    
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    
    #feed_publications = Publication.objects.filter(is_public=True).order_by('-created_at')#[:10]

    # Buscar as 10 publicações mais recentes do usuário
    recent_publications = (
        Publication.objects
        .filter(author=request.user)
        .order_by('-created_at')[:10]
    )

    # Consulta todas as publicações públicas
    feed_publications = (
        Publication.objects
        .filter(is_public=True)
        .annotate(direct_comments_count=Count('comments', filter=Q(comments__parent__isnull=True)))
        .order_by('-created_at')
    )
    
    # Número de publicações a serem exibidas por página
    publications_per_page = 12

    # Página atual, obtida da solicitação GET
    page = request.GET.get('page')

    #Paginator para dividir as publicações em páginas
    paginator = Paginator(feed_publications, publications_per_page)
    
    try:
        feed_publications = paginator.page(page)
    except PageNotAnInteger:
        feed_publications = paginator.page(1)
    except EmptyPage:
        # Se a página solicitada estiver vazia, retorne a última página disponível
        feed_publications = paginator.page(paginator.num_pages)



    comment_form = CommentForm()  # Crie uma instância do formulário de comentário vazio
    form = PublicationForm()

    # Formatando a data e hora das publicações
    for publication in feed_publications:
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

    if request.method == 'POST':
        # Verifique se o formulário de comentário foi enviado
        if 'publication_id' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                # Processar o envio do formulário de comentário
                # Salvar o comentário, adicionar à publicação e redirecionar
                comment = comment_form.save(commit=False)
                comment.author = request.user
                comment.publication = Publication.objects.get(id=request.POST['publication_id'])
                comment.save()
                return redirect('indie_app:main')
        else:
            # Processar o envio do formulário de nova publicação
            form = PublicationForm(request.POST, request.FILES)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.save()
                form = PublicationForm()  # uma nova instância do formulário de nova publicação
                return redirect('indie_app:main')

    context = {
        'user_profile': user_profile,
        'feed_publications': feed_publications,
        'form': form,
        'comment_form': comment_form,  #  formulário de comentário 
        'recent_publications': recent_publications,
    }

    return render(request, 'main/main.html', context)




def SignupPage(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = form.save()
            
            # Criação do UserProfile para o novo usuário
            UserProfile.objects.create(user=user)
            
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "Sucesso!", extra_tags='success-message')
            return redirect('indie_app:login')
        else:
            messages.error(request, 'As senhas são diferentes. Tente novamente', extra_tags='success-message')
    else:
        form = CustomUserCreationForm()
    return render(request, 'home/register.html', {'form': form})


def LoginPage(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                #messages.success(request, 'Login successful. Welcome back!')
                return redirect('indie_app:main')
        else:
            messages.error(request, 'Inválido, Tente novamente', extra_tags='error-message')
            #return render(request, 'home/login.html', {'form': form})

    else:
        form = AuthenticationForm()
    return render(request, 'home/login.html', {'form': form})

@login_required
def LogoutPage(request):
    logout(request)
    return redirect('indie_app:login')