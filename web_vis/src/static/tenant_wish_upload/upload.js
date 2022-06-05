
$("#upload").click(function(evt) {
    evt.preventDefault()
    console.log("ajax 送出")
    post()
})

function post() {
    var form = $("form").serializeArray()
    $.ajax({
        url: 'http://127.0.0.1:5000/api/store_wish',
        method: "post",
        data: form,
        success: function(res) {
            console.log(res)
            if(res == 'success') {
                $("#upload_success").css("display", "initial")
            }else{
                alert('上傳不成功')
            }
        },
        error: function(error) {
            alert('上傳不成功，請填選每個選項')
        }
    })
}

$("#upload_other").click(function(evt){
    $("#upload_success").css("display", "none")
})