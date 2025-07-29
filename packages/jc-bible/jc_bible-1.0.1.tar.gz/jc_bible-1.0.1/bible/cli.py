import argparse,gzip,inspect,json,os,re,requests,sys,textwrap,time
import tomlkit as toml

from dataclasses import dataclass,replace
from debug import DebugChannel
from handy import die,prog,get_module_versions

from pprint import pprint,pformat

dc=DebugChannel()

APP_DIR=os.path.expanduser("~/.local/bible")
CONFIG_FILENAME=os.path.join(APP_DIR,'config.toml')
CACHE_DIR=os.path.join(APP_DIR,"cache")
if not os.path.isdir(CACHE_DIR):
    os.makedirs(CACHE_DIR)

@dc
def tw(s,indent=0):
    "This is a convenience wrapper around textwrap.wrap(...)."

    return '\n'.join(textwrap.wrap(
        s,
        width=prog.term_width,
        initial_indent=' '*indent,
        subsequent_indent=' '*indent
    ))

 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Low-level reading and writing cache files.

def json_to_cache(name,data):
    "Write the given data to the named cache file as compressed JSON."

    filename=os.path.join(CACHE_DIR,name+'.json.gz')
    dc(f"Writing cache file {filename} ...")
    #with gzip.open(filename,'wt',encoding='uft-8') as f:
    #    json.dump(data,f)
    try:
        with gzip.open(filename,'wb') as f:
            f.write(json.dumps(data).encode('utf-8'))
    except Exception as e:
        dc(f"Received {str(e)} exception while writing {filename}.")
        if os.path.isfile(filename):
            os.unlink(filename)

def json_from_cache(name):
    """Read the given data from cache, or return None if no cache file
    exists."""
    
    filename=os.path.join(CACHE_DIR,name+'.json.gz')
    if not os.path.isfile(filename):
        dc(f"Cache file {filename} not found.")
        return None
    dc(f"Reading cache file {filename} ...")
    #with gzip.open(filename,'rt',encoding='utf-8') as f:
    #    return json.load(f)
    try:
        with gzip.open(filename,'rb') as f:
            return json.loads(f.read().decode('utf-8'))
    except Exception as e:
        dc(f"Received {str(e)} exception while reading {filename}.")
        if os.path.isfile(filename):
            os.unlink(filename)

 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Call Bible API endpoints, returning JSON data.

@dataclass
class Version:
    code: str           # id
    abbr: str           # localVersionAbbreviation
    name: str           # version
    description: str    # description
    scope:str           # scope
    language_name: str  # language.name
    language_code: str  # language.code
    country_name: str   # country.name
    country_code: str   # country.code
    numbers: str        # numeralSystem
    script: str         # script

    @staticmethod
    def from_json(data):
        return Version(
            code=data['id'],
            abbr=data['localVersionAbbreviation'],
            name=data['version'],
            description=data['description'],
            scope=data['scope'],
            language_name=data['language']['name'],
            language_code=data['language']['code'],
            country_name=data['country']['name'],
            country_code=data['country']['code'],
            numbers=data['numeralSystem'],
            script=data['script']
        )

    def __str__(self):
        return f"""\
{self.code}: {self.name} ({self.abbr}) ({self.scope})
  {self.description}
  Language: {self.language_name} ({self.language_code})
  Country: {self.country_name} ({self.country_code})
  Numbers are {self.numbers}; script is {self.script}."""

