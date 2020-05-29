# ***************************************************************************    
"""
-_Heat_TO
 |  |-- Prop: Name, Lengte, Breedte, Hoogte, Dikte, _R_Waarde, Lambda, Dummy,
 |  |         Temperature_Inside, Temperature_Outside
 |  |-- def Heat_Transfer
 |  |-- def Heat_Transfers
 |  |-- def __repr__
 |  |-- def Oppervlakte
 | 
 |Heat_Transfer_Object
   |
   |-Sandwich
     |  |-- Prop:
     |  |-- def Add
     |  |-- def _get_R_Waarde
     |  |-- def _get_U_waarde
     !  !-- def _get_C_Waarde
     |  |-- def __repr__
     |  |-- def Kosten_m2
     |
     |-Heat_Parallel_Object
         |-- Prop:
         |-- def Add
         |-- def Oppervlakte
         |-- def get_R_waarde
         |-- def __repr__
            
-- def Heat_Transfer_tabel            

"""
# ***************************************************************************    

GasPrice   = 0.80
GraadDagen = 2774
PrintLevel = 5          # 1 = heel summier
                        # ...
                        # 5 = heel uitgebreid


# ***************************************************************************    
# ***************************************************************************    
class _Heat_TO ( object ) :
  # ***********************************************
  def __init__ ( self, Name ) :
    self.Name      = Name
    #self.Inpandig  = False
    self.Lengte    = -1
    self.Breedte   = -1
    self.Hoogte    = -1
    self.Dikte     = -1
    self._R_Waarde = -1
    self._Cap_kJ   = 0
    self.Lambda    = -1
    self.Dummy     = False
    self.Temperature_Inside  = -1000
    self.Temperature_Outside = -1000
    

  # ***********************************************
  def Heat_Transfer ( self, Temperature_Outside = None, Temperature_Inside = None ) :
    if self.Oppervlakte() != -1 :
      if Temperature_Outside is None :
        Temperature_Outside = self.Temperature_Outside
      if Temperature_Inside is None :
        Temperature_Inside = self.Temperature_Inside
      Heat_Transfer = self.Oppervlakte() * ( Temperature_Inside - Temperature_Outside ) / self.R_Waarde
      return Heat_Transfer
        
  # ***********************************************
  def Heat_Transfers ( self, Temperature_Outside = [], Temperature_Inside = None ) :
    #print ( type ( self))
    self.Losts = []
    for T in Temperature_Outside :
      if not self.Dummy :
        self.Losts.append ( int ( self.Heat_Transfer ( T, Temperature_Inside )))
      else :
        self.Losts.append ( 0 )
    return self.Losts

  # ***********************************************
  def __repr__ ( self ) :
    Line = ""
    #Line += "Name        = %s\n" % self.Name
    Line += "==================  %s  ==================\n" % self.Name
    if ( PrintLevel > 3 ) and ( self.Lengte != -1 ) :
      Line += "Lengte      = %s [m]\n" % self.Lengte
    if ( PrintLevel > 3 ) and ( self.Breedte != -1 ) :
      Line += "Breedte     = %s [m]\n" % self.Lengte
    if ( PrintLevel > 3 ) and ( self.Hoogte!= -1 ) :
      Line += "Hoogte      = %s [m]\n" % self.Hoogte
    if ( PrintLevel > 3 ) and ( self.Dikte != -1 ) :
      Line += "Dikte       = %s [m]\n" % self.Dikte
    if ( PrintLevel > 3 ) and ( self.Oppervlakte() != -1 ) :
      Line += "Oppervlakte = %.1f [m2]\n" % self.Oppervlakte ()
    
    if ( PrintLevel > 3 ) and ( self.Lambda != -1 ) :
      Line += "Lambda      = %.2f [W/m.K]\n" % self.Lambda
    if ( PrintLevel > 3 ) and ( self.R_Waarde != -1 ):
      Line += "R-Waarde    = %.2f [m2.K/W]\n" % self.R_Waarde
    if ( PrintLevel > 3 ) and ( self.U_Waarde != -1 ) :
      Line += "U-Waarde    = %.2f [W/m2.K]\n" % self.U_Waarde
    if ( PrintLevel > 3 ) and ( self.Dikte != -1 ) :
      Line += "Capaciteit  = %.2f [Wh/m2.K]\n" % self.C_Waarde

    
    Heat_Transfer_m2 = -1 ;
    if ( PrintLevel > 3 ) and ( self.Temperature_Inside != -1000 ) and ( self.Temperature_Outside != -1000 ) :
      Line += "T-Inside    = %.1f [Celsius]\n" % self.Temperature_Inside
      Line += "T-Outside   = %.1f [Celsius]\n" % self.Temperature_Outside

      Heat_Transfer_m2 = ( self.Temperature_Inside - self.Temperature_Outside ) / self.R_Waarde
      if Heat_Transfer_m2 != -1 :
        if ( self.Lengte != -1 ) and ( self.Breedte != -1 ) :  
          Opp = self.Lengte * self.Breedte
        elif ( self.Lengte != -1 ) and ( self.Hoogte != -1 ) :  
          Opp = self.Lengte * self.Hoogte
        else :
          Opp = self.Breedte * self.Hoogte
          
        Line += "Heat Loss       = %d [W]\n"      % ( Heat_Transfer_m2 * Opp )
        Line += "Heat Loss/m2    = %.2f [W/m2]\n" % ( Heat_Transfer_m2       )

        Line += "Heat Capacity   = %.2f [Wh/K]\n" % ( self.C_Waarde * Opp )
        
        # 100 dagen, 24 uur per dag, 24 cent/3 per kWh (ongeveer de huidige gasprijs)
        Line += "Energy Cost 1m2 = %.2f [Euro]\n" % ( 100 * 24 * Heat_Transfer_m2 * GasPrice / 10000 )
        Line += "Gasprijs        = %.2f [Euro]\n" % GasPrice
        
    return Line    

  # ***********************************************
  def Oppervlakte ( self ) :
    if self.Lengte == -1 :
      if self.Breedte != -1 and self.Hoogte != -1 :
        return self.Breedte * self.Hoogte
      else :
        return -1
    elif self.Breedte == -1 :
      if self.Lengte != -1 and self.Hoogte != -1 :
        return self.Lengte * self.Hoogte
      else :
        return -1
    else :
      if self.Breedte != -1 and self.Lengte != -1 :
        return self.Breedte * self.Lengte
      else :
        return -1

  # ***********************************************
  def Volume ( self ) :
    if self.Oppervlakte() != -1  and self.Dikte != -1 :
      return self.Oppervlakte() * self.Dikte
    else :
      return -1

