//@ts-check
'use strict';

const auth = new Auth();

document.querySelector('.logout').addEventListener('click', function (evt) {
	auth.logOut();
});
