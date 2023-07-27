from math import sqrt
from math import ceil
import pprint
from math import sinh
from math import cosh
import requests
from debug import alert
from debug import error
from debug import debug
from debug import formulas
from debug import mostrar


# EQUIPAMENTOS DE REDE

class Rede_publica():
    """Classe de informações da rede da concessionária"""
    def __init__(self, json=None):
        self.name='Rede concessionária'
        self.nos_entrada=[]
        self.nos_saida=[]
        self.dict_rede={}
        # dados de rede fornecidos pela concessionária:
        self.dial_tempo=0 #multiplier #51 #51N
        self.I_p=0 #corrente partida 51
        self.curve='' # IEC-EI #50 #51N #idem var 'tipo_curva'
        self.partida1=0 #corrente de partida em amperes #50 #50N
        self.tempo1=0 #50 #50N
        self.partida2=0 #corrente de partida em amperes #51NS
        self.tempo2=0 #51NS
        self.fator_D=0 #fator D para calculo de corrente de partida 
        self.TAP=0 #corrente de partida de neutro #51N
        self.fator_Inr_resid=0.2 #fator de multiplicacao para corrente inrush residual (de neutro)
        self.beta=0.2 #fator beta para calculo de corrente de partida de neutro #51N
        self.Z0_rede=complex(0,0) #impedância de rede da concessionária (a,b)==(real, imaginario)
        self.Z1_rede=complex(0,0) #impedância de rede da concessionária (a,b)==(real, imaginario)
        self.Z2_rede=complex(0,0) #impedância de rede da concessionária (a,b)==(real, imaginario) #se nao deu Z2, o Z1=Z2
        self.Icc_rede_3f=0 #corrente de curto-circuito da concessionária (A) trifásico
        self.Icc_rede_2f=0 #corrente de curto-circuito da concessionária (A) bifásico
        self.Icc_rede_1f=0 #corrente de curto-circuito da concessionária (A) monofásico
        self.Sb= 0 #(VA) #se nao der, considerar 100MVA
        self.Vb= 0 #(V)
        self.Zb= 0 #(ohm)
        self.Ib= 0 #(A)
        self.freq=60 #Hz
        self.pot_inst=0 #potência instalada
        self.dem_contr=0 #demanda contratada
        self.I_nom_dem=0 # corrente nominal pela demanda contratada
        self.I_nom_inst=0 # corrente nominal pela potencia instalada
        self.FP=0.92 # Fator de potência
        self.I_inrush_total=0


        if json is None:
            self.update_rede()

        else: #json possui informação
            if 'name' in json: self.name=json['name']
            if 'nos_entrada' in json: self.nos_entrada=json['nos_entrada']
            if 'nos_saida' in json: self.nos_saida=json['nos_saida']
            if 'Sb' in json: self.Sb= json['Sb']
            if 'Vb' in json: self.Vb= json['Vb']
            if 'Zb' in json: self.Zb= json['Zb']
            if 'Ib' in json: self.Ib= json['Ib']
            if 'dial_tempo' in json: self.dial_tempo=json['dial_tempo'] #multiplier #51 #51N
            if 'I_p' in json: self.I_p=json['I_p'] #corrente partida 51
            if 'curve' in json: self.curve=json['curve'] # IEC-EI #50 #51N #idem var 'tipo_curva'
            if 'partida1' in json: self.partida1=json['partida1'] #corrente de partida em amperes #50 #50N
            if 'tempo1' in json: self.tempo1=json['tempo1'] #50 #50N
            if 'partida2' in json: self.partida2=json['partida2'] #corrente de partida em amperes #51NS
            if 'tempo2' in json: self.tempo2=json['tempo2'] #51NS
            if 'TAP' in json: self.TAP=json['TAP'] #corrente de partida de neutro #51N
            if 'beta' in json: self.beta=json['beta'] #fator beta para calculo de partida do neutro
            if 'Z0_rede' in json: self.Z0_rede=complex(json['Z0_rede'][0],json['Z0_rede'][1])  #impedância de rede da concessionária (a,b)==(real, imaginario)
            if 'Z1_rede' in json: self.Z1_rede=complex(json['Z1_rede'][0],json['Z1_rede'][1]) #impedância de rede da concessionária (a,b)==(real, imaginario)
            if 'Z2_rede' in json: self.Z2_rede=complex(json['Z2_rede'][0],json['Z2_rede'][1]) #impedância de rede da concessionária (a,b)==(real, imaginario)
            if 'Icc_rede_3f' in json: self.Icc_rede_3f=json['Icc_rede_3f'] #corrente de curto-circuito da concessionária (A) trifásico
            if 'Icc_rede_2f' in json: self.Icc_rede_2f=json['Icc_rede_2f'] #corrente de curto-circuito da concessionária (A) biifásico
            if 'Icc_rede_1f' in json: self.Icc_rede_1f=json['Icc_rede_1f'] #corrente de curto-circuito da concessionária (A) monofásico
            if 'dem_contr' in json: self.dem_contr=json['dem_contr'] #demanda contratada (kW)
            if 'I_nom_dem' in json: self.I_nom_dem=json['I_nom_dem'] #Corrente nominal do sistema pela dem_contratada
            if 'I_nom_inst' in json: self.I_nom_inst=json['I_nom_inst'] #Corrente nominal do sistema pela potencia instalada
            if 'FP' in json: self.FP=json['FP'] #Fator de Potência
            if 'fator_D' in json: self.fator_D=json['fator_D'] #Fator D fornecido pela concessionaria
            if 'fator_Inr_resid' in json: self.fator_Inr_resid=json['fator_Inr_resid'] #fator de multiplicacao para corrente inrush residual (de neutro)
            if 'I_inrush_total' in json: self.I_inrush_total=json['I_inrush_total'] #
            

            

        print(self)
        
    def update_rede(self):
        print(self)
        choice=''
        while choice.isnumeric() is False:
            print(" \n[1] Alterar TUDO \
                    \n[2] Potência do sistema\
                    \n[3] Tensão do sistema\
                    \n[4] Impedância do sistema\
                    \n[5] Corrente do sistema\
                    \n[6] Demanda Contratada\
                    \n[7] Fator D (p/ corr. partida)\
                    \n[8] Fator beta (p/ corr. partida neutro)\
                    \n[9] Icc trifásico\
                    \n[10] Icc bifásico\
                    \n[11] Icc monofásico\
                    \n[12] FP\
                    \n[0] Sair")
            choice=input("O que deseja alterar? ")
        
        # Calculos PU
        if choice=='1' or choice=='2':
            self.Sb= input('Potência do sistema (MVA): ')
            if self.Sb !='': self.Sb=float(self.Sb)*1000000

        if choice=='1' or choice=='3':
            self.Vb= input('Tensão do sistema (kV): ')
            if self.Vb !='': self.Vb=float(self.Vb)*1000

        if choice=='1' or choice=='4':
            self.Zb= input('Impedância do sistema (%): ')
            if self.Zb !='': self.Zb=float(self.Zb)/100
            
        if choice=='1' or choice=='5':
            self.Ib= input('Corrente do sistema (A): ')
            if self.Ib !='': self.Ib=float(self.Ib)
        if choice=='1' or choice=='6':
            self.dem_contr= input('Demanda Contratada (kW): ')
            if self.dem_contr !='': self.dem_contr=float(self.dem_contr)*1000

        if choice=='1' or choice=='7':
            self.fator_D= input('Fator D (p/ corr. partida (padrão 1.25)): ')
            if self.fator_D !='': self.fator_D=float(self.fator_D)

        if choice=='1' or choice=='8':
            self.beta= input('Fator beta (p/ corr. partida neutro (padrão 0.2))): ')
            if self.beta !='': self.beta=float(self.beta)
            
        if choice=='1' or choice=='9':
            self.Icc_rede_3f= input('I_cc 3f: ')
            if self.Icc_rede_3f !='': self.Icc_rede_3f=float(self.Icc_rede_3f)

        if choice=='1' or choice=='10':
            self.Icc_rede_2f= input('I_cc 2f: ')
            if self.Icc_rede_2f !='': self.Icc_rede_2f=float(self.Icc_rede_2f)

        if choice=='1' or choice=='11':
            self.Icc_rede_1f= input('I_cc 1f: ')
            if self.Icc_rede_1f !='': self.Icc_rede_1f=float(self.Icc_rede_1f)

        if choice=='1' or choice=='12':
            self.FP= input('FP: ')
            if self.FP !='': self.FP=float(self.FP)
            else: self.FP=0.92
        
        if choice=='0':
            return None
        

        if self.Ib=='':
            self.Ib=self.Sb/(sqrt(3)*self.Vb)
            print(f'Ib={self.Ib} A')

        if self.Zb=='':
            self.Zb=self.Vb**2/(self.Sb)
            print(f'Zb={self.Zb} ohms')

        if self.Vb=='':
            self.Vb=self.Sb/(sqrt(3)*self.Ib)
            print(f'Vb={self.Vb} kV')

        if self.Sb=='':
            self.Sb=sqrt(3)*self.Vb*self.Ib
            print(f'Sb={self.Sb} MVA')

        self.I_nom_dem=self.dem_contr/(self.Vb*sqrt(3)*self.FP)
        print(f"I nom (contratada)= {self.I_nom_dem}")

        if self.fator_D!='' and self.I_nom_inst!='':
            self.partida1=self.I_nom_inst*self.fator_D
            if self.beta != '':
                self.TAP=self.partida1*self.beta
        
        self.TAP=self.partida1*self.beta


    def calcula_Icc(self,Z_interno):
        Icc_pu=1/(self.Zb+Z_interno)
        self.Icc_rede_3f= self.Ib*Icc_pu #calculo de Icc da rede
        print(f'Icc rede (pu): {Icc_pu}')
        print(f'Icc rede (A): {self.Icc_rede_3f} A')



    def __str__(self):
        self.to_dict()
        self.report()
        return str(self.to_dict())
        # return f'Sb: {self.Sb}\nVb: {self.Vb}\nZb: {self.Zb}\nIb: {self.Ib}'
        # pp=pprint.PrettyPrinter()
        # pp.pprint(self.to_dict())
        # return(self.to_dict())
    
    def report(self):

        # DADOS DE REDE ORGANIZADOS
        print('\n')
        alert('DADOS DE REDE')
        for nome, dados in self.dict_rede.items():
            mostrar(nome, dados)

        #FORMULA INRUSH
        formulas('I inrush: Corrente de Inrush')
        formulas('Maior I_mag + Σ I_nom Demais Trafos')
        mostrar('Inrush', self.I_inrush_total)
        print('\n')
        

    def to_dict(self):
        '''Saves the current classo to dict to export to JSON'''
        self.dict_rede['name']=self.name
        self.dict_rede['nos_entrada']=self.nos_entrada
        self.dict_rede['nos_saida']=self.nos_saida        
        self.dict_rede['Sb']=self.Sb
        self.dict_rede['Vb']=self.Vb
        self.dict_rede['Ib']=self.Ib
        self.dict_rede['Zb']=self.Zb
        self.dict_rede['dial_tempo']=self.dial_tempo #multiplier #51 #51N
        self.dict_rede['I_p']=self.I_p #corrente partida 51
        self.dict_rede['curve']=self.curve# IEC-EI #50 #51N #idem var 'tipo_curva'
        self.dict_rede['partida1']=self.partida1 #corrente de partida em amperes #50 #50N
        self.dict_rede['tempo1']=self.tempo1 #50 #50N
        self.dict_rede['partida2']=self.partida2 #corrente de partida em amperes #51NS
        self.dict_rede['tempo2']=self.tempo2 #51NS
        self.dict_rede['TAP']=self.TAP #corrente de partida de neutro #51N
        self.dict_rede['beta']=self.beta #fator beta para calculo de corrente de partida de neutro #51N
        self.dict_rede['Z0_rede']=[self.Z0_rede.real, self.Z0_rede.imag] #impedância de rede da concessionária (a,b)==(real, imaginario)
        self.dict_rede['Z1_rede']=[self.Z1_rede.real, self.Z1_rede.imag] #impedância de rede da concessionária (a,b)==(real, imaginario)
        self.dict_rede['Z2_rede']=[self.Z2_rede.real, self.Z2_rede.imag] #impedância de rede da concessionária (a,b)==(real, imaginario)
        self.dict_rede['Icc_rede_3f']=self.Icc_rede_3f
        self.dict_rede['Icc_rede_2f']=self.Icc_rede_2f
        self.dict_rede['Icc_rede_1f']=self.Icc_rede_1f
        self.dict_rede['dem_contr']=self.dem_contr
        self.dict_rede['I_nom_dem']=self.I_nom_dem
        self.dict_rede['I_nom_inst']=self.I_nom_inst
        self.dict_rede['FP']=self.FP
        self.dict_rede['fator_D']=self.fator_D
        self.dict_rede['fator_Inr_resid']=self.fator_Inr_resid
        self.dict_rede['I_inrush_total']=self.I_inrush_total
        return self.dict_rede

    

