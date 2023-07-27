import json
import os
import equipamentos as equip
import plotter
from math import sqrt
from debug import alert
from debug import error
from debug import debug


'''COORDENADOR GERAL'''

# configurações gerais (variáveis globais)
temp=30 # temperatura do sistema
tipo_curva='' # tipo de curva do relé (IEC/IEEE/ANSI/KYLE/TD/OFF)
list_equipamentos={} #dicionario para exportar json
proj_filename=''
rede=None #object class Rede
transformacao=[] #lista de objetos transformador
protecao=[]
medicao=[]
consumo=[]


def start():

# importar dados de arquivo JSON do projeto - configuracoes gerais e equipamentos
    global proj_filename
    
    proj_filename=input('Entre com nome do arquivo ou novo projeto: ')
    if os.path.isfile(proj_filename+'.json'):
        with open(proj_filename+'.json', 'r') as categ_jsonfile:
            json_str = json.load(categ_jsonfile)
            list_equipamentos = json.loads(json_str)
            alert("Json file loaded successfully")
            
            load_equip(list_equipamentos)
            return 'file_loaded'
    elif proj_filename=='':
        proj_filename ='temp_proj'
        alert('Temp file created')
        return 'temp_file'
    else: 
        alert("No file loaded.")
        # global rede
        # rede=equip.Rede_publica()
        return 'no-file'

def load_equip(list_equipamentos):
    '''instanciar equipamentos do dicionario carregado do JSON'''
    
    # IMPORTA DADOS DE REDE
    global rede
    if 'rede' in list_equipamentos:
        rede=equip.Rede_publica(json=list_equipamentos['rede'])
    
    # IMPORTA TRANSFORMADORES
    global transformacao
    if 'transformacao' in list_equipamentos:
        list_transf=list(list_equipamentos['transformacao'])
        for json in list_transf:
            obj_transf1=equip.Transformador(json)
            transformacao.append(obj_transf1)            
 
    # IMPORTA EQUIPAMENTOS DE PROTECAO
    global protecao
    if 'protecao' in list_equipamentos:
        list_prot=list(list_equipamentos['protecao'])
        for json in list_prot:
            if 'tipo' in json:
                if json['tipo']=='rele':
                    item1=equip.Rele_secundario(json, Is=rede.partida1, beta=rede.beta)
                    protecao.append(item1)
                elif json['tipo']=='fusivel':
                    item2=equip.Fusivel_ELO(json=json)
                    protecao.append(item2)
                elif json['tipo']=='TC':
                    item3=equip.TC(json=json)
                    protecao.append(item3)

    # IMPORTA EQUIPAMENTOS DE MEDICAO
    global medicao
    if 'medicao' in list_equipamentos:
        list_med=list(list_equipamentos['medicao'])
        for json in list_med:
            if 'tipo' in json:
                if json['tipo']=='TP':
                    item4=equip.TP(json=json)
                    medicao.append(item4)

    # IMPORTA EQUIPAMENTOS DE CONSUMO
    global consumo
    if 'consumo' in list_equipamentos:
        list_cons=list(list_equipamentos['consumo'])
        for json in list_cons:
            if 'tipo' in json:
                if json['tipo']=='QGBT':
                    item5=equip.QGBT(json=json)
                    consumo.append(item5)


