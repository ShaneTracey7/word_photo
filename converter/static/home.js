/*class Home {
    constructor(imageState) {
      this.imageState = false;
    }
    
    // Method
    calcArea() {
      return this.height * this.width;
    }
  }
  
  const square = new Rectangle(10, 10);
  
*/
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

function handleClear()
{
    //remove image
    document.getElementById('selected-image').src = null;

    //clear input
    document.getElementById("img-upload").value = null;

    //hide buttons
    document.getElementById('convert-button').style.display = "none";
    document.getElementById('cancel-button').style.display = "none";

}