class Fusivel_ELO():
    """Classe de equipamento tipo fusivel elo"""
    def __init__(self, I_nom=None, json=None):
        self.nos_entrada=[]
        self.nos_saida=[]
        self.grupo='rede'
        self.name='Fusível ELO'
        self.tipos=['8K','10K','12K','15K','20K','25K','30K','40K','50K','65K','80K','100K','2H','3H','5H']
        self.I_nom=I_nom
        self.tipo='fusivel' #tipo escolhido entre os tipos
        self.dict_curva={}
        self.dict_fusivel={} #temp
        self.uso='geral' #o que ele está protegendo? geral / transformador
        
        if json is None:
            self.update_fusivel(I_nom)

        else: #json possui informação
            if 'name' in json: self.name=json['name']
            if 'nos_entrada' in json: self.nos_entrada=json['nos_entrada']
            if 'nos_saida' in json: self.nos_saida=json['nos_saida']
            if 'grupo' in json: self.grupo=json['grupo']
            if 'tipos' in json: self.tipos=json['tipos']
            if 'I_nom' in json: self.I_nom=json['I_nom']
            if 'tipo' in json: self.tipo=json['tipo']
            if 'uso' in json: self.uso=json['uso']
            
    
    def update_fusivel(self, I_nom=None):
        if I_nom is None:
            self.I_nom= input("I_Nominal ['8K','10K','12K','15K','20K','25K','30K','40K','50K','65K','80K','100K','2H','3H','5H']: ")
 

    def curva_min(self):
        '''Curva de fusão mínima'''
        self.dict_curva['6K']=([11,11,11,11,12,13,20,24,33,50,70,105,150,210],[300,100,50,20,10,5,2,1,0.5,0.2,0.1,0.05,0.02,0.01])
        self.dict_curva['12K']=([22,22,24,27,30,33,44,58,80,115,165,245,360,510],[300,100,50,20,10,5,2,1,0.5,0.2,0.1,0.05,0.02,0.01])
        self.dict_curva['25K']=([50,50,50,55,60,70,90,110,160,230,320,500,800,1100],[300,100,50,20,10,5,2,1,0.5,0.2,0.1,0.05,0.02,0.01])
        self.dict_curva['30K']=([62,62,65,70,80,90,120,150,210,310,440,630,1000,1400],[300,100,50,20,10,5,2,1,0.5,0.2,0.1,0.05,0.02,0.01])
        self.dict_curva['40K']=([80,80,85,90,100,110,140,200,260,400,600,800,1200,1800],[300,100,50,20,10,5,2,1,0.5,0.2,0.1,0.05,0.02,0.01])
        self.dict_curva['65K']=([120,120,125,140,150,180,240,310,440,650,900,1350,2000,3000],[300,100,50,20,10,5,2,1,0.5,0.2,0.1,0.05,0.02,0.01])
        self.dict_curva['100K']=([200,205,208,210,250,300,400,510,700,1100,1600,2400,3500,5000],[300,100,50,20,10,5,2,1,0.5,0.2,0.1,0.05,0.02,0.01])
        curva_x, curva_y=self.dict_curva[self.I_nom]
        return (curva_x,curva_y,self.name+' '+self.I_nom)






    def curva_max(self):
        '''Curva de fusão máxima'''
        self.dict_curva['12K']=([22,22,24,27,30,33,44,58,80,110,160,220,370,510],[300,100,50,20,10,5,2,1,0.5,0.2,0.1,0.05,0.02,0.01])
        self.dict_curva['25K']=([50,50,50,55,60,70,90,110,160,230,320,500,800,1100],[300,100,50,20,10,5,2,1,0.5,0.2,0.1,0.05,0.02,0.01])
        self.dict_curva['30K']=([62,62,65,70,80,90,120,150,210,310,440,630,1000,1400],[300,100,50,20,10,5,2,1,0.5,0.2,0.1,0.05,0.02,0.01])
        self.dict_curva['40K']=([80,80,85,90,100,110,140,200,260,400,600,800,1200,1800],[300,100,50,20,10,5,2,1,0.5,0.2,0.1,0.05,0.02,0.01])
        self.dict_curva['100K']=([200,205,208,210,250,300,400,510,700,1100,1500,2100,4200,5000],[300,100,50,20,10,5,2,1,0.5,0.2,0.1,0.05,0.02,0.01])
        curva_x, curva_y=self.dict_curva[self.I_nom]
        return (curva_x,curva_y,self.name+' '+self.I_nom)


    def to_dict(self):
        '''Saves the current classo to dict to export to JSON'''
        self.dict_fusivel['name']=self.name
        self.dict_fusivel['nos_entrada']=self.nos_entrada
        self.dict_fusivel['nos_saida']=self.nos_saida        
        self.dict_fusivel['grupo']=self.grupo
        self.dict_fusivel['name']=self.name
        self.dict_fusivel['I_nom']=self.I_nom
        self.dict_fusivel['tipo']=self.tipo
        self.dict_fusivel['uso']=self.uso
        return self.dict_fusivel

    def update_elo(self):
        '''Atualiza os parametros do fusivel'''

    def __str__(self):
        self.to_dict()
        self.report()
        return str(self.to_dict())

    def report(self):

        # DADOS DE FUSÍVEL ELO
        print('\n')
        alert('DADOS DO FUSÍVEL ELO')
        for nome, dados in self.dict_fusivel.items():
            mostrar(nome, dados)

        

# EQUIPAMENTOS DE MEDIÇÃO

# Para TC e TP de medição, usar classe de TC e TP na área de proteção

class medidor():
    """Classe de equipamento tipo medidor de energia"""
    def __init__(self):
        self.name='Medidor'
        self.nos_entrada=[]
        self.nos_saida=[]
        self.grupo='medicao'


# EQUIPAMENTOS DE PROTEÇÃO SECUNDÁRIA

