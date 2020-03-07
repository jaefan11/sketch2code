from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time


def web_normalise(url, count):
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    browser = webdriver.Chrome(options=chrome_options)
    # browser = webdriver.Chrome()
    js = r"""
        var domJson = [];
        var domList = [];
        domList.push({"node":document.getElementsByTagName("body")[0],"parentNode":-1});
        console.log(document.getElementsByTagName("body")[0])
        while(domList.length>0){
            var dom = domList.shift();
            if(nodeToJson(dom.node)){
                domJson.push(nodeToJson(dom.node));
                var parent = domJson.length-1
                if(dom.parentNode!=-1){
                    domJson[dom.parentNode].contains.push(parent)
                }
            }
        
            var nodeNext = dom.node.firstChild;
            while (nodeNext!=null){
                if(nodeNext.nodeType==1 && nodeNext.localName!="script"){
                    domList.push({"node":nodeNext,"parentNode":parent});
                }
                nodeNext = nodeNext.nextSibling;
            }
        
        }
        
        function nodeToJson(e) {
            var dom = {};
            if(e.getClientRects().length==0){
                return null;
            }
            var position = e.getClientRects()[0];
            
            dom["type"] = e.localName;
            if(e.localName =="li" && e.firstChild!=null && e.firstChild.nodeName=="#text"){
                data = e.firstChild.data.trim()
                if(data != ""){
                   dom["type"] = "p"; 
                }
            }
            dom["x"] = position.x;
            dom["y"] = position.y;
            dom["width"] = position.width;
            dom["height"] = position.height;
            dom["left-padding"] = 1;
            dom["top-padding"] = 1;
            dom["contains"] = [];
            return dom;
        }
        var node = document.getElementsByTagName("body")[0];
        var dom = domJson[0];
        node.innerHTML="";
        node.id = 0;
        node.style.position = "absolute";
        node.style.left = dom.x + "px";
        node.style.top = dom.y + "px";
        node.style.width = dom.width + "px";
        node.style.height = dom.height + "px";
        node.style.paddingTop = dom.topPadding + "px";
        node.style.paddingLeft = dom.leftPadding + "px";
        
        for(i=0;i<domJson.length;i++){
            console.log(domJson[i]);
            var childList = domJson[i].contains;
            if(domJson[i].flag){
                childList =[]
//                console.log(domJson[i].flag)
            }
            for(var domId of childList){
                if(document.getElementById(domId)==null){
                    var dom = domJson[domId];
                    var node = document.createElement(dom.type);
                    node.id = domId;
                    node.style.position = "absolute";
                    node.style.left = (dom.x - domJson[i].x) + "px";
                    node.style.top = (dom.y - domJson[i].y) + "px";
                    node.style.width = dom.width + "px";
                    node.style.height = dom.height + "px";
                    node.style.paddingTop = dom.topPadding + "px";
                    node.style.paddingLeft = dom.leftPadding + "px";
                    if(dom.type=="img"||dom.type=="svg"||dom.type=="video"){
                        console.log(dom.type);
                        domJson[domId].flag=1
                        node.style.backgroundColor = "blueviolet";
                        node.style.left = (dom.x - domJson[i].x+2) + "px";
                        node.style.top = (dom.y - domJson[i].y+2) + "px";
                        node.style.width = dom.width-5 + "px";
                        node.style.height = dom.height-5 + "px";
                    }else if(dom.type=="input"||dom.type=="select"){
                        console.log(dom.type);
                        domJson[domId].flag=1
                        node.style.backgroundColor = "#0000FF";
                        node.style.left = (dom.x - domJson[i].x+2) + "px";
                        node.style.top = (dom.y - domJson[i].y+2) + "px";
                        node.style.width = dom.width-5 + "px";
                        node.style.height = dom.height-5 + "px";
                    }else if(dom.type=="button"||dom.type=="a"){
                        console.log(dom.type);
                        domJson[domId].flag=1
                        node.style.backgroundColor = "#FFFF00";
                        node.style.left = (dom.x - domJson[i].x+2) + "px";
                        node.style.top = (dom.y - domJson[i].y+2) + "px";
                        node.style.width = dom.width-5 + "px";
                        node.style.height = dom.height-5 + "px";
                    }else if(dom.type=="p"||dom.type=="span"||dom.type=="i"||dom.type=="strong"||dom.type=="small"){
                        console.log(domJson[i].type);
                        domJson[domId].flag=1
                        node.style.backgroundColor = "red";
                        domJson[domId].flag=1
                        node.style.left = (dom.x - domJson[i].x+2) + "px";
                        node.style.top = (dom.y - domJson[i].y+2) + "px";
                        node.style.width = dom.width-5 + "px";
                        node.style.height = dom.height-5 + "px";
                    }else if(dom.type=="h1"||dom.type=="h2"||dom.type=="h3"||dom.type=="h4"||dom.type=="h5"||dom.type=="h6"||dom.type=="label"){
                        console.log(dom.type);
                        domJson[domId].flag=1
                        node.style.backgroundColor = "lawngreen";
                        node.style.left = (dom.x - domJson[i].x+2) + "px";
                        node.style.top = (dom.y - domJson[i].y+2) + "px";
                        node.style.width = dom.width-5 + "px";
                        node.style.height = dom.height-5 + "px";
                    }else if(dom.type=="div"||dom.type=="ul"||dom.type=="nav"){
                        node.style.borderStyle = "solid";
                        node.style.borderWidth = "1px";
                    }
                    if(document.getElementById(i)){
                        document.getElementById(i).appendChild(node)
                    }
                }
        
            }
        }
        return domJson
        """
    print("读取")
    browser.get(url)
    browser.set_window_size(1349, 625)
    width = browser.execute_script("return document.documentElement.scrollWidth")
    height = browser.execute_script("return document.documentElement.scrollHeight")
    browser.set_window_size(width, height)
    print("处理。。")
    domJson = browser.execute_script(js)
    browser.save_screenshot("web_norm/" + str(count) + ".png")
    print("保存",domJson )
    browser.close()
f = open("ulrData.txt")
ulrList = f.readlines()
count = 6
# for ulr in ulrList:
#     print(ulr.strip())
#     print(count)
#     count = count + 1
#     web_normalise(ulr.strip(),count)
web_normalise("https://getbootstrap.com/docs/4.0/examples/checkout/",3)