# ***************************************************************************    
# ***************************************************************************    
class Heat_Transfer_Object ( _Heat_TO ) :

  def _set_U_Waarde ( self, Value ) :
    self._R_Waarde = 1.0 / Value
  def _get_U_Waarde ( self ) :
    return 1.0 / self._get_R_Waarde ()

  def _set_R_Waarde ( self, Value ) :
    self._R_Waarde = Value
  def _get_R_Waarde ( self ) :
    if self._R_Waarde != -1 :
      return self._R_Waarde
    elif self.Lambda != -1 and self.Dikte != -1 :
      return self.Dikte / self.Lambda
    else :
      return 0

  def _set_Cap_kJ ( self, Value ) :
    self._Cap_kJ = Value
  def _get_Cap_kJ ( self ) :
    return self._Cap_kJ

  def _set_C_Waarde ( self, Value ) :
    self._Cap_kJ = 3.6 * Value / self.Dikte
  def _get_C_Waarde ( self ) :
    C_Waarde = self.Dikte * self._Cap_kJ / 3.6
    return C_Waarde

  # ***********************************************
  def Kosten_m2 ( self ) :
    #Heat_Transfer_m2 = ( self.Temperature_Inside - self.Temperature_Outside ) / self.R_Waarde
    #Kosten = 24 * 100 * Heat_Transfer_m2 * GasPrice / 10000
    Kosten = 24 * GraadDagen * GasPrice / ( 10000 * self.R_Waarde )
    return Kosten
  

  R_Waarde = property ( _get_R_Waarde, _set_R_Waarde )
  U_Waarde = property ( _get_U_Waarde, _set_U_Waarde )
  C_Waarde = property ( _get_C_Waarde, _set_C_Waarde )
  Cap_kJ   = property ( _get_Cap_kJ  , _set_Cap_kJ   )


