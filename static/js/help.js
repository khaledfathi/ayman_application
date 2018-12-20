/*********GENERAL RULES *********/


/*******************************/

//variable needed 
var server_config = document.getElementById('server_config'),
	radio_config = document.getElementsByName("radio_config");

//action on click on radio button to select server config
radio_config[0].onclick = function (){
	if (radio_config[0].checked){
		server_config.setAttribute("hidden","")
	};
};
radio_config[1].onclick = function (){
	if (radio_config[1].checked){
		server_config.removeAttribute("hidden")
	};
};

/*********************/
//set the request action in server by change value in an input in form 
//varneeded 
var export_sql = document.getElementById("export_sql"),
	export_html= document.getElementById("export_html"),
	action_type= document.getElementById("action_type"),
	execute = document.getElementById("execute"),
	destroy=document.getElementById("destroy");

export_sql.onclick = function (){
	action_type.value="EXPORT_SQL";
};
export_html.onclick = function (){
	action_type.value="EXPORT_HTML";
};
execute.onclick = function (){
	action_type.value="EXECUTE";
};
destroy.onclick = function (){
	action_type.value="DESTROY";
};