document.getElementById("button").addEventListener("click", ()=>{eel.pythonFunction(file_count)}, false);
document.getElementById("button2").addEventListener("click", ()=>{eel.drive_addition(drive_count)}, false);
document.getElementById("button-header").addEventListener("click", ()=>{eel.split_function_call()}, false);

let file_count = 0;
let drive_count = 0;

eel.expose(prompt_alerts);
function prompt_alerts(description) {
  alert(description);
}

eel.expose(db);
function db() {
  eel.load_db();
}

eel.expose(inner_element_file_change);
function inner_element_file_change(path) {
  const btn = document.getElementById("filename");
  btn.innerHTML = path;
}

eel.expose(add_filename_change);
function add_filename_change(path) {
  console.log(path);
  const para = document.createElement("p");
  para.setAttribute("id", "file" + file_count);
  para.setAttribute("class", "file");
  const myArray = path.split("/");
  console.log(myArray);
  const node = document.createTextNode(myArray.at(-1) );
  para.appendChild(node);
  const element = document.getElementById("id-files");
  element.appendChild(para);

  const div = document.createElement("div");
  div.setAttribute("id", "div" + file_count);
  div.setAttribute("class", "inline-div");
  element.appendChild(div);
  file_count ++;
}

eel.expose(add_para);
function add_para(content, element_name) {
  const para = document.createElement("p");
  para.setAttribute("id", "drive" + drive_count);
  para.setAttribute("class", element_name);
  const node = document.createTextNode(content );
  para.appendChild(node);
  const element = document.getElementById(element_name);
  element.appendChild(para);

  const div = document.createElement("div");
  div.setAttribute("id", "div" + drive_count);
  div.setAttribute("class", "inline-div");
  element.appendChild(div);
  drive_count ++;
}

eel.expose(add_para_file);
function add_para_file(content, element_name) {
  const para = document.createElement("p");
  para.setAttribute("id", "file_saved" + drive_count);
  para.setAttribute("class", element_name);
  const node = document.createTextNode(content );
  para.appendChild(node);
  const element = document.getElementById(element_name);
  element.appendChild(para);

  const div = document.createElement("div");
  div.setAttribute("id", "div" + drive_count);
  div.setAttribute("class", "inline-div");
  element.appendChild(div);
  drive_count ++;
}

eel.expose(getPathToFile);
function getPathToFile() {
    eel.pythonFunction()(call_back);
  };

  function call_back(output){
    document.getElementById("filename").value = output 
  }
