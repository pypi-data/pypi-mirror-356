#!/usr/bin/env python
# Script collected from other scripts
#
#   ../common/singleton.py
#   ../common/verbose.py
#   ../common/verboseguard.py
#   ../common/dicedraw.py
#   xml.py
#   base.py
#   element.py
#   folder.py
#   globalkey.py
#   gameelements.py
#   mapelements.py
#   globalproperty.py
#   turn.py
#   documentation.py
#   player.py
#   chessclock.py
#   widget.py
#   grid.py
#   zone.py
#   board.py
#   map.py
#   chart.py
#   command.py
#   trait.py
#   withtraits.py
#   extension.py
#   traits/area.py
#   traits/clone.py
#   traits/dynamicproperty.py
#   traits/globalproperty.py
#   traits/prototype.py
#   traits/place.py
#   traits/report.py
#   traits/calculatedproperty.py
#   traits/restrictcommand.py
#   traits/label.py
#   traits/layer.py
#   traits/globalcommand.py
#   traits/globalhotkey.py
#   traits/nostack.py
#   traits/deselect.py
#   traits/restrictaccess.py
#   traits/rotate.py
#   traits/stack.py
#   traits/mark.py
#   traits/mask.py
#   traits/trail.py
#   traits/delete.py
#   traits/sendto.py
#   traits/moved.py
#   traits/skel.py
#   traits/submenu.py
#   traits/basic.py
#   traits/trigger.py
#   traits/nonrect.py
#   traits/click.py
#   traits/mat.py
#   traits/cargo.py
#   traits/movefixed.py
#   traits/sheet.py
#   traits/hide.py
#   traits/retrn.py
#   game.py
#   buildfile.py
#   moduledata.py
#   save.py
#   vsav.py
#   vmod.py
#   upgrade.py
#   exporter.py
#
# ====================================================================
# From ../common/singleton.py
# ====================================================================
class Singleton(type):
    '''Meta base class for singletons'''
    _instances = {}
    def __call__(cls, *args, **kwargs):
        '''Create the singleton object or returned existing

        Parameters
        ----------
        args : tuple
            Arguments
        kwargs : dict
            Keyword arguments
        '''
        if cls not in cls._instances:
            cls._instances[cls] = \
                super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

#
# EOF
#
# ====================================================================
# From ../common/verbose.py
# --------------------------------------------------------------------

class Verbose(metaclass=Singleton):
    def __init__(self,verbose=False):
        '''Singleton for writing message to screen, contigent on setting

        Parameters
        ----------
        verbose : bool
             Whether to show messages or not
        '''
        self._indent  = ''
        self._verbose = verbose

    def setVerbose(self,verbose):
        '''Set whether to print or not

        Parameters
        ----------
        verbose : bool
             Whether to show messages or not
        '''
        self._verbose = verbose

    @property
    def verbose(self):
        '''Test if this is verbose'''
        return self._verbose

    def message(self,*args,**kwargs):
        '''Write messsage if verbose

        Parameters
        ----------
        args : tuple
            Arguments
        kwargs : dict
            Keyword arguments
        '''        
        if not self._verbose: return
        if not kwargs.pop('noindent', False):
            print(self._indent,end='')
        print(*args,**kwargs)

    def incr(self):
        '''Increment indention'''
        self._indent += ' '

    def decr(self):
        '''Decrement indention'''
        if len(self._indent) > 0:
            self._indent = self._indent[:-1]

#
# EOF
#
# ====================================================================
# From ../common/verboseguard.py
# --------------------------------------------------------------------

class VerboseGuard:
    def __init__(self,*args,**kwargs):
        '''A guard pattern that increases verbose indention

        This is a context manager.  The arguments passed are used for
        an initial message, before increasinig indention.

        Parameters
        ----------
        args : tuple
            Arguments
        kwargs : dict
            Keyword arguments
        '''                
        Verbose().message(*args,**kwargs)

    def __bool_(self):
        '''Test if verbose'''
        return Verbose().verbose
    
    def __enter__(self):
        '''Enter context'''
        Verbose().incr()
        return self

    def __exit__(self,*args):
        '''Exit context'''        
        Verbose().decr()

    @property
    def i(self):
        return Verbose()._indent
    
    def __call__(self,*args,**kwargs):
        '''Write a message at current indention level
        
        Parameters
        ----------
        args : tuple
            Arguments
        kwargs : dict
            Keyword arguments
        '''                
        Verbose().message(*args,**kwargs)

#
# EOF
#
# ====================================================================
# From ../common/dicedraw.py
# --------------------------------------------------------------------
class DiceContext:
    def __init__(self,draw,darker=None):
        self._draw = draw
        self._darker = darker
        
        

    def __enter__(self):
        from wand.color import Color
        self._draw._draw.push()

        if self._darker:
            r, g, b = (self._draw._draw.fill_color.red_int8,
                       self._draw._draw.fill_color.green_int8,
                       self._draw._draw.fill_color.blue_int8)
            r *= self._darker
            g *= self._darker
            b *= self._darker
            #print(r,g,b)        
            self._draw._draw.fill_color = \
                Color(f'srgb({int(r)},{int(g)},{int(b)})')
        
        return self._draw

    def __exit__(self,*e):
        self._draw._draw.pop()

# --------------------------------------------------------------------
class DicePath:
    def __init__(self,draw):
        self._draw = draw

    def __enter__(self):
        self._draw._draw.path_start()
        return self

    def __exit__(self,*e):
        self._draw._draw.path_finish()

    def move(self,to):
        self._draw._draw.path_move(to=(self._draw.x(to[0]),
                                       self._draw.y(to[1])))
        
    def line(self,to):
        self._draw._draw.path_line(to=(self._draw.x(to[0]),
                                       self._draw.y(to[1])))

    def arc(self,to,r,cw=True):
        self._draw._draw.path_elliptic_arc(to=(self._draw.x(to[0]),
                                               self._draw.y(to[1])),
                                           radius=(self._draw.x(r),
                                                   self._draw.y(r)),
                                           clockwise=cw)
        
