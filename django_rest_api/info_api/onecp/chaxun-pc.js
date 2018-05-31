
$(function () {
    $('.queding-cha').click(function () {
        var shuru1=$('.shuruzhanggao').val()
        if (shuru1==''){
            alert('请输入查询账号')
        }else{
            $.ajax({
                type:"GET",
                dataType:'json',
                data: {
                    search:shuru1
                },
                url: "http://char.ngrok.uplaygo.com:8000/event/?search",
                success:function(res){
                    console.log(res.results)
                    if(res.results.length==0){
                        $('.jinduchaxun').html("傻狗也");
                    }else{
                        $('.jinduchaxun').html("<div class='res-chenggong'><p1>66666</p1></div>");
                    }
                },
                error:function(res){
                    $('.jinduchaxun').html("傻狗也");
                }
            });
        }


    })
})