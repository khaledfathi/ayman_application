//varibale to get elements element 

var main_search = document.getElementById("main_search"),
	pattern_1 = document.getElementById("pattern_1"),
	pattern_2= document.getElementById("pattern_2"),
	pattern_3= document.getElementById("pattern_3"),
	search_pattern = document.getElementById("search_pattern"),
	order = document.getElementById("order"),
	az_za = document.getElementById("az_za"),
	search_field=document.getElementById("search_field"),
	from = document.getElementById("from"),
	to =document.getElementById("to"),
	label_from = document.getElementById("label_from"),
	label_to =document.getElementById("label_to");

//###############################################
//determination search patterns showing to user depend on main_search selections
function event_handler_main_search (){
	//function to remove hidden and selected attributes from all options in main_search "select elements" and some other elements changes
	function defualt_attribute_main_search(){
		pattern_1.setAttribute("hidden","");
		pattern_2.setAttribute("hidden","");
		pattern_3.setAttribute("hidden","");
		search_field.setAttribute("type","text");
		search_field.removeAttribute("hidden");
		from.value=null;
		to.value=null;
		from.setAttribute("hidden","");
		to.setAttribute("hidden","");
		label_from.setAttribute("hidden","");
		label_to.setAttribute("hidden","");
	};
	if (main_search.value == "ID" ) {
		defualt_attribute_main_search();
		pattern_1.removeAttribute("hidden");
		if (pattern_1.value=="ما بين"){
			if (pattern_1.value == "ما بين"){
				search_field.setAttribute("hidden","");
				from.removeAttribute("hidden");
				to.removeAttribute("hidden");
				label_from.removeAttribute("hidden");
				label_to.removeAttribute("hidden");
				from.setAttribute("type","text");
				to.setAttribute("type","text");
			}else{
				search_field.removeAttribute("hidden");
				from.setAttribute("hidden","");
				to.setAttribute("hidden","");
				label_from.setAttribute("hidden","");
				label_to.setAttribute("hidden","");
			};	
		};
	}else if ( main_search.value == "الاسم" || main_search.value == "العنوان" || main_search.value=="التليفون"|| main_search.value == "المحافظة" || main_search.value == "نوع المنتج" || main_search.value == "البريد الالكترونى" || main_search.value == "الملاحظات"){
		defualt_attribute_main_search();
		pattern_2.removeAttribute("hidden");
	}else if (main_search.value=="تاريخ الطلب" || main_search.value=="تاريخ التسليم"){
		defualt_attribute_main_search();
		pattern_3.removeAttribute("hidden");
		if (pattern_3.value == "الفترة من/الى"){
			search_field.setAttribute("hidden","");
			from.removeAttribute("hidden");
			to.removeAttribute("hidden");
			label_from.removeAttribute("hidden");
			label_to.removeAttribute("hidden");
			from.setAttribute("type","date");
			to.setAttribute("type","date");
		}else{
			search_field.removeAttribute("hidden");
			search_field.setAttribute("type","date");
			from.setAttribute("hidden","");
			to.setAttribute("hidden","");
			label_from.setAttribute("hidden","");
			label_to.setAttribute("hidden","");
		};
	};
};
main_search.onchange = function (){		
	event_handler_main_search ()
	var pattern=document.getElementById("pattern");
	if ( main_search.value == "الاسم" || main_search.value == "العنوان" || main_search.value=="التليفون"|| main_search.value == "المحافظة" || main_search.value == "نوع المنتج" || main_search.value == "البريد الالكترونى" || main_search.value == "الملاحظات"){
		pattern.value="pattern_2"
	}else if (main_search.value == "تاريخ الطلب" || main_search.value == "تاريخ التسليم"){
		pattern.value="pattern_3"
	}else if (main_search.value == "ID"){
		pattern.value="pattern_1"
	};		
};

//###############################################
//determination type of search field input depend on main_search selections and pattern selections (for date)
function event_handler_pattern_date(){
	if (main_search.value == "تاريخ الطلب" || main_search.value == "تاريخ التسليم"){
		if (pattern_3.value == "الفترة من/الى"){
			search_field.setAttribute("hidden","");
			from.removeAttribute("hidden");
			to.removeAttribute("hidden");
			label_from.removeAttribute("hidden");
			label_to.removeAttribute("hidden");
			from.setAttribute("type","date");
			to.setAttribute("type","date");
		}else{
			search_field.removeAttribute("hidden");
			from.setAttribute("hidden","");
			to.setAttribute("hidden","");
			label_from.setAttribute("hidden","");
			label_to.setAttribute("hidden","");
		};
	};
};
pattern_3.onchange = function (){
	event_handler_pattern_date();
};

//determination type of search field input depend on main_search selections and pattern selections (for id)
function event_handler_pattern_id(){
	if (main_search.value == "ID"){
		if (pattern_1.value == "ما بين"){
			search_field.setAttribute("hidden","");
			from.removeAttribute("hidden");
			to.removeAttribute("hidden");
			label_from.removeAttribute("hidden");
			label_to.removeAttribute("hidden");
			from.setAttribute("type","text");
			to.setAttribute("type","text");
		}else{
			search_field.removeAttribute("hidden");
			from.setAttribute("hidden","");
			to.setAttribute("hidden","");
			label_from.setAttribute("hidden","");
			label_to.setAttribute("hidden","");
		};
	};
};

pattern_1.onchange = function (){
	event_handler_pattern_id();
};
pattern_1.onclick = function (){
	event_handler_pattern_id();
};


//#############################################
// delete or updte row in serch result (values handled by server side)

var update_delete_status = document.getElementsByName("update_delete_status"),
	update_delete_id = document.getElementsByName("update_delete_id"),
	i;

//multi rows delete 
var del_check= document.getElementsByName("del_check"),
	del_button_submit = document.getElementById("del_button_submit");

del_button_submit.onmouseover = function (){
	var items="";
	for (i=0; i < del_check.length ;i+=1){
		if (del_check[i].checked) {
			items+=upadte_delete_id=del_check[i].value+","
		};	
	};
	console.log(items)
	update_delete_id[0].value=items
	update_delete_status[0].value="DELETE"
};