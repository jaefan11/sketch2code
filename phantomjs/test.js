e = document.getElementsByTagName("body")
console.log(e)
e1 = e[0]
e_list = e1.firstElementChild.children
console.log(e1.firstElementChild.getClientRects())
console.log(e_list)
console.log(e_list[1].getClientRects())

next = e_list[1].children[0]
console.log(next.getClientRects())