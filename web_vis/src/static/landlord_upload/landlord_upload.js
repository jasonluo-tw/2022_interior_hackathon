var root = location.protocol + '//' + location.host;

$("#upload").click(function(evt){
    evt.preventDefault()
    console.log("send")
    post()
})

function post() {
    var form = $("form").serializeArray()
    console.log(form)
    let query = {}
    let flag = true
    for(let i in form){
        let name = form[i]['name']
        let value = form[i]['value']
        if(value == ""){
            //alert(`${name} 沒有填值喔`)
            //flag = false
            //break
        }
        query[name] = value
    }

    let search_url = new URLSearchParams(query).toString()
    let redirect_url = root + "/landlord/map?" + search_url
    //TEST
    flag = true
    if(flag) {
        location.href = redirect_url
    }
}
