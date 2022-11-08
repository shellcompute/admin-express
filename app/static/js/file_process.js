layui.use(['form', 'layedit', 'element'], function () {
    let form = layui.form,
        layer = layui.layer,
        $ = layui.$,
        element = layui.element

    //自定义验证规则
    form.verify({
        filename2: function (value) {
            let file_name = value || ''
            if (file_name.length === 0) {
                return '文件名不能为空！';
            }
            let file_type = value.split('.')[1] || ''
            if (file_type !== 'xlsx') {
                return '文件类型错误！';
            }
        },
        optype: function (value) {
            if (value === '') {
                return '处理类型不能空！';
            }
        },
    });

    //监听指定开关
    form.on('switch(autodel)', function (data) {
        if (this.checked) {
            layer.msg('注意！您已开启了自动删除，处理完后文档将自动删除！', {
                offset: '6px'
            });
        }
    });

    // $('#mybutton').on('click', function () {
    //
    // },

    //监听提交
    form.on('submit(myform)', function (data) {
        // layer.alert(JSON.stringify(data.field), {
        //     title: '提交信息'
        // })
        console.log('event submit start')

        $.ajax({
            url: '/sysbook/fileprocess',
            method: 'post',
            data: data.field,
            dataType: 'JSON',
            success: function (res) {
                if (res.data === 'success') {
                    console.log('success return')
                    layer.alert('处理成功！', {
                        title: '数据文件自动处理'
                    })
                } else {
                    layer.alert('处理完成！' + res.data, {
                        title: '数据文件自动处理'
                    })
                }
                console.log('href=='+res.next)
                location.href = res.next || '/sysbook/'
                // return false;
            },
            error: function (res) {
                layer.alert('处理失败！' + res.data, {
                    title: '数据文件自动处理'
                })
                // return false;
            }
        });

    }),

//表单赋值
    $('#LAY-component-form-setval').on('click', function () {
        form.val('example', {
            "username": "贤心" // "name": "value"
            , "password": "123456"
            , "interest": 1
            , "like[write]": true //复选框选中状态
            , "close": true //开关状态
            , "sex": "女"
            , "desc": "我爱 layui"
        });
    });

//表单取值
    $('#LAY-component-form-getval').on('click', function () {
        var data = form.val('example');
        alert(JSON.stringify(data));
    });

})
;