class Rele_secundario():
    """Classe de equipamento tipo relé secundário"""
    def __init__(self, json=None, Is=None, I_instant=None, beta=None):
        self.name='Relé secundário'
        self.tipo='rele'
        self.nos_entrada=[]
        self.nos_saida=[]
        self.dict_rele={}
        self.protecoes=[] #50, 51, 50N, 51N, 50NS, 51NS, 81 frequencia, 27, 67, 32
        self.grupo='protecao'
        self.modelo=''
        self.Is=0
        self.Is_n=0

        self.dial_tempo=0.1
        self.tipo_curva='ti'
        if I_instant is None:
            self.instantaneo=1000
        else: 
            self.instantaneo=I_instant
        self.norma='iec'
        self.fator_M=1.2

        if json is None:
            self.update_rele(Is=self.Is)

        else: #json possui informação
            if 'name' in json: self.name=json['name']
            if 'nos_entrada' in json: self.nos_entrada=json['nos_entrada']
            if 'nos_saida' in json: self.nos_saida=json['nos_saida']
            if 'tipo' in json: self.tipo=json['tipo']
            if 'grupo' in json: self.grupo=json['grupo']
            if 'modelo' in json: self.modelo=json['modelo']
            if 'Is' in json: self.Is=json['Is']
            if 'Is_n' in json: self.Is_n=json['Is_n']
            if 'dial_tempo' in json: self.dial_tempo=json['dial_tempo']
            if 'tipo_curva' in json: self.tipo_curva=json['tipo_curva']
            if 'instantaneo' in json: self.instantaneo=json['instantaneo']
            if 'protecoes' in json: self.protecoes=json['protecoes']
            if 'norma' in json: self.norma=json['norma']
            if 'fator_M' in json: self.fator_M=json['fator_M'] # fator de multiplicacao para tirar I_instant a partir de I_Inrush

   
    def __str__(self):
        self.to_dict()
        self.report()
        return str(self.to_dict())

    def report(self):

        # DADOS DO RELÉ SECUNDÁRIO
        print('\n')
        alert('DADOS DO RELÉ SECUNDÁRIO')
        for nome, dados in self.dict_rele.items():
            mostrar(nome, dados)



    def update_rele(self, Is=None, I_inrush=None, beta=None):

        self.protecoes= input('Protecoes (50, 51, 50N, 51N, 50NS, 51NS, 81, 27, 67, 32): ')
        self.modelo= input('Modelo (ENTER para nenhum): ')
        if Is is None:
            self.Is= input('Corrente de partida (A): ')
        else:
            self.Is=Is
        if I_inrush is None:
            self.instantaneo=input('Instantâneo (A): ')
        else:
            self.instantaneo=I_inrush*self.fator_M
        self.dial_tempo=input('Dial de tempo (s): ')
        self.norma=input('Norma (IEC, IEEE, ANSI): ')
        self.tipo_curva=input('Tipo de curva (ti, tmi, tli, tei, tui): ')
        self.fator_M=input('Fator_M (para tirar I_instantâneo a partir de I_inrush) (%): ')

        if self.Is !='': self.Is=float(self.Is)
        if self.dial_tempo !='': self.dial_tempo=float(self.dial_tempo)
        if self.instantaneo !='': self.instantaneo=float(self.instantaneo)
        if self.fator_M !='': self.fator_M=float(self.fator_M)/100+1

        if Is is not None:
            self.Is=Is
            if beta is not None:
                self.Is_n=self.Is*beta

    def curva(self):
        step=1
        limite_seg=100 #limite de altura do grafico; limite de tempo em segundos
        curva_x=[]
        curva_y=[]
        for i in range(1,100000,step): 
            if i<self.instantaneo:
                result=curva_IEC(self.tipo_curva, self.dial_tempo, self.Is, i) #tipo, dial_tempo, corr_partida, I
            else:
                result=0
            if result is not None:
                if result<limite_seg:
                    curva_x.append(i)
                    curva_y.append(result)

            if result==0:
                break
            
            if i>100: step=10
            elif i>1000: step=100
            elif i>10000: step=1000
        # print(f'{result} s')
        
        #(([curvax],[curvay]), nome)
        return(curva_x,curva_y,'Rele_Fase')


    def curva_neutro(self):
        step=1
        limite_seg=100 #limite de altura do grafico; limite de tempo em segundos
        curva_x=[]
        curva_y=[]
        for i in range(1,100000,step): 
            if i<self.instantaneo:
                result=curva_IEC(self.tipo_curva, self.dial_tempo, self.Is_n, i) #tipo, dial_tempo, corr_partida, I
            else:
                result=0
            if result is not None:
                if result<limite_seg:
                    curva_x.append(i)
                    curva_y.append(result)

            if result==0:
                break
            
            if i>100: step=10
            elif i>1000: step=100
            elif i>10000: step=1000
        # print(f'{result} s')
        
        #(([curvax],[curvay]), nome)
        return(curva_x,curva_y,'Rele_Neutro')

    def to_dict(self):
        self.dict_rele['name']=self.name
        self.dict_rele['tipo']=self.tipo
        self.dict_rele['nos_entrada']=self.nos_entrada
        self.dict_rele['nos_saida']=self.nos_saida
        self.dict_rele['protecoes']=self.protecoes #50, 51, 50N, 51N, 50NS, 51NS, 81 frequencia, 27, 67, 32
        self.dict_rele['grupo']=self.grupo
        self.dict_rele['modelo']=self.modelo
        self.dict_rele['Is']=self.Is #corrente de partida
        self.dict_rele['Is_n']=self.Is_n #corrente de partida de neutro
        self.dict_rele['dial_tempo']=self.dial_tempo
        self.dict_rele['tipo_curva']=self.tipo_curva
        self.dict_rele['instantaneo']=self.instantaneo
        self.dict_rele['fator_M']=self.fator_M
        return self.dict_rele

class Fusivel_HH():
    """Classe de equipamento tipo fusível H-H"""
    def __init__(self):
        self.name='Fusível H-H'
        self.nos_entrada=[]
        self.nos_saida=[]
        self.grupo='protecao'

class Nobreak():
    """Classe de equipamento tipo nobreak"""
    def __init__(self):
        self.name='Nobreak'
        self.nos_entrada=[]
        self.nos_saida=[]
        self.fases=0
        self.pot_nominal=0
        self.FP=0
        self.grupo='protecao'

class Disjuntor_AT():
    """Classe de equipamento tipo disjuntor de alta tensão"""
    def __init__(self):
        self.name='Disjuntor AT'
        self.nos_entrada=[]
        self.nos_saida=[]
        self.grupo='protecao'


