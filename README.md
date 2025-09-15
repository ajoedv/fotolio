# Fotolio

## Overview
Fotolio is an e-commerce web application designed for selling printed photography.  
Users can browse collections, filter by category, view product details, add items to a cart, and complete purchases securely using Stripe.  
The platform is built with Django, PostgreSQL, and Bootstrap, following Agile methodology and UX best practices.  
The site is fully responsive and optimized for a smooth user shopping experience.

---

## Live Demo
🔗 [Click here to view the live app on Heroku](#)  
(Deployed link will be added after final deployment)

---

## Agile Methodology
This project follows Agile principles and uses GitHub Projects to plan and track progress.  
Work is organized into **Epics** and **User Stories**, prioritized using the **MoSCoW method** (Must/Should/Could/Won’t).  

---

## User Experience (UX)

### Strategy / Site Goals
- Provide a simple and enjoyable shopping experience for users.  
- Allow customers to easily browse, filter, and purchase photographs.  
- Ensure secure payments and order tracking.  
- Provide store owners with efficient tools to manage products and orders.  
- Maintain responsiveness and accessibility across all devices.  

---

### Scope / User Stories
The project is broken down into Epics and User Stories for clarity and implementation:

#### Epic 1: Project Setup, Agile & Deployment
**Goal:**  
Set up the project environment, GitHub repo, Agile board, and prepare for deployment on Heroku. Ensure secret keys are protected in `.env`.  

**User Stories:**  
- As a developer, I want to set up the Django project with proper environment configuration so that I can start development securely.  
- As a developer, I want to maintain a GitHub Project Board so that I can track progress of all User Stories.  
- As a developer, I want to deploy the app to Heroku so that it can be accessed online.  

**MoSCoW Priority:** Must Have  
**Related to:** Environment Setup, GitHub, Heroku, Agile  

---

#### Epic 2: User Accounts & Authentication
**Goal:**  
Allow visitors to register and existing customers to log in securely. Users can manage profiles and view past orders.  

**User Stories:**  
- As a visitor, I want to sign up with my email so that I can create an account.  
- As a customer, I want to log in/out securely so that I can access my profile and orders.  
- As a customer, I want to view my order history so that I can keep track of my purchased photographs.  

**MoSCoW Priority:** Must Have  
**Related to:** Django Auth, User Profiles, Security  

---

#### Epic 3: Browsing & Products
**Goal:**  
Enable users to browse a photography catalog. Customers can filter by category and view detailed product information.  

**User Stories:**  
- As a visitor, I want to view a gallery of printed photographs so that I can explore available artworks.  
- As a customer, I want to filter photographs by category (landscape, portrait, abstract…) so that I can easily find the style I like.  
- As a customer, I want to view details of each photograph (title, description, size, price, preview) so that I can make an informed decision before buying.  

**MoSCoW Priority:** Must Have  
**Related to:** Product Catalog, Gallery, Filtering  

---

#### Epic 4: Shopping Cart & Checkout
**Goal:**  
Provide a shopping cart and checkout flow so customers can manage their purchases before completing the order.  

**User Stories:**  
- As a customer, I want to add a photograph print to my shopping cart so that I can purchase it later.  
- As a customer, I want to update quantities or remove items from my cart so that I can manage my order.  
- As a customer, I want to proceed to a secure checkout page so that I can finalize my purchase.  

**MoSCoW Priority:** Must Have  
**Related to:** Cart, Checkout, Orders  

---

#### Epic 5: Payments
**Goal:**  
Allow customers to pay securely using Stripe. Provide confirmation after payment to ensure trust and successful order placement.  

**User Stories:**  
- As a customer, I want to pay for my order using Stripe so that my payment is processed safely.  
- As a customer, I want to receive a confirmation after successful payment so that I know my order was placed.  

**MoSCoW Priority:** Must Have  
**Related to:** Stripe, Secure Payments, Checkout  

---

#### Epic 6: Admin & Store Management
**Goal:**  
Provide store owners with tools to manage products. Owners can add, edit, and remove photographs to keep the catalog accurate and updated.  

**User Stories:**  
- As a store owner, I want to add new photograph products so that I can update my catalog.  
- As a store owner, I want to edit existing product details so that the information stays accurate.  
- As a store owner, I want to delete old or discontinued products so that my store stays relevant.  

**MoSCoW Priority:** Should Have  
**Related to:** Product Management, Admin Dashboard  

---

#### Epic 7: Customer Support & Info
**Goal:**  
Provide customers with support and essential information (contact, policies). Clear policies build trust and improve customer experience.  

**User Stories:**  
- As a customer, I want to see a contact section so that I can reach out for questions.  
- As a customer, I want to read a return/refund policy so that I feel safe buying prints online.  
- As a customer, I want to see a privacy policy page so that I know how my data is handled.  

**MoSCoW Priority:** Should Have  
**Related to:** Customer Trust, Support, Policies  

---

#### Epic 8: Testing & Documentation
**Goal:**  
Ensure the application is fully tested and documented for academic and professional standards.  

**User Stories:**  
- As a developer, I want to write and run manual and automated tests so that I can confirm the app works correctly.  
- As a developer, I want to document my wireframes, ERD, and testing so that the project meets Code Institute’s requirements.  

**MoSCoW Priority:** Must Have  
**Related to:** Testing, Documentation, Code Institute Standards  

---
## Skeleton / Wireframes

Below are the wireframes for the main pages of the **Fotolio** project.

<details>
  <summary>Wireframes</summary>

  ### Home
  ![Home](documentation/wireframes/home.png)

  ### Gallery
  ![Gallery](documentation/wireframes/gallery.png)

  ### Product List
  ![Product List](documentation/wireframes/product-list.png)

  ### Product Detail
  ![Product Detail](documentation/wireframes/product-detail.png)

  ### Cart
  ![Cart](documentation/wireframes/cart.png)

  ### Checkout
  ![Checkout](documentation/wireframes/checkout.png)

  ### Sign In
  ![Sign In](documentation/wireframes/singin.png)

  ### Sign Up
  ![Sign Up](documentation/wireframes/singup.png)

  ### Privacy Policy
  ![Privacy Policy](documentation/wireframes/privacy-policy.png)

  ### Refund Policy
  ![Refund Policy](documentation/wireframes/refound-policy.png)

  ### About Us
  ![About](documentation/wireframes/about.png)

  ### Contact
  ![Contact](documentation/wireframes/contact.png)

  ### Footer
  ![Footer](documentation/wireframes/footer.png)

  ### Error Pages
  ![404](documentation/wireframes/404.png)
  ![500](documentation/wireframes/500.png)

</details>

---

## Surface

### Colour Scheme

| Swatch | Hex | Name | Usage |
|---|---|---|---|
| ![FFFFFF](documentation/colors/%23FFFFFF.png) | `#FFFFFF` | White | Page background, product cards, high-contrast surfaces. |
| ![F8F9FA](documentation/colors/%23F8F9FA.png) | `#F8F9FA` | Light Gray | Section backgrounds, subtle separators. |
| ![1C1C1C](documentation/colors/%231C1C1C.png) | `#1C1C1C` | Charcoal | **Header** and **Footer** (hybrid theme dark areas). |
| ![111111](documentation/colors/%23111111.png) | `#111111` | Ink | Primary text on light backgrounds. |
| ![5F6368](documentation/colors/%235F6368.png) | `#5F6368` | Muted Gray | Secondary text, helper labels. |
| ![28E98C](documentation/colors/%2328E98C.png) | `#28E98C` | Neon Green | **Primary accent/CTA** (Shop Now, Add to Cart). |
| ![031E11](documentation/colors/%23031E11.png) | `#031E11` | Accent Ink | Text on neon-green buttons (contrast). |
| ![198754](documentation/colors/%23198754.png) | `#198754` | Bootstrap Green | Success alerts (e.g., “Order confirmed”). |
| ![DC3545](documentation/colors/%23DC3545.png) | `#DC3545` | Bootstrap Red | Errors / destructive actions. |
| ![0D6EFD](documentation/colors/%230D6EFD.png) | `#0D6EFD` | Bootstrap Blue *(optional)* | Links / secondary CTAs (use sparingly). |

> **Theme principle:** Light content area for photo clarity + dark header/footer for premium contrast + bold neon-green accent for actions.

---

### Typography
- **Primary font:** *Inter* (400 / 500 / 700) for clean, modern legibility across devices.  
- **Headings:** 700; **UI labels / buttons:** 500; **body:** 400.  
- **Fallbacks:** `system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif`.  
- **Line height:** ~1.5 for body; headings tight at ~1.1–1.2.  
- **Accessibility:** Maintain contrast ratio ≥ 4.5:1 (ink on white, white on charcoal, accent-ink on neon green).

---

### Icons
- **Set:** Bootstrap Icons.  
- **Usage:** navigation, social, feedback.  
- **A11y:** include `aria-label` or `title` for every icon link; avoid color-only meaning—pair with text where important.

---

### Buttons
- **Primary CTA (accent):** background `#28E98C`, text `#031E11`, subtle shadow/hover lift.  
- **Secondary (neutral):** white background with light border; hover adds shadow.  
- **On dark header/footer:** keep buttons either **accent** or **outline/ghost** with white text.  
- **States:** `:hover` lift/shadow, `:focus-visible` ring using semi-transparent accent (`rgba(40,233,140,.45)`), disabled reduced opacity.

---

### Feedback Colors (Bootstrap Alerts)
- **Success:** `#198754` — order placed, payment success, profile saved.  
- **Error/Danger:** `#DC3545` — payment failed, form errors, destructive actions.  
- **Info/Neutral (optional):** `#0D6EFD` — notices and non-critical hints.  
- Always accompany colored alerts with clear icons/text for accessibility.

---

## Back To Top
[🔝 Back to Top](#fotolio)