# ***************************************************************************    
# ***************************************************************************    
class Sandwich ( _Heat_TO ) :
  # ***********************************************
  def __init__ ( self, Name ) :
    _Heat_TO.__init__ ( self, Name )
    self.Layers  = []
    
  # ***********************************************
  def Add ( self, Layers ) :
    if isinstance ( Layers, Heat_Transfer_Object ) :
      self.Layers.append ( Layers )
    else :
      for Layer in self.Layers :
        self.Layers.append ( Layer )

  # ***********************************************
  def _get_R_Waarde ( self ) :
    R_Waarde = 0
    for Layer in self.Layers :
      if Layer.R_Waarde != -1 :
        R_Waarde += Layer.R_Waarde
    return R_Waarde

  # ***********************************************
  def _get_Rsie_Waarde ( self ) :
    R_Waarde = 0
    for Layer in self.Layers :
      if ( Layer.R_Waarde != -1 ) and ( Layer.Name[:3] in ["Rsi","Rse"] ) :
        R_Waarde += Layer.R_Waarde
    return R_Waarde

  # ***********************************************
  def _get_U_Waarde ( self ) :
    return 1.0 / self.R_Waarde 

  # ***********************************************
  def _get_C_Waarde ( self ) :
    C_Waarde = 0
    for Layer in self.Layers :
      if Layer.C_Waarde != -1 :
        C_Waarde += Layer.C_Waarde
    return C_Waarde

  # ***********************************************
  def __repr__ ( self ) :
    Line = _Heat_TO.__repr__ ( self )
    
    R_Waarde = "R-Waarden = %.2f [ " % self.R_Waarde
    U_Waarde = "U-Waarden = %.2f [ " % self.U_Waarde
    C_Waarde = "C-Waarden = %.2f [ " % self.C_Waarde
    Dikten   = "Dikten    = [ " 
    Line += "Layers    = [ "
    for Layer in self.Layers :
      Line     += Layer.Name + ", "
      if Layer.Dikte > 0 :
        Dikten   += "%.1f, " % (100*Layer.Dikte)
      else :
        Dikten   += "-, "
      R_Waarde += "%.2f, " % Layer.R_Waarde

      if Layer.R_Waarde > 0 :
        U_Waarde += "%.2f, " % Layer.U_Waarde
      else:
        U_Waarde += "-, "

      if Layer.C_Waarde > 0 :
        C_Waarde += "%.2f, " % Layer.C_Waarde
      else:
        C_Waarde += "-, "

    Line += " ]\n"
    if ( PrintLevel > 3 ) : Line += Dikten   + " ] [cm]\n"
    Line += R_Waarde + " ] [m2.K/W]\n"
    if ( PrintLevel > 3 ) : Line += U_Waarde + " ] [W/m2.K]\n"
    if ( PrintLevel > 3 ) : Line += C_Waarde + " ] [Wh/m2.K]\n"

    return Line

  # ***********************************************
  def Kosten_m2 ( self ) :
    R_Waarde = 0
    for Layer in self.Layers :
      R_Waarde += Layer.R_Waarde
    ##Heat_Transfer_m2 = ( self.Temperature_Inside - self.Temperature_Outside ) / R_Waarde
    Kosten = 24 * GraadDagen * GasPrice / ( R_Waarde * 10000 )
    return Kosten
  
  # ***********************************************
  R_Waarde = property ( _get_R_Waarde )
  U_Waarde = property ( _get_U_Waarde )
  C_Waarde = property ( _get_C_Waarde )

  Rsie_Waarde = property ( _get_Rsie_Waarde )

  