class TC():
    """Classe de equipamento tipo transformador de corrente para proteção ou medição"""
    def __init__(self,json=None):
        self.name='TC de proteção'
        self.nos_entrada=[]
        self.nos_saida=[]
        self.dict_TC={}
        self.grupo='' #protecao ou medicao
        self.tipo='TC' #Reconhecer como um TC
        self.modelo='' #barra, janela, enrolado, toróide
        self.RTC=0 #relação de TC
        self.I_p1=0 #corrente do primario 1 (P1 e P2)
        self.I_p2=0 #corrente do primario 2 (caso haja 1 primarios) (P3 e P4)
        self.fecham_prim='' #serie ou paralelo
        self.I_s1=0 #corrente do secundário 1
        self.I_s2=0 #corrente do secundário 2 (caso haja 2 secundários)
        self.fecham_sec='' #serie ou paralelo
        self.uso='' #interior/exterios
        self.isolamento='' #resibloc
        self.freq=60 #hertz
        self.U_max=0 #tensão máxima de isolamento do pino superior até a base (kV)
        self.impulso=0 #nível de impulso padrão
        self.f_term=0 #fator térmico
        self.I_t=0 #(*In) valor de curto-circuito simétrico que o TC aguenta. Dado em quantas vezes aguenta a corrente nominal pelo tempo de 1 segundo.
        self.I_din=0 #Corrente que aguenta por meio ciclo (normalmente 2,5X o I_t)
        self.exatidao=0
        self.TC_tipo='' #C=medicao B=protecao (baixa impedancia, alta saturacao); #NBR 6856 
        # 10 B 100: 10 é classe de exatidao até 10% de erro; B é protecao; 100 é a tensao na qual vai saturar, para considerar na hora de fazer calculo de saturacao.
        # 0,6 C 25: 0,6 é 0,6% (porque é medicao); C é medição; 25 é a carga que pode ser conectada no secundario
        self.Z_tc=0 # impedancia do TC
        self.consumo=0 # tensao de consumo do TC em VA
        #cargas padrao de consumo interno: 
        #                           eletromec   digital
        # multimedidores digitais   -           0.1 a 0.5
        #relés direcionais          25 a 40     2.5 a 6.5
        #relés de distância         10 a 15     2 a 8
        #relés diferenciais         8 a 15      2 a 8
        #relés de sobrecorrente     5 a 10      1.5 a 6
        self.z_burden=0 #carga nominal que pode ser conectada no TC
        self.I_nom=5 #corrente nominal do relé (normalmente 5A)
        self.I_max1=0 #corrente máxima do primário
        self.FS=0 #fator de sobrecorrente máximo, padronizado pela NBR6856
        self.V_sat=0 #tensão de saturação
        self.V_sec=0 #tensão no secundário quando do curto circuito no primario

        if json is None:
            self.update_tc()

        else: #json possui informação
            if 'name' in json: self.name=json['name']
            if 'nos_entrada' in json: self.nos_entrada=json['nos_entrada']
            if 'nos_saida' in json: self.nos_saida=json['nos_saida']
            if 'tipo' in json: self.tipo=json['tipo']
            if 'modelo' in json: self.modelo=json['modelo']
            if 'grupo' in json: self.grupo=json['grupo']
            if 'RTC' in json: self.RTC=json['RTC']
            if 'I_p1' in json: self.I_p1=json['I_p1']
            if 'I_p2' in json: self.I_p2=json['I_p2']
            if 'fecham_prim' in json: self.fecham_prim=json['fecham_prim']
            if 'I_s1' in json: self.I_s1=json['I_s1']
            if 'I_s2' in json: self.I_s2=json['I_s2']
            if 'fecham_sec' in json: self.fecham_sec=json['fecham_sec']
            if 'uso' in json: self.uso=json['uso']
            if 'isolamento' in json: self.isolamento=json['isolamento']
            if 'freq' in json: self.freq=json['freq']
            if 'U_max' in json: self.U_max=json['U_max']
            if 'impulso' in json: self.impulso=json['impulso']
            if 'f_term' in json: self.f_term=json['f_term']
            if 'I_t' in json: self.I_t=json['I_t']
            if 'I_din' in json: self.I_din=json['I_din']
            if 'exatidao' in json: self.exatidao=json['exatidao']
            if 'TC_tipo' in json: self.TC_tipo=json['TC_tipo']
            if 'Z_tc' in json: self.Z_tc=json['Z_tc']
            if 'consumo' in json: self.consumo=json['consumo']
            if 'I_nom' in json: self.I_nom=json['I_nom']
            if 'I_max1' in json: self.I_max1=json['I_max1']
            if 'FS' in json: self.FS=json['FS']
            if 'V_sat' in json: self.V_sat=json['V_sat']
            if 'V_sec' in json: self.V_sec=json['V_sec']

    def __str__(self):
        self.to_dict()
        self.report()
        return str(self.to_dict())

    def report(self):

        # DADOS DO TC
        print('\n')
        alert('DADOS DO TC')
        for nome, dados in self.dict_TC.items():
            mostrar(nome, dados)

    def update_tc(self, Icc_max, Ip_min, I_nom1, inrush_total):

        bitola=input("Bitola do cabo de comando do TC (mm²): ")
        distancia=input("Distancia do cabo de comando do TC (m): ")
        self.consumo_padrao()
        consumo=input("Consumo do TC (KVA) (sugestao 0.2): ")
        z_tc=input("Impedância do TC (ohms) (sugestao 0.2): ")
        z_burden=input("Impedância de Burden (ohms) (sugestao 1): ")
        # Icc_max=input("Maior corrente de curto (A): ")
        # Ip_min=input("Corrente de partida mínima (neutro) (A): ")
        # I_nom1=input("Corrente nominal dos transformadores (total) (A): ")
        # inrush_total=input("Inrush total (A): ")
        # I_tr1=input("Correntes dos transformadores somadas no primário: ")

        
        if bitola !='': bitola=float(bitola)
        if distancia !='': distancia=float(distancia)
        if Icc_max !='': Icc_max=float(Icc_max)
        if Ip_min !='': Ip_min=float(Ip_min)
        if I_nom1 !='': I_nom1=float(I_nom1)
        if inrush_total !='': inrush_total=float(inrush_total)
        if consumo !='': consumo=float(consumo)
        if z_tc !='': z_tc=float(z_tc)
        if z_burden !='': z_burden=float(z_burden)
        
        self.consumo=consumo #geralmente 0.2
        self.z_tc=z_tc #sugestao 0.2
        self.z_burden=z_burden #sugestao 1

        self.dimensiona_TC(bitola, distancia, Icc_max, Ip_min, I_nom1, inrush_total)

    def to_dict(self):
        self.dict_TC['name']=self.name
        self.dict_TC['nos_entrada']=self.nos_entrada
        self.dict_TC['nos_saida']=self.nos_saida
        self.dict_TC['tipo']=self.tipo
        self.dict_TC['modelo']=self.modelo
        self.dict_TC['grupo']=self.grupo
        self.dict_TC['RTC']=self.RTC
        self.dict_TC['I_p1']=self.I_p1
        self.dict_TC['I_p2']=self.I_p2
        self.dict_TC['fecham_prim']=self.fecham_prim 
        self.dict_TC['I_s1']=self.I_s1
        self.dict_TC['I_s2']=self.I_s2
        self.dict_TC['fecham_sec']=self.fecham_sec
        self.dict_TC['uso']=self.uso
        self.dict_TC['isolamento']=self.isolamento
        self.dict_TC['freq']=self.freq
        self.dict_TC['U_max']=self.U_max
        self.dict_TC['impulso']=self.impulso
        self.dict_TC['f_term']=self.f_term
        self.dict_TC['I_t']=self.I_t
        self.dict_TC['I_din']=self.I_din
        self.dict_TC['exatidao']=self.exatidao
        self.dict_TC['TC_tipo']=self.TC_tipo
        self.dict_TC['Z_tc']=self.Z_tc
        self.dict_TC['consumo']=self.consumo
        self.dict_TC['z_burden']=self.z_burden
        self.dict_TC['I_nom']=self.I_nom
        self.dict_TC['I_max1']=self.I_max1
        self.dict_TC['FS']=self.FS
        self.dict_TC['V_sat']=self.V_sat
        self.dict_TC['V_sec']=self.V_sec
        return self.dict_TC
    
    def dimensiona_TC(self, bitola_cabo, distancia, Icc_max, Ip_min, I_nom1, inrush_total):
        '''Dimensionamento de TC'''
        # distancia #metros # dist. TC até o relé
        # Ip_min # (A) corrente de partida (mínima)
        #I_tr1= correntes dos transformadores somadas no primário
        

        # DIMENSIONAMENTO DE TC

        # 0. CRITÉRIO DE CORRENTE NOMINAL DO PRIMARIO *******BASEADO NA CORRENTE DO PRIMARIO DO TRANSFORMADOR
        # baseado em https://www.youtube.com/watch?v=IfutKb4bZIc
        print(f"Corrente nominal do transformador I_nom1 = {I_nom1}\n*A corrente do TC precisa ser maior do que esse valor")

        # 1. CRITÉRIO DE SENSIBILIDADE
        #  A menor corrente de partida de ajuste do relé deve ser de no mínimo 10% a corrente nominal do TC de proteção
        #  pega a corrente de partida do neutro (pq é a menor)
        #  ex: se corrente mín de ajuste deve ser de 30A, entao 0,1 * Itc <= Ipmin ; Itc<=Ipmin/0,1 = 300A (a I max. do primário é de 300A)

        self.I_max1=Ip_min/0.1 # Tem que ler 10% da corrente de partida de neutro 
        self.RTC=self.I_max1/self.I_nom
        print(f"Corrente do TC IpTC = {self.I_max1}\t*A corrente do TC precisa ser menor do que esse valor")

        # 2. CRITÉRIO DE SATURAÇÃO
        #  A medida é a tensao reproduzida no secundario, dado uma carga no secundario.
        self.z_tc=0 #  Resistencia do TC
        z_cabo_km=ohm_km(bitola_cabo) #(resistencia do cabo em ohm/km)
        self.z_tc=0.2*self.z_burden #impedancia do TC
        z_cabo=(z_cabo_km * distancia) /1000 #impedancia total do cabo
        z_rele=self.consumo/(self.I_nom**2)
        self.V_sec=Icc_max/self.RTC*(self.z_tc+2*z_cabo+z_rele) #V_secundario tem q ser igual ou maior q essa
        print(f'A tensao de saturacao do secundario tem q ser maior que v_sec={self.V_sec} V') #Mesh recomenda dimensionar pelo menos 1.5X esse valor
        print(f'* Recomenda-se escolher ao menos 1.5X: {self.V_sec*1.5} V') #Mesh recomenda dimensionar pelo menos 1.5X esse valor

        #regra para saturação de TC:
        # para TC de medição 4X Ix e 4X Ip;
        # para TC de proteção 20X Ix e 20X Ip;
        #Fs=20 #fator de sobrecorrente máximo, padronizado pela NBR6856

        # 3. CORRENTE DE INRUSH DO TRANSFORMADOR ******A corrente do TC deve ser maior do que este valor
        # baseado no GED-2585 da CPFL
        #Corrente de Inrush é o nome que se dá à corrente elétrica de energização de um transformador, com ou sem carga em seu secundário, 
        #por uma fonte senoidal de tensão. É, portanto, uma corrente transitória e que pode atingir um valor de pico de mais de 20 (vinte) vezes, 
        #pelo menos, o valor de pico da corrente elétrica nominal. Consequentemente, para o transformador, a ocorrência do Inrush equivale a 
        #um curto-circuito.
        print(f"Iinrush real = {inrush_total} *A corrente do TC deve ser maior do que este valor")

        #DEVE ESCOLHER POR NOMENCLAURA ANTIGA E NOVA TAMBEM. ADICIONAR OS DETALHES DE TENSAO DE SATURACAO, PRECISAO, ETC.

        return self.escolhe_TC(I_nom1, inrush_total)

    def escolhe_TC(self, I_nom1, inrush_total):
        #ESCOLHA DO TC PELA ABNT
        #Dimensionamento de Transformador de Corrente NBR6856/2015
        # https://www.youtube.com/watch?v=7vai9hoq5lk

        TC_rel_list=[5,10,15,20,25,30,40,50,60,75,100,150,200,250,300,400,500,600,800,1000,1200,1500,2000,2500,3000,4000,5000,6000,8000]

        #TRANSF. PROTECAO
        #CARGAS COM FP=0.9 PARA CORRENTE NOMINAL SECUNDARIA 5A
        # DESIGNAÇÃO | RESISTÊNCIA | REATÂNCIA INDUTIVA | IMPEDÂNCIA
        pot_list_pr=[[2.5,0.09,0.044,0.1],[5,0.18,0.087,0.2],[12.5,0.45,0.218,0.5],[22.5,0.81,0.392,0.9],[45,1.62,0.785,1.8],[90,3.24,1.569,3.6]] #classes de potencia da norma, com FP=0.9 para corrente secundaria 5A

        exat_list=[5,10,15,20,30] #Fator de classe de exatidão

        #TRANSF. MEDICAO
        pot_list_med1=[1,2.5,4,5] #classes de potencia da norma, com FP=1 para corrente secundaria 1A
        pot_list_med09=[8,10,20] #classes de potencia da norma, com FP=0.9 para corrente secundaria 1A

        #A10 = PRECISÃO
        #F20 = FATOR DE SOBRECORRENTE DE 20
        #C12,5 = CLASSE DE EXATIDÃO PELA POTÊNCIA (s=z*i²; s=0,337*5² ; s=8,425va = 12,5)

        print("Resultados possíveis:")
        list_relacao=[]
        for relacao in TC_rel_list:
            if relacao>=self.RTC and I_nom1<=relacao and inrush_total<=relacao:
                print(f"{relacao} :5  Inom={I_nom1}<={relacao*5}\t I_inrush total {inrush_total} <={relacao}\tOK!")
                list_relacao.append(relacao)

        return list_relacao
    
    
    def consumo_padrao(self):
        tabela={}
        tabela['multimedidor digital']={'digital':'0,1 a 0,5'}
        tabela['reles direcionais']={'eletromecanico':'25 a 40', 'digital':'2,5 a 6,5'}
        tabela['reles de distancia']={'eletromecanico':'10 a 15', 'digital':'2 a 8'}
        tabela['reles diferenciais']={'eletromecanico':'8 a 15', 'digital':'2 a 8'}
        tabela['reles de sobrecorrente']={'eletromecanico':'5 a 10', 'digital':'1,5 a 6'}
        return tabela

