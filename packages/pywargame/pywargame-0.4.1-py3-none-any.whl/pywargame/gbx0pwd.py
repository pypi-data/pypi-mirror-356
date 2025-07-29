#!/usr/bin/env python
# Script collected from other scripts
#
#   cyberboard.py
#   zeropwd.py
#
# ====================================================================
# From cyberboard.py
# Script collected from other scripts
#
#   ../common/singleton.py
#   ../common/verbose.py
#   ../common/verboseguard.py
#   features.py
#   archive.py
#   base.py
#   head.py
#   image.py
#   tile.py
#   piece.py
#   mark.py
#   draw.py
#   cell.py
#   board.py
#   gamebox.py
#   scenario.py
#   player.py
#   windows.py
#   palette.py
#   tray.py
#   extractor.py
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
# From features.py
# --------------------------------------------------------------------

class Features(metaclass=Singleton):
    def __init__(self):
        self.bmp_zlib      = False # wxBMPHandler + Zlib
        self.id_size       = 2     # Size of IDs in bytes (1, 2 or 4)
        self.size_size     = 4     # Size of sizes in bytes (4 or 8)
        self.sub_size      = 2     # Size of sub-sizes in bytes (4 or 8)
        self.square_cells  = False # Geomorphic boards, square cells
        self.rotate_unit   = False # Geomorphic boards, rotated unit board
        self.piece_100     = False # Pieces w/<= 100 sides
        self.private_board = False #
        self.roll_state    = False # serialize roll state
        self.little_endian = True
# ====================================================================
# From archive.py



class BaseArchive:
    WORD_SIZE = 2
    
    def __init__(self,filename,mode='rb'):
        '''Read data from a MFT CArchive stored on disk

        Works as a context manager 
        '''
        with VerboseGuard(f'Opening archive {filename}'):
            self._filename = filename
            self._file = open(filename,mode)
            self._i    = 0
            self.vmsg  = lambda *args : Verbose().message(*args)
            #self.vmsg  = lambda *args : None
        
    def __enter__(self):
        '''Enter context'''
        return self

    def __exit__(self,*args,**kwargs):
        '''Exit context'''
        self._file.close()

    def tell(self):
        pass

    def read(self,n):
        '''Read n bytes from archive'''
        pass

    def chr(self,n):
        '''Read n characters from archive'''
        b = self.read(n)
        try:
            c = b.decode()
            self.vmsg(f'char->{c}')
            return c
        except:
            print(f'Failed at {b} ({self._file.tell()})')
            raise

    def int(self,n):
        '''Read an (unsigned) integer from archive'''
        b = self.read(n)
        i = int.from_bytes(b,'little' if Features().little_endian else 'big')
        self.vmsg(f'int->{i}')
        return i     

    def byte(self):
        '''Read a byte from archive'''
        return self.int(1)

    def word(self):
        '''Read a word (16bit integer) from archive'''
        w = self.int(BaseArchive.WORD_SIZE)
        self.vmsg(f'word->{w}')
        return w;


    def dword(self):
        '''Read a double word (32bit integer) from archive'''
        d = self.int(2*BaseArchive.WORD_SIZE)
        self.vmsg(f'dword->{d}')
        return d

    def size(self):
        '''Read a size'''
        s = self.int(Features().size_size)
        self.vmsg(f'size->{s}')
        return s

    def sub_size(self):
        '''Read a size'''
        s = self.int(Features().sub_size)
        self.vmsg(f'sub->{s}')
        return s
    
    def count(self):
        '''Read a count'''
        if Features().size_size == 4:
            return self.word()

        c = self.word()
        if c != 0xFFFF:
            return c

        c = self.dword()
        if c != 0xFFFFFFFF:
            return c

        return int(8)
        
    def iden(self):
        '''Read an identifier'''
        i = self.int(Features().id_size)
        self.vmsg(f'id->{i}')
        return i
        
    def _strlen(self):
        '''Read length of following string from archive'''
        # See https://github.com/pixelspark/corespark/blob/master/Libraries/atlmfc/src/mfc/arccore.cpp

        s = 1
        l = self.byte()
        
        if l < 0xFF: # Small ASCII string
            self.vmsg(f'slen->{l},{s}')
            return l, s
        
        l = self.word()
        if l == 0xFFFE: # Unicode  - try again
            s = 2
            l = self.byte()

            if l < 0xFF: # Small unicode
                self.vmsg(f'slen->{l},{s}')
                return l, s
            

            l = self.word() # Large unicode string

        if l < 0xFFFF: # Not super long
            self.vmsg(f'slen->{l},{s}')
            return l, s

        l = self.dword()

        if l < 0xFFFFFFFF: # Not hyper long
            self.vmsg(f'slen->{l},{s}')
            return l, s

        
        self.vmsg(f'slen->{8},fixed')
        return self.int(8)
        
    def str(self):
        '''Read a string from the archive'''
        # See https://github.com/pixelspark/corespark/blob/master/Libraries/atlmfc/src/mfc/arccore.cpp
        l, s = self._strlen()
        # print(f'Read string of length {l}*{s} at {self.tell()}')
        ret  = [self.read(s) for i in range(l)]
        try:
            ret = [c.decode() for c in ret]
        except:
            ret = ['']
        self.vmsg(f'str->"{"".join(ret)}"')
        return ''.join(ret)

    @property
    def filename(self):
        return self._filename

    @property
    def path(self):
        from pathlib import Path
        return Path(self._filename)
    
# ====================================================================
class UnbufferedArchive(BaseArchive):
    def __init__(self,filename,mode='rb'):
        '''Read data from a MFT CArchive stored on dist

        Works as a context manager 
        '''
        super(UnbufferedArchive,self).__init__(filename,mode='rb')

    def read(self,n):
        '''Read n bytes from archive - directly from file'''
        b = self._file.read(n)
        self.vmsg(f'read->{list(b)}')
        # print(f'{self._i:6d} -> {b}')
        self._i += n
        return b

    def tell(self):
        return self._file.tell()

# ====================================================================
class BufferedArchive(BaseArchive):
    def __init__(self,filename,mode='rb'):
        '''Read data from a MFT CArchive stored on dist

        Works as a context manager 
        '''
        super(BufferedArchive,self).__init__(filename,mode='rb')
        self._size    = 4096
        self._max     = self._size
        self._current = self._max
        self._buffer  = []

    def read(self,n):
        with VerboseGuard(f'Read {n} bytes') as g:
            '''Read n bytes from archive - buffered
            
            This emulates the behaviour of MFC CArchive::Read 
            '''
            
            nmax          = n
            ntmp          =  min(nmax, self._max - self._current)
            b             =  self._buffer[self._current:self._current+ntmp]
            g(f'Take {ntmp} bytes from buffer -> {b}')
            self._current += ntmp
            nmax          -= ntmp
            
            if nmax != 0:
                g(f'Need to read at least {nmax} from file')
                assert self._current == self._max,\
                    f'Something is wrong! {self._current} != ' \
                    f'{self._max} (1)'

                g(f'Missing {nmax} bytes -> ({nmax % self._size})')
                ntmp         = nmax - (nmax % self._size)
                nread        = 0
                nleft        = ntmp
                nbytes       = 0
                while True:
                    tmpbuf =  self._file.read(nleft)
                    nbytes =  len(tmpbuf)
                    nread  += nbytes
                    nleft  -= nbytes
                    b      += tmpbuf
                    g(f'Read {nleft} -> {tmpbuf}')
                    
                    if nbytes <= 0 or nleft <= 0:
                        break
            
                nmax -= nread
            
                if nmax > 0 and nread  == ntmp:
                    # Last read chunk into buffer and copy
                    assert self._current == self._max,\
                        f'Something is wrong! {self._current} != ' \
                        f'{self._max} (2)'
                    
                    assert nmax < self._size, \
                        f'Something is wrong {nmax} >= {self._size}'
                    
                    nlastleft    = max(nmax,self._size)
                    nlastbytes   = 0
                    nread        = 0
                    self._buffer = []
                    while True:
                        tmpbuf       =  self._file.read(nlastleft)
                        nlastbytes   =  len(tmpbuf)
                        nread        += nlastbytes
                        nlastleft    -= nlastbytes
                        self._buffer += tmpbuf
            
                        if (nlastbytes <= 0) or \
                           (nlastleft <= 0) or \
                           nread >= ntmp:
                            break
            
                    self._current = 0
                    self._max     = nread
            
                    ntmp          =  min(nmax, self._max - self._current)
                    b             += self._buffer[self._current:
                                                  self._current+ntmp]
                    self._current += ntmp
                    nmax          -= ntmp
            
            g(b)
            return b''.join(b)

    def tell(self):
        return self._file.tell()
    

Archive = UnbufferedArchive
# Archive = BufferedArchive

#
# EOF
#
# ====================================================================
# From base.py

# --------------------------------------------------------------------
class CbFont:
    def __init__(self,ar):
        '''Shared structure that holds font information'''
        # Fonts
        with VerboseGuard('Reading font definition'):
            self._size        = ar.word()
            self._flags       = ar.word()
            self._family      = ar.word()
            self._name        = ar.str()
            
    def isBold(self):
        return self._flags & 0x1

    def isItalic(self):
        return self._flags & 0x2

    def isUnderline(self):
        return self._flags & 0x4

    def __str__(self):
        return (f'Font:{self._name} ({self._family}) @ '
                f'{self._size} ({self._flags:08x})')

# --------------------------------------------------------------------
class CbManager:
    def __init__(self,ar):
        '''Base class for some managers'''
        with VerboseGuard('Reading general manager'):
            self._foreground  = ar.dword()
            self._background  = ar.dword()
            self._linewidth   = ar.word()
            self._font        = CbFont(ar)
            self._reserved    = [ar.word() for _ in range(4)]

    def _readNsub(self,ar,sub_size):
        return ar.int(sub_size)

    def _readSub(self,ar,cls,sub_size=None):
        if sub_size is None:
            sub_size = Features().sub_size
        with VerboseGuard(f'Reading sub {cls} of manager ({sub_size})'):
            n = self._readNsub(ar,sub_size)
            return [cls(ar) for _ in range(n)]

    def _strSub(self,title,subs):
        subl = '\n    '.join([str(s) for s in subs])
        return f'  # {title}: {len(subs)}\n    {subl}'

    def __str__(self):
        return (f'  Foreground:   {self._foreground:08x}\n'
                f'  Background:   {self._background:08x}\n'
                f'  Linewidth:    {self._linewidth}\n'
                f'  Font:         {self._font}\n'
                f'  Reserved:     {self._reserved}\n')

