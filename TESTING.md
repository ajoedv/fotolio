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
- Business logic
- Application behaviour within individual Django applications

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