class Bible:
    base_url="https://cdn.jsdelivr.net/gh/wldeh/bible-api/bibles"
  # books=[
  #     "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua",
  #     "Judges", "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings",
  #     "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job",
  #     "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah",
  #     "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel",
  #     "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah",
  #     "Haggai", "Zechariah", "Malachi",
  #     "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians",
  #     "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians",
  #     "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy",
  #     "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter",
  #     "1 John", "2 John", "3 John", "Jude", "Revelation"
  # ]
    books = {
        # Old Testiment
        "Genesis": 50,
        "Exodus": 40,
        "Leviticus": 27,
        "Numbers": 36,
        "Deuteronomy": 34,
        "Joshua": 24,
        "Judges": 21,
        "Ruth": 4,
        "1 Samuel": 31,
        "2 Samuel": 24,
        "1 Kings": 22,
        "2 Kings": 25,
        "1 Chronicles": 29,
        "2 Chronicles": 36,
        "Ezra": 10,
        "Nehemiah": 13,
        "Esther": 10, # The Protestant/Hebrew Canon version
        "Job": 42,
        "Psalms": 150,
        "Proverbs": 31,
        "Ecclesiastes": 12,
        "Song of Solomon": 8,
        "Isaiah": 66,
        "Jeremiah": 52,
        "Lamentations": 5,
        "Ezekiel": 48,
        "Daniel": 12, # The Protestant/Hebrew Canon version
        "Hosea": 14,
        "Joel": 3,
        "Amos": 9,
        "Obadiah": 1,
        "Jonah": 4,
        "Micah": 7,
        "Nahum": 3,
        "Habakkuk": 3,
        "Zephaniah": 3,
        "Haggai": 2,
        "Zechariah": 14,
        "Malachi": 4,

        # Deuterocanonical books
        "Tobit": 14,
        "Judith": 16,
        "Esther (Greek Addition)": 10,
        "Wisdom": 19,
        "Sirach": 51,
        "Baruch": 5,
        "Letter of Jeremiah": 1,
        "Daniel (Greek Addition)": 2,
        "1 Maccabees": 16,
        "2 Maccabees": 15,
        "1 Esdras": 9,
        "Prayer of Manasseh": 1,
      # "Psalm 151": 1, We'll let this land at the end of Psalms organically.
        "3 Maccabees": 7,
        "4 Maccabees": 18,

        # New Testiment
        "Matthew": 28,
        "Mark": 16,
        "Luke": 24,
        "John": 21,
        "Acts": 28,
        "Romans": 16,
        "1 Corinthians": 16,
        "2 Corinthians": 13,
        "Galatians": 6,
        "Ephesians": 6,
        "Philippians": 4,
        "Colossians": 4,
        "1 Thessalonians": 5,
        "2 Thessalonians": 3,
        "1 Timothy": 6,
        "2 Timothy": 4,
        "Titus": 3,
        "Philemon": 1,
        "Hebrews": 13,
        "James": 5,
        "1 Peter": 5,
        "2 Peter": 3,
        "1 John": 5,
        "2 John": 1,
        "3 John": 1,
        "Jude": 1,
        "Revelation": 22
    }
    versions=None # Will become a dictionary of Version instances keyed by code.
    t=0 # This will hold a Unix Epoch time for API rate limiting.

    @staticmethod
    def chapter_filename(version,book,chapter):
        """Return the name (without file extension) of cache file for
        this version, book, and chapter."""

        book=book.lower().replace(' ','')
        return f"{version}-{book}-{chapter:03d}"

    @staticmethod
    def matching_versions(scope=None,language=None,country=None,version=None):
        "Return a list of matching Version instances."

        scope=re.compile(scope,re.IGNORECASE) if scope else re.compile('.*')
        language=re.compile(language,re.IGNORECASE) if language else re.compile('.*')
        country=re.compile(country,re.IGNORECASE) if country else re.compile('.*')
        version=re.compile(version,re.IGNORECASE) if version else re.compile('.*')

        #if dc:
        #    dc(f"{scope.pattern=}")
        #    dc(f"{language.pattern=}")
        #    dc(f"{country.pattern=}")
        #    dc(f"{version.pattern=}")

        vlist=[
            v for v in Bible.versions.values()
            if scope.search(v.scope)
                and (language.search(v.language_code) or language.search(v.language_name))
                and (country.search(v.country_code) or language.search(v.country_name))
                and (version.search(v.abbr) or version.search(v.name))
        ]

        return vlist

    @staticmethod
    def version_code(scope=None,language=None,country=None,version=None):
        """Return the version code for the one version that matches all
        the given criteria."""

        possibles=Bible.matching_versions(scope,language,country,version)
        if len(possibles)==1:
            return possibles[0].code
        if possibles:
            l=', '.join([f"{v.name} ({v.abbr})" for v in possibles])
            raise ValueError(f"{version} matches multiple versions: {l}")
        else:
            raise ValueError(f"{version} matches no version abbreviations or names.")

    @staticmethod
    def book_name(book):
        """Given a possibly partial name of a book of the bible, return
        the correct name."""

        if book in Bible.books:
            return book

        # Make sure there's a space between the number of the book and its name.
        m=re.match(r'((\d)\s*)?(\w+)',book)
        if not m:
            die(f"{book!r} doesn't look like a book of the Bible")
        n,name=m.group(2,3)
        bname=f"{n} {name}" if n else name

        # See how many books this string matches. (Hopefully exactly one.)
        possibles=[
            b for b in Bible.books if b.lower().startswith(bname.lower())
        ]
        if len(possibles)==1:
            return possibles[0]
        if possibles:
            l=', '.join(possibles)
            die(f"{book} matches multiple boooks: {l}")
        else:
            die(f"{book} matches no book of the Bible.")

    @staticmethod
    def get_versions():
        "Get a list of Bible versions from cache or the API."

        # If this has already been done, return the previous result.
        if Bible.versions:
            return Bible.versions

        # Try reading the raw JSON from cache.
        data=json_from_cache("versions")
        if not data:
            # Retrieve the raw JSON from the API.
            url=f"{Bible.base_url}/bibles.json"
            dc(f"Retrieving Bible versions from {url} ...")
            resp=requests.get(url)
            data=resp.json()
            json_to_cache("versions",data)


        # Convert our raw JSON to a dictionary of Version instances.
        Bible.versions={
            v['id']:Version.from_json(v) for v in data
        }
        
        return Bible.versions

    @staticmethod
    def get_chapter(version,book,chapter):
        "Get a Bible chapter from cache or the API."

        # Make sure our version and book exist.
        book=Bible.book_name(book)

        # Get this chapter from cache if possible.
        filename=Bible.chapter_filename(version,book,chapter)
        data=json_from_cache(filename)
        if not data:
            # Make sure we don't beat the API to death. Wait at least 0.5
            # seconds between API requests.
            t1=time.time()
            if t1-Bible.t<0.5:
                dc("Sleeping 0.5 seconds ...")
                time.sleep(0.5)
            Bible.t=time.time()
            # Get this chapter from the API.
            b=book.lower().replace(' ','')
            url=f"{Bible.base_url}/{version}/books/{b}/chapters/{chapter}.json"
            dc(f"Retrieving Chapter from {url} ...")
            resp=requests.get(url)
            if resp.text.startswith('Package size exceeded the configured limit'):
                die(f"Failed to retrieve the {version} version of {book} {chapter}! (Are you sure that's a valid chapter?)")
            data=resp.json()
            json_to_cache(filename,data)

        # Convert our raw JSON to a Chapter instance.
        return Chapter.from_json(version,data)


 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Get Bible chapters from cache (if available) or from the Bible API.

