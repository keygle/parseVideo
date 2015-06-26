"""
HTMLDOM Library provides a simple interface for accessing and manipulating HTML documents.
You may find this library useful for building applications like screen-scraping.
Inspired by Jquery Library.
"""
import re
import math
import os

elementName = r'<([\w\d_:]+)'
restName = r'(?:\s+)?((?:[\w\d_:-]+\s*\=\s*[\'"](?:[^"\']+)?[\'"]?\s*;?)*)?\s*(?:/)?>'

#StartTag
startTag = re.compile( elementName + restName )

#endTag
endTag = re.compile(r'\s*</\s*([\w\d_:]+)\s*>')


whiteSpace = re.compile(r'\s+')

#Used to spilt attributes into name/value pair i.e. ( class="one" ==> { 'class':'one' } )
attributeSplitter = re.compile(r'(?:([\w_\d:-]+)\s*\=\s*[\'"]([^"\']+)[\'"]\s*)')

#These regex are used for class and id based selection.
"""
  i.e. given p.class#id
  @regVar:selector matches the "p" element and @regVar:left will contain ".class"
  and @regVar:right will hold the "#id" part.
"""
selector = re.compile(r'([\w_:\d*-]+)?((?:[#.\[][%?&+\s\w_ /:.\d#(),;\]\'"=$^*~\\-]+)*)?')

sep = r'(?:(?:[.#](?:[\w\d_:./-]+))'
leftSelector = r'|(?:\[\s*[\w\d_:*-]+\s*(?:[$*^~]?\s*\=\s*(?:[\'"]\s*[^"\']+\s*[\'"])|(?:[^\]]+))?\s*\]))?'
left = '('+sep + leftSelector+')'
right = r'((?:[*%#.\[][^"\']+)*)?'

newSelector = re.compile('(?:'+left + right+')?')

#This regex is used to detect [href*=someVal] | [href^=some_val] | [href$='someVal']
attributeSubStringSelector = re.compile(r'([~*$^])\s*\=')

emptyElements = [ "br", "hr", "meta", "link", 
                  "base", "link", "img", "embed",
                  "param", "area", "col", "input",
                  "basefont", "frame", "isindex" ]


class HtmlDomNode:
     def __init__( self, nodeName="text",nodeType=3):
          self.nodeName = nodeName
          self.nodeType = nodeType
          self.parentNode = None
          self.nextSiblingNode = None
          self.previousSiblingNode = None
          self.children = []
          self.attributes = {}
          self.ancestorList = []
          self.text = ""
          self.pos = -1

     def setParentNode( self, parentNode ):
          self.parentNode = parentNode
          return self
     def setSiblingNode( self, siblingNode ):
          self.nextSiblingNode = siblingNode
          return self
     def setPreviousSiblingNode( self, siblingNode ):
          self.previousSiblingNode = siblingNode
          return self
     def setChild( self, child ):
          self.children.append( child )
          return self
     def setAttributes( self, attributeDict ):
          self.attributes.update( attributeDict )
          return self
     def setAncestor( self, nodeList ):
          self.ancestorList = list(nodeList)
          return self
     def setText( self, text ):
          self.text = text
          return self
          
     def setAsFirstChild(self,node ):
          self.children.insert( 0, node )
          return self

     def setAncestorsForChildren( self, ancestor ):
          for childNode in self.children:
               if not childNode.ancestorList:
                    childNode.generateAncestorList()
               childNode.setAncestor( childNode.ancestorList + ancestor )
               childNode.setAncestorsForChildren( ancestor )
          return self
               
     def firstChild(self):
          return self.children[0]
     def lastChild(self):
          return self.children[-1]
          
     def getNextSiblingNode( self ):
        return self.nextSiblingNode
        
     def getPreviousSiblingNode(self):
          return self.previousSiblingNode
          
     def getAncestorList(self):
          return self.ancestorList
     def getName(self):
          return self.nodeName
     def html(self, spaces = 0 ):
          htmlStr = " " * spaces
          
          htmlStr += "<" + self.nodeName
          for attrName in self.attributes:
               htmlStr += " " + attrName +"="+'"'+" ".join(self.attributes[attrName]) + '"'
               
          htmlStr += '>'
          
          for node in self.children:
               if node.nodeType == 3:
                    htmlStr += "\n" + " " * ( spaces + 4 ) + node.text.strip()
               else:
                    htmlStr += "\n" + node.html( spaces + 4 )
                    
          htmlStr += "\n" + " " * spaces + '</'+self.nodeName +'>'
          return htmlStr

     def getText(self):
          textStr = ""
          for node in self.children:
               if node.nodeType == 3:
                    textStr += node.text
               else:
                    textStr += node.getText() + '\n'
          return textStr
     def getNextSiblings(self):
          siblingsSet = []
          node = self.nextSiblingNode
          while node:
               if node not in siblingsSet and node.nodeType != 3 :
                    siblingsSet.append(node)
               node = node.nextSiblingNode
          return siblingsSet
     def getPreviousSiblings(self):
          siblingsSet = []
          node = self.previousSiblingNode
          while node:
               if node not in siblingsSet and node.nodeType != 3:
                    siblingsSet.append(node)
               node = node.previousSiblingNode
          return siblingsSet
     def attr( self, attrName, val = False ):
          if val:
                self.attributes[ attrName ] = val.split()
               #return self.attributes.get( attrName, "Undefined Attribute" );
          else:
               return " ".join( self.attributes.get( attrName, ["Undefined","Attribute"] ) )
     
     def removeAttr( self, attrName ):
        if attrName in self.attributes.keys():
            del self.attributes[ attrName ]
                   
     def remove( self, node ):
         """
            This function must be called on parent node of the node.
            It removes the node from the parents child list and adjusts
            the sibling links.
         """
         parent_node = self
         if parent_node:
            try:
                pos = parent_node.children.index( node )
                del parent_node.children[ pos ]
                if node.previousSiblingNode and node.nextSiblingNode:
                    node.previousSiblingNode.nextSiblingNode = node.nextSiblingNode
                    node.nextSiblingNode.previousSiblingNode = node.previousSiblingNode
            except ValueError:
                raise Exception( str( node ) + ": node is not a children of the parent node" )
                
         return node
         
     def append( self, node ):
        if isinstance( node, HtmlDomNode ):
            if len( self.children ) == 0:
                self.setChild( node )
            else:
                self.after( None, node )
            node.setParentNode( self )
        else:
            raise Exception( "Invalid node object. object must be of type HtmlDomNode." )
     def prepend( self, node ):
        if isinstance( node, HtmlDomNode ):
            if len( self.children ) == 0:
                self.setAsFirstChild( node )
            else:
                self.before( None, node )
            node.setParentNode( self )
        else:
            raise Exception( "Invalid node object. object must be of type Element." )
     def after( self, src, target ):
        """
            Function must be called on the parent node.
            This function sets target node after the src node.
            if src node is None then the target node will be set
            as the last child of the parent node.
        """
        flag = False
        currNextSiblingNode = None
        if src == None:
            src = self.lastChild()
            currNextSiblingNode = src.getNextSiblingNode()
            self.setChild( target )
            flag = True
        if isinstance( target, HtmlDomNode ) and isinstance( src, HtmlDomNode ):
            if not flag:
                currNextSiblingNode = src.getNextSiblingNode()
                index = self.children.index( src )
                self.children.insert( index + 1, target )
                target.setParentNode( self )
            
            src.setSiblingNode( target )
            target.setPreviousSiblingNode( src )
            target.setSiblingNode( currNextSiblingNode )
            if currNextSiblingNode:
                currNextSiblingNode.setPreviousSiblingNode( target )
        else:
            raise Exception( "Invalid node object. object must be of type Element." )

     def before( self, src, target ):
        """
            Function must be called on the parent node.
            This function sets target node before the src node.
            if src node is None then the target node will be set 
            as the first child of the parent node.
        """
        flag = False
        currPrevSiblingNode = None
        if src == None:
            src = self.firstChild()
            currPrevSiblingNode = src.getPreviousSiblingNode()
            self.setAsFirstChild( target )
            flag = True
        if isinstance( target, HtmlDomNode ) and isinstance( src, HtmlDomNode ):
            if not flag:
                currPrevSiblingNode = src.getPreviousSiblingNode()
                try:
                    index = self.children.index( src )
                    self.children.insert( index, target )
                    target.setParentNode( self )
                    
                except ValueError:
                    raise Exception( "source node object must be children of the parent object" )
            src.setPreviousSiblingNode( target )
            target.setSiblingNode( src )
            target.setPreviousSiblingNode( currPrevSiblingNode )
            if currPrevSiblingNode :
                currPrevSiblingNode.setSiblingNode( target )
        else:
            raise Exception( "Invalid node object. object must be of type HtmlDomNode." )
     
     def insertAfter( self, node ):
        """
            This Function is similar to after but here
            self is target node and "node" is the source node
        """     
        if isinstance( self, HtmlDomNode ) and isinstance( node, HtmlDomNode ):
            node.parentNode.after( node, self )
            
     def insertBefore( self, node ):
        """
            This Function is similar to before but here
            self is target node and node is the source node
        """
        if isinstance( self, HtmlDomNode ) and isinstance( node, HtmlDomNode ):
            node.parentNode.before( node, self )
     def copy( self ):
        """
            This function creats copy of the "self" node
        """
        n = None
        if self.nodeType == 1:
            n = HtmlDomNode( self.nodeName, self.nodeType )
            n.children = self.children
            n.attributes = self.attributes
        elif self.nodeType == 3:
            n = HtmlDomNode()
            n.text = self.text
        return n
        
     def generateAncestorList( self ):
        parent = self.parentNode
        while parent:
            self.ancestorList.append( parent )
            parent = parent.parentNode

