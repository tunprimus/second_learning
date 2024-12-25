import {Login} from './js/login.js';

// Create a variable for the login form
const form = document.querySelectorAll('#login_form')[0];

// If the form exists, run the class
if (form) {
	// Setup the fields we want to validate, we only have two but you can add others
	const fields = ['username', 'password'];
	// Run the class
	const validator = new Login(form, fields);
}