#@dataclass
#class Verse:
#    number: str
#    text: str
#
#    def __str__(self):
#        return f"{self.number} {self.text}"

class Chapter(dict):
    """Create a Chapter instance from either cache, or failing that,
    from the Bible API (https://github.com/wldeh/bible-api). A Chapter
    instance is basically a dictionary of verses keyed by integer verse
    numbers."""

    def __init__(self,version):
        "Call Bible.get_chapter(...) instead of this constructor."

        self.version=Bible.versions[version]

    @staticmethod
    def from_json(version,data):
        """Called from Bible.get_chapter(...) to construct a Chapter
        instance."""

        int_pat=re.compile(r'(\d+)')
        data=data['data']
        c=Chapter(version)
        c.book=data[0]['book']
        c.chapter=int(data[0]['chapter'])
        for d in data:
            n=d['verse']
            v=d['text']
            m=int_pat.match(n)
            n=int(m.groups()[0])
            if n in c:
                c[n]+=' '+v
            else:
                c[n]=v
        return c

def init_config():
    """Create a new config file, possibly overriting the existing
    config file. Return this new config as a toml.Document."""

    empty_config="""\
# This is the config file for the `bible` command. Remove the `#` character
# before variable definitions to use or modify them.

[read]
# This section sets default parameters of the `bible read ...` operation.

# Set version if you want to read that version by default.
#version="en-lsv"

# Set the maximum width (in character) you want printed Scripture passages
# to wrap to. (Any positive integer will do.)
#width=78

# Set a default for whether to print  verse numbers. (true or false)
#numbers=false

# Set a default for whether to print the Scripture reference at then end.
#reference=false

# Experimental: Guess at where paragraphs should be, and insert blank lines
# accordingly.
#spaced=true

[versions]
# This section sets default parameters of the `bible versions ...` operation.
# Set the default scope.
#scope="bible"

# Set the default language.
#language="english"

# Set the default country.
#country="us"

[cache]
# Set a "time to live" for bible's cached data. Cache files older than this
# number of days will be ignored so up-to-date information will replace it
# the next time it is needed.
ttl=90
"""

    # Start with an empty config file.
    dc(f"Setting initial config values ...")
    c=toml.parse(empty_config)
    # Write this file to disk so the user can edit it directly if desired.
    dc(f"Writing initial config values to {CONFIG_FILENAME!r} ...")
    with open(CONFIG_FILENAME,'w',encoding="utf-8") as f:
        toml.dump(c,f)

    return c


