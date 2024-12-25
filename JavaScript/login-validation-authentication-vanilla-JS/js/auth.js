//@ts-check
'use strict';

class Auth {
	/**
	 * Initialises the Auth class by hiding the body and validating the user's authentication status.
	 * If the user is not authenticated, they are redirected to the homepage.
	 */
	constructor() {
		document.querySelector('body').style.display = 'none';
		const auth = localStorage.getItem('auth');
		this.validateAuth(auth);
	}

	/**
	 * Validates the user's authentication status.
	 * If the user is not authenticated, redirects them to the homepage.
	 * Otherwise, displays the content of the page.
	 * @param {string} auth - The authentication status retrieved from local storage.
	 */
	validateAuth(auth) {
		if (auth != 1) {
			window.location.replace('/');
		} else {
			document.querySelector('body').style.display = 'block';
		}
	}

	/**
	 * Logs the user out by removing the authentication status from local storage
	 * and redirects them to the homepage.
	 */
	logOut() {
		localStorage.removeItem('auth');
		window.location.replace('/');
	}
}