# --------------------------------------------------------------------
class DiceDraw:
    def __init__(self,width=100,height=100,fg='black',bg='white'):
        from wand.drawing import Drawing
        from wand.color import Color
        
        self._width  = width
        self._height = height
        self._fg     = fg if isinstance(fg,Color) else Color(fg)
        self._bg     = bg if isinstance(bg,Color) else Color(bg)
        self._draw   = Drawing()
        self._size   = min(self._width,self._height)

    @property
    def size(self):
        return self._size
    
    def x(self,xx):
        return int((xx  + 0.5) * self.size)

    def y(self,yy):
        return  int((0.5 -  yy) * self.size)

    def __enter__(self):
        self._draw.stroke_width = max(1,self.size//75)
        self._draw.stroke_color = self._fg
        self._draw.fill_color   = self._bg
        return self

    def number(self,num,yoff=0,scale=1):
        if num is None or num == '':
            return
        
        with DiceContext(self):
            self._draw.stroke_width   = 1
            self._draw.stroke_color   = self._fg
            self._draw.fill_color     = self._fg
            self._draw.text_alignment = 'center'
            self._draw.font_size      = scale * self.size / 2
            self._draw.text(self.x(0),
                            int(self.y(yoff)+self._draw.font_size//2),
                            f'{num}')
            
    def image(self):
        from wand.image import Image as WImage
        
        image = WImage(width=self._width,height=self._height,format='png')
        image.alpha_channel = True
        self._draw(image)
        
        off   = min(self._width,self._height) // 30
        copy  = image.clone()
        copy.shadow(50,off,0,0)
        copy.negate(channel='rgb')
        copy.composite(image,int(off/4),int(off/4))
        
        #copy.save(filename='d4.png')
        return copy

    def __exit__(self,*e):
        pass 

# --------------------------------------------------------------------
class DiceDrawer:
    def __init__(self,nsides,width,height,fg='red',bg='white'):
        from wand.color import Color
        self._nsides = nsides
        self._width  = width
        self._height = height
        self._fg     = Color(fg if isinstance(fg,str) else f'#{fg:06x}')
        self._bg     = Color(bg if isinstance(bg,str) else f'#{bg:06x}')
        if self._nsides not in [4,6,8,10,12,20]:
            raise RuntimeError(f'Unknown number of sides: {self._nsides}')
            

    def draw(self,num):
        if self._nsides ==  4:  return self.draw_d4 (num)
        if self._nsides ==  6:  return self.draw_d6 (num)
        if self._nsides ==  8:  return self.draw_d8 (num)
        if self._nsides == 10:  return self.draw_d10(num)
        if self._nsides == 12:  return self.draw_d12(num)
        if self._nsides == 20:  return self.draw_d20(num)
        return None
        
    def draw_d4(self,num):
        with DiceDraw(self._width,self._height,
                      fg=self._fg,bg=self._bg) as draw:
            with DicePath(draw) as path:
                path.move(to=( 0.000, 0.40))
                path.line(to=( 0.433,-0.35))
                path.line(to=(-0.433,-0.35))
                path.line(to=( 0.000, 0.40))

            draw.number(num)
            return draw.image()

    def draw_d6(self,num):
        with DiceDraw(self._width,self._height,
                      fg=self._fg,bg=self._bg) as draw:
            with DicePath(draw) as path:
                r = 0.05
                w = .4 - r
                path.move(to=(    w, 0.40))
                path.arc (to=( 0.40,    w), r=r)
                path.line(to=( 0.40,-   w))
                path.arc (to=(    w,-0.40), r=r)
                path.line(to=(-   w,-0.40))
                path.arc (to=(-0.40,-   w), r=r)
                path.line(to=(-0.40,    w))
                path.arc (to=(-   w, 0.40), r=r)
                path.line(to=(    w, 0.40))

            draw.number(num,yoff=.1)
            return draw.image()

    def draw_d8(self,num):
        with DiceDraw(self._width,self._height,
                      fg=self._fg,bg=self._bg) as draw:
            with DiceContext(draw,darker=.9):
                with DicePath(draw) as path:
                    path.move(to=(0.0000,0.5000))
                    path.line(to=(0.4330,0.2500))
                    path.line(to=(0.4330,-0.2500))
                    path.line(to=(0.0000,-0.5000))
                    path.line(to=(-0.4330,-0.2500))
                    path.line(to=(-0.4330,0.2500))
                    path.line(to=(0.0000,0.5000))
                        
            with DicePath(draw) as path:
                path.move(to=(0.0000,0.5000))
                path.line(to=(0.4330,-0.2500))
                path.line(to=(-0.4330,-0.2500))
                path.line(to=(0.0000,0.5000))

            draw.number(num,yoff=.1)
            return draw.image()

    def draw_d10(self,num):
        with DiceDraw(self._width,self._height,
                      fg=self._fg,bg=self._bg) as draw:
            with DiceContext(draw,darker=.9):
                with DicePath(draw) as path:
                    path.move(to=(0.0000,0.5000))            
                    path.line(to=(0.4750,0.1000))
                    path.line(to=(0.4750,-0.1000))
                    path.line(to=(0.0000,-0.5000))
                    path.line(to=(-0.4750,-0.1000))
                    path.line(to=(-0.4750,0.1000))
                    path.line(to=(0.0000,0.5000))
                    path.move(to=(0.2940,-0.1540))
                    path.line(to=(0.4750,-0.1000))
                    path.move(to=(-0.4750,-0.1000))
                    path.line(to=(-0.2940,-0.1540))
                    path.move(to=(0.0000,-0.5000))
                    path.line(to=(0.0000,-0.3000))
            with DicePath(draw) as path:
                path.move(to=(0.0000,0.5000))
                path.line(to=(0.2940,-0.1540))
                path.line(to=(0.0000,-0.3000))
                path.line(to=(-0.2940,-0.1540))
                path.line(to=(0.0000,0.5000))

            draw.number(num,yoff=.1)
            return draw.image()

    def draw_d12(self,num):
        with DiceDraw(self._width,self._height,
                      fg=self._fg,bg=self._bg) as draw:
            with DiceContext(draw,darker=.9):
                with DicePath(draw) as path:
                    path.move(to=( 0.0000, 0.5000))
                    path.line(to=( 0.2940, 0.4050))
                    path.line(to=( 0.4750, 0.1730))
                    path.line(to=( 0.4750,-0.1730))
                    path.line(to=( 0.2940,-0.4050))
                    path.line(to=( 0.0000,-0.5000))
                    path.line(to=(-0.2940,-0.4050))
                    path.line(to=(-0.4750,-0.1730))
                    path.line(to=(-0.4750, 0.1730))
                    path.line(to=(-0.2940, 0.4050))
                    path.line(to=( 0.0000, 0.5000))
                    path.line(to=( 0.0000, 0.3490))
                    path.move(to=( 0.4750, 0.1730))
                    path.line(to=( 0.3320, 0.1080))
                    path.move(to=( 0.2940,-0.4050))
                    path.line(to=( 0.2050,-0.2820))
                    path.move(to=(-0.2940,-0.4050))
                    path.line(to=(-0.2050,-0.2820))
                    path.move(to=(-0.4750, 0.1730))
                    path.line(to=(-0.3320, 0.1080))
            with DicePath(draw) as path:
                path.move(to=(0.0000,0.3490))
                path.line(to=(0.3320,0.1080))
                path.line(to=(0.2050,-0.2820))
                path.line(to=(-0.2050,-0.2820))
                path.line(to=(-0.3320,0.1080))
                path.line(to=(0.0000,0.3490))
                    

            draw.number(num,yoff=.1)
            return draw.image()
            
    def draw_d20(self,num):
        with DiceDraw(self._width,self._height,
                      fg=self._fg,bg=self._bg) as draw:
            with DiceContext(draw,darker=.85):
                with DicePath(draw) as path:
                    path.move(to=(0.0000,0.5000))
                    path.line(to=(0.4540,0.2620))
                    path.line(to=(0.4540,-0.2620))
                    path.line(to=(0.0000,-0.5000))
                    path.line(to=(-0.4540,-0.2620))
                    path.line(to=(-0.4540,0.2620))
                    path.line(to=(0.0000,0.5000))            
                    path.line(to=(0.0000,0.2920))
            with DiceContext(draw,darker=.95):
                with DicePath(draw) as path:
                    path.move(to=(0.0000,0.2920))
                    path.line(to=(0.4540,0.2620))
                    path.line(to=(0.2530,-0.1460))
                    path.line(to=(0.0000,-0.5000))
                    path.line(to=(-0.2530,-0.1460))
                    path.line(to=(-0.4540,0.2620))
                    path.line(to=(0.0000,0.2920))
                    path.move(to=(0.4540,-0.2620))
                    path.line(to=(0.2530,-0.1460))
                    path.move(to=(-0.4540,-0.2620))
                    path.line(to=(-0.2530,-0.1460))
            with DicePath(draw) as path:
                path.move(to=(0.0000,0.2920))
                path.line(to=(0.2530,-0.1460))
                path.line(to=(-0.2530,-0.1460))
                path.line(to=(0.0000,0.2920))
            

            scale = .7
            yoff  = .07
            if num > 9:
                scale *= .8
                yoff  =  .015
            draw.number(num,yoff=yoff,scale=scale)
            return draw.image()


# --------------------------------------------------------------------
class DiceAnimator:
    def __init__(self,nsides,width,height,fg='red',bg='white'):
        drawer = DiceDrawer(nsides = nsides,
                            width  = width,
                            height = height,
                            fg     = fg,
                            bg     = bg)
        self._pool = [drawer.draw(v) for v in range(1,nsides+1)]
            
    def draw(self,num,n,dt=10):
        
        '''
        delay : int
            1 / 100 of a second as base delay
        '''
        from random     import sample
        from wand.image import Image

        if num > len(self._pool):
            raise RuntimeError(f'Final value {num} not possible for '
                               f'd{len(self._pool)}')

        if n >= len(self._pool) - 1:
            raise RuntimeError(f'Pre-steps {n} not possible for '
                               f'd{len(self._pool)}')
            
        end   = self._pool[num-1]

        # Round-about, but for debug 
        nums  = list(range(1,len(self._pool)+1))
        nums.remove(num)
        pool  = sample(nums, k=n)
        other = [self._pool[i-1] for i in pool]
        print(num,pool)
        
        # More direct
        # pool  = self._pool[:num] + self._pool[num+1:]
        # other = sample(pool, k=n)
        
        faces = other + [end]
        dang  = 360 / (len(faces))
        img   = Image(format='gif')
        ang   = 360
        wait  = dt
        for i, face in enumerate(faces):
            ang  -= dang
            wait += dt

            with face.clone() as rotated:
                w, h = rotated.size
                rotated.rotate(ang, reset_coords=False)
                rotated.crop(0,0,w,h)
                rotated.dispose = 'previous'
                rotated.delay   = wait # dt * (i + 1)
                rotated.loop    = 1
                img.sequence.append(rotated)

        # Make sure we dispose of the previous image altogether
        #img.dispose = 'previous'
        img.coalesce()
        #img.deconstruct()
        

        return img

#
# EOF
#
# ====================================================================
# From xml.py
# --------------------------------------------------------------------
# XML Dom parser namespace
import xml.dom.minidom as xmlns
#import xml.dom as xmlns
# ====================================================================
# From base.py
# ====================================================================
# Key encoding
SHIFT = 65
CTRL = 130
ALT   = 520
CTRL_SHIFT = CTRL+SHIFT
ALT_SHIFT = ALT+SHIFT
NONE = '\ue004'
NONE_MOD = 0

# --------------------------------------------------------------------
def key(let,mod=CTRL):

    '''Encode a key sequence

    down  = 40,0
    up    = 38,0
    left  = 37,0
    right = 39,0

    Parameters
    ----------
    let : str
        Key code (Letter)
    mod : int
        Modifier mask
    '''
    if let is None:
        return f'{ord(NONE)},{NONE_MOD}'
    return f'{ord(let)},{mod}'

# --------------------------------------------------------------------
#
def hexcolor(s):
    if isinstance(s,str):
        s = s.replace('0x','')
        if len(s) == 3:
            r, g, b = [int(si,16)/16 for si in s]
        elif len(s) == 6:
            r = int(s[0:2],16) / 256
            g = int(s[2:4],16) / 256
            b = int(s[4:6],16) / 256
        else:
            raise RuntimeError('3 or 6 hexadecimal digits for color string')
    elif isinstance(s,int):
        r = ((s >> 16) & 0xFF) / 256
        g = ((s >>  8) & 0xFF) / 256
        b = ((s >>  0) & 0xFF) / 256
    else:
        raise RuntimeError('Hex colour must be string or integer')

    return rgb(int(r*256),int(g*256),int(b*256))
    
# --------------------------------------------------------------------
# Colour encoding 
def rgb(r,g,b):
    '''Encode RGB colour

    Parameters
    ----------
    r : int
        Red channel
    g : int
        Green channel
    b : int
        Blue channel

    Returns
    -------
    colour : str
        RGB colour as a string
    '''
    return ','.join([str(r),str(g),str(b)])

# --------------------------------------------------------------------
def rgba(r,g,b,a):
    '''Encode RGBA colour

    Parameters
    ----------
    r : int
        Red channel
    g : int
        Green channel
    b : int
        Blue channel
    a : int
        Alpha channel
    
    Returns
    -------
    colour : str
        RGBA colour as a string
    '''
    return ','.join([str(r),str(g),str(b),str(a)])

# --------------------------------------------------------------------
def dumpTree(node,ind=''):
    '''Dump the tree of nodes

    Parameters
    ----------
    node : xml.dom.Node
        Node to dump
    ind : str
        Current indent 
    '''
    print(f'{ind}{node}')
    for c in node.childNodes:
        dumpTree(c,ind+' ')

# --------------------------------------------------------------------
def registerElement(cls,uniqueAttr=[],tag=None):
    '''Register a TAG to element class, as well as unique attributes
    to compare when comparing objects of that element class.

    '''

    # Get class-level definitions of UNIQUE
    uniqueCls = getattr(cls,'UNIQUE',None)
    if uniqueCls:
        try:
            iter(uniqueCls)
        except:
            uniqueCls = list(uniqueCls)
    else:
        uniqueCls = []    
        
    tagName = cls.TAG if tag is None else tag 
    Element.known_tags  [tagName] = cls
    Element.unique_attrs[tagName] = uniqueAttr+uniqueCls
    
        
#
# EOF
#
# ====================================================================
# From element.py

# ====================================================================
class Element:
    BUILD  = 'VASSAL.build.'
    MODULE = BUILD  + 'module.'
    WIDGET = BUILD  + 'widget.'
    FOLDER = MODULE + 'folder.'
    MAP    = MODULE + 'map.'    
    PICKER = MAP    + 'boardPicker.'
    BOARD  = PICKER + 'board.'
    known_tags   = {}
    unique_attrs = {}
    
    def __init__(self,parent,tag,node=None,**kwargs):
        '''Create a new element

        Parameters
        ----------
        parent : Element
            Parent element to add this element to
        tag : str
            Element tag
        node : xml.dom.Node
            If not None, then read attributes from that. Otherwise
            set elements according to kwargs
        kwargs : dict
            Attribute keys and values.  Only used if node is None
        '''
        #from xml.dom.minidom import Document
        
        if parent is not None:
            self._tag  = tag                
            self._root = (parent if isinstance(parent,xmlns.Document) else
                          parent._root)
            self._node = (node if node is not None else
                          parent.addNode(tag,**kwargs))
        else:
            self._root = None
            self._node = None
            self._tag  = None

    # ----------------------------------------------------------------
    @classmethod
    def _make_unique(cls,tag,*values):
        return tag + ('_'+'_'.join(values) if len(values)>0 else '')
    
    def _unique(self):
        uattr = Element.unique_attrs.get(self._tag,[])
        return self._make_unique(self._tag,
                                 *[self.getAttribute(a) for a in uattr])
    
    def __hash__(self):
        return hash(self._unique())
    
    def __eq__(self,other):
        '''Equality comparison - check if to elements are the same.

        This is based on the tag of the elements first, then on the
        attributes.  However, not all attributes should be compared
        for equality - only thise that are meant to be unique.

        '''
        #print(f'Compare {self} to {other} ({self._tag},{other._tag})')
        if not isinstance(other,Element):
            return False
        return self.__hash__() == other.__hash__()
        #if self._tag != other._tag:
        #    return False

        # to be done
        #
        # uattr = Element.unique_attrs[self._tag]
        # attr  = self .getAttributes()
        # oattr = other.getAttributes()
        
        return True

        
    # ----------------------------------------------------------------
    # Attributes
    def __contains__(self,key):
        '''Check if element has attribute key'''        
        return self.hasAttribute(key)
    
    def __getitem__(self,key):
        '''Get attribute key value'''
        return self.getAttribute(key)

    def __setitem__(self,key,value):
        '''Set attribute key value'''
        self.setAttribute(key,value)

    def hasAttribute(self,k):
        '''Check if element has attribute '''
        return self._node.hasAttribute(k)

    def getAttribute(self,k):
        '''Get attribute key value'''
        return self._node.getAttribute(k)
        
    def setAttribute(self,k,v):
        '''Set attribute key value'''
        self._node.setAttribute(k,str(v).lower()
                                if isinstance(v,bool) else str(v))
        
    def setAttributes(self,**kwargs):
        '''Set attributes to dictionary key and value'''
        for k,v in kwargs.items():
            self.setAttribute(k,v)

    def getAttributes(self):
        '''Get attributes as dict'''
        return self._node.attributes

    # ----------------------------------------------------------------
    # Plain nodes
    def getChildren(self):
        '''Get child nodes (xml.dom.Node)'''
        return self._node.childNodes

    # ----------------------------------------------------------------
    # Getters
    #
    # First generics 
    def getAsDict(self,tag='',key=None,enable=True):
        '''Get elements with a specific tag as a dictionary
        where the key is given by attribute key'''
        cont = self._node.getElementsByTagName(tag)
        if not enable or key is None:
            return cont

        return {e.getAttribute(key): e for e in cont}

    def getAsOne(self,tag='',single=True):
        '''Get elements with a specific tag, as a list.
        If single is true, then assume we only have one such
        child element, or fail.'''
        cont = self._node.getElementsByTagName(tag)
        if single and len(cont) != 1:
            return None
        return cont
    
    def getElementsByKey(self,cls,key='',asdict=True):
        '''Get elments of a specific class as a dictionary,
        where the key is set by the key attribute.'''
        cont = self.getAsDict(cls.TAG,key,asdict)
        if cont is None: return None
        
        if not asdict: return [cls(self,node=n) for n in cont]

        return {k : cls(self,node=n) for k, n in cont.items()}

    def getAllElements(self,cls,single=True):
        '''Get elements with a specific tag, as a list.  If single is
        true, then assume we only have one such child element, or
        fail.

        If `cls` is None, then return _all_ child elements. 

        '''
        #from xml.dom.minidom import Text, Element as XMLElement
        if cls is None:
            ret = []
            for node in self.getChildren():
                if isinstance(node,xmlns.Text):
                    continue
                
                if not hasattr(node,'tagName'):
                    print(f'Do not know how to deal with {type(node)}')
                    continue

                tag = node.tagName
                cls = Element.getTagClass(tag)
                if cls is None:
                    raise RuntimeError(f'No class reflection of tag {tag}')
                
                ret.append(cls(self,node=node))

            return ret
                           
        cont = self.getAsOne(cls.TAG,single=single)
        if cont is None: return None
        return [cls(self,node=n) for n in cont]

    def getSpecificElements(self,cls,key,*names,asdict=True):
        '''Get all elements of specific class and that has the
        attribute key, and the attribute value is in names

        '''
        cont = self.getAsOne(cls.TAG,single=False)
        cand = [cls(self,node=n) for n in cont
                if n.getAttribute(key) in names]
        if asdict:
            return {c[key] : c for c in cand}
        return cand
    
    def getParent(self,cls=None,checkTag=True):
        if self._node.parentNode is None:
            return None
        if cls is None:
            cls = self.getTagClass(self._node.parentNode.tagName)
            checkTag = False
        if cls is None:
            return None
        if checkTag and self._node.parentNode.tagName != cls.TAG:
            return None
        return cls(self,node=self._node.parentNode)

    def getParentOfClass(self,cls):
        '''Searches back until we find the parent with the right
        class, or none
        '''
        try:
            iter(cls)
        except:
            cls = [cls]
        t = {c.TAG: c for c in cls}
        p = self._node.parentNode
        while p is not None:
            c = t.get(p.tagName,None)
            if c is not None: return c(self,node=p)
            p = p.parentNode
        return None

    @classmethod
    def getTagClass(cls,tag):
        '''Get class corresponding to the tag'''
        # if tag not in cls.known_tags: return None;
        # Older VASSAL may have funny tag-names
        return cls.known_tags.get(tag,None)
        
    # ----------------------------------------------------------------
    # Adders
    def addNode(self,tag,**attr):
        '''Add a note to this element

        Parameters
        ----------
        tag : str
            Node tag name
        attr : dict
            Attributes to set
        '''
        e = self._root.createElement(tag)
        if self._node: self._node.appendChild(e)

        for k, v in attr.items():
            e.setAttribute(k,str(v).lower() if isinstance(v,bool) else str(v))

        return e

    def addText(self,text):
        '''Add a text child node to an element'''
        t = self._root.createTextNode(text)
        self._node.appendChild(t)
        return t

    def hasText(self):
        return self._node.firstChild is not None and \
            self._node.firstChild.nodeType == self._node.firstChild.TEXT_NODE
        
    def getText(self):
        '''Get contained text node content'''
        if self._node.firstChild is None or \
           self._node.firstChild.nodeType != self._node.firstChild.TEXT_NODE:
            return ''
        return self._node.firstChild.nodeValue

    def setText(self,txt):
        '''Set contained text node content'''
        if self._node.firstChild is None or \
           self._node.firstChild.nodeType != self._node.firstChild.TEXT_NODE:
            return 
        self._node.firstChild.nodeValue = txt
    

    def add(self,cls,**kwargs):
        '''Add an element and return wrapped in cls object'''
        return cls(self,node=None,**kwargs)

    def append(self,elem):
        '''Append and element'''
        if self._node.appendChild(elem._node):
            return elem
        return False

    # ----------------------------------------------------------------
    def remove(self,elem):
        '''Remove an element'''
        try:
            self._node.removeChild(elem._node)
        except:
            return None
        return elem
    # ----------------------------------------------------------------
    def insertBefore(self,toadd,ref):
        '''Insert an element before another element'''
        try:
            self._node.insertBefore(toadd._node,ref._node)
        except:
            return None
        return toadd

    # ----------------------------------------------------------------
    def print(self,file=None,recursive=False,indent=''):
        '''Print this element, and possibly its child elements.

        If `file` is None, then print to stdout.  If `recursive` is
        `True`, then also print child elements.  If `recursive` is an
        integer, then print this many deep levels of child elements.

        '''
        if file is None:
            from sys import stdout
            file = stdout

        from io import StringIO
        from textwrap import indent as i

        stream = StringIO()
        
        print(f'Element TAG={self.TAG} CLS={self.__class__.__name__}',
              file=stream)
        attrs = self.getAttributes()
        #print(type(attrs))
        ln    = max([len(n) for n in attrs.keys()]+[0])
        for name,value in attrs.items():
            print(f' {name:{ln}s}: {value}',file=stream)

        if isinstance(recursive,bool):
            recursive = 1024 if recursive else 0# Large number
            
        if recursive > 1:
            for child in self.getAllElements(cls=None):
                child.print(file=stream,
                            recursive=recursive-1,
                            indent='  ')
        else:
            n = len(self.getChildren())
            if n > 0:
                print(f'  {n} child elements',file=stream)

        print(i(stream.getvalue(),indent).rstrip(),file=file)
            
            
        
# --------------------------------------------------------------------
class DummyElement(Element):
    def __init__(self,parent,node=None,**kwargs):
        '''A dummy element we can use to select elements of different
        classes

        '''  
        super(DummyElement,self).__init__(parent,'Dummy',node=node)

# --------------------------------------------------------------------
class ToolbarElement(Element):
    def __init__(self,
                 parent,
                 tag,
                 node         = None,
                 name         = '', # Toolbar element name
                 tooltip      = '', # Tool tip
                 text         = '', # Button text
                 icon         = '', # Button icon,
                 hotkey       = '', # Named key or key stroke
                 canDisable   = False,
                 propertyGate = '',
                 disabledIcon = '',
                 **kwargs):
        '''Base class for toolbar elements.

        Parameters
        ----------
        parent : Element
            Parent element if any
        tag : str
            Element tag
        node : XMLNode
            Possible node - when reading back
        name : str
            Name of element (user reminder).  If not set, and tooltip is set,
            set to tooltip
        toolttip : str        
            Tool tip when hovering. If not set, and name is set, then
            use name as tooltip.
        text : str
            Text of button
        icon : str
            Image path for button image
        hotkey : str
            Named key or key-sequence
        canDisable : bool
            If true, then the element can be disabled
        propertyGate : str        
            Name of a global property.  When this property is `true`,
            then this element is _disabled_.  Note that this _must_ be
            the name of a property - it cannot be a BeanShell
            expression.
        disabledIcon : str
            Path to image to use when the element is disabled.
        kwargs : dict
            Other attributes to set on the element
        '''
        if name == '' and tooltip != '': name    = tooltip
        if name != '' and tooltip == '': tooltip = name

        # Build arguments for super class 
        args = {
            'node':         node,
            'name':         name,
            'icon':         icon,
            'tooltip':      tooltip,
            'hotkey':       hotkey,
            'canDisable':   canDisable,
            'propertyGate': propertyGate,
            'disabledIcon': disabledIcon }
        bt = kwargs.pop('buttonText',None)
        # If the element expects buttonText attribute, then do not set
        # the text attribute - some elements interpret that as a
        # legacy name attribute,
        if bt is not None:
            args['buttonText'] = bt
        else:
            args['text']       = text
        args.update(kwargs)

        super(ToolbarElement,self).__init__(parent,
                                            tag,
                                            **args)
        # print('Attributes\n','\n'.join([f'- {k}="{v}"' for k,v in self._node.attributes.items()]))
        
#
# EOF
#
# ====================================================================
# From folder.py

class BaseFolder(Element):
    UNIQUE = ['name']
    
    def __init__(self,parent,tag,node=None,name='',description='',**kwargs):
        '''Create a folder'''
        super().__init__(parent,
                         tag,
                         node = node,
                         name = name,
                         desc = description,
                         **kwargs)

# --------------------------------------------------------------------
class GlobalPropertyFolder(BaseFolder):
    TAG = Element.FOLDER+'GlobalPropertySubFolder'
    def __init__(self,
                 parent,
                 node=None,
                 name='',
                 description=''):
        super().__init__(parent,
                         tag = self.TAG,
                         node = node,
                         name = name,
                         description = description)

registerElement(GlobalPropertyFolder)
    
# --------------------------------------------------------------------
class DeckFolder(BaseFolder):
    TAG = Element.FOLDER+'DeckSubFolder'
    def __init__(self,
                 parent,
                 node=None,
                 name='',
                 description=''):
        super().__init__(parent,
                         tag = self.TAG,
                         node = node,
                         name = name,
                         description = description)

registerElement(DeckFolder)
        
# --------------------------------------------------------------------
class MapFolder(BaseFolder):
    TAG = Element.FOLDER+'MapSubFolder'
    def __init__(self,
                 parent,
                 node=None,
                 name='',
                 description=''):
        super().__init__(parent,
                         tag = self.TAG,
                         node = node,
                         name = name,
                         description = description)
        
registerElement(MapFolder)

# --------------------------------------------------------------------
class ModuleFolder(BaseFolder):
    TAG = Element.FOLDER+'ModuleSubFolder'
    def __init__(self,
                 parent,
                 node=None,
                 name='',
                 description=''):
        super().__init__(parent,
                         tag = self.TAG,
                         node = node,
                         name = name,
                         description = description)
        
registerElement(ModuleFolder)

# --------------------------------------------------------------------
class PrototypeFolder(BaseFolder):
    TAG = Element.FOLDER+'PrototypeSubFolder'
    def __init__(self,
                 parent,
                 node=None,
                 name='',
                 description=''):
        super().__init__(parent,
                         tag = self.TAG,
                         node = node,
                         name = name,
                         description = description)
        
registerElement(PrototypeFolder)

# --------------------------------------------------------------------
#
# EOF
#

# ====================================================================
# From globalkey.py

# --------------------------------------------------------------------
class GlobalKey(ToolbarElement):
    SELECTED = 'MAP|false|MAP|||||0|0||true|Selected|true|EQUALS'
    UNIQUE = ['name']
    def __init__(self,
                 parent,
                 tag,
                 node                 = None,
                 name                 = '',                
                 icon                 = '',
                 tooltip              = '',
                 buttonHotkey         = '',
                 buttonText           = '',
                 canDisable           = False,
                 propertyGate         = '',
                 disabledIcon         = '',
                 # Local
                 hotkey               = '',
                 deckCount            = '-1',
                 filter               = '',
                 reportFormat         = '',
                 reportSingle         = False,
                 singleMap            = True,
                 target               = SELECTED):
        '''
        Parameters
        ----------
        - tag          The XML tag to use
        - parent       Parent node
        - node         Optionally existing node
        - name         Name of key
        - buttonHotkey Key in "global" scope
        - hotkey       Key to send to targeted pieces
        - buttonText   Text on button
        - canDisable   If true, disabled when propertyGate is true
        - deckCount    Number of decks (-1 is all)
        - filter       Which units to target
        - propertyGate When true, disable
        - reportFormat Chat message
        - reportSingle Also show single piece reports
        - singleMap    Only originating map if True
        - target       Preselection filter (default selected pieces)
        - tooltip      Hover-over message
        - icon         Image to use as icon

        Default targets are selected units
        '''
        
        super(GlobalKey,self).\
            __init__(parent,
                     tag,
                     node                 = node,
                     name                 = name,
                     icon                 = icon,
                     tooltip              = tooltip,
                     buttonHotkey         = buttonHotkey, # This hot key
                     buttonText           = buttonText,
                     canDisable           = canDisable,
                     propertyGate         = propertyGate,
                     disabledIcon         = disabledIcon,
                     hotkey               = hotkey,       # Target hot key
                     deckCount            = deckCount,
                     filter               = filter,
                     reportFormat         = reportFormat,
                     reportSingle         = reportSingle,
                     singleMap            = singleMap,
                     target               = target)
#
# EOF
# 
# ====================================================================
# From gameelements.py

# --------------------------------------------------------------------
class GameElementService:
    def getGame(self):
        return self.getParentOfClass(Game)

# --------------------------------------------------------------------
class GameElement(Element,GameElementService):
    def __init__(self,game,tag,node=None,**kwargs):
        super(GameElement,self).__init__(game,tag,node=node,**kwargs)

# --------------------------------------------------------------------
class Notes(ToolbarElement,GameElementService):
    TAG = Element.MODULE+'NotesWindow'
    UNIQUE = ['name']
    def __init__(self,elem,node=None,
                 name         = 'Notes', # Toolbar element name
                 tooltip      = 'Show notes window', # Tool tip
                 text         = '', # Button text
                 icon         = '/images/notes.gif', # Button icon,
                 hotkey       = key('N',ALT), # Named key or key stroke
                 canDisable   = False,
                 propertyGate = '',
                 disabledIcon = '',
                 description  = ''):
        super(Notes,self).__init__(elem,self.TAG,
                                   node         = node,
                                   name         = name,
                                   tooltip      = tooltip,
                                   text         = text,
                                   icon         = icon,
                                   hotkey       = hotkey,
                                   canDisable   = canDisable,
                                   propertyGate = propertyGate,
                                   disabledIcon = disabledIcon,
                                   description  = description)
    def encode(self):
        return ['NOTES\t\\','PNOTES']

registerElement(Notes)

# --------------------------------------------------------------------
class PredefinedSetup(GameElement):
    TAG = Element.MODULE+'PredefinedSetup'
    UNIQUE = ['name'] #,'file','useFile']
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
    UNIQUE = ['name']
    def __init__(self,elem,node=None,
                 name='',
                 initialValue = '',
                 description = ''):
        '''Translations

        Parameters
        ----------
        doc : Element
            Parent
        node : xml.dom.Element
            Node to read state from
        '''
        super(GlobalTranslatableMessages,self).\
            __init__(elem,self.TAG,node=node,
                     name = name,
                     initialValue = initialValue,
                     description = description)

registerElement(GlobalTranslatableMessages)
        
# --------------------------------------------------------------------
class Language(GameElement):
    TAG = 'VASSAL.i18n.Language'
    def __init__(self,elem,node=None,**kwargs):
        super(Language,self).__init__(elem,self.TAG,node=node,**kwargs)

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
#    <VASSAL.build.module.GlobalOptions
#      autoReport="Always"
#      centerOnMove="Use Preferences Setting"
#      chatterHTMLSupport="Always"
#      hotKeysOnClosedWindows="Always"
#      inventoryForAll="Never"
#      nonOwnerUnmaskable="Always"
#      playerIdFormat="$PlayerName$"
#      promptString="Opponents can unmask pieces"
#      sendToLocationMoveTrails="Always"
#      storeLeadingZeroIntegersAsStrings="true">
#        <option name="stepIcon">/images/StepForward16.gif</option>
#        <option name="stepHotKey">39,130</option>
#        <option name="undoIcon">/images/Undo16.gif</option>
#        <option name="undoHotKey">90,130</option>
#        <option name="serverControlsIcon">/images/connect.gif</option>
#        <option name="serverControlsHotKey">65,195</option>
#        <option name="debugControlsIcon"/>
#        <option name="debugControlsHotKey">68,195</option>
#    </VASSAL.build.module.GlobalOptions>
class GlobalOptions(GameElement):
    NEVER  = 'Never'
    ALWAYS = 'Always'
    PROMPT = 'Use Preferences Setting'
    TAG    = Element.MODULE+'GlobalOptions'
    def __init__(self,doc,node=None,
                 autoReport               = PROMPT,
                 centerOnMove             = PROMPT,
                 chatterHTMLSupport       = ALWAYS,
                 hotKeysOnClosedWindows   = NEVER,
                 inventoryForAll          = ALWAYS,
                 nonOwnerUnmaskable       = PROMPT,
                 playerIdFormat           = "$playerName$",
                 promptString             = "Opponents can unmask pieces",
                 sendToLocationMoveTrails = NEVER,
                 storeLeadingZeroIntegersAsStrings = False,
                 description                       = 'Global options',
                 dragThreshold                     = 10):
        '''Set global options on the module

        Parameters
        ----------
        doc : Element
            Parent
        node : xml.dom.Element
            Node to read state from
        
        autoReport                        : str='always'
        centerOnMove                      : str Option
        chatterHTMLSupport                : str='never'
        hotKeysOnClosedWindows            : str='never'
        inventoryForAll                   : str='always' 
        nonOwnerUnmaskable                : str='never'
        playerIdFormat                    : str='$PlayerName$'
        promptString                      : str=?
        sendToLocationMoveTrails          : bool=false
        storeLeadingZeroIntegersAsStrings : bool=False
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
                     sendToLocationMoveTrails = sendToLocationMoveTrails,
                     storeLeadingZeroIntegersAsStrings = storeLeadingZeroIntegersAsStrings,
                     dragThreshold            = dragThreshold,
                     description              = description)

    def addOption(self,**kwargs):
        '''Add a `Option` element to this

        Options known
        - newHotKey - key  - start new log
        - endHotKey - key  - end current log
        - stepIcon - image file name (/images/StepForward16.gif)
        - stepHotKey - key 
        - undoIcon - image file name (/images/Undo16.gif)
        - undoHotKey - key
        - serverControlsIcon - image file name (/images/connect.gif)
        - serverControlsHotKey - key
        - debugControlsIcon - image file name 
        - debugControlsHotKey - key 
        - scenarioPropertiesIcon - image file name
        - scenarioPropertiesHotKey - key

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
            - name : str
            - value : str
        
        Returns
        -------
        element : Option
            The added element
        '''
        return self.add(Option,**kwargs)
    def getOptions(self):
        return self.getElementsByKey(Option,'name')

    def addPreference(self,cls,**kwargs):
        return self.add(cls,**kwargs)

    def addIntPreference(self,**kwargs):
        return self.add(IntPreference,**kwargs)

    def addFloatPreference(self,**kwargs):
        return self.add(FloatPreference,**kwargs)
    
    def addBoolPreference(self,**kwargs):
        return self.add(BoolPreference,**kwargs)
    
    def addStrPreference(self,**kwargs):
        return self.add(StrPreference,**kwargs)
    
    def addTextPreference(self,**kwargs):
        return self.add(TextPreference,**kwargs)
    
    def addEnumPreference(self,**kwargs):
        return self.add(EnumPreference,**kwargs)
    
    def getIntPreferences(self):
        return self.getElementsByKey(IntPreference,'name')

    def getFloatPreferences(self):
        return self.getElementsByKey(FloatPreference,'name')

    def getBoolPreferences(self):
        return self.getElementsByKey(BoolPreference,'name')

    def getStrPreferences(self):
        return self.getElementsByKey(StrPreference,'name')

    def getTextPreferences(self):
        return self.getElementsByKey(TextPreference,'name')

    def getEnumPreferences(self):
        return self.getElementsByKey(EnumPreference,'name')

    def getPreferences(self):
        retd = {}
        for cls in [IntPreference,
                    FloatPreference,
                    BoolPreference,
                    StrPreference,
                    TextPreference,
                    EnumPreference]:
            retd.update(self.getElementsByKey(cls,'name'))

        return retd
    
registerElement(GlobalOptions)

# --------------------------------------------------------------------
class Option(Element):
    TAG = 'option'
    UNIQUE = ['name']
    def __init__(self,doc,node=None,name='',value=''):
        super(Option,self).__init__(doc,tag=self.TAG,node=node,name=name)
        self.addText(value)

    def getGlobalOptions(self):
        return self.getParent(GlobalOptions)

registerElement(Option)
    
# --------------------------------------------------------------------
class Preference(Element):
    PREFS = 'VASSAL.preferences.'
    UNIQUE = ['name','tab']
    def __init__(self,
                 doc,
                 tag,
                 node    = None,
                 name    = '',
                 default = '',
                 desc    = '',
                 tab     = '',
                 **kwargs):
        '''Add a preference

        Parameters
        ----------
        name : str
            Name of property
        default : str
            Default value
        desc : str
            Description
        tab : str
            Preference tab to put in to
        '''
        super(Preference,self).__init__(doc,
                                        tag     = tag,
                                        node    = node,
                                        name    = name,
                                        default = default,
                                        desc    = desc,
                                        tab     = tab)

    def getGlobalOptions(self):
        return self.getParent(GlobalOptions)
    
# --------------------------------------------------------------------
class IntPreference(Preference):
    TAG = Preference.PREFS+'IntegerPreference'
    def __init__(self,
                 doc,
                 node    = None,
                 name    = '',
                 default = 0,
                 desc    = '',
                 tab     = ''):
        super(IntPreference,self).__init__(doc,
                                           tag     = self.TAG,
                                           node    = node,
                                           name    = name,
                                           default = str(default),
                                           desc    = desc,
                                           tab     = tab)

registerElement(IntPreference)
    
# --------------------------------------------------------------------
class FloatPreference(Preference):
    TAG = Preference.PREFS+'DoublePreference'
    def __init__(self,
                 doc,
                 node    = None,
                 name    = '',
                 default = 0.,
                 desc    = '',
                 tab     = ''):
        super(FloatPreference,self).__init__(doc,
                                             tag     = self.TAG,
                                             node    = node,
                                             name    = name,
                                             default = str(default),
                                             desc    = desc,
                                             tab     = tab)

registerElement(FloatPreference)
    
# --------------------------------------------------------------------
class BoolPreference(Preference):
    TAG = Preference.PREFS+'BooleanPreference'
    def __init__(self,
                 doc,
                 node    = None,
                 name    = '',
                 default = False,
                 desc    = '',
                 tab     = ''):
        super(BoolPreference,self).__init__(doc,
                                            tag     = self.TAG,
                                            node    = node,
                                            name    = name,
                                            default = ('true' if default
                                                       else 'false'),
                                            desc    = desc,
                                            tab     = tab)

registerElement(BoolPreference)
    
# --------------------------------------------------------------------
class StrPreference(Preference):
    TAG = Preference.PREFS+'StringPreference'
    def __init__(self,
                 doc,
                 node    = None,
                 name    = '',
                 default = '',
                 desc    = '',
                 tab     = ''):
        super(StrPreference,self).__init__(doc,
                                           tag     = self.TAG,
                                           node    = node,
                                           name    = name,
                                           default = default,
                                           desc    = desc,
                                           tab     = tab)

registerElement(StrPreference)
    
# --------------------------------------------------------------------
class TextPreference(Preference):
    TAG = Preference.PREFS+'TextPreference'
    def __init__(self,
                 doc,
                 node    = None,
                 name    = '',
                 default = '',
                 desc    = '',
                 tab     = ''):
        super(TextPreference,self).__init__(doc,
                                            tag     = self.TAG,
                                            node    = node,
                                            name    = name,
                                            default = (default
                                                       .replace('\n','&#10;')),
                                            desc    = desc,
                                            tab     = tab)

registerElement(TextPreference)
    
# --------------------------------------------------------------------
class EnumPreference(Preference):
    TAG = Preference.PREFS+'EnumPreference'
    def __init__(self,
                 doc,
                 node    = None,
                 name    = '',
                 values  = [],
                 default = '',
                 desc    = '',
                 tab     = ''):
        ce = lambda v : str(v).replace(',',r'\,')
        sl = [ce(v) for v in values]
        df = ce(v)
        assert df in sl, \
            f'Default value "{default}" not in list {":".join(values)}'
        super(EnumPreference,self).__init__(doc,
                                            tag     = self.TAG,
                                            node    = node,
                                            name    = name,
                                            default = df,
                                            desc    = desc,
                                            tab     = tab,
                                            list    = sl)


registerElement(EnumPreference)
    
    
# --------------------------------------------------------------------
# CurrentMap == &quot;Board&quot;
class Inventory(ToolbarElement,GameElementService):
    TAG = Element.MODULE+'Inventory'
    ALPHA = 'alpha'
    LENGTH = 'length',
    NUMERIC = 'numeric'
    UNIQUE = ['name']
    def __init__(self,doc,node=None,
                 name                = '',
                 icon                = '/images/inventory.gif',
                 text                = '',
                 tooltip             = 'Show inventory of all pieces',
                 hotkey              = key('I',ALT),
                 canDisable          = False,
                 propertyGate        = '',
                 disabledIcon        = '',                 
                 centerOnPiece       = True,
                 drawPieces          = True,
                 foldersOnly         = False,
                 forwardKeystroke    = True,
                 groupBy             = '',
                 include             = '{}',
                 launchFunction      = 'functionHide',
                 leafFormat          = '$PieceName$',
                 nonLeafFormat       = '$PropertyValue$',
                 pieceZoom           = '0.33',
                 pieceZoom2          = '0.5',
                 pieceZoom3          = '0.6',
                 refreshHotkey       = key('I',ALT_SHIFT),
                 showMenu            = True,
                 sides               = '',
                 sortFormat          = '$PieceName$',
                 sortPieces          = True,
                 sorting             = ALPHA,
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
    def addFolder(self,**kwargs):
        '''Add a `ModuleFolder` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : ModuleFolder
            The added element
        '''
        return self.add(PrototypeFolder,**kwargs)
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
    def getFolders(self,asdict=True):
        '''Get all Menu element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Folder`
            elements.  If `False`, return a list of all `Folder`
            children.

        Returns
        -------
        children : dict or list
            Dictionary or list of `Folder` children

        '''
        return self.getElementsByKey(PrototypeFolder,'name',asdict)
        
registerElement(Prototypes)

# --------------------------------------------------------------------
class DiceButton(ToolbarElement,GameElementService):
    TAG=Element.MODULE+'DiceButton'
    UNIQUE = ['name']
    def __init__(self,elem,node=None,
                 name                 = '1d6',
                 tooltip              = 'Roll a 1d6',
                 text                 = '1d6',
                 icon                 = '/images/die.gif',
                 hotkey               = key('6',ALT),
                 canDisable           = False,
                 propertyGate         = '',
                 disabledIcon         = '',
                 addToTotal           = 0,
                 keepCount            = 1,
                 keepDice             = False,
                 keepOption           = '>',
                 lockAdd              = False,
                 lockDice             = False,
                 lockPlus             = False,
                 lockSides            = False,
                 nDice                = 1,
                 nSides               = 6,
                 plus                 = 0,
                 prompt               = False,
                 reportFormat         = '$name$ = $result$',
                 reportTotal          = False,
                 sortDice             = False):
        super(DiceButton,self).\
            __init__(elem,self.TAG,node=node,
                     addToTotal           = addToTotal,
                     canDisable           = canDisable,
                     disabledIcon         = disabledIcon,
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

# --------------------------------------------------------------------
class GameMassKey(GlobalKey,GameElementService):
    TAG = Element.MODULE+'GlobalKeyCommand'
    def __init__(self,map,node=None,
                 name                 = '',                
                 buttonText           = '',
                 tooltip              = '',
                 icon                 = '',
                 canDisable           = False,
                 propertyGate         = '',
                 disabledIcon         = '',
                 buttonHotkey         = '',
                 hotkey               = '',
                 deckCount            = '-1',
                 filter               = '',
                 reportFormat         = '',
                 reportSingle         = False,
                 singleMap            = True,
                 target               = GlobalKey.SELECTED):
        '''Default targets are selected units'''
        super(GameMassKey,self).\
            __init__(map,
                     self.TAG,
                     node                 = node,
                     name                 = name,                
                     buttonHotkey         = buttonHotkey, # This hot key
                     hotkey               = hotkey,       # Target hot key
                     buttonText           = buttonText,
                     canDisable           = canDisable,
                     deckCount            = deckCount,
                     filter               = filter,
                     propertyGate         = propertyGate,
                     reportFormat         = reportFormat,
                     reportSingle         = reportSingle,
                     singleMap            = singleMap,
                     target               = target,
                     tooltip              = tooltip,
                     icon                 = icon)
        
registerElement(GameMassKey)

# --------------------------------------------------------------------
class StartupMassKey(GlobalKey,GameElementService):
    TAG = Element.MODULE+'StartupGlobalKeyCommand'
    FIRST_LAUNCH = 'firstLaunchOfSession'
    EVERY_LAUNCH = 'everyLaunchOfSession'
    START_GAME   = 'startOfGameOnly'
    def __init__(self,
                 map,
                 node                 = None,
                 name                 = '',                
                 buttonHotkey         = '',
                 hotkey               = '',
                 buttonText           = '',
                 canDisable           = False,
                 deckCount            = '-1',
                 filter               = '',
                 propertyGate         = '',
                 reportFormat         = '',
                 reportSingle         = False,
                 singleMap            = True,
                 target               = GlobalKey.SELECTED,
                 tooltip              = '',
                 icon                 = '',
                 whenToApply          = EVERY_LAUNCH):
        '''Default targets are selected units'''
        super(StartupMassKey,self).\
            __init__(map,
                     self.TAG,
                     node                 = node,
                     name                 = name,                
                     buttonHotkey         = buttonHotkey, # This hot key
                     hotkey               = hotkey,       # Target hot key
                     buttonText           = buttonText,
                     canDisable           = canDisable,
                     deckCount            = deckCount,
                     filter               = filter,
                     propertyGate         = propertyGate,
                     reportFormat         = reportFormat,
                     reportSingle         = reportSingle,
                     singleMap            = singleMap,
                     target               = target,
                     tooltip              = tooltip,
                     icon                 = icon)
        if node is None:
            self['whenToApply'] = whenToApply

registerElement(StartupMassKey)

# --------------------------------------------------------------------
class Menu(GameElement):
    TAG = Element.MODULE+'ToolbarMenu'
    UNIQUE = ['name']
    def __init__(self,
                 game,
                 node                 = None,
                 name                 = '',
                 tooltip              = '',
                 text                 = '', # Menu name
                 canDisable           = False,
                 propertyGate         = '',
                 disabledIcon         = '',
                 description          = '',
                 hotkey               = '',
                 icon                 = '',
                 menuItems            = []):
        if len(description) <= 0 and len(tooltip) > 0:
            description = tooltip
        if len(tooltip) <= 0 and len(description) > 0:
            tooltip = description 
        super(Menu,self).\
            __init__(game,
                     self.TAG,
                     node                 = node,
                     name                 = name,
                     canDisable           = canDisable,
                     description          = description,
                     disabledIcon         = disabledIcon,
                     hotkey               = hotkey,
                     icon                 = icon,
                     menuItems            = ','.join(menuItems),
                     propertyGate         = propertyGate,
                     text                 = text,
                     tooltip              = tooltip)
                     
registerElement(Menu)

        
# --------------------------------------------------------------------
class SymbolicDice(GameElement):
    TAG = Element.MODULE+'SpecialDiceButton'
    UNIQUE = ['name']
    def __init__(self,
                 game,
                 node                    = None,
                 canDisable	         = False,
                 disabledIcon            = '',
                 hotkey                  = key('6',ALT),
                 name                    = "Dice",  # GP prefix
                 text                    = '', # Text on button
                 icon                    = '/images/die.gif', # Icon on button
                 format                  = '{name+": "+result1}', # Report 
                 tooltip                 = 'Die roll', # Help
                 propertyGate            = '', # Property to disable when T
                 resultButton            = False, # Result on button?
                 resultChatter           = True,  # Result in Chatter?
                 resultWindow            = False, # Result window?
                 backgroundColor	 = rgb(0xdd,0xdd,0xdd),  # Window background
                 windowTitleResultFormat = "$name$", # Window title
                 windowX                 = '67', # Window size
                 windowY                 = '65',
                 doHotkey                = False,
                 doLoop                  = False,
                 doReport                = False,
                 doSound                 = False,
                 hideWhenDisabled        = False,
                 hotkeys                 = '',
                 index                   = False,
                 indexProperty           = '',
                 indexStart              = 1,
                 indexStep               = 1,
                 loopCount               = 1,
                 loopType                = 'counted',
                 postLoopKey             = '',
                 reportFormat            = '',
                 soundClip               = '',
                 untilExpression         = '',
                 whileExpression         = ''
                 ):
        super(SymbolicDice,self).\
            __init__(game,
                     self.TAG,
                     node                    = node,
                     canDisable	             = canDisable,
                     disabledIcon            = disabledIcon,
                     hotkey                  = hotkey,
                     name                    = name,
                     text                    = text,
                     icon                    = icon,
                     format                  = format,
                     tooltip                 = tooltip,
                     propertyGate            = propertyGate,
                     resultButton            = resultButton,
                     resultChatter           = resultChatter,
                     resultWindow            = resultWindow,
                     backgroundColor	     = backgroundColor,
                     windowTitleResultFormat = windowTitleResultFormat,
                     windowX                 = windowX,
                     windowY                 = windowY,
                     doHotkey                = doHotkey,
                     doLoop                  = doLoop,
                     doReport                = doReport,
                     doSound                 = doSound,
                     hideWhenDisabled        = hideWhenDisabled,
                     hotkeys                 = hotkeys,
                     index                   = index,
                     indexProperty           = indexProperty,
                     indexStart              = indexStart,
                     indexStep               = indexStep,
                     loopCount               = loopCount,
                     loopType                = loopType,
                     postLoopKey             = postLoopKey,
                     reportFormat            = reportFormat,
                     soundClip               = soundClip,
                     untilExpression         = untilExpression,
                     whileExpression         = whileExpression)
        

    def addDie(self,**kwargs):
        return self.add(SpecialDie,**kwargs)

    def getSymbolicDice(self):
        return self.getParent(SymbolicDice)
        
registerElement(SymbolicDice)

        
# --------------------------------------------------------------------
class SpecialDie(GameElement):
    TAG = Element.MODULE+'SpecialDie'
    UNIQUE = ['name']
    def __init__(self,
                 symbolic,               # Symblic dice 
                 node                    = None,
                 name                    = '', # Name of dice (no GP)
                 report                  = '{name+": "+result}',
                 faces                   = None):
        super(SpecialDie,self).\
            __init__(symbolic,
                     self.TAG,
                     node = node,
                     name = name,
                     report = report)
        if node is not None or faces is None:
            return
        if isinstance(faces,list):
            faces = {i+1: f for i,f in enumerate(faces)}
        for v,f in faces:
            self.addFace(text = str(v), value = v, icon = f)

    def addFace(self,**kwargs):
        self.add(DieFace,**kwargs)

    def getSymbolicDice(self):
        return self.getParent(SymbolicDice)

    def getFaces(self):
        return self.getAllElements(DieFace,single=False)
        
registerElement(SpecialDie)
                     
# --------------------------------------------------------------------
class DieFace(GameElement):
    TAG = Element.MODULE+'SpecialDieFace'
    # Is this OK? Multiple faces can have the same icon, text and value 
    UNIQUE = ['icon','text','value']
    def __init__(self,
                 special,               # Special dice
                 node,                  # existing node
                 icon      = '',        # graphical representation
                 text      = '',        # Text representation
                 value     = 0):        # Value representation
        super(DieFace,self).\
            __init__(special,
                     self.TAG,
                     node      = node,
                     icon      = icon,
                     text      = text,
                     value     = value)
                     
    def getSpecialDie(self):
        return self.getParent(SpecialDie)

    # -- This one is tricky! --
    # def __hash__(self):
    #     return super().__hash__()+getSpecialDie()

registerElement(DieFace)

# --------------------------------------------------------------------
class ImageDefinitions(GameElement):
    #TAG = Element.MODULE+'gamepieceimage.GamePieceImageDefinitions'
    TAG = Element.MODULE+'gamepieceimage.GamePieceImageDefinitions'
    def __init__(self,
                 game,
                 node,
                 **kwargs):
        super().__init__(game,self.TAG,node=node,**kwargs)

registerElement(ImageDefinitions)

# --------------------------------------------------------------------
class LayoutsContainer(GameElement):
    #TAG = Element.MODULE+'gamepieceimage.GamePieceLayoutsContainer'
    TAG = Element.MODULE+'gamepieceimage.GamePieceLayoutsContainer'
    def __init__(self,
                 game,
                 node,
                 **kwargs):
        super().__init__(game,self.TAG,node=node,**kwargs)

registerElement(LayoutsContainer)

# --------------------------------------------------------------------
class ColorManager(GameElement):
    #TAG = Element.MODULE+'gamepieceimage.ColorManager'
    TAG = Element.MODULE+'gamepieceimage.ColorManager'
    def __init__(self,
                 game,
                 node,
                 **kwargs):
        super().__init__(game,self.TAG,node=node,**kwargs)

registerElement(ColorManager)

# --------------------------------------------------------------------
class FontManager(GameElement):
    #TAG = Element.MODULE+'gamepieceimage.FontManager'
    TAG = Element.MODULE+'gamepieceimage.FontManager'
    def __init__(self,
                 game,
                 node,
                 **kwargs):
        super().__init__(game,self.TAG,node=node,**kwargs)

registerElement(FontManager)

# --------------------------------------------------------------------
class FontStyle(GameElement):
    #TAG = Element.MODULE+'gamepieceimage.FontStyle'
    TAG = Element.MODULE+'gamepieceimage.FontStyle'
    def __init__(self,
                 game,
                 node,
                 **kwargs):
        super().__init__(game,self.TAG,node=node,**kwargs)

registerElement(FontStyle)

# --------------------------------------------------------------------
class MultiActionButton(GameElement):
    TAG = Element.MODULE+'MultiActionButton'
    def __init__(self,
                 game,
                 node,
                 description  = '',    # Reminder
                 text         = '',    # Text on button
                 tooltip      = '',    # Button tooltip 
                 icon         = '',    # Image on button
                 hotkey       = '',    # Key-stroke or command
                 canDisable   = False, # Can it be disabled
                 propertyGate = '',    # Disable when propety true
                 disabledIcon = '',    # image when disabled
                 menuItems    = []):   # Button texts
        '''
        <VASSAL.build.module.MultiActionButton
          canDisable="false"
          description="Menu"
          disabledIcon="" hideWhenDisabled="false"
          hotkey="67,130"
          icon="C.png"
          menuItems="Attacked,Defended" 
          propertyGate=""
          text=""
          tooltip="Clear combat status flags."
        />
        '''
        super().__init__(game,
                         self.TAG,
                         node    = node,
                         description  = description,
                         text         = text,
                         tooltip      = tooltip,
                         icon         = icon,
                         hotkey       = hotkey,
                         canDisable   = canDisable,
                         propertyGate = propertyGate,
                         disabledIcon = disabledIcon,
                         menuItems    = ','.join(menuItems))
                         
registerElement(MultiActionButton)

#
# EOF
#
# ====================================================================
# From mapelements.py

# --------------------------------------------------------------------
class MapElementService:
    def getMap(self):
        '''Get map - either a Map or WidgetMap'''
        return self.getParentOfClass([WidgetMap,Map])
        # if self._parent is None:
        #     return None
        # 
        # if 'WidgetMap' in self._parent.tagName:
        #     return self.getParent(WidgetMap)
        #     
        # return self.getParent(Map)
    def getGame(self):
        m = self.getMap()
        if m is not None: return m.getGame()
        return None

# --------------------------------------------------------------------
class MapElement(Element,MapElementService):
    def __init__(self,map,tag,node=None,**kwargs):
        super(MapElement,self).__init__(map,tag,node=node,**kwargs)


# --------------------------------------------------------------------
class PieceLayers(MapElement):
    TAG=Element.MAP+'LayeredPieceCollection'
    UNIQUE = ['property']
    def __init__(self,map,node=None,
                 property = 'PieceLayer',
                 description = '',
                 layerOrder = []):
        super(PieceLayers,self).__init__(map,self.TAG,node=node,
                                         property    = property,
                                         description = description,
                                         layerOrder  = ','.join(layerOrder))

    def addControl(self,**kwargs):
        '''Add `LayerControl` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : LayerControl
            The added element
        '''
        return self.add(LayerControl,**kwargs)
    def getControls(self,asdict=True):
        '''Get all `LayerControl` element(s) from this

        Parameters
        ----------
        asdict : bool        
            If `True`, return a dictonary that maps name to
            `LayerControl` elements.  If `False`, return a list of all
            `LayerControl` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `LayerControl` children

        '''
        return self.getElementsByKey(LayerControl,'name',asdict)
                 
registerElement(PieceLayers)
    
# --------------------------------------------------------------------
class LayerControl(MapElement):
    TAG=Element.MAP+'LayerControl'
    CYCLE_UP='Rotate Layer Order Up'
    CYCLE_DOWN='Rotate Layer Order Down'
    ENABLE='Make Layer Active'
    DISABLE='Make Layer Inactive'
    TOGGLE='Switch Layer between Active and Inactive'
    RESET='Reset All Layers'
    UNIQUE = ['name']
    def __init__(self,col,node=None,
                 name         = '',
                 tooltip      = '',
                 text         = '',
                 hotkey       = '',
                 icon         = '',
                 canDisable   = False,
                 propertyGate = '', #Property name, disable when property false
                 disabledIcon = '',
                 command      = TOGGLE,
                 skip         = False,
                 layers       = [],
                 description = ''):
        super(LayerControl,self).__init__(col,self.TAG,node=node,
                                          name         = name,
                                          tooltip      = tooltip,
                                          text         = text,
                                          buttonText   = text,
                                          hotkey       = hotkey,
                                          icon         = icon,
                                          canDisable   = canDisable,
                                          propertyGate = propertyGate,
                                          disabledIcon = disabledIcon,
                                          command      = command,
                                          skip         = skip,
                                          layers       = ','.join(layers),
                                          description  = description)

    def getLayers(self):
        '''Get map - either a Map or WidgetMap'''
        return self.getParentOfClass([PieceLayers])
        
registerElement(LayerControl)
        

# --------------------------------------------------------------------
class LineOfSight(MapElement):
    TAG=Element.MAP+'LOS_Thread'
    ROUND_UP        = 'Up'
    ROUND_DOWN      = 'Down'
    ROUND_NEAREST   = 'Nearest whole number'
    FROM_LOCATION   = 'FromLocation'
    TO_LOCATION     = 'ToLocation'
    CHECK_COUNT     = 'NumberOfLocationsChecked'
    CHECK_LIST      = 'AllLocationsChecked'
    RANGE           = 'Range'
    NEVER           = 'Never'
    ALWAYS          = 'Always'
    WHEN_PERSISTENT = 'When persistent'
    CTRL_CLICK      = 'Cltr-Click & Drag'    
    UNIQUE          = ['threadName']
    
    def __init__(self,map,
                 node=None,
                 threadName         = 'LOS',
                 hotkey             = key('L',ALT),
                 tooltip            = 'Trace line of sight',
                 iconName           = '/images/thread.gif', #'los-icon.png',
                 label              = '',
                 snapLOS            = False,
                 snapStart          = True,
                 snapEnd            = True,
                 report             = (f'{{"Range from "+{FROM_LOCATION}'
                                       f'+" to "+{TO_LOCATION}+" is "'
                                       f'+{RANGE}+" (via "+{CHECK_LIST}+")"}}'),
                 persistent         = CTRL_CLICK,
                 persistentIconName = '/images/thread.gif',
                 globl              = ALWAYS,
                 losThickness       = 3,
                 threadColor        = rgb(255,0,0),
                 drawRange          = True,
                 # rangeBg            = rgb(255,255,255),
                 # rangeFg            = rgb(0,0,0),
                 rangeScale         = 0,
                 hideCounters       = True,
                 hideOpacity        = 50,
                 round              = ROUND_UP,
                 canDisable         = False,
                 propertyGate       = '',
                 disabledIcon       = ''):
        '''Make Line of Sight interface
        
        Parameters
        ----------
        threadName : str
            Name of interface
        hotkey : str
            Start LOS key
        tooltip : str
            Tool tip text
        iconName : str
            Path to button icon
        label : str
            Button text 
        snapLOS : bool
            Wether to snap both ends
        snapStart : bool
            Snap to start
        snapEnd: bool
            Snap to end
        report : str
            Report format
        persistent : str
            When persistent
        persistentIconName : str
            Icon when persistent(?)
        globl : str
            Visisble to opponents
        losThickness : int
            Thickness in pixels
        losColor : str
            Colour of line
        drawRange : bool
            Draw the range next to LOST thread
        rangeBg : str
            Range backgroung colour
        rangeFg : str
            Range foregrond colour
        rangeScale : int
            Scale of range - pixels per unit
        round : str
            How to round range
        hideCounters :bool
            If true, hide counters while making thread
        hideOpacity : int
            Opacity of hidden counters (percent)
        canDisable : bool
            IF true, then can be hidden
        propertyGate : str
            Name of property.  When that property is TRUE, then the
            interface is disabled.  Must be a property name, not an expression.
        disabledIcon : str
            Icon to use when disabled
        '''
        super(LineOfSight,self).__init__(map,self.TAG,
                                         node = node,
                                         threadName         = threadName,
                                         hotkey             = hotkey,
                                         tooltip            = tooltip,
                                         iconName           = iconName,
                                         label              = label,
                                         snapLOS            = snapLOS,
                                         snapStart          = snapStart,
                                         snapEnd            = snapEnd,
                                         report             = report,
                                         persistent         = persistent,
                                         persistentIconName = persistentIconName,
                                         losThickness       = losThickness,
                                         threadColor        = threadColor,
                                         drawRange          = drawRange,
                                         #rangeBg            = rangeBg,
                                         #rangeFg            = rangeFg,
                                         rangeScale         = rangeScale,
                                         hideCounters       = hideCounters,
                                         hideOpacity        = hideOpacity,
                                         round              = round,
                                         canDisable         = canDisable,
                                         propertyGate       = propertyGate,
                                         disabledIcon       = disabledIcon)
        self.setAttribute('global',globl)
                                     
    
registerElement(LineOfSight)
    
# --------------------------------------------------------------------
class StackMetrics(MapElement):
    TAG=Element.MAP+'StackMetrics'
    def __init__(self,map,node=None,
                 bottom               = key('(',0),
                 down                 = key('%',0),
                 top                  = key('&',0),
                 up                   = key("'",0),
                 disabled             = False,
                 exSepX               = 6,   # Expanded (after double click)
                 exSepY               = 18,  # Expanded (after double click)
                 unexSepX             = 8,   # Compact
                 unexSepY             = 16): # Compact
        super(StackMetrics,self).__init__(map,self.TAG,node=node,
                                          bottom               = bottom,
                                          disabled             = disabled,
                                          down                 = down,
                                          exSepX               = exSepX,
                                          exSepY               = exSepY,
                                          top                  = top,
                                          unexSepX             = unexSepX,
                                          unexSepY             = unexSepY,
                                          up                   = up)

registerElement(StackMetrics)

# --------------------------------------------------------------------
class ImageSaver(MapElement):
    TAG=Element.MAP+'ImageSaver'
    def __init__(self,map,node=None,
                 buttonText           = '',
                 canDisable           = False,
                 hotkey               = '',
                 icon                 = '/images/camera.gif',
                 propertyGate         = '',
                 tooltip              = 'Save map as PNG image'):
        super(ImageSaver,self).__init__(map,self.TAG,node=node,
                                        buttonText           = buttonText,
                                        canDisable           = canDisable,
                                        hotkey               = hotkey,
                                        icon                 = icon,
                                        propertyGate         = propertyGate,
                                        tooltip              = tooltip)

registerElement(ImageSaver)

# --------------------------------------------------------------------
class TextSaver(MapElement):
    TAG=Element.MAP+'TextSaver'
    def __init__(self,map,node=None,
                 buttonText           = '',
                 canDisable           = False,
                 hotkey               = '',
                 icon                 = '/images/camera.gif',
                 propertyGate         = '',
                 tooltip              = 'Save map as text'):
        super(TextSaver,self).__init__(map,self.TAG,node=node,
                                        buttonText           = buttonText,
                                        canDisable           = canDisable,
                                        hotkey               = hotkey,
                                        icon                 = icon,
                                        propertyGate         = propertyGate,
                                        tooltip              = tooltip)

registerElement(TextSaver)

# --------------------------------------------------------------------
class ForwardToChatter(MapElement):
    TAG=Element.MAP+'ForwardToChatter'
    def __init__(self,map,node=None,**kwargs):
        super(ForwardToChatter,self).__init__(map,self.TAG,node=node,**kwargs)

registerElement(ForwardToChatter)

# --------------------------------------------------------------------
class MenuDisplayer(MapElement):
    TAG=Element.MAP+'MenuDisplayer'
    def __init__(self,map,node=None,**kwargs):
        super(MenuDisplayer,self).__init__(map,self.TAG,node=node,**kwargs)

registerElement(MenuDisplayer)

# --------------------------------------------------------------------
class MapCenterer(MapElement):
    TAG=Element.MAP+'MapCenterer'
    def __init__(self,map,node=None,**kwargs):
        super(MapCenterer,self).__init__(map,self.TAG,node=node,**kwargs)

registerElement(MapCenterer)

# --------------------------------------------------------------------
class StackExpander(MapElement):
    TAG=Element.MAP+'StackExpander'
    def __init__(self,map,node=None,**kwargs):
        super(StackExpander,self).__init__(map,self.TAG,node=node,**kwargs)

registerElement(StackExpander)

# --------------------------------------------------------------------
class PieceMover(MapElement):
    TAG=Element.MAP+'PieceMover'
    def __init__(self,map,node=None,**kwargs):
        super(PieceMover,self).__init__(map,self.TAG,node=node,**kwargs)

registerElement(PieceMover)

# --------------------------------------------------------------------
class SelectionHighlighters(MapElement):
    TAG=Element.MAP+'SelectionHighlighters'
    def __init__(self,map,node=None,**kwargs):
        super(SelectionHighlighters,self).\
            __init__(map,self.TAG,node=node,**kwargs)

registerElement(SelectionHighlighters)

# --------------------------------------------------------------------
class KeyBufferer(MapElement):
    TAG=Element.MAP+'KeyBufferer'
    def __init__(self,map,node=None,**kwargs):
        super(KeyBufferer,self).__init__(map,self.TAG,node=node,**kwargs)

registerElement(KeyBufferer)

# --------------------------------------------------------------------
class HighlightLastMoved(MapElement):
    TAG=Element.MAP+'HighlightLastMoved'
    def __init__(self,map,node=None,
                 color     = rgb(255,0,0),
                 enabled   = True,
                 thickness = 2):
        super(HighlightLastMoved,self).__init__(map,self.TAG,node=node,
                                                color     = color,
                                                enabled   = enabled,
                                                thickness = thickness)

registerElement(HighlightLastMoved)

# --------------------------------------------------------------------
class CounterDetailViewer(MapElement):
    TAG=Element.MAP+'CounterDetailViewer'
    TOP_LAYER  = 'from top-most layer only'
    ALL_LAYERS = 'from all layers'
    INC_LAYERS = 'from listed layers only'
    EXC_LAYERS = 'from layers other than those listed'
    FILTER     = 'by using a property filter'
    ALWAYS     = 'always'
    NEVER      = 'never'
    IF_ONE     = 'ifOne'
    UNIQUE     = ['description']
    def __init__(self,map,node=None,
                 borderWidth            = 0, # Horizontal padding between pieces
                 borderThickness        = 2, # Outer border thickness
                 borderInnerThickness   = 2, # Inner borders thickness
                 borderColor            = None,
                 centerAll              = False,
                 centerText             = False,
                 centerPiecesVertically = True,
                 combineCounterSummary  = False,
                 counterReportFormat    = '',
                 delay                  = 700,
                 description            = '',
                 display                = TOP_LAYER,
                 emptyHexReportForma    = '$LocationName$',
                 enableHTML             = True,
                 extraTextPadding       = 0,
                 bgColor                = None,
                 fgColor                = rgb(0,0,0),
                 fontSize               = 11,
                 graphicsZoom           = 1.0,# Zoom on counters
                 hotkey                 = key('\n'),
                 layerList              = [],
                 minDisplayPieces       = 2,
                 propertyFilter         = '',
                 showDeck               = False,
                 showDeckDepth          = 1,
                 showDeckMasked         = False,
                 showMoveSelected       = False,
                 showNoStack            = False,
                 showNonMovable         = False,
                 showOverlap            = False,
                 showgraph              = True,
                 showgraphsingle        = False,
                 showtext               = True,
                 showtextsingle         = False,
                 stretchWidthSummary    = False,
                 summaryReportFormat    = '$LocationName$',
                 unrotatePieces         = False,
                 version                = 4,
                 verticalOffset         = 2,
                 verticalTopText        = 0,
                 zoomlevel              = 1.0,
                 stopAfterShowing       = False,
                 showTerrainBeneath     = NEVER,
                 showTerrainSnappy      = True,
                 showTerrainWidth       = 120,
                 showTerrainHeight      = 120,
                 showTerrainZoom        = None,
                 showTerrainText        = ''
                 ): # showTerrain attributes

        bg = '' if bgColor is None else bgColor
        fg = '' if fgColor is None else fgColor
        bc = '' if borderColor is None else borderColor
        ll = ','.join(layerList)
        showTerrainZoom = zoomlevel if showTerrainZoom == None else showTerrainZoom
        super(CounterDetailViewer,self)\
            .__init__(map,self.TAG,node=node,
                      borderWidth            = borderWidth,
                      borderThickness        = borderThickness,
                      borderInnerThickness   = borderInnerThickness,
                      borderColor            = bc,
                      centerAll              = centerAll,
                      centerText             = centerText,
                      centerPiecesVertically = centerPiecesVertically,
                      combineCounterSummary = combineCounterSummary,
                      counterReportFormat   = counterReportFormat,
                      delay                 = delay,
                      description           = description,
                      display               = display, # How to show from layers
                      emptyHexReportForma   = emptyHexReportForma,
                      enableHTML            = enableHTML,
                      extraTextPadding      = extraTextPadding,
                      bgColor               = bg,
                      fgColor               = fg,
                      fontSize              = fontSize,
                      graphicsZoom          = graphicsZoom, # pieces at zoom
                      hotkey                = hotkey,
                      layerList             = ll,
                      minDisplayPieces      = minDisplayPieces,
                      propertyFilter        = propertyFilter,
                      showDeck              = showDeck,
                      showDeckDepth         = showDeckDepth,
                      showDeckMasked        = showDeckMasked,
                      showMoveSelectde      = showMoveSelected,
                      showNoStack           = showNoStack,
                      showNonMovable        = showNonMovable,
                      showOverlap           = showOverlap,
                      showgraph             = showgraph,
                      showgraphsingle       = showgraphsingle,
                      showtext              = showtext,
                      showtextsingle        = showtextsingle,
                      stretchWidthSummary   = stretchWidthSummary,
                      summaryReportFormat   = summaryReportFormat,
                      unrotatePieces        = unrotatePieces,
                      version               = version,
                      verticalOffset        = verticalOffset,
                      verticalTopText       = verticalTopText,
                      zoomlevel             = zoomlevel,
                      stopAfterShowing      = stopAfterShowing,
                      showTerrainBeneath    = showTerrainBeneath,
                      showTerrainSnappy     = showTerrainSnappy,
                      showTerrainWidth      = showTerrainWidth,
                      showTerrainHeight     = showTerrainHeight,
                      showTerrainZoom       = showTerrainZoom,
                      showTerrainText       = showTerrainText)

registerElement(CounterDetailViewer)

# --------------------------------------------------------------------
class GlobalMap(MapElement):
    TAG=Element.MAP+'GlobalMap'
    def __init__(self,map,node=None,
                 buttonText           = '',
                 color                = rgb(255,0,0),
                 hotkey               = key('O',CTRL_SHIFT),
                 icon                 = '/images/overview.gif',
                 scale                = 0.2,
                 tooltip              = 'Show/Hide overview window'):
        super(GlobalMap,self).\
            __init__(map,self.TAG,node=node,
                     buttonText           = buttonText,
                     color                = color,
                     hotkey               = hotkey,
                     icon                 = icon,
                     scale                = scale,
                     tooltip              = 'Show/Hide overview window')

registerElement(GlobalMap)

# --------------------------------------------------------------------
class Zoomer(MapElement):
    TAG = Element.MAP+'Zoomer'
    def __init__(self,map,node=None,
                 inButtonText         = '',
                 inIconName           = '/images/zoomIn.gif',
                 inTooltip            = 'Zoom in',
                 outButtonText        = '',
                 outIconName          = '/images/zoomOut.gif',
                 outTooltip           = 'Zoom out',
                 pickButtonText       = '',
                 pickIconName         = '/images/zoom.png',
                 pickTooltip          = 'Select Zoom',
                 zoomInKey            = key('=',CTRL_SHIFT),
                 zoomLevels           = [0.2,0.25,0.333,0.4,0.5,
                                         0.555,0.625,0.75,1.0,1.25,1.6],
                 zoomOutKey           = key('-'),
                 zoomPickKey          = key('='),
                 zoomStart            = 3):

        '''Zoom start is counting from the back (with default zoom levels,
        and zoom start, the default zoom is 1'''
        lvls = ','.join([str(z) for z in zoomLevels])
        super(Zoomer,self).\
            __init__(map,self.TAG,node=node,
                     inButtonText         = inButtonText,
                     inIconName           = inIconName,
                     inTooltip            = inTooltip,
                     outButtonText        = outButtonText,
                     outIconName          = outIconName,
                     outTooltip           = outTooltip,
                     pickButtonText       = pickButtonText,
                     pickIconName         = pickIconName,
                     pickTooltip          = pickTooltip,
                     zoomInKey            = zoomInKey,
                     zoomLevels           = lvls,
                     zoomOutKey           = zoomOutKey,
                     zoomPickKey          = zoomPickKey,
                     zoomStart            = zoomStart)

registerElement(Zoomer)

# --------------------------------------------------------------------
class HidePiecesButton(MapElement):
    TAG=Element.MAP+'HidePiecesButton'
    def __init__(self,map,node=None,
                 buttonText           = '',
                 hiddenIcon           = '/images/globe_selected.gif',
                 hotkey               = key('O'),
                 showingIcon          = '/images/globe_unselected.gif',
                 tooltip              = 'Hide all pieces on this map'):
        super(HidePiecesButton,self).\
            __init__(map,self.TAG,node=node,
                     buttonText           = buttonText,
                     hiddenIcon           = hiddenIcon,
                     hotkey               = hotkey,
                     showingIcon          = showingIcon,
                     tooltip              = tooltip)
        
registerElement(HidePiecesButton)

# --------------------------------------------------------------------
class MassKey(GlobalKey,MapElementService):
    TAG = Element.MAP+'MassKeyCommand'
    UNIQUE     = ['name']
    def __init__(self,map,node=None,
                 name                 = '',                
                 buttonHotkey         = '',
                 hotkey               = '',
                 buttonText           = '',
                 canDisable           = False,
                 deckCount            = '-1',
                 filter               = '',
                 propertyGate         = '',
                 reportFormat         = '',
                 reportSingle         = False,
                 singleMap            = True,
                 target               = GlobalKey.SELECTED,
                 tooltip              = '',
                 icon                 = ''):
        '''Default targets are selected units'''
        super(MassKey,self).\
            __init__(map,self.TAG,node=node,
                     name                 = name,                
                     buttonHotkey         = buttonHotkey, # This hot key
                     hotkey               = hotkey,       # Target hot key
                     buttonText           = buttonText,
                     canDisable           = canDisable,
                     deckCount            = deckCount,
                     filter               = filter,
                     propertyGate         = propertyGate,
                     reportFormat         = reportFormat,
                     reportSingle         = reportSingle,
                     singleMap            = singleMap,
                     target               = target,
                     tooltip              = tooltip,
                     icon                 = icon)

registerElement(MassKey)

# --------------------------------------------------------------------
class Flare(MapElement):
    TAG=Element.MAP+'Flare'
    def __init__(self,map,node=None,
                 circleColor          = rgb(255,0,0),
                 circleScale          = True,
                 circleSize           = 100,
                 flareKey             = 'keyAlt',
                 flareName            = 'Map Flare',
                 flarePulses          = 6,
                 flarePulsesPerSec    = 3,
                 reportFormat         = ''):
        super(Flare,self).__init__(map,self.TAG,node=node,
                                   circleColor          = circleColor,
                                   circleScale          = circleScale,
                                   circleSize           = circleSize,
                                   flareKey             = flareKey,
                                   flareName            = flareName,
                                   flarePulses          = flarePulses,
                                   flarePulsesPerSec    = flarePulsesPerSec,
                                   reportFormat         = '')

registerElement(Flare)

# --------------------------------------------------------------------
class Deck(MapElement):
    TAG = Element.MODULE+'map.DrawPile'
    ALWAYS     = 'Always'
    NEVER      = 'Never',
    VIA_MOUSE2 = 'Via right-click Menu'
    UNIQUE     = ['name','owningBoard']
    def __init__(self,map,
                 node                  = None,
                 name                  = 'deckName',
                 owningBoard           = '',
                 x                     = 0,   # int
                 y                     = 0,   # int
                 width                 = 200, # int
                 height                = 200, # int
                 #
                 allowMultiple         = False,
                 drawMultipleMessage   = 'Draw multiple cards',
                 #
                 allowSelect           = False,
                 drawSpecificMessage   = 'Draw specific cards',
                 selectDisplayProperty = '$BasicName$',
                 selectSortProperty    = 'BasicName',
                 #
                 faceDown              = ALWAYS,#ALWAYS,VIA_MOUSE2
                 faceFlipHotkey        = key('F'),
                 faceDownFormat        = '',
                 faceDownHotkey        = '',
                 faceDownMessage       = 'Face down',
                 faceUpHotkey          = '',
                 faceUpMessage         = 'Face up',
                 faceUpReportFormat    = '',
                 drawFaceUp            = False,
                 #
                 shuffle               = VIA_MOUSE2,#ALWAYS,NEVER
                 shuffleCommand        = 'Shuffle',
                 shuffleFormat         = '$playerSide$ shuffles $deckName$',
                 shuffleHotkey         = key('S',ALT),
                 #
                 reversible            = False,
                 reverseCommand        = 'Reverse',
                 reverseFormat         = '',
                 reverseHotkey         = '',
                 #
                 draw                  = True,
                 color                 = rgb(255,51,51),
                 hotkeyOnEmpty         = False,
                 emptyHotkey           = key(NONE,0)+',DeckEmpty',
                 #
                 reshufflable          = False,
                 reshuffleCommand      = '',
                 reshuffleHotkey       = '',
                 reshuffleMessage      = '',
                 reshuffleTarget       = '',
                 #
                 canSave               = False,
                 saveHotkey            = '',
                 saveMessage           = 'Save Deck',
                 saveReportFormat      = 'Deck Saved',
                 loadHotkey            = '',
                 loadMessage           = 'Load Deck',
                 loadReportFormat      = 'Deck Loaded',
                 #
                 maxStack              = 15,
                 #
                 expressionCounting    = False,
                 countExpressions      = '',
                 #
                 restrictExpression    = '',
                 restrictOption        = False,
                 #
                 deckOwners            = '',
                 deckRestrictAccess    = False
                 ): # int
        pass
        super(Deck,self).\
            __init__(map,self.TAG,node=node,
                     name                  = name,
                     owningBoard           = owningBoard,
                     x                     = int(x),      # int
                     y                     = int(y),      # int
                     width                 = int(width),  # int
                     height                = int(height), # int
                     #
                     allowMultiple         = allowMultiple,
                     drawMultipleMessage   = drawMultipleMessage,
                     #
                     allowSelect           = allowSelect,
                     drawSpecificMessage   = drawSpecificMessage,
                     selectDisplayProperty = selectDisplayProperty,
                     selectSortProperty    = selectSortProperty,
                     #
                     faceDown              = faceDown,
                     faceFlipHotkey        = faceFlipHotkey,
                     faceDownFormat        = faceDownFormat,
                     faceDownHotkey        = faceDownHotkey,
                     faceDownMessage       = faceDownMessage,
                     faceUpHotkey          = faceUpHotkey,
                     faceUpMessage         = faceUpMessage,
                     faceUpReportFormat    = faceUpReportFormat,
                     drawFaceUp            = drawFaceUp,
                     #
                     shuffle               = shuffle,
                     shuffleCommand        = shuffleCommand,
                     shuffleFormat         = shuffleFormat,
                     shuffleHotkey         = shuffleHotkey,
                     #
                     reversible            = reversible,
                     reverseCommand        = reverseCommand,
                     reverseFormat         = reverseFormat,
                     reverseHotkey         = reverseHotkey,
                     #
                     draw                  = draw,
                     color                 = color,
                     hotkeyOnEmpty         = hotkeyOnEmpty,
                     emptyHotkey           = emptyHotkey,
                     #
                     reshufflable          = reshufflable,
                     reshuffleCommand      = reshuffleCommand,
                     reshuffleHotkey       = reshuffleHotkey,
                     reshuffleMessage      = reshuffleMessage,
                     reshuffleTarget       = reshuffleTarget,
                     #
                     canSave               = canSave,
                     saveHotkey            = saveHotkey,
                     saveMessage           = saveMessage,
                     saveReportFormat      = saveReportFormat,
                     loadHotkey            = loadHotkey,
                     loadMessage           = loadMessage,
                     loadReportFormat      = loadReportFormat,
                     #
                     maxStack              = maxStack,
                     #
                     expressionCounting    = expressionCounting,
                     countExpressions      = countExpressions,
                     #
                     restrictExpression    = restrictExpression,
                     restrictOption        = restrictOption,
                     #
                     deckOwners            = deckOwners,
                     deckRestrictAccess    = deckRestrictAccess
                     )

    def addCard(self,**kwargs):
        '''Add a `Card` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Card
            The added element
        '''
        if not isinstance(card,CardSlot):
            print(f'Trying to add {type(card)} to Deck')
            return None
            
        p = card.clone(self)
        # self._node.appendChild(p._node)
        return p
    def addFolder(self,**kwargs):
        '''Add a `ModuleFolder` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : ModuleFolder
            The added element
        '''
        return self.add(DeckFolder,**kwargs)
        
    def getCards(self,asdict=True):
        '''Get all Card element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Card`
            elements.  If `False`, return a list of all Card`
            children.

        Returns
        -------
        children : dict or list
            Dictionary or list of `Card` children

        '''
        return self.getElementsByKey(CardSlot,'entryName',asdict)
    def getFolders(self,asdict=True):
        '''Get all Menu element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Folder`
            elements.  If `False`, return a list of all `Folder`
            children.

        Returns
        -------
        children : dict or list
            Dictionary or list of `Folder` children

        '''
        return self.getElementsByKey(DeckFolder,'name',asdict)

    
registerElement(Deck)
        
                 
# --------------------------------------------------------------------
class AtStart(MapElement):
    TAG = Element.MODULE+'map.SetupStack'
    UNIQUE     = ['name','location','owningBoard']
    def __init__(self,map,
                 node            = None,
                 name            = '',
                 location        = '',
                 useGridLocation = True,
                 owningBoard     = '',
                 x               = 0,
                 y               = 0):
        '''Pieces are existing PieceSlot elements


        Parameters
        ----------
        node : xml.minidom.Node
            Existing node or None
        name : str
            Name of node
        location : str
            Where the at-start element is put if `useGridLocation`
        useGridLocation : bool
            If true, use maps grid
        owningBoard : str
            Board that owns the at-start (can be empty)
        x : float
            Coordinate (ignored if `useGridLocation`)
        y : float
            Coordinate (ignored if `useGridLocation`)
        '''
        super(AtStart,self).\
            __init__(map,self.TAG,node=node,
                     name            = name,
                     location        = location,
                     owningBoard     = owningBoard,
                     useGridLocation = useGridLocation,
                     x               = x,
                     y               = y)

    def addPieces(self,*pieces):
        '''Add a `Pieces` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Pieces
            The added element
        '''
        # copy pieces here
        copies = []
        for p in pieces:
            c = self.addPiece(p)
            if c is not None:
                copies.append(c)
        return copies
        
    def addPiece(self,piece):
        '''Add a `Piece` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Piece
            The added element
        '''
        if not isinstance(piece,WithTraitsSlot):
            # Next is a bit of a hack - not nice
            if piece.__class__.__name__ not in ['PieceSlot','CardSlot']:
                print(f'Trying to add {type(piece)} to AtStart, '
                      f'not a {isinstance(piece,WithTraitsSlot)}')
                return None
            
        p = piece.clone(self)
        # self._node.appendChild(p._node)
        return p
    
    def getPieces(self,asdict=True):
        '''Get all Piece element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Piece`
            elements.  If `False`, return a list of all Piece`
            children.

        Returns
        -------
        children : dict or list
            Dictionary or list of `Piece` children

        '''
        return self.getElementsByKey(PieceSlot,'entryName',asdict)

registerElement(AtStart)

# --------------------------------------------------------------------
class ForwardKeys(MapElement):
    TAG = Element.MODULE+'map.ForwardToKeyBuffer'
    def __init__(self,map,
                 node            = None):
        '''Forward keys to key buffer from where it is distributed to
        selected pieces.  Don't know how I missed this!

        ''' 
        
        super(ForwardKeys,self).\
            __init__(map,self.TAG,node=node)

registerElement(ForwardKeys)

# --------------------------------------------------------------------
class Scroller(MapElement):
    TAG = Element.MODULE+'map.Scroller'
    ALWAYS = 'always'
    NEVER  = 'never'
    PROMPT = 'prompt'
    def __init__(self,map,
                 node           = None,
                 useArrows      = PROMPT):
        '''This component listens to key events on a Map window and
        scrolls the map.  Depending on the useArrows attribute, will
        use number keypad or arrow keys, or will offer a preferences
        setting for the user to choose
        ''' 
        
        super(Scroller,self).\
            __init__(map,self.TAG,node=node,
                     useArrows = useArrows)

registerElement(Scroller)

#
# EOF
#
# ====================================================================
# From globalproperty.py

# --------------------------------------------------------------------
class GlobalProperties(Element):
    TAG = Element.MODULE+'properties.GlobalProperties'
    def __init__(self,elem,node=None,**named):
        super(GlobalProperties,self).__init__(elem,self.TAG,node=node)
        
        for n, p in named:
            self.addProperty(n, **p)

    def getGame(self):
        return self.getParent(Game)
    def addProperty(self,**kwargs):
        '''Add a `Property` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Property
            The added element
        '''
        return GlobalProperty(self,node=None,**kwargs)
    def addFolder(self,**kwargs):
        '''Add a `ModuleFolder` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : ModuleFolder
            The added element
        '''
        return self.add(GlobalPropertyFolder,**kwargs)
    
    def getProperties(self):
        return getElementsByKey(GlobalProperty,'name')

    def addScenarioTab(self,**kwargs):
        '''Add a scenario property tab

        Parameters
        -----------
        kwargs : dict
            Key-value pairs to send to ScenarioOptionsTab

        Returns
        -------
        element : ScenarioOptionsTab
            Added element
        '''
        return ScenarioOptionsTab(self,node=None,**kwargs)

    def getScenarioTabs(self):
        return getElementsByKey(ScenarioOptionsTab,'name')
    def getFolders(self,asdict=True):
        '''Get all Menu element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Folder`
            elements.  If `False`, return a list of all `Folder`
            children.

        Returns
        -------
        children : dict or list
            Dictionary or list of `Folder` children

        '''
        return self.getElementsByKey(GlobalPropertyFolder,'name',asdict)
    
registerElement(GlobalProperties)

# --------------------------------------------------------------------
class GlobalProperty(Element):
    TAG = Element.MODULE+'properties.GlobalProperty'
    UNIQUE = ['name']
    def __init__(self,
                 elem,
                 node         = None,
                 name         = '',
                 initialValue = '',
                 isNumeric    = False,
                 min          = "null",
                 max          = "null",
                 wrap         = False,
                 description  = ""):
        super(GlobalProperty,self).__init__(elem,self.TAG,
                                            node         = node,
                                            name         = name,
                                            initialValue = initialValue,
                                            isNumeric    = isNumeric,
                                            min          = min,
                                            max          = max,
                                            wrap         = wrap,
                                            description  = description)

    def getGlobalProperties(self):
        return self.getParent(GlobalProperties)

registerElement(GlobalProperty)

# ====================================================================
class ScenarioOptionsTab(Element):
    TAG = Element.MODULE+'properties.ScenarioPropertiesOptionTab'
    LEFT = 'left'
    RIGHT = 'right'
    UNIQUE = ['name']
    
    def __init__(self,elem,node=None,
                 name         = 'Options',
                 description  = 'Scenario options',
                 heading      = '',
                 leftAlign    = 'left',
                 reportFormat = ('!$PlayerId$ changed Scenario Option '
                                 '[$tabName$] $propertyPrompt$ from '
                                '$oldValue$ to $newValue$')):
        super(ScenarioOptionsTab,self).__init__(elem,
                                                self.TAG,
                                                node         = node,
                                                name         = name,
                                                description  = description,
                                                heading      = heading,
                                                leftAlign    = leftAlign,
                                                reportFormat = reportFormat)

    def addList(self,**kwargs):
        '''Add a list property option

        Parameters
        ----------
        kwargs : dict
            Key, value pairs to initalise ScenarioOptionList

        Returns
        -------
        element : ScenarioOption
            The added element
        '''
        return ScenarioOptionList(self,node=None,**kwargs)

    def addBoolean(self,**kwargs):
        '''Add a list property option

        Parameters
        ----------
        kwargs : dict
            Key, value pairs to initalise ScenarioOptionBool

        Returns
        -------
        element : ScenarioOption
            The added element
        '''
        return ScenarioOptionBool(self,node=None,**kwargs)

    def addString(self,**kwargs):
        '''Add a list property option

        Parameters
        ----------
        kwargs : dict
            Key, value pairs to initalise ScenarioOptionString

        Returns
        -------
        element : ScenarioOption
            The added element
        '''
        return ScenarioOptionString(self,node=None,**kwargs)

    def addNumber(self,**kwargs):
        '''Add a list property option

        Parameters
        ----------
        kwargs : dict
            Key, value pairs to initalise ScenarioOptionNumber

        Returns
        -------
        element : ScenarioOption
            The added element
        '''
        return ScenarioOptionString(self,node=None,**kwargs)

    def getOptions(self):
        return self.getElementsByKey(ScenarioOption,'name')

    def getListOptions(self):
        return self.getElementsByKey(ScenarioOptionList,'name')

    def getBoolOptions(self):
        return self.getElementsByKey(ScenarioOptionBool,'name')

    def getStringOptions(self):
        return self.getElementsByKey(ScenarioOptionString,'name')
    
    def getNumberOptions(self):
        return self.getElementsByKey(ScenarioOptionNumber,'name')
    
    def getGlobalProperties(self):
        return self.getParent(GlobalProperties)

registerElement(ScenarioOptionsTab)
    
# --------------------------------------------------------------------
class ScenarioOption(Element):
    UNIQUE = ['name']

    def __init__(self,
                 tab, 
                 tag,
                 node         = None,
                 name         = '',
                 hotkey       = '',
                 description  = 'Set option value',
                 switch       = False,
                 initialValue = '',
                 **kwargs):
        '''
        Parameters
        ----------
        tab : ScenarioOptionsTab
            Tab to add to 
        tag : str
            Tag value (full)
        name : str
            Name of global property 
        hotkey : named-key
            Key stroke to send (global key)
        description : str
            Text to show user
        switch : bool
            If true, then prompt is put to the right
        initialValue : str
            Initial value
        kwargs : dict
            Other arguments
        '''
        super(ScenarioOption,self).__init__(tab,
                                            tag,
                                            node         = node,
                                            name         = name,
                                            hotkey       = hotkey,
                                            description  = description,
                                            switch       = switch,
                                            initialValue = initialValue,
                                            **kwargs)

    def getTab(self):
        return self.getParent(ScenarioOptionsTab)

# --------------------------------------------------------------------
class ScenarioOptionList(ScenarioOption):
    TAG = Element.MODULE+'properties.ListScenarioProperty'

    def __init__(self,
                 tab,
                 node         = None,
                 name         = '',
                 hotkey       = '',
                 description  = 'Set option value',
                 switch       = False,
                 initialValue = None,
                 options      = []):
        '''
        Parameters
        ----------
        tag : str
            Tag value (full)
        name : str
            Name of global property 
        hotkey : named-key
            Key stroke to send (global key)
        description : str
            Text to show user
        switch : bool
            If true, then prompt is put to the right
        initialValue : str
            Initial value.  If None, set to first option
        options : list 
            Possible values
        '''
        opts = ','.join([str(s) for s in options])
        if initialValue is None:
            initialValue = opts[0]
            
        super(ScenarioOptionList,self).__init__(tab,
                                                self.TAG,
                                                node         = node,
                                                name         = name,
                                                hotkey       = hotkey,
                                                description  = description,
                                                switch       = switch,
                                                initialValue = initialValue,
                                                options      = opts)

registerElement(ScenarioOptionList)

# --------------------------------------------------------------------
class ScenarioOptionBool(ScenarioOption):
    TAG = Element.MODULE+'properties.BooleanScenarioProperty'

    def __init__(self,
                 tab,
                 node         = None,
                 name         = '',
                 hotkey       = '',
                 description  = 'Set option value',
                 switch       = False,
                 initialValue = False):
        '''
        Parameters
        ----------
        tag : str
            Tag value (full)
        name : str
            Name of global property 
        hotkey : named-key
            Key stroke to send (global key)
        description : str
            Text to show user
        switch : bool
            If true, then prompt is put to the right
        initialValue : bool
            Initial value
        '''
        super(ScenarioOptionBool,self).__init__(tab,
                                                self.TAG,
                                                node         = node,
                                                name         = name,
                                                hotkey       = hotkey,
                                                description  = description,
                                                switch       = switch,
                                                initialValue = initialValue)
        
registerElement(ScenarioOptionBool)

# --------------------------------------------------------------------
class ScenarioOptionString(ScenarioOption):
    TAG = Element.MODULE+'properties.StringScenarioProperty'

    def __init__(self,
                 tab,
                 node         = None,
                 name         = '',
                 hotkey       = '',
                 description  = 'Set option value',
                 switch       = False,
                 initialValue = False):
        '''
        Parameters
        ----------
        tag : str
            Tag value (full)
        name : str
            Name of global property 
        hotkey : named-key
            Key stroke to send (global key)
        description : str
            Text to show user
        switch : bool
            If true, then prompt is put to the right
        initialValue : str
            Initial value
        '''
        super(ScenarioOptionString,self).__init__(tab,
                                                  self.TAG,
                                                  node         = node,
                                                  name         = name,
                                                  hotkey       = hotkey,
                                                  description  = description,
                                                  switch       = switch,
                                                  initialValue = initialValue)
        
registerElement(ScenarioOptionString)

# --------------------------------------------------------------------
class ScenarioOptionNumber(ScenarioOption):
    TAG = Element.MODULE+'properties.NumberScenarioProperty'

    def __init__(self,
                 tab,
                 node         = None,
                 name         = '',
                 hotkey       = '',
                 description  = 'Set option value',
                 switch       = False,
                 initialValue = False):
        '''
        Parameters
        ----------
        tag : str
            Tag value (full)
        name : str
            Name of global property 
        hotkey : named-key
            Key stroke to send (global key)
        description : str
            Text to show user
        switch : bool
            If true, then prompt is put to the right
        initialValue : str
            Initial value
        '''
        super(ScenarioOptionNumber,self).__init__(tab,
                                                  self.TAG,
                                                  node         = node,
                                                  name         = name,
                                                  hotkey       = hotkey,
                                                  description  = description,
                                                  switch       = switch,
                                                  initialValue = initialValue)

registerElement(ScenarioOptionNumber)

#
# EOF
#
# ====================================================================
# From turn.py

# --------------------------------------------------------------------
class TurnLevel(Element):
    UNIQUE = ['property']
    def __init__(self,elem,tag,node=None,**kwargs):
        super(TurnLevel,self).__init__(elem,tag,node=node,**kwargs)

    def addLevel(self,counter=None,phases=None):
        '''Add a `Level` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Level
            The added element
        '''
        if counter is None and phases is None:
            return self
        
        t = TurnCounter if counter is not None else TurnList
        o = counter     if counter is not None else phases

        subcounter = o.pop('counter',None)
        subphases  = o.pop('phases',None)

        s = t(self,node=None,**o)

        return s.addLevel(subcounter, subphases)

    def getUp(self):
        return self.getParent(TurnLevel)
    def addCounter(self,**kwargs):
        '''Add a `Counter` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Counter
            The added element
        '''
        return self.add(self,TurnCounter,**kwargs)
    def addList(self,**kwargs):
        '''Add a `List` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : List
            The added element
        '''
        return self.add(self,TurnList,**kwargs)
    def getCounter(self):
        return self.getAllElements(TurnCounter)
    def getList(self):
        return self.getAllElements(TurnList)

# --------------------------------------------------------------------
class TurnTrack(TurnLevel):
    TAG = Element.MODULE+'turn.TurnTracker'
    UNIQUE   = ['name']
    MAXIMUM  = 'Maximum'
    FIXED    = 'Fixed'
    VARIABLE = 'Variable'
    def __init__(self,elem,node=None,
                 name             = '',
                 buttonText       = 'Turn',
                 hotkey           = '',
                 icon             = '',
                 length           = -1,
                 lengthStyle      = MAXIMUM,
                 nexthotkey       = key('T',ALT),
                 plusButtonSize   = 22,
                 prevhotkey       = key('T',ALT_SHIFT),
                 reportFormat     = 'Turn updated from $oldTurn$ to $newTurn$',
                 turnButtonHeight = 22,
                 fwdOnly          = True,
                 turnFormat       = None,
                 counter          = None,
                 phases           = None):
        levels = (counter if counter is not None else
                  phases if phases is not None else None)
        if levels is not None:
            lvl = 1
            lvls = [f'$level{lvl}$']
            sub  = levels
            while True:
                sub = sub.get('counter',sub.get('phases',None))
                if sub is None:
                    break
                lvl += 1
                lvls.append(f'$level{lvl}$')
            
            turnFormat = ' '.join(lvls)
        
        if turnFormat is None:
            turnFormat = '$level1$ $level2$ $level3$ $level4$'        
        
        super(TurnTrack,self).__init__(elem, self.TAG,
                                       node             = node,
                                       name             = name,
                                       buttonText       = buttonText,
                                       hotkey           = hotkey,
                                       icon             = icon,
                                       length           = length,
                                       lengthStyle      = lengthStyle,
                                       nexthotkey       = nexthotkey,
                                       plusButtonSize   = plusButtonSize,
                                       prevhotkey       = prevhotkey,
                                       reportFormat     = reportFormat,
                                       turnButtonHeight = turnButtonHeight,
                                       turnFormat       = turnFormat)

        self.addLevel(counter=counter, phases=phases)

    def getGame(self):
        return self.getParent(Game)
    def getLists(self,asdict=True):
        '''Get all List element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `List`
            elements.  If `False`, return a list of all List`
            children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `List` children

        '''
        return self.getElementsByKey(TurnList,'property',asdict=asdict)
    def getCounters(self,asdict=True):
        '''Get all Counter element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Counter`
            elements.  If `False`, return a list of all Counter`
            children.

        Returns
        -------
        children : dict or list
            Dictionary or list of `Counter` children

        '''
        return self.getElementsByKey(TurnCounter,'property',asdict=asdict)
    def addHotkey(self,**kwargs):
        '''Add a `Hotkey` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Hotkey
            The added element
        '''
        return self.add(TurnGlobalHotkey,**kwargs)
    def getHotkeys(self,asdict=True):
        return self.getElementsByKey(TurnGlobalHotkey,'name',asdict=asdict)
    def encode(self):
        ret = f'TURN{self["name"]}\t'
        
        return []

registerElement(TurnTrack)

# --------------------------------------------------------------------
class TurnCounter(TurnLevel):
    TAG = Element.MODULE+"turn.CounterTurnLevel"
    def __init__(self,elem,node=None,
                 property      = '',
                 start         = 1,
                 incr          = 1,
                 loop          = False,
                 loopLimit     = -1,
                 turnFormat    = "$value$"):
        super(TurnCounter,self).__init__(elem,self.TAG,node=node,
                                         property       = property,
                                         start          = start,
                                         incr           = incr,
                                         loop           = loop,
                                         loopLimit      = loopLimit,
                                         turnFormat     = turnFormat)
                    
registerElement(TurnCounter)

# --------------------------------------------------------------------
class TurnList(TurnLevel):
    TAG = Element.MODULE+"turn.ListTurnLevel"
    def __init__(self,elem,node=None,
                 property      = '',
                 names         = [],
                 configFirst   = False,
                 configList    = False,
                 turnFormat    = '$value$'):
        super(TurnList,self).\
            __init__(elem,self.TAG,node=node,
                     property       = property,
                     list           = ','.join([str(p) for p in names]),
                     configFirst    = configFirst,
                     configList     = configList,
                     turnFormat     = turnFormat)
                  
registerElement(TurnList)

# --------------------------------------------------------------------
class TurnGlobalHotkey(Element):
    TAG = Element.MODULE+'turn.TurnGlobalHotkey'
    UNIQUE = ['name']
    def __init__(self,elem,
                 node         = None,
                 hotkey       = '',
                 match        = '{true}',
                 reportFormat = '',
                 name         = ''):
        '''Global key activated by turn change

        Parameters
        ----------
        doc : Element
            Parent
        node : xml.dom.Element
            Node to read state from
        hotkey : str
            What to send (global command)
        match : str
            When to send
        reportFormat : str
            What to what
        name : str
            A free form name
        '''
        super(TurnGlobalHotkey,self).__init__(elem,self.TAG,
                                              node         = node,
                                              hotkey       = hotkey,
                                              match        = match,
                                              reportFormat = reportFormat,
                                              name         = name)

    def getTurnTrack(self):
        '''Get the turn track'''
        return self.getParent(TurnTrack)

registerElement(TurnGlobalHotkey)

#
# EOF
#
# ====================================================================
# From documentation.py

# ====================================================================
def createKeyHelp(*args,**kwargs):
    '''Creates a help file with key-bindings

    See Documentation.createKeyHelp
    '''
    return Documentation.createKeyHelp(*args,**kwargs)

# --------------------------------------------------------------------
class Documentation(GameElement):
    TAG=Element.MODULE+'Documentation'
    def __init__(self,doc,node=None,**kwargs):
        '''Documentation (or help menu)

        Parameters
        ----------
        doc : Element
            Parent
        node : xml.dom.Element
            Node to read state from
        kwargs : dict
            Attributes
        '''
        super(Documentation,self).__init__(doc,self.TAG,node=node,**kwargs)

    def addAboutScreen(self,**kwargs):
        '''Add a `AboutScreen` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : AboutScreen
            The added element
        '''
        return self.add(AboutScreen,**kwargs)
    def addHelpFile(self,**kwargs):
        '''Add a `HelpFile` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : HelpFile
            The added element
        '''
        return self.add(HelpFile,**kwargs)
    def addBrowserHelpFile(self,**kwargs):
        '''Add a `BrowserHelpFile` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : BrowserHelpFile
            The added element
        '''
        return self.add(BrowserHelpFile,**kwargs)
    def addBrowserPDFFile(self,**kwargs):
        '''Add a `BrowserPDFFile` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : BrowserPDFFile
            The added element
        '''
        return self.add(BrowserPDFFile,**kwargs)
    def addTutorial(self,**kwargs):
        '''Add a `Tutorial` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Tutorial
            The added element
        '''
        return self.add(Tutorial,**kwargs)
    def getAboutScreens(self):
        return self.getElementsByKey(AboutScreen,'title')
    def getHelpFiles(self):
        return self.getElementsByKey(HelpFile,'title')
    def getBrowserHelpFiles(self):
        return self.getElementsByKey(BrowserHelpFile,'title')
    def getBrowserPDFFiles(self):
        return self.getElementsByKey(BrowserPDFFile,'title')
    def getTutorials(self):
        return self.getElementsByKey(Tutorial,'name')

    @classmethod
    def createKeyHelp(cls,keys,title='',version=''):
        '''Creates a help file with key-bindings
        
        Parameters
        ----------
        keys : list of list of str
             List of key-binding documentation
        title : str
             Title of help file
        version : str
             Version number
        
        Returns
        -------
        txt : str
            File content
        '''
        txt = f'''
        <html>
         <body>
          <h1>{title} (Version {version}) Key bindings</h1>
          <table>
          <tr><th>Key</th><th>Where</th><th>Effect</th></tr>'''
        
        for key, where, description in keys:
            txt += (f'<tr><td>{key}</td>'
                    f'<td>{where}</td>'
                    f'<td>{description}</td></tr>')
        
        txt += '''
          </table>
         </body>
        </html>'''
        
        return txt 

registerElement(Documentation)

# --------------------------------------------------------------------
class AboutScreen(Element):
    TAG = Element.MODULE+'documentation.AboutScreen'
    UNIQUE = ['title']
    def __init__(self,doc,node=None,title='',fileName=""):
        '''Create an about screen element that shows image

        Parameters
        ----------
        doc : Element
            Parent
        node : xml.dom.Element
            Node to read state from
        title : str
            Entry title
        fileName : str
            Internal file name        
        '''
        super(AboutScreen,self).__init__(doc,
                                         self.TAG,
                                         node     = node,
                                         fileName = fileName,
                                         title    = title)
    def getDocumentation(self):
        '''Get Parent element'''
        return self.getParent(Documentation)

registerElement(AboutScreen)

# --------------------------------------------------------------------
class BrowserPDFFile(Element):
    TAG = Element.MODULE+'documentation.BrowserPDFFile'
    UNIQUE = ['title','pdfFile']
    def __init__(self,doc,node=None,title='',pdfFile=''):
        '''Create help menu item that opens an embedded PDF
        
        Parameters
        ----------
        doc : Element
            Parent
        node : xml.dom.Element
            Node to read state from
        title : str
            Entry title
        pdfFile : str
            Internal file name
        '''
        super(BrowserPDFFile,self).__init__(doc,self.TAG,
                                            node    = node,
                                            pdfFile = pdfFile,
                                            title   = title)
    def getDocumentation(self):
        '''Get Parent element'''
        return self.getParent(Documentation)

registerElement(BrowserPDFFile)
    
# --------------------------------------------------------------------
class HelpFile(Element):
    TAG = Element.MODULE+'documentation.HelpFile'
    ARCHIVE = 'archive'
    UNIQUE = ['title','fileName']
    def __init__(self,doc,node=None,
                 title='',
                 fileName='',
                 fileType=ARCHIVE):
        '''Create a help menu entry that opens an embeddded file
        
        Parameters
        ----------
        doc : Element
            Parent
        node : xml.dom.Element
            Node to read state from
        title : str
            Entry title
        fileName : str
            Internal file name
        fileType : str
            How to find the file 
        '''
        super(HelpFile,self).__init__(doc,self.TAG,node=node,
                                      fileName = fileName,
                                      fileType = fileType,
                                      title    = title)

    def getDocumentation(self):
        '''Get Parent element'''
        return self.getParent(Documentation)

registerElement(HelpFile)
    
# --------------------------------------------------------------------
class BrowserHelpFile(Element):
    TAG = Element.MODULE+'documentation.BrowserHelpFile'
    UNIQUE = ['title','startingPage']
    def __init__(self,doc,node=None,
                 title='',
                 startingPage='index.html'):
        '''Create a help menu entry that opens an embeddded HTML
        page (with possible sub-pages) file
        
        Parameters
        ----------
        doc : Element
            Parent
        node : xml.dom.Element
            Node to read state from
        title : str
            Entry title
        startingPage : str
            which file to start at
        '''
        super(BrowserHelpFile,self).__init__(doc,self.TAG,node=node,
                                             startingPage=startingPage,
                                             title=title)

    def getDocumentation(self):
        '''Get Parent element'''
        return self.getParent(Documentation)

registerElement(BrowserHelpFile)
    
# --------------------------------------------------------------------
class Tutorial(Element):
    TAG = Element.MODULE+'documentation.Tutorial'
    UNIQUE = ['name','logfile']
    def __init__(self,doc,node=None,
                 name            = 'Tutorial',
                 logfile         = 'tutorial.vlog',
                 promptMessage   = 'Load the tutorial?',
                 welcomeMessage  = 'Press "Step forward" (PnDn) to step through the tutorial',
                 launchOnStartup = True):
        '''Add a help menu item that loads the tutorial

        Also adds the start-up option to run the tutorial


        Parameters
        ----------
        doc : Element
            Parent
        node : xml.dom.Element
            Node to read state from
        name : str
            Name of entry
        logfile : str
            Internal file name
        promptMessage : str
            What to show
        launchOnStartup : bool
            By default, launch tutorial first time running module
        '''
        super(Tutorial,self).__init__(doc,self.TAG,node=node,
                                      name            = name,
                                      logfile         = logfile,
                                      promptMessage   = promptMessage,
                                      welcomeMessage  = welcomeMessage,
                                      launchOnStartup = launchOnStartup)

    def getDocumentation(self):
        '''Get Parent element'''
        return self.getParent(Documentation)

registerElement(Tutorial)
    

#
# EOF
#
# ====================================================================
# From player.py

# --------------------------------------------------------------------
class PlayerRoster(GameElement):
    TAG = Element.MODULE+'PlayerRoster'
    def __init__(self,doc,node=None,buttonKeyStroke='',
               buttonText='Retire',
               buttonToolTip='Switch sides, become observer, or release faction'):
        '''Add a player roster to the module
        
        Parameters
        ----------
        doc : Element
            Parent
        node : xml.dom.Element
            Node to read state from
        buttonText : str
            Text on button
        buttonTooltip : str
            Tool tip to show when hovering over button
        '''
        super(PlayerRoster,self).__init__(doc,self.TAG,node=node,
                                          buttonKeyStroke = buttonKeyStroke,
                                          buttonText      = buttonText,
                                          buttonToolTip   = buttonToolTip)
    def addSide(self,name):
        '''Add a `Side` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Side
            The added element
        '''
        return self.add(PlayerSide,name=name)
    def getSides(self):
        '''Get all sides'''
        return self.getAllElements(PlayerSide,False)
    def encode(self):
        '''Encode for save'''
        return ['PLAYER\ta\ta\t<observer>']

registerElement(PlayerRoster)

# --------------------------------------------------------------------
class PlayerSide(Element):
    TAG = 'entry'
    UNIQUE = ['name']
    def __init__(self,doc,node=None,name=''):
        '''Adds a side to the player roster

        Parameters
        ----------
        doc : Element
            Parent
        node : xml.dom.Element
            Node to read state from
        name : str
            Name of side 
        '''
        super(PlayerSide,self).__init__(doc,self.TAG,node=node)
        if node is None:
            self.addText(name)

    def getPlayerRoster(self):
        '''Get Parent element'''
        return self.getParent(PlayerRoster)

registerElement(PlayerSide)


#
# EOF
#
# ====================================================================
# From chessclock.py

# ====================================================================
class ChessClock(Element):
    TAG=Element.MODULE+'chessclockcontrol.ChessClock'
    UNIQUE = ['side']
    def __init__(self,
                 doc,
                 node                   = None,
                 icon                   = '',
                 description            = '',
                 side                   = '',
                 tooltip                = 'Individual clock control',
                 buttonText             = '',
                 startHotkey            = '',
                 stopHotkey             = '',
                 tickingBackgroundColor = rgb(255,255,0),
                 tickingFontColor       = rgb(0,0,0),
                 tockingFontColor       = rgb(51,51,51)):
        '''Individual clock for a side

        When the clock is running, the background colour may be
        changed, and the colour of the numbers alternate between
        `tickingFontColor` and `tockingFontColor`.
        
        Parameters
        ----------
        doc : Element
            Parent element 
        node : xml.dom.Element 
            Read from this node
        icon : str
            File name of button icon
        description : str
            Note on this clock
        side : str
            Name of side this clock belongs to
        tooltop : str
            Hover help text
        buttonText : str
            Text on button
        startHotkey : str (key code)
            Key or command to start timer
        stopHotkey : str (key code)
            Key or command to stop timer
        tickingBackgroundColor : str (color)
            Background color of time display when clock is running
        tickingFontColor : str (color)
            First color of numbers in display when clock is running.
        tockingFontColor : str (color)
            Second color of numbers in display when clock is running.
        '''
        super(ChessClock,self).__init__(#ChessClock
                 doc,
                 self.TAG,
                 node                   = node,
                 icon                   = icon,
                 description            = description,
                 side                   = side,
                 tooltip                = tooltip,
                 buttonText             = buttonText,
                 startHotkey            = startHotkey,
                 stopHotkey             = stopHotkey,
                 tickingBackgroundColor = tickingBackgroundColor,
                 tickingFontColor       = tickingFontColor,
                 tockingFontColor       = tockingFontColor)
            
    def getControl(self):
        '''Get Parent element'''
        return self.getParent(ChessClockControl)

registerElement(ChessClock)

# ====================================================================
class ChessClockControl(GameElement):
    TAG=Element.MODULE+'ChessClockControl'
    ALWAYS = 'Always'
    AUTO   = 'Auto'
    NEVER  = 'Never'
    UNIQUE = ['name']
    def __init__(self,
                 doc,
                 node              = None,
                 name              = 'Chess clock',
                 description       = '',
                 buttonIcon        = 'chess_clock.png',
                 buttonText        = '',
                 buttonTooltip     = 'Show/stop/hide chess clocks',
                 showHotkey        = key('U',ALT),
                 pauseHotkey       = key('U',CTRL_SHIFT),
                 nextHotkey        = key('U'),
                 startOpponentKey  = '',
                 showTenths        = AUTO,
                 showSeconds       = AUTO,
                 showHours         = AUTO,
                 showDays          = AUTO,
                 allowReset        = False,
                 addClocks         = True):
        '''A set of chess clocs

        Parameters
        ----------
        doc : Element
            Parent
        node : xml.dom.Element
            Node to read state from
        name : str
            Name of clock control
        description : str
            Note on the chess clocks control
        buttonIcon : str
            Icon file name for button (chess_clock.png)
        buttonText : str
            Text on button 
        buttonTooltip : str
            Hower help
        showHotkey : str (key code)
            Show or hide interface hot key
        nextHotkey : str (key code)
            Start the next clock hot key
        pauseHotkey : str (key code)
            Pause all clocks hot key 
        startOpponentKey : str (key code)
            Start opponens clock 
        showTenths : one of AUTO, ALWAYS, NEVER
            Whether to show tenths of seconds
        showSeconds : one of AUTO, ALWAYS, NEVER
            Whether to show seconds in clock 
        showHours : one of AUTO, ALWAYS, NEVER
            Whether to show hours in clock
        showDays : one of AUTO, ALWAYS, NEVER
            Whether to show days in clock
        allowReset : boolean
            If true, allow manual reset of all clocks
        '''
        super(ChessClockControl,self).__init__(# ChessclockControl
            doc,
            self.TAG,
            node              = node,
            name              = name,
            description       = description,
            buttonIcon        = buttonIcon,
            buttonText        = buttonText,
            buttonTooltip     = buttonTooltip,
            showHotkey        = showHotkey,
            pauseHotkey       = pauseHotkey,
            nextHotkey        = nextHotkey,
            startOpponentKey  = startOpponentKey,
            showTenths        = showTenths,
            showSeconds       = showSeconds,
            showHours         = showHours,
            showDays          = showDays,
            allowReset        = allowReset)
        print(node,addClocks)
        if node is not None or not addClocks:
            return
        
        print('--- Will add clocks')
        game   = self.getGame()
        roster = game.getPlayerRoster()[0]
        sides  = roster.getSides()
        for side in sides:
            name = side.getText()
            self.addClock(side        = name,
                          tooltip     = f'Clock for {name}',
                          buttonText  = name,
                          startHotkey = key('U'),
                          stopHotkey  = key('U'))
    
    def addClock(self,**kwargs):
        '''Add a clock element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : AboutScreen
            The added element
        '''
        return self.add(ChessClock,**kwargs)
    def getClocks(self,asdict=True):
        '''Return dictionary of clocs'''
        return self.getElementsByKey(ChessClock,'side',asdict)

registerElement(ChessClockControl)

#
# EOF
#
# ====================================================================
# From widget.py

# --------------------------------------------------------------------
class WidgetElement:
    UNIQUE = ['entryName']
    def __init__(self):
        pass

    def addTabs(self,**kwargs):
        '''Add a `Tabs` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Tabs
            The added element
        '''
        return self.add(TabWidget,**kwargs)
    def addCombo(self,**kwargs):
        '''Add a drop-down menu to this

        Parameters
        ----------
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Combo
            The added element
        '''
        return self.add(ComboWidget,**kwargs)
    def addPanel(self,**kwargs):
        '''Add a `Panel` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Panel
            The added element
        '''
        return self.add(PanelWidget,**kwargs)
    def addList(self,**kwargs):
        '''Add a `List` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : List
            The added element
        '''
        return self.add(ListWidget,**kwargs)
    def addMapWidget(self,**kwargs):
        '''Add a `MapWidget` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : MapWidget
            The added element
        '''
        return self.add(MapWidget,**kwargs)
    def addChart(self,**kwargs):
        '''Add a `Chart` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Chart
            The added element
        '''
        return self.add(Chart,**kwargs)
    def addPieceSlot(self,**kwargs):
        '''Add a `PieceSlot` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : PieceSlot
            The added element
        '''
        return self.add(PieceSlot,**kwargs)
    def addPiece(self,piece):
        '''Add a `Piece` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Piece
            The added element
        '''
        if not isinstance(piece,PieceSlot):
            print(f'Trying to add {type(piece)} to ListWidget')
            return None
            
        p = piece.clone(self)
        return p
    def getTabs(self,asdict=True):
        '''Get all Tab element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Tab` elements.  If `False`, return a list of all Tab` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `Tab` children
        '''
        return self.getElementsByKey(TabWidget,'entryName',asdict)
    def getCombos(self,asdict=True):
        '''Get all Combo element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Tab` elements.  If `False`, return a list of all Tab` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `Tab` children
        '''
        return self.getElementsByKey(ComboWidget,'entryName',asdict)
    def getLists(self,asdict=True):
        '''Get all List element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `List` elements.  If `False`, return a list of all List` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `List` children
        '''
        return self.getElementsByKey(ListWidget,'entryName',asdict)
    def getPanels(self,asdict=True):
        '''Get all Panel element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Panel` elements.  If `False`, return a list of all Panel` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `Panel` children
        '''
        return self.getElementsByKey(PanelWidget,'entryName',asdict)
    def getMapWidgets(self,asdict=True):
        '''Get all MapWidget element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `MapWidget` elements.  If `False`, return a list of all MapWidget` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `MapWidget` children
        '''
        return self.getElementsByKey(MapWidget,'entryName',asdict)
    def getCharts(self,asdict=True):
        '''Get all Chart element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Chart` elements.  If `False`, return a list of all Chart` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `Chart` children
        '''
        return self.getElementsByKey(Chart,'chartName',asdict)
    def getPieceSlots(self,asdict=True):
        '''Get all PieceSlot element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `PieceSlot` elements.  If `False`, return a list of all PieceSlot` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `PieceSlot` children
        '''
        return self.getElementsByKey(PieceSlot,'entryName',asdict)

# --------------------------------------------------------------------
class PieceWindow(GameElement,WidgetElement):
    TAG=Element.MODULE+'PieceWindow'
    UNIQUE = ['name']
    def __init__(self,elem,node=None,
                 name         = '',
                 defaultWidth = 0,
                 hidden       = False,
                 hotkey       = key('C',ALT),
                 scale        = 1.,
                 text         = '',
                 tooltip      = 'Show/hide piece window',
                 icon         = '/images/counter.gif'):
        super(PieceWindow,self).__init__(elem,self.TAG,node=node,
                                         name         = name,
                                         defaultWidth = defaultWidth,
                                         hidden       = hidden,
                                         hotkey       = hotkey,
                                         scale        = scale,
                                         text         = text,
                                         tooltip      = tooltip,
                                         icon         = icon)

registerElement(PieceWindow)

# --------------------------------------------------------------------
class ComboWidget(Element,WidgetElement):
    TAG=Element.WIDGET+'BoxWidget'
    def __init__(self,elem,node=None,entryName='',width=0,height=0):
        super(ComboWidget,self).__init__(elem,
                                       self.TAG,
                                       node = node,
                                       entryName = entryName,
                                       width     = width,
                                       height    = height)
        
registerElement(ComboWidget)

# --------------------------------------------------------------------
class TabWidget(Element,WidgetElement):
    TAG=Element.WIDGET+'TabWidget'
    def __init__(self,elem,node=None,entryName=''):
        super(TabWidget,self).__init__(elem,
                                       self.TAG,
                                       node      = node,
                                       entryName = entryName)

registerElement(TabWidget)

# --------------------------------------------------------------------
class ListWidget(Element,WidgetElement):
    TAG=Element.WIDGET+'ListWidget'
    def __init__(self,elem,node = None,
                 entryName = '',
                 height    = 0,
                 width     = 300,
                 scale     = 1.,
                 divider   = 150):
        super(ListWidget,self).__init__(elem,self.TAG,node=node,
                                        entryName = entryName,
                                        height    = height,
                                        width     = width,
                                        scale     = scale,
                                        divider   = divider)

registerElement(ListWidget)

# --------------------------------------------------------------------
class PanelWidget(Element,WidgetElement):
    TAG=Element.WIDGET+'PanelWidget'
    def __init__(self,elem,node=None,
                 entryName = '',
                 fixed     = False,
                 nColumns  = 1,
                 vert      = False):
        super(PanelWidget,self).__init__(elem,self.TAG,node=node,
                                         entryName = entryName,
                                         fixed     = fixed,
                                         nColumns  = nColumns,
                                         vert      = vert)

registerElement(PanelWidget)

# --------------------------------------------------------------------
class MapWidget(Element):
    TAG=Element.WIDGET+'MapWidget'
    def __init__(self,elem,node=None,entryName=''):
        super(MapWidget,self).__init__(elem,self.TAG,
                                       node      = node,
                                       entryName = entryName)

    def addWidgetMap(self,**kwargs):
        '''Add a `WidgetMap` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : WidgetMap
            The added element
        '''
        return self.add(WidgetMap,**kwargs)
    def getWidgetMaps(self,asdict=True):
        '''Get all WidgetMap element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `WidgetMap` elements.  If `False`, return a list of all WidgetMap` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `WidgetMap` children
        '''
        return self.getElementsByKey(WidgetMap,'mapName',asdict=asdict)
    
registerElement(MapWidget)

#
# EOF
#
# ====================================================================
# From grid.py

# --------------------------------------------------------------------
HEX_WIDTH = 88.50779626676963
HEX_HEIGHT = 102.2
RECT_WIDTH  = 80
RECT_HEIGHT = 80
# --------------------------------------------------------------------
class BaseGrid(Element):
    def __init__(self,zone,tag,node=None,
                 color        = rgb(0,0,0),
                 cornersLegal = False,
                 dotsVisible  = False,
                 dx           = HEX_WIDTH,  # Meaning seems reversed!
                 dy           = HEX_HEIGHT,
                 edgesLegal   = False,
                 sideways     = False,
                 snapTo       = True,
                 visible      = True,
                 x0           = 0,
                 y0           = 32):
        super(BaseGrid,self).__init__(zone,tag,node=node,
                                      color        = color,
                                      cornersLegal = cornersLegal,
                                      dotsVisible  = dotsVisible,
                                      dx           = dx,
                                      dy           = dy,
                                      edgesLegal   = edgesLegal,
                                      sideways     = sideways,
                                      snapTo       = snapTo,
                                      visible      = visible,
                                      x0           = x0,
                                      y0           = y0)
    def getZone(self):
        z = self.getParent(Zone)
        return z
    def getZonedGrid(self):
        z = self.getZone()
        if z is not None:
            return z.getZonedGrid()
        return None
    def getBoard(self):
        z = self.getZonedGrid()
        if z is not None:
            return z.getBoard()
        return self.getParent(Board)
    def getPicker(self):
        z = self.getBoard()
        if z is not None:
            return z.getPicker()
        return None
    def getMap(self):
        b = self.getPicker()
        if b is not None:
            return b.getMap()
        return None
    def getNumbering(self):
        pass 
    def getLocation(self,loc):
        numbering = self.getNumbering()
        if numbering is None or len(numbering) < 1:
            return None

        return numbering[0].getLocation(loc)
    
# --------------------------------------------------------------------
class BaseNumbering(Element):
    def __init__(self,grid,tag,node=None,
                 color                = rgb(255,0,0),
                 first                = 'H',
                 fontSize             = 24,
                 hDescend             = False,
                 hDrawOff             = 0,
                 hLeading             = 1,
                 hOff                 = 0,
                 hType                = 'A',
                 locationFormat       = '$gridLocation$',
                 rotateText           = 0,
                 sep                  = '',
                 stagger              = True,
                 vDescend             = False,
                 vDrawOff             = 32,
                 vLeading             = 0,
                 vOff                 = 0,
                 vType                = 'N',
                 visible              = True):
        super(BaseNumbering,self).__init__(grid,tag,node=node,
                                           color           = color,
                                           first           = first,
                                           fontSize        = fontSize,
                                           hDescend        = hDescend,
                                           hDrawOff        = hDrawOff,
                                           hLeading        = hLeading,
                                           hOff            = hOff,
                                           hType           = hType,
                                           locationFormat  = locationFormat,
                                           rotateText      = rotateText,
                                           sep             = sep,
                                           stagger         = stagger,
                                           vDescend        = vDescend,
                                           vDrawOff        = vDrawOff,
                                           vLeading        = vLeading,
                                           vOff            = vOff,
                                           vType           = vType,
                                           visible         = visible)
    def getGrid(self): return getParent(BaseGrid)

    def _getMatcher(self,tpe,leading):
        if tpe == 'A':
            return \
                '-?(?:A+|B+|C+|D+|E+|F+|G+|H+|I+|'  + \
                'J+|K+|L+|M+|N+|O+|P+|Q+|R+|S+|T+|' + \
                'U+|V+|W+|X+|Y+|Z+)'

        return f'-?[0-9]{{{int(leading)+1},}}'

    def _getIndex(self,name,tpe):
        if tpe == 'A':
            negative = name.startswith('-')
            if negative:
                name = name[1:]

            value = 0
            for num,let in enumerate(name):
                if not let.isupper():
                    continue
                if num < len(name) - 1:
                    value += 26
                else:
                    value += ord(let)-ord('A')

            if negative:
                value *= -1

            return value

        return int(name)

    def _getCenter(self,col,row):
        '''Convert col and row index to picture coordinates'''
        print('Dummy GetCenter')
        pass
    
    def getLocation(self,loc):
        '''Get picture coordinates from grid location'''
        from re import match

        first   = self['first']
        vType   = self['vType']
        hType   = self['hType']
        vOff    = int(self['vOff'])
        hOff    = int(self['hOff'])
        sep     = self['sep']
        colPat  = self._getMatcher(hType,self['hLeading'])
        rowPat  = self._getMatcher(vType,self['vLeading'])
        patts   = ((colPat,rowPat) if first == 'H' else (rowPat,colPat))
        colGrp  = 1 if first == 'H' else 2
        rowGrp  = 2 if first == 'H' else 1
        patt    = sep.join([f'({p})' for p in patts])
        matched = match(patt,loc)
        if not matched:
            return None

        rowStr  = matched[rowGrp]
        colStr  = matched[colGrp]
        rowNum  = self._getIndex(rowStr,vType)
        colNum  = self._getIndex(colStr,hType)

        ret = self._getCenter(colNum-hOff, rowNum-vOff);
        #print(f'Get location of "{loc}" -> {rowNum},{colNum} -> {ret}')
        return ret
       
    
# --------------------------------------------------------------------
class HexGrid(BaseGrid):
    TAG = Element.BOARD+'HexGrid'
    def __init__(self,zone,node=None,**kwargs):
        super(HexGrid,self).__init__(zone,self.TAG,node=node,**kwargs)

    def addNumbering(self,**kwargs):
        '''Add a `Numbering` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Numbering
            The added element
        '''
        return self.add(HexNumbering,**kwargs)
    def getNumbering(self):
        return self.getAllElements(HexNumbering)
    def getDeltaX(self):
        return float(self['dx'])
    def getDeltaY(self):
        return float(self['dy'])
    def getXOffset(self):
        return int(self['x0'])
    def getYOffset(self):
        return int(self['y0'])
    def getMaxRows(self):
        from math import floor
        height    = self.getZone().getHeight()
        return floor(height / self.getDeltaX() + .5)
    def getMaxCols(self):
        from math import floor
        width    = self.getZone().getWidth()
        return floor(width / self.getDeltaY()  + .5)

registerElement(HexGrid)

# --------------------------------------------------------------------
class SquareGrid(BaseGrid):
    TAG = Element.BOARD+'SquareGrid'
    def __init__(self,zone,node=None,
                 dx           = RECT_WIDTH,
                 dy           = RECT_HEIGHT,
                 edgesLegal   = False,
                 x0           = 0,
                 y0           = int(0.4*RECT_HEIGHT),
                 **kwargs):
        super(SquareGrid,self).__init__(zone,self.TAG,node=node,
                                        dx         = dx,
                                        dy         = dy,
                                        edgesLegal = edgesLegal,
                                        x0         = x0,
                                        y0         = y0,
                                        **kwargs)
    def addNumbering(self,**kwargs):
        '''Add a `Numbering` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Numbering
            The added element
        '''
        return self.add(SquareNumbering,**kwargs)
    def getNumbering(self):
        return self.getAllElements(SquareNumbering)
    def getDeltaX(self):
        return float(self['dx'])
    def getDeltaY(self):
        return float(self['dy'])
    def getXOffset(self):
        return int(self['x0'])
    def getYOffset(self):
        return int(self['y0'])
    def getMaxRows(self):
        from math import floor
        height    = self.getZone().getHeight()
        return floor(height / self.getDeltaY() + .5)
    def getMaxCols(self):
        from math import floor
        width    = self.getZone().getWidth()
        return floor(width / self.getDeltaX()  + .5)

registerElement(SquareGrid)

# --------------------------------------------------------------------
class HexNumbering(BaseNumbering):
    TAG = Element.BOARD+'mapgrid.HexGridNumbering'
    def __init__(self,grid,node=None,**kwargs):
        super(HexNumbering,self).__init__(grid,self.TAG,node=node,**kwargs)
        
    def getGrid(self):
        g = self.getParent(HexGrid)
        return g

    def _getCenter(self,col,row):
        '''Convert col and row index to picture coordinates'''
        from math import floor
        
        stagger  = self['stagger'] == 'true'
        sideways = self.getGrid()['sideways'] == 'true'
        hDesc    = self['hDescend'] == 'true'
        vDesc    = self['vDescend'] == 'true'
        xOff     = self.getGrid().getXOffset()
        yOff     = self.getGrid().getYOffset()
        hexW     = self.getGrid().getDeltaX()
        hexH     = self.getGrid().getDeltaY()
        zxOff    = self.getGrid().getZone().getXOffset()
        zyOff    = self.getGrid().getZone().getYOffset()
        maxRows  = self.getGrid().getMaxRows()
        maxCols  = self.getGrid().getMaxCols()
        # print(f'  Col:         {col}')
        # print(f'  Row:         {row}')
        # print(f'  Stagger:     {stagger}')
        # print(f'  Sideways:    {sideways}')
        # print(f'  hDesc:       {hDesc}')
        # print(f'  vDesc:       {vDesc}')
        # print(f'  maxRows:     {maxRows}')
        # print(f'  maxCols:     {maxCols}')

        # This code from HexGridNumbering.java
        if stagger:
            if sideways:
                if col % 2 != 0:
                    if hDesc:
                        row += 1
                    else:
                        row -= 1
            else:
                if col % 2 != 0:
                    if vDesc:
                        row += 1
                    else:
                        row -= 1

        if sideways:
            if vDesc:
                col = maxRows - col
            if hDesc:
                row = maxCols - row
        else:
            if hDesc:
                col = maxCols - col
            if vDesc:
                row = maxRows - row


        x = col * hexW + xOff
        if col % 2 == 0:
            y = row * hexH
        else:
            y = row * hexH + hexH / 2
        y += yOff

        # print(f'  Col:         {col}')
        # print(f'  Row:         {row}')
        # print(f'  hexW:        {hexW}')
        # print(f'  hexH:        {hexH}')
        # print(f'  xOff:        {xOff}')
        # print(f'  yOff:        {yOff}')
        # print(f'  x:           {x}')
        # print(f'  y:           {y}')
        
        if sideways:
            x, y = y, x

        return int(floor(x+.5)),int(floor(y+.5))
            
        # if sideways:
        #     maxRows, maxCols = maxCols, maxRows
        #     
        # if stagger:
        #     if sideways:
        #         if col % 2 != 0:
        #             row += 1 if hDesc else -1
        #     else:
        #         if col % 2 != 0:
        #             row += 1 if vDesc else -1
        # 
        # if hDesc:
        #     col = maxCols - col
        # if vDesc:
        #     row = maxRows - row
        # 
        # print(f'  Col:         {col}')
        # print(f'  Row:         {row}')
        # print(f'  hexW:        {hexW}')
        # print(f'  hexH:        {hexH}')
        # print(f'  xOff:        {xOff}')
        # print(f'  yOff:        {yOff}')
        # 
        # x = col * hexW + xOff
        # y = row * hexH + yOff + (hexH/2 if col % 2 != 0 else 0)
        # 
        # print(f'  Col:         {col}')
        # print(f'  Row:         {row}')
        # print(f'  hexW:        {hexW}')
        # print(f'  hexH:        {hexH}')
        # print(f'  xOff:        {xOff}')
        # print(f'  yOff:        {yOff}')
        # print(f'  x:           {x}')
        # print(f'  y:           {y}')
        # 
        # x = int(floor(x + .5))
        # y = int(floor(y + .5))
        # if sideways:
        #     # print(f'Swap coordinates because {sideways}')
        #     x, y = y, x
        # 
        # return x,y

registerElement(HexNumbering)

# --------------------------------------------------------------------
class SquareNumbering(BaseNumbering):
    TAG = Element.BOARD+'mapgrid.SquareGridNumbering'
    def __init__(self,grid,node=None,hType='N',**kwargs):
        super(SquareNumbering,self).__init__(grid,self.TAG,node=node,
                                             hType=hType,**kwargs)
    def getGrid(self):
        return self.getParent(SquareGrid)

    def getCenter(self,col,row):
        hDesc    = self['hDescend'] == 'true'
        vDesc    = self['vDescend'] == 'true'
        xOff     = self.getGrid().getXOffset()
        yOff     = self.getGrid().getYOffset()
        squareW  = self.getGrid().getDeltaX()
        squareH  = self.getGrid().getDeltaY()
        maxRows  = self.getGrid().getMaxRows()
        maxCols  = self.getGrid().getMaxCols()

        if vDesc:  row = maxRows - row
        if hDesc:  col = maxCols - col

        x = col * squareW + xOff
        y = row * squareH + yOff

        return x,y
        
registerElement(SquareNumbering)
    
# --------------------------------------------------------------------
class RegionGrid(Element):
    TAG = Element.BOARD+'RegionGrid'
    def __init__(self,zone,node=None,snapto=True,fontsize=9,visible=True):
        super(RegionGrid,self).__init__(zone,self.TAG,node=node,
                                        snapto   = snapto,
                                        fontsize = fontsize,
                                        visible  = visible)

    def getZone(self):
        return self.getParent(Zone)
    def getZoneGrid(self):
        z = self.getZone()
        if z is not None:
            return z.getBoard()
        return None
    def getBoard(self):
        z = self.getZonedGrid()
        if z is not None:
            return z.getBoard()
        return self.getParent(Board)
    def getMap(self):
        b = self.getBoard()
        if b is not None:
            return b.getMap()
        return None
    def getRegions(self):
        return self.getElementsByKey(Region,'name')    
    def checkName(self,name):
        '''Get unique name'''
        poss = len([e for e in self.getRegions()
                    if e == name or e.startswith(name+'_')])
        if poss == 0:
            return name

        return name + f'_{poss}'
    def addRegion(self,**kwargs):
        '''Add a `Region` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Region
            The added element
        '''
        return self.add(Region,**kwargs)
    def getLocation(self,loc):
        for r in self.getRegions().values():
            if loc == r['name']:
                return int(r['originx']),int(r['originy'])

        return None
        
registerElement(RegionGrid)

# --------------------------------------------------------------------
class Region(Element):
    TAG = Element.BOARD+'Region'
    UNIQUE = ['name']
    def __init__(self,grid,node=None,
                 name      = '',
                 originx   = 0,
                 originy   = 0,
                 alsoPiece = True,
                 piece     = None,
                 prefix    = ''):
        fullName = name + ("@"+prefix if len(prefix) else "")
        realName = grid.checkName(fullName) if node is None else fullName
        super(Region,self).__init__(grid,
                                    self.TAG,
                                    node    = node,
                                    name    = realName,
                                    originx = originx,
                                    originy = originy)

        if node is None and alsoPiece:
            m = self.getMap()
            b = self.getBoard()
            if m is not None and b is not None:
                if piece is None:
                    g      = m.getGame()
                    pieces = g.getSpecificPieces(name,asdict=False)
                    piece  = pieces[0] if len(pieces) > 0 else None
             
                if piece is not None:
                    # bname = m['mapName']
                    bname = b['name']
                    #print(f'Adding at-start name={name} location={realName} '
                    #      f'owning board={bname}')
                    a = m.addAtStart(name            = name,
                                     location        = realName,
                                     useGridLocation = True,
                                     owningBoard     = bname,
                                     x               = 0,
                                     y               = 0)
                    p = a.addPiece(piece)
                    if p is None:
                        print(f'EEE Failed to add piece {name} ({piece}) to add-start {a}')
                    #if p is not None:
                    #    print(f'Added piece {name} in region')
                #else:
                #    print(f'Could not find piece {name}')
            
    def getGrid(self):
        return self.getParent(RegionGrid)
    def getZone(self):
        g = self.getGrid()
        if g is not None:
            return g.getZone()
        return None
    def getZonedGrid(self):
        z = self.getZone()
        if z is not None:
            return z.getZonedGrid()
        return None
    def getBoard(self):
        z = self.getZonedGrid()
        if z is not None:
            return z.getBoard()
        return self.getParent(Board)
    def getPicker(self):
        z = self.getBoard()
        if z is not None:
            return z.getPicker()
        return None
    def getMap(self):
        b = self.getPicker()
        if b is not None:
            return b.getMap()
        return None

registerElement(Region)

#
# EOF
#
# ====================================================================
# From zone.py

# --------------------------------------------------------------------
class ZonedGrid(Element):
    TAG=Element.BOARD+'ZonedGrid'
    def __init__(self,board,node=None):
        super(ZonedGrid,self).__init__(board,self.TAG,node=node)

    def getBoard(self):
        b = self.getParent(Board)
        # print(f'Get Board of Zoned: {b}')        
        return b
    def getPicker(self):
        z = self.getBoard()
        if z is not None:
            return z.getPicker()
        return None
    def getMap(self):
        z = self.getPicker()
        if z is not None:
            return z.getMap()
        return None
    def addHighlighter(self,**kwargs):
        '''Add a `Highlighter` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Highlighter
            The added element
        '''
        return self.add(ZonedGridHighlighter,**kwargs)
    def getHighlighters(self,single=True):
        '''Get all or a sole `ZonedGridHighlighter` element(s) from this
        
        Parameters
        ----------
        single : bool
            If `True`, there can be only one `Highligter` child, otherwise fail.
            If `False` return all `Highligter` children in this element
        
        Returns
        -------
        children : list
            List of `Highligter` children (even if `single=True`)
        '''
        return self.getAllElements(ZonedGridHighlighter,single=single)
    def addZone(self,**kwargs):
        '''Add a `Zone` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Zone
            The added element
        '''
        return self.add(Zone,**kwargs)
    def getZones(self,asdict=True):
        '''Get all Zone element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Zone` elements.  If `False`, return a list of all Zone` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `Zone` children
        '''
        return self.getElementsByKey(Zone,'name',asdict=asdict)

registerElement(ZonedGrid)

# --------------------------------------------------------------------
class ZonedGridHighlighter(Element):
    TAG=Element.BOARD+'mapgrid.ZonedGridHighlighter'
    def __init__(self,zoned,node=None):
        super(ZonedGridHighlighter,self).__init__(zoned,self.TAG,node=node)
    def getZonedGrid(self): return self.getParent(ZonedGrid)

    def addZoneHighlight(self,**kwargs):
        '''Add a `ZoneHighlight` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : ZoneHighlight
            The added element
        '''
        return self.add(ZoneHighlight,**kwargs)
    def getZoneHighlights(self,asdict=True):
        '''Get all ZoneHighlight element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Zone` elements.  If `False`, return a list of all Zone` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `Zone` children
        '''
        return self.getElementsByKey(ZoneHighlight,'name',asdict=asdict)

registerElement(ZonedGridHighlighter)

# --------------------------------------------------------------------
class ZoneHighlight(Element):
    TAG=Element.BOARD+'mapgrid.ZoneHighlight'
    FULL    = 'Entire Zone',
    BORDER  = 'Zone Border',
    PLAIN   = 'Plain',
    STRIPED = 'Striped'
    CROSS   = 'Crosshatched',
    TILES   = 'Tiled Image'
    UNIQUE  = ['name']
    def __init__(self,
                 highlighters,
                 node     = None,
                 name     = '',
                 color    = rgb(255,0,0),
                 coverage = FULL,
                 width    = 1,
                 style    = PLAIN,
                 image    = '',
                 opacity  = 50):
        super(ZoneHighlight,self).__init__(highlighters,
                                           self.TAG,
                                           node     = node,
                                           name     = name,
                                           color    = color,
                                           coverage = coverage,
                                           width    = width,
                                           style    = style,
                                           image    = image,
                                           opacity  = int(opacity))
    def getZonedGridHighlighter(self):
        return self.getParent(ZonedGridHighlighter)


registerElement(ZoneHighlight)


# --------------------------------------------------------------------
class ZoneProperty(Element):
    TAG = Element.MODULE+'properties.ZoneProperty'
    UNIQUE  = ['name']
    def __init__(self,zone,node=None,
                 name         = '',
                 initialValue = '',
                 isNumeric    = False,
                 min          = "null",
                 max          = "null",
                 wrap         = False,
                 description  = ""):
        super(ZoneProperty,self).__init__(zone,self.TAG,
                                            node         = node,
                                            name         = name,
                                            initialValue = initialValue,
                                            isNumeric    = isNumeric,
                                            min          = min,
                                            max          = max,
                                            wrap         = wrap,
                                            description  = description)

    def getZone(self):
        return self.getParent(Zone)

registerElement(ZoneProperty)

# --------------------------------------------------------------------
class Zone(Element):
    TAG = Element.BOARD+'mapgrid.Zone'
    UNIQUE  = ['name']
    def __init__(self,zoned,node=None,
                 name              = "",
                 highlightProperty = "",
                 locationFormat    = "$gridLocation$",
                 path              = "0,0;976,0;976,976;0,976",
                 useHighlight      = False,
                 useParentGrid     = False):
        super(Zone,self).\
            __init__(zoned,self.TAG,node=node,
                     name              = name,
                     highlightProperty = highlightProperty,
                     locationFormat    = locationFormat,
                     path              = path,
                     useHighlight      = useHighlight,
                     useParentGrid     = useParentGrid)

    def getZonedGrid(self):
        z = self.getParent(ZonedGrid)
        # print(f'Get Zoned of Zone {self["name"]}: {z}')        
        return z
    
    def getBoard(self):
        z = self.getZonedGrid()
        if z is not None:
            return z.getBoard()
        return None
    def getPicker(self):
        z = self.getBoard()
        if z is not None:
            return z.getPicker()
        return None
    def getMap(self):
        z = self.getPicker()
        if z is not None:
            return z.getMap()
        return None    
    def addHexGrid(self,**kwargs):
        '''Add a `HexGrid` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : HexGrid
            The added element
        '''
        return self.add(HexGrid,**kwargs)
    def addSquareGrid(self,**kwargs):
        '''Add a `SquareGrid` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : SquareGrid
            The added element
        '''
        return self.add(SquareGrid,**kwargs)
    def addRegionGrid(self,**kwargs):
        '''Add a `RegionGrid` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : RegionGrid
            The added element
        '''
        return self.add(RegionGrid,**kwargs)
    def addProperty(self,**kwargs):
        '''Add a `Property` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Property
            The added element
        '''
        return self.add(ZoneProperty,**kwargs)
    def getHexGrids(self,single=True):
        '''Get all or a sole `HexGrid` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `HexGrid` child, otherwise fail.
            If `False` return all `HexGrid` children in this element
        
        Returns
        -------
        children : list
            List of `HexGrid` children (even if `single=True`)
        '''
        return self.getAllElements(HexGrid,single=single)
    def getSquareGrids(self,single=True):
        '''Get all or a sole `SquareGrid` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `SquareGrid` child, otherwise fail.
            If `False` return all `SquareGrid` children in this element
        
        Returns
        -------
        children : list
            List of `SquareGrid` children (even if `single=True`)
        '''
        return self.getAllElements(SquareGrid,single=single)
    def getRegionGrids(self,single=True):
        '''Get all or a sole `RegionGrid` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `RegionGrid` child, otherwise fail.
            If `False` return all `RegionGrid` children in this element
        
        Returns
        -------
        children : list
            List of `RegionGrid` children (even if `single=True`)
        '''
        return self.getAllElements(RegionGrid,single=single)
    def getGrids(self,single=True):
        '''Get all or a sole `Grid` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `Grid` child, otherwise fail.
            If `False` return all `Grid` children in this element
        
        Returns
        -------
        children : list
            List of `Grid` children (even if `single=True`)
        '''
        g = self.getHexGrids(single=single)
        if g is not None: return g

        g = self.getSquareGrids(single=single)
        if g is not None: return g

        g = self.getRegionGrids(single=single)
        if g is not None: return g

        return g
    def getProperties(self):
        '''Get all `Property` element from this

        Returns
        -------
        children : dict
            dict of `Property` children
        '''
        return getElementsByKey(ZoneProperty,'name')
    
    def getPath(self):
        p  = self['path'].split(';')
        r  = []
        for pp in p:
            c = pp.split(',')
            r.append([int(c[0]),int(c[1])])
        return r
    
    def getBB(self):
        from functools import reduce
        path = self.getPath()
        llx  = reduce(lambda old,point:min(point[0],old),path,100000000000)
        lly  = reduce(lambda old,point:min(point[1],old),path,100000000000)
        urx  = reduce(lambda old,point:max(point[0],old),path,-1)
        ury  = reduce(lambda old,point:max(point[1],old),path,-1)
        return llx,lly,urx,ury
    def getWidth(self):
        llx,_,urx,_ = self.getBB()
        return urx-llx
    def getHeight(self):
        _,lly,_,ury = self.getBB()
        return ury-lly
    def getXOffset(self):
        return self.getBB()[0]
    def getYOffset(self):
        return self.getBB()[1]

registerElement(Zone)

#
# EOF
#
# ====================================================================
# From board.py

# --------------------------------------------------------------------
class BoardPicker(MapElement):
    TAG = Element.MAP+'BoardPicker'
    def __init__(self,doc,node=None,
                 addColumnText        = 'Add column',
                 addRowText           = 'Add row',
                 boardPrompt          = 'Select board',
                 slotHeight           = 125,
                 slotScale            = 0.2,
                 slotWidth            = 350,
                 title                = 'Choose Boards'):
        super(BoardPicker,self).__init__(doc,self.TAG,node=node,
                                         addColumnText        = addColumnText,
                                         addRowText           = addRowText,
                                         boardPrompt          = boardPrompt,
                                         slotHeight           = slotHeight,
                                         slotScale            = slotScale,
                                         slotWidth            = slotWidth,
                                         title                = title,
                                         selected             = '')

    def addSetup(self,**kwargs):
        '''Add a `Setup` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Setup
            The added element
        '''
        if 'mapName' not in kwargs:
            m = self.getMap()
            kwargs['mapName'] = m.getAttribute('mapName')
            
        return self.add(Setup,**kwargs)
    def getSetups(self,single=False):
        '''Get all or a sole `Setup` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `Setup` child, otherwise fail.
            If `False` return all `Setup` children in this element
        
        Returns
        -------
        children : list
            List of `Setup` children (even if `single=True`)
        '''
        return self.getAllElements(Setup,single=single)
    def addBoard(self,**kwargs):
        '''Add a `Board` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Board
            The added element
        '''
        return self.add(Board,**kwargs)
    def getBoards(self,asdict=True):
        '''Get all Board element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Board` elements.  If `False`, return a list of all Board` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `Board` children
        '''
        return self.getElementsByKey(Board,'name',asdict=asdict)
    
    def selectBoard(self,name):
        if name is None:
            self.setAttribute('selected','')
            return
        
        if name not in self.getBoards():
            print(f'Board "{name}" not in "{self.getMap()["mapName"]}" picker')
            return

        escname = name.replace('|',' ')
        self.setAttribute('selected',f'{self["selected"]}|{name}|')
        #print(f'Added "{name}" to selected boards: {self["selected"]}')
        
    def encode(self):
        setups = self.getSetups()
        if setups is not None and len(setups)>0:
            return [setups[0]._node.childNodes[0].nodeValue]
        
        ret    = []
        selected = self['selected']
        #print(f'Selected boards: {selected}')
        for bn in self.getBoards().keys():
            escname = '|'+bn.replace('|',' ')+'|'
            # if selected != '':
            #     print(f'Ignore board "{bn}" in map '
            #           f'{self.getMap()["mapName"]} '
            #           f'"{selected}" -> '
            #           f'{escname not in selected}')
            if escname not in selected:
                continue 
            ret.append(self.getMap()['mapName']+'BoardPicker\t'+bn+'\t0\t0')

        return ret

registerElement(BoardPicker)

# --------------------------------------------------------------------
class Setup(Element):
    TAG = 'setup'
    def __init__(self,picker,node=None,
                 mapName = '',
                 maxColumns = 1,
                 boardNames = []):
        super(Setup,self).__init__(picker,self.TAG,node=node)
        col = 0
        row = 0
        lst = [f'{mapName}BoardPicker']
        for bn in boardNames:
            lst.extend([bn,str(col),str(row)])
            col += 1
            if col >= maxColumns:
                col = 0
                row += 1
                
        txt = r'	'.join(lst)
        self.addText(txt)

    def getPicker(self): return self.getParent(BoardPicker)

registerElement(Setup)
    
# --------------------------------------------------------------------
class Board(Element):
    TAG = Element.PICKER+'Board'
    UNIQUE = ['name']
    def __init__(self,picker,node=None,
                 name       = '',
                 image      = '',
                 reversible = False,
                 color      = rgb(255,255,255),
                 width      = 0,
                 height     = 0):
        super(Board,self).__init__(picker,self.TAG,node=node,
                                   image      = image,
                                   name       = name,
                                   reversible = reversible,
                                   color      = color,
                                   width      = width,
                                   height     = height)

    def getPicker(self): return self.getParent(BoardPicker)
    def getMap(self):
        z = self.getPicker()
        if z is not None:
            return z.getMap()
        return None
    def addZonedGrid(self,**kwargs):
        '''Add a `ZonedGrid` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : ZonedGrid
            The added element
        '''
        return self.add(ZonedGrid,**kwargs)
    def getZonedGrids(self,single=True):
        '''Get all or a sole `ZonedGrid` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `ZonedGrid` child, otherwise fail.
            If `False` return all `ZonedGrid` children in this element
        
        Returns
        -------
        children : list
            List of `ZonedGrid` children (even if `single=True`)
        '''
        return self.getAllElements(ZonedGrid,single=single)
    def getZones(self,asdict=True):
        '''Get all Zone element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Zone` elements.  If `False`, return a list of all Zone` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `Zone` children
        '''
        zoned = self.getZonedGrids(single=True)
        if zoned is None: return None

        return zoned[0].getZones(asdict=asdict)

    def getWidth(self):
        # print(f'Getting width of {self}: {self["width"]}')
        if 'width' in self and int(self['width']) != 0:
            return int(self['width'])
        return 0

    def getHeight(self):
        # print(f'Getting height of {self}: {self["height"]}')
        if 'height' in self and int(self['height']) != 0:
            return int(self['height'])
        return 0

registerElement(Board)

#
# EOF
#
# ====================================================================
# From map.py

# --------------------------------------------------------------------
class BaseMap(Element):
    UNIQUE = ['mapName']
    def __init__(self,doc,tag,node=None,
                 mapName              = '',
                 allowMultiple        = 'false',
                 backgroundcolor      = rgb(255,255,255),
                 buttonName           = '',
                 changeFormat         = '$message$',
                 color                = rgb(0,0,0), # Selected pieces
                 createFormat         = '$pieceName$ created in $location$ *',
                 edgeHeight           = '0',
                 edgeWidth            = '0',
                 hideKey              = '',
                 hotkey               = key('M',ALT),
                 icon                 = '/images/map.gif',
                 launch               = 'false',
                 markMoved            = 'Always',
                 markUnmovedHotkey    = '',
                 markUnmovedIcon      = '/images/unmoved.gif',
                 markUnmovedReport    = '',
                 markUnmovedText      = '',
                 markUnmovedTooltip   = 'Mark all pieces on this map as not moved',
                 moveKey              = '',
                 moveToFormat         = '$pieceName$ moves $previousLocation$ &rarr; $location$ *',
                 moveWithinFormat     = '$pieceName$ moves $previousLocation$ &rarr; $location$ *',
                 showKey              = '',
                 thickness            = '3',
                 **kwargs):
        '''Create a map

        Parameters
        ----------
        doc : xml.minidom.Document
            Parent document 
        tag : str
            XML tag 
        node : xml.minidom.Node or None
            Existing node or None
        mapName : str
            Name of map 
        allowMultiple        : bool
            Allow multiple boards 
        backgroundcolor      : color
            Bckground color 
        buttonName           : str
            Name on button to show map = '',
        changeFormat         :
            Message format to show on changes 
        color                : color
            Color of selected pieces
        createFormat         : str
            Message format when creating a piece 
        edgeHeight           : int
            Height of edge (margin)
        edgeWidth            : int
            Width of edge (margin)
        hideKey              : Key
            Hot-key or key-command to hide map
        hotkey               : Key
            Hot-key or key-command to show map
        icon                 : path
            Icon image 
        launch               : bool
            Show on launch 
        markMoved            : str
            Show moved 
        markUnmovedHotkey    : key
            Remove moved markers 
        markUnmovedIcon      : path
            Icon for unmoved 
        markUnmovedReport    : str
            Message when marking as unmoved
        markUnmovedText      : str
            Text on button
        markUnmovedTooltip   : str
            Tooltip on button
        moveKey              : key
            Key to set moved marker 
        moveToFormat         : str
            Message format when moving 
        moveWithinFormat     : str
            Message when moving within map
        showKey              : str,
            Key to show map 
        thickness            : int
            Thickness of line around selected pieces 
        '''
        super(BaseMap,self).__init__(doc,tag,node=node,
                                     allowMultiple        = allowMultiple,
                                     backgroundcolor      = backgroundcolor,
                                     buttonName           = buttonName,
                                     changeFormat         = changeFormat,
                                     color                = color,
                                     createFormat         = createFormat,
                                     edgeHeight           = edgeHeight,
                                     edgeWidth            = edgeWidth,
                                     hideKey              = hideKey,
                                     hotkey               = hotkey,
                                     icon                 = icon,
                                     launch               = launch,
                                     mapName              = mapName,
                                     markMoved            = markMoved,
                                     markUnmovedHotkey    = markUnmovedHotkey,
                                     markUnmovedIcon      = markUnmovedIcon,
                                     markUnmovedReport    = markUnmovedReport,
                                     markUnmovedText      = markUnmovedText,
                                     markUnmovedTooltip   = markUnmovedTooltip,
                                     moveKey              = moveKey,
                                     moveToFormat         = moveToFormat,
                                     moveWithinFormat     = moveWithinFormat,
                                     showKey              = showKey,
                                     thickness            = thickness,
                                     **kwargs)

    def getGame(self):
        '''Get the game'''
        return self.getParentOfClass([Game])
    def addPicker(self,**kwargs):
        '''Add a `Picker` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Picker
            The added element
        '''
        return self.add(BoardPicker,**kwargs)
    def addFolder(self,**kwargs):
        '''Add a `ModuleFolder` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : ModuleFolder
            The added element
        '''
        return self.add(MapFolder,**kwargs)
    def getBoardPicker(self,single=True):
        '''Get all or a sole `BoardPicker` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `BoardPicker` child, otherwise fail.
            If `False` return all `BoardPicker` children in this element
        
        Returns
        -------
        children : list
            List of `BoardPicker` children (even if `single=True`)
        '''
        return self.getAllElements(BoardPicker,single)
    def getPicker(self,single=True):
        '''Get all or a sole `BoardPicker` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `BoardPicker` child, otherwise fail.
            If `False` return all `BoardPicker` children in this element
        
        Returns
        -------
        children : list
            List of `BoardPicker` children (even if `single=True`)
        '''
        return self.getAllElements(BoardPicker,single)
    def getStackMetrics(self,single=True):
        '''Get all or a sole `StackMetric` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `StackMetric` child, otherwise fail.
            If `False` return all `StackMetric` children in this element
        
        Returns
        -------
        children : list
            List of `StackMetric` children (even if `single=True`)
        '''
        return self.getAllElements(StackMetrics,single)
    def getImageSaver(self,single=True):
        '''Get all or a sole `ImageSaver` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `ImageSaver` child, otherwise fail.
            If `False` return all `ImageSaver` children in this element
        
        Returns
        -------
        children : list
            List of `ImageSaver` children (even if `single=True`)
        '''
        return self.getAllElements(ImageSaver,single)
    def getTextSaver(self,single=True):
        '''Get all or a sole `TextSaver` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `TextSaver` child, otherwise fail.
            If `False` return all `TextSaver` children in this element
        
        Returns
        -------
        children : list
            List of `TextSaver` children (even if `single=True`)
        '''
        return self.getAllElements(TextSaver,single)
    def getForwardToChatter(self,single=True):
        '''Get all or a sole `ForwardToChatter` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `ForwardToChatter` child, otherwise fail.
            If `False` return all `ForwardToChatter` children in this element
        
        Returns
        -------
        children : list
            List of `ForwardToChatter` children (even if `single=True`)
        '''
        return self.getAllElements(ForwardToChatter,single)
    def getMenuDisplayer(self,single=True):
        '''Get all or a sole `MenuDi` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `MenuDi` child, otherwise fail.
            If `False` return all `MenuDi` children in this element
        
        Returns
        -------
        children : list
            List of `MenuDi` children (even if `single=True`)
        '''
        return self.getAllElements(MenuDisplayer,single)
    def getMapCenterer(self,single=True):
        '''Get all or a sole `MapCenterer` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `MapCenterer` child, otherwise fail.
            If `False` return all `MapCenterer` children in this element
        
        Returns
        -------
        children : list
            List of `MapCenterer` children (even if `single=True`)
        '''
        return self.getAllElements(MapCenterer,single)
    def getStackExpander(self,single=True):
        '''Get all or a sole `StackExpander` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `StackExpander` child, otherwise fail.
            If `False` return all `StackExpander` children in this element
        
        Returns
        -------
        children : list
            List of `StackExpander` children (even if `single=True`)
        '''
        return self.getAllElements(StackExpander,single)
    def getPieceMover(self,single=True):
        '''Get all or a sole `PieceMover` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `PieceMover` child, otherwise fail.
            If `False` return all `PieceMover` children in this element
        
        Returns
        -------
        children : list
            List of `PieceMover` children (even if `single=True`)
        '''
        return self.getAllElements(PieceMover,single)
    def getSelectionHighlighters(self,single=True):
        '''Get all or a sole `SelectionHighlighter` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `SelectionHighlighter` child, otherwise fail.
            If `False` return all `SelectionHighlighter` children in this element
        
        Returns
        -------
        children : list
            List of `SelectionHighlighter` children (even if `single=True`)
        '''
        return self.getAllElements(SelectionHighlighters,single)
    def getKeyBufferer(self,single=True):
        return self.getAllElements(KeyBufferer,single)
    def getHighlightLastMoved(self,single=True):
        '''Get all or a sole `HighlightLa` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `HighlightLa` child, otherwise fail.
            If `False` return all `HighlightLa` children in this element
        
        Returns
        -------
        children : list
            List of `HighlightLa` children (even if `single=True`)
        '''
        return self.getAllElements(HighlightLastMoved,single)
    def getCounterDetailViewer(self,single=True):
        '''Get all or a sole `CounterDetailViewer` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `CounterDetailViewer` child, otherwise fail.
            If `False` return all `CounterDetailViewer` children in this element
        
        Returns
        -------
        children : list
            List of `CounterDetailViewer` children (even if `single=True`)
        '''
        return self.getAllElements(CounterDetailViewer,single)
    def getGlobalMap(self,single=True):
        '''Get all or a sole `GlobalMap` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `GlobalMap` child, otherwise fail.
            If `False` return all `GlobalMap` children in this element
        
        Returns
        -------
        children : list
            List of `GlobalMap` children (even if `single=True`)
        '''
        return self.getAllElements(GlobalMap,single)
    def getZoomer(self,single=True):
        '''Get all or a sole `Zoomer` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `Zoomer` child, otherwise fail.
            If `False` return all `Zoomer` children in this element
        
        Returns
        -------
        children : list
            List of `Zoomer` children (even if `single=True`)
        '''
        return self.getAllElements(Zoomer,single)
    def getHidePiecesButton(self,single=True):
        '''Get all or a sole `HidePiece` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `HidePiece` child, otherwise fail.
            If `False` return all `HidePiece` children in this element
        
        Returns
        -------
        children : list
            List of `HidePiece` children (even if `single=True`)
        '''
        return self.getAllElements(HidePiecesButton,single)
    def getMassKeys(self,asdict=True):
        '''Get all MassKey element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `MassKey` elements.  If `False`, return a list of all MassKey` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `MassKey` children
        '''
        return self.getElementsByKey(MassKey,'name',asdict)
    def getFlare(self,single=True):
        '''Get all or a sole `Flare` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `Flare` child, otherwise fail.
            If `False` return all `Flare` children in this element
        
        Returns
        -------
        children : list
            List of `Flare` children (even if `single=True`)
        '''
        return self.getAllElements(Flare,single)
    def getAtStarts(self,single=True):
        '''Get all or a sole `AtStart` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `AtStart` child, otherwise fail.
            If `False` return all `AtStart` children in this element
        
        Returns
        -------
        children : list
            List of `AtStart` children (even if `single=True`)
        '''
        return self.getAllElements(AtStart,single)
    def getBoards(self,asdict=True):
        '''Get all Board element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Board` elements.  If `False`, return a list of all Board` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `Board` children
        '''
        picker = self.getPicker()
        if picker is None:  return None
        return picker[0].getBoards(asdict=asdict)
    def getLayers(self,asdict=True):
        '''Get all `PieceLayer` element(s) from this

        Parameters
        ----------
        asdict : bool        
            If `True`, return a dictonary that maps property name
            `PieceLayers` elements.  If `False`, return a list of all
            `PieceLayers` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `PieceLayers` children

        '''
        return self.getElementsByKey(PieceLayers,'property',asdict)
    def getMenus(self,asdict=True):
        '''Get all Menu element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Board`
            elements.  If `False`, return a list of all Board`
            children.

        
        Returns
        -------
        children : dict or list
            Dictionary or list of `Board` children

        '''
        return self.getElementsByKey(Menu,'name',asdict)
    def getFolders(self,asdict=True):
        '''Get all Menu element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Folder`
            elements.  If `False`, return a list of all `Folder`
            children.

        Returns
        -------
        children : dict or list
            Dictionary or list of `Folder` children

        '''
        return self.getElementsByKey(MapFolder,'name',asdict)
    def getLOSs(self,asdict=True):
        '''Get all Menu element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Board`
            elements.  If `False`, return a list of all Board`
            children.

        
        Returns
        -------
        children : dict or list
            Dictionary or list of `Board` children

        '''
        return self.getElementsByKey(LineOfSight,'threadName',asdict)
    def addBoardPicker(self,**kwargs):
        '''Add a `BoardPicker` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : BoardPicker
            The added element
        '''
        return self.add(BoardPicker,**kwargs)
    def addStackMetrics(self,**kwargs):
        '''Add a `StackMetrics` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : StackMetrics
            The added element
        '''
        return self.add(StackMetrics,**kwargs)
    def addImageSaver(self,**kwargs):
        '''Add a `ImageSaver` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : ImageSaver
            The added element
        '''
        return self.add(ImageSaver,**kwargs)
    def addTextSaver(self,**kwargs):
        '''Add a `TextSaver` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : TextSaver
            The added element
        '''
        return self.add(TextSaver,**kwargs)
    def addForwardToChatter(self,**kwargs):
        '''Add a `ForwardToChatter` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : ForwardToChatter
            The added element
        '''
        return self.add(ForwardToChatter,**kwargs)
    def addForwardKeys(self,**kwargs):
        '''Add a `ForwardKeys` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : ForwardToChatter
            The added element
        '''
        return self.add(ForwardKeys,**kwargs)
    def addScroller(self,**kwargs):
        '''Add a `ForwardKeys` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : ForwardToChatter
            The added element
        '''
        return self.add(Scroller,**kwargs)
    def addMenuDisplayer(self,**kwargs):
        '''Add a `MenuDisplayer` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : MenuDisplayer
            The added element
        '''
        return self.add(MenuDisplayer,**kwargs)
    def addMapCenterer(self,**kwargs):
        '''Add a `MapCenterer` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : MapCenterer
            The added element
        '''
        return self.add(MapCenterer,**kwargs)
    def addStackExpander(self,**kwargs):
        '''Add a `StackExpander` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : StackExpander
            The added element
        '''
        return self.add(StackExpander,**kwargs)
    def addPieceMover(self,**kwargs):
        '''Add a `PieceMover` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : PieceMover
            The added element
        '''
        return self.add(PieceMover,**kwargs)
    def addSelectionHighlighters(self,**kwargs):
        '''Add a `SelectionHighlighters` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : SelectionHighlighters
            The added element
        '''
        return self.add(SelectionHighlighters,**kwargs)
    def addKeyBufferer(self,**kwargs):
        '''Add a `KeyBufferer` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : KeyBufferer
            The added element
        '''
        return self.add(KeyBufferer,**kwargs)
    def addHighlightLastMoved(self,**kwargs):
        '''Add a `HighlightLastMoved` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : HighlightLastMoved
            The added element
        '''
        return self.add(HighlightLastMoved,**kwargs)
    def addCounterDetailViewer(self,**kwargs):
        '''Add a `CounterDetailViewer` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : CounterDetailViewer
            The added element
        '''
        return self.add(CounterDetailViewer,**kwargs)
    def addGlobalMap(self,**kwargs):
        '''Add a `GlobalMap` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : GlobalMap
            The added element
        '''
        return self.add(GlobalMap,**kwargs)
    def addZoomer(self,**kwargs):
        '''Add a `Zoomer` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Zoomer
            The added element
        '''
        return self.add(Zoomer,**kwargs)
    def addHidePiecesButton(self,**kwargs):
        '''Add a `HidePiecesButton` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : HidePiecesButton
            The added element
        '''
        return self.add(HidePiecesButton,**kwargs)
    def addMassKey(self,**kwargs):
        '''Add a `MassKey` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : MassKey
            The added element
        '''
        return self.add(MassKey,**kwargs)
    def addStartupMassKey(self,**kwargs):
        '''Add a `StartupMassKey` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : StartupMassKey
            The added element
        '''
        return self.add(MassKey,**kwargs)
    def addFlare(self,**kwargs):
        '''Add a `Flare` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Flare
            The added element
        '''
        return self.add(Flare,**kwargs)
    def addAtStart(self,**kwargs):
        '''Add a `AtStart` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : AtStart
            The added element
        '''
        return self.add(AtStart,**kwargs)


    def addLayers(self,**kwargs):
        '''Add `PieceLayers` element to this
        
        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : PieceLayers
            The added element
        '''
        return self.add(PieceLayers,**kwargs)
    def addMenu(self,**kwargs):
        '''Add a `Menu` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Menu
            The added element
        '''
        return self.add(Menu,**kwargs)
    def addLOS(self,**kwargs):
        '''Add a `Menu` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Menu
            The added element
        '''
        return self.add(LineOfSight,**kwargs)
     
# --------------------------------------------------------------------
class Map(BaseMap):
    TAG = Element.MODULE+'Map'
    def __init__(self,doc,node=None,
                 mapName              = '',
                 allowMultiple        = 'false',
                 backgroundcolor      = rgb(255,255,255),
                 buttonName           = '',
                 changeFormat         = '$message$',
                 color                = rgb(0,0,0),
                 createFormat         = '$pieceName$ created in $location$ *',
                 edgeHeight           = '0',
                 edgeWidth            = '0',
                 hideKey              = '',
                 hotkey               = key('M',ALT),
                 icon                 = '/images/map.gif',
                 launch               = 'false',
                 markMoved            = 'Always',
                 markUnmovedHotkey    = '',
                 markUnmovedIcon      = '/images/unmoved.gif',
                 markUnmovedReport    = '',
                 markUnmovedText      = '',
                 markUnmovedTooltip   = 'Mark all pieces on this map as not moved',
                 moveKey              = '',
                 moveToFormat         = '$pieceName$ moves $previousLocation$ &rarr; $location$ *',
                 moveWithinFormat     = '$pieceName$ moves $previousLocation$ &rarr; $location$ *',
                 showKey              = '',
                 thickness            = '3'):
        super(Map,self).__init__(doc,self.TAG,node=node,
                                 allowMultiple        = allowMultiple,
                                 backgroundcolor      = backgroundcolor,
                                 buttonName           = buttonName,
                                 changeFormat         = changeFormat,
                                 color                = color,
                                 createFormat         = createFormat,
                                 edgeHeight           = edgeHeight,
                                 edgeWidth            = edgeWidth,
                                 hideKey              = hideKey,
                                 hotkey               = hotkey,
                                 icon                 = icon,
                                 launch               = launch,
                                 mapName              = mapName,
                                 markMoved            = markMoved,
                                 markUnmovedHotkey    = markUnmovedHotkey,
                                 markUnmovedIcon      = markUnmovedIcon,
                                 markUnmovedReport    = markUnmovedReport,
                                 markUnmovedText      = markUnmovedText,
                                 markUnmovedTooltip   = markUnmovedTooltip,
                                 moveKey              = moveKey,
                                 moveToFormat         = moveToFormat,
                                 moveWithinFormat     = moveWithinFormat,
                                 showKey              = showKey,
                                 thickness            = thickness)

    def getGame(self):
        return self.getParent(Game)

registerElement(Map)

# --------------------------------------------------------------------
class WidgetMap(BaseMap):
    TAG = Element.WIDGET+'WidgetMap'
    def __init__(self,doc,node=None,**attr):
        super(WidgetMap,self).__init__(doc,self.TAG,node=node,**attr)

    def getGame(self):
        return self.getParentOfClass([Game])
    def getMapWidget(self):
        return self.getParent(MapWidget)

registerElement(WidgetMap)

# --------------------------------------------------------------------
class BasePrivateMap(BaseMap):
    def __init__(self,
                 doc,
                 tag,                  
                 node                 = None,
                 mapName              = '',
                 allowMultiple        = 'false',
                 backgroundcolor      = rgb(255,255,255),
                 buttonName           = '',
                 changeFormat         = '$message$',
                 color                = rgb(0,0,0),
                 createFormat         = '$pieceName$ created in $location$ *',
                 edgeHeight           = '0',
                 edgeWidth            = '0',
                 hideKey              = '',
                 hotkey               = key('M',ALT),
                 icon                 = '/images/map.gif',
                 launch               = 'false',
                 markMoved            = 'Always',
                 markUnmovedHotkey    = '',
                 markUnmovedIcon      = '/images/unmoved.gif',
                 markUnmovedReport    = '',
                 markUnmovedText      = '',
                 markUnmovedTooltip   = 'Mark all pieces on this map as not moved',
                 moveKey              = '',
                 moveToFormat         = '$pieceName$ moves $previousLocation$ &rarr; $location$ *',
                 moveWithinFormat     = '$pieceName$ moves $previousLocation$ &rarr; $location$ *',
                 showKey              = '',
                 thickness            = '3',
                 side                 = [],
                 visible              = False,
                 use_boards           = ''):
        lsides = [side] if isinstance(side,str) else ','.join(side)
        super().__init__(doc,
                         self.TAG,
                         node                 = node,
                         allowMultiple        = allowMultiple,
                         backgroundcolor      = backgroundcolor,
                         buttonName           = buttonName,
                         changeFormat         = changeFormat,
                         color                = color,
                         createFormat         = createFormat,
                         edgeHeight           = edgeHeight,
                         edgeWidth            = edgeWidth,
                         hideKey              = hideKey,
                         hotkey               = hotkey,
                         icon                 = icon,
                         launch               = launch,
                         mapName              = mapName,
                         markMoved            = markMoved,
                         markUnmovedHotkey    = markUnmovedHotkey,
                         markUnmovedIcon      = markUnmovedIcon,
                         markUnmovedReport    = markUnmovedReport,
                         markUnmovedText      = markUnmovedText,
                         markUnmovedTooltip   = markUnmovedTooltip,
                         moveKey              = moveKey,
                         moveToFormat         = moveToFormat,
                         moveWithinFormat     = moveWithinFormat,
                         showKey              = showKey,
                         thickness            = thickness,
                         side                 = lsides,
                         visible              = visible,
                         use_boards           = use_boards)

    def getSides(self):
        return self['side'].split(',')

    def setSides(self,*sides):
        self['side'] = ','.join(sides)

    def getMap(self):
        game = self.getGame()
        maps = game.getMaps()
        return maps.get(self['use_boards'])

    def setMap(self,map):
        self['use_boards'] = map if isinstance(map,str) else map['mapName']

# --------------------------------------------------------------------
class PrivateMap(BasePrivateMap):
    TAG = Element.MODULE+'PrivateMap'
    def __init__(self,
                 doc,
                 **kwargs):
        super().__init__(doc,self.TAG,**kwargs)
        
registerElement(PrivateMap)

# --------------------------------------------------------------------
class PlayerHand(BasePrivateMap):
    TAG = Element.MODULE + 'PlayerHand'
    def __init__(self,doc,**kwargs):
        super().__init__(doc,self.TAG,**kwargs)

registerElement(PlayerHand)

#
# EOF
#
# ====================================================================
# From chart.py

# --------------------------------------------------------------------
class ChartWindow(GameElement,WidgetElement):
    TAG=Element.MODULE+'ChartWindow'
    UNIQUE = ['name']
    def __init__(self,elem,node=None,
                 name        = '',
                 hotkey      = key('A',ALT),
                 description = '',
                 text        = '',
                 tooltip     = 'Show/hide Charts',
                 icon        = '/images/chart.gif'):
        super(ChartWindow,self).__init__(elem,self.TAG,node=node,
                                         name        = name,
                                         hotkey      = hotkey,
                                         description = description,
                                         text        = text,
                                         tooltip     = tooltip,
                                         icon        = icon)

    def addChart(self,**kwargs):
        '''Add a `Chart` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Chart
            The added element
        '''
        return self.add(Chart,**kwargs)
    def getCharts(self,asdict=True):
        '''Get all Chart element(s) from this

        Parameters
        ----------
        asdict : bool        
            If `True`, return a dictonary that maps key to `Chart`
            elements.  If `False`, return a list of all Chart`
            children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `Chart` children

        '''
        return self.getElementsById(Chart,'chartName',asdict=asdict)
    
registerElement(ChartWindow)    

# --------------------------------------------------------------------
class Chart(Element):
    TAG=Element.WIDGET+'Chart'
    UNIQUE = ['chartName','fileName']
    def __init__(self,elem,node=None,
                 chartName   = '',
                 fileName    = '',
                 description = ''):
        super(Chart,self).__init__(elem,self.TAG,node=node,
                                   chartName   = chartName,
                                   description = description,
                                   fileName    = fileName)

registerElement(Chart)

#
# EOF
#
# ====================================================================
# From command.py

# --------------------------------------------------------------------
class Command:
    def __init__(self,what,iden,tpe,state):
        self.cmd = '/'.join([what,iden,tpe,state])
    
# --------------------------------------------------------------------
class AddCommand(Command):
    ID = '+'
    def __init__(self,iden,tpe,state):
        super(AddCommand,self).__init__(self.ID,iden,tpe,state)
        

#
# EOF
#
# ====================================================================
# From trait.py
# ====================================================================
class Trait:
    known_traits = []
    def __init__(self):
        '''Base class for trait capture.
        
        Unlike the Element classes, this actually holds state that
        isn't reflected elsewhere in the DOM.  This means that the
        data here is local to the object.  So when we do
        
            piece  = foo.getPieceSlots()[0]
            traits = p.getTraits()
            for trait in traits:
                if trait.ID == 'piece': 
                    trait["gpid"] = newPid
                    trait["lpid"] = newPid
        
        we do not actually change anything in the DOM.  To do that, we
        must add back _all_ the traits as
        
            piece.setTraits(traits)
        
        We can add traits to a piece, like
        
            piece.addTrait(MarkTrait('Hello','World'))
        
        But it is not particularly efficient.  Better to do
        (continuing from above)
        
            traits.append(MarkTrait('Hello','World;)
            piece.setTraits(traits)
        
        .. include:: ../../vassal/traits/README.md
           :parser: myst_parser.sphinx_
        
        '''
        self._type  = None
        self._state = None

    def setType(self,**kwargs):
        '''Set types.  Dictionary of names and values.  Dictonary keys
        defines how we access the fields, which is internal here.
        What matters is the order of the values.

        '''
        self._type   = list(kwargs.values())
        self._tnames = list(kwargs.keys())

    def setState(self,**kwargs):
        '''Set states.  Dictionary of names and values.  Dictonary keys
        defines how we access the fields, which is internal here.
        What matters is the order of the values.
        '''
        self._state  = list(kwargs.values())
        self._snames = list(kwargs.keys())

    def __getitem__(self,key):
        '''Look up item in either type or state'''
        try:
            return self._type[self._tnames.index(key)]
        except:
            pass
        return self._state[self._snames.index(key)]

    def __setitem__(self,key,value):
        '''Set item in either type or state'''
        try:
            self._type[self._tnames.index(key)] = value
            return
        except:
            pass
        self._state[self._snames.index(key)] = value

    def encode(self,term=False):
        '''
        returns type and state encoded'''
        t = self.encodeFields(self.ID,*self._type,term=term)
        s = self.encodeFields(*self._state,term=term)
        return t,s

    @classmethod
    def findTrait(cls,traits,ID,key=None,value=None,verbose=False):
        for trait in traits:
            if trait.ID != ID:
                continue
            if verbose:
                print(f' {trait.ID}')
            if key is None or value is None:
                if verbose:
                    print(f' Return {trait.ID}')
                return trait
            if verbose:
                print(f' Check {key}={value}: {trait[key]}')
            if trait[key] == value:
                return trait
        if verbose:
            print(f' Trait of type {ID} with {key}={value} not found')
        return None
        
    @classmethod
    def take(cls,iden,t,s):
        '''If the first part of the string t matches the ID, then take it.

        t and s are lists of strings.
        ''' 
        if iden != cls.ID: return None

        ret = cls()
        ret._type = t
        ret._state = s
        ret.check() # Check if we're reasonable, or raise
        #print(f'Took {iden} {cls}\n'
        #      f'  {ret._tnames}\n'
        #      f'  {ret._snames}')
        return ret

    def check(self):
        '''Implement if trait should check that all is OK when cloning'''
        pass

    @classmethod
    def encodeFields(cls,*args,term=False):
        return ';'.join([str(e).lower() if isinstance(e,bool) else str(e)
                         for e in args])+(';' if term else '')

    @classmethod
    def decodeFields(cls,s):
        from re import split
        return split(r'(?<!\\);',s)
        # return s.split(';') # Probably too simple-minded 

    @classmethod
    def encodeKeys(cls,keys,sep=','):
        return sep.join([k.replace(',','\\'+f'{sep}') for k in keys])
        
    @classmethod
    def decodeKeys(cls,keys,sep=','):
        from re import split
        ks = split(r'(?<!\\)'+f'{sep}',keys)
        return [k.replace('\\'+f'{sep}',f'{sep}') for k in ks]

    @classmethod
    def flatten(cls,traits,game=None,prototypes=None,verbose=False):
        if prototypes is None:
            if game is None:
                print(f'Warning: Game or prototypes not passed')
                return None
            prototypes = game.getPrototypes()[0].getPrototypes()

        if len(traits) < 1: return None

        basic = None
        if traits[-1].ID == 'piece': # BasicTrait.ID:
            basic = traits.pop()

        if verbose:
            print(f'Piece {basic["name"]}')
            
        ret = cls._flatten(traits,prototypes,' ',verbose)
        ret.append(basic)

        return ret
    
    @classmethod
    def _flatten(cls,traits,prototypes,ind,verbose):
        '''Expand all prototype traits in traits'''
        ret = []
        for trait in traits:
            # Ignore recursive basic traits
            if trait.ID == BasicTrait.ID:
                continue
            # Add normal traits
            if trait.ID != PrototypeTrait.ID:
                if verbose:
                    print(f'{ind}Adding trait "{trait.ID}"')
                    
                ret.append(trait)
                continue

            # Find prototype
            name  = trait['name']
            proto = prototypes.get(name,None)
            if proto is None:
                if name != ' prototype':
                    print(f'{ind}Warning, prototype {name} not found')
                continue

            if verbose:
                print(f'{ind}Expanding prototype "{name}"')
                
            # Recursive call to add prototype traits (and possibly
            # more recursive calls 
            ret.extend(cls._flatten(proto.getTraits(), prototypes,
                                    ind+' ',verbose))

        return ret

    def print(self,file=None):
        if file is None:
            from sys import stdout
            file = stdout

        nt = max([len(i) for i in self._tnames]) if self._tnames else 0
        ns = max([len(i) for i in self._snames]) if self._snames else 0
        nw = max(nt,ns)

        print(f'Trait ID={self.ID}',file=file)
        print(f' Type:',            file=file)
        for n,v in zip(self._tnames,self._type):
            print(f'  {n:<{nw}s}: {v}',file=file)
        print(f' State:',           file=file)
        for n,v in zip(self._snames,self._state):
            print(f'  {n:<{nw}s}: {v}',file=file)
            
#
# EOF
#
# ====================================================================
# From withtraits.py

# --------------------------------------------------------------------
#
# Traits of this kind of object are
#
# - Evaluated from the start of the list to the end of the list,
#   skipping over report and trigger traits
# - Then evaluated from the end of the list to the start, only
#   evaluating report and trigger traits
# - The list _must_ end in a BasicTrait
#
# Traits are copied when making a copy of objects of this class, and
# are done so using a full decoding and encoding.  This means that
# copying is a bit susceptible to expansions of the strings of the traits,
# in particular if they contain special characters such as ',' or '/'.
#
class WithTraits(Element):
    UNIQUE = ['entryName']
    def __init__(self,parent,tag,node=None,traits=[],**kwargs):
        '''Base class for things that have traits

        Parameters
        ----------
        parent : Element
            Parent to add this to
        node : xml.minidom.Element
            If not None, XML element to read definition from.
            Rest of the arguments are ignored if not None.
        traits : list of Trait objects
            The traits to set on this object
        kwargs : dict
            More attributes to set on element
        '''
        super(WithTraits,self).__init__(parent,tag,node=node,**kwargs)
        if node is None: self.setTraits(*traits)
        
    def addTrait(self,trait):
        '''Add a `Trait` element to this.  Note that this re-encodes
        all traits.

        Parameters
        ----------
        trait : Trait
            The trait to add 
        '''
        traits = self.getTraits()
        traits.append(trait)
        self.setTraits(*traits)


    def getTraits(self):
        '''Get all element traits as objects.  This decodes the trait
        definitions.  This is useful if we have read the element from
        the XML file, or similar.

        Note that the list of traits returned are _not_ tied to the
        XML nodes content.  Therefore, if one makes changes to the list,
        or to elements of the list, and these changes should be
        reflected in this object, then we _must_ call

            setTraits(traits)

        with the changed list of traits. 

        Returns
        -------
        traits : list of Trait objects
            The decoded traits

        '''
        code = self._node.childNodes[0].nodeValue
        return self.decodeAdd(code)

    def encodedStates(self):
        from re import split

        code = self._node.childNodes[0].nodeValue
        cmd, iden, typ, sta = split(fr'(?<!\\)/',code) #code.split('/')

        return sta

    def decodeStates(self,code,verbose=False):
        from re import split
        
        newstates, oldstates = split(fr'(?<!\\)/',code)#code.split('/')
        
        splitit = lambda l : \
            [s.strip('\\').split(';') for s in l.split(r'	')]

        newstates = splitit(newstates)
        oldstates = splitit(oldstates)
        
        traits = self.getTraits()

        if len(traits) != len(newstates):
            print(f'Piece has {len(traits)} traits but got '
                  f'{len(newstates)} states')
        
        for trait, state in zip(traits,newstates):
            trait._state = state;
            # print(trait.ID)
            # for n,s in zip(trait._snames,trait._state):
            #     print(f'  {n:30s}: {s}')

        self.setTraits(*traits)
            
    def copyStates(self,other,verbose=False):
        straits = other.getTraits()
        dtraits = self.getTraits()

        matches = 0
        for strait in straits:
            if len(strait._state) < 1:
                continue

            cand = []
            ttrait = None
            for dtrait in dtraits:
                if dtrait.ID == strait.ID:
                    cand.append(dtrait)

            if verbose and len(cand) < 1:
                print(f'Could not find candidate for {strait.ID}')
                continue

            if len(cand) == 1:
                ttrait = cand[0]

            else:
                # print(f'Got {len(cand)} candidiate targets {strait.ID}')

                best  = None
                count = 0
                types = strait._type
                for c in cand:
                    cnt = sum([ct == t for ct,t in zip(c._type, types)])
                    if cnt > count:
                        best = c
                        count = cnt
                        
                if verbose and best is None:
                    print(f'No candidate for {strait.ID} {len(again)}')

                if verbose and count+2 < len(types):
                    print(f'Ambigious candidate for {strait.ID} '
                          f'({count} match out of {len(types)})')
                    #print(best._type)
                    #print(types)
                       
                ttrait = best

            if ttrait is None:
                continue

            ttrait._state = strait._state
            matches += 1
            # print(ttrait.ID)
            # for n,s in zip(ttrait._snames,ttrait._state):
            #     print(f'  {n:30s}: {s}')

        if verbose:
            print(f'Got {matches} matches out of {len(dtraits)}')

        self.setTraits(*dtraits)
            
            
    def decodeAdd(self,code,verbose=False):
        '''Try to decode make a piece from a piece of state code'''
        from re import split
        
        cmd, iden, typ, sta = split(fr'(?<!\\)/',code) #code.split('/')
        # print(cmd,iden,typ,sta)
        
        types               = typ.split(r'	')
        states              = sta.split(r'	')
        types               = [t.strip('\\').split(';') for t in types]
        states              = [s.strip('\\').split(';') for s in states]
        traits              = []
        
        for t, s in zip(types,states):
            tid   = t[0]
            trem  = t[1:]
            known = False
            
            for c in Trait.known_traits:
                t = c.take(tid,trem,s) # See if we have it
                if t is not None:
                    traits.append(t)  # Got it
                    known = True
                    break
                
            if not known:
                print(f'Warning: Unknown trait {tid}')

        return traits

    def encodeAdd(self,*traits,iden='null',verbose=False):
        '''Encodes type and states'''
        if len(traits) < 1: return ''
        
        last = traits[-1]
        # A little hackish to use the name of the class, but needed
        # because of imports into patch scripts.
        lastBasic = isinstance(last,BasicTrait) or \
            last.__class__.__name__.endswith('BasicTrait')
        lastStack = isinstance(last,StackTrait) or \
            last.__class__.__name__.endswith('StackTrait')
        if not lastBasic and not lastStack:
            from sys import stderr
            print(f'Warning - last trait NOT a Basic(Stack)Trait, '
                  f'but a {type(last)}',
                  file=stderr)
            
        types = []
        states = []
        for trait in traits:
            if trait is None:
                print(f'Trait is None (traits: {traits})')
                continue
            tpe, state = trait.encode()
            types.append(tpe)
            states.append(state)

        tpe   = WithTraits.encodeParts(*types)
        state = WithTraits.encodeParts(*states)
        add   = AddCommand(str(iden),tpe,state)
        return add.cmd
        
    
    def setTraits(self,*traits,iden='null'):
        '''Set traits on this element.  This encodes the traits into
        this object.
        
        Parameters
        ----------
        traits : tuple of Trait objects
            The traits to set on this object.
        iden : str
            Identifier

        '''
        add = self.encodeAdd(*traits,iden=iden)
        if self._node is None:
            # from xml.dom.minidom import Element, Text
            self._node = xmlns.Element(self.TAG)
            self._node.appendChild(xmlns.Text())
            
        if len(self._node.childNodes) < 1:
            self.addText('')
        self._node.childNodes[0].nodeValue = add

    def removeTrait(self,ID,key=None,value=None,verbose=False):
        '''Remove a trait from this object.

        Parameters
        ----------
        ID : str
            The type of trait to remove.  Must be a valid
            ID of a class derived from Trait.
        key : str
            Optional key to inspect to select trait that has 
            this key and the traits key value is the argument value,
        value :
            If specified, then only traits which key has this value
            are removed
        verbose : bool
            Be verbose if True

        Returns
        -------
        trait : Trait
            The removed trait or None
        '''
        traits = self.getTraits()
        trait  = Trait.findTrait(traits,ID,key,value,verbose)
        if trait is not None:
            traits.remove(trait)
            self.setTraits(traits)
        return trait

    def addTraits(self,*toadd):
        '''Add traits to this.  Note that this will
        decode and reencode the traits.  Only use this when
        adding traits on-mass.  Repeated use of this is inefficient.

        This member function takes care to push any basic trait to
        the end of the list.

        The added traits will not override existing triats. 

        Paramters
        ---------
        toAdd : tuple of Trait objects
            The traits to add 

        '''
        traits = self.getTraits()
        basic  = Trait.findTrait(traits,BasicTrait.ID)
        if basic:
            traits.remove(basic)
        traits.extend(toAdd)
        if basic:
            traits.append(basic)
        self.setTraits(traits)
        
        
    @classmethod
    def encodeParts(cls,*parts):
        '''Encode parts of a full piece definition

        Each trait (VASSAL.counter.Decorator,
        VASSAL.counter.BasicPiece) definition or state is separated by
        a litteral TAB character.  Beyond the first TAB separator,
        additional escape characters (BACKSLAH) are added in front of
        the separator.  This is to that VASSAL.utils.SequenceDecoder
        does not see consequitive TABs as a single TAB.
        '''
        ret = ''
        sep = r'	'
        for i, p in enumerate(parts):
            if i != 0:
                ret += '\\'*(i-1) + sep
            ret += str(p)

        return ret
        
        
    def cloneNode(self,parent):
        '''This clones the underlying XML node.

        Parameters
        ----------
        parent : Element
            The element to clone this element into

        Returns
        -------
        copy : xml.minidom.Element
            The newly created clone of this object's node
        '''
        copy = self._node.cloneNode(deep=True)
        if parent is not None:
            parent._node.appendChild(copy)
        else:
            print('WARNING: No parent to add copy to')
        return copy

    def print(self,file=None,recursive=1024,indent=''):
        if file is None:
            from sys import stdout
            file = stdout
            
        from textwrap import indent as i
        
        if recursive <= 1:
            n = len(self.getTraits())
            if n > 1:
                print(i(f'  {n} traits',indent),file=file)
            return
        
            
        from io import StringIO


        stream = StringIO()
        traits = self.getTraits()
        for trait in traits:
            trait.print(stream)

        s = i(stream.getvalue().rstrip(), '  ')
        print(i(s,indent), file=file)
        
    
# --------------------------------------------------------------------
class DummyWithTraits(WithTraits):
    TAG = 'dummy'
    def __init__(self,parent,node=None,traits=[]):
        '''An empty element.  Used when making searching'''
        super(DummyWithTraits,self).__init__(tag       = self.TAG,
                                             parent    = parent,
                                             node      = node,
                                             traits    = traits)
        if parent is not None:
            parent.remove(self)


registerElement(DummyWithTraits)

# --------------------------------------------------------------------
class WithTraitsSlot(WithTraits):
    def __init__(self,
                 parent,
                 tag,
                 node           = None,
                 entryName      = '',
                 traits         = [],
                 gpid           = 0,
                 height         = 72,
                 width          = 72,
                 icon           = ''):
        '''A piece slot.  Used all the time.

        Parameters
        ----------
        parent : Element
            Parent to add this to
        node : xml.minidom.Element
            If not None, XML element to read definition from.
            Rest of the arguments are ignored if not None.
        entryName : str
            Name of this
        traits : list of Trait objects
            The traits to set on this object
        gpid : int
            Global Piece identifier. If 0, will be set by Game
        height : int
            Height size of the piece (in pixels)
        width : int
            Width size of the piece (in pixels)
        icon : str
            Piece image file name within 'image' sub-dir of archive
        '''
        super().\
            __init__(parent,
                     tag,
                     node      = node,
                     traits    = traits,
                     entryName = entryName,
                     gpid      = gpid,
                     height    = height,
                     width     = width,
                     icon      = icon)

    
    def _clone(self,cls,parent):
        '''Adds copy of self to parent, possibly with new GPID'''
        game  = self.getParentOfClass([Game])
        gpid  = game.nextPieceSlotId()
        #opid  = int(self.getAttribute('gpid'))
        #print(f'Using GPID={gpid} for clone {opid}')
        
        node  = self.cloneNode(parent)
        piece = cls(parent,node=node)
        piece.setAttribute('gpid',gpid)
        
        traits = piece.getTraits()
        for trait in traits:
            if isinstance(trait,BasicTrait):
                trait['gpid'] = gpid

        piece.setTraits(*traits)
        return piece

    def print(self,file=None,recursive=1024,indent=''):
        if file is None:
            from sys import stdout
            file = stdout
        from textwrap import indent as i

        print(i(f'{type(self).__name__} {self["entryName"]}'+'\n'
                f' gpid  : {self["gpid"]}'+'\n'
                f' height: {self["height"]}'+'\n'
                f' width : {self["width"]}'+'\n'
                f' icon  : {self["icon"]}',indent),
              file = file)

        super().print(file=file,
                      recursive=recursive-1,
                      indent=indent)

# --------------------------------------------------------------------
class PieceSlot(WithTraitsSlot):
    TAG = Element.WIDGET+'PieceSlot'
    def __init__(self,
                 parent,
                 node           = None,
                 entryName      = '',
                 traits         = [],
                 gpid           = 0,
                 height         = 72,
                 width          = 72,
                 icon           = ''):
        '''A piece slot.  Used all the time.

        Parameters
        ----------
        parent : Element
            Parent to add this to
        node : xml.minidom.Element
            If not None, XML element to read definition from.
            Rest of the arguments are ignored if not None.
        entryName : str
            Name of this
        traits : list of Trait objects
            The traits to set on this object
        gpid : int
            Global Piece identifier. If 0, will be set by Game
        height : int
            Height size of the piece (in pixels)
        width : int
            Width size of the piece (in pixels)
        icon : str
            Piece image file name within 'image' sub-dir of archive
        '''
        super().\
            __init__(parent,
                     self.TAG,
                     node      = node,
                     traits    = traits,
                     entryName = entryName,
                     gpid      = gpid,
                     height    = height,
                     width     = width,
                     icon      = icon)

    
    def clone(self,parent):
        return self._clone(PieceSlot,parent)
        
        
registerElement(PieceSlot)

# --------------------------------------------------------------------
class CardSlot(WithTraitsSlot):
    TAG = Element.WIDGET+'CardSlot'
    def __init__(self,
                 parent,
                 node           = None,
                 entryName      = '',
                 traits         = [],
                 gpid           = 0,
                 height         = 72,
                 width          = 72,
                 icon           = ''):        
        '''A card slot.  Used all the time.  It is essentially the
        same as a PieceSlot, though a `MaskTrait` is added (with
        default settings), if no such trait is present (to-be-done)

        Parameters
        ----------
        parent : Element
            Parent to add this to
        node : xml.minidom.Element
            If not None, XML element to read definition from.
            Rest of the arguments are ignored if not None.
        entryName : str
            Name of this
        traits : list of Trait objects
            The traits to set on this object
        gpid : int
            Global Piece identifier. If 0, will be set by Game
        height : int
            Height size of the card (in pixels)
        width : int
            Width size of the card (in pixels)
        icon : str
            Card image file name within 'image' sub-dir of archive

        '''
        super().\
            __init__(parent,
                     self.TAG,
                     node      = node,
                     traits    = traits,
                     entryName = entryName,
                     gpid      = gpid,
                     height    = height,
                     width     = width,
                     icon      = icon)

    def clone(self,parent):
        return self._clone(CardSlot,parent)
        
registerElement(CardSlot)
        
# --------------------------------------------------------------------
class Prototype(WithTraits):
    TAG = Element.MODULE+'PrototypeDefinition'
    UNIQUE = ['name']
    def __init__(self,cont,node=None,
                 name          = '',
                 traits        = [],
                 description   = ''):
        '''A prototype.  Used all the time.

        Parameters
        ----------
        cont : Element
            Parent to add this to
        node : xml.minidom.Element
            If not None, XML element to read definition from.
            Rest of the arguments are ignored if not None.
        name : str
            Name of this
        traits : list of Trait objects
            The traits to set on this object
        description : str
            A free-form description of this prototype
        '''
        super(Prototype,self).__init__(cont,self.TAG,node=node,
                                       traits      = traits,
                                       name        = name,
                                       description = description)
    
    def print(self,file=None,recursive=1024,indent=''):
        if file is None:
            from sys import stdout
            file = stdout
        from textwrap import indent as i

        print(i(f'Prototype {self["name"]}'+'\n'
                f' description: {self["description"]}',indent),
              file = file)
        
        super(Prototype,self).print(file=file,
                                    indent=indent,
                                    recursive=recursive-1)
        
registerElement(Prototype)

#
# EOF
#
# ====================================================================
# From extension.py

# ====================================================================
class Extension(Element):
    TAG = Element.MODULE+'ModuleExtension'
    def __init__(self,
                 parent          = None,
                 node            = None,
                 anyModule       = False,
                 version         = '',
                 description     = '',
                 module          = '',
                 moduleVersion   = '',
                 vassalVersion   = '',
                 nextPieceSlotId = 0,
                 extensionId     = 0,
                 asDocument      = False):
        super().__init__(parent,self.TAG,node)

        self._tag  = 'extension'
        if self._node is None:
            #from xml.dom.minidom import Document


            self._root = xmlns.Document()
            self._node = self._root
            self.setAttributes(
                anyModule       = anyModule,
                version         = version,
                description     = description,
                module          = module,
                moduleVersion   = moduleVersion,
                vassalVersion   = vassalVersion,
                nextPieceSlotId = nextPieceSlotId,
                extensionId     = extensionId)

    def addExtensionElement(self,**kwargs):
        '''Add an extension element'''

        return self.add(ExtensionElement,**kwargs)
        
    # ----------------------------------------------------------------
    def getExtensionElements(self,asdict=True):
        '''Get all or a sole `GlobalPropertie` element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to
            `ExtensionElement` elements.  If `False`, return a list of
            all `ExtensionElement` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `Extension` children

        '''
        return self.getElementsByKey(ExtensionElement,'target',asdict)

registerElement(Extension)
    
# --------------------------------------------------------------------
class ExtensionElement(Element):
    TAG    = Element.MODULE + 'ExtensionElement'
    UNIQUE = ['target']
    
    def __init__(self,
                 extension,
                 node         = None,
                 target       = ''):
        super().__init__(extension,
                         self.TAG,
                         node = node,
                         target = target)


    def getTarget(self):
        return self['target']

    @property 
    def target(self):
        return self.getTarget()
    
    def getSelect(self):
        parts = self.target.split('/')
        specs = [p.split(':') for p in parts]
        return specs


registerElement(ExtensionElement)
        
# --------------------------------------------------------------------
#
# EOF
#
# ====================================================================
# From traits/area.py

class AreaTrait(Trait):
    ID = 'AreaOfEffect'
    def __init__(self,
                 transparancyColor = rgb(0x77,0x77,0x77),
                 transparancyLevel = 30,
                 radius            = 1,
                 alwaysActive      = False,
                 activateCommand   = 'Toggle area of effect',
                 activateKey       = key('A'), # Ctrl-A
                 mapShaderName     = '',
                 fixedRadius       = True,
                 radiusMarker      = '', # Property
                 description       = 'Show area of effect',
                 name              = 'EffectArea',
                 onMenuText        = '', # Show area of effect
                 onKey             = '', # key('A')
                 offMenuText       = '', # Hide area of effect
                 offKey            = '', # key(A,SHIFT)
                 globallyVisible   = True):
        super(AreaTrait,self).__init__()
        self.setType(
                 transparancyColor = transparancyColor,
                 transparancyLevel = int(transparancyLevel),
                 radius            = radius,
                 alwaysActive      = alwaysActive,
                 activateCommand   = activateCommand,
                 activateKey       = activateKey,
                 mapShaderName     = mapShaderName,
                 fixedRadius       = fixedRadius,
                 radiusMarker      = radiusMarker,
                 description       = description,
                 name              = name,
                 onMenuText        = onMenuText,
                 onKey             = onKey,
                 offMenuText       = offMenuText,
                 offKey            = offKey,
                 globallyVisible   = globallyVisible
        )
        self.setState(active = alwaysActive or not globallyVisible)

Trait.known_traits.append(AreaTrait)
#
# EOF
#
# ====================================================================
# From traits/clone.py

# --------------------------------------------------------------------
class CloneTrait(Trait):
    ID      = 'clone'
    def __init__(self,
                 command         = '',
                 key             = '',
                 description     = ''):
        '''Create a clone trait (VASSAL.counter.Clone)'''
        super().__init__()

        self.setType(command         = command,          # Context menu name
                     key             = key,              # Context menu key
                     description     = description)     
        self.setState(state='')

        

Trait.known_traits.append(CloneTrait)

#
# EOF
#
# ====================================================================
# From traits/dynamicproperty.py

# --------------------------------------------------------------------
# 
# 
class ChangePropertyTrait(Trait):
    DIRECT = 'P'
    INCREMENT = 'I'
    PROMPT = 'R'
    def __init__(self,
                 *commands,
                 numeric     = False,
                 min         = 0,
                 max         = 100,
                 wrap        = False):
        '''Base class for property (piece or global) change traits.
        
           Encodes constraints and commands.
        '''
        # assert name is not None and len(name) > 0, \
        #     'No name specified for ChangePropertyTriat'
        super(ChangePropertyTrait,self).__init__()
        self._constraints = self.encodeConstraints(numeric,wrap,min,max)
        self._commands    = self.encodeCommands(commands)

    def encodeConstraints(self,numeric,wrap,min,max):
        isnum             = f'{numeric}'.lower()
        iswrap            = f'{wrap}'.lower()
        return f'{isnum},{min},{max},{iswrap}'

    def decodeConstraints(self,constraints):
        f = Trait.decodeKeys(constraints)
        return f[0]=='true',f[3]=='true',int(f[1]),int(f[2])
    
    def encodeCommands(self,commands):
        cmds              = []
        for cmd in commands:
            # print(cmd)
            com = cmd[0] + ':' + cmd[1].replace(',',r'\,') + ':' + cmd[2]
            if cmd[2] == self.DIRECT:
                com += r'\,'+cmd[3].replace(',',r'\\,').replace(':',r'\:')
            elif cmd[2] == self.INCREMENT:
                com += r'\,'+cmd[3].replace(',',r'\\,').replace(':',r'\:')
            cmds.append(com)
        # print(cmds)
        return ','.join(cmds)

    def decodeCommands(self,commands):
        cmds = Trait.decodeKeys(commands)
        ret  = []
        for cmd in cmds:
            parts = Trait.decodeKeys(cmd,':')
            # print('parts',parts)
            if parts[-1][0] == self.DIRECT:
                parts = parts[:-1]+Trait.decodeKeys(parts[-1],',')
            if parts[-1][0] == self.INCREMENT:
                parts = parts[:-1]+Trait.decodeKeys(parts[-1],',')
            ret.append(parts)
        # print(commands,parts)
        return ret
    
    def getCommands(self):
        return self.decodeCommands(self['commands'])

    def setCommands(self,commands):
        self['commands'] = self.encodeCommands(commands)
        
    def check(self):
        assert len(self['name']) > 0,\
            f'No name given for ChangePropertyTrait'
        
        
# --------------------------------------------------------------------
class DynamicPropertyTrait(ChangePropertyTrait):
    ID = 'PROP'
    def __init__(self,
                 *commands,
                 name        = '',
                 value       = 0,
                 numeric     = False,
                 min         = 0,
                 max         = 100,
                 wrap        = False,
                 description = ''):
        '''Commands are

            - menu
            - key
            - Type (only 'P' for now)
            - Expression
        '''
        super(DynamicPropertyTrait,self).__init__(*commands,
                                                  numeric = numeric,
                                                  min     = min,
                                                  max     = max,
                                                  wrap    = wrap)
        # print(commands,'Name',name)
        self.setType(name        = name,
                     constraints = self._constraints,
                     commands    = self._commands,
                     description = description)
        self.setState(value=value)

    
Trait.known_traits.append(DynamicPropertyTrait)

#
# EOF
#
# ====================================================================
# From traits/globalproperty.py

# --------------------------------------------------------------------
class GlobalPropertyTrait(ChangePropertyTrait):
    # The real value of CURRENT_ZONE causes problems when copying the
    # trait, since it contains slashes.  Maybe a solition is to make
    # it a raw string with escaped slashes?  No, that's already done
    # below when setting the type.  However, the default in the Java
    # code is the CURRENT_ZONE real value, so setting this to the
    # empty string should make it be that value.
    ID = 'setprop'
    CURRENT_ZONE = 'Current Zone/Current Map/Module'
    NAMED_ZONE   = 'Named Zone'
    NAMED_MAP    = 'Named Map'
    DIRECT       = 'P'
    def __init__(self,
                 *commands,
                 name        = '',
                 numeric     = False,
                 min         = 0,
                 max         = 100,
                 wrap        = False,
                 description = '',
                 level       = CURRENT_ZONE,
                 search      = ''):
        '''Commands are

            - menu
            - key
            - Type (only 'P' for now)
            - Expression
        '''
        super(GlobalPropertyTrait,self).__init__(*commands,
                                                 numeric = numeric,
                                                 min     = min,
                                                 max     = max,
                                                 wrap    = wrap)
        self.setType(name        = name,
                     constraints = self._constraints,
                     commands    = self._commands,
                     description = description,
                     level       = level.replace('/',r'\/'),
                     search      = search)
        self.setState()

Trait.known_traits.append(GlobalPropertyTrait)

#
# EOF
#
# ====================================================================
# From traits/prototype.py

# --------------------------------------------------------------------
class PrototypeTrait(Trait):
    ID = 'prototype'
    def __init__(self,name=''):
        '''Create a prototype trait (VASSAL.counter.UsePrototype)'''
        super(PrototypeTrait,self).__init__()
        self.setType(name = name)
        self.setState(ignored = '')


Trait.known_traits.append(PrototypeTrait)

#
# EOF
#
# ====================================================================
# From traits/place.py

# --------------------------------------------------------------------
class PlaceTrait(Trait):
    ID      = 'placemark'
    STACK_TOP = 0
    STACK_BOTTOM = 1
    ABOVE = 2
    BELOW = 3

    # How the LaTeX exporter organises the units.  Format with
    # 0: the group
    # 1: the piece name 
    # SKEL_PATH = (PieceWindow.TAG +r':Counters\/'        +
    #              TabWidget.TAG   +r':Counters\/'        +
    #              PanelWidget.TAG +':{0}'         +r'\/'+
    #              ListWidget.TAG  +':{0} counters'+r'\/'+
    #              PieceSlot.TAG   +':{1}')
    @classmethod
    # @property
    def SKEL_PATH(cls):

        return (PieceWindow.TAG +r':Counters\/'        +
                TabWidget.TAG   +r':Counters\/'        +
                PanelWidget.TAG +':{0}'         +r'\/'+
                ListWidget.TAG  +':{0} counters'+r'\/'+
                PieceSlot.TAG   +':{1}')
    
    def __init__(self,
                 command         = '', # Context menu name
                 key             = '', # Context menu key
                 markerSpec      = '', # Full path in module
                 markerText      = 'null', # Hard coded message
                 xOffset         = 0,
                 yOffset         = 0,
                 matchRotation   = True,
                 afterKey        = '',
                 description     = '',
                 gpid            = '', # Set in JAVA, but with warning
                 placement       = ABOVE,
                 above           = False):
        '''Create a place marker trait (VASSAL.counter.PlaceMarker)'''
        super(PlaceTrait,self).__init__()
        self.setType(command         = command,          # Context menu name
                     key             = key,              # Context menu key
                     markerSpec      = markerSpec,
                     markerText      = markerText,
                     xOffset         = xOffset,
                     yOffset         = yOffset,
                     matchRotation   = matchRotation,
                     afterKey        = afterKey,
                     description     = description,
                     gpid            = gpid,
                     placement       = placement,
                     above           = above)
        self.setState()

Trait.known_traits.append(PlaceTrait)

# --------------------------------------------------------------------
class ReplaceTrait(PlaceTrait):
    ID = 'replace'
    def __init__(self,
                 command         = '', # Context menu name
                 key             = '', # Context menu key
                 markerSpec      = '', # Full path in module
                 markerText      = 'null', # Hard message
                 xOffset         = 0,
                 yOffset         = 0,
                 matchRotation   = True,
                 afterKey        = '',
                 description     = '',
                 gpid            = '', # Set in JAVA
                 placement       = PlaceTrait.ABOVE,
                 above           = False):
        super(ReplaceTrait,self).__init__(command         = command, 
                                          key             = key,  
                                          markerSpec      = markerSpec,
                                          markerText      = markerText,
                                          xOffset         = xOffset,
                                          yOffset         = yOffset,
                                          matchRotation   = matchRotation,
                                          afterKey        = afterKey,
                                          description     = description,
                                          gpid            = gpid,
                                          placement       = placement,
                                          above           = above)
    

Trait.known_traits.append(ReplaceTrait)

#
# EOF
#
# ====================================================================
# From traits/report.py

# --------------------------------------------------------------------
class ReportTrait (Trait):
    ID = 'report'
    def __init__(self,
                 *keys,
                 nosuppress = True,
                 description = '',
                 report      = '$location$: $newPieceName$ $menuCommand$ *',
                 cyclekeys   = '',
                 cyclereps   = ''):
        '''Create a report trait (VASSAL.counters.ReportActon)'''
        super(ReportTrait,self).__init__()
        esckeys = ','.join([k.replace(',',r'\,') for k in keys])
        esccycl = ','.join([k.replace(',',r'\,') for k in cyclekeys])
        escreps = ','.join([k.replace(',',r'\,') for k in cyclereps])
        
        self.setType(keys         = esckeys,
                     report       = report,
                     cycleKeys    = esccycl,
                     cycleReports = escreps,
                     description  = description,
                     nosuppress   = nosuppress)
        self.setState(cycle = -1)

Trait.known_traits.append(ReportTrait)

#
# EOF
#
# ====================================================================
# From traits/calculatedproperty.py

# --------------------------------------------------------------------
class CalculatedTrait(Trait):
    ID = 'calcProp'
    def __init__(self,name='',expression='',description=''):
        '''Define a trait that calculates a property'''
        super(CalculatedTrait,self).__init__()
        self.setType(name        = name,
                     expression  = expression,
                     description = description)
        self.setState()


Trait.known_traits.append(CalculatedTrait)

#
# EOF
#
# ====================================================================
# From traits/restrictcommand.py

# --------------------------------------------------------------------
class RestrictCommandsTrait(Trait):
    ID = 'hideCmd'
    HIDE = 'Hide'
    DISABLE = 'Disable'
    def __init__(self,
                 name          = '',
                 hideOrDisable = HIDE,
                 expression    = '',# Restrict when true
                 keys          = []):
        '''Create a layer trait (VASSAL.counter.RestrictCommands)'''
        super(RestrictCommandsTrait,self).__init__()
        encKeys = ','.join([k.replace(',',r'\,') for k in keys])
        self.setType(name          = name,
                     hideOrDisable = hideOrDisable,
                     expression    = expression,
                     keys          = encKeys)
        self.setState(state='')
    def setKeys(self,keys):
        self['keys'] = ','.join([k.replace(',',r'\,') for k in keys])
    

Trait.known_traits.append(RestrictCommandsTrait)

#
# EOF
#
# ====================================================================
# From traits/label.py

class LabelTraitCodes:
    TOP    = 't'
    BOTTOM = 'b'
    CENTER = 'c'
    LEFT   = 'l'
    RIGHT  = 'r'
    PLAIN  = 0
    BOLD   = 1
    ITALIC = 2
    
# --------------------------------------------------------------------
class LabelTrait(Trait):
    ID     = 'label'
    def __init__(self,
                 label           = None,
                 labelKey        = '',
                 menuCommand     ='Change label',
                 fontSize        = 10,
                 background      = 'none',
                 foreground      = '255,255,255',
                 vertical        = LabelTraitCodes.TOP,
                 verticalOff     = 0,
                 horizontal      = LabelTraitCodes.CENTER,
                 horizontalOff   = 0,
                 verticalJust    = LabelTraitCodes.BOTTOM,
                 horizontalJust  = LabelTraitCodes.CENTER,
                 nameFormat      = '$pieceName$ ($label$)',
                 fontFamily      = 'Dialog',
                 fontStyle       = LabelTraitCodes.PLAIN,
                 rotate          = 0,
                 propertyName    = 'TextLabel',
                 description     = '',
                 alwaysUseFormat = False):
        '''Create a label trait (can be edited property)

        Note that rotation comes last in the operations.  That is,
        `horizontal...` and `vertical...` must be specified as if the
        label is not rotated, and then rotation is applied.

        Negative vertical offset moves the label _up_. 

        '''
        super(LabelTrait,self).__init__()
        if not background or background == 'none': background = ''
        if not foreground or foreground == 'none': foreground = ''
        self.setType(labelKey		= labelKey,
                     menuCommand	= menuCommand,
                     fontSize		= fontSize,
                     background		= background,
                     foreground		= foreground,
                     vertical		= vertical,
                     verticalOff	= verticalOff,
                     horizontal		= horizontal,
                     horizontalOff	= horizontalOff,
                     verticalJust	= verticalJust,
                     horizontalJust	= horizontalJust,
                     nameFormat		= nameFormat,
                     fontFamily		= fontFamily,
                     fontStyle		= fontStyle,
                     rotate		= rotate,
                     propertyName	= propertyName,
                     description	= description,
                     alwaysUseFormat	= alwaysUseFormat)
        self.setState(label = (nameFormat if label is None else label))


Trait.known_traits.append(LabelTrait)

#
# EOF
#
# ====================================================================
# From traits/layer.py

# --------------------------------------------------------------------
class LayerTrait(Trait):
    ID = 'emb2'
    def __init__(self,
                 images       = [''],
                 newNames     = None,
                 activateName = 'Activate',
                 activateMask = CTRL,
                 activateChar = 'A',
                 increaseName = 'Increase',
                 increaseMask = CTRL,
                 increaseChar = '[',
                 decreaseName = '',
                 decreaseMask = CTRL,
                 decreaseChar  = ']',
                 resetName    = '',
                 resetKey     = '',
                 resetLevel   = 1,
                 under        = False,
                 underXoff    = 0,
                 underYoff    = 0,
                 loop         = True,
                 name         = '',
                 description  = '',
                 randomKey    = '',
                 randomName   = '',
                 follow       = False,
                 expression   = '',
                 first        = 1,
                 version      = 1, # 1:new, 0:old
                 always       = True,
                 activateKey  = key('A'),
                 increaseKey  = key('['),
                 decreaseKey  = key(']'),
                 scale        = 1.):
        '''Create a layer trait (VASSAL.counter.Embellishment)'''
        super(LayerTrait,self).__init__()
        if newNames is None and images is not None:
            newNames = ['']*len(images)
        self.setType(
            activateName        = activateName,
            activateMask        = activateMask,
            activateChar        = activateChar,
            increaseName        = increaseName,
            increaseMask        = increaseMask,
            increaseChar        = increaseChar,
            decreaseName        = decreaseName,
            decreaseMask        = decreaseMask,
            decreaseChar        = decreaseChar,
            resetName           = resetName,
            resetKey            = resetKey,
            resetLevel          = resetLevel,
            under               = under,
            underXoff           = underXoff,
            underYoff           = underYoff,
            images              = ','.join(images),
            newNames            = ','.join(newNames),
            loop                = loop,
            name                = name,
            randomKey           = randomKey,
            randomName          = randomName,
            follow              = follow,
            expression          = expression,
            first               = first,
            version             = version,
            always              = always,
            activateKey         = activateKey,
            increaseKey         = increaseKey,
            decreaseKey         = decreaseKey,
            description         = description,
            scale               = scale)
        self.setState(level=1)

    def getImages(self):
        return self['images'].split(',')

    def setImages(self,*images):
        self['images'] = ','.join(images)
        
    def getNames(self):
        return self['newNames'].split(',')

    def setNames(self,*names):
        images   = self.getImages()
        newNames = ','.join(names+['']*(len(images)-len(names)))
        self['newNames'] = newNames

    def getLevel(self):
        return self['level']

    def setLevel(self,level):
        self['level'] = level
                            

Trait.known_traits.append(LayerTrait)

#
# EOF
#
# ====================================================================
# From traits/globalcommand.py

# --------------------------------------------------------------------
class GlobalCommandTrait(Trait):
    ID = 'globalkey'
    def __init__(self,
                 commandName   = '',
                 key           = '', # Command received
                 globalKey     = '', # Command to send to targets
                 properties    = '', # Filter target on this expression
                 ranged        = False,
                 range         = 1,
                 reportSingle  = True,
                 fixedRange    = True,
                 rangeProperty = '',
                 description   = '',
                 deckSelect    = '-1',
                 target        = ''):
        '''Create a global key command in piece.  This sends a key
        command to near-by counters, as if invoked by a global key
        (module window) command.

        This is _different_ from GlobalHotkeyTrait in that this does
        not invoke and actual module window global hot key, but rather
        sends the command directly to a near-by counter (just how
        close depends on the range or rangeProperty parameter).

        The `deckSelect` select either _all_ (value -1) or specified
        number of pieces from deck.
        
        (VASSAL.counters.CounterGlobalKeyCommand)

        '''
        self.setType(commandName   = commandName,
                     key           = key,
                     globalKey     = globalKey,
                     properties    = properties,
                     ranged        = ranged,
                     range         = range,
                     reportSingle  = reportSingle,
                     fixedRange    = fixedRange,
                     rangeProperty = rangeProperty,
                     description   = description,
                     deckSelect    = deckSelect,
                     target        = target)
        self.setState()
        
Trait.known_traits.append(GlobalCommandTrait)

#
# EOF
#
# ====================================================================
# From traits/globalhotkey.py

# --------------------------------------------------------------------
class GlobalHotkeyTrait(Trait):
    ID = 'globalhotkey'
    def __init__(self,
                 name          = '', # Command received
                 key           = '', # Command key received
                 globalHotkey  = '', # Key to send
                 description   = ''):
        '''Create a global key command in piece
        (VASSAL.counters.GlobalHotkey)'''
        self.setType(name          = name,
                     key           = key,
                     globalHotkey  = globalHotkey,
                     description   = description)
        self.setState()
        
Trait.known_traits.append(GlobalHotkeyTrait)

#
# EOF
#
# ====================================================================
# From traits/nostack.py

# --------------------------------------------------------------------
class NoStackTrait(Trait):
    ID                    = 'immob'
    NORMAL_SELECT         = ''
    SHIFT_SELECT          = 'i'
    CTRL_SELECT           = 't'
    ALT_SELECT            = 'c'
    NEVER_SELECT          = 'n'
    NORMAL_BAND_SELECT    = ''
    ALT_BAND_SELECT       = 'A'
    ALT_SHIFT_BAND_SELECT = 'B'
    NEVER_BAND_SELECT     = 'Z'
    NORMAL_MOVE           = 'N'
    SELECT_MOVE           = 'I'
    NEVER_MOVE            = 'V'
    NORMAL_STACK          = 'L'
    NEVER_STACK           = 'R'
    IGNORE_GRID           = 'g'
    def __init__(self,
                 select      = NORMAL_SELECT,
                 bandSelect  = NORMAL_BAND_SELECT,
                 move        = NORMAL_MOVE,
                 canStack    = False,
                 ignoreGrid  = False,
                 description = ''):
        '''No stacking trait

        (VASSAL.counter.Immobilized)
        '''
        selectionOptions = (select +
                            (self.IGNORE_GRID if ignoreGrid else '') +
                            bandSelect)
        movementOptions  = move
        stackingOptions  = self.NORMAL_STACK if canStack else self.NEVER_STACK
                 
        '''Create a mark trait (static property)'''
        super(NoStackTrait,self).__init__()
        
        self.setType(selectionOptions = selectionOptions,
                     movementOptions  = movementOptions,
                     stackingOptions  = stackingOptions,
                     description      = description)
        self.setState()


Trait.known_traits.append(NoStackTrait)

#
# EOF
#
# ====================================================================
# From traits/deselect.py

# --------------------------------------------------------------------
class DeselectTrait(Trait):
    ID = 'deselect'
    THIS = 'D' # Deselect only this piece
    ALL  = 'A' # Deselect all pieces 
    ONLY = 'S' # Select this piece only
    def __init__(self,
                 command     = '',
                 key         = '',
                 description = '',
                 unstack     = False,
                 deselect    = THIS):
        '''Create a deselect trait'''
        super(DeselectTrait,self).__init__()
        self.setType(command     = command,
                     key         = key,
                     description = description,
                     unstack     = unstack,
                     deselect    = deselect)
        self.setState()


Trait.known_traits.append(DeselectTrait)

#
# EOF
#
# ====================================================================
# From traits/restrictaccess.py

# --------------------------------------------------------------------
class RestrictAccessTrait(Trait):
    ID = 'restrict'
    def __init__(self,
                 sides         = [],
                 byPlayer      = False,
                 noMovement    = True,
                 description   = '',
                 owner         = '',):
        '''Create a layer trait (VASSAL.counter.Restricted)'''
        super(RestrictAccessTrait,self).__init__()
        encSides = ','.join(sides)
        self.setType(sides         = encSides,
                     byPlayer      = byPlayer,
                     noMovement    = noMovement,
                     description   = description)
        self.setState(owner=owner)

Trait.known_traits.append(RestrictAccessTrait)

#
# EOF
#
# ====================================================================
# From traits/rotate.py

# --------------------------------------------------------------------
class RotateTrait(Trait):
    ID = 'rotate'
    def __init__(self,
                 nangles          = 6,
                 rotateCWKey      = key(']'),
                 rotateCCWKey     = key('['),
                 rotateCW         = 'Rotate CW',
                 rotateCCW        = 'Rotate CCW',
                 rotateFree       = 'Rotate ...',
                 rotateFreeKey    = key(']'),
                 rotateRndKey     = '',
                 rotateRnd        = '',
                 name             = 'Rotate',
                 description      = 'Rotate piece',
                 rotateDirectKey  = '',
                 rotateDirect     = '',
                 directExpression = '',
                 directIsFacing   = True,
                 angle            = 0):
        '''Create a Rotate trait'''
        super(RotateTrait,self).__init__()
        if nangles == 1:
            self.setType(nangles          = nangles,
                         rotateKey        = rotateFreeKey,
                         rotate           = rotateFree,
                         rotateRndKey     = rotateRndKey,
                         rotateRnd        = rotateRnd,
                         name             = name,
                         description      = description,
                         rotateDirectKey  = rotateDirectKey,
                         rotateDirect     = rotateDirect,
                         directExpression = directExpression,
                         directIsFacing   = directIsFacing)
        else:
            self.setType(nangles          = nangles,
                         rotateCWKey      = rotateCWKey,
                         rotateCCWKey     = rotateCCWKey,
                         rotateCW         = rotateCW,
                         rotateCCW        = rotateCCW,
                         rotateRndKey     = rotateRndKey,
                         rotateRnd        = rotateRnd,
                         name             = name,
                         description      = description,
                         rotateDirectKey  = rotateDirectKey,
                         rotateDirect     = rotateDirect,
                         directExpression = directExpression,
                         directIsFacing   = directIsFacing)
            
        self.setState(angle = int(angle) if nangles > 1 else float(angle))

Trait.known_traits.append(RotateTrait)

#
# EOF
#
# ====================================================================
# From traits/stack.py

# --------------------------------------------------------------------
class StackTrait(Trait):
    ID = 'stack'
    def __init__(self,
                 board     = '',
                 x         = '',  
                 y         = '',  
                 pieceIds  = [],
                 layer     = -1): 
        '''Create a stack trait in a save file'''
        self.setType()       # NAME
        # print('Piece IDs:',pieceIds)
        self.setState(board      = board,
                      x          = x,
                      y          = y,
                      pieceIds   = ';'.join([str(p) for p in pieceIds]),
                      layer      = f'@@{layer}')
        
Trait.known_traits.append(StackTrait)

#
# EOF
#
# ====================================================================
# From traits/mark.py

# --------------------------------------------------------------------
class MarkTrait(Trait):
    ID = 'mark'
    def __init__(self,name='',value=''):
        '''Create a mark trait (static property)'''
        super(MarkTrait,self).__init__()
        self.setType(name = name)
        self.setState(value = value)


Trait.known_traits.append(MarkTrait)

#
# EOF
#
# ====================================================================
# From traits/mask.py

# --------------------------------------------------------------------
# Inset
# obs;88,130;ag_hide_1.png;Reveal;I;?;sides:Argentine;Peek;;true;;
# obs;88,130;ag_hide_1.png;Reveal;I;?;side:Argentine;;;true;;
#
# Peek
# obs;88,130;ag_hide_1.png;Reveal;P89,130;?;sides:Argentine;Peek;;true;;
#
# Image
#
class MaskTrait(Trait):
    ID = 'obs'
    INSET = 'I'
    BACKGROUND = 'B'
    PEEK = 'P'
    IMAGE = 'G'
    INSET2 = '2'
    PLAYER = 'player:'
    SIDE = 'side:'
    SIDES = 'sides:'
    def __init__(self,
                 keyCommand   = '',
                 imageName    = '',
                 hideCommand  = '',
                 displayStyle = '',
                 peekKey      = '',
                 ownerImage   = '',
                 maskedName   = '?',
                 access       = '',#?
                 peekCommand  = '',
                 description  = '',
                 autoPeek     = True,
                 dealKey      = '',
                 dealExpr     = ''):
        '''Create a masking trait'''
        super(MaskTrait,self).__init__()
        disp = displayStyle
        if displayStyle == self.PEEK:
            disp += peekKey
        elif displayStyle == self.IMAGE:
            disp += ownerImage
            
        acc = self.PLAYER
        if isinstance(access,list):
            acc = self.SIDES + ':'.join(access)
        elif access.startswith('player'):
            acc = self.PLAYER
        elif access.startswith('side'):
            acc = self.SIDE
                
        self.setType(keyCommand   = keyCommand,
                     imageImage   = imageName,
                     hideCommand  = hideCommand,
                     displayStyle = disp,
                     maskedName   = maskedName,
                     access       = acc, # ?
                     peekCommand  = peekCommand,
                     description  = description,
                     autoPeek     = autoPeek,
                     dealKey      = dealKey,
                     dealExpr     = dealExpr)
        self.setState(value='null')

    @classmethod
    def peekDisplay(cls,key):#Encoded key
        return cls.PEEK + key
    
    @classmethod
    def peekImage(cls,ownerImage):
        return cls.IMAGE + ownerImage

    @classmethod
    def sides(cls,*names):
        return cls.SIDES+':'.join(names)

Trait.known_traits.append(MaskTrait)

#
# EOF
#
# ====================================================================
# From traits/trail.py

# --------------------------------------------------------------------
class TrailTrait(Trait):
    ID = 'footprint'
    def __init__(self,
                 key             = key('T'),
                 name            = 'Movement Trail',
                 localVisible    = False, # Start on
                 globalVisible   = True, # Visible to all players
                 radius          = 10,
                 fillColor       = rgb(255,255,255),
                 lineColor       = rgb(0,0,0),
                 activeOpacity   = 100,
                 inactiveOpacity = 50,
                 edgesBuffer     = 20,
                 displayBuffer   = 30,
                 lineWidth       = 5,
                 turnOn          = key(NONE,0)+',wgTrailsOn',
                 turnOff         = key(NONE,0)+',wgTrailsOff',
                 reset           = '',
                 description     = 'Enable or disable movement trail'):        
        ''' Create a movement trail trait ( VASSAL.counters.Footprint)'''
        super(TrailTrait,self).__init__()
        lw = (lineWidth
              if isinstance(lineWidth,str) and lineWidth.startswith('{') else
              int(lineWidth))
        ra = (radius
              if isinstance(radius,str) and radius.startswith('{') else
              int(radius))
        
        self.setType(key               = key,# ENABLE KEY
                     name              = name,# MENU 
                     localVisible      = localVisible,# LOCAL VISABLE
                     globalVisible     = globalVisible,# GLOBAL VISABLE
                     radius            = ra,# RADIUS
                     fillColor         = fillColor,# FILL COLOR
                     lineColor         = lineColor,# LINE COLOR 
                     activeOpacity     = activeOpacity,# ACTIVE OPACITY
                     inactiveOpacity   = inactiveOpacity,# INACTIVE OPACITY
                     edgesBuffer       = edgesBuffer,# EDGES BUFFER
                     displayBuffer     = displayBuffer,# DISPLAY BUFFER
                     lineWidth         = lw,# LINE WIDTH 
                     turnOn            = turnOn,# TURN ON KEY
                     turnOff           = turnOff,# TURN OFF KEY
                     reset             = reset,# RESET KEY
                     description       = description)       # DESC
        self.setState(isGlobal  = False,
                      map       = '',
                      points    = 0,     # POINTS (followed by [; [X,Y]*]
                      init      = False) 

Trait.known_traits.append(TrailTrait)

#
# EOF
#
# ====================================================================
# From traits/delete.py

# --------------------------------------------------------------------
class DeleteTrait(Trait):
    ID = 'delete'
    def __init__(self,
                 name   = 'Delete',
                 key = key('D')):
        '''Create a delete trait (VASSAL.counters.Delete)'''
        super(DeleteTrait,self).__init__()
        self.setType(name  = name,
                     key   = key,
                     dummy = '')
        self.setState()

Trait.known_traits.append(DeleteTrait)

#
# EOF
#
# ====================================================================
# From traits/sendto.py

# --------------------------------------------------------------------
class SendtoTrait(Trait):
    ID = 'sendto'
    LOCATION = 'L'
    ZONE     = 'Z'
    REGION   = 'R'
    GRID     = 'G'
    COUNTER  = 'A'
    def __init__(self,
                 mapName     = '',
                 boardName   = '',
                 name        = '',
                 key         = key('E'),
                 restoreName = 'Restore',
                 restoreKey  = key('R'),
                 x           = 200,# Location
                 y           = 200,# Location
                 xidx        = 0,  # All - extra x
                 yidx        = 0,  # All - extra y
                 xoff        = 1,  # All - factor on xidx
                 yoff        = 1,  # All - factor on yidx
                 description = '',
                 destination = LOCATION,
                 zone        = '',  # Zone and region - expression
                 region      = '',  # Region - expression
                 expression  = '',  # Counter - expression?
                 position    = ''): # Grid - Fixed
        '''Create a send to trait (VASSAL.counter.SendToLocation)'''
        self.setType(name           = name,# NAME
                     key            = key,# KEY , MODIFIER
                     mapName        = mapName,# MAP
                     boardName      = boardName,# BOARD
                     x              = x,
                     y              = y,# X ; Y
                     restoreName    = restoreName,# BACK
                     restoreKey     = restoreKey,# KEY , MODIFIER
                     xidx           = xidx,
                     yidx           = yidx,# XIDX ; YIDX
                     xoff           = xoff,
                     yoff           = yoff,# XOFF ; YOFF
                     description    = description,# DESC
                     destination    = destination,# DEST type
                     zone           = zone,# ZONE
                     region         = region,# REGION
                     expression     = expression,# EXPRESSION
                     position       = position)                   # GRIDPOS
        self.setState(backMap = '', backX = '', backY = '')

Trait.known_traits.append(SendtoTrait)

#
# EOF
#
# ====================================================================
# From traits/moved.py

# --------------------------------------------------------------------
class MovedTrait(Trait):
    ID = 'markmoved'
    def __init__(self,
                 image      = 'moved.gif',
                 xoff       = 36,
                 yoff       = -38,
                 name       = 'Mark moved',
                 key        = key('M'),
                 dummy      = ''  # Description
                 # ignoreSame = True
                 ):
        '''Create a moved trait (VASSAL.counters.MovementMarkable)'''
        super(MovedTrait,self).__init__()
        self.setType(image    = image,
                     xoff     = xoff,
                     yoff     = yoff,
                     name     = name,
                     key      = key,
                     dummy    = dummy, # Description
                     # ignoreSame = ignoreSame
                     )
        self.setState(moved = False)

Trait.known_traits.append(MovedTrait)

#
# EOF
#
# ====================================================================
# From traits/skel.py


#
# EOF
#
# ====================================================================
# From traits/submenu.py

# --------------------------------------------------------------------
class SubMenuTrait(Trait):
    ID = 'submenu'
    def __init__(self,
                 subMenu     = '',  # Title
                 keys        = [],  # Keys
                 description = ''):
        '''Create a sub menu (VASSAL.counters.SubMenu)'''
        self.setType(subMenu     = subMenu,   # CLONEKEY
                     keys        = ','.join([k.replace(',',r'\,')
                                             for k in keys]),
                     description = description)
        self.setState() # PROPERTY COUNT (followed by [; KEY; VALUE]+)
    def setKeys(self,keys):
        '''Set the keys'''
        self['keys'] = ','.join([k.replace(',',r'\,') for k in keys])
        
Trait.known_traits.append(SubMenuTrait)

#
# EOF
#
# ====================================================================
# From traits/basic.py

# --------------------------------------------------------------------
class BasicTrait(Trait):
    ID = 'piece'
    def __init__(self,
                 name      = '',
                 filename  = '',  # Can be empty
                 gpid      = '',  # Can be empty
                 cloneKey  = '',  # Deprecated
                 deleteKey = ''): # Deprecated
        '''Create a basic unit (VASSAL.counters.BasicPiece)'''
        self.setType(cloneKey  = cloneKey,   # CLONEKEY
                     deleteKey = deleteKey,  # DELETEKEY
                     filename  = filename,   # IMAGE  
                     name      = name)       # NAME
        self.setState(map        = 'null', # MAPID (possibly 'null')
                      x          = 0,
                      y          = 0,
                      gpid       = gpid,
                      properties = 0) # PROPERTY COUNT (followed by [; KEY; VALUE]+)

    def getProperties(self):
        n = int(self._state[4])
        return {k: v for k, v in zip(self._state[5::2],
                                     self._state[6::2])}
        
Trait.known_traits.append(BasicTrait)

#
# EOF
#
# ====================================================================
# From traits/trigger.py

# --------------------------------------------------------------------
class TriggerTrait(Trait):
    ID      = 'macro'
    WHILE   = 'while'
    UNTIL   = 'until'
    COUNTED = 'counted' # - Always one "do ... while"
    def __init__(self,
                 name            = '',
                 command         = '', # Context menu name
                 key             = '', # Context menu key
                 property        = '', # Enable/Disable
                 watchKeys       = [],
                 actionKeys      = [], # What to do
                 loop            = False,
                 preLoop         = '', # Key
                 postLoop        = '', # Key
                 loopType        = COUNTED, # Loop type
                 whileExpression = '',
                 untilExpression = '',
                 count           = 0,
                 index           = False,
                 indexProperty   = '',
                 indexStart      = '',
                 indexStep       = ''):
        '''Create a layer trait (VASSAL.counter.Trigger)'''
        super(TriggerTrait,self).__init__()
        encWKeys = Trait.encodeKeys(watchKeys, ',')
        encAKeys = Trait.encodeKeys(actionKeys,',')
        self.setType(name            = name,            
                     command         = command,          # Context menu name
                     key             = key,              # Context menu key
                     property        = property,         # Enable/Disable
                     watchKeys       = encWKeys,       
                     actionKeys      = encAKeys,         # What to do
                     loop            = loop,            
                     preLoop         = preLoop,          # Key
                     postLoop        = postLoop,         # Key
                     loopType        = loopType,         # Loop type
                     whileExpression = whileExpression, 
                     untilExpression = untilExpression, 
                     count           = count,           
                     index           = index,           
                     indexProperty   = indexProperty,   
                     indexStart      = indexStart,      
                     indexStep       = indexStep)       
        self.setState(state='')

    def getActionKeys(self):
        return Trait.decodeKeys(self['actionKeys'],',')
    
    def getWatchKeys(self):
        return Trait.decodeKeys(self['watchKeys'],',')
    
    def setActionKeys(self,keys):
        self['actionKeys'] = Trait.encodeKeys(keys,',')
        
    def setWatchKeys(self,keys):
        self['watchKeys'] = Trait.encodeKeys(keys,',')
        
        

Trait.known_traits.append(TriggerTrait)

#
# EOF
#
# ====================================================================
# From traits/nonrect.py

# --------------------------------------------------------------------
class NonRectangleTrait(Trait):
    ID      = 'nonRect2'
    CLOSE   = 'c'
    MOVETO  = 'm'
    LINETO  = 'l'
    CUBICTO = 'l'
    QUADTO  = 'l'
    def __init__(self,
                 scale    = 1.,
                 filename = '',
                 path     = [],
                 image    = None):
        '''Create a NonRectangle trait (static property)'''
        super(NonRectangleTrait,self).__init__()
        l = []
        if len(filename) > 0:
            l.append(f'n{filename}')

        if len(path) <= 0:
            path = self.getShape(image)

        if len(path) > 0:
            # print(path)
            l += [f'{p[0]},{int(p[1])},{int(p[2])}' if len(p) > 2 else p
                  for p in path]
    
        self.setType(scale = scale,
                     code  = ','.join(l))
        self.setState()

    @classmethod
    def getShape(cls,buffer):
        if buffer is None:
            return []

        from io import BytesIO

        image = buffer
        if image[:5] == b'<?xml':
            from cairosvg import svg2png
            image = svg2png(image)

        from PIL import Image

        code = []
        with Image.open(BytesIO(image)) as img:
            alp = img.getchannel('A') # Alpha channel
            # Find least and largest non-transparent pixel in each row
            rows  = []
            w     = alp.width
            h     = alp.height
            bb    = alp.getbbox()
            for r in range(bb[1],bb[3]):
                ll, rr = bb[2], bb[0]
                for c in range(bb[0],bb[2]):
                    if alp.getpixel((c,r)) != 0:
                        ll = min(c,ll)
                        rr = max(c,rr)
                rows += [[r-h//2,ll-w//2,rr-w//2]]
                    
            # Now produce the code - we start with the top line
            code = [(cls.MOVETO,rows[0][1],rows[0][0]-1),
                    (cls.LINETO,rows[0][2],rows[0][0]-1)]
            
            # Now loop  down right side of image
            for c in rows:
                last = code[-1]
                if last[1] != c[2]:
                    code += [(cls.LINETO, c[2], last[2])]
                code += [(cls.LINETO, c[2], c[0])]
                
            # Now loop up left side of image
            for c in rows[::-1]:
                last = code[-1]
                if last[1] != c[1]:
                    code += [(cls.LINETO,c[1],last[2])]
                code += [(cls.LINETO,c[1],c[0])]

            # Terminate with close
            code += [(cls.CLOSE)]

        return code


Trait.known_traits.append(NonRectangleTrait)

#
# EOF
#
# ====================================================================
# From traits/click.py

# --------------------------------------------------------------------
class ClickTrait(Trait):
    ID = 'button'
    def __init__(self,
                 key         = '',
                 x           = 0,
                 y           = 0,
                 width       = 0,
                 height      = 0,
                 description = '',
                 context     = False,
                 whole       = True,
                 version     = 1,
                 points      = []):
        '''Create a click trait (static property)'''
        super(ClickTrait,self).__init__()
        self.setType(key          = key,
                     x            = x,
                     y            = y,
                     width        = width,
                     height       = height,
                     description  = description,
                     context      = context,
                     whole        = whole,
                     version      = version,
                     npoints      = len(points),
                     points       = ';'.join([f'{p[0]};{p[1]}'
                                              for p in points]))            
        self.setState()


Trait.known_traits.append(ClickTrait)

#
# EOF
#
# ====================================================================
# From traits/mat.py


class MatTrait(Trait):
    ID = 'mat'

    def __init__(self,
                 name = 'Mat',
                 description = ''):
        self.setType(name        = name,
                     description = description)
        self.setState(content='0')

    def setContent(self,*args):
        # Not sure this is correct 
        self.setState(content=str(len(args))+';'+';'.joint(args))


Trait.known_traits.append(MatTrait)
	        
#
# EOF
#
# ====================================================================
# From traits/cargo.py

class CargoTrait(Trait):
    ID = 'matPiece'
    NO_MAT = 'noMat'

    def __init__(self,
                 description = '',
                 maintainRelativeFacing = True,
                 detectionDistanceX     = 0,
                 detectionDistanceY     = 0,
                 attachKey              = '',
                 detachKey              = ''):
        self.setType(description            = description,
                     maintainRelativeFacing = maintainRelativeFacing,
                     detectionDistanceX     = detectionDistanceX,
                     detectionDistanceY     = detectionDistanceY,
                     attachKey              = attachKey,
                     detachKey              = detachKey)
        self.setState(mat = CargoTrait.NO_MAT)

Trait.known_traits.append(CargoTrait)
        
#
# EOF
#
# ====================================================================
# From traits/movefixed.py


class MoveFixedTrait(Trait):
    ID = 'translate'

    def __init__(self,
                 command        = '',   # menu command,
                 key            = '',   # Hotkey or command
                 dx             = 0,    # X distance (int or expr))
                 dy             = 0,    # Y distance (int or expr))
                 stack          = False,# Move entire stack
                 xStepFactor    = 0,    # Factor on X offset (int or expr)
                 yStepFactor    = 0,    # Factor on Y offset (int or expr)
                 xStep          = 0,    # X offset (int or expr)
                 yStep          = 0,    # Y offset (int or expr)
                 description    = '',   # str 
                 ):
        '''Move a fixed distance.

           x' = dx + xStepFactor * xStep 
           y' = dy + yStepFactor * yStep 

        If piece can rotate, and this is trait is given _after_ (more
        recent in the traits list), then the piece will move according
        to the direction faced. If given _before_ (later in the traits list),
        then the move is relative  to the current map. 
        
        (VASSAL.counters.Translate)

        '''
        self.setType(command     = command,
                     key         = key,
                     dx          = dx,
                     dy          = dy,
                     stack       = stack,
                     xStepFactor = xStepFactor,
                     yStepFactor = yStepFactor,
                     xStep       = xStep,
                     yStep       = yStep,
                     description = description)
        self.setState()


Trait.known_traits.append(MoveFixedTrait)
#
# EOF
#
# ====================================================================
# From traits/sheet.py

# --------------------------------------------------------------------
class SheetTrait(Trait):
    ID             = 'propertysheet'
    EVERY_KEY_TEXT = 'Every Keystroke'
    APPLY_TEXT     = 'Apply Button or Enter Key'
    CLOSE_TEXT     = 'Close Window or Enter Key'
    EVERY_KEY      = 0
    APPLY          = 1
    CLOSE          = 2
    TEXT           = 0
    AREA           = 1
    LABEL          = 2
    TICKS          = 3
    TICKS_MAX      = 4
    TICKS_VAL      = 5
    TICKS_BOTH     = 6
    SPINNER        = 7
    TYPE_DELIM     = ';'
    DEF_DELIM      = '~'
    STATE_DELIM    = '~'
    LINE_DELIM     = '|'
    VALUE_DELIM    = '/'

    @classmethod 
    def encodeState(cls,k,e):
        type = e['type']
        if type == cls.TEXT:    return f'{e["value"]}'
        if type == cls.AREA:    return f'{e["value"].replace("\n",LINE_DELIM)}'
        if type == cls.SPINNER: return f'{e["value"]}'
        if type in [cls.TICKS,cls.TICKS_MAX,cls.TICKS_VAL,cls.TICKS_BOTH]:
            try:
                val = int(e["value"])
            except:
                val = 0
            try:
                max = int(e["max"])
            except:
                max = 0
            return f'{val}{cls.VALUE_DELIM}{max}'
        return ''

    @classmethod
    def encodeDefinition(cls,rows):
        definition = cls.DEF_DELIM.join([f'{e["type"]}{k}'
                                     for k,e in rows.items()])
                                
        state      = cls.STATE_DELIM.join([self.encodeState(k,e)
                                       for k,e in rows.items()])
        return definition, state

    @classmethod
    def decodeDefinition(cls,definitions,state):
        tns  = definitions.split(cls.DEF_DELIM)
        sts  = state      .split(cls.STATE_DELIM)
        def decodeDef(d):
            try:
                type = int(d[0])
            except:
                type = cls.TEXT
            return type, d[1:]
        rows = {}
        for tn, st in zip(tns,sts):
            type, name = decodeDef(tn)
            rows[name] = { 'type': type }
            rows[name].update(cls.decodeState(name,type,st))
        return rows

    @classmethod 
    def decodeState(cls,name,type,state):
        if type == cls.TEXT:    return {'value': state}
        if type == cls.AREA:    return {'value': state.replace('|','\n') }
        if type == cls.SPINNER: return {'value': state}
        if type in [cls.TICKS,
                    cls.TICKS_MAX,
                    cls.TICKS_VAL,
                    cls.TICKS_BOTH]:
            fields = state.split(VALUE_DELIM)
            try:
                value = int(fields[0])
            except:
                value = 0
            try:
                max = int(fields[1])
            except:
                max = 0
            return {'value': value, 'max': max }
        return {}
    
    def __init__(self,
                 command         = '',
                 commit          = EVERY_KEY,
                 color           = ',,',
                 key             = '',
                 description     = '',
                 rows            = {}):
        '''Create a clone trait (VASSAL.counter.Clone)'''
        super().__init__()
        definition, state = self.encodeDefinition(rows)
        rgbcol = color.split(',')
        self.setType(definition      = definition,
                     command         = command,          # Context menu name
                     letter          = '',
                     commit          = commit,
                     red             = rgbcol[0],
                     green           = rgbcol[1],
                     blue            = rgbcol[2],
                     key             = key,              # Context menu key
                     description     = description)     
        self.setState(state=state)
        
        
    def getDefinitionState(self):
        return self.decodeDefinition(self['definition'],self['state'])

    def setDefinitionState(self,rows):
        self['definition'], self['state'] = self.encodeDefinition(rows)
    

Trait.known_traits.append(SheetTrait)

#
# EOF
#
# ====================================================================
# From traits/hide.py

# --------------------------------------------------------------------
class HideTrait(Trait):
    ID           = 'hide'
    ANY_SIDE     = 'side:'
    ANY_PLAYER   = 'player:'
    SIDES        = 'sides:'
    @classmethod
    def encodeAccess(cls,spec):
        if isinstance(spec,list) and len(spec) == 1:
            spec = spec[0]
        if isinstance(spec,str):
            if spec == cls.ANY_SIDE: return cls.ANY_SIDE
            if spec == cls.ANY_PLAYER: return cls.ANY_PLAYER
            return cls.SIDES+":"+spec
        return cls.SIDES+':'.join(spec)

    @classmethod
    def decodeAccess(cls,spec):
        if spec.startswith(cls.ANY_SIDE):   return cls.ANY_SIDE
        if spec.startswith(cls.ANY_PLAYER): return cls.ANY_PLAYER
        if spec.startswith(cls.SIDES):      return spec.split(':')[1:]
        return None
        
    def __init__(self,
                 key                   = '',
                 command               = '',
                 bgColor               = rgb(0x0,0x0,0x0),
                 access                = [],
                 transparency          = 1, # between 0 and 1
                 description           = '',
                 disableAutoReportMove = False,
                 state                 = 'null'):
        '''Create a hide trait (VASSAL.counter.Hideable)'''

        super().__init__()
        spec = self.encodeAccess(access)
        
        self.setType(key                   = key,      # Context menu key
                     command               = command,  # Context menu name
                     bgColor               = bgColor,
                     access                = spec,
                     transparency          = transparency,
                     description           = description,
                     disableAutoReportMove = disableAutoReportMove)     
        self.setState(hiddenBy = state)

    def getAccess(self):
        return self.decodeAccess(self['access'])

    def setAccess(self, access = []):
        self['access'] = self.encodeAccess(access)

        

        

Trait.known_traits.append(HideTrait)

#
# EOF
#
# ====================================================================
# From traits/retrn.py

# --------------------------------------------------------------------
class ReturnTrait(Trait):
    ID      = 'return'
    def __init__(self,
                 command         = '',
                 key             = '',
                 deckId          = '',
                 prompt          = '',
                 description     = '',
                 version         = 2,
                 select          = False, # If true, select at run-time
                 expression      = ''
                 ):
        '''Create a return trait (VASSAL.counter.ReturnToDeck)'''
        super().__init__()

        self.setType(command         = command,          # Context menu name
                     key             = key,              # Context menu key
                     deckId          = deckId,
                     prompt          = prompt,
                     description     = description,
                     version         = version,
                     select          = select,
                     expression      = expression
                     )     
        self.setState(state='')

        

Trait.known_traits.append(ReturnTrait)

#
# EOF
#
# ====================================================================
# From game.py

# --------------------------------------------------------------------
class Game(Element):
    TAG = Element.BUILD+'GameModule'
    UNIQUE = ['name']
    def __init__(self,build,node=None,
                 name            = '',
                 version         = '', 
                 ModuleOther1    = "",
                 ModuleOther2    = "",
                 VassalVersion   = "3.6.7",
                 description     = "",
                 nextPieceSlotId = 20):
        '''Create a new Game object

        Parameters
        ----------
        build : xml.dom.Document
            root note
        node : xml.dom.Node
            To read from, or None
        name : str
            Name of module
        version : str
            Version of module
        ModuleOther1 : str
            Free form string 
        ModuleOther2 : str
            Free form string
        VassalVersion : str
            VASSAL version this was created for
        description : str
            Speaks volumes
        nextPieceSlotId : int
            Starting slot ID.
        '''
        super(Game,self).__init__(build, self.TAG,
                                  node            = node,
                                  name            = name,
                                  version         = version,
                                  ModuleOther1    = ModuleOther1,
                                  ModuleOther2    = ModuleOther2,
                                  VassalVersion   = VassalVersion,
                                  description     = description,
                                  nextPieceSlotId = nextPieceSlotId)
    def nextPieceSlotId(self):
        '''Increment next piece slot ID'''
        ret = int(self.getAttribute('nextPieceSlotId'))
        self.setAttribute('nextPieceSlotId',str(ret+1))
        return ret
    #
    def addBasicCommandEncoder(self,**kwargs):
        '''Add a `BasicCommandEncoder` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : BasicCommandEncoder
            The added element
        '''
        return self.add(BasicCommandEncoder,**kwargs)
    def addGlobalTranslatableMessages(self,**kwargs):
        '''Add a `GlobalTranslatableMessages` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : GlobalTranslatableMessages
            The added element
        '''
        return self.add(GlobalTranslatableMessages,**kwargs)
    def addPlayerRoster(self,**kwargs):
        '''Add a `PlayerRoster` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : PlayerRoster
            The added element
        '''
        return self.add(PlayerRoster,**kwargs)
    def addChessClock(self,**kwargs):
        '''Add a `ChessClockControl` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : PlayerRoster
            The added element
        '''
        return self.add(ChessClockControl,**kwargs)
    def addLanguage(self,**kwargs):
        '''Add a `Language` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Language
            The added element
        '''
        return self.add(Language,**kwargs)
    def addChatter(self,**kwargs):
        '''Add a `Chatter` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Chatter
            The added element
        '''
        return self.add(Chatter,**kwargs)
    def addKeyNamer(self,**kwargs):
        '''Add a `KeyNamer` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : KeyNamer
            The added element
        '''
        return self.add(KeyNamer,**kwargs)
    def addNotes(self,**kwargs):
        '''Add a `Notes` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Notes
            The added element
        '''
        return self.add(Notes,**kwargs)
    def addLanguage(self,**kwargs):
        '''Add a `Language` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Language
            The added element
        '''
        return self.add(Language,**kwargs)
    def addChatter(self,**kwargs):
        '''Add a `Chatter` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Chatter
            The added element
        '''
        return self.add(Chatter,**kwargs)
    def addKeyNamer(self,**kwargs):
        '''Add a `KeyNamer` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : KeyNamer
            The added element
        '''
        return self.add(KeyNamer,**kwargs)
    def addGlobalProperties(self,**kwargs):
        '''Add a `GlobalProperties` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : GlobalProperties
            The added element
        '''
        return self.add(GlobalProperties,**kwargs)
    def addGlobalOptions(self,**kwargs):
        '''Add a `GlobalOptions` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : GlobalOptions
            The added element
        '''
        return self.add(GlobalOptions,**kwargs)
    def addTurnTrack(self,**kwargs):
        '''Add a `TurnTrack` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : TurnTrack
            The added element
        '''
        return self.add(TurnTrack,**kwargs)
    def addDocumentation(self,**kwargs):
        '''Add a `Documentation` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Documentation
            The added element
        '''
        return self.add(Documentation,**kwargs)
    def addPrototypes(self,**kwargs):
        '''Add a `Prototypes` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Prototypes
            The added element
        '''
        return self.add(Prototypes,**kwargs)
    def addPieceWindow(self,**kwargs):
        '''Add a `PieceWindow` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : PieceWindow
            The added element
        '''
        return self.add(PieceWindow,**kwargs)
    def addChartWindow(self,**kwargs):
        '''Add a `ChartWindow` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : ChartWindow
            The added element
        '''
        return self.add(ChartWindow,**kwargs)
    def addInventory(self,**kwargs):
        '''Add a `Inventory` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Inventory
            The added element
        '''
        return self.add(Inventory,**kwargs)
    def addMap(self,**kwargs):
        '''Add a `Map` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Map
            The added element
        '''
        return self.add(Map,**kwargs)
    def addDiceButton(self,**kwargs):
        '''Add a `DiceButton` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : DiceButton
            The added element
        '''
        return self.add(DiceButton,**kwargs)
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
    def addGameMassKey(self,**kwargs):
        '''Add a `GameMassKey` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : GameMassKey
            The added element
        '''
        return self.add(GameMassKey,**kwargs)
    def addStartupMassKey(self,**kwargs):
        '''Add a `StartupMassKey` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : StartupMassKey
            The added element
        '''
        return self.add(StartupMassKey,**kwargs)
    def addMenu(self,**kwargs):
        '''Add a `Menu` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Menu
            The added element
        '''
        return self.add(Menu,**kwargs)
    def addSymbolicDice(self,**kwargs):
        '''Add a `SymbolicDice` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : SymbolicDice
            The added element
        '''
        return self.add(SymbolicDice,**kwargs)

    def addFolder(self,**kwargs):
        '''Add a `ModuleFolder` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : ModuleFolder
            The added element
        '''
        return self.add(ModuleFolder,**kwargs)
    
    
    # ----------------------------------------------------------------
    def getGlobalProperties(self,single=True):
        '''Get all or a sole `GlobalPropertie` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `GlobalPropertie` child, otherwise fail.
            If `False` return all `GlobalPropertie` children in this element
        
        Returns
        -------
        children : list
            List of `GlobalPropertie` children (even if `single=True`)
        '''
        return self.getAllElements(GlobalProperties,single)
    def getBasicCommandEncoder(self,single=True):
        '''Get all or a sole `Ba` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `Ba` child, otherwise fail.
            If `False` return all `Ba` children in this element
        
        Returns
        -------
        children : list
            List of `Ba` children (even if `single=True`)
        '''
        return self.getAllElements(BasicCommandEncoder,single)
    def getGlobalTranslatableMessages(self,single=True):
        '''Get all or a sole `GlobalTranslatableMessage` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `GlobalTranslatableMessage` child, otherwise fail.
            If `False` return all `GlobalTranslatableMessage` children in this element
        
        Returns
        -------
        children : list
            List of `GlobalTranslatableMessage` children (even if `single=True`)
        '''
        return self.getAllElements(GlobalTranslatableMessages,single)
    def getLanguages(self,single=False):
        '''Get all or a sole `Language` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `Language` child, otherwise fail.
            If `False` return all `Language` children in this element
        
        Returns
        -------
        children : list
            List of `Language` children (even if `single=True`)
        '''
        return self.getAllElements(Language,single)
    def getChessClocks(self,asdict=False):
        '''Get all or a sole `Language` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `Language` child, otherwise fail.
            If `False` return all `Language` children in this element
        
        Returns
        -------
        children : list
            List of `Language` children (even if `single=True`)
        '''
        return self.getElementsByKey(ChessClockControl,'name',asdict)
    def getChatter(self,single=True):
        '''Get all or a sole `Chatter` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `Chatter` child, otherwise fail.
            If `False` return all `Chatter` children in this element
        
        Returns
        -------
        children : list
            List of `Chatter` children (even if `single=True`)
        '''
        return self.getAllElements(Chatter,single)
    def getKeyNamer(self,single=True):
        '''Get all or a sole `KeyNamer` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `KeyNamer` child, otherwise fail.
            If `False` return all `KeyNamer` children in this element
        
        Returns
        -------
        children : list
            List of `KeyNamer` children (even if `single=True`)
        '''
        return self.getAllElements(KeyNamer,single)
    def getDocumentation(self,single=True):
        '''Get all or a sole `Documentation` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `Documentation` child, otherwise fail.
            If `False` return all `Documentation` children in this element
        
        Returns
        -------
        children : list
            List of `Documentation` children (even if `single=True`)
        '''
        return self.getAllElements(Documentation,single)
    def getPrototypes(self,single=True):
        '''Get all or a sole `Prototypes` (i.e., the containers of
        prototypes, not a list of actual prototypes) element(s) from
        this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `Prototypes` child, otherwise fail.
            If `False` return all `Prototypes` children in this element
        
        Returns
        -------
        children : list
            List of `Prototype` children (even if `single=True`)

        '''
        return self.getAllElements(Prototypes,single)
    def getPlayerRoster(self,single=True):
        '''Get all or a sole `PlayerRo` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `PlayerRo` child, otherwise fail.
            If `False` return all `PlayerRo` children in this element
        
        Returns
        -------
        children : list
            List of `PlayerRo` children (even if `single=True`)
        '''
        return self.getAllElements(PlayerRoster,single)
    def getGlobalOptions(self,single=True):
        '''Get all or a sole `GlobalOption` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `GlobalOption` child, otherwise fail.
            If `False` return all `GlobalOption` children in this element
        
        Returns
        -------
        children : list
            List of `GlobalOption` children (even if `single=True`)
        '''
        return self.getAllElements(GlobalOptions,single)
    def getInventories(self,asdict=True):
        '''Get all Inventorie element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Inventorie` elements.  If `False`, return a list of all Inventorie` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `Inventorie` children
        '''
        return self.getElementsByKey(Inventory,'name',asdict)
    def getPieceWindows(self,asdict=True):
        '''Get all PieceWindow element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `PieceWindow` elements.  If `False`, return a list of all PieceWindow` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `PieceWindow` children
        '''
        return self.getElementsByKey(PieceWindow,'name',asdict)
    def getChartWindows(self,asdict=True):
        '''Get all ChartWindow element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `ChartWindow` elements.  If `False`, return a list of all ChartWindow` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `ChartWindow` children
        '''
        return self.getElementsByKey(ChartWindow,'name',asdict)
    def getDiceButtons(self,asdict=True):
        '''Get all DiceButton element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `DiceButton` elements.  If `False`, return a list of all DiceButton` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `DiceButton` children
        '''
        return self.getElementsByKey(DiceButton,'name',asdict)
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
    def getNotes(self,single=True):
        '''Get all or a sole `Note` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `Note` child, otherwise fail.
            If `False` return all `Note` children in this element
        
        Returns
        -------
        children : list
            List of `Note` children (even if `single=True`)
        '''
        return self.getAllElements(Notes,single)
    def getTurnTracks(self,asdict=True):
        '''Get all TurnTrack element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `TurnTrack` elements.  If `False`, return a list of all TurnTrack` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `TurnTrack` children
        '''
        return self.getElementsByKey(TurnTrack,'name',asdict)
    def getPieces(self,asdict=False):
        '''Get all Piece element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Piece` elements.  If `False`, return a list of all Piece` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `Piece` children
        '''
        return self.getElementsByKey(PieceSlot,'entryName',asdict)
    def getCards(self,asdict=False):
        '''Get all Cards element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Piece` elements.  If `False`, return a list of all Piece` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `Piece` children
        '''
        return self.getElementsByKey(CardSlot,'entryName',asdict)
    def getSpecificPieces(self,*names,asdict=False):
        '''Get all SpecificPiece element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `SpecificPiece` elements.  If `False`, return a list of all SpecificPiece` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `SpecificPiece` children
        '''
        return self.getSpecificElements(PieceSlot,'entryName',
                                        *names,asdict=asdict)
    def getMap(self,asdict=False):
        return self.getElementsByKey(Map,'mapName',asdict)
    def getWidgetMaps(self,asdict=True):
        '''Get all WidgetMap element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `WidgetMap` elements.  If `False`, return a list of all WidgetMap` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `WidgetMap` children
        '''
        return self.getElementsByKey(WidgetMap,'mapName',asdict=asdict)
    def getMaps(self,asdict=True):
        '''Get all Map element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Map` elements.  If `False`, return a list of all Map` children.
        
        Returns
        -------
        children : dict or list
            Dictionary or list of `Map` children
        '''
        maps = self.getMap(asdict=asdict)
        wmaps = self.getWidgetMaps(asdict=asdict)
        if asdict:
            maps.update(wmaps)
        else:
            maps.extend(wmaps)
        return maps
    def getBoards(self,asdict=True):
        '''Get all Board element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Board`
            elements.  If `False`, return a list of all Board`
            children.

        
        Returns
        -------
        children : dict or list
            Dictionary or list of `Board` children

        '''
        return self.getElementsByKey(Board,'name',asdict)
    def getGameMassKeys(self,asdict=True):
        '''Get all GameMassKey element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Board`
            elements.  If `False`, return a list of all Board`
            children.

        
        Returns
        -------
        children : dict or list
            Dictionary or list of `Board` children

        '''
        return self.getElementsByKey(GameMassKey,'name',asdict)
    def getStartupMassKeys(self,asdict=True):
        '''Get all StartupMassKey element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Board`
            elements.  If `False`, return a list of all Board`
            children.

        
        Returns
        -------
        children : dict or list
            Dictionary or list of `Board` children

        '''
        return self.getElementsByKey(StartupMassKey,'name',asdict)
    def getMenus(self,asdict=True):
        '''Get all Menu element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Board`
            elements.  If `False`, return a list of all Board`
            children.

        
        Returns
        -------
        children : dict or list
            Dictionary or list of `Board` children

        '''
        return self.getElementsByKey(Menu,'text',asdict)
    def getSymbolicDices(self,asdict=True):
        '''Get all Menu element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `SymbolicDice`
            elements.  If `False`, return a list of all `SymbolicDice`
            children.

        Returns
        -------
        children : dict or list
            Dictionary or list of `SymbolicDice` children

        '''
        return self.getElementsByKey(SymbolicDice,'name',asdict)
    def getFolders(self,asdict=True):
        '''Get all Menu element(s) from this

        Parameters
        ----------
        asdict : bool
            If `True`, return a dictonary that maps key to `Folder`
            elements.  If `False`, return a list of all `Folder`
            children.

        Returns
        -------
        children : dict or list
            Dictionary or list of `Folder` children

        '''
        return self.getElementsByKey(ModuleFolder,'name',asdict)
    
    def getAtStarts(self,single=False):
        '''Get all or a sole `AtStart` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `AtStart` child, otherwise fail.
            If `False` return all `AtStart` children in this element
        
        Returns
        -------
        children : list
            List of `AtStart` children (even if `single=True`)
        '''
        return self.getAllElements(AtStart,single)

registerElement(Game)

# --------------------------------------------------------------------
# Old game module class
class OldGame(Game):
    TAG = 'VASSAL.launch.BasicModule'
    def __init__(self,build,**kwargs):
        super().__init__(build,**kwargs)
    
registerElement(OldGame)

# --------------------------------------------------------------------
class BasicCommandEncoder(GameElement):
    TAG = Element.MODULE+'BasicCommandEncoder'
    def __init__(self,doc,node=None):
        super(BasicCommandEncoder,self).__init__(doc,self.TAG,node=node)

registerElement(BasicCommandEncoder)

#
# EOF
#
# ====================================================================
# From buildfile.py

# --------------------------------------------------------------------
class BuildFile(Element):
    def __init__(self,root=None):
        '''Construct from a DOM object, if given, otherwise make new'''
        # from xml.dom.minidom import Document
        super(BuildFile,self).__init__(None,'',None)
        
        self._root = root
        self._tag  = 'buildFile'
        if self._root is None:
            self._root = xmlns.Document()

        self._node = self._root

    def addGame(self,**kwargs):
        '''Add a `Game` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Game
            The added element
        '''
        return Game(self,**kwargs)

    def getGame(self):
        '''Get the `Game`'''
        try:
            return Game(self,
                        node=self._root.\
                        getElementsByTagName('VASSAL.build.GameModule')[0])
        except:
            pass

        return Game(self,
                    node=self._root.\
                    getElementsByTagName('VASSAL.launch.BasicModule')[0])
                    

    def encode(self):
        '''Encode into XML'''
        return self._root.toprettyxml(indent=' ',
                                      encoding="UTF-8",
                                      standalone=False)


#
# EOF
#
# ====================================================================
# From moduledata.py

# --------------------------------------------------------------------
class Data(Element):
    TAG = 'data'
    def __init__(self,doc,node=None,version='1'):
        super(Data,self).__init__(doc,self.TAG,node=node,version=version)
        
    def addVersion(self,**kwargs):
        '''Add a `Version` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Version
            The added element
        '''
        return self.add(Version,**kwargs)
    def addVASSALVersion(self,**kwargs):
        '''Add a `VASSALVersion` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : VASSALVersion
            The added element
        '''
        return self.add(VASSALVersion,**kwargs)
    def addName(self,**kwargs):
        '''Add a `Name` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Name
            The added element
        '''
        return self.add(Name,**kwargs)
    def addDescription(self,**kwargs):
        '''Add a `Description` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Description
            The added element
        '''
        return self.add(Description,**kwargs)
    def addDateSaved(self,**kwargs):
        '''Add a `DateSaved` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : DateSaved
            The added element
        '''
        return self.add(DateSaved,**kwargs)
    def getVersion(self,single=True):
        '''Get all or a sole `Version` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `Version` child, otherwise fail.
            If `False` return all `Version` children in this element
        
        Returns
        -------
        children : list
            List of `Version` children (even if `single=True`)
        '''
        return self.getAllElements(Version,single=single)
    def getVASSALVersion(self,single=True):
        '''Get all or a sole `VASSALVersion` element(s) from this

        Parameters
        ----------
        single : bool        
            If `True`, there can be only one `VASSALVersion` child,
            otherwise fail.  If `False` return all `VASSALVersion`
            children in this element
        
        Returns
        -------
        children : list
            List of `VASSALVersion` children (even if `single=True`)

        '''
        return self.getAllElements(VASSALVersion,single=single)
    def getName(self,single=True):
        return self.getAllElements(Name,single=single)
    def getDescription(self,single=True):
        '''Get all or a sole `Description` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `Description` child,
            otherwise fail.  If `False` return all `De` children in
            this element
        
        Returns
        -------
        children : list
            List of `De` children (even if `single=True`)

        '''
        return self.getAllElements(Description,single=single)
    def getDateSaved(self,single=True):
        '''Get all or a sole `DateSaved` element(s) from this

        Parameters
        ----------
        single : bool
            If `True`, there can be only one `DateSaved` child, otherwise fail.
            If `False` return all `DateSaved` children in this element
        
        Returns
        -------
        children : list
            List of `DateSaved` children (even if `single=True`)
        '''
        return self.getAllElements(DateSaved,single=single)
    
registerElement(Data)

# --------------------------------------------------------------------
class DataElement(Element):
    def __init__(self,data,tag,node=None,**kwargs):
        super(DataElement,self).__init__(data,tag,node=node,**kwargs)

    def getData(self):
        return self.getParent(Data)

# --------------------------------------------------------------------
class Version(DataElement):
    TAG = 'version'
    def __init__(self,data,node=None,version=''):
        super(Version,self).__init__(data,self.TAG,node=node)
        if node is None:
            self.addText(version)

registerElement(Version)

# --------------------------------------------------------------------
class Extra1(DataElement):
    TAG = 'extra1'
    def __init__(self,data,node=None,extra=''):
        super(Extra1,self).__init__(data,self.TAG,node=node)
        if node is None:
            self.addText(extra)

registerElement(Extra1)

# --------------------------------------------------------------------
class Extra2(DataElement):
    TAG = 'extra2'
    def __init__(self,data,node=None,extra=''):
        super(Extra2,self).__init__(data,self.TAG,node=node)
        if node is None:
            self.addText(extra)

registerElement(Extra2)

# --------------------------------------------------------------------
class VASSALVersion(DataElement):
    TAG = 'VassalVersion'
    def __init__(self,data,node=None,version='3.6.7'):
        super(VASSALVersion,self).__init__(data,self.TAG,node=node)
        if node is None:
            self.addText(version)

registerElement(VASSALVersion)

# --------------------------------------------------------------------
class Name(DataElement):
    TAG = 'name'
    def __init__(self,data,node=None,name=''):
        super(Name,self).__init__(data,self.TAG,node=node)
        if node is None:
            self.addText(name)
            
registerElement(Name)

# --------------------------------------------------------------------
class Description(DataElement):
    TAG = 'description'
    def __init__(self,data,node=None,description=''):
        super(Description,self).__init__(data,self.TAG,node=node)
        if node is None:
            self.addText(description)

registerElement(Description)

# --------------------------------------------------------------------
class DateSaved(DataElement):
    TAG = 'dateSaved'
    def __init__(self,data,node=None,milisecondsSinceEpoch=-1):
        super(DateSaved,self).__init__(data,self.TAG,node=node)
        if node is None:
            from time import time
            s = f'{int(time()*1000)}' if milisecondsSinceEpoch < 0 else \
                str(milisecondsSinceEpoch)
            self.addText(s)
            
registerElement(DateSaved)

# --------------------------------------------------------------------
class ModuleData(Element):

    def __init__(self,root=None):
        '''Construct from a DOM object, if given, otherwise make new'''
        #from xml.dom.minidom import Document
        super(ModuleData,self).__init__(None,'',None)
        
        self._root = root
        self._tag  = 'moduledata'
        if self._root is None:
            self._root = xmlns.Document()

        self._node = self._root

    def addData(self,**kwargs):
        '''Add a `Data` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : Data
            The added element
        '''
        return Data(self,**kwargs)

    def getData(self):
        return Data(self,
                    node=self._root.getElementsByTagName(Data.TAG)[0])

    def encode(self):
        return self._root.toprettyxml(indent=' ',
                                      encoding="UTF-8",
                                      standalone=False)


#
# EOF
#
# ====================================================================
# From save.py

# ====================================================================
class SaveIO:
    '''Wrapper around a save file 
    
    Save file is
    
        "!VCSK" KEY content
    
    Key is two bytes drawn as a random number in 0-255.  Content is
    two bytes per character.  Content characters are encoded with the
    random key.
    
    Save file (.vsav) content is
    
        "begin_save" ESC
        "\" ESC
        [commands]* ESC
        "PLAYER" name password side ESC
        [map+"BoardPicker" name x y ESC]+
        "SETUP_STACK" ESC
        "TURN"+name state ESC
        "end_save"
    
    Commands are
    
        "+/" id "/" body "\"
    
    where body are
    
        "stack" "/" mapName ; x ; y ; ids "\"
        piece_type "/" piece_state   (x and y set here too) "\"
    
    x and y are pixel coordinates (sigh!).  This means we have to know
    
    - the pixel location of a hex
    - the hex coordinates of that hex
    - whether rows and columns are descending
    - if even hexes are higher or not
    
    The two first items _must_ be user supplied (I think).  When we
    add stacks or pieces, we must then get the numerical hex
    coordinates - not what the user specified in the VASSAL editor or
    the like.  Of course, this means opening the module before writing
    the patch.py script.
    
    It seems like every piece is added in a stack.
    
    The id is a numerical value.  Rather big (e.g., 1268518000806). It
    is the current number of miliseconds since epoch, with offset to
    disambiguate.
    
    The ID is the current time, taken from a milisecond clock,
    possibly adjusted up if there is a clash.  This is all managed by
    the GameState class.

    '''
    VCS_HEADER = b'!VCSK'
    VK_ESC     = chr(27)
    DEC_MAP    = {
        # 0-9
        0x30: 0x30,
        0x31: 0x30,
        0x32: 0x30,
        0x33: 0x30,
        0x34: 0x30,
        0x35: 0x30,
        0x36: 0x30,
        0x37: 0x30,
        0x38: 0x30,
        0x39: 0x30,
        # A-F
        0x41: 0x37,
        0x42: 0x37,
        0x43: 0x37,
        0x44: 0x37,
        0x45: 0x37,
        0x46: 0x37,
        # a-f
        0x61: 0x57,
        0x62: 0x57,
        0x63: 0x57,
        0x64: 0x57,
        0x65: 0x57,
        0x66: 0x57
    }
    ENC_MAP = [b'0',b'1',b'2',b'3',b'4',b'5',b'6',b'7',b'8',b'9',
               b'a',b'b',b'c',b'd',b'e',b'f']

    # ----------------------------------------------------------------
    @classmethod
    def decHex(cls,b):
        '''Decode a single char into a number

        If the encoded number is b, then the decoded number is
        
            b - off
    
        where off is an offset that depends on b
    
           off = 0x30   if 0x30 <= b <= 0x39
                 0x37   if 0x41 <= b <= 0x46
                 0x57   if 0x61 <= b <= 0x66
        '''
        return b - cls.DEC_MAP[b]
    # --------------------------------------------------------------------
    @classmethod
    def readByte(cls,inp,key):
        '''Read a single byte of information from input stream
    
        Two characters (c1 and c2) are read from input stream, and the
        decoded byte is then
    
            ((dechex(c1) << 4 | dechex(c2)) ^ key) & 0xFF
        
        Parameters
        ----------
        inp : stream
            Input to read from
        key : int
            Key to decode the input
    
        Returns
        -------
        b : int
            The read byte
        '''
        try:
            pair = inp.read(2)
        except Exception as e:
            from sys import stderr
            print(e,file=stderr)
            return None
    
        if len(pair) < 2:
            return None
    
        return ((cls.decHex(pair[0]) << 4 | cls.decHex(pair[1])) ^ key) & 0xFF
    # --------------------------------------------------------------------
    @classmethod
    def readSave(cls,file,alsometa=False):
        '''Read data from save file.  The data is read into lines
        returned as a list.

        '''
        from zipfile import ZipFile
        
        # We open the save file as a zip file 
        with ZipFile(file,'r') as z:
            # open the save file in the archive
            save = z.open('savedGame','r')
            
            # First, we check the header
            head = save.read(len(cls.VCS_HEADER))
            assert head == cls.VCS_HEADER, \
                f'Read header {head} is not {cls.VCS_HEADER}'
    
            # Then, read the key
            pair = save.read(2)
            key  = (cls.decHex(pair[0]) << 4 | cls.decHex(pair[1]))
    
            # Now read content, one byte at a time 
            content = ''
            while True:
                byte = cls.readByte(save,key)
                if byte is None:
                    break
    
                # Convert byte to character 
                content += chr(byte)
    
            lines = content.split(cls.VK_ESC)

            if alsometa:
                savedata = z.read(VSav.SAVE_DATA)
                moduledata = z.read(VMod.MODULE_DATA)

        if not alsometa:
            return key, lines

        return key,lines,savedata,moduledata

    # --------------------------------------------------------------------
    @classmethod
    def writeByte(cls,out,byte,key):
        '''Write a single byte

        Parameters
        ----------
        out : IOStream
            Stream to write to
        byte : char
            Single byte to write
        key : int
            Key to encode with (defaults to 0xAA - alternating 0's and 1's)
        '''
        b    = ord(byte) ^ key
        pair = cls.ENC_MAP[(b & 0xF0) >> 4], cls.ENC_MAP[b & 0x0F]
        out.write(pair[0])
        out.write(pair[1])

    # --------------------------------------------------------------------
    @classmethod
    def writeInZip(cls,z,key,lines,filename='savedGame'):
        '''Write a save file in a zip file (VMod)'''
        # open the save file in the archive
        with z.open(filename,'w') as save:
            # Write header
            save.write(cls.VCS_HEADER)
    
            # Split key
            pair = cls.ENC_MAP[(key & 0xF0) >> 4], cls.ENC_MAP[(key & 0x0F)]
            save.write(pair[0])
            save.write(pair[1])
    
            # Form content
            content = cls.VK_ESC.join(lines)
    
            # Write each character as two
            for c in content:
                cls.writeByte(save, c, key)
        
    # --------------------------------------------------------------------
    @classmethod
    def writeSave(cls,file,key,lines,savedata=None,moduledata=None):
        '''Write a save file'''
        from zipfile import ZipFile, ZIP_DEFLATED
        
        # We open the save file as a zip file 
        with ZipFile(file,'w',ZIP_DEFLATED) as z:
            cls.writeInZip(z,key,lines,filename='savedGame')

            if savedata is not None:
                z.writestr(VSav.SAVE_DATA,savedata)
                z.writestr(VMod.MODULE_DATA,moduledata)
        
# ====================================================================
#
# VSave file
#
class SaveFile:
    def __init__(self,game,firstid=None):
        '''Creates a save file to add positions to'''
        from time import time
        self._game     = game
        self._counters = {}
        self._stacks   = {}
        self._pieces   = self._game.getPieces(asdict=True)
        self._nextId   = (int(time()*1000) - 360000
                          if firstid is None else firstid)
        
    def add(self,grid,mapname,**kwargs):
        '''Add pieces to the save.

        Parameters
        ----------
        grid : BaseGrid
            Grid to add pieces to 
        kwargs : dict
            Either a map from piece name to hex position,
            Or a map from hex position to list of pieces
        '''
        for k,v in kwargs.items():
            # print('Add to save',k,v)
            self._add(grid,mapname,k,v)

    def addNoGrid(self,mapName,mapping):
        for k,v in mapping.items():
            # print('Add to save',k,v)
            self._add(None,mapName,k,v)
        

    def _add(self,grid,mapName,k,v):

        '''Add to the save'''
        with VerboseGuard(f'Adding piece(s) to save: {len(k)}') as vg:
            # print(f'Adding {k} -> {v}')
            loc       = None
            piece     = self._pieces.get(k,None)
            pieces    = []
            boardName = (grid.getMap()['mapName']
                         if mapName is None else mapName)
            # print(f'Map name: {mapName}')
            vg(f'Adding to {boardName}')
            if piece is not None:
                vg(f'Key {k} is a piece')
                #print(f'Key is piece: {k}->{piece}')
                pieces.append(piece)
                loc = v
            else:
                vg(f'Key {k} is a location')
                # Key is not a piece name, so a location
                loc = k
                # Convert value to iterable 
                try:
                    iter(v)
                except:
                    v = list(v)
                
                for vv in v:
                    if isinstance(vv,PieceSlot):
                        pieces.append(vv)
                        continue
                    if isinstance(vv,str):
                        piece = self._pieces.get(vv,None)
                        if piece is None:
                            continue
                        pieces.append(piece)
            
            vg(f'Loc: {loc} -> {pieces}')
            if len(pieces) < 1:
                return
            
            if (mapName,loc) not in self._stacks:
                vg(f'Adding stack {mapName},{loc}')
                coord = grid.getLocation(loc) if grid is not None else loc
                if coord is None:
                    print(f'did not get coordinates from {loc}')
                    return
                self._stacks[(mapName,loc)] = {
                    'x': coord[0],
                    'y': coord[1],
                    'pids': [] }
                    
            place = self._stacks[(mapName,loc)]
            for piece in pieces:
                name    = piece['entryName']
                gpid    = piece['gpid']
                counter = self._counters.get((name,gpid),None)
                vg(f'Got counter {counter} for {name},{gpid}')

                if counter is None:
                    if gpid == 0:
                        print(f'making new counter with pid={self._nextId}: '
                              f'{gpid}')
                        gpid = self._nextId
                        self._nextId += 1
                        
            
                    vg(f'Save adding counter with pid={gpid}')
                    counter = {'pid':   gpid,
                               'piece': piece,
                               'board': mapName,
                               'x':     place['x'],
                               'y':     place['y'],
                               }
                    self._counters[(name,gpid)] = counter
                    
                vg(f'Adding to stack {mapName},{loc}: {counter}')
                place['pids'].append(counter['pid'])

    def getLines(self,update=None):
        '''Get the final lines of code'''
        key   = 0xAA # fixed key
        
        lines = ['begin_save',
                 '',
                 '\\']

        self._pieceLines(lines,update=update)
        self._otherLines(lines)
        
        lines.append('end_save')
        return lines

    def _pieceLines(self,lines,update=lambda t:t):
        '''Add piece lines to save file

        Parameters
        ----------
        lines : list
            The lines to add
        '''
        # print(self._counters)
        for (name,gpid),counter in self._counters.items():
            iden   = counter['pid']
            piece  = counter['piece']
            traits = piece.getTraits()
            traits = Trait.flatten(traits,self._game)
            # Get last - trait (basic piece), and modify coords
            basic  = traits[-1]
            basic['map'] = counter['board']
            basic['x']   = counter['x']
            basic['y']   = counter['y']
            # Set old location if possible
            parent = piece.getParent(DummyElement,checkTag=False)
            if parent is not None and parent._node.nodeName == AtStart.TAG:
                oldLoc   = parent['location']
                oldBoard = parent['owningBoard']
                oldMap   = self._game.getBoards()[oldBoard].getMap()['mapName']
                oldX     = parent['x']
                oldY     = parent['y']
                oldZone  = None
                zones    = self._game.getBoards()[oldBoard].getZones()
                for zone in zones.values():
                    grid = zone.getGrids()[0]
                    if grid is None: continue
                    
                    coord = grid.getLocation(oldLoc)
                    if coord is None: continue

                    oldZone = zone['name']
                    oldX    = coord[0]
                    oldY    = coord[1]
                    break

                if oldZone is not None:
                    basic['properties'] = \
                        f'8;'+\
                        f'UniqueID;{iden};'+\
                        f'OldZone;{oldZone};'+\
                        f'OldLocationName;{oldLoc};'+\
                        f'OldDeckName;;'+\
                        f'OldX;{oldX};'+\
                        f'OldY;{oldY};'+\
                        f'OldBoard;{oldBoard};'+\
                        f'OldMap;{oldMap}'
                else:
                    basic['properties'] = \
                        f'7;'+\
                        f'UniqueID;{iden};'+\
                        f'OldLocationName;{oldLoc};'+\
                        f'OldDeckName;;'+\
                        f'OldX;{oldX};'+\
                        f'OldY;{oldY};'+\
                        f'OldBoard;{oldBoard};'+\
                        f'OldMap;{oldMap}'

                for trait in traits:
                    if trait.ID == TrailTrait.ID:
                        trait['map']    = oldMap
                        trait['points'] = f'1;{oldX},{oldY}'
                        trait['init']   = True

            # Let user code update the flattened traits
            if update is not None:
                update(name,traits)
            # Wrapper 
            wrap   = DummyWithTraits(self._game,traits=[])
            wrap.setTraits(*traits,iden=str(iden))
            lines.append(wrap._node.childNodes[0].nodeValue+'\\')

        layer = -1
        for key,dat in self._stacks.items():
            pids = dat.get('pids',None)
            x    = dat['x']
            y    = dat['y']
            if pids is None or len(pids) < 1:
                print(f'No pieces at {key[0]},{key[1]}')
                continue
            
            iden         =  self._nextId
            self._nextId += 1
            stack        =  StackTrait(board=key[0],x=x,y=y,pieceIds=pids,layer=layer)
            layer        = 1
            wrap         =  DummyWithTraits(self._game,traits=[])
            wrap.setTraits(stack,iden=iden)
            lines.append(wrap._node.childNodes[0].nodeValue+'\\')
            
    def _otherLines(self,lines):
        '''Add other lines to save'''
        lines.append('UNMASK\tnull')
        if self._game.getPlayerRoster():
            for r in self._game.getPlayerRoster():
                lines.extend(r.encode())
        if self._game.getNotes(single=False):
            for n in self._game.getNotes(single=False):
                lines.extend(n.encode())
        setupStack = False
        for m in self._game.getMaps(asdict=False):
            for bp in m.getBoardPicker(single=False):
                lines.extend(bp.encode())
            if not setupStack:
                atstart = m.getAtStarts(single=False)
                if atstart and len(atstart) > 0:
                    lines.append('SETUP_STACK')
                    setupStack = True
                
        # for tk,tt in self._game.getTurnTracks(asdict=True):
        #     lines.extend(tt.encode())

            
# --------------------------------------------------------------------
class SaveData(ModuleData):
    def __init__(self,root=None):
        '''Convinience wrapper'''
        super(SaveData,self).__init__(root=root)
# ====================================================================
# From vsav.py

# --------------------------------------------------------------------
class VSav:
    SAVE_DATA = 'savedata'
    
    def __init__(self,build,vmod):
        '''Create a VASSAL save file programmatically

        Parameters
        ----------
        build : xml.dom.Document
            `buildFile.xml` as XML
        vmod : VMod
            Module file
        '''
        from time import time 
        self._vmod  = vmod
        self._game  = build.getGame()
        self._start = int(time()*1000)
        

    def createSaveData(self,description=None):
        '''Create `savedgame`'''
        desc           = (self._game['description']
                          if description is None else description)
        self._saveData = SaveData(root=None)
        data           = self._saveData.addData()
        data.addVersion      (version    =self._game['version'])
        data.addVASSALVersion(version    =self._game['VassalVersion'])
        data.addDescription  (description=desc)
        data.addDateSaved    (milisecondsSinceEpoch=self._start)
        return self._saveData

    def createModuleData(self):
        '''Create `moduleData`'''
        self._moduleData = ModuleData()
        data = self._moduleData.addData()
        data.addVersion      (version    =self._game['version'])
        data.addVASSALVersion(version    =self._game['VassalVersion'])
        data.addName         (name       =self._game['name'])
        data.addDescription  (description=self._game['description'])
        data.addDateSaved    (milisecondsSinceEpoch=self._start)
        return self._moduleData
        
    def addSaveFile(self):
        '''Add a save file to the module

        Returns
        -------
        vsav : SaveFile
            Save file to add content to        
        '''
        self._saveFile = SaveFile(game=self._game,firstid=self._start)
        return self._saveFile

    def run(self,
            savename    = 'Save.vsav',
            description = None,
            update      = None):
        '''Run this to generate the save file

        Parameters
        ----------
        savename : str
            Name of save file to write
        description : str
            Short description of the save file
        update : callable or None
            A callable that can update trait states after the piece
            traits have been fully flattened.  The callable should
            adhere to the interface

                update(name,traits)

            where `name` is the name of the piece (entryName) and
            `traits` is a list of unrolled traits.

        '''
        from zipfile import ZipFile, ZIP_DEFLATED
        
        self.createSaveData(description=description)
        self.createModuleData()
        
        with self._vmod.getInternalFile(savename,'w') as vsav:
            with ZipFile(vsav,'w',ZIP_DEFLATED) as zvsav:
                # The key is set to 0xAA (alternating ones and zeros)
                SaveIO.writeInZip(zvsav,0xAA,
                                  self._saveFile.getLines(update=update))
            
                zvsav.writestr(VMod.MODULE_DATA, self._moduleData.encode())
                zvsav.writestr(VSav.SAVE_DATA,   self._saveData.encode())
            
#
# EOF
#
# ====================================================================
# From vmod.py
# ====================================================================
#
# Wrapper around a module 
#

class VMod:
    BUILD_FILE = 'buildFile.xml'
    BUILD_FILE_SANS = 'buildFile'
    MODULE_DATA = 'moduledata'
    EXTENSION_DATA = 'extensiondata'
    
    def __init__(self,filename,mode):
        '''Interface to VASSAL Module (a Zip file)'''
        self._mode = mode
        self._vmod = self._open(filename,mode)

    def __enter__(self):
        '''Enter context'''
        return self

    def __exit__(self,*e):
        '''Exit context'''
        self._vmod.close()
        return None

    def _open(self,filename,mode):
        '''Open a file in VMod'''
        from zipfile import ZipFile, ZIP_DEFLATED

        return ZipFile(filename,mode,compression=ZIP_DEFLATED)
        
    def removeFiles(self,*filenames):
        '''Open a temporary zip file, and copy content from there to
        that file, excluding filenames mentioned in the arguments.
        Then close current file, rename the temporary file to this,
        and reopen in 'append' mode.  The deleted files are returned
        as a dictionary.

        Parameters
        ----------
        filenames : tuple
            List of files to remove from the VMOD

        Returns
        -------
        files : dict
            Dictionary from filename to content of the removed files.

        Note, the VMOD is re-opened in append mode after this
        '''
        from tempfile import mkdtemp
        from zipfile import ZipFile
        from shutil import move, rmtree 
        from os import path

        tempdir = mkdtemp()
        ret     = {}

        try:
            tempname = path.join(tempdir, 'new.zip')
            with self._open(tempname, 'w') as tmp:

                for item in self._vmod.infolist():
                    data = self._vmod.read(item.filename)

                    if item.filename not in filenames:
                        tmp.writestr(item, data)
                    else:
                        ret[item.filename] = data

            name = self._vmod.filename
            self._vmod.close()
            move(tempname, name)

            self._mode = 'a'
            self._vmod = self._open(name,'a')
        finally:
            rmtree(tempdir)

        # Return the removed files 
        return ret

    def clone(self,newname,mode='a',filter=lambda f:False):
        '''Clones the VMod and returns new object.

        This is done by first opening a temporary ZIP file, and then
        copy all files of this module to that tempoary.  Then the
        temporary ZIP is closed and moved to its `newname`.  After
        that, we open it up as a VMod (write-enabled).

        '''
        from tempfile import mkdtemp
        from zipfile import ZipFile
        from shutil import move, rmtree 
        from os import path

        tempdir = mkdtemp()
        ret     = None

        try:
            tempname = path.join(tempdir, 'new.zip')
            with self._open(tempname, 'w') as tmp:

                for item in self._vmod.infolist():
                    # Ignore some files, a given by filter functoin 
                    if filter(item.filename):
                        continue
                    
                    data = self._vmod.read(item.filename)

                    tmp.writestr(item, data)

            move(tempname, newname)

            ret =  VMod(newname,mode)
        finally:
            rmtree(tempdir)

        return ret
        

    def fileName(self):
        '''Get name of VMod file'''
        return self._vmod.filename

    def replaceFiles(self,**files):
        '''Replace existing files with new files

        Parameters
        ----------
        files : dict
            Dictionary that maps file name to content
        '''
        self.removeFiles(*list(files.keys()))

        self.addFiles(**files);
    
    def addFiles(self,**files):
        '''Add a set of files  to this

        Parameters
        ----------
        files : dict
            Dictionary that maps file name to content.
        '''
        for filename,data in files.items():
            self.addFile(filename,data)

    def addFile(self,filename,content):
        '''Add a file to this

        Parameters
        ----------
        filename : str
            File name in module
        content : str
            File content
        
        Returns
        -------
        element : File
            The added element
        '''
        self._vmod.writestr(filename,content)

    def addExternalFile(self,filename,target=None):
        '''Add an external file element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : ExternalFile
            The added element
        '''
        if target is None: target = filename
        self._vmod.write(filename,target)
        
    def getFileNames(self):
        '''Get all filenames in module'''
        return self._vmod.namelist()

    def getFileMapping(self):
        '''Get mapping from short name to full archive name'''
        from pathlib import Path
        
        names = self.getFileNames()

        return {Path(p).stem: str(p) for p in names}
    
    def getFiles(self,*filenames):
        '''Return named files as a dictionary.

        Parameters
        ----------
        filenames : tuple
            The files to get 
        
        Returns
        -------
        files : dict
            Mapping of file name to file content
        '''
        fn  = self.getFileNames()
        ret = {}
        for f in filenames:
            if f not in fn:
                continue

            ret[f] = self._vmod.read(f)

        return ret

    def getDOM(self,filename):
        '''Get content of a file decoded as XML DOM

        Parameters
        ----------
        filename : str
            Name of file in module 
        '''
        #from xmlns import parseString

        r = self.getFiles(filename)
        if filename not in r:
            raise RuntimeError(f'No {filename} found!')

        return xmlns.parseString(r[filename])
        
    def getBuildFile(self):
        '''Get the buildFile.xml decoded as a DOM tree'''
        try:
            return self.getDOM(VMod.BUILD_FILE)
        except Exception as e:
            print(e)
        try:
            return self.getDOM(VMod.BUILD_FILE_SANS)
        except:
            raise

    def getModuleData(self):
        '''Get the moduledata decoded as a DOM tree'''
        return self.getDOM(VMod.MODULE_DATA)

    def getExtensionData(self):
        '''Get the moduledata decoded as a DOM tree'''
        return self.getDOM(VMod.EXTENSION_DATA)

    def isExtension(self):
        return VMod.EXTENSION_DATA in self.getFileNames()
    
    def getInternalFile(self,filename,mode):
        return self._vmod.open(filename,mode)

    def addVSav(self,build):
        '''Add a `VSav` element to this

        Parameters
        ----------
        kwargs : dict
            Dictionary of attribute key-value pairs
        
        Returns
        -------
        element : VSav
            The added element
        '''
        return VSav(build=build,vmod=self)

    @classmethod
    def patch(cls,vmod_filename,patch_name,verbose):
        '''Patch a module with a Python script

        Parameters
        ----------
        vmod_filename : str
            File name of module to patch.  Will be overwritten
        patch_name : str
            File name of Python script to patch with
        verbose : bool
            Whether to be verbose or not
        '''
    
        with cls(vmod_filename,'r') as vmod:
            buildFile  = BuildFile(vmod.getBuildFile())
            moduleData = ModuleData(vmod.getModuleData())

        from importlib.util import spec_from_file_location, module_from_spec
        from pathlib import Path
        from sys import modules

        p = Path(patch_name)

        spec   = spec_from_file_location(p.stem, p.absolute())
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
    
        modules[p.stem] = module

        with cls(vmod_filename,'a') as vmod:
            module.patch(buildFile,
                         moduleData,
                         vmod,
                         verbose)
    
            vmod.replaceFiles(**{VMod.BUILD_FILE :
                                 buildFile.encode(),
                                 VMod.MODULE_DATA :
                                 moduleData.encode()})


    @classmethod
    def patchFunction(cls,vmod_filename,patch,verbose):
        '''Patch a module with a Python script

        Parameters
        ----------
        vmod_filename : str
            File name of module to patch.  Will be overwritten
        patch : callable
            A callable to patch the VMod.  It must have signature
        
                patch(buildFile  : pywargames.vassal.BuildFile,
                      moduleData : pywargames.vassal.ModuleData,
                      vmod       : pywargames.vassal.VMod
                      verbose    : boolean)

        verbose : bool
            Whether to be verbose or not
        '''
    
        with cls(vmod_filename,'r') as vmod:
            buildFile  = BuildFile(vmod.getBuildFile())
            moduleData = ModuleData(vmod.getModuleData())

        with cls(vmod_filename,'a') as vmod:
            try:
                patch(buildFile,
                      moduleData,
                      vmod,
                      verbose)
    
                vmod.replaceFiles(**{VMod.BUILD_FILE :
                                     buildFile.encode(),
                                     VMod.MODULE_DATA :
                                     moduleData.encode()})
            except Exception as e:
                raise
            

#
# EOF
#
# ====================================================================
# From upgrade.py


class VLogUpgrader:
    def __init__(self,
                 vmodFileName,
                 vlogFileName,
                 verbose=False):
        self._readVModFile(vmodFileName,verbose)
        self._readVLogFile(vlogFileName,verbose)

    def _readVModFile(self,vmodFileName,verbose=False):
        with VMod(vmodFileName, 'r') as vmod:
            self._build = BuildFile(vmod.getBuildFile())
            self._game  = self._build.getGame()

        self._vmod_pieces = {}
        for piece in self._game.getPieces():
            name, piece             = self._expandPiece(piece,verbose)
            self._vmod_pieces[name] = piece

    def _expandPiece(self,piece,verbose=False):
        traits    = piece.getTraits();
        newTraits = Trait.flatten(traits, game=self._game,verbose=verbose)

        piece.setTraits(*newTraits)

        name = newTraits[-1]['name']

        return name, piece

    def _readVLogFile(self,vlogFileName,verbose=False):
        key, lines, sdata, mdata = SaveIO.readSave(vlogFileName,
                                                   alsometa=True)

        self._key         = key
        self._lines       = lines
        self._save_data   = sdata
        self._meta_data   = mdata
        self._vlog_pieces = {}
        
        for line in self._lines:
            iden, name, piece = self._vlogPiece(line,verbose)
            if piece is None:
                continue

            vmod_piece        = self._vmod_pieces.get(name,None)
            if vmod_piece is None:
                print(f'Did not find piece "{name}" in vmod')
                vmod_piece = piece

            vmod_piece.copyStates(piece)
            self._vlog_pieces[iden] = {'name': name,
                                       'vlog': piece,
                                       'vmod': vmod_piece}        


    def _vlogPiece(self,line,verbose=False):
        from re import match

        m = match(r'^\+/([0-9]+)/.*;([a-z0-9_]+)\.png.*',line)
        if m is None:
            return None,None,None

        iden  = int(m.group(1))
        piece = PieceSlot(None)
        piece.setTraits(*piece.decodeAdd(line,verbose),iden=iden)
        basic = piece.getTraits()[-1]
        
        return iden,basic['name'],piece
        

    def _newLine(self,line,verbose):
        self._new_lines.append(line)
        if verbose:
            print(line)
        
    def upgrade(self,shownew=False,verbose=False):
        self._new_lines = []
        for line in self._lines:
            add_line = self.newDefine(line,verbose)
            if add_line:
                self._newLine(add_line,shownew)
                continue

            cmd_line = self.newCommand(line,verbose)
            if cmd_line:
                self._newLine(cmd_line,shownew)
                continue 

            oth_line = self.other(line,verbose)
            if oth_line:
                self._newLine(oth_line,shownew)
                continue

            self._newLine(line,shownew)

    def newCommand(self,line,verbose=False):
        from re import match

        m = match(r'LOG\s+([+MD])/([0-9]+)/([^/]+)(.*)',line)
        if not m:
            return None
    
        cmd  = m.group(1)
        iden = int(m.group(2))
        more = m.group(3)

        if more == 'stack':
            return None

        vp = self._vlog_pieces.get(iden,None)
        if vp is None:
            print(f'Piece {iden} not found: "{line}"')
            return None

        if cmd == '+' or cmd == 'M':
            return None 

        # Get the code
        code = more + m.group(4)

        # Decode the states from the code into the old piece 
        vp['vlog'].decodeStates(code,verbose)

        # Get the previsous state from the new piece 
        old = vp['vmod'].encodedStates()

        # Copy states from the old piece to the new piece 
        vp['vmod'].copyStates(vp['vlog'],verbose)
    
        # Get the new state code from the new piece 
        new = vp['vmod'].encodedStates()

        newline = 'LOG\t'+cmd+'/'+str(iden)+'/'+new+'/'+old+'\\\\'
        # print('WAS',line)
        # print('NOW',newline)
        return newline

    def newDefine(self,line,verbose):
        from re import match
    
        m = match(r'\+/([0-9]+)/([^/]+).*',line)

        if not m:
            return False

        iden = int(m.group(1))
        more = m.group(2)
        if more == 'stack':
            return False

        vp = self._vlog_pieces.get(iden,None)
        if vp is None:
            print(f'Piece {iden} not known')

        old = vp['vlog']
        new = vp['vmod']

        old_add = old._node.childNodes[0].nodeValue;
        new_add = new.encodeAdd(*new.getTraits(),iden=iden,verbose=verbose);

        return new_add
        
    def other(self,line,verbose=False):
        return None
    

    def write(self,outFileName,verbose=False):
        SaveIO.writeSave(outFileName,
                         key         = 0xAA,
                         lines       = self._new_lines,
                         savedata    = self._save_data,
                         moduledata  = self._meta_data)

        
        
#
# EOF
#
# ====================================================================
# From exporter.py

class Exporter:
    def __init__(self):
        '''Base class for exporters'''
        pass


    def setup(self):
        '''Should be defined to set-up for processing, for example
        generating images and such.  This is executed in a context
        where the VMod file has been opened for writing via
        `self._vmod`. Thus, files can be added to the module at this
        stage.
        '''         
        pass

    def createBuildFile(self,ignores='(.*markers?|all|commons|[ ]+)'):
        '''Should be defined to make the `buildFile.xml` document

        Parameters
        ----------
        ignores : str
            Regular expression to match ignored categories for factions
            determination. Python's re.fullmatch is applied to this
            regular exression against chit categories.  If the pattern
            is matched, then the chit is not considered to belong to a
            faction.

        '''
        pass

    def createModuleData(self):
        '''Should be defined to make the `moduledata` document'''
        pass
    
    def run(self,vmodname,patch=None):
        '''Run the exporter to generate the module
        '''
        with VMod(vmodname,'w') as vmod:
            self._vmod = vmod
            self.setup()
            self.createBuildFile() 
            self.createModuleData()
            self.runPatch(patch)
            self._vmod.addFiles(**{VMod.BUILD_FILE  :
                                   self._build.encode(),
                                   VMod.MODULE_DATA :
                                   self._moduleData.encode()})
        Verbose().message('Created VMOD')
        

    def runPatch(self,patch):
        '''Run user specified patch script.  The script should define

            ```
            def patch(buildFile,moduleData,vmod,verbose):
            ```

        where `buildFile` is the `buildFile.xml` and `moduleData` are
        the XML documents as `xml.dom.Document` objects, `vmod` is a
        `VMod` instance, and `verbose` is a `bool` selecting verbose
        mode or not.
        '''
        if patch is None or patch == '':
            return
        
        from importlib.util import spec_from_file_location, module_from_spec
        from pathlib import Path
        from sys import modules

        p = Path(patch)
        with VerboseGuard(f'Will patch module with {p.stem}.patch function') \
             as v:

            spec   = spec_from_file_location(p.stem, p.absolute())
            module = module_from_spec(spec)
            spec.loader.exec_module(module)
            modules[p.stem] = module
            
            # Patch must accept xml.dom.document,xml.dom.document,ZipFile
            module.patch(self._build,
                         self._moduleData,
                         self._vmod,
                         Verbose().verbose)
    
##
# End of generated script
##
