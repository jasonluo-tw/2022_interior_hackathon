var root = location.protocol + '//' + location.host;

$("#search").click(function(evt){
    evt.preventDefault()
    console.log("ajax 送出")
    get_request()
})

function get_request () {
    var form = $("form").serializeArray()
    console.log(form)
    let query = {}
    let flag = true
    for(let i in form) {
        let name = form[i]['name']
        let value = form[i]['value']
        console.log(name, value)
        //if(value == "") {
        //    alert(`${name} 沒有填值`)
        //    flag = false
        //    break
        //}
        query[name] = value
    }
    
    let search_url = new URLSearchParams(query).toString()
    let redirect_url = root + "/tenant/map?" + search_url
    // send url
    if(flag) {
        location.href = redirect_url 
    }
}

// smart btn
$("#bt_ss1").click(function(evt) {
    location.href = root + "/tenant/map?smart=bt_ss1"
})
$("#bt_ss2").click(function(evt) {
    location.href = root + "/tenant/map?smart=bt_ss2"
})
$("#bt_ss3").click(function(evt) {
    location.href = root + "/tenant/map?smart=bt_ss3"
})
//Not implemented yet
//$("#bt_ss4").click(function(evt) {
//    location.href = root + "/tenant/map?smart=bt_ss4"
//})