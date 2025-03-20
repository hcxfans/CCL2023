#import pycantonese
#url = ("https://childes.talkbank.org/data/Biling/YipMatthews.zip")
#corpus = pycantonese.read_chat(url)
#corpus.n_files()
#len(corpus.words())

#corpus = pycantonese.hkcancor()
#corpus.head()

import os
import pycantonese
import json
#import jieba
from graphviz import Digraph
import hanlp
import zhconv

def substring_before(s, delim):
    if not s:
        return ''
    if delim in s:
        return s.partition(delim)[0]
    else:
        return s
def substring_after(s, delim):
    if not s:
        return ''
    if delim in s:
        return s.partition(delim)[2]
    else:
        return ''
def genSDPgraph(mcdict,graph):
    g = Digraph('sdp')
    g.attr(rankdir="same" )
    glen=len(graph)
    for i in range(glen):
        #print(i)
        gitemList=str(graph[i]).split('	')
        #g.node(name=gitemList[0],fontname="SimSun bold",label=gitemList[1])
        g.node(name=gitemList[0],fontname="SimSun bold",label=mcdict.get(gitemList[1], gitemList[1]))
        
        source=substring_before(gitemList[8],':')
        elabel=substring_after(gitemList[8],':')
        if source=='0' or elabel=='Root':
            g.edge('Root',gitemList[0],label=elabel)
        else:
            g.edge(source,gitemList[0],label=elabel)
        
    return g
def printSDPgraph(mcdict,graph):
    tgraph=graph
    glen=len(tgraph)
    for i in range(glen):
        #print(i)
        gitemList=str(tgraph[i]).split('	')
        #g.node(name=gitemList[0],fontname="SimSun bold",label=gitemList[1])
        print(gitemList[0]+'\t'+mcdict.get(gitemList[1], gitemList[1])+'\t'+'...'+'\t'+gitemList[8])

def printAMRgraph(mcdict,graph):
    tgraph=graph
    gstr=str(tgraph)
    tstr=substring_before(gstr, ' /')
    RootTage=substring_after(tstr, '(')
    mytrip=tgraph.triples
    #print(mytrip)
    
    nodeList=[]
    #for i in range(len(mytrip)):
    #    print(mytrip[i])
    for i in range(len(mytrip)):
        if mytrip[i][1]==':instance':
            nodeword=substring_before(mytrip[i][2],'-')
            nodecword=mcdict.get(nodeword, nodeword)
            ttup=mytrip[i]
            tlist=list(ttup)
            tlist[2]=tlist[2].replace(nodeword,nodecword)
            gstr=gstr.replace(nodeword,nodecword)
            mytrip[i]=tuple(tlist)
            nodeList.append(mytrip[i])
    print(gstr)
def genAMRgraph(mcdict,graph):
    g = Digraph('amr')
    g.attr(rankdir="same" )
    gstr=str(graph)
    tstr=substring_before(gstr, ' /')
    RootTage=substring_after(tstr, '(')
    mytrip=graph.triples
    nodeList=[]
    edgeList=[]
    #for i in range(len(mytrip)):
    #    print(mytrip[i])
    for i in range(len(mytrip)):
        if mytrip[i][1]==':instance':
            nodeList.append(mytrip[i])
        #elif ':arg' in mytrip[i][1]:
        else:
            edgeList.append(mytrip[i])
    for i in range(len(nodeList)):
        nodeword=substring_before(nodeList[i][2],'-')
        nodecword=mcdict.get(nodeword, nodeword)
        tmpNode=nodeList[i][2].replace(nodeword,nodecword)
        g.node(name=nodeList[i][0],fontname="SimSun bold",label=tmpNode)
    
    g.node(name='Root', fontname="Times New Roman bold", style="invis",)
    g.edge('Root',RootTage,label='')
    for i in range(len(edgeList)):
        g.edge(edgeList[i][0],edgeList[i][2],label=edgeList[i][1])        
    return g
