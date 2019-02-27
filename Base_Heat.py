
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
    Line += "Name        = %s\n" % self.Name
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
#      Line += "Oppervlakte = %s [m2]\n" % self.Oppervlakte ()
    
    if ( PrintLevel > 3 ) and ( self.Lambda != -1 ) :
      Line += "Lambda      = %.2f [W/m.K]\n" % self.Lambda
    if ( PrintLevel > 3 ) and ( self.R_Waarde != -1 ):
      Line += "R-Waarde    = %.2f [m2.K/W]\n" % self.R_Waarde
    if ( PrintLevel > 3 ) and ( self.U_Waarde != -1 ) :
      Line += "U-Waarde    = %.2f [W/m2.K]\n" % self.U_Waarde
    
    Het_Transfer_m2 = -1 ;
    if ( PrintLevel > 3 ) and ( self.Temperature_Inside != -1000 ) and ( self.Temperature_Outside != -1000 ) :
      Line += "T-Inside    = %.1f [Celsius]\n" % self.Temperature_Inside
      Line += "T-Outside   = %.1f [Celsius]\n" % self.Temperature_Outside

      Heat_Transfer_m2 = ( self.Temperature_Inside - self.Temperature_Outside ) / self.R_Waarde
      if Heat_Transfer_m2 != -1 :
        if ( self.Lengte != -1 ) and ( self.Breedte != -1 ) :  
          Heat_Transfer = self.Lengte * self.Breedte * Heat_Transfer_m2
          Line += "Heat Loss   = %d [W]\n" % Heat_Transfer

        elif ( self.Lengte != -1 ) and ( self.Hoogte != -1 ) :  
          Heat_Transfer = self.Lengte * self.Hoogte * Heat_Transfer_m2
          Line += "Heat Loss   = %d [W]\n" % Heat_Transfer

        Line += "Heat Loss 1m2   = %d [W]\n" % Heat_Transfer_m2
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

  # ***********************************************
  def Kosten_m2 ( self ) :
    #Heat_Transfer_m2 = ( self.Temperature_Inside - self.Temperature_Outside ) / self.R_Waarde
    #Kosten = 24 * 100 * Heat_Transfer_m2 * GasPrice / 10000
    Kosten = 24 * GraadDagen * GasPrice / ( 10000 * self.R_Waarde )
    return Kosten
  

  R_Waarde = property ( _get_R_Waarde, _set_R_Waarde )
  U_Waarde = property ( _get_U_Waarde, _set_U_Waarde )


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
  def _get_U_Waarde ( self ) :
    return 1.0 / self.R_Waarde 

  # ***********************************************
  def __repr__ ( self ) :
    Line = _Heat_TO.__repr__ ( self )
    
    R_Waarde = "R-Waarden = %.2f [ " % self.R_Waarde
    U_Waarde = "U-Waarden = %.2f [ " % self.U_Waarde
    Dikten   = "Dikten    = [ " 
    Line += "Layers    = [ "
    for Layer in self.Layers :
      Line     += Layer.Name + ", "
      if Layer.Dikte > 0 :
        Dikten   += "%.1f, " % (100*Layer.Dikte)
      else :
        Dikten   += "-, "
      R_Waarde += "%.2f, " % Layer.R_Waarde
      U_Waarde += "%.2f, " % Layer.U_Waarde
    Line += " ]\n"
    if ( PrintLevel > 3 ) : Line += Dikten   + " ] [cm]\n"
    Line += R_Waarde + " ] [m2.K/W]\n"
    if ( PrintLevel > 3 ) : Line += U_Waarde + " ] [W/m2.K]\n"

    if ( PrintLevel > 3 ) and ( self.Temperature_Inside != -1000 ) and ( self.Temperature_Outside != -1000 ) :
      Line += "T-Inside  = %.1f [Celsius]\n" % self.Temperature_Inside
      Line += "T-Outside = %.1f [Celsius]\n" % self.Temperature_Outside

      if ( self.Lengte != -1 ) and ( self.Breedte != -1 ) :  
        Heat_Transfer = self.Lengte * self.Breedte * ( self.Temperature_Inside - self.Temperature_Outside ) / self.R_Waarde
        Line += "Heat Loss = %d [W]\n" % Heat_Transfer
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

  Totaal = [ "R-waarde", "U-waarde", "Oppervlak", "T-Binnen", "T-Buiten", "Kosten-m2", "Kosten", "Jaar-m3" ]
  df = pd.DataFrame ( index = Totaal + list(Ts) )
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

  #%%!print ( df )
  #print ( Element_Names )
  return df


# ***************************************************************************    
# ***************************************************************************    


# ***************************************************************************    
# ***************************************************************************    


