$(function () {
    $.ajaxSetup({cache: false});

    $(".left_menu").height($(".frameMax").height());

    $('body').on('click', '.close_btn,.ok_btn', function () {
        $(this).parents('.maskLayer').hide();
    })

    // 选中�?
    $('body').on('click', '.selectline', function () {
        $(this).addClass('selected').siblings().removeClass('selected');
        var valueto = $(this).attr('valueto') ? $($(this).attr('valueto')) : $('#selectid');
        $(valueto).val($(this).attr('selectid'));
    })
    //多�?
    $('body').on('click', '#choose-all', function () {
        $(this).parents('.table').find('.chooseline').removeAttr('checked');
        if ($(this).prop('checked')) {
            $(this).parents('.table').find('.chooseline').attr('checked', 'checked');
        }
    })
    //取消输入框内�?
    $('body').on('click', '.eliminate', function () {
        if ($(this).parents('.rid_check').hasClass('select_channel')) {
            $(this).parents('.content').find('.select_shop input').val('');
        }
        $(this).siblings('input').val('').removeAttr('ids');
    })

    $('.popup_btns .close_btn').click(function () {
        $(this).parents('.maskLayer').hide();
    })

    // 重置密码
    $('.resetPassBtn').click(function () {
        $('.resetPassLayer').show();
        $('.resetPassLayer form').Validform({
            ajaxPost: true,
            tiptype: function (msg, o, cssctl) {
                show_tip(msg);
            },
            tipSweep: true,
            callback: function (r) {
                if (r.error != 0) {
                    show_tip(r.msg, r.error, r.url);
                } else {
                    show_tip('密码修改成功，请重新登录', 'success', 'index');
                }
            }
        });
    })
    $('.upimage span').live('click', function () {
        $(this).parents('li').remove();
    })


    // 前一�? 后一�?
    $('.prev_day, .next_day').click(function () {
        //var quick_select_day = $('.quick_select_day').val();
        if (!$('#start_time').val() || !$('#end_time').val()) {
            return false;
        }
        var quick_select_day = $('#start_time').val().substr(0, 10);
        var quick_date_str = quick_select_day + ' 00:00:00';
        var quick_date = new Date(quick_date_str.replace(/-/g, '/'));

        if ($(this).hasClass('prev_day')) {
            var _day = new Date(quick_date.getTime() - 1000);
        } else {
            var _day = new Date(quick_date.getTime() + 86400100);
            if (_day.getTime() > new Date().getTime()) {
                return false;
            }
        }

        var day = _day.getFullYear() + '-' + (_day.getMonth() < 9 ? '0' : '') + (_day.getMonth() + 1) + '-' + (_day.getDate() < 10 ? '0' : '') + _day.getDate();
        $('.quick_select_day').val(day)
        $('#start_time').val(day + ($('#start_time').val().length > 10 ? ' 00:00:00' : ''));
        $('#end_time').val(day + ($('#end_time').val().length > 10 ? ' 23:59:59' : ''));
    })

    // hover信息提示
    $('.hover_tips_ico').mouseover(function () {
        $('.box_tips').show();
    });
    $('.hover_tips_ico').mouseout(function () {
        $('.box_tips').hide();
    });

    // 禁止输入空格
    $('body').on('keydown', '.banInputSapce', function (e) {
        return banInputSapce(e);
    })

    // 密码框禁止粘�?
    $('body').on('paste', 'input[type=password]', function (e) {
        alert('密码框禁止粘贴，请直接输�?');
        return false;
    })

    // 设定每页条数
    $('body').on('change', '.pagesize', function () {
        setCookie('pagesize', $(this).val(), 365);
        var pageDiv = $(this).parent('div');
        $(pageDiv).find('.page').val(1);
        $(pageDiv).find('.page').attr('currentpage', 1);
        $(pageDiv).find('.jump').click();
    })
})

//设置cookie
function setCookie(c_name, value, expiredays) {
    var exdate = new Date();
    exdate.setDate(exdate.getDate() + expiredays)
    document.cookie = c_name + "=" + escape(value) + ";path=/" +
        ((expiredays == null) ? "" : ";expires=" + exdate.toGMTString())
}

function banInputSapce(e) {
    var keynum;
    if (window.event) {
        keynum = e.keyCode
    }
    else if (e.which) {
        keynum = e.which
    }
    if (keynum == 32) {
        show_tip('不能输入空格');
        return false;
    }
    return true;
}

