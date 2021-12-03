document.getElementById("button").addEventListener("click", ()=>{eel.pythonFunction(file_count)}, false);
document.getElementById("button2").addEventListener("click", ()=>{eel.drive_addition(drive_count)}, false);
document.getElementById("button-header").addEventListener("click", ()=>{eel.split_function_call()}, false);

let file_count = 0;
let drive_count = 0;

eel.expose(prompt_alerts);
function prompt_alerts(description) {
  alert(description);
}

eel.expose(remove_to_split);
function remove_to_split(){
  const myNode = document.getElementById("id-files");
  myNode.innerHTML = '';
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
  para.setAttribute("id", file_count);
  para.setAttribute("class", "file");
  const myArray = path.split("/");
  const node = document.createTextNode(myArray.at(-1) );
  para.appendChild(node);
  const element = document.getElementById("id-files");
  element.appendChild(para);

  const div = document.createElement("div");
  div.setAttribute("id", file_count);
  div.setAttribute("class", "inline-div");
  element.appendChild(div);
  file_count ++;
}

eel.expose(add_content);
function add_content(content, element_name, parent_element_name, element_type, unique_id) {
  const para = document.createElement(element_type);
  para.setAttribute("id", unique_id);
  para.setAttribute("class", element_name);
  if(element_type == "p"){
    if(parent_element_name == "files_saved"){
      const myArray = content.split("/");
      node = document.createTextNode(myArray.at(-1) );
      para.onclick = function() { // Note this is a function
        eel.get_file_path(this.id);
        document.getElementById(this.id).remove();
      };
    }
    else{
      node = document.createTextNode(content);
    }
    para.appendChild(node);
  }
  const element = document.getElementById(parent_element_name);
  element.appendChild(para);
}


eel.expose(getPathToFile);
function getPathToFile() {
    eel.pythonFunction()(call_back);
  };

  function call_back(output){
    document.getElementById("filename").value = output 
  }