def read_config():
    """Read our config.toml file, creating one if needed, and return
    that data."""

    if os.path.isfile(CONFIG_FILENAME):
        # Set our config from the existing config.toml file.
        dc(f"Reading config values from {CONFIG_FILENAME!r} ...")
        with open(CONFIG_FILENAME,'r',encoding="utf-8") as f:
            c=toml.load(f)
    else:
        # Start with an empty config file.
        c=init_config()

    # If the user's been deleting whole tables, we really need each one
    # to exist, even if it's empty.
    for t in ('read','versions','cache'):
        if not t in c:
            dc("Adding table {t} to config ...")
            c.append(t,toml.Table(t))

    return c

def read_command_line():
    "Return an opt namespace representing our command line."

    ap=argparse.ArgumentParser(
        add_help=False,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Look up Bible passages from a large selection of translations."
    )

    # Universal command line options.
    ap.add_argument('--debug',action='store_true',help="Turn on debugging output.")
    ap.add_argument('-h','--help',action='store_true',help="Show this help message.")
    ap.add_argument('--all-help',action='store_true',help="Show elaborated help for each of %(prog)s's sub-commands.")
    ap.add_argument('--version',action='store_true',help="Show the main and dependency versions")
    ap.set_defaults(func=None) # In case we have no subcommand.

    # Set up a subparser for each bible sub-command.
    sp=ap.add_subparsers(
        dest='command',
        title='Bible Subcommands',
        description=textwrap.fill(f"{ap.prog} uses subcommands to know what type of operation you'd like to perform. You can use the --help option after any subcommand on the command line to get further help for that subcommand.",width=prog.term_width)
    )

    # Read (and output) a given Bible passage.
    c=config['read']
    sp_read=sp.add_parser('read',help="Output the given Bible passage.")
    sp_read.set_defaults(func=cmd_read)
    sp_read.add_argument('--version',metavar='VER_CODE',action='store',default=c.get('version'),help=f"The version code of the Bible to use. (Run `{prog.name} versions` for a list. Use `{prog.name} config` to set a default version.) (default: %(default)s)")
    sp_read.add_argument('--width',metavar='WIDTH',action='store',type=int,default=c.get('width',prog.term_width),help="The width (in characters) allowed for wrapping the output (defaults to terminal width). (default: %(default)d)")
    sp_read.add_argument('--number',action=argparse.BooleanOptionalAction,default=c.get('number',False),help="Include (or exclude) verse numbers. (default: %(default)s)")
    sp_read.add_argument('--reference',action=argparse.BooleanOptionalAction,default=c.get('reference',False),help="Append (or suppress) the Scripture reference at the end of the output. (default: %(default)s)")
    sp_read.add_argument('--spaced',action=argparse.BooleanOptionalAction,default=c.get('spaced',False),help="Guess at where paragraphs might be, and add blank lines accordingly (experimental). (default: %(default)s)")
    sp_read.add_argument('passage',action='store',nargs='*',help="""Give a specific passage to be printed. This can be any value of the form "BOOK[ CHAPTER[:VERSES]]" where BOOK is a full or abbreviated book of the Bible, CHAPTER is any chapter in that book, and VERSES (if given) says which verse or verses to output. If no verse is given, the whole chapter is printed. If no chapter is given, the whole book is printed.""")

    # versions
    c=config['versions']
    sp_versions=sp.add_parser('versions',help="List all available Bible versions.")
    sp_versions.set_defaults(func=cmd_versions)
    sp_versions.add_argument('--scope',action='store',default=c.get('scope'),help="""Common values for this are "bible", "new testament", and "old testament", but any regular expression will do. (default: %(default)s)""")
    sp_versions.add_argument('--language',action='store',default=c.get('language'),help="""The default value is %(default)r, but any regular expression is valid.""")
    sp_versions.add_argument('--country',action='store',default=c.get('country'),help="""The default value is %(default)r, but any regular expression is valid.""")
    sp_versions.add_argument("version",action='store',nargs='?',help="""This is optional, but any regular expression will narrow the search to matching versions.""")

    # config
    sp_config=sp.add_parser('config',help="Show or modify configuration variables. This helps to manage things like a default Bible version.")
    sp_config.set_defaults(func=cmd_config)
    sp_config.add_argument('--init',action='store_true',help="Re-initialize {prog.name}'s config file, possibly overwriting the existing one.")
    sp_config.add_argument('--show',action='store_true',help="Show all configuration values.")
    sp_config.add_argument('variables',nargs='*',action='store',help="""Zero or more configuration variables may be set by using the "VAR=[VAL]" format for each such variable. VAL is formatted as "SECTION.VARIABLE" to specify a section of the configuration file (e.g. "read") and a variable within that section (e.g. "width"). If VAL is missing, that configuration variable will be removed.""")

    # Parse the command line and handle any universal options.
    opt=ap.parse_args()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    dc.enable(opt.debug)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    if opt.help:
        ap.print_help()
        sys.exit(0)
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    if opt.all_help:
        ap.print_help()
        subparser_actions=[
            action for action in ap._actions if isinstance(action,argparse._SubParsersAction)
        ]
        for a in subparser_actions:
            for name,subparser in a.choices.items():
                print("\n------------------------------------------------------")
                subparser.print_help()
        sys.exit(0)
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    if opt.version and not opt.func:
        mv=get_module_versions()
        print(mv.pop(0))
        while mv:
            print(f"  {mv.pop(0)}")
        sys.exit(0)
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Return our command line options to be processed.
    return opt

