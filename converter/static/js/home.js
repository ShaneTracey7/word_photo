function handleClear()
{
  console.log('inside handleclear');
    
    //clear input
    document.getElementById("img-upload").value = null;

    //hide buttons
    document.getElementById('convert-button').style.display = "none";
    document.getElementById('cancel-button').style.display = "none";

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

        //show buttons
        document.getElementById('convert-button').style.display = "block";
        document.getElementById('cancel-button').style.display = "block";
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
  
  const imageEndpoint = 'http://127.0.0.1:8000/image'; //might need to change this
  let formData = new FormData();
  let pic_input = (document.getElementById("img-upload")).files; //had to make some changes to OG
  if( pic_input != null && pic_input?.item(0))
  {
    let image = pic_input[0];
    formData.append('image_file',image);

    let newImage = fetch(imageEndpoint,{
      method: 'POST',
      body: formData
     });
  }
     
}