class TP():
    """Classe de equipamento tipo transformador de potencial"""
    def __init__(self,json=None, V_prim=0):
        self.name='TP de proteção'
        self.nos_entrada=[]
        self.nos_saida=[]
        self.grupo='' #protecao ou medicao
        self.exatidao=0
        self.RTP=0 #relacao de transformacao
        self.V_prim=0 #tensão nominal de operação primário
        self.V_sec=115 #tensao secundario, geralmente 115 ou 115V3
        self.pot_term=0 #potência térmica
        self.Z_nom=0
        self.U_max=0
        self.tipo="TP"
        self.dict_TP={}

        if json is None:
            self.update_tp(V_prim=V_prim)

        else: #json possui informação
            if 'name' in json: self.name=json['name']
            if 'nos_entrada' in json: self.nos_entrada=json['nos_entrada']
            if 'nos_saida' in json: self.nos_saida=json['nos_saida']
            if 'grupo' in json: self.grupo=json['grupo']
            if 'RTC' in json: self.RTC=json['RTC']
            if 'exatidao' in json: self.exatidao=json['exatidao']
            if 'RTP' in json: self.RTP=json['RTP']
            if 'V_prim' in json: self.V_prim=json['V_prim']
            if 'V_sec' in json: self.V_sec=json['V_sec']
            if 'pot_term' in json: self.pot_term=json['pot_term']
            if 'Z_nom' in json: self.Z_nom=json['Z_nom']
            if 'U_max' in json: self.U_max=json['U_max']
            if 'tipo' in json: self.tipo=json['tipo']

    def to_dict(self):
        self.dict_TP['name']=self.name
        self.dict_TP['nos_entrada']=self.nos_entrada
        self.dict_TP['nos_saida']=self.nos_saida
        self.dict_TP['grupo']=self.grupo
        self.dict_TP['exatidao']=self.exatidao
        self.dict_TP['RTP']=self.RTP
        self.dict_TP['V_prim']=self.V_prim
        self.dict_TP['V_sec']=self.V_sec
        self.dict_TP['pot_term']=self.pot_term
        self.dict_TP['Z_nom']=self.Z_nom
        self.dict_TP['U_max']=self.U_max
        self.dict_TP['tipo']=self.tipo
        return self.dict_TP
        

    def update_tp(self, V_prim=0, V_sec=115):
        exatidao=input("Exatidão (%): ")
        if V_prim==0:
            V_prim=input("Tensão no primário (kV): ")
            if V_prim !='': V_prim=float(V_prim)*1000
        # V_sec=input("Tensão de saída: ")
        
        pot_term=input("Potência térmica máxima (VA): ")
        Z_Nom=input("Impedancia (ohms): ")
        U_Max=input("Tensão máxima de isolamento (kV): ")
        
                
        if exatidao !='': exatidao=float(exatidao)/100
        # if RTP !='': RTP=float(RTP)
        
        # if V_sec !='': V_sec=float(V_sec)
        if pot_term !='': pot_term=float(pot_term)
        if Z_Nom !='': Z_Nom=float(Z_Nom)
        if U_Max !='': U_Max=float(U_Max)*1000
        
        RTP=V_prim/V_sec
        
        self.exatidao=exatidao
        self.RTP=RTP
        self.V_prim=V_prim
        # self.V_sec=V_sec
        self.pot_term=pot_term
        self.Z_Nom=Z_Nom
        self.U_Max=U_Max

    def __str__(self):
        self.to_dict()
        self.report()
        return str(self.to_dict())

    def report(self):

        # DADOS DO TP
        print('\n')
        alert('DADOS DO TP')
        for nome, dados in self.dict_TP.items():
            mostrar(nome, dados)

class Religador():
    """Classe de equipamento tipo religador"""
    def __init__(self):
        self.name='religador'
        self.nos_entrada=[]
        self.nos_saida=[]
        self.grupo='protecao'

# EQUIPAMENTOS DE TRANSFORMAÇÃO

class Disjuntor_BT():
    """Classe de equipamento tipo disjuntor de baixa tensão"""
    def __init__(self):
        self.name='Disjuntor BT'
        self.nos_entrada=[]
        self.nos_saida=[]
        self.grupo='transformacao'

