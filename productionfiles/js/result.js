
//copy's char array to clipboard
function handleCopy()
{
    console.log('copy');
    var val = String(document.getElementById("t-container").innerText);
    navigator.clipboard.writeText(val);
}

//directs to home page
function handleReset()
{
    console.log('reset');
    window.location.href = 'https://shantrac.pythonanywhere.com/home/'; // local env testing: 'http://127.0.0.1:8000/home/'
}