#
# EOF
#
# ====================================================================
# From head.py

def num_version(major,minor):
    return major * 256 + minor

def readVector(ar,cls):
    with VerboseGuard('Reading vector') as g:
        if Features().size_size == 8:
            n = ar.size()
        else:
            n                   = ar.word()
            if n == 0xFFFF:
                n               = ar.dword()
                if n == 0xFFFFFFFF:
                    n           = ar.int(64)
        g(f'{n} elements')
    return [cls(ar) for _ in range(n)]

# ====================================================================
class GBXHeader:
    BOX      = 'GBOX'
    SCENARIO = 'GSCN'
    def __init__(self,ar,expect=BOX):
        '''GBXHeader of file 

        4 bytes format ID
        4x1 byte format and program version

        8 bytes in total 
        '''
        with VerboseGuard('Reading header') as g:
            sig = ar.chr(len(expect))
            assert sig == expect, f'Not a {expect} file: {sig}'

            self._major        = ar.byte()
            self._minor        = ar.byte()
            self._programMajor = ar.byte()
            self._programMinor = ar.byte()
            self._vers         = num_version(self._major,self._minor)
            g(f'Version {self._major}.{self._minor}')

            assert self._vers >= num_version(3,0),\
                f'{self._major}.{self._minor} format not supported'

            if self._vers >= num_version(4,0):
                g(f'Detected version 4.0 or newer, setting some features')
                Features().id_size       = 4
                Features().size_size     = 8
                Features().sub_size      = 8
                Features().square_cells  = True
                Features().rotate_unit   = True
                Features().piece_100     = True
                Features().private_board = True
                Features().roll_state    = True
                
                
            


    def __str__(self):
        return ('Header:\n'
                f'  Format major version:  {self._major}\n'
                f'  Format minor version:  {self._minor}\n'
                f'  Program major version: {self._programMajor}\n'
                f'  Program minor version: {self._programMinor}\n')


# --------------------------------------------------------------------
class GBXStrings:
    def __init__(self,ar):
        '''Map IDs to strings'''
        with VerboseGuard(f'Reading string mappings'):
            strMapN = ar.size()
            
            self._id2str = {}
            for _ in range(strMapN):
                key = ar.dword()
                val = ar.str()
            
                self._id2str[key] = val

    def __str__(self):
        return ('Strings:\n'+
                '\n'.join([f'  {key:8x}: {val}'
                           for key,val in self._id2str.items()]))

# --------------------------------------------------------------------
class GSNStrings:
    def __init__(self,ar):
        '''Map IDs to strings'''
        with VerboseGuard(f'Reading string mappings'):
            strMapN = ar.size()
            
            self._id2str = {}
            for _ in range(strMapN):
                key = ar.size()
                val = ar.str()
            
                self._id2str[key] = val

    def __str__(self):
        return ('Strings:\n'+
                '\n'.join([f'  {key:8x}: {val}'
                           for key,val in self._id2str.items()]))
    
#
# EOF
#
# ====================================================================
# From image.py

# ====================================================================
class GBXImage:
    def __init__(self,ar,transparent=None,save=None):
        '''A DIB image stored in GameBox'''
        with VerboseGuard('Reading an image') as g:
            size = ar.dword()
                
            if size & 0x80000000: # Compressed
                from zlib import decompress
                g(f'Read compressed image')
                
                size       &= 0x80000000  # Remove flag
                compSize   =  ar.dword() # Compressed size
                compressed =  ar.read(compSize) # Compressed
                buffer     = decompress(compressed,bufsize=size)
                #assert len(buffer) == size, \
                #    f'Failed to decompress to expected {size}, ' \
                #    f'got {len(buffer)}'
                    
            else:
                buffer  = ar.read(size)
            
            from PIL import Image as PILImage
            from io import BytesIO
            from numpy import asarray, where, uint8
            
            img = PILImage.open(BytesIO(buffer)).convert('RGBA')
            
            # If transparancy is defined, clean up the image 
            if transparent is None:
                self._img = img
            else:
                g(f'Making #{transparent:06x} transparent')
                dat         = asarray(img)
                tr          = (transparent >> 16) & 0xFF
                tg          = (transparent >> 8)  & 0xFF
                tb          = (transparent >> 0)  & 0xFF
                dat2        = dat.copy()
                dat2[:,:,3] = (255*(dat[:,:,:3]!=[tb,tg,tr]).any(axis=2))\
                    .astype(uint8)

                #if (dat[:,:,3] == dat2[:,:,3]).all():
                #    print(f'Transparency operation seemed to have no effect '
                #          f'for image')
                
                self._img  = PILImage.fromarray(dat2)
            
            if save is None:
                return
            
            self._img.save(save)

    @classmethod
    def b64encode(cls,img):
        '''Encode image as a base64 data URL'''
        from io import BytesIO
        from base64 import b64encode

        if img is None:
            return None
        
        buffered = BytesIO()
        img.save(buffered,format='PNG')
        data = b64encode(buffered.getvalue())
        if not isinstance(data,str):
            data = data.decode()

        return 'data:image/png;base64,'+data

#
# EOF
#
# ====================================================================
# From tile.py

# ====================================================================
class GBXTileLocation:
    def __init__(self,ar):
        '''Where a tile can be found'''
        with VerboseGuard('Reading tile location') as g:
            self._sheet  = (ar.word() if not Features().size_size == 8 else
                            ar.size())
            self._offset = ar.word() 
            g(f'Tile location at sheet={self._sheet} offset={self._offset}')
            if self._sheet == 65535: self._sheet = -1

    def __str__(self):
        return f'{self._sheet:3d} @ {self._offset:6d}'

        
# --------------------------------------------------------------------
class GBXTileDefinition:
    def __init__(self,ar):
        '''The definition of a tile'''
        with VerboseGuard('Reading tile definition'):
            self._full = GBXTileLocation(ar)
            self._half = GBXTileLocation(ar)
            self._fill = ar.dword()

    def __str__(self):
        return f'Full: {self._full}, Half: {self._half}, Fill: {self._fill:08x}'
    
        
# --------------------------------------------------------------------
class GBXTileSet:
    def __init__(self,ar):
        '''A set of tiles'''
        with VerboseGuard('Reading tile set'):
            self._name = ar.str()
            n = ar.word() if Features().size_size != 8 else ar.size()
            self._ids  = [ar.iden()
                          for _ in range(n)]

    def __str__(self):
        return (self._name + ':' + ','.join([str(i) for i in self._ids]))

    
# --------------------------------------------------------------------
class GBXTileSheet:
    def __init__(self,ar,transparent):
        '''A single image that has multiple tile images in it
        
        X,Y are the tile sizes
        '''
        with VerboseGuard('Reading tile sheet'):
            self._x      = ar.word()
            self._y      = ar.word()
            hasBM        = ar.word()
            self._img    = GBXImage(ar,transparent) if hasBM else None

    def sub(self,off):
        if self._img is None:
            return None

        return self._img._img.crop((0,off,self._x,off+self._y))
    
    def __str__(self):
        bm = str(self._img) if self._img is not None else 'None'
        return (f'c=({self._x:4d},{self._y:4d}) bitmap={bm}')
        

# --------------------------------------------------------------------
class GBXTileManager(CbManager):
    def __init__(self,ar):
        '''Tile manager (including tiles)'''
        with VerboseGuard('Reading tile manager'):
            self._transparent = ar.dword()
            super(GBXTileManager,self).__init__(ar)
            
            ts = lambda ar : GBXTileSheet(ar, self._transparent)
            self._tiledefs    = self._readSub(ar,GBXTileDefinition,
                                              Features().id_size)
            self._tilesets    = self._readSub(ar,GBXTileSet)
            self._tilesheets  = self._readSub(ar,ts)
            self._toStore     = {} # Used in boards, not elsewhere

    def image(self,tileID):
        if tileID is None:
            return None 
        if tileID == 0xFFFF:
            return None

        tileDef = self._tiledefs[tileID]
        tileSht = self._tilesheets[tileDef._full._sheet]
        img     = tileSht.sub(tileDef._full._offset)
        return img

    def store(self,tileID):
        filename = self._toStore.get(tileID,{}).get('filename',None)
        if filename is None:
            filename              = f'tile_{tileID:04d}.png'
            self._toStore[tileID] = {
                'filename': filename,
                'image'   : self.image(tileID)
            }

        return filename
        
        
    def __str__(self):
        return ('Tile manager:\n'
                 + f'  Transparent:  {self._transparent:08x}\n'
                 + super(GBXTileManager,self).__str__()
                 + self._strSub('tiles',self._tiledefs) + '\n'
                 + self._strSub('tile sets',self._tilesets) + '\n'
                 + self._strSub('tile sheets',self._tilesheets))

#
# EOF
#
# ====================================================================
# From piece.py
# ====================================================================
class GBXPieceDef:
    def __init__(self,ar):
        '''Definition of a piece

        FRONT and BACK are tile IDs

        FLAGS is ...
        '''
        with VerboseGuard(f'Reading piece definition'):
            if Features().piece_100:
                n = ar.size()
                self._ids = [ar.iden() for _ in range(n)]
            else:
                self._ids = [ar.word(),ar.word()]
            self._flags = ar.word()


    @property
    def _front(self):
        return self._ids[0]

    @property
    def _back(self):
        return self._ids[1] if len(self._ids) > 1 else 0
    
    def __str__(self):
        return f'Piece: {self._front:04x},{self._back:04x},{self._flags:04x}'
    
# --------------------------------------------------------------------
class GBXPieceSet:
    def __init__(self,ar):
        '''Set of pieces'''
        with VerboseGuard(f'Reading piece set'):
            self._name   = ar.str()
            n            = ar.sub_size()
            self._pieces = [ar.iden() for _ in range(n)]

    def __len__(self):
        return len(self._pieces)

    def __str__(self):
        return (f'{self._name}: '+','.join([str(p) for p in self._pieces]))
    
