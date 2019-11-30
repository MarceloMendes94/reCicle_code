from django.shortcuts               import render,redirect
from django.contrib.auth            import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models                        import Carteira, User, Cliente,Motorista,Empresa, Endereco,Coleta,Cupom, EmpresaCupom, Pesagem,Residuo
from .forms                         import ClienteForm, EnderecoForm, MotoristaForm, EmpresaForm
from .builder                       import DiretorCliente,DiretorEmpresa,DiretorMotorista
from django.contrib                 import messages
from django.views.decorators.csrf   import csrf_protect

def index(request):
    return render(request,'index.html')

def cadastro(request):
    return render(request, 'cadastro.html', {})
     


# INICIO TELAS DE CADASTRO
def cliente_cadastro(request): 
    clienteform  = ClienteForm()
    enderecoform = EnderecoForm()
    if request.POST:
        #user fields
        nome        = request.POST.get('nome')
        sobrenome   = request.POST.get('sobrenome')
        senha       = request.POST.get('password')
        email       = request.POST.get('email')
        #endereco fields
        estado      = request.POST.get('estado')
        cep         = request.POST.get('cep')
        cidade      = request.POST.get('cidade')
        bairro      = request.POST.get('bairro')
        logradouro  = request.POST.get('logradouro')
        numero      = request.POST.get('numero')
        referencia  = request.POST.get('referencia')
        #FIELDS CLIENTE
        cpf  = request.POST.get('cpf')
        data_nascimento  = request.POST.get('data_nascimento')        
        DiretorCliente(nome,sobrenome,senha,email,estado,cep,cidade,bairro,logradouro,numero,referencia,cpf,data_nascimento)
    return render(request,'cliente_cadastro.html',{'clienteform':clienteform,'enderecoform':enderecoform})

def motorista_cadastro(request):
    motoristaform = MotoristaForm()
    enderecoform = EnderecoForm()
    if request.POST:
        #fields USER
        nome        = request.POST.get('nome')
        sobrenome   = request.POST.get('sobrenome')
        senha       = request.POST.get('password')
        email       = request.POST.get('email')
        #fields ENDERECO
        estado      = request.POST.get('estado')
        cep         = request.POST.get('cep')
        cidade      = request.POST.get('cidade')
        bairro      = request.POST.get('bairro')
        logradouro  = request.POST.get('logradouro')
        numero      = request.POST.get('numero')
        referencia  = request.POST.get('referencia')        
        #fields MOTORISTA
        habilitacao = request.POST.get('habilitacao')
        placa = request.POST.get('placa')
        DiretorMotorista(nome,sobrenome,senha,email,estado,cep,cidade,bairro,logradouro,numero,referencia,habilitacao,placa)
    return render(request, 'motorista_cadastro.html', {'motoristaform': motoristaform, 'enderecoform': enderecoform})

def empresa_cadastro(request):
    empresaform = EmpresaForm()
    enderecoform = EnderecoForm()
    if request.POST:
        #fields USER
        nome        = request.POST.get('nome')
        sobrenome   = request.POST.get('sobrenome')
        senha       = request.POST.get('password')
        email       = request.POST.get('email')
        #fields ENDERECO
        estado      = request.POST.get('estado')
        cep         = request.POST.get('cep')
        cidade      = request.POST.get('cidade')
        bairro      = request.POST.get('bairro')
        logradouro  = request.POST.get('logradouro')
        numero      = request.POST.get('numero')
        referencia  = request.POST.get('referencia')        
        #fields EMPRESA
        cnpj  = request.POST.get('cnpj')        
        razao_social  = request.POST.get('razao_social')        
        telefone  = request.POST.get('telefone')        
        #diretor
        DiretorEmpresa(nome,sobrenome,senha,email,estado,cep,cidade,bairro,logradouro,numero,referencia,cnpj,razao_social,telefone)
    return render(request, 'empresa_cadastro.html', {'form_empresa': empresaform, 'enderecoform': enderecoform})
# FIM TELAS DE CADASTRO



#INICIO DE TELAS DE AUTENTICACAO
def login_page(request):
    return render(request,'login.html')

def login_submit(request):
    if request.POST:
        user = authenticate(username=request.POST.get('email'),password=request.POST.get('password') )
        if user is not None:
            login(request, user)
            request.session['email'] = user.email
            typeof = typeUser(request.session['email'])
            return redirect('/{}/perfil/'.format(typeof))
        else:
            messages.error(request, "usuario ou senha invalidos.")

    return render(request,'login.html')

