var domJson = [];
        var domList = [];
        domList.push({"node":document.getElementsByTagName("body")[0],"parentNode":-1});
//        console.log(document.getElementsByTagName("body")[0])
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
//            console.log(e)
//            console.log(e.getClientRects())
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
            if(domJson[i].flag){
                childList =[]
//                console.log(domJson[i].flag)
            }
            for(var domId of childList){
                if(domJson[i].flag){
//                    childList =[]
                    console.log(domJson[i].flag)
                }
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
//                        console.log(dom.type);
                        node.style.backgroundColor = "blueviolet";
                        domJson[domId].flag=1
                        node.style.left = (dom.x - domJson[i].x+2) + "px";
                        node.style.top = (dom.y - domJson[i].y+2) + "px";
                        node.style.width = dom.width-5 + "px";
                        node.style.height = dom.height-5 + "px";
                    }else if(dom.type=="input"){
//                        console.log(dom.type);
                        node.style.backgroundColor = "#0000FF";
                        domJson[domId].flag=1
                        node.style.left = (dom.x - domJson[i].x+2) + "px";
                        node.style.top = (dom.y - domJson[i].y+2) + "px";
                        node.style.width = dom.width-5 + "px";
                        node.style.height = dom.height-5 + "px";
                    }else if(dom.type=="button"||dom.type=="a"){
//                        console.log(dom.type);
                        node.style.backgroundColor = "#FFFF00";
                        domJson[domId].flag=1
                        node.style.left = (dom.x - domJson[i].x+2) + "px";
                        node.style.top = (dom.y - domJson[i].y+2) + "px";
                        node.style.width = dom.width-5 + "px";
                        node.style.height = dom.height-5 + "px";
                    }else if(dom.type=="p"||dom.type=="span"||dom.type=="i"||dom.type=="strong"||dom.type=="label"||dom.type=="small"){
//                        console.log(domJson[i].type);
                        node.style.backgroundColor = "red";
                        domJson[domId].flag=1
                        node.style.left = (dom.x - domJson[i].x+2) + "px";
                        node.style.top = (dom.y - domJson[i].y+2) + "px";
                        node.style.width = dom.width-5 + "px";
                        node.style.height = dom.height-5 + "px";
                    }else if(dom.type=="h1"||dom.type=="h2"||dom.type=="h3"||dom.type=="h4"||dom.type=="h5"){
//                        console.log(dom.type);
                        node.style.backgroundColor = "lawngreen";
                        domJson[domId].flag=1
                        node.style.left = (dom.x - domJson[i].x+2) + "px";
                        node.style.top = (dom.y - domJson[i].y+2) + "px";
                        node.style.width = dom.width-5 + "px";
                        node.style.height = dom.height-5 + "px";
                    }else if(dom.type=="div"||dom.type=="ul"){
                        node.style.borderStyle = "solid";
                        node.style.borderWidth = "1px";
                    }
                    if(document.getElementById(i)){
                        document.getElementById(i).appendChild(node)
                    }

                }

            }
        }