# --------------------------------------------------------------------
class GBXPieceManager:
    def __init__(self,ar):
        '''Manager of pieces'''
        with VerboseGuard(f'Reading piece manager') as g: 
            self._reserved     = [ar.word() for _ in range(4)]
            g(f'Reserved are {self._reserved}')
            n                  = ar.iden();
            g(f'Will read {n} pieces')
            self._pieces       = [GBXPieceDef(ar) for _ in range(n)]
            n                  = ar.sub_size()
            g(f'Will read {n} sets')
            self._sets         = [GBXPieceSet(ar) for _ in range(n)]

    def __len__(self):
        return len(self._sets)

    def toDict(self,tileManager,strings):
        from math import log10, ceil
        with VerboseGuard(f'Creating dict from piece manager') as gg:
            gg(f'Has {len(self._sets)} and {len(self._pieces)} pieces')
            setDigits   = int(ceil(log10(len(self)+.5)))
            pieceDigits = 1
            for pieceSet in self._sets:
                pieceDigits = max(pieceDigits,
                                  int(ceil(log10(len(pieceSet)+.5))))

            cnt       = 0
            piecesMap = {}
            setList   = []
            ret = {'map': piecesMap,
                   'sets': setList }

            for ips, pieceSet in enumerate(self._sets):
                with VerboseGuard(f'Creating dict from piece set '
                                  f'{pieceSet._name}') as g:
                    setPrefix = f'piece_{ips:0{setDigits}d}'
                    idList    = []
                    setDict   = { 'description': pieceSet._name.strip(),
                                  'pieces':      idList }
                    setList.append(setDict)
                    
                    for ipc, pieceID in enumerate(pieceSet._pieces):
                        
                        piecePrefix = f'{setPrefix}_{ipc:0{pieceDigits}d}'
                        pieceDef    = self._pieces[pieceID]
                        tmpStr      = strings._id2str.get(pieceID,'')
                        pieceDesc   = tmpStr.replace('\r','').replace('\n',', ').replace('/','\\/')
                        pieceDict   = {}
                        if pieceDesc != '':
                            pieceDict['description'] = pieceDesc
                        cnt += 1
                        # pieceList.append(pieceDict)
                        idList   .append(pieceID)
                        
                        # print(f'{pd}  => "{tr}"')
                        for tileId,which in zip([pieceDef._front,
                                                 pieceDef._back],
                                                ['front',
                                                 'back']):                    
                            img = tileManager.image(tileId)
                    
                            if img is None:
                                continue
                    
                            sav     = f'{piecePrefix}_{which}.png'
                            setname = pieceSet._name.strip()\
                                .replace('\n',' ')\
                                .replace('\r',' ')\
                                .replace('/','\\/')
                            gg(f'Set name, escaped: "{setname}"')
                            pieceDict[which] = {
                                'image':     img,
                                'filename':  sav,
                                'set':       setname }
                        piecesMap[pieceID] = pieceDict
                        g(f'{pieceID}: {pieceDict}')

            gg(f'{list(piecesMap.keys())}')
            return ret
    
        
    def __str__(self):
        return ('Piece manager:\n'
                +f'Reserved: {self._reserved}\n'
                +f'# pieces: {len(self._pieces)}\n  '
                +'\n  '.join([str(p) for p in self._pieces])+'\n'
                +f'# piece sets: {len(self._sets)}\n  '
                +'\n  '.join([str(p) for p in self._sets])
                )

# --------------------------------------------------------------------
class GSNPieceEntry:
    def __init__(self,ar,vers,i):
        '''Manager of pieces'''
        with VerboseGuard(f'Reading piece # {i:3d} ({vers//256}.{vers%256})'):
            self._side   = ar.byte()
            self._facing = ar.word()
            self._owner  = ar.word() if vers < num_version(3,10) else ar.dword()

    def __str__(self):
        return f'Piece: {self._side}, {self._facing:3d}, {self._owner:08x}'
    
# --------------------------------------------------------------------
class GSNPieceTable:
    def __init__(self,ar,vers):
        '''Manager of pieces'''
        with VerboseGuard(f'Reading piece table'):
            self._reserved     = [ar.word() for _ in range(4)] 
            n                  = ar.word()#sub_size()
            if Features().piece_100:
                dummy          = ar.word();
            self._pieces       = [GSNPieceEntry(ar,vers,i) for i in range(n)]
            
    def __str__(self):
        pl = '\n    '.join([str(s) for s in self._pieces])
        return (f'Piece table: {self._reserved} {len(self._pieces)}'
                f'\n    {pl}\n')
#
# EOF
#
# ====================================================================
# From mark.py

# ====================================================================
class GBXMarkDef:
    def __init__(self,ar):
        '''Definition of a mark'''
        with VerboseGuard(f'Reading mark definition'):
            self._id    = ar.iden()
            self._flags = ar.word()

    def __str__(self):
        return f'Mark: {self._id:04x},{self._flags:04x}'
    
# --------------------------------------------------------------------
class GBXMarkSet:
    def __init__(self,ar):
        '''Set of marks'''
        with VerboseGuard(f'Reading mark set'):
            self._name   = ar.str()
            self._viz    = ar.word()
            n            = ar.sub_size()
            self._marks = [ar.iden() for _ in range(n)]

    def __len__(self):
        return len(self._marks)

    def __str__(self):
        return (f'{self._name}: '+','.join([str(p) for p in self._marks]))
    
# --------------------------------------------------------------------
class GBXMarkManager:
    def __init__(self,ar):
        '''Manager of marks'''
        with VerboseGuard(f'Reading mark manager'):
            self._reserved     = [ar.word() for _ in range(4)] 
            n                  = ar.iden()
            self._marks        = [GBXMarkDef(ar) for _ in range(n)]
            n                  = ar.sub_size()
            self._sets         = [GBXMarkSet(ar) for _ in range(n)]
        
    def __len__(self):
        return len(self._sets)

    def toDict(self,tileManager,strings):
        from math import log10, ceil
        with VerboseGuard(f'Creating dict from mark manager'):
            setDigits  = int(ceil(log10(len(self)+.5)))
            markDigits = 1
            for markSet in self._sets:
                markDigits = max(markDigits,
                                 int(ceil(log10(len(markSet)+.5))))

            marksMap  = {}
            setList   = []
            ret = {'map': marksMap,
                   'sets': setList }
            
            for ips, markSet in enumerate(self._sets):
                with VerboseGuard(f'Creating dict mark set {markSet._name}'):
                    setPrefix = f'mark_{ips:0{setDigits}d}'
                    idList    = []
                    setDict   = { 'description': markSet._name.strip(),
                                  'marks':       idList }
                    setList.append(setDict)
                    
                    for ipc, markID in enumerate(markSet._marks):
                        markPrefix = f'{setPrefix}_{ipc:0{markDigits}d}'
                        markDef    = self._marks[markID]
                        tmpStr     = strings._id2str.get(markID|0xF0000000,'')
                        markDesc   = tmpStr.replace('\r','').replace('\n',', ')
                        markDict   = {}
                        if markDesc != '':
                            markDict['description'] = markDesc
                        marksMap[markID] = markDict
                        idList  .append(markID)
                        
                        img = tileManager.image(markDef._id)
                    
                        if img is None:
                            continue
                    
                        sav     = f'{markPrefix}.png'
                        markDict.update({'image':     img,
                                         'filename':  sav })

            return ret
    
    def __str__(self):
        return ('Mark manager:\n'
                +f'Reserved: {self._reserved}\n'
                +f'# marks: {len(self._marks)}\n  '
                +'\n  '.join([str(p) for p in self._marks])+'\n'
                +f'# mark sets: {len(self._sets)}\n  '
                +'\n  '.join([str(p) for p in self._sets])
                )

#
# EOF
#
# ====================================================================
# From draw.py

# ====================================================================
class GBXDraw:
    def __init__(self,ar):
        '''Base class for drawing objects'''
        self._flags  = ar.dword()
        self._left   = ar.word()
        self._top    = ar.word()
        self._right  = ar.word()
        self._bottom = ar.word()

    def isSecondPass(self):
        return self._flags & 0x00000008

    def bbWidth(self):
        return self._right - self._left

    def bbHeight(self):
        return self._bottom - self._top

    def centerX(self):
        return (self._left + self._right)//2

    def centerY(self):
        return (self._top + self._bottom)//2

    def center(self):
        return (self.centerX(),self.centerY())

    def upperLeft(self):
        return (self._left,self._top)

    def lowerRight(self):
        return (self._right,self._bottom)

    def bbSize(self):
        return (self.bbWidth(),self.bbHeight())

    @classmethod
    def hex(cls,val):
        if val == 0xFF000000:
            h = 'none'
        else:
            b = (val >> 16) & 0xFF
            g = (val >>  8) & 0xFF
            r = (val >>  0) & 0xFF
            h = f'rgb({r},{g},{b})'
        return h

    def toDict(self,calc):
        return None

    def baseDict(self):
        return {
            'left':   self._left,
            'top':    self._top,
            'right':  self._right,
            'bottom': self._bottom,
            'x':      self.centerX(),
            'y':      self.centerY()
        }
    
    def svg(self,dwg,g,defmap):
        print(f'{self.__class__}.svg method not implemented')
        pass
    
    def __str__(self):
        return (f'Flags:{self._flags:08x} '
                + f'({self._left},{self._top})x({self._right},{self._bottom})')

# --------------------------------------------------------------------
class GBXRectangle(GBXDraw):
    def __init__(self,ar):
        '''Draw a rectangle'''
        with VerboseGuard(f'Reading rectangle'):
            super(GBXRectangle,self).__init__(ar)
            self._fill  = ar.dword()
            self._line  = ar.dword()
            self._width = ar.word()

    def svg(self,dwg,g,defmap):
        r = g.add(dwg.rect(insert=(self.upperLeft()),
                           size=(self.bbSize()),
                           fill=self.hex(self._fill),
                           stroke=self.hex(self._line),
                           stroke_width=self._width))
        
    def __str__(self):
        return 'Rectangle: '+super(GBXRectangle,self).__str__()

# --------------------------------------------------------------------
class GBXEllipse(GBXRectangle):
    def __init__(self,ar):
        '''Draw an ellipse'''
        with VerboseGuard(f'Reading ellipse'):
            super(GBXEllipse,self).__init__(ar)

    def svg(self,dwg,g,defmap):
        '''Create SVG object'''
        g.add(dwg.ellipse(center=(self.centerX(),self.centerY()),
                          r=(self.bbWidth(),self.bbHeight()),
                          fill=self.hex(self._fill),
                          stroke=self.hex(self._line),
                          stroke_width=self._width))
    def __str__(self):
        return 'Ellipse: '+super(GBXRectangle,self).__str__()
        