class HtmlDom:
     def __init__( self, url="" ):
          self.baseURL = url

          #@var:domNodes is a dictionary which holds all the tags present in the page.
          # So that it will be very easy to look up the tags when queried.
          self.domNodes = {}
          self.domNodesList = []
          self.referenceToRootElement = None
          self.sorted = False
          self.xml_file = False

     def createDom(self,htmlString=None):
          if htmlString:
               data = htmlString
               self.parseHTML( data )
               #self.domDictToList()               
          else:
               try:
                    try:
                         import urllib.request as urllib2
                    except ImportError:
                         #For python3
                         raise Exception( "urllib module not found" )
                    request = urllib2.Request(self.baseURL)
                    request.add_header('User-agent','Mozilla/9.876 (X11; U; Linux 2.2.12-20 i686, en; rv:2.0) Gecko/25250101 Netscape/5.432b1 (C-MindSpring)')
                    response = urllib2.urlopen(request)
                    data = response.read().decode( self.getEncoding( response ) )
                    name, extension = os.path.splitext( self.baseURL )
                    if extension.lower().strip() == ".xml":
                        self.xml_file = True
                    self.parseHTML( data )
                    #self.domDictToList()
               except Exception as e:
                    print("Error while reading url: %s" % (self.baseURL))
                    #new_addition:@start
                    raise Exception
                    #new_addition:@end

          return self
     def parseHTML( self, data ):
          # pos is used in order to preserve their logical order of nodes in the document
          # because i am using dictionary datastructure to store the nodes so while retriving
          # nodes their orders will be different. In order to avoid that i sort the set on
          # "pos" variable[ sort_function:time sort ]
          pos = 1
          index = 0
          doc_seen = False
          comment_string = "<!--"
          #Node stack will hold the parent Nodes. The top most node will be the current parent.
          nodeStack = []
          while data:
              # to remove new lines.
               data = data.strip()
               #Doctype tag
               if not doc_seen and ( data.find("<!DOCTYPE") == 0 or data.find("<!doctype") == 0 or data.find( "<?xml" ) == 0 ):
                    #Just pass through the doctype tag.
                    index = data.find(">")
                    data = data[ index + 1:]
                    doc_seen = True
                    continue
               #Comment Node
               #if data.find("<!--") == 0:
               #pointer = 0
               for i in range( 0, 4 ):
                 if data[ i ] != comment_string[ i ]:
                   break
               else:
                    #Just pass through the comment node.
                    index = data.find("-->")
                    data = data[index + 3:]
                    continue

               #index is just used for extracting texts within the tags.
               #could change in future.
               index = data.find("<")

               # len(nodeStack) >= 1 means found text content between the end of a tag and the start of a new tag
               if len( nodeStack ) >= 1:
                    _index = -1
                    #if "script" element is on the top of the stack then entire content of it will be stored in a single text node
                    if nodeStack[-1].getName() == "script":
                         _index = data.find( "</script>" )
                         if _index != -1:
                              tmpData = data[ :_index ]
                    #if "style" element is on the top of the stack then entire content of it will be stored in a single text node
                    elif nodeStack[-1].getName() == "style":
                         _index = data.find("</style>")
                         if _index != -1:
                              tmpData = data[:_index]
                    else:
                         tmpData = data[:index]
                         
                    #tmpData should not be empty.
                    if tmpData:
                         textNode = HtmlDomNode("text")
                         textNode.setText(tmpData)
                         
                         textNode.pos = pos
                         pos += 1
                         
                         if len(nodeStack) > 0:
                              nodeStack[ -1 ].append( textNode )
                              textNode.setAncestor( nodeStack[::-1] )
                              self.domNodesList.append( textNode )
                              self.registerNode( textNode.nodeName, textNode )
                         if _index != -1:
                              data = data[_index:].strip()
                         else:
                              data = data[index:].strip()
                              
                    else:
                         data = data.strip()
               #end of a tag
               if data.find("</") == 0:
                    match = endTag.search( data )
                    data = data[len(match.group()):].strip()
                    try:
                         nodeStack.pop()
                         continue
                    except IndexError:
                         nodeStack = []

               #start of a tag.
               if data.find("<") == 0:
                    match = startTag.search( data )
                    if not match:
                         #Fail silently
                         continue
                         
                    #match.group(1) will contain the element name
                    elementName = match.group(1)
                    #new addition:  added lower function to the element name.
                    domNode = HtmlDomNode( elementName.lower(), 1 )
                    domNode.pos = pos
                    pos += 1
                    attr = match.group(2)
                    if attr:
                         #converting multispaces into single space.for easy handling of attributes
                         attr = whiteSpace.sub( ' ', attr.strip() )
                         attr = attributeSplitter.findall( attr )
                         attrDict = {}
                         for attrName,attrValues in attr:
                              attrDict[attrName] = attrValues.split()

                         domNode.setAttributes( attrDict )
                    if len(nodeStack) > 0:
                         # nodeStack[ -1 ] is a HtmlDomNode object
                         nodeStack[ -1 ].append( domNode )
                         #setting ancestor list
                         domNode.setAncestor( nodeStack[::-1] )
                         #push the current node into the stack.so now domNode becomes the current parent node.
                         #if the current node is an empty element,do not push the element into the stack.
                         if not self.xml_file:
                             if elementName not in emptyElements:
                                  nodeStack.append( domNode )
                         elif match.group().find( "/>" ) == -1:
                             nodeStack.append( domNode )
                    else:
                         domNode.setAncestor( nodeStack )
                         # nodeStack is a list
                         nodeStack.append( domNode )                         
                         self.referenceToRootElement = domNode

                    self.registerNode( domNode.nodeName, domNode )
                    data = data[len(match.group()):].strip()
               else:
                    domNode = HtmlDomNode( "text" )
                    domNode.pos = pos
                    pos += 1
                    if index == -1:
                        domNode.setText( data )
                        data = data[ len( data ): ].strip()
                    else:
                        domNode.setText( data[ :index ] )
                        data = data[ index: ]
                    self.registerNode( domNode.nodeName, domNode ) 
                    self.domNodesList.append( domNode )

     def registerNode( self, nodeName, domNode ):
          if self.domNodes.get(nodeName,None):
               #self.domNodes[nodeName].append( domNode )
               if domNode not in self.domNodes[ nodeName ]:
                    self.domNodes[nodeName].append( domNode )               
