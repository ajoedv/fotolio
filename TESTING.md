# Testing

## Contents
1. [Introduction](#introduction)
2. [Testing Strategy](#testing-strategy)
3. [Manual Testing](#manual-testing)
4. [Automated Testing](#automated-testing)
5. [Stripe Testing](#stripe-testing)
6. [Validator Testing](#validator-testing)
7. [Accessibility, Responsiveness and Cross-Browser Testing](#accessibility-responsiveness-and-cross-browser-testing)
8. [Lighthouse Testing](#lighthouse-testing)
9. [Bugs Found and Fixes](#bugs-found-and-fixes)
10. [Final Testing Summary](#final-testing-summary)

---

## Introduction

This document outlines the testing carried out for the Fotolio e-commerce project.

Testing was carried out throughout development and again on the deployed Heroku version of the application to confirm that the main user flows, validation rules, payment process, and key error handling all work as expected.

The testing process included:
- Manual testing of key user journeys and edge cases
- Automated testing across relevant Django applications
- Stripe payment testing
- Code and markup validation
- Accessibility, responsiveness, and cross-browser checks
- Lighthouse performance and SEO auditing

---

## Testing Strategy

A combination of manual and automated testing was used in order to evaluate both backend functionality and real user interaction.

### Manual testing was used to verify:
- Navigation and page flow
- Form behaviour with valid and invalid input
- Authentication behaviour
- Cart and checkout flow
- Order history and profile functionality
- Error handling and redirects
- Real user experience on the live deployed site

### Automated testing was used to verify:
- Models
- Forms
- Views
- URLs
- Admin configuration
- Signals
- Context processors
- Utility functions
- Project-level routes and handlers
- Business logic across the main Django applications

### Test environment

Testing was carried out on:
- Local development environment
- Deployed Heroku application

---

## Manual Testing

Manual testing was used to verify the main user journeys of the Fotolio application and to confirm that the live deployed site behaved as expected during normal use.

The focus of manual testing was placed on:
- Navigation and page flow
- Product browsing and product detail views
- Search functionality
- Authentication and access control
- Profile and order history features
- Cart functionality
- Checkout and payment flow
- Contact and newsletter forms
- Error handling

The following manual tests were carried out on the deployed Heroku application.


### Manual Testing Table

| Feature / Area | Test Case | Steps | Expected Result | Actual Result | Pass / Fail |
|---|---|---|---|---|---|
| Home page | Home page loads correctly | Open the homepage | The homepage loads without errors and displays the main content correctly | The homepage loaded correctly and displayed the expected content | Pass |
| Navigation | Main navigation links work correctly | Click the main navigation links from the navbar | Each link takes the user to the correct page | All tested navigation links worked correctly | Pass |
| Products | Product listing page loads correctly | Open the gallery/products page | Products are displayed correctly without errors | The product listing page loaded correctly and displayed the products as expected | Pass |
| Product detail | Product detail page opens correctly | Click on a product from the product listing page | The selected product detail page opens and displays the correct information | The product detail page loaded correctly with the expected product information | Pass |
| Invalid product URL | Non-existent product returns a 404 page | Enter an invalid product URL in the browser | A custom 404 page is displayed | The custom 404 page was displayed correctly | Pass |
| Search | Search returns matching results | Search for an existing keyword or product | Relevant matching products are displayed | Matching search results were displayed correctly | Pass |
| Search | Search with no results displays the correct feedback | Search for a non-existent keyword or product | A no-results message is displayed | The no-results feedback was displayed correctly | Pass |
| Sign up | Valid sign up form submission works correctly | Submit the sign up form with valid information | The account is created successfully and the user is redirected appropriately | The sign up process worked correctly | Pass |
| Sign up | Invalid sign up form submission shows validation errors | Submit the sign up form with invalid or incomplete information | Validation errors are displayed and the account is not created | Validation errors were displayed correctly | Pass |
| Sign in | Valid sign in works correctly | Submit correct login credentials | The user signs in successfully and is redirected appropriately | The sign in process worked correctly | Pass |
| Sign in | Invalid sign in shows the correct error | Submit incorrect login credentials | An error message is displayed and login is blocked | The expected error was shown and login was blocked | Pass |
| Protected pages | Guest users are redirected when trying to access protected pages | Open a protected page while logged out | The user is redirected to the sign in page | The redirect worked correctly | Pass |
| Profile | Profile page loads correctly for authenticated users | Sign in and open the profile page | The profile page loads correctly with the user's information | The profile page loaded correctly | Pass |
| Orders | Order history is visible to the correct user | Sign in and open the order history page | The logged-in user can view their own order history | The order history was displayed correctly | Pass |
| Cart | Product can be added to the cart | Add a product to the cart from the product or gallery page | The product is added successfully and the cart updates correctly | The product was added to the cart correctly | Pass |
| Cart | Cart quantity can be updated | Change the quantity of an item in the cart | The quantity updates correctly and the cart reflects the change | The quantity was updated correctly | Pass |
| Cart | Product can be removed from the cart | Remove an item from the cart | The product is removed successfully from the cart | The product was removed correctly | Pass |
| Cart | Empty cart state is handled correctly | Open the cart when there are no items or remove all items | An empty cart message is displayed | The empty cart state was displayed correctly | Pass |
| Checkout | Checkout page loads correctly | Proceed to checkout with items in the cart | The checkout page opens correctly and displays the checkout content | The checkout page loaded correctly | Pass |
| Checkout | Checkout is blocked when the cart is empty | Attempt to access checkout without items in the cart | The user receives feedback and cannot continue the normal checkout flow | The correct feedback was displayed and the flow was blocked as expected | Pass |
| Checkout | Checkout flow reaches payment successfully | Add items to the cart and proceed through checkout to the payment stage | The user reaches the payment stage without errors | The checkout flow reached the payment stage correctly | Pass |
| Order access | Invalid order access is blocked correctly | Attempt to access an invalid or unauthorised order | The user cannot access the order and appropriate handling is shown | The invalid order access was blocked correctly | Pass |
| Contact form | Valid contact form submission works correctly | Submit the contact form with valid information | The form is submitted successfully and the user receives the correct feedback | The contact form submitted correctly | Pass |
| Contact form | Invalid contact form submission shows validation errors | Submit the contact form with invalid or incomplete information | Validation errors are displayed and submission is blocked | Validation errors were displayed correctly | Pass |
| Newsletter | Valid newsletter signup works correctly | Submit a valid email address through the newsletter form | The email is added successfully and the correct feedback is shown | The newsletter signup worked correctly | Pass |
| Newsletter | Duplicate newsletter signup is handled correctly | Submit an email address that is already subscribed | The duplicate is handled gracefully and the correct feedback is shown without a server error | The duplicate signup was handled correctly without errors | Pass |
| Logout | Logout works correctly | Sign in and then log out | The user is logged out successfully and redirected appropriately | The logout process worked correctly | Pass |


---

## Automated Testing

Automated testing was implemented across the project once the core technical fixes were completed. The purpose of the automated testing phase was to verify the stability of the application's backend behaviour and confirm that key Django components worked correctly in isolation.

Automated testing was written using Django's built-in test framework and was organised app by app. Tests were split into separate files where appropriate in order to keep the test structure clear and maintainable.

The automated test suite covers:
- Models
- Forms
- Views
- URLs
- Admin configuration
- Signals
- Context processors
- Utility functions
- Project-level routes and handlers

A full project test run was completed with the following result:

- **178 automated tests passed successfully**

The full test suite was run using:

```bash
python manage.py test
```

The final result returned:

- **Found 178 test(s)**
- **Ran 178 tests**
- **OK**

### Applications and areas covered

#### Newsletter

Automated tests were added for the newsletter app covering:

- model behaviour
- form validation
- view behaviour
- URL routing
- admin configuration

#### Home

Automated tests were added for the home app covering:

- model behaviour
- form validation
- view behaviour
- URL routing
- admin configuration

#### Cart

Automated tests were added for the cart app covering:

- model behaviour
- view behaviour
- URL routing
- admin configuration
- cart context processor
- cart utility functions for item retrieval and total calculation

#### Profiles

Automated tests were added for the profiles app covering:

- model behaviour
- form validation
- view behaviour
- URL routing
- admin configuration
- user profile signal behaviour

#### Products

Automated tests were added for the products app covering:

- category, product, and review model behaviour
- review form validation
- product and review view behaviour
- URL routing
- admin configuration

#### Orders

Automated tests were added for the orders app covering:

- order and order line item model behaviour
- order list and order detail view behaviour
- URL routing

#### Project-level testing

Additional automated tests were added at project level to cover:

- `robots.txt`
- `sitemap.xml`
- custom 404 page handling
- custom 500 page handling

### What the automated tests verified

The automated tests verified key areas including:

- automatic creation and protection of related model data
- form validation for valid and invalid input
- access control for authenticated and unauthenticated users
- redirects and permissions for protected views
- correct rendering of templates in major views
- correct URL resolution for application routes
- correct admin registration and admin configuration
- correct signal behaviour for profile creation
- correct cart summary and cart total calculations
- correct project-level route behaviour for sitemap and error pages

### Bugs identified during automated testing

Automated testing helped identify real issues during development.

One important issue discovered during testing was within the profiles app:

- the delete profile confirmation page initially failed because `profiles/delete_confirm.html` was missing
- this caused a `TemplateDoesNotExist` error during view testing
- the issue was fixed by creating the missing template
- the tests were then rerun successfully

Automated testing also highlighted an issue in the sitemap implementation:

- the sitemap queryset returned an unordered product queryset
- this produced an `UnorderedObjectListWarning`
- the issue was fixed by updating the sitemap queryset to use explicit ordering with `order_by("pk")`

### Automated testing conclusion

The automated testing process provided strong confirmation that the main Django logic of the project behaves correctly. The final test run passed successfully with **178 passing tests**, giving confidence that the application is stable across its core backend functionality.

---
## Stripe Testing

Stripe payment functionality was tested manually on the deployed Heroku version of the application using Stripe test mode.

The following Stripe-related payment scenarios were tested to verify successful payments, failed payments, payment validation, checkout navigation, empty cart protection, and correct order creation behaviour in the live application.

### 1. Successful Stripe payment

A product was added to the cart and the checkout flow was completed using a valid Stripe test card.

**Expected result:**  
The payment should complete successfully and the user should be redirected to the payment confirmation page.

**Actual result:**  
Passed. The payment was completed successfully and the user was redirected to the confirmation page.

![Successful Stripe payment](assets/testing/stripe/stripe-success-page.png)

---

### 2. Success page appears after successful payment

After a successful Stripe payment, the resulting page was reviewed.

**Expected result:**  
A clear success or payment confirmation page should be displayed after payment completion.

**Actual result:**  
Passed. The success page was displayed correctly after the payment was completed.

![Stripe success page after payment](assets/testing/stripe/stripe-success-page.png)

---

### 3. Successful order is added to My Orders

After a successful payment, the user account order list was reviewed.

**Expected result:**  
A newly created successful order should appear in **My Orders**.

**Actual result:**  
Passed. The successful order was added to **My Orders** and was visible in the order list.

![Successful order added to My Orders](assets/testing/stripe/stripe-my-orders.png)

---

### 4. Opening the order from My Orders shows the order detail page

The newly created order was opened from the **My Orders** page.

**Expected result:**  
Selecting the created order should open the corresponding order detail page.

**Actual result:**  
Passed. Opening the order from **My Orders** displayed the correct order detail page.

![Order opened from My Orders](assets/testing/stripe/stripe-order-detail.png)

---

### 5. Invalid payment form validation

Invalid card details were entered into the Stripe payment form.

**Expected result:**  
The form should display validation errors and prevent the payment from being submitted successfully.

**Actual result:**  
Passed. Stripe displayed validation errors for invalid payment details and the payment could not be completed.

![Invalid Stripe payment form validation](assets/testing/stripe/stripe-invalid-payment-form.png)

---

### 6. Declined Stripe test card

A Stripe test card designed to simulate a declined payment was used.

**Expected result:**  
The payment should be declined, the user should remain on the payment page, and no successful payment should be completed.

**Actual result:**  
Passed. Stripe returned a declined payment message stating that the card had insufficient funds, and the user was not redirected to the success page.


---

### 7. Return from payment page to checkout

From the payment page, the **Back to checkout** option was used.

**Expected result:**  
The user should be returned to the checkout page without errors and should still be able to continue the checkout process.

**Actual result:**  
Passed. The user was returned to the checkout page successfully and no errors occurred.

![Return from payment page to checkout](assets/testing/stripe/stripe-back-to-checkout.png)

---

### 8. Empty cart warning appears when checkout is attempted

The cart was emptied and checkout was attempted.

**Expected result:**  
The system should display a warning message indicating that checkout cannot proceed with an empty cart.

**Actual result:**  
Passed. A warning message was displayed stating: **"Your cart is empty. Add an item before checkout."**

![Empty cart warning when checkout is attempted](assets/testing/stripe/stripe-empty-cart-warning.png)

---

### 9. Proceed to checkout is blocked when cart is empty

After emptying the cart, the **Proceed to checkout** button was clicked.

**Expected result:**  
The user should not be allowed to continue to checkout or payment with an empty cart.

**Actual result:**  
Passed. The user remained on the cart page and could not continue to checkout while the empty cart warning remained visible.

![Proceed to checkout blocked when cart is empty](assets/testing/stripe/stripe-empty-cart-warning.png)

---

### 10. Order details are correct after successful payment

The order detail page for a successful payment was reviewed.

**Expected result:**  
The order detail page should display the correct order number, payment confirmation, customer details, product details, quantity, VAT, and total price.

**Actual result:**  
Passed. The order detail page showed the correct order number, payment confirmation, customer information, purchased item, quantity, VAT, and total price.

![Correct order details after successful payment](assets/testing/stripe/stripe-order-detail.png)

---

### 11. Successful order is visible in My Orders with correct summary information

The **My Orders** page was reviewed after successful payment.

**Expected result:**  
The successful order should appear with the correct order number, date, total price, and a working **View** option.

**Actual result:**  
Passed. The successful order appeared correctly in **My Orders** with the expected summary information and a working **View** button.

![Successful order summary in My Orders](assets/testing/stripe/stripe-my-orders.png)

---

### 12. Failed payment does not create a new successful order

After a failed payment attempt, the **My Orders** page was checked again.

**Expected result:**  
A failed payment should not create a new successful order record.

**Actual result:**  
Passed. No new successful order was created after the failed payment attempt. The latest successful order remained unchanged in **My Orders**.

![Failed payment does not create a new successful order](assets/testing/stripe/stripe-no-new-order-after-failed-payment.png)

---

### Stripe Testing Summary

Stripe testing confirmed that the payment flow works correctly for successful payments, invalid payment input, declined payments, checkout navigation, empty cart protection, and order creation. The tests also confirmed that successful payments create visible orders in the user account, while failed payments do not create new successful order records.