# --------------------------------------------------------------------
class GBXLine(GBXDraw):
    def __init__(self,ar):
        '''Draw a line'''
        with VerboseGuard(f'Reading line'):
            super(GBXLine,self).__init__(ar)
            self._x0    = ar.word()
            self._y0    = ar.word()
            self._x1    = ar.word()
            self._y1    = ar.word()
            self._line  = ar.dword()
            self._width = ar.word()

    def svg(self,dwg,g,defmap):
        '''Create SVG object'''
        g.add(dwg.line(start=(self._x0,self._y0),
                       end=(self._x1,self._y1),
                       stroke=self.hex(self._line),
                       stroke_width=self._width))
        
              
    def __str__(self):
        return 'Line: ' + super(GBXLine,self).__str__()
        # f'({self._x0},{self._y0}) -> ({self._x1},{self._y1})')
    
        
# --------------------------------------------------------------------
class GBXTile(GBXDraw):
    def __init__(self,ar):
        '''Draw a tile'''
        with VerboseGuard(f'Reading tile'):
            super(GBXTile,self).__init__(ar)
            self._id = ar.word()

    def svgDef(self,dwg,tileManager,markManager,defmap):
        '''Create SVG definition from image'''
        if self._id in defmap:
            return

        img  = tileManager.image(self._id)
        data = GBXImage.b64encode(img)
        if data is None:
            return

        iden = f'tile_{self._id:04x}'
        img  = dwg.defs.add(dwg.image(id=iden,href=(data),
                                      size=(img.width,img.height)))
        defmap[self._id] = img
        
    def svg(self,dwg,g,defmap):
        '''Create SVG object'''
        if self._id not in defmap: return
        
        g.add(dwg.use(defmap[self._id],
                      insert=(self._left,self._top)))
        
    def __str__(self):
        return f'Tile: {self._id} ' + super(GBXTile,self).__str__()
    
# --------------------------------------------------------------------
class GBXText(GBXDraw):
    def __init__(self,ar):
        '''Draw text'''
        with VerboseGuard(f'Reading text'):
            super(GBXText,self).__init__(ar)
            self._angle   = ar.word()
            self._color   = ar.dword()
            self._text    = ar.str()
            self._font    = CbFont(ar)

    def svg(self,dwg,g,defmap):
        '''Create SVG object'''
        g.add(dwg.text(self._text,
                       insert=(self._left,self._bottom),
                       rotate=[self._angle],
                       fill=self.hex(self._color),
                       font_family='monospace' if self._font._name == '' else self._font._name,
                       font_size=self._font._size,
                       font_weight='bold' if self._font.isBold() else 'normal',
                       font_style='italic' if self._font.isItalic() else 'normal',
                       text_decoration='underline' if self._font.isUnderline() else 'none'))
        
    def __str__(self):
        return f'Text: "{self._text}" '+super(GBXText,self).__str__()
    
# --------------------------------------------------------------------
class GBXPolyline(GBXDraw):
    def __init__(self,ar):
        '''Draw a polyline'''
        with VerboseGuard(f'Reading polyline'):
            super(GBXPolyline,self).__init__(ar)
            self._fill   = ar.dword()
            self._line   = ar.dword()
            self._width  = ar.word()
            n            = (ar.word() if Features().size_size != 8 else
                            ar.size())
            self._points = [[ar.word(),ar.word()] for _ in range(n)]

    def svg(self,dwg,g,defmap):
        '''Create SVG object'''
        g.add(dwg.polyline(self._points,
                           fill=self.hex(self._fill),
                           stroke=self.hex(self._line),
                           stroke_width=self._width))

    def __str__(self):
        return f'Polyline: {len(self._points)} '+super(GBXPolyline,self).__str__()
    
# --------------------------------------------------------------------
class GBXBitmap(GBXDraw):
    CNT = 0
    
    def __init__(self,ar):
        '''Draw a bitmap'''
        with VerboseGuard(f'Reading bitmap'):
            super(GBXBitmap,self).__init__(ar)
            sav = f'B{GBXBitmap.CNT:04d}.png'
            GBXBitmap.CNT += 1
            self._scale = ar.word()
            self._img   = GBXImage(ar,save=None)

    def svg(self,dwg,g,defmap):
        '''Create SVG object'''
        data = GBXImage.b64encode(self._img._img)
        size = self._img._img.width, self._img._img.height
        g.add(dwg.image(insert=(self._left,self._top),
                        size=size,
                        href=(data)))
        
    def __str__(self):
        return f'Bitmap: {self._img} ' + super(GBXBitmap,self).__str__()
    
# --------------------------------------------------------------------
class GBXPiece(GBXDraw):
    def __init__(self,ar):
        '''Draw a piece'''
        with VerboseGuard(f'Reading piece (draw)'):
            super(GBXPiece,self).__init__(ar)
            self._id = ar.iden()

    def toDict(self,calc=None):
        d = {'type': 'Piece',
             'id':    self._id,
             'pixel': self.baseDict()
             }
        if calc is not None:
            d['grid'] = calc(*self.center())
        return d

    def __str__(self):
        return f'Piece: {self._id} ' + super(GBXPiece,self).__str__()
    
# --------------------------------------------------------------------
class GBXMark(GBXDraw):
    def __init__(self,ar):
        '''Draw a mark tile'''
        with VerboseGuard(f'Reading mark (draw)'):
            super(GBXMark,self).__init__(ar)
            self._id  = ar.size()
            self._mid = ar.iden()
            self._ang = ar.word()

    def toDict(self,calc=None):
        d = {'type': 'Mark',
             'id':    self._mid,
             'pixel': self.baseDict()
             }
        if calc is not None:
            d['grid'] = calc(*self.center())
        return d
    def svgDef(self,dwg,tileManager,markManager,defmap):
        '''Create SVG def from mark'''
        if self._id in defmap:
            return

        data = GBXImage.b64encode(tileManager.image(self._id))
        if data is None:
            return

        iden = f'mark_{self._id:04x}'
        img  = dwg.defs.add(dwg.image(id=iden,href=(data)))
        defmap[self._id] = img
        
    def svg(self,dwg,g,defmap):
        '''Create SVG object'''
        if self._id not in defmap: return
        
        g.add(dwg.use(defmap[self._id],
                      insert=(self._left,self._top)))
        
    def __str__(self):
        return f'Mark: {self._id}/{self._mid} ' + super(GBXMark,self).__str__()
    
# --------------------------------------------------------------------
class GBXLineObj(GBXLine):
    def __init__(self,ar):
        '''Line object via reference'''
        with VerboseGuard(f'Reading line object'):
            super(GBXLineObj,self).__init__(ar)

            self._id  = ar.iden()

    def __str__(self):
        return f'Line: {self._id} ' + super(GBXLineObj,self).__str__()

    
# --------------------------------------------------------------------
class GBXDrawList:
    RECT     = 0
    ELLIPSE  = 1
    LINE     = 2
    TILE     = 3
    TEXT     = 4
    POLYLINE = 5
    BITMAP   = 6
    PIECE    = 0x80
    MARK     = 0x81
    LINEOBJ  = 0x82

    TMAP    = { RECT:      GBXRectangle,
                ELLIPSE:   GBXEllipse,
                LINE:      GBXLine,
                TILE:      GBXTile,
                TEXT:      GBXText,
                POLYLINE:  GBXPolyline,
                BITMAP:    GBXBitmap,
                PIECE:     GBXPiece,
                MARK:      GBXMark,
                LINEOBJ:   GBXLineObj}

    def __init__(self,ar):
        '''A list of drawn objects'''
        with VerboseGuard(f'Reading draw list'):
            n = ar.sub_size()

            self._obj = [self._readObj(ar) for n in range(n)]

    def toDict(self,calc=None):
        with VerboseGuard(f'Making dictionary from draw list at pass'):
            ret = []
            for i in self._obj:
                d = i.toDict(calc)
                if d is None:
                    continue

                ret.append(d)

            return ret
        
    def _readObj(self,ar):
        '''Read one object'''
        tpe  = ar.word()
        cls  = self.TMAP.get(tpe,None)
        if cls is None:
            raise RuntimeError(f'Unknown type of draw: {tpe}')

        return cls(ar)

    def svgDefs(self,dwg,tileManager,markManager,defmap):
        '''Create SVG defs'''
        with VerboseGuard(f'Create SVG defs from draw list'):
            for i in self._obj:
                if type(i) not in [GBXTile,GBXMark]: continue

                i.svgDef(dwg,tileManager,markManager,defmap)

    def svg(self,dwg,g,passNo,defmap):
        '''Create SVG objects'''
        with VerboseGuard(f'Drawing SVG from draw list at pass {passNo}'
                          f' ({len(self._obj)} objects)') as gg:
            for i in self._obj:
                if passNo == 1 and i.isSecondPass():
                    continue
                elif passNo == 2 and not i.isSecondPass():
                    continue
                gg(f'Drawing {i}')
                i.svg(dwg,g,defmap)
            
    def __str__(self):
        return '\n        '.join([str(o) for o in self._obj])

#
# EOF
#
# ====================================================================
# From cell.py