class Transformador():
    """Classe de equipamento tipo transformador"""
    def __init__(self, json=None):
        self.dict_transf={}
        self.name='Transformador'
        self.nos_entrada=[]
        self.nos_saida=[]
        self.pot_nom=0
        self.Z_ohm=0
        self.V_in=0
        self.V_out=0
        self.I_nom1=0 #corrente nominal no primario
        self.I_nom2=0 #corrente nominal no secundario
        self.entrada='' # estrela/triangulo
        self.saida='' # estrela/triangulo
        self.grupo='transformacao'
        self.Icc1=0
        self.Pt_ANSI=[] #[Iansi, Tansi]
        self.Pt_NANSI=[] #[Iansi, Tansi] de NEUTRO
        self.I_inrush=0
        self.I_inrush_real=0
        self.fator_mag=12 #quando o fabricante nao der uma corrente de magnetizacao, usar 10X a corrente nominal do equipamento (se a óleo). 12X se for transformador a seco.
        self.fases=3
        self.resfriamento='seco' #ou óleo
        

        if json is None:
            self.update_transf()
        
        else: #json possui informação
            if 'name' in json: self.name=json['name']
            if 'nos_entrada' in json: self.nos_entrada=json['nos_entrada']
            if 'nos_saida' in json: self.nos_saida=json['nos_saida']
            if 'pot_nom' in json: self.pot_nom=json['pot_nom']
            if 'Z_ohm' in json: self.Z_ohm=json['Z_ohm']
            if 'V_in' in json: self.V_in=json['V_in']
            if 'V_out' in json: self.V_out=json['V_out']
            if 'I_nom1' in json: self.I_nom1=json['I_nom1'] #corrente nominal no primario
            if 'I_nom2' in json: self.I_nom2=json['I_nom2'] #corrente nominal no secundario
            if 'entrada' in json: self.entrada=json['entrada'] # estrela/triangulo
            if 'saida' in json: self.saida=json['saida'] # estrela/triangulo
            if 'grupo' in json: self.grupo=json['grupo']
            if 'Icc1' in json: self.Icc1=json['Icc1']
            if 'Pt_ANSI' in json: self.Pt_ANSI=json['Pt_ANSI']
            if 'Pt_NANSI' in json: self.Pt_NANSI=json['Pt_NANSI']
            if 'I_inrush' in json: self.I_inrush=json['I_inrush']
            if 'I_inrush_real' in json: self.I_inrush_real=json['I_inrush_real']
            if 'fator_mag' in json: self.fator_mag=json['fator_mag']
            if 'fases' in json: self.fases=json['fases']
            if 'resfriamento' in json: self.resfriamento=json['resfriamento']



    def update_transf(self, recalcular=False):
        '''Atualizar os dados do transformador. Se recalcular==True, apenas atualiza os dados calculados com base nos dados de entrada'''
        if recalcular is False:
            #entradas do usuário:
            self.name= input('Nome do transformador: ')
            self.pot_nom= input('Potência nominal (kVA): ')
            self.V_in= input('Tensão de entrada (kV): ')
            self.V_out= input('Tensão de saída (linha) (V): ')
            self.Z_ohm= input('Impedância (%): ')
            self.resfriamento= input('Resfriamento (oleo/seco): ')

            if self.pot_nom !='': self.pot_nom=float(self.pot_nom)*1000
            if self.Z_ohm !='': self.Z_ohm=float(self.Z_ohm)/100
            if self.V_in !='': self.V_in=float(self.V_in)*1000
            if self.V_out !='': self.V_out=float(self.V_out)

            if self.resfriamento=='seco': self.fator_mag=12
            elif self.resfriamento=='oleo': self.fator_mag=10

        #calculo de corrente nominal
        if self.pot_nom!='' and self.V_in !='':
            self.I_nom1=self.pot_nom/(self.V_in*sqrt(3)) #no primario
        if self.pot_nom!='' and self.V_out !='':
            self.I_nom2=self.pot_nom/(self.V_out*sqrt(3)) #no secundario

        #calculo de Icc do transformador
        self.Icc1=self.I_nom1/self.Z_ohm #no primario
        self.Icc2=self.I_nom2/self.Z_ohm #no secundario

        # ponto ANSI
        Iansi=self.I_nom1/(self.Z_ohm)
        Tansi=(self.Z_ohm*100)**2/8
        self.Pt_ANSI=[Iansi,Tansi]
        self.Pt_NANSI=[Iansi*0.58,Tansi]
        print(f'Ansi: {self.Pt_ANSI}\nNansi:{self.Pt_NANSI}')


        self.calcula_inrush()

        choice=input("Calcular cabo secundário? (s/n)\n: ")
        if choice=="s":
            self.dimensiona_cabo_secundario()
    
    def __str__(self):
        self.to_dict()
        self.report()
        return str(self.to_dict())

    def report(self):

        # DADOS DO TRANSFORMADOR
        print('\n')
        alert('DADOS DO TRANSFORMADOR')
        for nome, dados in self.dict_transf.items():
            mostrar(nome, dados)
    
    def to_dict(self):
        '''Saves the current classo to dict to export to JSON'''
        self.dict_transf['name']=self.name
        self.dict_transf['nos_entrada']=self.nos_entrada
        self.dict_transf['nos_saida']=self.nos_saida
        self.dict_transf['pot_nom']=self.pot_nom
        self.dict_transf['Z_ohm']=self.Z_ohm
        self.dict_transf['V_in']=self.V_in
        self.dict_transf['V_out']=self.V_out
        self.dict_transf['I_nom1']=self.I_nom1
        self.dict_transf['I_nom2']=self.I_nom2
        self.dict_transf['entrada']=self.entrada
        self.dict_transf['saida']=self.saida
        self.dict_transf['grupo']=self.grupo
        self.dict_transf['Icc1']=self.Icc1
        self.dict_transf['Pt_ANSI']=self.Pt_ANSI
        self.dict_transf['Pt_NANSI']=self.Pt_NANSI
        self.dict_transf['I_inrush']=self.I_inrush
        self.dict_transf['I_inrush_real']=self.I_inrush_real
        self.dict_transf['fator_mag']=self.fator_mag
        self.dict_transf['fases']=self.fases
        self.dict_transf['resfriamento']=self.resfriamento
        return self.dict_transf

    def calcula_inrush(self):
        '''CORRENTE DE INRUSH DO TRANSFORMADOR ******A corrente do TC deve ser maior do que este valor
        baseado no GED-2585 da CPFL
        Corrente de Inrush é o nome que se dá à corrente elétrica de energização de um transformador, 
        com ou sem carga em seu secundário, por uma fonte senoidal de tensão. É, portanto, uma corrente
         transitória e que pode atingir um valor de pico de mais de 20 (vinte) vezes, pelo menos, o valor 
         de pico da corrente elétrica nominal. Consequentemente, para o transformador, a ocorrência do 
         Inrush equivale a um curto-circuito.'''
        self.I_inrush=self.I_nom1*self.fator_mag
        self.I_inrush_real=1/((1/self.Icc1)+(1/self.I_inrush))
        print(f"Iinrush real = {self.I_inrush_real} # A corrente do TC deve ser maior do que este valor")

    def dimensiona_cabo_secundario(self):
        print("Dimensionar cabo secundário: ")
        cabo1=Cabo_BT()
        comprimento=input('Qual o comprimento dos cabos do secundário (m)? ')
        if comprimento!='':comprimento=float(comprimento)
        cabo1.comprimento=comprimento
        queda_max_pc=input('Qual a queda de tensao maxima permitida (%)? ')
        if queda_max_pc!='':queda_max_pc=float(queda_max_pc)
        tensao_fase=self.V_out/sqrt(3)
        if queda_max_pc!='' and comprimento!='':
            cabo1.dimensionar_cabos(potencia_fase=self.pot_nom/self.fases,queda_max_pc=queda_max_pc,tensao_fase=tensao_fase)
            alert('Connecting to API to get updated prices...')
            preco=cabo1.get_price()
            if preco is not None:
                print(f'Preço para 1 m: R$ {preco}')
                print(f'Preço para {cabo1.comprimento} m: R$ {preco*cabo1.comprimento}')

# EQUIPAMENTOS DE GERAÇÃO

class Gerador():
    """Classe de equipamento tipo gerador"""
    def __init__(self):
        self.name='Gerador'
        self.nos_entrada=[]
        self.nos_saida=[]
        self.V_out=0
        self.pot_nom=0
        self.FP=0
        self.grupo='geracao'



# CABOS E BARRAS

# variáveis globais:
dict_ID_Prod={0.5:1230, 1:1232, 0.75:1231, 1.5:1233, 2.5:1239, 4:1268, 6:6406, 10:16, 16:17, 25:1241, 35:1222, 50:1270, 70:22, 95:1247, 120:321, 150:1236, 185:1217, 240:257, 300:1221, 400:1224, 500:1271, 630:0, 800:0, 1000:0}

class Cabo_BT():
    """Classe de componente tipo cabo de Baixa Tensão"""
    def __init__(self, name='Cabo BT', json=None, tensao_fase=None, comprimento=None, corrente_fase=None, queda_tensao=0.03):
        self.name=name
        self.nos_entrada=[]
        self.nos_saida=[]
        self.blindagem=''
        self.tensao_isolamento=0
        self.bitola_fase=0
        self.bitola_neutro=0
        self.bitola_terra=0
        self.pernas_fase=0
        self.pernas_terra=0
        self.material=''
        self.comprimento=comprimento
        self.I_max=0
        self.fator_agrup=None # nro de circuitos agrupados
        self.grupo='cabos/barras'
        self.resist_km=0 #resistência/km
        self.reat_km=0 #reatância/km
        self.Z=0 #impedância/km
        self.custo_alim=0 
        self.corrente_fase=corrente_fase
        self.tensao_fase=tensao_fase
        self.queda_tensao=queda_tensao
        self.fator_temp=None
        
        self.dict_cabo={}
        self.tipo='cabo'

        if json is None:
            self.update_cabo()

        else: #json possui informação
            if 'name' in json: self.name=json['name']
            if 'nos_entrada' in json: self.nos_entrada=json['nos_entrada']
            if 'nos_saida' in json: self.nos_saida=json['nos_saida']
            if 'blindagem' in json: self.blindagem=json['blindagem']
            if 'tensao_isolamento' in json: self.tensao_isolamento=json['tensao_isolamento']
            if 'bitola_fase' in json: self.bitola_fase=json['bitola_fase']
            if 'bitola_neutro' in json: self.bitola_neutro=json['bitola_neutro']
            if 'bitola_terra' in json: self.bitola_terra=json['bitola_terra']
            if 'pernas_terra' in json: self.pernas_terra=json['pernas_terra']
            if 'pernas_fase' in json: self.pernas_fase=json['pernas_fase']
            if 'material' in json: self.material=json['material']
            if 'comprimento' in json: self.comprimento=json['comprimento']
            if 'I_max' in json: self.I_max=json['I_max']
            if 'fator_agrup' in json: self.fator_agrup=json['fator_agrup']
            if 'grupo' in json: self.grupo=json['grupo']
            if 'resist_km' in json: self.resist_km=json['resist_km']
            if 'reat_km' in json: self.reat_km=json['reat_km']
            if 'Z' in json: self.Z=json['Z']
            if 'tipo' in json: self.tipo=json['tipo']
            if 'custo_alim' in json: self.custo_alim=json['custo_alim']
            if 'fator_temp' in json: self.fator_temp=json['fator_temp']
            if 'corrente_fase' in json: self.corrente_fase=json['corrente_fase']
            if 'tensao_fase' in json: self.tensao_fase=json['tensao_fase']
            if 'queda_tensao' in json: self.queda_tensao=json['queda_tensao']

    def to_dict(self):
        self.dict_cabo['name']=self.name
        self.dict_cabo['nos_entrada']=self.nos_entrada
        self.dict_cabo['nos_saida']=self.nos_saida
        self.dict_cabo['blindagem']=self.blindagem
        self.dict_cabo['tensao_isolamento']=self.tensao_isolamento
        self.dict_cabo['bitola_fase']=self.bitola_fase
        self.dict_cabo['bitola_neutro']=self.bitola_neutro
        self.dict_cabo['bitola_terra']=self.bitola_terra
        self.dict_cabo['pernas_fase']=self.pernas_fase
        self.dict_cabo['pernas_terra']=self.pernas_terra
        self.dict_cabo['material']=self.material
        self.dict_cabo['comprimento']=self.comprimento
        self.dict_cabo['I_max']=self.I_max
        self.dict_cabo['fator_agrup']=self.fator_agrup
        self.dict_cabo['grupo']=self.grupo
        self.dict_cabo['resist_km']=self.resist_km
        self.dict_cabo['reat_km']=self.reat_km
        self.dict_cabo['Z']=self.Z
        self.dict_cabo['tipo']=self.tipo
        self.dict_cabo['custo_alim']=self.custo_alim
        self.dict_cabo['corrente_fase']=self.corrente_fase
        self.dict_cabo['fator_temp']=self.fator_temp
        self.dict_cabo['queda_tensao']=self.queda_tensao
        self.dict_cabo['tensao_fase']=self.tensao_fase

        return self.dict_cabo

    def update_cabo(self):
        if self.tensao_fase is None or self.tensao_fase==0:
            tensao_fase=input("Tensão de fase (V): ")
            if tensao_fase!='':self.tensao_fase=float(tensao_fase)
        if self.comprimento is None:        
            comprimento=input("Comprimento (m): ")
            if comprimento!='':self.comprimento=float(comprimento)
        if self.queda_tensao is None:
            queda_max_pc=input("Qual a queda de tensão máxima permitida? (%): ")
            if queda_max_pc!='': 
                queda_max_pc=float(queda_max_pc)
                self.queda_tensao=queda_max_pc/100 #converter de percentual
        if self.fator_agrup is None:
            circuitos=input("Numero de circuitos agrupados: ")
            if circuitos!='':self.fator_agrup=fator_agrupamento(int(circuitos))
        if self.fator_temp is None:
            temp=input("Temperatura média (ºC) [10-15-20-25-30-35-40-45-50-55-60-65-70-75-80] (ENTER para padrão: 30º): ")
            if temp!='':self.fator_temp=fator_temp(int(temp))
            elif temp=='':self.fator_temp=fator_temp(30)


        bitola=123456789
        pernas=1
        while bitola>50:
            bitola=dimensionar_cabos(corrente_fase=self.corrente_fase, queda_max_pc=self.queda_tensao, comprimento=self.comprimento, tensao_fase=self.tensao_fase, 
            pernas=pernas, fator_temperatura=self.fator_temp, fator_agrupamento=self.fator_agrup)
            if bitola is not None:
                bitola_terra=dimens_terra(bitola_fase=bitola, pernas_fase=pernas)
                custo_total=(4*get_price(bitola)*pernas+1*get_price(bitola_terra[0])*bitola_terra[1])*self.comprimento
                alert(f'Custo total: para 4x ({pernas} x {bitola} mm²) + {bitola_terra[1]} x {bitola_terra[0]} mm² R$ {custo_total}\n')
                if custo_total<self.custo_alim or self.custo_alim==0:
                    self.custo_alim=custo_total
                    self.bitola_fase=bitola
                    self.pernas_fase=pernas
                    self.bitola_neutro=bitola
                    self.bitola_terra=bitola_terra[0]
                    self.pernas_terra=bitola_terra[1]
            else:
                bitola=123456789
            pernas+=1




    def __str__(self):
        self.to_dict()
        self.report()
        return str(self.to_dict())
    
    def report(self):
        # DADOS DO CABO DE BT
        print('\n')
        alert('DADOS DO CABO BT')
        for nome, dados in self.dict_cabo.items():
            mostrar(nome, dados)


    # def dimens_terra(self, bitola_fase=None):
    #     '''Calcula a bitola do terra como pelo menos a metade da bitola de fase'''
    #     if bitola_fase is None:
    #         bitola_fase=self.bitola_fase
    #     if bitola_fase<=10:
    #         self.bitola_terra=self.bitola_fase
    #     else:
    #         if self.pernas_fase==1:
    #             for bitola in dict_cabos.keys():
    #                 if bitola>bitola_fase/2:
    #                     self.bitola_terra=bitola
    #         elif self.pernas_fase//2==0:
    #             self.bitola_terra=bitola_fase/self.pernas_fase
    #             self.pernas_terra=self.pernas_fase/2
    #         elif self.pernas_fase//2==1:
    #             self.bitola_terra=self.dimensionar_cabos(corrente_fase=self.dimensionar_cabos(corrente_fase=self.corrente_fase/self.pernas_fase))
    #             # ver a corrente da bitola fase
    #             # escolher bitola para essa corrente
    #             #se for igual, ok
    #             #se for maior, reduzir em 2

    def calcula_impedancia(self, angulo):
        #Z=R.CosO + XL.senO
        self.Z=self.resist_km*cosh(angulo)+self.reat_km*sinh(angulo)