# ***************************************************************************    
# ***************************************************************************    
class Heat_Parallel_Object ( Sandwich ) :
  # ***********************************************
  def __init__ ( self, Name ) :
    _Heat_TO.__init__ ( self, Name )
    self.Layers  = []
    
  # ***********************************************
  def Add ( self, Layers ) :
    if isinstance ( Layers, Sandwich ) :
      self.Layers.append ( Layers )
    else :
      for Layer in self.Layers :
        self.Layers.append ( Layer )

  # ***********************************************
  def Oppervlakte ( self ) :
    Opp = 0
    for Layer in self.Layers :
      Opp  += Layer.Oppervlakte ()   
    return Opp

  # ***********************************************
  def _get_R_Waarde ( self ) :
    R_Waarde = 0
    Opp = self.Oppervlakte ()
    for Layer in self.Layers :
      if Layer.R_Waarde != -1 :
        R_Waarde += Layer.R_Waarde * ( Layer.Oppervlakte() / Opp )
    return R_Waarde

  # ***********************************************
  #def Kosten_m2 ( self ) :
  #  Heat_Transfer_m2 = ( self.Temperature_Inside - self.Temperature_Outside ) / self.R_Waarde
  #  Kosten = 24 * 100 * Heat_Transfer_m2 * GasPrice / 10000
  #  return Kosten

  # ***********************************************
  def __repr__ ( self ) :
    Opp      = self.Oppervlakte ()

    Line = _Heat_TO.__repr__ ( self )

    Line += "Objects     = [ "  
    for Layer in self.Layers :
      Line += Layer.Name + ", "
    Line += "]"

    Line += "\nOppervlakte = %.1f [" % Opp
    for Layer in self.Layers :
      Line     += "%.1f" % Layer.Oppervlakte() + ", "
    Line += "] [m2]"  

    Line += "\nR-Waarde    = %.2f [ " % self.R_Waarde  
    for Layer in self.Layers :
      Line     += "%.1f" % Layer.R_Waarde + ", "
    Line += "] [m2.K/W]\n" 

    return Line

  # ***********************************************
  R_Waarde = property ( _get_R_Waarde )
  #U_Waarde = property ( _get_U_Waarde )

# ***************************************************************************    
# ***************************************************************************    
def Heat_Transfer_Table ( Elements, Ts ) :
  import pandas as pd

  Totaal = [ "R-waarde", "U-waarde", "Oppervlak", "T-Binnen", "T-Buiten", "Kosten/m2", "Kosten", "m3/Jaar" ]
  Header_Ts = []
  for item in Ts :
    Header_Ts.append ( "%sC[W]" % item )
  df = pd.DataFrame ( index = Totaal + list ( Header_Ts ) )
  Element_Names = []
  Element_Kosten_Sum = 0
  Element_Jaar_m3_Sum = 0
  
  for Element in Elements :
    # to get nice roundings in table multiply/divide by 100
    Element_Kosten = int ( Element.Kosten_m2 () * Element.Oppervlakte () )
    Element_Kosten_Sum += Element_Kosten
    Element_Jaar_m3 = int ( 24 * GraadDagen * Element.Oppervlakte () / ( Element.R_Waarde * 1000 * 10 ) )
    Element_Jaar_m3_Sum += Element_Jaar_m3

    Row = [ int ( 100* Element.R_Waarde ) /100.0, 
            int ( 100* Element.U_Waarde ) /100.0, 
            int ( 100* Element.Oppervlakte() ) / 100.0, 
            Element.Temperature_Inside,
            Element.Temperature_Outside,
            int ( 100* Element.Kosten_m2 () ) / 100.0,
            Element_Kosten,
            Element_Jaar_m3 ]
            #"<b>%i</b>" % Element_Jaar_m3 ]
    #print (Row)
    Row += Element.Heat_Transfers ( Ts )
    df [ Element.Name ] = Row
    Element_Names.append ( Element.Name )

  # Replace last couple of elements by the sum  
  Totaal [-2] = "%i" % Element_Kosten_Sum
  Totaal [-1] = "%i" % Element_Jaar_m3_Sum
    
  for i in Ts :
    Sum  = 0
    for Element in Elements :
      Sum += df [ Element.Name ] [i]
    Totaal.append ( Sum )
    
  df[ "Totaal" ] = Totaal
  df = df.transpose ()
  return df