# ====================================================================
class GBXCellGeometry:
    RECTANGLE        = 0
    HORIZONTAL_BRICK = 1
    VERTICAL_BRICK   = 2
    HEXAGON          = 3
    SIDEWAYS_HEXAGON = 4
    STAGGER_OUT      = 0
    STAGGER_IN       = 1
    TYPES = {
        RECTANGLE       : 'rectangle',
        HORIZONTAL_BRICK: 'horizontal brick',
        VERTICAL_BRICK  : 'vertical brick',
        HEXAGON         : 'hexagon',
        SIDEWAYS_HEXAGON: 'sideways hexagon'
    }
    STAGGERS = {
        STAGGER_OUT: 'out',
        STAGGER_IN:  'in'
    }

    def __init__(self,ar):
        '''The geometry of cells'''
        with VerboseGuard('Reading cell geometry'):
            from numpy import max
            
            self._type      = ar.word()
            self._stagger   = ar.word()
            self._left      = ar.word()
            self._top       = ar.word()
            self._right     = ar.word()
            self._bottom    = ar.word()
            n               = 7 if self._type > 2 else 5
            self._points    = [[ar.word(),ar.word()] for _ in range(n)]
            size            = max(self._points,axis=0)
            self._dx        = int(size[0])
            self._dy        = int(size[1])
            self._size      = [self._dx,self._dy]
            
            if self._type == self.HEXAGON:
                self._dx = int(0.75 * self._dx)
            elif self._type == self.SIDEWAYS_HEXAGON:
                self._dy = int(0.75 * self._dy)

    def toDict(self):
        from numpy import max
        return {'shape':      self.TYPES.get(self._type,''),
                'stagger':    self.STAGGERS.get(self._stagger,''),
                'size':       self._size,
                'bounding box (ltrb)':
                (self._left, self._top, self._right, self._bottom),
                'points':     self._points }

    def svgDef(self,dwg):
        with VerboseGuard('Defining SVG cell geometry'):
            if self._type in [0,1,2]:
                return dwg.defs.add(dwg.rect(id='cell',
                                             size=(self._right-self._left,
                                                   self._bottom-self._top)))
        
            return dwg.defs.add(dwg.polygon(self._points,id='cell'))

    def translate(self,row,col,center=False):
        x = col * self._dx
        y = row * self._dy
        if self._type == self.RECTANGLE: # No offset for rectangles
            return x,y
        if self._type in [self.HORIZONTAL_BRICK,self.SIDEWAYS_HEXAGON]:
            x += self._dx//2 if (row % 2) != self._stagger else 0
        if self._type in [self.VERTICAL_BRICK,self.HEXAGON]:
            y += self._dy//2 if (col % 2) != self._stagger else 0
        if center:
            x += self._size[0]//2
            y += self._size[1]//2
        return x,y

    def inverse(self,x,y):
        col = x / self._dx
        row = y / self._dy
        if self._type in [self.HORIZONTAL_BRICK,self.SIDEWAYS_HEXAGON]:
            col -= .5 if (int(row) % 2) != self._stagger else 0
        if self._type in [self.VERTICAL_BRICK,self.HEXAGON]:
            row -= .5  if (int(col) % 2) != self._stagger else 0

        # CyberBoard start at 1
        return int(row)+1, int(col)+1 
        

    def boardSize(self,nrows,ncols):
        w = ncols * self._dx
        h = nrows * self._dy

        if self._type in [2,3]:
            h += self._dy // 2
        if self._type in [1,4]:
            w += self._dx // 2
        if self._type == 3:
            w += self._dx // 3
        if self._type == 4:
            h += self._dy // 3

        return w+1,h+1
    
    def __str__(self):
        return (f'type: {self.TYPES.get(self._type,"")} '
                + f'stagger: {self.STAGGERS.get(self._stagger,"")} '
                + f'({self._left},{self._top})x({self._right},{self._bottom}) '
                + f': [{self._points}]')

        
# --------------------------------------------------------------------
class GBXCell:
    def __init__(self,ar,row,column):
        '''A single cell'''
        with VerboseGuard(f'Reading cell row={row} column={column}'):
            self._row    = row
            self._column = column
            if Features().id_size == 4:
                self._is_tile = ar.byte();
            self._tile   = ar.dword()
            if Features().id_size != 4:
                self._is_tile  = (self._tile >> 16) == 0xFFFF;
                if self._is_tile:
                    self._tile = self._tile & 0xFFFF

    def tileID(self):
        if not self._is_tile:
            return None
        return self._tile

    def color(self):
        if self._is_tile:
            return None
        return GBXDraw.hex(self._tile)

    def toDict(self,tileManager,calc=None):
        d = {'row': self._row,
             'column': self._column}
        if not self._is_tile:
            d['color'] = GBXDraw.hex(self._tile)
        else:
            d['tile'] = tileManager.store(self._tile)
        if calc is not None:
            d['pixel'] = calc.translate(self._row,self._column,True)
        return d
    
    
    def svgDef(self,dwg,tileManager,ptm):
        tileID = self.tileID()
        if tileID is None:
            return

        if tileID in ptm: # Have it
            return 

        with VerboseGuard(f'Defining SVG pattern'):
            img  = tileManager.image(tileID)
            data = GBXImage.b64encode(img)
            if data is None:
                return
            
            iden = f'terrain_{tileID:04x}'
            pat  = dwg.defs.add(dwg.pattern(id=iden,
                                            size=(img.width,img.height)))
            pat.add(dwg.image(href=(data)))
            ptm[tileID] = pat

    def svg(self,dwg,g,cell,geom,ptm):
        tileID = self.tileID()
        if tileID is not None:
            fill = ptm[tileID].get_paint_server()
        else:
            fill = self.color()

        trans = geom.translate(self._row,self._column)
        iden  = f'cell_bg_{self._column:03d}{self._row:03d}'
        g.add(dwg.use(cell,insert=trans,fill=fill,id=iden))
        
    def svgFrame(self,dwg,g,cell,geom,color):
        trans = geom.translate(self._row,self._column)
        iden  = f'cell_fg_{self._column:03d}{self._row:03d}'
        g.add(dwg.use(cell,
                      insert=trans,
                      stroke=GBXDraw.hex(color),
                      fill='none',
                      id=iden))
        

    def __str__(self):
        return f'({self._row:02d},{self._column:02d}): {self._tile:08x}'

#
# EOF
#
# ====================================================================
# From board.py

# --------------------------------------------------------------------
class GBXBoardCalculator:
    def __init__(self,board):
        self._geometry  = board._full
        self._nRows     = board._nRows
        self._nCols     = board._nCols
        self._rowOffset = board._rowOffset
        self._colOffset = board._colOffset
        self._rowInvert = board._rowInvert
        self._colInvert = board._colInvert

    def __call__(self,x,y):
        # Shift depending on grid type and stagger
        row, col = self._geometry.inverse(x,y)
        if self._rowInvert:
            row = self._nRows - row - 1
        if self._colInvert:
            col = self._nCols - col - 1

        return row+self._rowOffset, col+self._colOffset

# --------------------------------------------------------------------
class GBXBoard:
    def __init__(self,ar):
        '''A board'''
        with VerboseGuard(f'Reading board') as g:
            self._serial          = ar.iden()
            self._visible         = ar.word()
            self._snap            = ar.word()
            self._xSnap           = ar.dword()
            self._ySnap           = ar.dword()
            self._xSnapOffset     = ar.dword()
            self._ySnapOffset     = ar.dword()
            self._maxLayer        = ar.word()
            self._background      = ar.dword()
            self._name            = ar.str()
            hasDraw               = ar.word()
            self._baseDraw        = GBXDrawList(ar) if hasDraw else None
                
            self._showCellBorder  = ar.word()
            self._topCellBorder   = ar.word()
            self._reserved        = [ar.word() for _ in range(4)]
            self._reserved2       = None
            self._rowOffset       = 0
            self._colOffset       = 0
            self._rowInvert       = False
            self._colInvert       = False
            self._nRows           = 0
            self._nCols           = 0
            self._transparent     = False
            self._numbers         = 0
            self._trackCell       = False
            self._frameColor      = 0xFF000000
            self._full            = None
            self._half            = None
            self._small           = None
            self._map             = []
            self._topDraw         = None
            
            hasArray              = ar.word()
            if hasArray != 0:
                self._reserved2   = [ar.word() for _ in range(4)]
                self._rowOffset   = ar.word()
                self._colOffset   = ar.word()
                self._rowInvert   = ar.word()
                self._colInvert   = ar.word()
                self._nRows       = ar.int(Features().sub_size)
                self._nCols       = ar.int(Features().sub_size)
                self._transparent = ar.word()
                self._numbers     = ar.word()
                self._trackCell   = ar.word()
                self._frameColor  = ar.dword()
            
                self._full        = GBXCellGeometry(ar)
                self._half        = GBXCellGeometry(ar)
                self._small       = GBXCellGeometry(ar)
            
                self._map = [[GBXCell(ar,row,col) for col in range(self._nCols)]
                             for row in range(self._nRows)]
            
            hasDraw              = ar.word()
            self._topDraw        = GBXDrawList(ar) if hasDraw else None
            g(f'Board background read: {self._background:06x}, frame color: {self._frameColor:06x}')

    def toDict(self,tileManager,markManager,strings,no,boardDigits,
               alsoMap=True):
        from io import StringIO
        
        with VerboseGuard(f'Making dict of board {self._name}') as g:
            sav = f'board_{no:0{boardDigits}d}.svg'
            g(f'File to save in: {sav}')
            dct = {'name':               self._name,
                   'serial':             self._serial,
                   'visible':            self._visible,
                   'snap':  {
                       'enable':         self._snap,
                       'x': { 
                           'distance':   self._xSnap,
                           'offset':     self._xSnapOffset
                       },
                       'y': {
                           'distance':   self._ySnap,
                           'offset':     self._ySnapOffset
                       }
                   },
                   'max layer':          self._maxLayer,
                   'cell border': {
                       'visible':        self._showCellBorder,
                       'on top layer':   self._topCellBorder,
                   },
                   'rows': {
                       'size':           self._nRows,
                       'offset':         self._rowOffset,
                       'inverted':       self._rowInvert
                   },
                   'columns': {
                       'size':           self._nCols,
                       'offset':         self._colOffset,
                       'inverted':       self._colInvert
                   },
                   'cells': {
                       'transparent':    self._transparent,
                       'foreground':     self._frameColor,
                   },
                   'numbering': {
                       'order':   'V' if self._numbers % 2 == 0 else 'H',
                       'padding': self._numbers in [2,3],
                       'first':   'A' if self._numbers in [4,5] else 'N'
                   }
                }
            if self._full is not None:
                dct['cells']['geometry'] = self._full.toDict()
            if alsoMap and self._map is not None:
                dct['cells']['list'] = [[c.toDict(tileManager,self._full)
                                         for c in row]
                                        for row in self._map]
            
            
            sav = f'board_{no:0{boardDigits}d}.svg'
            img = self.drawing(sav,
                               tileManager=tileManager,
                               markManager=markManager)
            # img.save(pretty=True)

            stream = StringIO()
            img.write(stream,pretty=True)
            
            dct['filename'] = sav
            dct['image']    = stream.getvalue()#img.tostring()
            dct['size']     = self._full.boardSize(self._nRows,self._nCols)
            
            return dct

    def drawing(self,sav,tileManager,markManager,*args,**kwargs):
        from svgwrite import Drawing
        from svgwrite.base import Title
        with VerboseGuard(f'Making SVG of board {self._name}') as g:
            size  = self._full.boardSize(self._nRows,self._nCols)
            dwg   = Drawing(filename=sav,size=size)
            frame, defMap, patMap = self.defs(dwg,tileManager,markManager)
            
            # Draw background
            g(f'Board background: {self._background:06x} {GBXDraw.hex(self._background)}')
            dwg.add(Title(self._name))
            dwg.add(dwg.rect(id='background',
                             insert=(0,0),
                             size=size,
                             fill=GBXDraw.hex(self._background)
                             #f'#{self._background:06x}')
                             ))
            # GBXDraw.hex(self._background)

            g('Drawing base layer')
            bse  = self.base (dwg, 0, defMap)
            g('Drawing cells')
            grd  = self.cells(dwg, frame, patMap)
            if self._showCellBorder and not self._topCellBorder:
                self.borders(dwg,frame)
            g('Drawing top layer')
            top1 = self.top  (dwg, 1, defMap)
            if self._showCellBorder and self._topCellBorder:
                self.borders(dwg,frame)
            top2 = self.top  (dwg, 2, defMap)
                    
            return dwg

    def defs(self,dwg,tileManager,markManager):
        defMap         = {}
        patMap         = {}
        frame          = self._full.svgDef(dwg)
        defMap['cell'] = frame

        # Get defininitions from base layer 
        if self._baseDraw:
            self._baseDraw.svgDefs(dwg,
                                   tileManager,
                                   markManager,
                                   defMap)
        # Get definitions from cell layer 
        for row in self._map:
            for cell in row:
                cell.svgDef(dwg,tileManager,patMap)
            
        # Get definitions from top layer 
        if self._topDraw:
            self._topDraw.svgDefs(dwg,
                                  tileManager,
                                  markManager,
                                  defMap)

        return frame, defMap, patMap

    def base(self,dwg,passNo,defMap):
        bse  = dwg.add(dwg.g(id=f'base_{passNo:02d}'))
        if self._baseDraw:
            self._baseDraw.svg(dwg,bse,passNo,defMap)

        return bse
        
    def cells(self,dwg,frame,patMap):
        grd  = dwg.add(dwg.g(id='grid'))
        for row in self._map:
            for cell in row:
                cell.svg(dwg,grd,frame,self._full,patMap)

        return grd

    def borders(self,dwg,frame):
        brd  = dwg.add(dwg.g(id='borders'))
        for row in self._map:
            for cell in row:
                cell.svgFrame(dwg,brd,frame,self._full,self._frameColor)

        return brd
        
    def top(self,dwg,passNo,defMap):
        top  = dwg.add(dwg.g(id=f'top_{passNo:02d}'))
        if self._topDraw:
            self._topDraw.svg (dwg,top,passNo,defMap)
        
        return top

    def __str__(self):
        return (f'GBXBoard: {self._name}\n'
                f'      serial:           {self._serial}\n'
                f'      visible:          {self._visible}\n'
                f'      snap:             {self._snap}\n'
                f'      xSnap:            {self._xSnap}\n'
                f'      ySnap:            {self._ySnap}\n'
                f'      xSnapOffset:      {self._xSnapOffset}\n'
                f'      ySnapOffset:      {self._ySnapOffset}\n'
                f'      maxLayer:         {self._maxLayer}\n'
                f'      background:       {self._background:08x}\n'
                f'      Base draws:       {self._baseDraw}\n'
                f'      Show cell border: {self._showCellBorder}\n'
                f'      Top cell border:  {self._topCellBorder}\n'
                f'      Reserved:         {self._reserved}\n'
                f'      Reserved2:        {self._reserved}\n'
                f'      Row offset:       {self._rowOffset}\n'
                f'      Column offset:    {self._colOffset}\n'
                f'      Row invert:       {self._rowInvert}\n'
                f'      Colunn invert:    {self._colInvert}\n'
                f'      # Rows:           {self._nRows}\n'
                f'      # Cols:           {self._nCols}\n'
                f'      Transparent:      {self._transparent}\n'
                f'      Numbers:          {self._numbers}\n'
                f'      Track cells:      {self._trackCell}\n'
                f'      Frame color:      {self._frameColor:08x}\n'
                f'      Full geometry:    {self._full}\n'
                f'      Half geometry:    {self._half}\n'
                f'      Small geometry:   {self._small}\n'
                f'      Top draws:        {self._topDraw}'
                )
    
            
            
        
