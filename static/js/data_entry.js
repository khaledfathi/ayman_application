//varibale needed
	var pic_file = document.getElementById("pic_file"),
	pic_url = document.getElementById("pic_url"),
	radio_button = document.getElementsByName("pic"),
	i;
	

//get the current value of radio button in picture section 
function check_radio_selected(){
	for (i in radio_button){
		if (radio_button[i].checked){
			var res= radio_button[i].value
		};
	};
	if (res == "pic"){
		pic_file.removeAttribute("hidden");
		pic_url.setAttribute("hidden","");
			
	}else if (res == "link"){
		pic_url.removeAttribute("hidden");
		pic_file.setAttribute("hidden","");
	};
};

//action on change radio button in picture section
radio_button[0].onclick = function(){
	check_radio_selected();
};
radio_button[1].onclick = function(){
	check_radio_selected();
};

/*#######################################################*/

//variable needed
var cities = document.getElementById("cities"),
	label_other_city = document.getElementById("label_other_city"),
	othe_city = document.getElementById("other_city");

//add field for another city wich is not in cities list
cities.onchange = function (){
	if (cities.value=="--اخرى--"){
		label_other_city.removeAttribute("hidden");
		othe_city.removeAttribute("hidden");
	}else{
		label_other_city.setAttribute("hidden","");
		othe_city.setAttribute("hidden","");
	};
	
};
/*#######################################################*/

//variable needed
var loading_image = document.getElementById("loading_image"),
	save_button=document.getElementById("save_button"),
	clear_button = document.getElementById("clear_button");

//show loading image while page loading after press on save_button
save_button.onfocus = function (){
	loading_image.removeAttribute("hidden")
};
save_button.onblur = function (){
	loading_image.setAttribute("hidden","")
};

//show loading image while page loading after press on clear_button
clear_button.onfocus = function (){
	loading_image.removeAttribute("hidden")
};
clear_button.onblur = function (){
	loading_image.setAttribute("hidden","")
};

/*#######################################################*/
//variable needed
input_tags=document.getElementsByTagName("input");

//clear all inputs in form 
clear_button.onclick = function (){
	input_tags[1].value="";	
	input_tags[2].value="";	
	input_tags[3].value="";	
	input_tags[5].value="";	
	input_tags[6].value="";	
	input_tags[10].value="";	
	input_tags[11].value="";	
	input_tags[12].value="";	
	input_tags[13].value="";	
	input_tags[14].value="";	
	loading_image.setAttribute("hidden","")
}

/*#######################################################*/
//varibale needed
var product_image = document.getElementById("product_image")
//show pic in form , and convert link to html image tage with this link
pic_url.onkeyup = function (){
	product_image.setAttribute("src",pic_url.value);
}