def lim_corrente(bitola,metodo):
    return dict_cabos[bitola][metodo]

def fator_agrupamento(nro_circuitos):
    fator={1:1,2:0.8,3:0.7,4:0.65,5:0.6,6:0.57,7:0.54,8:0.52,9:0.5,10:0.5,11:0.5,12:0.45,13:0.45,14:0.45,15:0.45,16:0.41,17:0.41,18:0.41,19:0.41,20:0.38}
    return fator[nro_circuitos]

def fator_temp(temperatura):
    fator={10:1.15,15:1.12,20:1.08,25:1.04,30:1,35:0.96,40:0.91,45:0.87,50:0.82,55:0.76,60:0.71,65:0.65,70:0.58,75:0.5,80:0.41}
    return fator[temperatura]

def dimensionar_cabos(queda_max_pc=5, bitola=None, corrente_fase=None, fator_agrupamento=1, fator_temperatura=1, metodo_instalacao=None, potencia_fase=None, pernas=1, tensao_fase=None, comprimento=1):
    '''Escolhe cabos baseado nas informacoes que tem disponiveis
    Por fase. queda_max_pc em %'''
    calcular_tensao=True
    if tensao_fase is None:
        debug("Cálculo baseado apenas na corrente, e não na queda de tensão.")
        calcular_tensao=False
        if queda_max_pc=='' or queda_max_pc is None:
            if queda_max_pc!='': 
                queda_max_pc=float(queda_max_pc)
                queda_max_pc=queda_max_pc/100 #converter de percentual
    
    # Tabela 2 - Distâncias máximas possíveis, potência conhecida
    elif tensao_fase is not None:
        if potencia_fase is not None and corrente_fase is None:
            corrente_fase=potencia_fase/tensao_fase
        else:
            potencia_fase1=input('Qual a potencia trifasica que passa por este cabo (kVA)?')
            potencia_fase=float(potencia_fase1)/3*1000
            corrente_fase=potencia_fase/tensao_fase
        
    corrente_corrigida=corrente_fase/fator_agrupamento/fator_temperatura
    corrente_perna=corrente_corrigida/pernas
    alert(f'Corrente demanda: {corrente_fase} A\t Corrente corrigida: {corrente_corrigida} A')

    # Tabela 1 - Distâncias máximas possíveis, corrente conhecida
    metodo='B1-3'
    if corrente_perna is not None:
        for bitola, impedancia in dict_imp.items(): #analisa, para cada bitola existente, se o cabo aguenta por queda de tensao e por corrente.
            dist_cont=1
            # if impedancia/1000*1*corrente_perna<queda_max_pc*tensao_fase: #impedancia é por km, por isso o /1000
            if calcular_tensao:
                while impedancia/1000*dist_cont*corrente_perna<queda_max_pc*tensao_fase: #impedancia é por km, por isso o /1000
                    dist_cont+=1
            if dist_cont>comprimento or calcular_tensao is False:
                limite_corrente=lim_corrente(bitola,metodo)
                if calcular_tensao:
                    print(f'O cabo {pernas} x {bitola} mm² atende na distância até {dist_cont} m')
                if limite_corrente>corrente_perna:
                    alert(f'O cabo {pernas} x {bitola} mm² atende até a corrente de {limite_corrente*pernas} A.\n')
                    # self.bitola_fase=bitola

                    return bitola
    
    #ADICIONAR OS FATORES DE CORRECAO
    #MOSTRAR O RESULTADO FINAL: PARA TAL CABO, A QUEDA EM TAL DEMANDA SERÁ DE TANTOS VOLTS.


def get_price(bitola):
    if bitola is not None:
        try:
            id_prod=dict_ID_Prod[bitola]
            if id_prod !=0:
                response = requests.get(f"https://api2.painelconstru.com.br/products/list/?id={id_prod}&items=yes")
                print(response.content)
                price=response.json() ['products'][0]['average_unit_price']
                return price
            elif id_prod ==0:
                return 0
        except:
            error(f"Erro ao coletar preço id_prod={id_prod}")
            return 0
    else: return 0