# --------------------------------------------------------------------
class GBXBoardManager(CbManager):
    def __init__(self,ar):
        '''Manager of boards'''
        with VerboseGuard(f'Reading board manager'):
            self._nextSerial  = ar.iden()
            super(GBXBoardManager,self).__init__(ar)
            # print(Features().id_size)
            self._boards = self._readSub(ar,GBXBoard)

    def __len__(self):
        return len(self._boards)

    def bySerial(self,serial):
        for b in self._boards:
            if b._serial == serial:
                return b

        return None
    
    def toDict(self,tileManager,markManager,strings):
        from math import log10, ceil
        with VerboseGuard(f'Making dict board manager'):
            boardDigits = int(ceil(log10(len(self)+.5)))

            return {b._serial:
                    b.toDict(tileManager,markManager,strings,no,boardDigits)
                    for no, b in enumerate(self._boards)}
    
    def __str__(self):
        return ('GBXBoard manager:\n'
                + f'  Next serial:  {self._nextSerial:08x}\n'
                + super(GBXBoardManager,self).__str__()
                + self._strSub('boards',self._boards))

# --------------------------------------------------------------------
class GSNGeomorphicElement:
    def __init__(self,ar):
        with VerboseGuard('Reading geomorphic element'):
            self._serial = ar.word()
        
    def __str__(self):
        return f'GSNGeomorphicElement: {self._serial}'
    
# --------------------------------------------------------------------
class GSNGeomorphicBoard:
    def __init__(self,ar):
        with VerboseGuard('Reading geomorphic board'):
            self._name     = ar.str()
            self._nRows    = ar.word()
            self._nCols    = ar.word()
            n              = ar.word()
            self._elements = [GSNGeomorphicElement(ar) for _ in range(n)]
        
    def __str__(self):
        pl = '\n    '.join([str(s) for s in self._elements])
        return (f'GeomorphicBoard: {self._name}\n'
                f'  Size: {self._nRows}x{self._nCols}\n'
                f'  Elements:\n    {pl}\n')
    
# --------------------------------------------------------------------
class GSNBoard:
    def __init__(self,ar,vers):
        with VerboseGuard(f'Reading scenario board {vers//256}.{vers%256}'):
            hasGeo                 = ar.byte()
            self._geo              = GSNGeomorphicBoard(ar) if hasGeo else None
            self._serial           = ar.iden()
            self._snap             = ar.word()
            self._xSnap            = ar.dword()
            self._ySnap            = ar.dword()
            self._xSnapOffset      = ar.dword()
            self._ySnapOffset      = ar.dword()
            self._xStagger         = ar.word()
            self._yStagger         = ar.word()
            self._piecesVisible    = ar.word()
            self._blockBeneath     = ar.word()
            self._rotate180        = ar.word()
            self._showTiny         = ar.word()
            self._indicatorsVisible= ar.word()
            self._cellBorders      = ar.word()
            self._smallCellBorders = ar.word()
            self._enforceLocks     = ar.word()
            self._plotLineColor    = ar.dword()
            self._plotLineWidth    = ar.word()
            self._lineColor        = ar.dword()
            self._lineWidth        = ar.word()
            self._textColor        = ar.dword()
            self._textBoxColor     = ar.dword()
            self._font             = CbFont(ar)
            self._gridCenters      = ar.word()
            self._snapMove         = ar.word()
            self._indactorsTop     = ar.word()
            self._openOnLoad       = ar.word()
            self._prevPlotMode     = ar.word()
            self._prevPlotX        = ar.word()
            self._prevPlotY        = ar.word()
            self._ownerMask        = (ar.word() if vers < num_version(3,10) else
                                      ar.dword())
            self._restrictToOwner  = ar.word()
            self._pieces           = GBXDrawList(ar)
            self._indicators       = GBXDrawList(ar)
        
        
    def toDict(self,boardManager):
        board = (None if boardManager is None else
                 boardManager.bySerial(self._serial))
        geom  = None if board is None else board._full
        calc  = None if geom  is None else GBXBoardCalculator(board)
        
        return {
            'onload':             self._openOnLoad != 0,
            'snap':  {
                'enable':         self._snap,
                'onmove':         self._snapMove != 0,
                'gridCenter':     self._gridCenters != 0,
                'x': { 
                    'distance':   self._xSnap,
                    'offset':     self._xSnapOffset
                },
                'y': {
                    'distance':   self._ySnap,
                    'offset':     self._ySnapOffset
                }
            },
            'moves': {
                'color':          self._plotLineColor,
                'width':          self._plotLineWidth
            },
            'stacking':           [self._xStagger, self._yStagger],
            'owner':              self._ownerMask,
            'restrict':           self._restrictToOwner != 0,
            'grid': {
                'show':           self._cellBorders != 0,
                'color':          self._lineColor,
                'width':          self._lineWidth
            },
            'pieces':             self._pieces.toDict(calc),
            'indicators':         self._indicators.toDict(calc)
        }
    
    def __str__(self):
        return (f'ScenarioBoard: {self._serial}'
                f'      Geomorphic: {"None" if self._geo is None else self._geo}\n'
                f'      Font:       {self._font}\n'
                f'      Pieces:\n{str(self._pieces)}\n'
                f'      Indicators:\n{str(self._indicators)}')
    
# --------------------------------------------------------------------
class GSNBoardManager:    
    def __init__(self,ar,vers):
        with VerboseGuard(f'Reading scenario board manager') as g:
            self._nextGeoSerial = ar.iden()
            self._reserved      = [ar.word() for _ in range(3)]
            n                   = ar.sub_size()
            g(f'Got {n} boards to read')
            self._boards        = [GSNBoard(ar,vers) for _ in range(n)]

    def toDict(self,boardManager):
        hasStart = False
        for b in self._boards:
            if b._openOnLoad:
                hasStart = True

        # Make sure at least one map is loaded 
        if not hasStart and len(self._boards) > 0:
            self._boards[0]._openOnLoad = True
            
        return {b._serial: b.toDict(boardManager) for b in self._boards }

    def __str__(self):
        pl = '\n    '.join([str(s) for s in self._boards])
        return f'GSNBoardManager: {self._nextGeoSerial}\n    {pl}\n'
    
