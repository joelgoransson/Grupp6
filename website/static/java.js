function showgrupp() {
    document.getElementById("Students").style.display = null;
}
var t = [];
var i;
spaning();

function spaning() {
  
  var photo = document.getElementsByClassName("pic");
  for (i = 0; i < photo.length; i++) {
    photo[i].style.display = "none";  
  }
  t++
  if (t > photo.length) 
  {t = 1;}    
  
  photo[t-1].style.display = null;  
  setTimeout(spaning, 4000);
}