#               self.domNodes[ nodeName ] += self.getUniqueNodes( self.domNodes[ nodeName ], [ domNode ] )
          else:
               self.domNodes[ nodeName ] = [domNode]
               
     def updateDomNodes( self, newDomNodes ):
          for nodeName in newDomNodes:
               self.domNodes[nodeName] += newDomNodes[nodeName]
     def removeFromDomDict( self, node ):   
        if self.domNodes.get( node.nodeName, None ):
            try:
                pos = self.domNodes[ node.nodeName ].index( node )
                del self.domNodes[ node.nodeName ][ pos ]
            except ValueError:
                pass
        
     def getDomDict(self):
          return self.domNodes

     def domDictToList(self, no_text_node = True ):
          n = []
          for nodeName in self.domNodes:
               for selectedNode in self.domNodes[nodeName]:
                    #Converting the dictionary into a list of values.
                    self.domNodesList.append( selectedNode )
                    if not no_text_node:
                        if selectedNode.nodeType == 1:
                            n.append( selectedNode )
          
          self.domNodesList = list( set( self.domNodesList ) )
          if not self.sorted:
              self.domNodesList = sorted( self.domNodesList, key = lambda x: x.pos )
              self.sorted = True
          if not no_text_node:
                return sorted( n, key = lambda x: x.pos )
          return self.domNodesList
                    
     #new edition nList=[]
     #this addition is for find function for HtmlNodeList
     def find(self,selectors,nList=[]):
          classSelector = []
          idSelector = []
          attributeSelector = {}
          attributeSelectorFlags = {
                                     '$':False,'^':False,'*':False,'noVal':False,"~":False
                                   }
          selectorMethod = {'+':False,'>':False}
          attr_list = []
          #new edition
          nodeList = nList
          _index = -1
          # the following line is required for handling following kinds of inputs
          # "div+a" getConverted into "div + a". Now it is easy to split on spaces.
          selectors = re.sub(r'([+>])',r' \1 ',selectors)
          
          #normalizing the inputs.
          selectors = whiteSpace.sub( ' ', selectors )
          
          selectors = selectors.split()
          
          data = ""
          elemName = ""
          for value in selectors:
               _index += 1
               if value == '+' or value == '>':
                    selectorMethod[value] = True
                    continue
               match = selector.search( value )
               if match:
                    elemName = match.group(1)
                    data = match.group(2)
                    invalid = 0
                    while data and invalid != 100:
                         invalid += 1
                         match = newSelector.search( data )
                         if match:
                              data = match.group(2)                
                              #class selector
                              if match.group(1).find(".") == 0:
                                   index = match.group(1).find(".")
                                   classSelector.append( match.group(1)[index+1:] )
                              #id selector
                              elif match.group(1).find("#") == 0:
                                   index = match.group(1).find("#")
                                   idSelector.append( match.group(1)[index +1:] )
                              # attribute selector
                              elif match.group(1).find("[") == 0:
                                   index = match.group(1).find("]")
                                   attr = match.group(1)[1:][:-1]
                                   attrMatch = re.search( attributeSubStringSelector, attr )
                                   if attrMatch:
                                        attributeSelectorFlags[attrMatch.group(1)] = True
                                        _index = attr.find(attrMatch.group(1))
                                        attr = attr[:_index - len(attr)] + attr[_index + 1:]
                                        attr = attr.split("=")
                                   elif attr.find("=") == -1:
                                        #Only attribute name is given not the value.
                                        attributeSelectorFlags['noVal'] = True
                                        attr = attr.split()
                                        attr.append('')
                                   else:
                                        attr = attr.split("=")
                                   #new addition
                                   attr[1] = re.sub(r'[\'\"]?','',attr[1])
                                   #new addition
                                   attributeSelector[attr[0]] = attr[1]
                                   if attr[ 1 ] == '':
                                        attributeSelectorFlags[ "noVal" ] = True
                                   attr_list.append( ( dict( attributeSelector ), dict( attributeSelectorFlags ) ) )
                                   attributeSelector = {}
                                   attributeSelectorFlags = {
                                                                    '$':False,'^':False,'*':False,'noVal':False,"~":False
                                                            }
                    if invalid == 100:
                        raise Exception( "Invalid regular expression" )
                    else:
                        invalid = 0
                    if elemName:
                         if elemName == "*" and _index == 0:
                            nodes = self.domDictToList( no_text_node = False )
                            nodeList = []
                         elif elemName == "*":
                            nodes = self.domDictToList( no_text_node = False )
                         else:
                             nodes = self.domNodes.get( elemName, [] )
                    else:
                         if classSelector:
                              nodes = self.getNodesWithClassOrId(classSelector[-1],selectType='class')
                         elif idSelector:
                              nodes = self.getNodesWithClassOrId(idSelector[-1],selectType='id')
                         elif attr_list:
                              nodes = []
                              #new Addition:Mon 13 Feb
                              for a_s, a_f in attr_list:
                                  nodes += self.getNodesWithAttributes( a_s, a_f )
                              nodes = list( set( nodes ) )
                              
                    tmpList = []
                    method = ''
                    for node in nodeList:
                         if selectorMethod['+']:
                              method = '+'
                              for selectedNode in nodes:
                                   if node.nextSiblingNode == selectedNode:
                                        tmpList.append( selectedNode )
                              tmpList = list( set( tmpList ) )
                         elif selectorMethod['>']:
                              method = '>'
                              for selectedNode in nodes:
                                   if selectedNode in node.children:
                                        tmpList.append( selectedNode )
                              tmpList = list( set( tmpList ) )
                         else:
                              for selectedNode in nodes:
                                   if not selectedNode.ancestorList:
                                        selectedNode.generateAncestorList()
                                   if node in selectedNode.ancestorList:
                                        tmpList.append( selectedNode )
                              tmpList = list( set( tmpList ) )
                    if method != '':
                        selectorMethod[ method ] = False
                        method = ''
                    if not nodeList:
                         tmpList = nodes
                    nodes = tmpList
                    nodeList = []
                    for node in nodes:
                         nodeAccepted = True
                         for value in classSelector:
                              if value not in node.attributes.get('class',[]):
                                   nodeAccepted = False
                                   break
                         if nodeAccepted:
                              for value in idSelector:
                                   if value not in node.attributes.get('id',[]):
                                        nodeAccepted = False
                                        break
                         if nodeAccepted:
                              for a_s, a_f in attr_list:
                                   nodeAccepted = self.getNodesWithAttributes( a_s, a_f, [node] )
                                   if not nodeAccepted:
                                        break
                         if nodeAccepted:
                              nodeList.append(node)
                    classSelector = []
                    idSelector = []
                    attributeSelector = {}
                    attributeSelectorFlags = {'$':False,'^':False,'*':False,'noVal':False}
                    attr_list = []
               if not nodeList:
                    break
          
          nodeList = sorted( nodeList, key = lambda x : x.pos )
          return HtmlNodeList( nodeList, self )
     def getNodesWithClassOrId( self,className="",nodeList = None,selectType=""):
          tmpList = []
          for nodeName in self.domNodes:
               [ tmpList.append( selectedNode ) for selectedNode in self.domNodes[nodeName] if className in selectedNode.attributes.get(selectType,['']) ]
          return tmpList
     def getNodesWithAttributes( self, attributeSelector,attributeSelectorFlags,nodeList = None):
          if not self.sorted:
              self.domDictToList()
          tmpList = self.domNodesList
          
          if nodeList:
               tmpList = nodeList
          key,attrValue = list(attributeSelector.items())[0]
          newList = []
          for node in tmpList:
               nodeAccepted = True
               if attributeSelectorFlags['$']:
                    #if attributeSelector[key] not in node.attributes.get(key,[''])[-1][len(node.attributes.get(key,[''])[-1])::-1]:
                    if attributeSelector[key] != node.attributes.get(key,[''])[-1]:
                         nodeAccepted = False
               elif attributeSelectorFlags['^']:
                    if attributeSelector[key] not in node.attributes.get(key,[''])[0]:
                         nodeAccepted = False
               elif attributeSelectorFlags['*']:
                    if attributeSelector[key] not in " ".join(node.attributes.get(key,[])):
                         nodeAccepted = False
               elif attributeSelectorFlags['noVal']:
                    if key not in node.attributes:
                         nodeAccepted = False
               elif attributeSelectorFlags[ "~" ]:
                    if attributeSelector[key] not in node.attributes.get( key, [] ):
                        nodeAccepted = False
               elif attributeSelector[key] != " ".join(node.attributes.get(key,[])):
                    nodeAccepted = False
               if nodeAccepted:
                    newList.append(node)
          return newList
     def getUniqueNodes(self,srcList, newList ):
          tmpList = []
          for selectedNode in newList:
               if selectedNode not in srcList:
                    tmpList.append( selectedNode  )
          return tmpList
     def getEncoding( self, response ):
          encoding = 'utf-8'
          for key,val in response.headers.items():
               if key == 'Content-Type':
                    encoding = val.split(";")
                    try:
                         encoding = encoding[1].split('=')[1].strip()
                    except IndexError:
                         encoding = 'utf-8'
                         break
                    break
          return encoding                    