#
# EOF
#

# ====================================================================
# From gamebox.py

# --------------------------------------------------------------------
class GBXInfo:
    def __init__(self,ar):
        '''GameBox information'''
        with VerboseGuard('Reading information') as g:
            self._bitsPerPixel = ar.word()   # 2 -> 2
            self._majorRevs    = ar.dword()  # 4 -> 6
            self._minorRevs    = ar.dword()  # 4 -> 10
            self._gameID       = ar.dword()  # 4 -> 14
            self._boxID        = ar.read(16) # 16 -> 30
            self._author       = ar.str()    # X  -> 30+X
            self._title        = ar.str()    # Y  -> 30+X+Y
            self._description  = ar.str()    # Z  -> 30+X+Y+Z
            self._password     = ar.read(16) # 16 -> 46+X+Y+Z
            self._stickyDraw   = ar.word()   # 2  -> 48+X+Y+Z
            self._compression  = ar.word()   # 2  -> 50+X+Y+Z
            self._reserved     = [ar.word() for _ in range(4)] # 4x2 -> 58+X+Y+Z
            g(f'GameBox is {self._title} by {self._author} (password: {self._password})')
        
    def __str__(self):
        return ('Information:\n'
                f'  Bits/pixel:         {self._bitsPerPixel}\n'
                f'  Major revision:     {self._majorRevs}\n'
                f'  Minor revision:     {self._minorRevs}\n'
                f'  Game ID:            {self._gameID}\n'
                f'  Box ID:             {self._boxID}\n'
                f'  Author:             {self._author}\n'
                f'  Title:              {self._title}\n'
                f'  Description:        {self._description}\n'
                f'  Password:           {self._password}\n'
                f'  Sticky Draw tools:  {self._stickyDraw}\n'
                f'  Compression level:  {self._compression}\n'
                f'  Reserved:           {self._reserved}')

    
# ====================================================================
class GameBox:
    def __init__(self,ar):
        '''Container of game'''
        with VerboseGuard(f'Reading gamebox'):
            self._header       = GBXHeader(ar,GBXHeader.BOX)
            self._info         = GBXInfo(ar)
            self._strings      = GBXStrings(ar)
            self._tileManager  = GBXTileManager(ar)
            self._boardManager = GBXBoardManager(ar)
            self._pieceManager = GBXPieceManager(ar)
            self._markManager  = GBXMarkManager(ar)

        # print(self._strings)
        # print(self._markManager)
        
    def __str__(self):
        return (str(self._header)+      
                str(self._info)+        
                str(self._strings)+     
                str(self._tileManager)+ 
                str(self._boardManager)+
                str(self._pieceManager)+
                str(self._markManager)) 

    
    @classmethod
    def fromFile(cls,filename):
        with VerboseGuard(f'Read gamebox from {filename}'):
            with Archive(filename,'rb') as ar:
                return GameBox(ar)

#
# EOF
#
# ====================================================================
# From scenario.py

class GSNInfo:
    def __init__(self,ar):
        '''Scenario information'''
        self._disableOwnerTips = ar.word()
        self._reserved         = [ar.word() for _ in range(3)]
        self._gameID           = ar.dword()  # 4 -> 14
        self._majorRevs        = ar.dword()  # 4 -> 6
        self._minorRevs        = ar.dword()  # 4 -> 10
        self._gbxFilename      = ar.str()
        self._scenarioID       = ar.dword()
        self._title            = ar.str()    # Y  -> 30+X+Y
        self._author           = ar.str()    # X  -> 30+X
        self._description      = ar.str()    # Z  -> 30+X+Y+Z
        self._keepBackup       = ar.word()
        self._keepHistory      = ar.word()
        self._verifyState      = ar.word()
        self._verifySave       = ar.word()
        self._showObjectTip    = ar.word()

    def __str__(self):
        return ('Information:\n'
                f'  Disable owner tips: {self._disableOwnerTips}\n'
                f'  Reserved:           {self._reserved}\n'
                f'  Game ID:            {self._gameID}\n'
                f'  Major revision:     {self._majorRevs}\n'
                f'  Minor revision:     {self._minorRevs}\n'
                f'  Game box filename:  {self._gbxFilename}\n'
                f'  Scenario ID:        {self._scenarioID}\n'
                f'  Title:              {self._title}\n'
                f'  Author:             {self._author}\n'
                f'  Description:        {self._description}\n'
                f'  Keep backup:        {self._keepBackup}\n'
                f'  Keep history:       {self._keepHistory}\n'
                f'  Verify state:       {self._verifyState}\n'
                f'  Verify save:        {self._verifySave}\n'
                f'  Show object tips:   {self._showObjectTip}\n')
                
# ====================================================================
class Scenario:
    def __init__(self,ar,gbxfilename=None):
        '''Container of game'''
        with VerboseGuard(f'Reading scenario'):
            self._header        = GBXHeader       (ar,GBXHeader.SCENARIO)
            self._info          = GSNInfo         (ar)
            self._strings       = GSNStrings      (ar)
            self._playerManager = GSNPlayerManager(ar)
            self._windows       = GSNWindows      (ar)
            self._trayA         = GSNTrayPalette  (ar,self._header._vers,'A')
            self._trayB         = GSNTrayPalette  (ar,self._header._vers,'B')
            self._mark          = GSNMarkPalette  (ar,self._header._vers)
            self._boards        = GSNBoardManager (ar,self._header._vers)
            self._trayManager   = GSNTrayManager  (ar,self._header._vers)
            self._pieceTable    = GSNPieceTable   (ar,self._header._vers)
            # Possibly override GBX file name 
            if gbxfilename is not None and gbxfilename != '':
                self._info._gbxFilename = gbxfilename

            self.readGameBox(ar)

    def readGameBox(self,ar):
        from pathlib import Path
        with VerboseGuard(f'Read game box file {self._info._gbxFilename}') as v:
            gbxname = self._info._gbxFilename
            gbxpath = Path(gbxname)
            
            if not gbxpath.exists():
                v(f'GameBox file {gbxpath} does not exist')
                if '\\' in gbxname:
                    gbxname = gbxname.replace('\\','/')
                    gbxpath = Path(gbxname)
                gbxpath = ar.path.parent / Path(gbxpath.name)
                if not gbxpath.exists():
                    raise RuntimeError(f'GameBox file {gbxpath} cannot be found')
                
            self._gbx = GameBox.fromFile(str(gbxpath))

            if self._gbx._info._gameID != self._info._gameID:
                raise RuntimeError(f'Game IDs from GBX and GSN does not match: '
                                   f'{self._gbx._info._gameID} versus '
                                   f'{self._header._gameID}')
        
    def __str__(self):
        return (str(self._header)+      
                str(self._info)+        
                str(self._strings)+
                str(self._playerManager)+
                str(self._windows)+
                str(self._trayA)+
                str(self._trayB)+
                str(self._mark)+
                str(self._boards)+
                str(self._trayManager)+
                str(self._pieceTable)+
                str(self._gbx)+
                ''
                )

    
    @classmethod
    def fromFile(cls,filename,gbxfile=None):
        with Archive(filename,'rb') as ar:
            return Scenario(ar,gbxfile)
# ====================================================================
# From player.py

class GSNPlayerManager:
    def __init__(self,ar):
        with VerboseGuard(f'Reading players mappings'):
            self._enable  = ar.byte()
            self._players = []
            if self._enable:
                n             = ar.sub_size()
                self._players = [GSNPlayer(ar) for _ in range(n)]

    def toDict(self):
        return [p._name for p in self._players]

    def __str__(self):
        pl = '\n    '.join([str(s) for s in self._players])
        return ('Players:\n'
                f'  Enabled:      {self._enable}\n'
                f'  # players:    {len(self._players)}\n    {pl}\n')

class GSNPlayer:
    def __init__(self,ar):
        with VerboseGuard(f'Reading player'):
            self._key  = ar.dword()
            self._name = ar.str()


    def __str__(self):
        return f'Player: {self._name} (0x{self._key:08x})'

#
# EOF
#

# ====================================================================
# From windows.py

class GSNWindow:
    def __init__(self,ar):
        with VerboseGuard('Reading window state') as g:
            self._code   = ar.word()
            self._user   = ar.word()
            self._board  = ar.iden()
            self._state  = [ar.dword() for _ in range(10)]
            n            = ar.size()
            g(f'Read {self._code} {self._user} {self._board} {self._state}')
            g(f'Reading {n} bytes at {ar.tell()}')
            self._buffer = ar.read(n)

    def __str__(self):
        return (f'code={self._code:04x} '
                f'user={self._user:04x} '
                f'board={self._board:04x} '
                f'buffer={len(self._buffer)}')
        
class GSNWindows:
    def __init__(self,ar):
        with VerboseGuard(f'Reading window states') as g: 
            self._savePositions = ar.word()
            self._enable        = ar.byte()
            n                   = ar.size() if self._enable else 0
            g(f'Save position: {self._savePositions}, '
              f'enable {self._enable} '
              f'n={n}')
            self._states        = [GSNWindow(ar) for _ in range(n)]

    def __str__(self):
        pl = '\n    '.join([str(s) for s in self._states])
        return f'Windows states ({len(self._states)})\n    {pl}\n'
    

#
# EOF
#
# ====================================================================
# From palette.py

class GSNPalette:
    def __init__(self,ar):
        with VerboseGuard('Reading palette'):
            self._visible    = ar.word()
            self._comboIndex = ar.dword()
            self._topIndex   = ar.dword()
            
class GSNTrayPalette(GSNPalette):
    def __init__(self,ar,vers,iden):
        with VerboseGuard(f'Reading scenario tray palette {iden}'):
            super(GSNTrayPalette,self).__init__(ar)
            self._iden       = iden
            self._listSel    = readVector(ar,lambda ar : ar.dword())
            
    def __str__(self):
        return f'GSNTrayPalette: {self._comboIndex} '\
            f'{self._topIndex} {self._listSel}\n'

class GSNMarkPalette(GSNPalette):
    def __init__(self,ar,vers):
        with VerboseGuard(f'Reading scenario mark palette'):
            super(GSNMarkPalette,self).__init__(ar)
            self._listSel    = ar.dword()
    def __str__(self):
        return f'GSNMarkPalette: {self._comboIndex} '\
            f'{self._topIndex} {self._listSel}\n'