def addwords(word,attr):
    word= zhconv.convert(word.strip(), 'zh-hk')
    #word=word.strip()
    path=pycantonese.__file__
    (filepath, tempfilename) = os.path.split(path)
    filepath=filepath+'\\data\\hkcancor\\FC-RPlus_v.cha'
    #print(filepath)
    f = open(filepath,'r+',encoding="utf-8")
    f_line_xxa=f.readline()
    f_lines_a=f_line_xxa.split('\t')
    f_line_mor=f.readline()
    f_lines_m=f_line_mor.split('\t')
    #print(f_line_xxa.split('\t'))
    #wordin=False
    #for i in range(1,len(f_lines_a)):
    #    if (word is f_lines_a[i]):
    #        wordin=True
    #        break
    wordin=word in f_lines_a
    if not wordin:
        f_line_xxa=f_lines_a[0]+'\t'+word
        for i in range(1,len(f_lines_a)):
            f_line_xxa=f_line_xxa+'\t'+f_lines_a[i]
        f_line_mor=f_lines_m[0]+'\t'+attr
        for i in range(1,len(f_lines_m)):
            f_line_mor=f_line_mor+'\t'+f_lines_m[i]
        #print(f_line_xxa)
        #print(f_line_mor)
        f.seek(0,0)
        f.write(f_line_xxa)
        f.write(f_line_mor)
        f.close()
def CanToMan(words):
    #word= zhconv.convert(word.strip(), 'zh-hk')
    #word=word.strip()
    path=pycantonese.__file__
    (filepath, tempfilename) = os.path.split(path)
    filepath=filepath+'\\data\\can_man\\hkcandict.json'
    #print(filepath)
    f =open(filepath,encoding='utf-8') #打开‘hkcandict.json’的json文件
    res=f.read()  #读文件
    hkcandict=json.loads(res)#把json串变成python的数据类型：字典
    tmwords=[]
    for i in range(len(words)):
        if words[i] in hkcandict:#[words[i]]["Mor"][0]["国语释义"]:
            #print('OK'+words[i])
            tmwords.append(hkcandict[words[i]]["Mor"][0]["国语释义"])
        elif words[i]:
            tmwords.append(words[i])
        #tmwords.append(dict.get(hkcandict[words[i]]["Mor"][0]["国语释义"], words[i]))
    f.close()
    return tmwords
def update_POSword(word):
    #word= zhconv.convert(word.strip(), 'zh-hk')
    #word=word.strip()
    path=pycantonese.__file__
    (filepath, tempfilename) = os.path.split(path)
    filepath=filepath+'\\pos_tagging\\POS_dict.json'
    #print(filepath)
    f =open(filepath,encoding='utf-8') #打开‘cce-cedict.json’的json文件
    res=f.read()  #读文件
    POSdict=json.loads(res)#把json串变成python的数据类型：字典
    if POSdict[word]["POS"]:
        f.close()
        return POSdict[word]["POS"]
    else:
        return "X"
    f.close()
if __name__=='__main__':
#    data="我都系，我叫李明。好高兴识得你。"
    data="张女士哋我妈咪嘅好朋友,佢系做惯乞儿懒做官。"
    data="話就話係公平競爭，到最後咪又係塘水滾塘魚。"
    data="佢哋两个大缆都扯唔埋，你能撮合到佢哋，我㓟个头畀你当凳坐。"
    
    data="呢排現金周轉唔嚟，搞到我一戙都冇。"
    data="呢排現金周轉唔嚟，搞到我一栋都冇。"
    data="佢今日寫嗰啲嘢，乜嘢都九唔搭八。"
    data="呢個部門就得我哋三個人，單眼佬睇榜——一眼睇曬。"
    #data="佢哋两个大缆都扯唔埋，你能撮合到佢哋，我㓟个头畀你当凳坐。"
    #data="唐伯虎手执毛笔，好似写字噉嘅款，原来系用豉油搽鸡翼"
    #data="每逢个月光咁靓嗰阵，你向佢许个愿哩，一定会心想事成嘅。"
    #data="我个花名呢就叫做'挛都拗得直，死都拗返生'"
    #data="婆婆，妹妹包龙星系咪同你哋个个都有十冤九仇嘅?"
    #data="妹妹佢高傲，但係宅心人厚；佢低调，但係受万人景仰；佢可以将神赐畀人类嘅火运用得出神入化，可以煮出堪称火之艺术嘅超级菜式！佢究竟係神仙嘅化身，定係地狱嚟嘅使者呢？"
    #data="佢可以將神賜畀人類嘅火運用得出神入化，可以煮出堪稱火之藝術嘅超級菜式"
    hkdata= zhconv.convert(data, 'zh-hk')
    #print(hkdata)
    #words = list(jieba.cut(data))
    #print(words)