# ***************************************************************************    
# ***************************************************************************    
def Heat_Params_Table ( Elements ) :
  import pandas as pd

  Totaal = [ "@12.5 [Wh/dag]", "@20 [Wh/dag]",
             "@12.5 [W]", "@20 [W]",
             "Opp [m2]",
             "Robj [m2.K/W]", "Rsie [m2.K/W]", 
             "U [W/m2.K]", "C [Wh/m2.K]",  
            
             
             ]
  df = pd.DataFrame ( index = Totaal )
  
  Tot_Opp = 0
  Tot_U   = 0
  Tot_C   = 0
  
  Airco_factor = 1.0 / 6000   # Airco 600% rendement en naar kWh
  
  for Element in Elements :

    Opp = Element.Oppervlakte ()

    R    = Element.R_Waarde 
    Rsie = Element.Rsie_Waarde 
    if Rsie != 0 :
      R = R- Rsie

    Row = [ 
            int ( 100* 24 * 12.5 * Opp * Airco_factor / ( R + Rsie ) ) /100.0,
            int ( 100* 24 * 20   * Opp * Airco_factor / ( R + Rsie ) ) /100.0,

            int ( 12.5  * Opp / ( R + Rsie ) ),
            int ( 20    * Opp / ( R + Rsie ) ),

            int ( 100* Opp ) / 100.0, 
            
            int ( 100* R ) /100.0, 
            int ( 100* Rsie ) /100.0, 

            int ( 100* Element.U_Waarde ) /100.0, 
            int ( 100* Element.C_Waarde ) /100.0, 
            ]

    df [ Element.Name ] = Row

    
  df = df.transpose ()
  return df


  #%%!print ( df )
  #print ( Element_Names )
  return df

# ***************************************************************************    
# ***************************************************************************    
class Calc_Transfer_Object ( object ) :
  # ***********************************************
  def __init__ ( self, TBinnen=None, TBinnenMuur=None, TBuiten=None, TBuitenMuur=None,
                       Positie=None, Rsi=None, Rse=None, Rc=None, Rm=None, GrenstAan=None ) :
    self.TBinnen = TBinnen

  # ***********************************************
  def _set_TBinnen ( self, Value ) :
    self._TBinnen  = Value
    self.__TBinnen = self._TBinnen
    if self._TBinnen == None : 
      self._TBinnen = 20
  def _get_TBinnen ( self ) :
    return self._TBinnen

  # ***********************************************
  TBinnen = property ( _get_TBinnen, _set_TBinnen )
  
  # ***********************************************
  def __repr__ ( self ) :
    Line  = "\n==========   Finals   ===========\n"
    Line += "TBinnen = %.1f\n" %self.TBinnen
    
    Line+= "\n==========   Inputs   ===========\n"
    Line += "_TBinnen = %s\n" %self.__TBinnen
    
    Line+= "\n==========   Modified   ===========\n"
    if self._TBinnen != self.__TBinnen :
      Line += "_TBinnen = %.1f / %s\n" % ( self._TBinnen, self.__TBinnen )

    return Line

