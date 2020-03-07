import scrapy
from urllib import parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
class UrldataSpider(scrapy.Spider):
    name = 'urldata'
    allowed_domains = ['getbootstrap.com/docs/4.0/examples/']
    start_urls = ['http://getbootstrap.com/docs/4.0/examples/']

    def parse(self, response):
        url_list = response.css('.col-sm-6.col-md-4.col-xl-3.mb-3 a::attr(href)').extract()
        url_list = [parse.urljoin(response.url,a) for a in url_list]
        count = 0
        f = open("./spiders/ulrData.txt", "w")
        # f.write("start\n")

        for url in url_list:
            print(url)
            # self.web_normalise(url,0)
            f.write(url+"\n")
        f.close()
    def web_normalise(self, url, count):
        print("web_normalise")
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
            if(e.localName =="li" && e.firstChild.nodeName=="#text"){
                data = e.firstChild.data.trim()
                if(data != ""){
                   dom["type"] = "p"; 
                }
            }
            dom["x"] = position.x;
            dom["y"] = position.y;
            dom["width"] = position.width;
            dom["height"] = position.height;
            dom["left-padding"] = e.style.paddingLeft;
            dom["top-padding"] = e.style.paddingTop;
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
                        node.style.backgroundColor = "blueviolet";
                    }else if(dom.type=="input"){
                        console.log(dom.type);
                        node.style.backgroundColor = "#0000FF";
                    }else if(dom.type=="button"||dom.type=="a"){
                        console.log(dom.type);
                        node.style.backgroundColor = "#FFFF00";
                    }else if(dom.type=="p"||dom.type=="span"||dom.type=="i"||dom.type=="strong"||dom.type=="label"||dom.type=="small"){
                        console.log(domJson[i].type);
                        node.style.backgroundColor = "red";
                    }else if(dom.type=="h1"||dom.type=="h2"||dom.type=="h3"||dom.type=="h4"||dom.type=="h5"){
                        console.log(dom.type);
                        node.style.backgroundColor = "lawngreen";
                    }else if(dom.type=="div"||dom.type=="ul"){
                        node.style.borderStyle = "solid";
                        node.style.borderWidth = "1px";
                    }
                    document.getElementById(i).appendChild(node)
                }

            }
        }
        return domJson
        """
        browser.get(url)
        browser.set_window_size(1349, 625)
        width = browser.execute_script("return document.documentElement.scrollWidth")
        height = browser.execute_script("return document.documentElement.scrollHeight")
        browser.set_window_size(width, height)
        domJson = browser.execute_script(js)
        count = count + 1
        browser.save_screenshot("web_norm/" + str(count) + ".png")
        print("**********************")
        browser.close()