#
# EOF
#

# ====================================================================
# From tray.py
    
class GSNTraySet:
    def __init__(self,ar,vers):
        with VerboseGuard(f'Reading tray set') as g:
            self._name          = ar.str()
            g(f'Tray set: {self._name}')
            self._random        = (ar.word() if Features().piece_100 else 0)
            self._visibleFlags  = ar.dword()
            self._ownerMask     = (ar.word() if vers < num_version(3,10) else
                                   ar.dword())
            self._restrict      = ar.word()
            self._pieces        = readVector(ar,lambda ar: ar.iden())

    def __len__(self):
        return len(self._pieces)

    def toDict(self):
        viz = self._visibleFlags & ~0xFFFF8000
        # print(f'{self._visibleFlags:08x} -> {viz}')
        vizStr = {0: 'all',
                  1: 'owner',
                  2: 'generic',
                  3: 'none'}.get(viz,'')
        return {'name':     self._name,
                'visible':  vizStr,
                'owner':    self._ownerMask,
                'restrict': self._restrict,
                'pieces':   self._pieces }
    
    def __str__(self):
        return (f'Tray set: {self._name} '
                f'[visible={self._visibleFlags},'
                f'ownerMask={self._ownerMask},'
                f'resrict={self._restrict}] '
                f'({len(self)}): {self._pieces}')


class GSNTrayManager:
    def __init__(self,ar,vers,iden=''):
        with VerboseGuard(f'Reading tray {iden} manager @ {ar.tell()}') as g:
            self._iden     = iden
            self._reserved = [ar.word() for _ in range(4)]
            g(f'{self._reserved}')
            self._dummy    = (ar.byte() if vers >= num_version(4,0) else 0)
            self._sets     = readVector(ar, lambda ar : GSNTraySet(ar,vers))

    def __len__(self):
        return len(self._sets)

    def toDict(self):
        return [s.toDict() for s in self._sets]
    
    def __str__(self):
        pl = '\n    '.join([str(s) for s in self._sets])
        return f'TrayManager: {self._iden} ({len(self)})\n    {pl}\n'


#
# EOF
#

        
            
            
# ====================================================================
# From extractor.py

# ====================================================================
class CbExtractor:
    def __init__(self):
        pass
    
    def save(self,filename):
        from zipfile import ZipFile
        from copy import deepcopy
        
        with VerboseGuard(f'Saving to {filename}') as g:
            with ZipFile(filename,'w') as zfile:
                self._save(zfile)

    def saveImages(self,d,zfile):
        with VerboseGuard(f'Saving images') as g:
            for serial, board in d['boards'].items():
                g(f'Saving board: {board}')
                self.saveSVG(board,zfile)
            
            for piece in d['pieces']['map'].values():
                g(f'Saving piece: {piece}')
                for which in ['front','back']:
                    if which not in piece:
                        continue
                
                    side     = piece[which]
                    self.savePNG(side,zfile)
                    piece[which] = side['filename']
            
            for mark in d['marks']['map'].values():
                g(f'Saving marks: {mark}')
                self.savePNG(mark,zfile)
            
            for tile in d['tiles'].values():
                g(f'Saving tile: {tile}')
                self.savePNG(tile,zfile)
            
            del d['tiles']
        

    def saveSVG(self,d,zfile,removeImage=True):
        from io import StringIO
        
        with VerboseGuard(f'Saving SVG') as g:
            filename = d['filename']
            image    = d['image']
            
            # stream = StringIO()
            # image.write(stream,pretty=True)
            g(f'Saving SVG: {image}')
            zfile.writestr(filename,image)#stream.getvalue())

            if removeImage:
                del d['image']

    def savePNG(self,d,zfile,removeImage=True):
        with VerboseGuard(f'Saving PNG') as g:
            filename = d['filename']
            img      = d['image']
        
            with zfile.open(filename,'w') as file:
                g(f'Save {img}')
                img.save(file,format='PNG')

            if removeImage:
                del d['image']
        
    def _save(self,zfile):
        pass 
    
    
# ====================================================================
class GBXExtractor(CbExtractor):
    def __init__(self,gbx):
        '''Turns gambox into a more sensible structure'''
        super(GBXExtractor,self).__init__()

        with VerboseGuard(f'Extract gamebox {gbx._info._title}') as g:
            self._d = {
                'title':       gbx._info._title,
                'author':      gbx._info._author,
                'description': gbx._info._description.replace('\r',''),
                'major':       gbx._info._majorRevs,
                'minor':       gbx._info._minorRevs,
                'version':     f'{gbx._info._majorRevs}.{gbx._info._minorRevs}'
            }

            self._d['pieces'] = gbx._pieceManager.toDict(gbx._tileManager,
                                                         gbx._strings)
            self._d['marks']  = gbx._markManager.toDict(gbx._tileManager,
                                                        gbx._strings)
            self._d['boards'] = gbx._boardManager.toDict(gbx._tileManager,
                                                         gbx._markManager,
                                                         gbx._strings)
            self._d['tiles']  = gbx._tileManager._toStore
            
            g(f'Done rationalizing {gbx._info._title}')

        
    def _save(self,zfile):
        from pprint import pprint
        from io import StringIO
        from json import dumps
        from copy import deepcopy
        
        with VerboseGuard(f'Saving {self._d["title"]} to {zfile.filename}')as g:
            d = deepcopy(self._d)
            
            self.saveImages(d,zfile)
            
            zfile.writestr('info.json',dumps(d,indent=2))

            g(f'Done saving')

    def fromZipfile(self,zipfile,d):
        pass 

    def __str__(self):
        from pprint import pformat

        return pformat(self._d,depth=2)

# ====================================================================
class GSNExtractor(CbExtractor):
    def __init__(self,gsn,zipfile=None):
        '''Turns gambox into a more sensible structure'''
        super(GSNExtractor,self).__init__()

        if zipfile is not None:
            self.fromZipfile(zipfile)
            return
        
        with VerboseGuard(f'Extract scenario {gsn._info._title}') as g:
            gbxextractor = GBXExtractor(gsn._gbx)
            self._d = {
                'title':       gsn._info._title,
                'author':      gsn._info._author,
                'description': gsn._info._description.replace('\r',''),
                'major':       gsn._info._majorRevs,
                'minor':       gsn._info._minorRevs,
                'version':     f'{gsn._info._majorRevs}.{gsn._info._minorRevs}',
                'gamebox':     gbxextractor._d}
            self._d['players'] = gsn._playerManager.toDict()
            self._d['trays']   = gsn._trayManager.toDict()
            self._d['boards']  = gsn._boards.toDict(gsn._gbx._boardManager)
            
            
    def _save(self,zfile):
        from pprint import pprint
        from io import StringIO
        from json import dumps
        from copy import deepcopy
        
        with VerboseGuard(f'Saving {self._d["title"]} to {zfile.filename}')as g:
            d = deepcopy(self._d)
            
            self.saveImages(d['gamebox'],zfile)
                
            zfile.writestr('info.json',dumps(d,indent=2))

            g(f'Done saving')

    def fromZipfile(self,zipfile):
        from json import loads
        from PIL import Image as PILImage
        from io import BytesIO
        from wand.image import Image as WandImage
        with VerboseGuard(f'Reading module from zip file') as v:
            self._d = loads(zipfile.read('info.json').decode())
            
            newMap = {}
            for pieceSID,piece in self._d['gamebox']['pieces']['map'].items():
                pieceID = int(pieceSID)
                if pieceID in newMap:
                    continue
                for which in ['front', 'back']:
                    if which not in piece:
                        continue
            
                    
                    fn           = piece[which]
                    v(f'Read image {fn}')
                    bts          = BytesIO(zipfile.read(fn))
                    img          = PILImage.open(bts)
                    piece[which] = {'filename': fn,
                                    'image':    img,
                                    'size':     img.size}
            
                newMap[pieceID] = piece
                
            del self._d['gamebox']['pieces']['map']
            self._d['gamebox']['pieces']['map'] = newMap
            
            newMap = {}
            for markSID,mark in self._d['gamebox']['marks']['map'].items():
                markID       = int(markSID)
                if markID in newMap:
                    continue 
                fn             = mark['filename']
                v(f'Read image {fn}')
                bts            = BytesIO(zipfile.read(fn))
                img            = PILImage.open(bts)
                dsc            = mark.get('description',None)
                mark['image']  = img
                mark['size']   = img.size
                newMap[markID] = mark
                
            del self._d['gamebox']['marks']['map']
            self._d['gamebox']['marks']['map'] = newMap
            
            newMap = {}
            for boardSID,board in self._d['gamebox']['boards'].items():
                boardID  = int(boardSID)
                if boardID in newMap:
                    continue
                filename        = board['filename']
                v(f'Read file {filename}')
                content         = zipfile.read(filename)
                img             = WandImage(blob=content)
                board['image']  = content.decode()
                board['size']   = img.size 
                newMap[boardID] = board
            
            # del self._d['gamebox']['boards']
            # self._d['gamebox']['boards'] = newMap

        # print(self)
        
    def __str__(self):
        from pprint import pformat

        return pformat(self._d)#,depth=5)
    
#
# EOF
#
# ====================================================================
# From zeropwd.py

nullpwd = b'\xee\n\xcbg\xbc\xdb\x92\x1a\x0c\xd2\xf1y\x83*\x96\xc9'

def zeropwd(filename):
    from pathlib import Path
    
    pos = None
    with Archive(filename,'rb') as ar:
        header       = GBXHeader(ar,GBXHeader.BOX)
        box          = GBXInfo(ar)


        pos = ar.tell() - 4*2 - 2 - 2 - 16

    with open(filename,'rb') as file:
        cnt = file.read()
        old = cnt[pos:pos+16]

    lcnt = list(cnt)
    lcnt[pos:pos+16] = list(nullpwd)
    ncnt = bytes(lcnt)

    on = Path(filename)
    on = on.with_stem(on.stem + '-new')
    with open(on,'wb') as file:
        file.write(ncnt)


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType
    ap = ArgumentParser(description='Disable password in gamebox')
    ap.add_argument('input', type=str, help='The file')

    args = ap.parse_args()

    zeropwd(args.input)
    
    
    
##
# End of generated script
##
