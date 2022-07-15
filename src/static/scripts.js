function clipBoard() {
    var copyText = document.getElementById('linker1');
    copyText.select();
    navigator.clipboard.writeText(copyText.value);
}