def irregular_range(values):
    """This generator function returns integer values in the order of
    ranges given in the `values` string argument. It has the form of
    "N[-M][,N[-M] ...]" where N is the first number of a range, and the
    optional M is the last (and included) number in that range. As many
    such elements as desired by be separated by commas. The numbers can
    be in any order, and overlapping rages are fine. You geet what you
    ask for."""

    rp=re.compile(r"(\d+)(?:-(\d+))?$")
    ranges=[r.strip() for r in values.split(',')]
    for r in ranges:
        m=rp.match(r)
        if not m:
            raise ValueError(f"Range {r!r} is not a valid range.")
        N,M=m.groups()
        N=int(N)
        if M:
            M=int(M)
        if M:
            for i in range(N,M+1):
                yield i
        else:
            yield N

def cmd_read(opt):
    "Output a Bible passage."

    # Parse the book, chapter, and (optionally) verse(s) from our passage.
    opt.passage=' '.join(opt.passage)
    m=re.match(
        r"(?P<book>(\d\s*)?\w+)(\s+(?P<chapter>\d+)(:(?P<verse>.*))?)?$",
        opt.passage,
        re.IGNORECASE
    )
    if not m:
       die(f"{opt.passage} doesn't look like a valid passage.")
    book=m.groupdict()['book']
    chapter=m.groupdict()['chapter']
    if chapter:
        chapter=int(chapter)
    verse=m.groupdict()['verse']
    
    # Find the given version and book.
    if not opt.version:
        die(f"No version (-v) was given, and it has no configured default.")
    if not opt.version in Bible.versions:
        die(f"{opt.version} is not a valid version code. Run `{prog.name} versions` for a list.")
    book=Bible.book_name(book)
    dc(f"{opt.version=}")
    dc(f"{book=}")
    dc(f"{chapter=}")
    dc(f"{verse=}")

    # Allow for the posibility we're reading a whole book.
    if chapter:
        i=chapter
        j=chapter+1
    else:
        i=1
        j=Bible.books[book]+1

    for chap in range(i,j):
        chapter=chap
        if i!=j-1:
            time.sleep(.5)
        c=Bible.get_chapter(opt.version,book,chapter)
        dc(f"Found {len(c)} verses in {c.book} chapter {c.chapter}.")

        # Get a list of verses to be printed, including verse numbers if called for.
        verses=[]
        if verse:
            for i in irregular_range(verse):
                dc(f"Adding verse {i=}, {c[i]=}")
                if i in c:
                    if opt.number:
                        verses.append(f"{i} {c[i]}")
                    else:
                        verses.append(c[i])
        else:
            for i in c:
                dc(f"Adding verse {i=}, {c[i]=}")
                if opt.number:
                    verses.append(f"{i} {c[i]}")
                else:
                    verses.append(c[i])

        # Get a list of paragraphs, each of which will be individually wrapped.
        paragraphs=[]
        p='' # We'll accumulate multi-verse paragraphs in p.
        while verses:
            v=verses.pop(0)
            if ' || ' in v:
                if p:
                    paragraphs.append(p)
                    p=''
                if opt.number:
                    ind=' '*(v.index(' ')+1)
                    x=v.split(' || ')
                    x[1:]=[ind+y for y in x[1:]]
                    paragraphs.extend(x)
                else:
                    paragraphs.extend(v.split(' || '))
            else:
                if p:
                    p+=' '+v
                else:
                    p=v
            if opt.spaced and p and (p[-1] in '.?!' or p[-2:] in ('."','?"','!"')):
                # Guess that a verse ending with '.' or '?' is then end of a
                # paragraph.
                paragraphs.append(p+'|')
                p=''
        if p:
            # This will often be the only paragraph.
            paragraphs.append(p)

        # Wrap each paragraph to the width of the terminal, and print it.
        if book=='Psalms':
            book='Psalm' # Each chapter is a single psalm.
        if opt.reference and not verse:
            print(f"--{book} {chapter}")
        for p in paragraphs:
            #print('\n'.join(textwrap.wrap(p,width=opt.width,subsequent_indent=ind)))
            if p.endswith('|'):
                end='\n'
                p=p[:-1]
            else:
                end=''
            print('\n'.join(textwrap.wrap(p,width=opt.width)),end)
        if opt.reference and verse:
            print(f"--{book} {chapter}:{verse}")