#    data="""
#我妈咪有一把利落嘅短发,睇上去好有精神,佢唔高亦唔矮，唔肥亦唔瘦.佢系一个好冇记性嘅人,而且仲好罗唆.佢成日都唔记得D野,好多次,我叫佢去买D野,佢话就话听日去买,但系第2日佢根本就唔记得左呢件事,话咩好忙，唔记得左.结果最后过左几日先去买。而且有时佢都成日唔记得熄灯等等其他嘅野。佢呢样野真系令到我好烦,搞到我要成日提佢,但系佢喺做野同读书(或学野)方面就好认真，绝对唔会求其。
#系我考试成绩唔好个阵，距需然都会哦我几句，叫我唔好咁大头虾，但更多嘅系用和蔼嘅语气鼓励我，叫我下次考好D，我系学习方面遇到困难个阵，距会抽时间出黎耐心教我，等我明白晒，系我唔小心整亲手个阵，距会好仔细咁帮我处理伤口，其实有时真系要到大个仔（女）个阵先会明白父母嘅苦心，距地嘅长气，严厉嘅教导无非都系为我地好，其实距地总系时时为我地著想。
#"""
#    data="你食咗飯未呀?食咗喇!你聽日得唔得閒呀?"
#    data="偶然睇到尼段话第一时间真系觉得好激气啊,好想即刻写个评论驳返佢,但捻到同尼种人争来争去都冇咩意思,唔同文化真系好难倾得埋噶,觉得自己嘅文化冇比人地理解同"


