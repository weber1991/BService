function checkidcard() {
    var idcard = document.getElementById("reg_idcard");
    if (idcard.value.length != 18)
    {
        alert("请输入正确的身份证号码");
        idcard.value = "";
    }
    else{
        return true;
    }
}