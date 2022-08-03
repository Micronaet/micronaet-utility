mainMenu = document.getElementsByClassName('oe_application_menu_placeholder');

aLi = document.createElement('li');
anA = document.createElement('a');
anA.setAttribute('id', 'toggle_sidebar_btn');
anI = document.createElement('i');
anI.setAttribute('class', 'fa fa-bars');
anA.appendChild(anI);
aLi.appendChild(anA);

anA.onclick = function() {
	sideBar = document.getElementsByClassName("o_sub_menu")[0];
	if (!sideBar.classList.contains('hide')){
		sideBar.classList.add('hide');
	}else{
		sideBar.classList.remove('hide');
	}
};

window.onload=function(){	
	mainMenu = mainMenu[0];
	mainMenu.insertBefore(aLi, mainMenu.firstChild);
}