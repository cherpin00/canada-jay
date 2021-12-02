//document.getElementById("button-name").addEventListener("click", ()=>{eel.get_random_name()}, false);
//document.getElementById("button-number").addEventListener("click", ()=>{eel.get_random_number()}, false);
//document.getElementById("button-date").addEventListener("click", ()=>{eel.get_date()}, false);
//document.getElementById("button-ip").addEventListener("click", ()=>{eel.get_ip()}, false);

document.getElementById("button").addEventListener("click", ()=>{eel.pythonFunction()}, false);

let count = 0;

eel.expose(prompt_alerts);
function prompt_alerts(description) {
  alert(description);
}

eel.expose(inner_element_file_change);
function inner_element_file_change(path) {
  const btn = document.getElementById("filename");
  btn.innerHTML = path;
}

eel.expose(add_filename_change);
function add_filename_change(path) {
  const para = document.createElement("p");
  count ++;
  para.setAttribute("id", "file" + count);
  para.setAttribute("class", "file");
  const myArray = path.split("\\");
  const node = document.createTextNode(myArray.at(-1) );
  //const node = document.createTextNode(path);
  para.appendChild(node);
  const element = document.getElementById("id-files");
  element.appendChild(para);
  //class-for-filenames
  //const btn = document.getElementById("filename");
  //btn.innerHTML = path;
}

eel.expose(getPathToFile);
function getPathToFile() {
    eel.pythonFunction()(call_back);

    //eel.pythonFunction(){
    //  const btn = document.getElementById("filename");
    //  btn.innerHTML = path;
    //}
  };

  function call_back(output){
    document.getElementById("filename").value = output 
  }
