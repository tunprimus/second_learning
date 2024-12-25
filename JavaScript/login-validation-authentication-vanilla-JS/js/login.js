//@ts-check
'use strict';

const MIN_PASSWORD_LENGTH = 12;

class Login {
	/**
	 * Instantiates the Login class.
	 * @param {HTMLFormElement} form - The form to validate.
	 * @param {string[]} fields - The fields to validate.
	 */
	constructor(form, fields) {
		this.form = form;
		this.fields = fields;
		this.validateOnSubmit();
	}

	/**
	 * Sets up a `submit` event listener on the form.
	 * On form submission, the function will loop through the fields and check them against the `validateFields` method.
	 * If any of the fields do not validate, the submission is prevented and an error is incremented.
	 * If all fields validate, the submission is allowed and the `localStorage` item is set.
	 */
	validateOnSubmit() {
		// Setup calls to the "this" values of the class described in the constructor
		let self = this;

		// Add a `submit` event listener to the form
		this.form.addEventListener('submit', function (evt) {
			// Prevent the form from submitting
			evt.preventDefault();
			let error = 0;

			// Loop through the fields and check them against a function
			self.fields.forEach(function (field) {
				const input = document.querySelector(`#${field}`);
				if (self.validateFields(input) === false) {
					// If a field does not validate, auto-increment our error integer
					error++;
				}
			});
			// If everything validates, error will be 0 and can continue
			if (error === 0) {
				// Do login api here or in this case, just submit the form and set a localStorage item
				localStorage.setItem('auth', 1);
				this.form.submit();
			}
		});
	}

	/**
	 * Validate a field.
	 * @param {HTMLElement} field - The field to validate.
	 * @returns {boolean} True if the field is valid, false otherwise.
	 */
	validateFields(field) {
		// Remove any whitespace and check to see if the field is blank, if so return false
		if (field.value.trim() === '') {
			// Set the status based on the field, field label and if it is an error message
			this.setStatus(
				field,
				`${field.previousElementSibling.innerText} cannot be blank`,
				'error'
			);
			return false;
		} else {
			// If the field is not blank, check to see if it is password
			if (field.type === 'password') {
				// If it is password, check the length
				if (field.value.length < MIN_PASSWORD_LENGTH) {
					// Set the status based on the field, field label and if it is an error message
					this.setStatus(
						field,
						`${field.previousElementSibling.innerText} must be at least ${MIN_PASSWORD_LENGTH} characters`,
						'error'
					);
					return false;
				} else {
					// Set the status based on the field without text and return a success message
					this.setStatus(field, null, 'success');
					return true;
				}
			} else {
				// Set the status based on the field without text and return a success message
				this.setStatus(field, null, 'success');
				return true;
			}
		}
	}

	/**
	 * Set the status of the field.
	 * @param {HTMLElement} field - The field to update.
	 * @param {string} message - The error message to display if the status is error.
	 * @param {string} status - The status to apply to the field. Can be 'success' or 'error'.
	 */
	setStatus(field, message, status) {
		// Create variable to hold message
		const errorMessage = field.parentElement.querySelector('.error-message');

		// If success, remove messages and error classes
		if (status === 'success') {
			if (errorMessage) {
				errorMessage.innerText = '';
			}
			field.classList.remove('input-error');
		}
		// If error, add messages and error classes
		if (status === 'error') {
			errorMessage.innerText = message;
			field.classList.add('input-error');
		}
	}
}

// Create a variable for the login form
const form = document.querySelectorAll('#login_form')[0];

// If the form exists, run the class
if (form) {
	// Setup the fields we want to validate, we only have two but you can add others
	const fields = ['username', 'password'];
	// Run the class
	const validator = new Login(form, fields);
}