def cmd_versions(opt):
    "Output a possibly filtered list of available Bible versions."

    vlist=Bible.matching_versions(
        scope=opt.scope,
        language=opt.language,
        country=opt.country,
        version=opt.version
    )
    for v in vlist:
        print(v,end='\n\n')
    print(f"Versions found: {len(vlist)}")

def cmd_config(opt):
    "Handle showing and setting config variables."

    def toml_value_string(val):
        "Given a TOML value, return it in string form."

        if isinstance(val,bool):
            dc(f"{type(val)=}, {val=}, {str(val).lower()=}")
            return str(val).lower()
        else:
            dc(f"{type(val)=}, {val=}, ",end='')
            dc(f"{val.as_string()=}")
            return val.as_string()

    if opt.show:
        # Print the "table.variable=value" information for each value in the
        # config file. Use TOML syntax for the values because that's what we
        # want the user to do when updating values.
        for t in config.keys():
            for var,val in config[t].items():
                print(f"{t}.{var}={toml_value_string(val)}")
        sys.exit(0)

    if opt.init:
        if os.path.isfile(CONFIG_FILENAME):
            print(f"{CONFIG_FILENAME} exists!")
            ans=input("Overwrite it with initial config values? (y/N) ")
            if ans.lower()=='y':
                init_config()
                print("Replaced previous config with initial config values.")
            else:
                print("Aborting. Your config file remains unchanged.")
        else:
            init_config()
            print(f"Created {CONFIG_FILENAME} with initial config values.")
        sys.exit(0)


    if not opt.variables:
        die("""No "VAR=[VAL]" arguments found on command line.""")
    changed=False
    vpat=re.compile(r'(\w+)\.(\w+)\s*=\s*(.*)?$')
    for v in opt.variables:
        m=vpat.match(v)
        if not m:
            die(f"Bad variable format: {v}")
        table,var,val=m.groups()
        if table not in config:
            die(f"Unknown configuration section: {table}")
        t=config[table]
        if val:
            # This seems like an expensive way to convert a string to a TOML
            # value, but I haven't found another way to do it.
            c=toml.parse(f"{var}={val}")
            t[var]=c[var]
            print(f'In "{table} section: {var}={toml_value_string(t[var])}')
            changed=True
        else:
            if var in t:
                print(f'Deleted from "{table}" section: {var}={toml_value_string(t[var])}')
                del t[var]
                changed=True
            else:
                print(f'No "{var}" variable found in section "{table}".')
    if changed:
        with open(CONFIG_FILENAME,'w',encoding='utf-8') as f:
            toml.dump(config,f)

def main():
    # Parse and return the command line.
    opt=read_command_line()

    # Initialize the Bible.versions dictionary.
    Bible.get_versions()

    # Do the user's bidding according to the command line.
    opt.func(opt)

# Parse (or create) config data from our config.toml file. We'll make
# config a global variable since that's really the scope of its use.
config=read_config()

if __name__ == "__main__":
    main()