def menu():
    choice='-1'
    global rede
    while choice!='':
        choice=input('O que quer fazer? \n[0] Alterar dados de rede \n[1] Ver dados \
            \n[2] Adicionar Transformador \n[3] Recalcular Transformador \n[4] Plotar Coordenograma de Fase\
            \n[5] Plotar Coordenograma de Neutro\
            \n[6] Calcular Icc Rede \n[7] Adiciona TC \n[8] Corrente nominal \n[9] Salvar dados\
            \n[10] Adicionar/atualizar Relé \n[11] Adiciona Fusível \n[12] Altera fusível \n[13] Atualiza TC\
            \n[14] Adiciona TP \n[15] Atualiza TP\n[16] Adiciona QGBT \n[17] Atualiza QGBT\
            \n[ENTER] Sair\n: ')
        if choice=='0': #alterar dados de rede
            rede.update_rede()
        elif choice=='1': #alterar dados de rede
            ver_dados()
        elif choice=='2': #adicionar transformador ao sistema
            add_transformador()
        elif choice=='3': #recalcular transformadores
            option=input('Atualizar dados de (E)ntrada ou apenas (R)ecalcular?')
            if option.lower()=='e': 
                recalcular=False
            else: recalcular=True
            global list_equipamentos
            for transf1 in transformacao:
                print(transf1)
            opt_tranf=input("Digite o nome do transformador a recalcular (ou TODOS): ")
            for transf1 in transformacao:
                if transf1.name==opt_tranf or opt_tranf.lower()=='todos':
                    transf1.update_transf(recalcular)
                    alert('Calculo do transformador atualizado.')
                    # break
        elif choice=='4':
            plotar_coordenograma_fase()
        elif choice=='5':
            plotar_coordenograma_neutro()
        elif choice=='6':
            calcula_icc_rede()
        elif choice=='7':
            adiciona_TC()
        elif choice=='8':
            corrente_nominal()
        elif choice=='9':
            save_json()
        elif choice=='10':
            adiciona_rele()
        elif choice=='11':
            adiciona_fusivel()
        elif choice=='12':
            atualiza_fusivel()
        elif choice=='13':
            atualiza_TC()
        elif choice=='14':
            adiciona_TP()
        elif choice=='15':
            atualiza_TP()
        elif choice=='16':
            adiciona_QGBT()
        elif choice=='17':
            atualiza_QGBT()
        


def save_json():
    #reagrupar todos equipamentos e enviar para arquivo JSON
    # global dict_equipamentos
    global rede
    global transformacao
    global protecao
    global medicao
    global consumo
    
    #rede
    if rede is not None:
        list_equipamentos['rede']=rede.to_dict()
    
    #transformacao
    if len(transformacao)>0 :
        temp_list=[]
        for transf1 in transformacao: #transformar objetos em string para salvar em json
            str_transf=transf1.to_dict()
            temp_list.append(str_transf)
        list_equipamentos['transformacao']=temp_list
    
    
    #protecao
    if len(protecao)>0:
        temp_list=[]
        for item1 in protecao:
            str_items=item1.to_dict()
            temp_list.append(str_items)
        list_equipamentos['protecao']=temp_list

    #medicao
    if len(medicao)>0:
        temp_list=[]
        for item1 in medicao:
            str_items=item1.to_dict()
            temp_list.append(str_items)
        list_equipamentos['medicao']=temp_list
    
    #consumo
    if len(consumo)>0:
        temp_list=[]
        for item1 in consumo:
            str_items=item1.to_dict()
            temp_list.append(str_items)
        list_equipamentos['consumo']=temp_list


    #dump
    categ_json = json.dumps(list_equipamentos)
    
    # global proj_filename
    with open(proj_filename+'.json', 'w') as categ_jsonfile:
        json.dump(categ_json, categ_jsonfile, indent=2)
        alert("Json file updated")

def ver_dados(ver_rede=True, ver_transf=True, ver_rele=True, ver_medicao=True, ver_consumo=True):
    if ver_rede:
        global rede
        print(rede)

    if ver_transf:
        global transformacao
        for transf1 in transformacao: #transformar objetos em string para salvar em json
                print(transf1)
    
    if ver_rele:
        global protecao
        for item1 in protecao:
            print(item1)

    if ver_medicao:
        global medicao
        for item1 in medicao:
            print(item1)

    if ver_consumo:
        global consumo
        for item1 in consumo:
            print(item1)

# importar dados de catálogos e preços PainelConstru

# se nao tiver dados, pedir ao usuário
# ao final, atualizar os dados do arquivo JSON


# REDE



    # dados de entrada do cliente:

def calcula_icc_rede():
    global rede
    global transformacao
    Z_transf=0
    Z_int1=0
    for n,transf1 in enumerate(transformacao):
        if n==0:
            Z_int1=(1/transf1.Z_ohm)
        else:
            Z_int1=(1/Z_transf)+(1/transf1.Z_ohm) #impedancias internas dos transformadores
        Z_transf=1/Z_int1
    
    rede.calcula_Icc(Z_transf)

def dimensionar_cabo_entrada():
    pass


