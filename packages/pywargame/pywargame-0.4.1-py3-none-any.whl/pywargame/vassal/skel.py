## BEGIN_IMPORT
from .. common import VerboseGuard
from . base import *
from . element import Element
## END_IMPORT

# --------------------------------------------------------------------
class GameElement(Element):
    def __init__(self,game,tag,node=None,**kwargs):
        super(GameElement,self).__init__(game,tag,node=node,**kwargs)

    def getGame(self):
        return self.getParent(Game)
    

# --------------------------------------------------------------------
class Notes(GameElement):
    TAG = Element.MODULE+'NotesWindow'
    def __init__(self,elem,node=None,
                 name             = 'Notes',
                 buttonText       = '',
                 hotkey           = key('N',ALT),
                 icon             = '/images/notes.gif',
                 tooltip          = 'Show notes window'):
        super(Notes,self).__init__(elem,self.TAG,node=node,
                                   name       = name,
                                   buttonText = buttonText,
                                   hotkey     = hotkey,
                                   icon       = icon,
                                   tooltip    = tooltip)
    def encode(self):
        return ['NOTES\t\\','PNOTES']

registerElement(Notes)

# --------------------------------------------------------------------
class PredefinedSetup(GameElement):
    TAG = Element.MODULE+'PredefinedSetup'
    def __init__(self,elem,node=None,
                 name             = '',
                 file             = '',
                 useFile          = False,
                 isMenu           = False,
                 description      = ''):
        useFile = ((useFile or not isMenu) and
                   (file is not None and len(file) > 0))
        if file is None: file = ''
        super(PredefinedSetup,self).__init__(elem,self.TAG,node=node,
                                             name        = name,
                                             file        = file,
                                             useFile     = useFile,
                                             isMenu      = isMenu,
                                             description = description)
    def addPredefinedSetup(self,**kwargs):
        '''Add a `PredefinedSetup` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        Returns
        -------
        element : PredefinedSetup
            The added element
        '''
        return self.add(PredefinedSetup,**kwargs)
    def getPredefinedSetups(self,asdict=True):
        '''Get all PredefinedSetup element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `PredefinedSetup` elements.  If `False`, return a list of all PredefinedSetup` children.
        Returns
        -------
        children : dict or list
            Dictionary or list of `PredefinedSetup` children
        '''
        return self.getElementsByKey(PredefinedSetup,'name',asdict)
        
    
        
                   
registerElement(PredefinedSetup)
                  
# --------------------------------------------------------------------
class GlobalTranslatableMessages(GameElement):
    TAG=Element.MODULE+'properties.GlobalTranslatableMessages'
    def __init__(self,elem,node=None):
        '''Translations

        Parameters
        ----------
        doc : Element
            Parent
        node : xml.dom.Element
            Node to read state from
        '''
        super(GlobalTranslatableMessages,self).\
            __init__(elem,self.TAG,node=node)

registerElement(GlobalTranslatableMessages)
                  
# --------------------------------------------------------------------
class Language(GameElement):
    TAG = 'VASSAL.i18n.Language'
    def __init__(self,elem,node=None,**kwargs):
        super(Languate,self).__init__(sele,self.TAG,node=none,**kwargs)
        
registerElement(Language)
                  
# --------------------------------------------------------------------
class Chatter(GameElement):
    TAG=Element.MODULE+'Chatter'
    def __init__(self,elem,node=None,**kwargs):
        '''Chat

        Parameters
        ----------
        doc : Element
            Parent
        node : xml.dom.Element
            Node to read state from
        kwargs : dict
            Attributes
        '''
        super(Chatter,self).__init__(elem,self.TAG,node=node,**kwargs)
        
registerElement(Chatter)
                  
# --------------------------------------------------------------------
class KeyNamer(GameElement):
    TAG=Element.MODULE+'KeyNamer'
    def __init__(self,elem,node=None,**kwargs):
        '''Key namer (or help menu)

        Parameters
        ----------
        doc : Element
            Parent
        node : xml.dom.Element
            Node to read state from
        kwargs : dict
            Attributes
        '''
        super(KeyNamer,self).__init__(elem,self.TAG,node=node,**kwargs)
        
registerElement(KeyNamer)

# --------------------------------------------------------------------
class GlobalOptions(GameElement):
    TAG = Element.MODULE+'GlobalOptions'
    def __init__(self,doc,node=None,
                 autoReport               = "Use Preferences Setting",
                 centerOnMove             = "Use Preferences Setting",
                 chatterHTMLSupport       = "Always",
                 hotKeysOnClosedWindows   = "Never",
                 inventoryForAll          = "Always",
                 nonOwnerUnmaskable       = "Use Preferences Setting",
                 playerIdFormat           = "$playerName$",
                 promptString             = "Opponents can unmask pieces",
                 sendToLocationMoveTrails = "Never"):
        '''Set global options on the module

        Parameters
        ----------
        doc : Element
            Parent
        node : xml.dom.Element
            Node to read state from 
        autoReport               : str Option
        centerOnMove             : str Option
        chatterHTMLSupport       : str Option
        hotKeysOnClosedWindows   : str Option
        inventoryForAll          : str Option
        nonOwnerUnmaskable       : str Option
        playerIdFormat           : str Option
        promptString             : str Option
        sendToLocationMoveTrails : str Option
        '''
        super(GlobalOptions,self).\
            __init__(doc,self.TAG,node=node,
                     autoReport               = autoReport,
                     centerOnMove             = centerOnMove,
                     chatterHTMLSupport       = chatterHTMLSupport,
                     hotKeysOnClosedWindows   = hotKeysOnClosedWindows,
                     inventoryForAll          = inventoryForAll,
                     nonOwnerUnmaskable       = nonOwnerUnmaskable,
                     playerIdFormat           = playerIdFormat,
                     promptString             = promptString,
                     sendToLocationMoveTrails = sendToLocationMoveTrails)

    def addOption(self,**kwargs):
        '''Add a `Option` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        Returns
        -------
        element : Option
            The added element
        '''
        return self.add(Option,**kwargs)
    def getOptions(self):
        return self.getElementsByKey(Option,'name')
    
