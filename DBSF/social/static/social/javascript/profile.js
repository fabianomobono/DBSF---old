
document.querySelector('.profile_pic').addEventListener('click', () => {
  document.querySelector(".upload_picture_div").style.display = 'block';
})


function closeElement(element) {
  element.parentElement.style.display = 'none';
}


var loadFile = function(event){
  document.querySelector(".profile_pic_in_popup").innerHTML = ''
  var files = event.target.files['0']
  var image = document.createElement("IMG")
  image.width = 200
  image.src = URL.createObjectURL(event.target.files['0']);
  document.querySelector(".profile_pic_in_popup").appendChild(image)

}