def dimens_terra( bitola_fase=None, pernas_fase=1):
    '''Calcula a bitola do terra como pelo menos a metade da bitola de fase'''
    if bitola_fase is None:
        bitola_fase=bitola_fase
    elif bitola_fase<=10:
        bitola_terra=bitola_fase
    else:
        if pernas_fase==1: #se só tem 1 perna por fase, retorna a maior que metade da bitola de fase
            for bitola in dict_cabos.keys():
                if bitola>bitola_fase/2:
                    bitola_terra=bitola
                    return bitola_terra, pernas_fase
        elif pernas_fase%2==0: #se tem nro par de pernas na fase, retorna a mesma bitola, metade das pernas
            bitola_terra=bitola_fase
            pernas_terra=pernas_fase/2
            return bitola_terra, pernas_terra
        elif pernas_fase%2==1:
            for bitola in dict_cabos.keys():
                if bitola*(pernas_fase//2+1)>=bitola_fase*pernas_fase/2:
                    bitola_terra=bitola
                    return bitola_terra, pernas_fase//2+1
            # bitola_terra=dimensionar_cabos(corrente_fase=dict_cabos[bitola_fase]['B1-3']*3)
            # return bitola_terra, pernas_terra
            
            #se for igual, ok
            #se for maior, reduzir em 2

def dimens_pela_corrente():
    pass

def ohm_km(bitola):
    '''retorna a impedância do cabo dada a bitola'''
    # fonte: http://www.construfios.com.br/area-tecnica/tabelastecnicas.pdf
    dict_imp={1:12.1, 2.5:7.41, 4: 4.61, 6: 3.08, 10:1.83, 16: 1.15, 25:0.73, 35: 0.52, 50: 0.39, 70: 0.27, 95:0.19, 120: 0.15, 150: 0.12, 185: 0.099, 240: 0.075, 300: 0.06, 400:0.047, 500:0.037, 630:0.028, 800: 0.022, 1000:0.018}
    return dict_imp[bitola] #em ohm/km

dict_imp={1:12.1, 2.5:7.41, 4: 4.61, 6: 3.08, 10:1.83, 16: 1.15, 25:0.73, 35: 0.52, 50: 0.39, 70: 0.27, 95:0.19, 120: 0.15, 150: 0.12, 185: 0.099, 240: 0.075, 300: 0.06, 400:0.047, 500:0.037, 630:0.028, 800: 0.022, 1000:0.018}

dict_cabos={
    0.5:{'B1-3':8},
    0.75:{'B1-3':10},
    1:{'B1-3':12},
    1.5:{'B1-3':15.5},
    2.5:{'B1-3':21},
    4:{'B1-3':28},
    6:{'B1-3':36},
    10:{'B1-3':50},
    16:{'B1-3':68},
    25:{'B1-3':89},
    35:{'B1-3':110},
    50:{'B1-3':134},
    70:{'B1-3':171},
    95:{'B1-3':207},
    120:{'B1-3':239},
    150:{'B1-3':275},
    185:{'B1-3':314},
    240:{'B1-3':370},
    300:{'B1-3':426},
    400:{'B1-3':510},
    500:{'B1-3':587},
    630:{'B1-3':678},
    800:{'B1-3':788},
    1000:{'B1-3':906}
        }

class Cabo_AT():
    """Classe de componente tipo cabo de Alta Tensão"""
    def __init__(self):
        self.name='Cabo AT'
        self.nos_entrada=[]
        self.nos_saida=[]
        self.blindagem='' #15kV, 36kV
        self.tensao_isolamento=0
        self.bitola=0
        self.material='' # EPR/XLPE
        self.comprimento=0
        self.I_max=0
        self.instalacao='' # aéreo/subterraneo
        self.grupo='cabos/barras'



# EQUIPAMENTOS DE CONSUMO        

class QGBT():
    """Classe de equipamento tipo Quadro Geral de Baixa Tensão"""
    def __init__(self, json=None):
        self.name='QGBT'
        self.nos_entrada=[]
        self.nos_saida=[]
        self.pot_instalada=0
        self.pot_demandada=0
        self.demanda=0
        self.I_barras=0
        self.prot_geral=0
        self.grupo='consumo'
        self.dict_QGBT={}
        self.tensao=0 #tensão de linha
        self.tensao_fase=0
        self.fases=3
        self.corrente=3
        self.tipo='QGBT'
        self.cabos_saida=[]
        self.alimentador=None
        self.corrente=0
        self.corrente_fase=0

        if json is None:
            self.update_qgbt()
        
        else: #json possui informação
            if 'name' in json: self.name=json['name']
            if 'nos_entrada' in json: self.nos_entrada=json['nos_entrada']
            if 'nos_saida' in json: self.nos_saida=json['nos_saida']
            if 'pot_instalada' in json: self.pot_instalada=json['pot_instalada']
            if 'pot_demandada' in json: self.pot_demandada=json['pot_demandada']
            if 'demanda' in json: self.demanda=json['demanda']
            if 'I_barras' in json: self.I_barras=json['I_barras']
            if 'prot_geral' in json: self.prot_geral=json['prot_geral']
            if 'grupo' in json: self.grupo=json['grupo']
            if 'tensao' in json: self.tensao=json['tensao']
            if 'tensao_fase' in json: self.tensao_fase=json['tensao_fase']
            if 'fases' in json: self.fases=json['fases']
            if 'corrente' in json: self.corrente=json['corrente']
            if 'corrente_fase' in json: self.corrente_fase=json['corrente_fase']
            if 'tipo' in json: self.tipo=json['tipo']
            if 'cabos_saida' in json: self.cabos_saida=json['cabos_saida']
            if 'alimentador' in json: self.alimentador=Cabo_BT(json=json['alimentador'])


    def to_dict(self):
        self.dict_QGBT['name']=self.name
        self.dict_QGBT['nos_entrada']=self.nos_entrada
        self.dict_QGBT['nos_saida']=self.nos_saida
        self.dict_QGBT['pot_instalada']=self.pot_instalada
        self.dict_QGBT['pot_demandada']=self.pot_demandada
        self.dict_QGBT['demanda']=self.demanda
        self.dict_QGBT['I_barras']=self.I_barras
        self.dict_QGBT['prot_geral']=self.prot_geral
        self.dict_QGBT['grupo']=self.grupo
        self.dict_QGBT['tensao']=self.tensao
        self.dict_QGBT['tensao_fase']=self.tensao_fase
        self.dict_QGBT['fases']=self.fases
        self.dict_QGBT['corrente']=self.corrente
        self.dict_QGBT['corrente_fase']=self.corrente_fase
        self.dict_QGBT['tipo']=self.tipo
        # self.dict_QGBT['cabos_saida']=self.cabos_saida.to_dict()
        self.dict_QGBT['alimentador']=self.alimentador.to_dict()

        return self.dict_QGBT


    def update_qgbt(self, choice='all'):
                
        if choice=='1' or choice=='all':
            self.name=input("Nome: ")
            if choice=='1': return None
        if choice=='2' or choice=='all':
            tensao=input("Tensão de linha (V): ")
            if tensao!='':self.tensao=float(tensao)
        if choice=='3' or choice=='all':        
            pot_instalada=input("Potência total instalada (kW): ")
            if pot_instalada!='':self.pot_instalada=float(pot_instalada)*1000
        if choice=='4' or choice=='all':            
            pot_demandada=input("Potência total demandada (kW) [ENTER para calcular pela demanda %]: ")
            if self.pot_demandada=='':
                demanda=input("Demanda média %: ")
                if demanda!='':self.demanda=float(demanda)/100
                self.pot_demandada=self.pot_instalada*self.demanda
            else:
                if pot_demandada!='':
                    self.pot_demandada=float(pot_demandada)*1000
                    self.demanda=self.pot_demandada/self.pot_instalada
        if choice=='5' or choice=='all':
            fases=input("Nro de fases: ")
            if fases!='':self.fases=float(fases)

        
        
        if self.fases==3: 
            self.tensao_fase=ceil(self.tensao/sqrt(3))
            self.corrente=self.pot_demandada/self.tensao_fase/sqrt(3)
        elif self.fases==2 or self.fases==1: 
            self.tensao_fase=self.tensao
            self.corrente=pot_demandada/self.tensao_fase
            alert(f'Corrente: {self.corrente}')
        else: raise NameError("Sistema não pode ter fases diferentes de 1, 2 ou 3.")
        
        self.corrente_fase=self.pot_demandada/self.fases/self.tensao_fase
        alert(f'Corrente de fase: {self.corrente_fase} A')
        if choice!='6':
            if self.alimentador is not None:
                comprimento=self.alimentador.comprimento
                queda_tensao=self.alimentador.queda_tensao
            else:
                comprimento=None
                queda_tensao=None
        else:
            comprimento=None
            queda_tensao=None
        cabo1=Cabo_BT(name=f'Alimentador {self.name}',tensao_fase=self.tensao_fase, corrente_fase=self.corrente_fase, comprimento=comprimento, queda_tensao=queda_tensao) #enviar pra calculo já com a corrente corrigida (fatores de temperatura e agrupamento)
        print(f'Calculo pela potencia demandada do quadro: {cabo1.__str__()}')
        self.alimentador=cabo1
    
    def __str__(self):
        self.to_dict()
        self.report()

        self.alimentador.to_dict()
        self.alimentador.report()
        print('\n')
        return str(self.to_dict())

    def report(self):
        # DADOS DO QGBT
        print('\n')
        alert('DADOS DO QGBT')
        for nome, dados in self.dict_QGBT.items():
            mostrar(nome, dados)

    def dimensiona_cabos_saida(self):
        cabo1=Cabo_BT()
        cabo1.dimensionar_cabos(tensao_fase=self.tensao_fase)
        self.cabos_saida.append(cabo1)






# ACESSÓRIOS, CONECTORES

class Mufla():
    """Classe de equipamento tipo mufla"""
    def __init__(self):
        self.name='Mufla'
        self.nos_entrada=[]
        self.nos_saida=[]
        self.grupo='conectores'
        

def curva_IEC(tipo, dial_tempo, corr_partida, I):
    '''Curva IEC. I=corrente de partida'''

    Is=corr_partida
    dict_curva={}
    dict_curva['ti']=(0.14,0.02,2.97) #Tempo Inverso
    dict_curva['tmi']=(13.5,1,1.5) #Tempo Muito Inverso
    dict_curva['tli']=(120,1,13.33) #Tempo Longo Inverso
    dict_curva['tei']=(80,2,0.808) #Tempo Extremamente Inverso
    dict_curva['tui']=(315.2,2.5,1) #Tempo Ultra-Inverso

    k, alfa, beta=dict_curva[tipo]

    # td=k/((I/Is)**alfa-1)*T/beta
    if I/Is>1:
        td=k/((I/Is)**alfa-1)*dial_tempo
    else: return None

    # T/beta == dial_tempo
    #Is corrente de partida
    #T= Tempo de atuacao

    return td

if __name__ == '__main__': #Start program
    """Autoteste"""

    # #PARA TESTAR CURVAS:
    # result=round(curva_IEC('ti', 0.1, 25, 100),4)
    # print(f'{result} s')

    #PARA DIMENSIONAR CABOS:
    cabo1=Cabo_BT()
    cabo1.comprimento=20
    cabo1.dimensionar_cabos(potencia_fase=750000/3,queda_max_pc=1,tensao_fase=380)
    alert('Connecting to API to get updated prices...')
    preco=get_price(cabo1.bitola_fase)
    print(f'Preço para 1 m: R$ {preco}')
    print(f'Preço para {cabo1.comprimento} m: R$ {preco*cabo1.comprimento}')
