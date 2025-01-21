

//changes text inside of mini-screen 
function changeSize(increase)
{
  let screen = document.getElementById("mini-screen-text");
  let initial_val = document.getElementById("mini-screen-text").innerHTML;
  let sizes = ["SMALL", "MEDIUM", "LARGE","X-LARGE"]
  let index = sizes.indexOf(initial_val);
  if(increase)
  {
    if(index == 3)
    {
      screen.innerHTML = sizes[0]
    }
    else
    {
      screen.innerHTML = sizes[(index + 1)]
    }
  }
  else //decrease
  {
    if(index == 0)
      {
        screen.innerHTML = sizes[3]
      }
      else
      {
        screen.innerHTML = sizes[(index - 1)]
      }
  }
}

//resets home page (removes image from html element, clears input ,and disables buttons)
function handleClear()
{
  console.log('inside handleclear');
    
    //clear input
    document.getElementById("img-upload").value = null;

    //disable buttons
    document.getElementById("set-button").disabled = true;
    document.getElementById("cancel-button").disabled = true;

    //remove image
    document.getElementById('selected-image').src = null;
}

//enables buttons and sets image to html element
function handleImageSelection()
{
document.getElementById("img-upload").onchange = function() {

    try{
    var image_name = String(document.getElementById("img-upload").value);
    
    if(image_name.length > 0) //image exists
    {
        //set image to element
        document.getElementById('selected-image').src = window.URL.createObjectURL(this.files[0]);

        //enable buttons
        document.getElementById("set-button").disabled = false;
        document.getElementById("cancel-button").disabled = false;

    }
    }
    catch (e)
    {
        console.log('caught error: ' + e)
    }
};
}


//called upon click of 'SET' button and sends data to back-end
function handleConvert()
{
  const imageEndpoint = 'http://127.0.0.1:8000/data/'; //might need to change this
  let formData = new FormData();
  let pic_input = (document.getElementById("img-upload")).files; 
  if( pic_input != null && pic_input?.item(0))
  {
    let image = pic_input[0];
    formData.append('image_file',image);

    let size = document.getElementById("mini-screen-text").innerHTML;
    formData.append("size",size);
   
    let newImage = fetch(imageEndpoint,{
      method: 'POST',
      body: formData
     });

     setTimeout(() => {
      window.location.href = 'http://127.0.0.1:8000/result/';
    }, 2000);
     
  }
}