class HtmlNodeList:
     def __init__( self, nodeList,dom,prevNodeList=[],prevObject = None):
          self.nodeList = nodeList
          self.htmlDom = dom
          # new addition
          self.len = len( self.nodeList )
          # used for iteration
          self.counter = 0
          
          self.previousNodeList = prevNodeList
          if not prevObject:
               self.referenceToPreviousNodeListObject = self
          else:
               self.referenceToPreviousNodeListObject = prevObject
               
     def __iter__( self ):
          self.counter = 0
          return self

     def __next__( self ):
          if self.counter >= self.len:
               raise StopIteration
          else:
               tmpObj = self.eq( self.counter )
               self.counter += 1
               return tmpObj
               
     def __getitem__( self, index ):
          if isinstance( index, int ):
              return self.eq( index )
          elif isinstance( index, slice ):
              return HtmlNodeList( self.nodeList[ index ], self.htmlDom, self.nodeList, self )
     
     def children(self, selector = None, all_children = False):
          childrenList = []
          if not all_children:
              for node in self.nodeList:
                   [ childrenList.append(child) for child in node.children if child.nodeType == 1]
          else:
              for node in self.nodeList:
                   [ childrenList.append(child) for child in node.children ]
          
          if selector:
               return HtmlNodeList( childrenList, self.htmlDom, self.nodeList, self ).filter( selector )
          else:
               childrenList = sorted( childrenList, key = lambda x: x.pos )
               return HtmlNodeList( childrenList,self.htmlDom,self.nodeList,self)
          
     def html( self, data = None ):
          if not data:
              htmlStr = ""
              for node in self.nodeList:
                   htmlStr += node.html()
              return htmlStr
          else:
              for node in self.nodeList:
                for child_node in node.children:
                    node.remove( child_node )
                    self.htmlDom.removeFromDomDict( child_node )
                    del child_node
                node.children = []
              self.append( data )
              return self
               
     def text( self, data = None ):
          if not data:
              textStr = ""
              for node in self.nodeList:
                   textStr += node.getText()
              return textStr
          else:
              for node in self.nodeList:
                for child_node in node.children:
                    node.remove( child_node )
                    self.htmlDom.removeFromDomDict( child_node )
                    del child_node
                node.children = []
              self.append( data )
              return self
     
     def attr( self, attrName, val = False):
          if len( self.nodeList ) > 0 and not val:
               return self.nodeList[0].attr( attrName, val )
          elif val:
               for node in self.nodeList:
                    node.attr( attrName, val )
               return self
          else:
               raise IndexError
     
     def removeAttr( self, attrName ):
        for node in self.nodeList:
            node.removeAttr( attrName )
        return self

     def filter(self,selector):
          nList = self.htmlDom.find( selector )
          tmpList = []
          for node in self.nodeList:
               if node in nList.nodeList:
                    tmpList += self.getUniqueNodes( tmpList, [node] )
                    
          tmpList = sorted( tmpList, key = lambda x : x.pos )

          return HtmlNodeList( tmpList,self.htmlDom, self.nodeList,self)
          
     def _not(self,selector ):
          nList = self.htmlDom.find( selector )
          tmpList = []
          for node in self.nodeList:
               if node not in nList.nodeList:
                    tmpList.append( node )
                    
          tmpList = list( set( tmpList ) )
          tmpList = sorted( tmpList, key = lambda x : x.pos )
          return HtmlNodeList( tmpList,self.htmlDom, self.nodeList, self )
          
     def eq(self,index ):
          if index >= -len(self.nodeList) and index < len( self.nodeList ):
               return HtmlNodeList( [self.nodeList[index]], self.htmlDom, self.nodeList,self )
          else:
               return None
               
     def first( self ):
          return self.eq(0)
          
     def last( self ):
          return self.eq( len(self.nodeList ) - 1 )
          
     def has(self,selector ):
          nList = self.htmlDom.find( selector )
          tmpList = []
          for node in self.nodeList:
               for selectedNode in nList.nodeList:
                    if not selectedNode.ancestorList:
                        node.generateAncestorList()
                    if node in selectedNode.ancestorList:
                        tmpList += self.getUniqueNodes( tmpList, [ node ] )
          
          tmpList = sorted( tmpList, key = lambda x: x.pos )
          return HtmlNodeList( tmpList,self.htmlDom, self.nodeList,self)
          
     def _is(self,selector):
          val = self.filter( selector )
          if val.nodeList:
               return True
          else:
               return False
               
     def next(self, selector = None):
          tmpList = []
          nextNode = None
          for node in self.nodeList:
               nextNode = node.nextSiblingNode
               while nextNode and nextNode.nodeType == 3:
                    nextNode = nextNode.nextSiblingNode
               if nextNode:
                    tmpList += self.getUniqueNodes( tmpList, [ nextNode ] )
          
          if selector:
               return HtmlNodeList( tmpList, self.htmlDom, self.nodeList, self ).filter( selector )
          else:
               tmpList = sorted( tmpList, key = lambda x: x.pos )
               return HtmlNodeList( tmpList, self.htmlDom, self.nodeList,self)
     
     def nextAll(self, selector = None ):
          tmpList = []
          for node in self.nodeList:
               tmpList += self.getUniqueNodes( tmpList, node.getNextSiblings() )
               
          if selector:
               return HtmlNodeList( tmpList, self.htmlDom, self.nodeList, self ).filter( selector )
          else:
               tmpList = sorted( tmpList, key = lambda x: x.pos )
               return HtmlNodeList( tmpList, self.htmlDom, self.nodeList, self)
     
     def nextUntil(self,selector):
          nList = self.htmlDom.find(selector)
          siblingsSet = []
          tmpList = []
          selectedNodeList = []
          for node in self.nodeList:
               #This function gets all the siblings.
               tmpList = node.getNextSiblings()
               for selectedNode in nList.nodeList:
                    try:
                         index = tmpList.index( selectedNode )
                         selectedNodeList = tmpList[:index]
                         siblingsSet += self.getUniqueNodes( siblingsSet, selectedNodeList )
                         break
                    except ValueError:
                         pass
               else:
                    siblingsSet += self.getUniqueNodes( siblingsSet, tmpList )
          siblingsSet = sorted( siblingsSet, key = lambda x: x.pos )                    
          return HtmlNodeList( siblingsSet,self.htmlDom, self.nodeList, self)
     
     def prev(self, selector = None ):
          tmpList = []
          prNode = None
          for node in self.nodeList:
               prevNode = node.previousSiblingNode
               while prevNode and prevNode.nodeType == 3: # if its text node: loop
                    prevNode = prevNode.previousSiblingNode
               if prevNode:
                    tmpList += self.getUniqueNodes( tmpList, [ prevNode ] )
               
          if selector:
               return HtmlNodeList( tmpList, self.htmlDom, self.nodeList, self ).filter( selector )
          else:
               tmpList = sorted( tmpList, key = lambda x: x.pos )            
               return HtmlNodeList( tmpList, self.htmlDom, self.nodeList, self)
     
     def prevAll( self, selector = None ):
          tmpList = []
          for node in self.nodeList:
               tmpList += self.getUniqueNodes( tmpList, node.getPreviousSiblings() )
          if selector:
               return HtmlNodeList( tmpList, self.htmlDom, self.nodeList, self ).filter( selector )
          else:
               tmpList = sorted( tmpList, key = lambda x: x.pos )               
               return HtmlNodeList( tmpList, self.htmlDom, self.nodeList, self)
     
     def prevUntil(self,selector):
          nList = self.htmlDom.find(selector)
          siblingsSet = []
          tmpList = []
          selectedNodeList = []
          for node in self.nodeList:
               #This function gets all the previous siblings.
               tmpList = node.getPreviousSiblings()
               for selectedNode in nList.nodeList:
                    try:
                         index = tmpList.index( selectedNode )
                         selectedNodeList = tmpList[:index]
                         siblingsSet += self.getUniqueNodes( siblingsSet, selectedNodeList )
                         break
                    except ValueError:
                         pass
               else:
                    siblingsSet += self.getUniqueNodes( siblingsSet, tmpList )
                    
          siblingsSet = sorted( siblingsSet, key = lambda x: x.pos )
          return HtmlNodeList( siblingsSet,self.htmlDom, self.nodeList, self )
     
     def siblings(self,selector=None):
          """
             This function gets all the siblings of each node present in the current 
             HtmlNodeList object.( including previous and next siblings )
          """
          prevSiblingsSet = []
          nextSiblingsSet = []
          siblingsSet = []
          for node in self.nodeList:
               prevSiblingsSet = node.getPreviousSiblings()
               siblingsSet += self.getUniqueNodes( siblingsSet, prevSiblingsSet )
               nextSiblingsSet = node.getNextSiblings()
               siblingsSet += self.getUniqueNodes( siblingsSet, nextSiblingsSet )
          if selector:
               return HtmlNodeList( siblingsSet, self.htmlDom, self.nodeList, self ).filter( selector )
          else:
               siblingsSet = sorted( siblingsSet, key = lambda x: x.pos )
               return HtmlNodeList( siblingsSet, self.htmlDom, self.nodeList,self )
          
     def parent( self, selector = None ):
          """
               This function gets all the parents, not just immediate parent
               of each node present in the current HtmlNodeList object.
               selector: It is used to filter the parent list means to select only specific parents.
          """     
          tmpList = []
          for node in self.nodeList:
               if node.parentNode:
                    tmpList += self.getUniqueNodes( tmpList, [ node.parentNode ] )
          if selector:
               return HtmlNodeList( tmpList, self.htmlDom, self.nodeList, self ).filter( selector )
          else:
               tmpList = sorted( tmpList, key = lambda x: x.pos )
               return HtmlNodeList( tmpList, self.htmlDom, self.nodeList,self)
               
     def parents( self, selector = None ):
          """
               This function gets all the parents, not just immediate parent but parent of parent and so on..
               of each node present in the current HtmlNodeList object.
               selector: It is used to filter the parent list means to select only specific parents.
          """     
          tmpList = []
          for node in self.nodeList:
               if not node.ancestorList:
                    node.generateAncestorList()
               tmpList += self.getUniqueNodes( tmpList, node.ancestorList )
          if selector:
               return HtmlNodeList( tmpList, self.htmlDom, self.nodeList, self ).filter( selector )
          else:
               tmpList = sorted( tmpList, key = lambda x: x.pos ) 
               return HtmlNodeList( tmpList, self.htmlDom, self.nodeList, self)

     def parentsUntil(self,selector):
          """
               This function gets all the parents, not just immediate parent but parent of parent and so on..
               of each node present in the current HtmlNodeList object until the parent specified by the 
               selector is reached.
          """
          nList = self.htmlDom.find(selector)
          parentsList = []
          tmpList = []
          selectedNodesList = []
          for node in self.nodeList:
               if not node.ancestorList:
                    node.generateAncestorList()
               tmpList = node.ancestorList
               for selectedNode in nList.nodeList:
                    try:
                         index = tmpList.index( selectedNode )
                         selectedNodeList = tmpList[:index]
                         parentsList += self.getUniqueNodes( parentsList, selectedNodeList )
                         break
                    except ValueError:
                         pass
               else:
                    parentsList += self.getUniqueNodes( parentsList, tmpList )
          parentsList = sorted( parentsList, key = lambda x: x.pos )
          return HtmlNodeList( parentsList, self.htmlDom, self.nodeList, self )
          
     def add(self,selector):
          """
             This function adds new elements to the current list.
          """
          nList = self.htmlDom.find( selector )
          newNodeList = self.nodeList + self.getUniqueNodes( self.nodeList, nList.nodeList )
          newNodeList = sorted( newNodeList, key = lambda x: x.pos )
          return HtmlNodeList( newNodeList, self.htmlDom, self.nodeList,self )
          
     def andSelf(self):
          newList = []
          newList += self.getUniqueNodes( newList, self.previousNodeList )
          newList += self.getUniqueNodes( newList, self.nodeList )
          
          newList = sorted( newList, key = lambda x: x.pos )
          return HtmlNodeList( newList, self.htmlDom, self.nodeList,self )
     
     def end(self):
          return HtmlNodeList( self.previousNodeList, self.htmlDom, self.referenceToPreviousNodeListObject.referenceToPreviousNodeListObject.nodeList,self.referenceToPreviousNodeListObject.referenceToPreviousNodeListObject )

     def find(self,selector):
          nList = self.htmlDom.find( selector,self.nodeList )
          return HtmlNodeList( nList.nodeList, self.htmlDom, self.nodeList, self )

     def write( self,fileName ):
          import codecs
          fp = codecs.open( fileName, "w","utf-8")
          fp.write( self.html() )
          fp.close()
          return self
     def length(self):
          return len(self.nodeList)
          
     def contains( self, pattern ):
          pattern = re.compile( pattern )
          selectedNodeList = []
          for node in self.nodeList:
            text = node.getText()
            if pattern.search( text ):
              selectedNodeList += self.getUniqueNodes( selectedNodeList, [node] )
              
          selectedNodeList = sorted( selectedNodeList, key = lambda x: x.pos )
          return HtmlNodeList( selectedNodeList, self.htmlDom, self.nodeList, self )
          
     def toList(self):
         return self.nodeList
     
     def append( self, nodes ):
        flag = False
        if isinstance( nodes, HtmlNodeList ):
            nodes = nodes.toList()
        elif isinstance( nodes, list ):
            nodes = nodes
        elif isinstance( nodes, str ):
            h = HtmlDom().createDom( nodes )
            h.domDictToList()
            nodes = h.domNodesList
            tmpList = []
            other_nodes = []
            flag = True
            for node in nodes:
                if not node.parentNode:
                    tmpList.append( node )
                else:
                    self.htmlDom.registerNode( node.nodeName, node )
                    other_nodes.append( node )
            nodes = tmpList
            nodes = sorted( nodes, key = lambda x: x.pos )
        else:
            nodes = [ nodes ]
        if len( self.nodeList ) == 1:
            for node in nodes:
                self.htmlDom.removeFromDomDict( node )
                if node.parentNode:
                    node.parentNode.remove( node )
                self.nodeList[ 0 ].append( node )
                self.htmlDom.registerNode( node.nodeName, node )
        else:
            removedAll = False
            for eachNode in self.nodeList:
                for node in nodes:
                    if not removedAll and node.parentNode:
                        self.htmlDom.removeFromDomDict( node )
                        try:
                            if node.parentNode:
                                node.parentNode.remove( node )
                        except Exception:
                            removedAll = True
                    node_c = node.copy()
                    eachNode.append( node_c )
                    self.htmlDom.registerNode( node_c.nodeName, node_c )
        self.htmlDom.sorted = False
        modifyPositions( self.htmlDom.referenceToRootElement )
        return self
                
     def prepend( self, nodes ):
        flag = False
        if isinstance( nodes, HtmlNodeList ):
            nodes = nodes.toList()[::-1]
        elif isinstance( nodes, list ):
            nodes = nodes[ ::-1]
        elif isinstance( nodes, str ):
            h = HtmlDom().createDom( nodes )
            h.domDictToList()
            nodes = h.domNodesList
            tmpList = []
            other_nodes = []
            flag = True
            for node in nodes:
                if not node.parentNode:
                    tmpList.append( node )
                else:
                    self.htmlDom.registerNode( node.nodeName, node )
                    other_nodes.append( node )
            nodes = tmpList
            nodes = sorted( nodes, key = lambda x: x.pos )
            nodes = nodes[::-1]
        else:
            nodes = [ nodes ]
        if len( self.nodeList ) == 1:
            for node in nodes:
                self.htmlDom.removeFromDomDict( node )
                if node.parentNode:
                    node.parentNode.remove( node )
                self.nodeList[ 0 ].prepend( node )
                self.htmlDom.registerNode( node.nodeName, node )
        else:
            removedAll = False
            for eachNode in self.nodeList:
                for node in nodes:            
                    if not removedAll and node.parentNode:
                        self.htmlDom.removeFromDomDict( node )
                        try:
                            if node.parentNode:
                                node.parentNode.remove( node )
                        except Exception:
                            removedAll = True
                    node_c = node.copy()
                    eachNode.prepend( node_c )
                    self.htmlDom.registerNode( node_c.nodeName, node_c )
        self.htmlDom.sorted = False
        modifyPositions( self.htmlDom.referenceToRootElement )
        return self
     def after( self, nodes ):
        flag = False
        if isinstance( nodes, HtmlNodeList ):
            nodes = nodes.toList()[::-1]
        elif isinstance( nodes, list ):
            nodes = nodes[::-1]
        elif isinstance( nodes, str ):
            h = HtmlDom().createDom( nodes )
            h.domDictToList()
            nodes = h.domNodesList
            tmpList = []
            other_nodes = []
            flag = True
            for node in nodes:
                if not node.parentNode:
                    tmpList.append( node )
                else:
                    self.htmlDom.registerNode( node.nodeName, node )
                    other_nodes.append( node )
            nodes = tmpList
            nodes = sorted( nodes, key = lambda x: x.pos )
            nodes = nodes[ ::-1 ]
        else:
            nodes = [ nodes ]
        if len( self.nodeList ) == 1:
            parent = self.nodeList[ 0 ].parentNode
            for node in nodes:
                if node.parentNode:
                    node.parentNode.remove( node )
                self.htmlDom.removeFromDomDict( node )
                if parent:
                    parent.after( self.nodeList[ 0 ], node )
                else:
                    self.nodeList[ 0 ].after( None, node )
                self.htmlDom.registerNode( node.nodeName, node )
        else:
            removedAll = False
            for eachNode in self.nodeList:
                for node in nodes:            
                    if not removedAll and node.parentNode:
                        self.htmlDom.removeFromDomDict( node )
                        try:
                            if node.parentNode:
                                node.parentNode.remove( node )
                        except Exception:
                            removedAll = True
                    node_c = node.copy()
                    parent = eachNode.parentNode
                    if parent:
                        parent.after( eachNode, node_c )
                    else:
                        eachNode.after( None, node_c, self.htmlDom )
                    self.htmlDom.registerNode( node_c.nodeName, node_c )
        self.htmlDom.sorted = False
        modifyPositions( self.htmlDom.referenceToRootElement )
        return self
     def before( self, nodes ):
        flag = False
        if isinstance( nodes, HtmlNodeList ):
            nodes = nodes.toList()
        elif isinstance( nodes, list ):
            nodes = nodes
        elif isinstance( nodes, str ):
            h = HtmlDom().createDom( nodes )
            h.domDictToList()
            nodes = h.domNodesList
            tmpList = []
            other_nodes = []
            flag = True
            for node in nodes:
                if not node.parentNode:
                    tmpList.append( node )
                else:
                    self.htmlDom.registerNode( node.nodeName, node )
                    other_nodes.append( node )
            nodes = tmpList            
            nodes = sorted( nodes, key = lambda x: x.pos )
        else:
            nodes = [ nodes ]
        if len( self.nodeList ) == 1:
            parent = self.nodeList[ 0 ].parentNode        
            for node in nodes:
                if node.parentNode:
                    node.parentNode.remove( node )
                self.htmlDom.removeFromDomDict( node )
                if parent:
                    parent.before( self.nodeList[ 0 ], node )
                else:
                    self.nodeList[ 0 ].before( None, node )
                self.htmlDom.registerNode( node.nodeName, node )                    
        else:
            removedAll = False
            for eachNode in self.nodeList:
                for node in nodes:            
                    if not removedAll and node.parentNode:
                        self.htmlDom.removeFromDomDict( node )
                        try:
                            if node.parentNode:
                                node.parentNode.remove( node )
                        except Exception:
                            removedAll = True
                    node_c = node.copy()
                    parent = eachNode.parentNode
                    if parent:
                        parent.before( eachNode, node_c )
                    else:
                        eachNode.before( None, node_c )
                    self.htmlDom.registerNode( node_c.nodeName, node_c )
        self.htmlDom.sorted = False
        modifyPositions( self.htmlDom.referenceToRootElement )
        return self
     
     def appendTo( self, nodes, context = None ):
        """ 
            Here nodes is the src and self is the target.
            nodes can be either HtmlNodeList or string
            if it is a string object then user has to supply 
            a HtmlDom context object otherwise self`s context
            will be used.
        """
        if isinstance( nodes, HtmlNodeList ):
            nodes.append( self )
        elif isinstance( nodes, str ):  
            if context and isinstance( context, HtmlDom ):
                cotext.find( nodes ).append( self )
            else:
                self.htmlDom.find( nodes ).append( self )
        if not context:
            modifyPositions( self.htmlDom.referenceToRootElement )
        else:
            modifyPositions( context.referenceToRootElement )
        return self
     def prependTo( self, nodes, context = None ):
        """ 
            Here nodes is the src and self is the target.
            nodes can be either HtmlNodeList or string
            if it is a string object then user has to supply 
            a HtmlDom context object otherwise self`s context
            will be used.
        """
        if isinstance( nodes, HtmlNodeList ):
            nodes.prepend( self )
        elif isinstance( nodes, str ):
            if context and isinstance( context, HtmlDom ):
                context.find( nodes ).prepend( self )
            else:
                self.htmlDom.find( nodes ).prepend( self )
                
        if not context:
            modifyPositions( self.htmlDom.referenceToRootElement )
        else:
            modifyPositions( context.referenceToRootElement )                
        return self
        
     def insertAfter( self, nodes, context = None ):
        if isinstance( nodes, HtmlNodeList ):
            nodes.after( self )
        elif isinstance( nodes, str ):
            if context and isinstance( context, HtmlDom ):
                context.find( nodes ).after( self )
            else:
                self.htmlDom.find( nodes ).after( self )
        if not context:
            modifyPositions( self.htmlDom.referenceToRootElement )
        else:
            modifyPositions( context.referenceToRootElement )                
        return self
        
     def insertBefore( self, nodes, context = None ):
        if isinstance( nodes, HtmlNodeList ):
            nodes.before( self )
        elif isinstance( nodes, str ):
            if context and isinstance( context, HtmlDom ):
                context.find( nodes ).before( self )
            else:
                self.htmlDom.find( nodes ).before( self )
        if not context:
            modifyPositions( self.htmlDom.referenceToRootElement )
        else:
            modifyPositions( context.referenceToRootElement )                
        return self
     
     def remove( self, selector = None ):
        if not selector:
            nodes = self.nodeList
        else:
            n = self.filter( selector )
            nodes = n.nodeList
        for node in nodes:
            if node.parentNode:
                node.parentNode.remove( node )
                self.htmlDom.removeFromDomDict( node )
                del node
        self.htmlDom.sorted = False
        return self
     
     def getNode( self ):
        return self.nodeList[ 0 ]
     
     def getUniqueNodes(self,srcList, newList ):
          tmpList = []
          for selectedNode in newList:
               if selectedNode not in srcList:
                    tmpList.append( selectedNode  )
                    
          return tmpList

def createElement( nodeName ):
    return HtmlDomNode( nodeName, 1 )
    
def createTextElement( nodeVal ):
    elem = HtmlDomNode( "text", 3 )
    elem.setText( nodeVal )
    return elem
    
def modifyPositions( node, pos = 1 ):
    node.pos = pos
    for chld in node.children:
        pos = modifyPositions( chld, pos + 1 )
    return pos