registerElement(GlobalOptions)


# --------------------------------------------------------------------
class Option(Element):
    TAG = 'option'
    def __init__(self,doc,node=None,name='',value=''):
        super(Option,self).__init__(doc,node=node,name=name)
        self._root.addText(self._node,value)

    def getGlobalOptions(self):
        return self.getParent(GlobalOptions)
    
registerElement(Option)

# --------------------------------------------------------------------
# CurrentMap == &quot;Board&quot;
class Inventory(GameElement):
    TAG = Element.MODULE+'Inventory'
    def __init__(self,doc,node=None,
                  canDisable          = False,
                  centerOnPiece       = True,
                  disabledIcon        = '',
                  drawPieces          = True,
                  foldersOnly         = False,
                  forwardKeystroke    = True,
                  groupBy             = '',
                  hotkey              = key('I',ALT),
                  icon                = '/images/inventory.gif',
                  include             = '{}',
                  launchFunction      = 'functionHide',
                  leafFormat          = '$PieceName$',
                  name                = '',
                  nonLeafFormat       = '$PropertyValue$',
                  pieceZoom           = '0.33',
                  pieceZoom2          = '0.5',
                  pieceZoom3          = '0.6',
                  propertyGate        = '',
                  refreshHotkey       = key('I',ALT_SHIFT),
                  showMenu            = True,
                  sides               = '',
                  sortFormat          = '$PieceName$',
                  sortPieces          = True,
                  sorting             = 'alpha',
                  text                = '',
                  tooltip             = 'Show inventory of all pieces',
                  zoomOn              = False):
        super(Inventory,self).__init__(doc,self.TAG,node=node,
                                       canDisable          = canDisable,
                                       centerOnPiece       = centerOnPiece,
                                       disabledIcon        = disabledIcon,
                                       drawPieces          = drawPieces,
                                       foldersOnly         = foldersOnly,
                                       forwardKeystroke    = forwardKeystroke,
                                       groupBy             = groupBy,
                                       hotkey              = hotkey,
                                       icon                = icon,
                                       include             = include,
                                       launchFunction      = launchFunction,
                                       leafFormat          = leafFormat,
                                       name                = name,
                                       nonLeafFormat       = nonLeafFormat,
                                       pieceZoom           = pieceZoom,
                                       pieceZoom2          = pieceZoom2,
                                       pieceZoom3          = pieceZoom3,
                                       propertyGate        = propertyGate,
                                       refreshHotkey       = refreshHotkey,
                                       showMenu            = showMenu,
                                       sides               = sides,
                                       sortFormat          = sortFormat,
                                       sortPieces          = sortPieces,
                                       sorting             = sorting,
                                       text                = text,
                                       tooltip             = tooltip,
                                       zoomOn              = zoomOn)
                  
registerElement(Inventory)

# --------------------------------------------------------------------
class Prototypes(GameElement):
    TAG = Element.MODULE+'PrototypesContainer'
    def __init__(self,game,node=None,**kwargs):
        super(Prototypes,self).\
            __init__(game,self.TAG,node=node,**kwargs)

    def addPrototype(self,**kwargs):
        '''Add a `Prototype` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        Returns
        -------
        element : Prototype
            The added element
        '''
        return self.add(Prototype,**kwargs)
    def getPrototypes(self,asdict=True):
        '''Get all Prototype element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Prototype` elements.  If `False`, return a list of all Prototype` children.
        Returns
        -------
        children : dict or list
            Dictionary or list of `Prototype` children
        '''
        return self.getElementsByKey(Prototype,'name',asdict=asdict)
        
    

registerElement(Prototypes)

# --------------------------------------------------------------------
class DiceButton(GameElement):
    TAG=Element.MODULE+'DiceButton'
    def __init__(self,elem,node=None,
                 addToTotal           = 0,
                 canDisable           = False,
                 hotkey               = key('6',ALT),
                 icon                 = '/images/die.gif',
                 keepCount            = 1,
                 keepDice             = False,
                 keepOption           = '>',
                 lockAdd              = False,
                 lockDice             = False,
                 lockPlus             = False,
                 lockSides            = False,
                 nDice                = 1,
                 nSides               = 6,
                 name                 = '1d6',
                 plus                 = 0,
                 prompt               = False,
                 propertyGate         = '',
                 reportFormat         = '** $name$ = $result$ *** <$PlayerName$>;',
                 reportTotal          = False,
                 sortDice             = False,
                 text                 = '1d6',
                 tooltip              = 'Roll a 1d6'):
        super(DiceButton,self).\
            __init__(elem,self.TAG,node=node,
                     addToTotal           = addToTotal,
                     canDisable           = canDisable,
                     hotkey               = hotkey,
                     icon                 = icon,
                     keepCount            = keepCount,
                     keepDice             = keepDice,
                     keepOption           = keepOption,
                     lockAdd              = lockAdd,
                     lockDice             = lockDice,
                     lockPlus             = lockPlus,
                     lockSides            = lockSides,
                     nDice                = nDice,
                     nSides               = nSides,
                     name                 = name,
                     plus                 = plus,
                     prompt               = prompt,
                     propertyGate         = propertyGate,
                     reportFormat         = reportFormat,
                     reportTotal          = reportTotal,
                     sortDice             = sortDice,
                     text                 = text,
                     tooltip              = tooltip)

registerElement(DiceButton)

#
# EOF
#
