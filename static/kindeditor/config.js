/**
 * Created by Administrator on 2018/5/17.
 */
KindEditor.ready(function(K) {
    K.create('textarea[name="content"]', {
        width : "600px",
        height : "500px",
        uploadJson: '/admin/uploads/kindeditor',
    });
});