// 信息提示
function show_tip(message) {
    if ($('#show_tip .tips').html() || message) {
        $('#show_tip .ok_btn').removeAttr('onclick');
        $('#show_tip .popup_btns').show();
        if (message) {
            var error = !isNaN(arguments[1]) ? arguments[1] : (arguments[1] == 'success' ? 0 : 'error');
            var type = !isNaN(error) ? (error < 0 ? 'error' : 'success') : error;
            var fun = arguments[2] ? arguments[2] : '';
            message = error != 0 ? message : (message.length > 0 && message != 'success' && message != 'success' ? message : '操作成功');
            $('#show_tip .tips').html('<div class="' + type + 'Message">' + message + '</div>');
            if (message == '正在提交数据�?' || fun == 'unbtn') {
                $('#show_tip .popup_btns').hide();
            } else if ((fun && error == 0) || error == -40001) {
                fun = fun.indexOf('(') >= 0 ? fun : 'window.location.href="' + (fun.indexOf("http") < 0 ? '/' : '') + fun + '"';
                $('#show_tip .ok_btn').attr('onclick', fun);
            }
        }
        $('#show_tip').parent('.maskLayer').show();
    }
    $('#show_tip .ok_btn').click(function () {
        $('#show_tip').parent('.maskLayer').hide();
        $('#show_tip .tips').html('');
    })
}

//异步重新加载列表
function ajax_reload(_class) {
    $(".query").addClass("reload");
    $("." + _class + " .reload").click();
    $(".maskLayer").hide();
}

// 确认�?
function confirm_tip(message) {
    var fun = arguments[1] ? arguments[1] : '';
    $('#confirm_tip .ok_btn').removeAttr('onclick');
    $('#confirm_tip .tips').html(message);
    $('#confirm_tip').parent('.maskLayer').show();

    if (fun.length > 0) {
        var ck_fun = fun.indexOf('(') >= 0 ? fun.substring(0, fun.indexOf('(')) : fun;
        var fn = window[ck_fun];
        if (typeof(fn) == 'function') {
            $('#confirm_tip .ok_btn').attr('onclick', fun);
        }
    }
}

// 确认输入�?
function prompt_tip(message) {
    var fun = arguments[1] ? arguments[1] : '';
    $('#prompt_tip .ok_btn').removeAttr('onclick');
    $('#prompt_tip .tips').html(message + ':');
    $('#prompt_tip .prompt_input').val('');
    $('#prompt_tip').parent('.maskLayer').show();
    $('#prompt_tip .prompt_input').val('');
    if (fun.length > 0) {
        var ck_fun = fun.indexOf('(') >= 0 ? fun.substring(0, fun.indexOf('(')) : fun;
        var fn = window[ck_fun];
        if (typeof(fn) == 'function') {
            $('#prompt_tip .ok_btn').attr('onclick', fun);
        }
    }
}

// 异步加载页码获取
function ajax_page(parent_dom, _this) {
    var page = $(_this).hasClass('reload') ? parseInt($(parent_dom + ' .page').val()) : 1;
    $(_this).removeClass('reload');
    if (($(_this).hasClass('up') || $(_this).hasClass('next') || $(_this).hasClass('jump'))) {
        page = parseInt($(parent_dom + ' .page').val());
        var totalPages = parseInt($(parent_dom + ' .page').attr('totalPages'));
        if ($(_this).hasClass('up')) {
            page--;
        } else if ($(_this).hasClass('next')) {
            page++;
        }
        if (page <= 0) {
            page = 1;
        } else if (page > totalPages) {
            page = totalPages;
        }
    }

    return page;
}

// 异步提交表单与初始化表单验证，注，异步加载的界面需再次调用
function _Valid() {
    $('.Validform').Validform({
        ajaxPost: true,
        tiptype: function (msg, o, cssctl) {
            show_tip(msg);
        },
        ignoreHidden: true,
        postonce: true,
        tipSweep: true,
        callback: function (r) {
            show_tip(r.msg, r.error, r.url);
        }
    });

    $('.require_input').each(function (x, y) {
        if ($(y).prev('h4').length == 1) {
            $(y).attr('nullmsg', ($(y).prev('h4').text().replace('�?', '')) + '不能为空');
            //$(y).attr('errormsg', '请输入正确的' + ($(y).prev('h4').text().replace('�?', '')));
        }
    })
}

// 异步上传
function ajax_file_upload(dom) {
    //解决chrome浏览器上传同一文件不能触发change事件的问题�?
    var nf = dom.cloneNode(true);
    nf.value = ''; // 设计新控件value为空
    dom.parentNode.replaceChild(nf, dom);

    var mark = arguments[1] != undefined ? arguments[1] : null;
    if (typeof(ajaxFileUploadStart) == 'function') {
        ajaxFileUploadStart(dom, mark);
    }
    $.ajaxFileUpload({
        url: $(dom).attr('url'),
        data: {'path': $(dom).attr('path'), 'crop': $(dom).attr('crop'), 'compress': $(dom).attr('compress')},
        secureuri: false,
        fileElementId: $(dom),
        dataType: 'json',
        success: function (data) {
            if (data.error == 0) {
                if (typeof(ajaxFileUploadSuccessdExcel) == 'function' && mark == 'batch_import') {
                    ajaxFileUploadSuccessdExcel(data, mark);
                } else if (typeof(ajaxFileUploadSuccessd) == 'function') {
                    ajaxFileUploadSuccessd(data, mark);
                }
            } else {
                if (typeof(ajaxFileUploadFail) == 'function') {
                    ajaxFileUploadFail(data, mark);
                }
                show_tip(data.msg, data.error, data.url);
            }
        }
    })
    return false;
}