# dados de rede

        
def corrente_nominal():
    #Corrente nominal considerando a demanda contratada
    global rede
    rede.I_nom_dem=rede.dem_contr/(rede.Vb*sqrt(3)*rede.FP)
    print(f"I nom (demandada)= {rede.I_nom_dem}")

    #Corrente nominal considerando potencia instalada
    pot_inst=potencia_instalada()
    rede.I_nom_inst=pot_inst/(rede.Vb*sqrt(3)*rede.FP)
    print(f"I nom (instalada) = {rede.I_nom_inst}")


# MEDIÇÃO

def dimensionar_medicao():
    pass

def dimensionar_cabo_medicao_protecao():
    pass

# PROTEÇÃO SECUNDÁRIA

def dimensionar_protecoes():
    pass

def adiciona_rele():
    global protecao
    tem_rele=False
    choice=''
    for item1 in protecao:
        if type(item1)==equip.Rele_secundario: #relé secundário
            tem_rele=True
            print(item1)
            choice=input('Atualizar ou Adicinar novo? (a/novo) ').lower()
            if choice=='a':
                global rede
                item1.update_rele(Is=rede.partida1, I_inrush=inrush_total(), beta=rede.beta)
    if tem_rele==False or choice=='novo':
        print("Criar novo relé")
        rele1=equip.Rele_secundario(Is=rede.partida1, beta=rede.beta)
        protecao.append(rele1)
    

def adiciona_TC():

    dados=dados_gerais()

    tc1=equip.TC()
    tc1.update_tc(dados['Icc_max'], dados['I_Part_Mín'], dados['nominal_total'], dados["I_inrush_total"])
    
    
    # print(tc1.dimensiona_TC(bitola,distancia,Icc_max, Ip_min, I_nom1, inrush_total()))

    print(tc1)

    global protecao
    protecao.append(tc1)

def atualiza_TC():
    global protecao
    for tc1 in protecao:
        if tc1.tipo=="TC":
            print(tc1.to_dict())
    choice=input("Atualizar este? (s/n/del): ")
    if choice.lower()=='s':
        dados=dados_gerais()
        tc1.update_tc(dados['Icc_max'], dados['I_Part_Mín'], dados['I_nominal_total'], dados["I_inrush_total"])
    
    elif choice.lower()=='del':
        protecao.remove(tc1)

def adiciona_fusivel(I_nom=None):
    global protecao
    I_nom=input("I_Nominal ['8K','10K','12K','15K','20K','25K','30K','40K','50K','65K','80K','100K','2H','3H','5H']: ")
    fusivel1=equip.Fusivel_ELO(I_nom=I_nom)
    protecao.append(fusivel1)

def atualiza_fusivel():
    global protecao
    for fusivel1 in protecao:
        if fusivel1.tipo=='fusivel':
            print(fusivel1)
            choice=input("Atualizar este? (s/n/del): ")
            if choice.lower()=='s':
                I_nom=input("I_Nominal ['8K','10K','12K','15K','20K','25K','30K','40K','50K','65K','80K','100K','2H','3H','5H']: ")
                fusivel1.I_nom=I_nom
            elif choice.lower()=='del':
                protecao.remove(fusivel1)
    
def adiciona_TP():
    global rede
    global medicao
    tp1=equip.TP(V_prim=rede.Vb)
    # tp1.update_tp(V_prim=rede.Vb)

    print(tp1)

    medicao.append(tp1)

def atualiza_TP():
    global medicao
    for tp1 in medicao:
        if tp1.tipo=="TP":
            print(tp1.to_dict())
    choice=input("Atualizar este? (s/n/del): ")
    if choice.lower()=='s':
        tp1.update_tp()
    
    elif choice.lower()=='del':
        medicao.remove(tp1)

# TRANSFORMAÇÃO
I_inrush = 0 # somatório dos inrush dos transformadores
def inrush_total():
    
    return dados_gerais()['I_inrush_total']