def logout_user(request):
    print(request.user)
    logout(request)
    return redirect('/login/')
#FIM DE TELAS DE AUTENTICACAO



# INICIO DE TELAS DE Cliente
@login_required(login_url='/login/')
def cliente_perfil(request):
    nome=getNome(request)
    return render(request,'cliente_perfil.html',{'nome':nome})

@login_required(login_url='/login/')
def pedir_coleta(request):
    clientes=Cliente.objects.all()
    for cliente in clientes:
        if(cliente.usuario.email==request.session['email']):
            print('achou')
            coleta=Coleta(cliente=cliente,aguardando=True)
            coleta.save()
    return render(request,'cliente_coleta.html')
# FIM DE TELAS DE Cliente



# INICIO DE TELAS DE MOTORISTA
@login_required(login_url='/login/')
def motorista_perfil(request):
    nome=getNome(request)
    return render(request,'motorista_perfil.html',{'nome':nome})

@login_required(login_url='/login/')
def visualizar_coletas(request):
    
    nome = getNome(request)
    result = Coleta.objects.filter(aguardando=True)
    coletas = []

    for i in result:
        coletas.append(i)

    return render(request,'motorista_coleta.html',{'coletas':coletas,'nome':nome})

@login_required(login_url='/login/')
def pesagem_coleta(request):
    return render(request,'motorista_pesagem.html')
# FIM DE TELAS DE MOTORISTA



# ADMIN INICIO
@login_required(login_url='/login/')
def admin_perfil(request):
    permissao = permValidador(type_user='admin',email=request.session['email']) 
    if(permissao==''): 
        return render(request,'admin_perfil.html')
    else:        
        return redirect(permissao)      

@login_required(login_url='/login/')
def painel_usuario(request):
    permissao = permValidador(type_user='admin',email=request.session['email']) 
    if(permissao==''):        
        clientes    = Cliente.objects.all()
        Motoristas  = Motorista.objects.all()
        return render(request,'admin_usuarios.html')  
    else:        
        return redirect(permissao)  

@login_required(login_url='/login/')
def relatorio_pesagens(request):
    pesagens = Pesagem.objects.all()
    peso_aux=0 
    for i in range(0,len(pesagens)):
        peso_aux=peso_aux+pesagens[i].peso        
    
    if request.POST:
        peso_aux=0 
        filtro = request.POST.get('filtro')
        if filtro=='0':
            pesagens = Pesagem.objects.all()
            for i in range(0,len(pesagens)):
                peso_aux=peso_aux+pesagens[i].peso   
        else:
            res = Residuo.objects.filter(nome_residuo=filtro)
            res=res[0]
            pesagens = Pesagem.objects.filter(residuo=res)
            for i in range(0,len(pesagens)):
                peso_aux=peso_aux+pesagens[i].peso 
            
    return render(request,'admin_rel_pesagens.html',{'pesagens':pesagens,'soma':peso_aux})

@login_required(login_url='/login/')
def relatorio_cupons(request):
    cupons=Cupom.objects.all()
    if request.POST:
        filtro = request.POST.get('filtro')
        if filtro=='00':
            cupons=Cupom.objects.all()
        else:
            cupons=Cupom.objects.filter(valor=int(filtro))
        #cupons=Cupom.objects.filter(valor=10)
    return render(request,'admin_rel_cupom.html',{'cupons':cupons})  
# ADMIN FIM



#INICIO FUNÇOES QUE TRATAM SESSAO
def getNome(request):
    result=User.objects.filter(email=request.session['email'])
    nome=result[0].first_name
    return nome

def typeUser(email):
    admins = User.objects.filter(is_superuser=True)
    for admin in admins:
        if (admin.email == email):
            return 'admin'

    clientes = Cliente.objects.all()
    for cliente in clientes:
        if (cliente.usuario.email == email):
            return 'cliente'

    motoristas = Motorista.objects.all()
    for motorista in motoristas:
        if (motorista.usuario.email == email):
            return 'motorista'

    empresas = Empresa.objects.all()
    for empresa in empresas:
        if (empresa.usuario.email == email):
            return 'empresa'

    return None

def permValidador(type_user,email):    
    typeof = typeUser(email)
    if type_user != typeof :
        print('permissão negada')        
        return '/{}/perfil/'.format(typeof)
    else:
        return ''      
#FIM FUNÇOES QUE TRATAM SESSAO    