# Have you eaten yet? Yes,I have! Are you free tomorrow?
#pycantonese.parse_text(data)
    #corpus=pycantonese.parse_text(data,parallel=False)
    
    #data_dir = os.path.join(os.path.dirname(__file__), "data", "hkcancor")
    #print(data_dir)
    #reader = _HKCanCorReader.from_dir(data_dir)
    #for f in reader._files:
    #    f.file_path = f.file_path.replace(data_dir, "").lstrip(os.sep)
    #return reader
    #addwords('张女士','n|zoeng1neoi5si6')
    #addwords(' 短发','n|jyu5si1')
    addwords(' 大缆都扯唔埋','a|daai6laam6dou1ce2m4maai4')
    addwords(' 㓟个头畀你当凳坐','v|pai1go3tau4bei2nei5dong3dang3tso5')
    addwords(' 一戙都冇','a|jat7dung6dou1mou5')
    addwords(' 呢排','adv|ni1paai4')
    addwords(' 單眼佬睇榜——一眼睇曬','adj|daan1ngaan5lou2tai2bong2jat7ngaan5taosaai2')
    corpus=pycantonese.parse_text(hkdata)
    tmp=corpus.head()
    #print(tmp)
    words=corpus.words()
    for i in range(len(words)):
        words[i]=zhconv.convert(words[i], 'zh2Hans')
    print(words)
    token_list=corpus.tokens()
    
    path=pycantonese.__file__
    (filepath, tempfilename) = os.path.split(path)
    filepath=filepath+'\\pos_tagging\\POS_dict.json'
    #print(filepath)
    f =open(filepath,encoding='utf-8') #打开‘cce-cedict.json’的json文件
    res=f.read()  #读文件
    f.close()
    POSdict=json.loads(res)#把json串变成python的数据类型：字典
    for i in range(len(token_list)):
        if POSdict.__contains__(token_list[i].word):
        #if POSdict[token_list[i].word]["POS"]:
            token_list[i].jyutping=POSdict[token_list[i].word]["Jutping"]
            token_list[i].pos=POSdict[token_list[i].word]["POS"]
            token_list[i].gloss=POSdict[token_list[i].word]["gloss"]
    #token_list[3].pos='ADJ'
    
    for i in range(len(token_list)):
        #print(token_list[i])
        #token_list[i].word=zhconv.convert(token_list[i].word, 'zh-cn')
        #token_list[i].word=zhconv.convert(token_list[i].word, 'zh-cn')
        print(zhconv.convert(token_list[i].word, 'zh2Hans'),end=',')
        print(token_list[i].jyutping,end=',')
        print(token_list[i].pos,end=',')
        print(token_list[i].gloss)
        #print(token_list[i].mor)
        #print(token_list[i].gra)
            
    
    

    
    '''
    新細明體：PMingLiU
    細明體：MingLiU
    標楷體：DFKai-SB
    黑体：SimHei
    宋体：SimSun
    新宋体：NSimSun
    仿宋：FangSong
    楷体：KaiTi
    仿宋_GB2312：FangSong_GB2312
    楷体_GB2312：KaiTi_GB2312
    微軟正黑體：Microsoft JhengHei
    微软雅黑体：Microsoft YaHei
    '''
    
    #mwords=['他', '今天', '写', '那些', '东西', '，', '什么东西', '都', '八竿子打不着', '。']
    mwords=CanToMan(words)
    #twords=["呢個", "部門", "就","得",  "我哋", "三", "個", "人", "，", "單眼佬睇榜——一眼睇曬", "。"]
    #mwords=["這個", "部門", "就","得",  "我們", "三", "個", "人", "，", "一目了然", "。"]
    mcdict={}
    for i in range(len(mwords)):
        mcdict.update({mwords[i]: words[i]})
        #mcdict.update({mwords[i]: twords[i]})
    
    #print("哈哈")
    #print(mwords)
    print('mwords:')
    print(mwords)

    amr = hanlp.load('MRP2020_AMR_ENG_ZHO_XLM_BASE')
    amrgraph = amr(mwords)
    print('\n')
    printAMRgraph(mcdict,amrgraph)
    sdp = hanlp.load('SEMEVAL16_ALL_ELECTRA_SMALL_ZH')
    sdpgraph = sdp(mwords)
    print('\n')
    printSDPgraph(mcdict,sdpgraph)

    g2 = Digraph('词性拼音')
    c0 = Digraph(name='child0')
    c0.graph_attr['rankdir'] = 'LR'
    c2 = Digraph(name='child1')
    c2.graph_attr['rankdir'] = 'LR'
    c1 = Digraph(name='child2', node_attr={'shape': 'plaintext'})
    c1.graph_attr['rankdir'] = 'LR'
    c3 = Digraph(name='child3', node_attr={'shape': 'plaintext'})
    c3.graph_attr['rankdir'] = 'LR'
    
    for i in range(len(words)):
        words[i]=zhconv.convert(words[i], 'zh2Hans')        
        c0.node(name='cy'+str(i),fontname="Microsoft JhengHei",label=words[i])
    #print(len(words))
    for i in range(len(words)):
        #print(i)
        mwords[i]=zhconv.convert(mwords[i], 'zh2Hans')        
        c2.node(name='cg'+str(i),fontname="Microsoft JhengHei",label=mwords[i])
    for i in range(len(words)):
        if token_list[i].jyutping:
            c1.node(name='cj'+str(i),fontname="Microsoft YaHei",label=token_list[i].  jyutping)
        else:
            c1.node(name='cj'+str(i),fontname="Microsoft YaHei",label='')
    for i in range(len(words)):
        c3.node(name='cx'+str(i),fontname="Microsoft YaHei",label=token_list[i].pos)

    
    g2.subgraph(c0)
    g2.subgraph(c1)
    g2.subgraph(c2)
    g2.subgraph(c3)
    #for i in range(len(prcs)):
    #    g2.subgraph(c3[i])
    for i in range(len(words)):
        g2.edge('cy'+str(i), 'cj'+str(i),style="invis",len='0.1')
        g2.edge('cj'+str(i), 'cg'+str(i),style="invis",len='0.1')
        g2.edge('cg'+str(i), 'cx'+str(i),style="invis",len='0.1')
        #g2.edge('cx'+str(i), 'ne'+str(i),style="invis",len='0.1')
        
    g4=genAMRgraph(mcdict,amrgraph)
    g3=genSDPgraph(mcdict,sdpgraph)
    
    g2.render('cxpy.gv', view=False)
    g3.render('sdp.gv', view=False)
    g4.render('amr.gv', view=False)
    #g2.view()
    #print('ok:')
    
    import shutil
    
    if os.path.isfile("Sample2.pdf"):
        os.unlink("Sample2.pdf")
    
    if os.path.isfile("Sample4.pdf"):
        os.unlink("Sample4.pdf")    
     
    shutil.copy("cxpy.gv.pdf","Sample2.pdf")
    
    shutil.copy("amr.gv.pdf","Sample4.pdf")

    from PyPDF2 import PdfWriter, PdfReader, PageObject,Transformation

    pdf_filenames = ['Sample2.pdf','Sample4.pdf']
    
    inputpdf2 = PdfReader(open(pdf_filenames[0], 'rb'), strict=False)
    
    inputpdf4 = PdfReader(open(pdf_filenames[1], 'rb'), strict=False)

    
    page2 = inputpdf2.pages[0]
    
    page4 = inputpdf4.pages[0]

    
    print(page2.mediabox.upper_right[1])
    
    print(page4.mediabox.upper_right[1])

    pdf_writer = PdfWriter()

    total_width = max([page2.mediabox.upper_right[0], page4.mediabox.upper_right[0]])
    total_height =page2.mediabox.upper_right[1]+page4.mediabox.upper_right[1]

    tmp=page4.mediabox.upper_right[1]
    tmp4=round(tmp*0.85)
    
    
    new_page = PageObject.create_blank_page(None, total_width, total_height)
    

    page4.add_transformation(Transformation().translate((total_width-page4.mediabox.upper_right[0])/2,0),1)
    page2.add_transformation(Transformation().translate(0,tmp4),1)
    
    
    
   
    #page2.merge_page(page1)
    #page1.add_transformation(Transformation().translate((total_width-page1.mediabox.upper_right[0])/2,page2.mediabox.upper_right[0]+page3.mediabox.upper_right[0]-1500),1);
    #page2.add_transformation(Transformation().translate((total_width-page2.mediabox.upper_right[0])/2,page3.mediabox.upper_right[0]-200),1);
    '''
    page1.add_transformation(Transformation().translate(0,page2.mediabox.upper_right[0]+page3.mediabox.upper_right[0]+page4.mediabox.upper_right[0]-2650),1);
    page2.add_transformation(Transformation().translate((total_width-page2.mediabox.upper_right[0])/2,page4.mediabox.upper_right[0]+page3.mediabox.upper_right[0]-1500),1);
    page3.add_transformation(Transformation().translate(0,page4.mediabox.upper_right[0]-200),1);
    page4.add_transformation(Transformation().translate((total_width-page4.mediabox.upper_right[0])/2,0),1);
    '''
    
    new_page.merge_page(page2,0)
    
    new_page.merge_page(page4,0)
    pdf_writer.add_page(new_page)
    with open('MergedPDF.pdf','wb') as fileobj:
        pdf_writer.write(fileobj)
    os.startfile('MergedPDF.pdf')
    
