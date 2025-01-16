//global variable
var size = 'small' //default

function changeSize(increase)
{
  console.log('inside function')
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

function handleClear()
{
  console.log('inside handleclear');
    
    //clear input
    document.getElementById("img-upload").value = null;

    //disable buttons
    document.getElementById("set-button").disabled = true;
    document.getElementById("cancel-button").disabled = true;

    //hide buttons
    //document.getElementById('convert-button').style.display = "none";
    //document.getElementById('cancel-button').style.display = "none";

    //remove image
    document.getElementById('selected-image').src = null;
}

function handleImageSelection()
{
//on change event listener for #file-select
document.getElementById("img-upload").onchange = function() {

    try{
    var image_name = String(document.getElementById("img-upload").value);
    
    if(image_name.length > 0)
    {
        //image exists
        document.getElementById('selected-image').src = window.URL.createObjectURL(this.files[0]);

        //enable buttons
        document.getElementById("set-button").disabled = false;
        document.getElementById("cancel-button").disabled = false;

        //document.getElementById('convert-button').style.display = "block";
        //document.getElementById('cancel-button').style.display = "block";
    }
    }
    catch (e)
    {
        console.log('caught error: ' + e)
    }
};
}

function handleConvert()
{
  console.log('inside handleConvert');
  const imageEndpoint = 'http://127.0.0.1:8000/data/'; //might need to change this
  let formData = new FormData();
  let pic_input = (document.getElementById("img-upload")).files; //had to make some changes to OG
  if( pic_input != null && pic_input?.item(0))
  {
    let image = pic_input[0];
    formData.append('image_file',image);

    let size = document.getElementById("mini-screen-text").innerHTML;

    formData.append("size",size);
    //ADD ADDITONAL FORM DATA HERE
    let newImage = fetch(imageEndpoint,{
      method: 'POST',
      body: formData
     });

     window.location.href = 'http://127.0.0.1:8000/result/';
  }
     
}

function test()
{
  return 'hello'
}
