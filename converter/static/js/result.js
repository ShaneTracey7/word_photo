function handleCopy()
{
    console.log('copy');
    var val = String(document.getElementById("result-value").innerText);
    navigator.clipboard.writeText(val);
}

function handleReset()
{
    console.log('reset');
    window.location.href = 'http://127.0.0.1:8000/home/';
}