def dados_gerais():
    global rede
    result={}

    #soma as correntes de Inrush do maior + nominal dos menores
    I_inrush_total=0
    I_nominal_total=0
    P_nominal_total=0
    global transformacao

    
    maior=0
    for n, transf1 in enumerate(transformacao):
        if n==0:
            I_inrush_total=transf1.I_inrush_real
        if transf1.I_inrush_real>I_inrush_total:
            I_inrush_total=transf1.I_inrush_real
            maior=n
            print(f'Maior I_inrush: {transf1.name}/t{transf1.I_inrush_real}')
    for n, transf1 in enumerate(transformacao):
        I_nominal_total+=transf1.I_nom1
        P_nominal_total+=transf1.pot_nom
        if n!=maior:
            I_inrush_total+=transf1.I_nom1
            print(f'I Nominais: {transf1.name}/t{transf1.I_nom1}')

    #organiza os dados necessarios para dimensionamento do TC:
    print(f'I_nominal_total: {P_nominal_total/rede.Vb}')
    result["I_nominal_total"]=P_nominal_total/rede.Vb
    print(f'I_inrush_total: {I_inrush_total}')
    result["I_inrush_total"]=I_inrush_total
    rede.I_inrush_total=I_inrush_total
    print(f'I_Part_Mín: {rede.TAP}')
    result['I_Part_Mín']=rede.TAP
    print(f'Icc_max: {rede.Icc_rede_3f}')
    result['Icc_max']=rede.Icc_rede_3f
    
    return result


def add_transformador():
    global transformacao
    transf1=equip.Transformador()
    # transf1.update_transf()
    transformacao.append(transf1)

def potencia_instalada():
    #soma as potencias de todos transformadores
    pot_total=0
    global transformacao
    for transf1 in transformacao:
        pot_total+=transf1.pot_nom
    print(f'Potência total instalada: {pot_total}')
    return pot_total

# GERAÇÃO

# CONSUMO
def demanda_total():
    pass

def pot_instalada():
    pass

def adiciona_QGBT():
    global consumo
    qgbt1=equip.QGBT()

    print(qgbt1)

    consumo.append(qgbt1)

def atualiza_QGBT():
    global consumo
    for n, qgbt1 in enumerate(consumo): #listar todos quadros
        if qgbt1.tipo=="QGBT":
            print(f'[{n}]\t{qgbt1.to_dict()}')
    print('\n')
    for n, qgbt1 in enumerate(consumo): #escolher quadro pra alterar
        if qgbt1.tipo=="QGBT":
            print(f'[{n}]\t{qgbt1.to_dict()}')
            choice=input("Atualizar este? (s/n/del): ")

            if choice.lower()=='s':
                choice=input("Escolha o parâmetro para ajuste: \n[0] Atualiza tudo \n[1] Nome \n[2] Tensão de linha \n[3] Potência instalada \n[4] Potencia demandada \n[5] Nro de fases \n[6] Alimentador \n[9] Apenas recalcular:\n")
                qgbt1.update_qgbt(choice=choice)
            
            elif choice.lower()=='del':
                consumo.remove(qgbt1)


# FUNÇÕES GLOBAIS