# ***********************************************************************
# ***********************************************************************
def Calc_Transfer ( TBinnen=None, TBinnenMuur=None, TBuiten=None, TBuitenMuur=None,
                    Positie=None, Rsi=None, Rse=None, Rc=None, Rm=None, GrenstAan=None ) :
  A = {}
  A [ "TBinnen"     ] = TBinnen      # Verplicht
  A [ "TBinnenMuur" ] = TBinnenMuur  # Verplicht
  A [ "TBuiten"     ] = TBuiten
  A [ "TBuitenMuur" ] = TBuitenMuur
  A [ "Positie"     ] = Positie      # Vloer, Plafond, anders Wand
  A [ "GrenstAan"   ] = GrenstAan    # Buiten, anders Onverwarmd
  A [ "Rsi"         ] = Rsi
  A [ "Rse"         ] = Rse
  A [ "Rc"          ] = Rc
  A [ "Rm"          ] = Rm
  A [ "delta_T"     ] = 0
  A [ "delta_Time"  ] = 0
  A [ "Opmerkingen" ] = ""

  if A["TBinnen"]==None or A["TBinnenMuur"]==None :
    print ( "ERROR: TBinnen en TBinnenMuur zijn verplicht" )
    return A

  if A["Positie"]==None :
    A["Positie"]="Wand"
    A["Opmerkingen"] += "\nPositie ==> Wand"

  if A["GrenstAan"]==None :
    A["GrenstAan"]="Onverwarmd"
    A["Opmerkingen"] += "\nGrenstAan ==> Onverwarmd"

  if A["Rsi"]==None :
    if A["Positie"]=="Vloer" :
      A["Rsi"]=0.17
        
    elif A["Positie"]=="Plafond" :
      A["Rsi"]=0.10
        
    else :  # Wand
      A["Rsi"]=0.13

        
  if A["Rse"]==None :
    if A["Positie"]=="Vloer" :
      if A["GrenstAan"]=="Buiten" :
        A["Rse"]=0.04 
      else : #"Onverwarmd"  
        A["Rse"]=0.17
        
    elif A["Positie"]=="Plafond" :
      if A["GrenstAan"]=="Buiten" :
        A["Rse"]=0.04 
      else : #"Onverwarmd"  
        A["Rse"]=0.10
        
    else :  # Wand
      if A["GrenstAan"]=="Buiten" :
        A["Rse"]=0.04 
      else : #"Onverwarmd"  
        A["Rse"]=0.13
        
  if A["Rc"]== None :
    if A["Rm"]== None :
      if A["TBuiten"]==None and A["TBuitenMuur"]==None :
        print ( "ERROR: Rc, Rm, TBuiten, TBuitenMuur hiervan moet minstens 1 bekend zijn" )
        return A
      elif A["TBuiten"]==None :
        A["TBuiten"] = A["TBuitenMuur"] - ( A["Rse"] / A["Rsi"] ) * ( A["TBinnen"]-A["TBinnenMuur"]) 
      elif A["TBuitenMuur"]==None :
        A["TBuitenMuur"] = A["TBuiten"] + ( A["Rse"] / A["Rsi"] ) * ( A["TBinnen"]-A["TBinnenMuur"]) 
      else :   # TBuiten en TBuitenMuur zijn bekend
        A["TBuiten*"    ]=A["TBuitenMuur"] - ( A["Rse"] / A["Rsi"] ) * ( A["TBinnen"]-A["TBinnenMuur"]) 
        A["TBuitenMuur*"]=A["TBuiten"] + ( A["Rse"] / A["Rsi"] ) * ( A["TBinnen"]-A["TBinnenMuur"]) 

    else :  # Rm opgegeven
      A["Rc"] = A["Rsi"] + A["Rm"] + A["Rse"]
      A["TBuitenMuur**"]=A["TBinnenMuur"] - ( A["Rm"] / A["Rsi"] ) * ( A["TBinnen"]-A["TBinnenMuur"]) 
      A["TBuiten**"    ]=A["TBuitenMuur**"] - ( A["Rse"] / A["Rsi"] ) * ( A["TBinnen"]-A["TBinnenMuur"]) 

  else :   # Rc opgegeven          
    A["Rm*"] = A["Rc"] - A["Rsi"] - A["Rse"]
    A["TBuitenMuur**"]=A["TBinnenMuur"] - ( A["Rm*"] / A["Rsi"] ) * ( A["TBinnen"]-A["TBinnenMuur"]) 
    A["TBuiten**"    ]=A["TBuitenMuur**"] - ( A["Rse"] / A["Rsi"] ) * ( A["TBinnen"]-A["TBinnenMuur"]) 
        
  
    
  # *********************************************************    
  # Nu moet ik een van de volgende 4 hebben
  # Rm, Rc, TBuiten, TBuitenMuur
  # *********************************************************    
  if A["TBuiten"]==None :
    if A["TBuitenMuur"]==None :
      #%if 
      A["TBuitenMuur"] = A["TBuiten"] + ( A["Rse"] / A["Rsi"] ) * ( A["TBinnen"]-A["TBinnenMuur"]) 
      
      A["Flux_Out"] = ( A["TBuitenMuur"] - A["TBuiten"] ) / A["Rse"]
  else :
    if A["TBuitenMuur"]==None :
      A["TBuitenMuur"] = A["TBuiten"] + ( A["Rse"] / A["Rsi"] ) * ( A["TBinnen"]-A["TBinnenMuur"]) 
    else :
      A["Flux_Out"] = ( A["TBuitenMuur"] - A["TBuiten"] ) / A["Rse"]

      

  return A

# ***********************************************************************
# Main program
# ***********************************************************************
if __name__ == '__main__':
  from pprint import pprint as print



  PrintLevel = 5

  Lengte  = 7
  Breedte = 7
  Hoogte  = 2.50

  Temperatuur_Binnen      = 20.0
  Temperatuur_Buiten      = 0.0
  Temperatuur_Kruipruimte = 8.0

  Piepschuim_Lambda       = 0.035
  Kurk_Lambda             = 0.039
  Beton_Licht_Lambda      = 1.3
  Beton_Zwaar_Lambda      = 1.7
  Hardboard_Lambda        = 0.15
  Hout_Lambda             = 0.14
  Hardhout_Lambda         = 0.17
  Lucht_Lambda            = 0.025
  
  # overgangsweerstand van de binnenmuur, zoals gedefinieerd in het bouwbesluit
  Rsi = Heat_Transfer_Object ( "Rsi" )
  Rsi.R_Waarde = 0.13
  
  # overgangsweerstand van de buitenmuur, zoals gedefinieerd in het bouwbesluit
  Rse = Heat_Transfer_Object ( "Rse" )
  Rse.R_Waarde = 0.04
  
  
  Spouw_Zwak_Geventileerd = Heat_Transfer_Object ( "Spouw Zwak Geventileerd" )
  Kalkzandsteen = Heat_Transfer_Object ( "Kalkzandsteen" )
  Kalkzandsteen.R_Waarde = 0.1
  Kalkzandsteen.Dikte    = 0.1
  Kalkzandsteen.Cap_kJ   = 1500
  print ( Kalkzandsteen )
  
  Baksteen = Heat_Transfer_Object ( "Baksteen" )
  Baksteen.R_Waarde = 0.08
  Baksteen.Dikte    = 0.1
  Baksteen.Cap_kJ   = 1500
  
  Glaswol_5cm = Heat_Transfer_Object ( "Glaswol 5cm" )
  Glaswol_5cm.Lambda = 0.035
  Glaswol_5cm.Dikte  = 0.05

  Buitenmuur_Lengte = 9.40
  Binnenmuur_Lengte = 1

  Buitenmuur_Nu = Sandwich ( "Buitenmuur_Nu" )
  Buitenmuur_Nu.Lengte              = Buitenmuur_Lengte
  Buitenmuur_Nu.Hoogte              = Hoogte
  Buitenmuur_Nu.Dikte               = 0.1
  Buitenmuur_Nu.Temperature_Inside  = Temperatuur_Binnen
  Buitenmuur_Nu.Temperature_Outside = Temperatuur_Buiten
  Buitenmuur_Nu.Add ( Rsi )
  Buitenmuur_Nu.Add ( Kalkzandsteen )
  Buitenmuur_Nu.Add ( Glaswol_5cm )
  Buitenmuur_Nu.Add ( Spouw_Zwak_Geventileerd )
  Buitenmuur_Nu.Add ( Baksteen )
  Buitenmuur_Nu.Add ( Rse )
  print ( Buitenmuur_Nu )


  # Voor de vloer gelden afwijkende waarden
  Rsi_Vloer = Heat_Transfer_Object ( "Rsi Vloer" )
  Rsi_Vloer.R_Waarde = 0.17
  Rse_Vloer = Heat_Transfer_Object ( "Rse Vloer" )
  Rse_Vloer.R_Waarde = 0.17
  
  Rsi_Plafond = Heat_Transfer_Object ( "Rsi Plafond" )
  Rsi_Plafond.R_Waarde = 0.1
  Rse_Plafond = Heat_Transfer_Object ( "Rse Plafond" )
  Rse_Plafond.R_Waarde = 0.1

  
  Woonkamer_Vloer = Heat_Transfer_Object ( "Woonkamer Vloer Beton" )  
  Woonkamer_Vloer.Lambda = Beton_Zwaar_Lambda
  Woonkamer_Vloer.Dikte = 0.20
  
  Woonkamer_Piepschuim = Heat_Transfer_Object ( "Woonkamer Vloer Piepschuim" )  
  Woonkamer_Piepschuim.Lambda = Piepschuim_Lambda
  Woonkamer_Piepschuim.Dikte = 0.10
  
  Kurk_Vloer = Heat_Transfer_Object ( "Woonkamer KurkVloer" )  
  Kurk_Vloer.Lambda = Kurk_Lambda
  Kurk_Vloer.Dikte = 0.003
  
  Vloer = Sandwich ( "Woonkamer.Vloer" )
  Vloer.Lengte              = Lengte
  Vloer.Breedte             = Breedte
  Vloer.Temperature_Inside  = Temperatuur_Binnen
  Vloer.Temperature_Outside = Temperatuur_Kruipruimte
  Vloer.Add ( Rsi_Vloer )
  Vloer.Add ( Kurk_Vloer )
  Vloer.Add ( Woonkamer_Vloer )
  Vloer.Add ( Woonkamer_Piepschuim )
  Vloer.Add ( Rse_Vloer )
  print ( Vloer )
  
  Ts  = range ( -5, 15, 5 )
  Elements = [ Vloer, Buitenmuur_Nu ]
  print ( Heat_Transfer_Table ( Elements, Ts ) )
  print ( Heat_Params_Table   ( Elements ) )
  
  stop #****************************************************
  A = Calc_Transfer ( 
        TBinnen     = 20.5,
        TBinnenMuur = 20.05,
        Rsi         = 0.13,
        Rse         = 0.13,
        Rm          = 2.5,
        TBuitenMuur = 11.3,
        Positie     = "Wand",
        GrenstAan   = "Onverwarmd",
      )                  
  print ( A ) 
  B = Calc_Transfer ( 
        TBinnen     = 20.5,
        TBinnenMuur = 20.05,
        TBuitenMuur = 11.3,
        #TBuiten     = 11,
      )                  
  print ( B ) 
  #print ( A["Opmerkingen"])
  
  C = Calc_Transfer_Object (
        #TBinnen     = 20.5,
        TBinnenMuur = 20.05,
        TBuitenMuur = 11.3,
        #TBuiten     = 11,
      )

  print ( C )  