def plotar_coordenograma_fase(show_inrush=False):
    '''Plotar ponto ANSI, curto-circuitos, ELO, H-H, relé/disjuntor, Corrente de partida '''
    curvas=[]
    num=1
    altura=0.2

    #DADOS DE REDE (Icc)
    global rede
    # plotar curto circuito
    curvas.append(([rede.Icc_rede_3f,rede.Icc_rede_3f],[0,2],num,f'({num})Icc_rede_3f')) #(([curvax],[curvay]), nome)  curva2=([3],[16],'teste')
    # plotar corrente nominal demanda do sistema
    num+=1
    curvas.append(([rede.I_nom_dem,rede.I_nom_dem],[0,2],num,f'({num})I_nom_dem')) 
    # plotar corrente nominal demanda do sistema
    num+=1
    curvas.append(([rede.I_nom_inst,rede.I_nom_inst],[0,2],num,f'({num})I_nom_inst')) 
    # inrush (corr de magnetização):
    inrush_tot=inrush_total()
    num+=1
    curvas.append(([inrush_tot,inrush_tot],[0,0.1],num,f'({num})I_Inrush_tot'))
    
    #TRANSFORMACAO (Pto ANSI e Icc)
    global transformacao
    for transf1 in transformacao: #abrir Icc e Tansi de cada trafo
        
        # Plotar corrente nominal
        num+=1
        curvas.append(([transf1.I_nom1,transf1.I_nom1],[0,altura], num,f'({num})I_nom_'+transf1.name))
        altura=altura*2
        
        # plotar ponto ANSI
        num+=1
        curvas.append((transf1.Pt_ANSI[0],transf1.Pt_ANSI[1],num,f'({num})ANSI_'+transf1.name)) #(([curvax],[curvay]), nome)  curva2=([3],[16],'teste')
        
        if show_inrush==True:
            # Plotar inrush de cada transfo
            num+=1
            curvas.append(([transf1.I_inrush,transf1.I_inrush],[0,0.1], num,f'({num})Inrush_'+transf1.name))
        
        
        
        # plotar Curto-circuito
        # num+=1
        # curvas.append(([transf1.Icc1,transf1.Icc1],[0,altura],num,f'({num})Icc1_'+transf1.name))
    
    

    # RELÉ SECUNDÁRIO
    global protecao
    for item in protecao:
        num+=1
        if type(item)==equip.Rele_secundario: #relé secundário
            data_x, data_y, name=item.curva()
            curvas.append((data_x, data_y, num, f'({num}){name}'))
        elif item.tipo=='fusivel':
            if item.uso=='geral' or (item.uso=='transformador' and show_inrush==True):
                data_x, data_y, name=item.curva_min()
                curvas.append((data_x, data_y, num, f'({num}){name}'))
    
    #FUSÍVEIS


    
    # plotar curvas
    plotter.plotar(curvas)

    #ENERGISA:
        #  Valores de curto-circuito no ponto de derivação (fornecidos pela Concessionária).
        #  Curva (mínimo e máximo) de atuação dos fusíveis de proteção do ramal de ligação
        #  Corrente nominal (In).
        #  Corrente de partida do relé (Ip).
        #  Curva de tempo inversa do relé da proteção a montante para fase e terra (fornecida pela Concessionária).
        #  Curva de tempo inversa do relé com os ajustes definidos no projeto (catálogo ou manual do relé) para fase e terra.
        #  Ajuste de atuação instantânea para fase e terra (reta perpendicular ao eixo das correntes).
        #  Curva(s) de atuação da proteção individual de cada transformador.
        #  Ponto ANSI do(s) transformador (es).
        #  Im do(s) transformador (es).
        # Deve ser considerado que:
        #  Deverão ser apresentados no mínimo 2 coordenogramas, sendo um para fase e um para neutro.

def plotar_coordenograma_neutro():
    '''Plotar ponto NANSI, Corrente de Partida de Neutro, 50N/51N, Icc Fase-Terra (mín) IM residual, '''
    curvas=[]
    num=1
    altura=0.8

    #REDE
    global rede
    # corrente de partida de neutro:
    curvas.append(([rede.TAP,rede.TAP],[0,altura],num,f'({num})I_partida_N'))
    
    # inrush  residual (corr de magnetização de neutro):
    num+=1
    inrush_tot_N=inrush_total()*rede.fator_Inr_resid
    curvas.append(([inrush_tot_N,inrush_tot_N],[0,altura],num,f'({num})I_Inrush_residual'))
    

    #TRANSFORMACAO (Pto NANSI e Icc)
    global transformacao
    for transf1 in transformacao: #abrir Icc e Tansi de cada trafo
        
        # plotar ponto NANSI
        num+=1
        curvas.append((transf1.Pt_NANSI[0],transf1.Pt_NANSI[1],num,f'({num})NANSI_'+transf1.name))

    # RELÉ SECUNDÁRIO
    global protecao
    for item in protecao:
        num+=1
        if type(item)==equip.Rele_secundario: #relé secundário
            data_x, data_y, name=item.curva_neutro()
            curvas.append((data_x, data_y, num, f'({num}){name}'))
        


    # plotar curvas
    plotter.plotar(curvas)


def relatorio():
    pass

def custo_total():
    pass


def lista_materiais():
    pass


def export_mapa_conexoes():
    pass


if __name__ == '__main__': #Start program
    """Usado para iniciar e coordenar o sistema"""
    alert(start())
    menu()
    save_json()