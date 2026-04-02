# Fotolio

A full-stack e-commerce web application for selling printed photography, with secure Stripe payments, user accounts, order management, and a responsive shopping experience.

---

![Fotolio mockup](documentation/readme/fotolio-mockup.png)

---

## Contents
1. [Live Demo](#live-demo)
2. [Test User](#test-user)
3. [Overview](#overview)
4. [Project Summary](#project-summary)
5. [Target Audience](#target-audience)
6. [User Needs and How the Site Meets Them](#user-needs-and-how-the-site-meets-them)
7. [E-commerce Business Model](#e-commerce-business-model)
8. [Agile Methodology](#agile-methodology)
9. [User Experience (UX)](#user-experience-ux)
   1. [Strategy / Site Goals](#strategy--site-goals)
   2. [Scope / User Stories](#scope--user-stories)
   3. [Structure / Design Choices](#structure--design-choices)
   4. [Skeleton / Wireframes](#skeleton--wireframes)
   5. [Surface](#surface)
      1. [Colour Scheme](#colour-scheme)
      2. [Typography](#typography)
      3. [Icons](#icons)
      4. [Buttons](#buttons)
      5. [Feedback Colors](#feedback-colors)
10. [Features](#features)
    1. [Existing Features](#existing-features)
    2. [Future Features](#future-features)
11. [Technologies Used](#technologies-used)
12. [Database Schema](#database-schema)
    1. [Data Model Overview](#data-model-overview)
    2. [Entity Relationship Diagram](#entity-relationship-diagram)
13. [Testing](#testing)
14. [SEO](#seo)
15. [Marketing Strategy](#marketing-strategy)
16. [Deployment](#deployment)
    1. [Local Development](#local-development)
    2. [PostgreSQL Setup](#postgresql-setup)
    3. [Environment Variables](#environment-variables)
    4. [Heroku Deployment](#heroku-deployment)
    5. [Static Files and Media](#static-files-and-media)
    6. [Migrations](#migrations)
17. [Credits](#credits)
18. [Acknowledgements](#acknowledgements)


---

## Live Demo
🔗 [Fotolio Live Site](https://fotolio-joe-p5-1bff429e735e.herokuapp.com/)

---

## Test User

To allow the project to be explored without creating a new account, the following test user can be used:

- **Username:** `fotolio.tester`
- **Email:** `fotolio.tester@example.com`
- **Password:** `Testuser123!`

This account can be used to:
- Sign in to the site
- View the user profile page
- Access order history
- Test authenticated user features such as cart, checkout flow, and account-related navigation

> Note: This is a standard test account provided for assessment purposes only. No sensitive personal data is associated with this account.

### Stripe Test Payments

When testing the checkout process, Stripe test card details can be used. For example:

- **Card Number:** `4242 4242 4242 4242`
- **Expiry Date:** Any future date
- **CVC:** Any 3 digits
- **ZIP / Postcode:** Any valid value

These test details allow the full checkout flow to be completed without making a real payment.

---


## Overview
Fotolio is an e-commerce web application designed for selling printed photography.  
Users can browse collections, filter by category, view product details, add items to a cart, and complete purchases securely using Stripe.  
The platform is built with Django, PostgreSQL, and Bootstrap, following Agile methodology and UX best practices.  
The site is fully responsive and optimized for a smooth user shopping experience.

---

## Project Summary

Fotolio is a full-stack e-commerce application created to provide a clean, visually focused, and user-friendly platform for selling printed photography online. The project was developed as a commercial-style online store where users can browse photographic prints, explore product categories, view detailed product information, and complete purchases through a secure checkout experience.

The application is designed to balance presentation and functionality. Because photography is a highly visual product, the site places strong emphasis on layout clarity, image presentation, and simple navigation, while also supporting the practical requirements of an e-commerce platform such as user accounts, order history, cart management, and secure Stripe payments.

From a business perspective, Fotolio represents a digital storefront for photography-based products, allowing store owners to showcase and manage their catalogue while giving customers a straightforward and trustworthy shopping journey. The project combines front-end user experience considerations with full-stack functionality, database-driven content, and secure payment processing to create a complete e-commerce solution.

---

## Target Audience

Fotolio is aimed at customers who are interested in buying printed photography through a simple and visually engaging online shopping experience. The primary target audience includes art lovers, photography enthusiasts, and customers looking for decorative wall prints for personal spaces such as homes, offices, or creative studios.

The site is also designed for users who value a clear and trustworthy e-commerce journey. This includes customers who want to browse products easily, compare options by category, view photography in detail before purchasing, and complete checkout securely without unnecessary complexity.

From the business side, the platform also serves the needs of a store owner or photography brand that wants to present products professionally, manage catalogue content efficiently, and offer customers a modern online storefront with secure payments and account-based order tracking.

---

## User Needs and How the Site Meets Them

The project was designed around the needs of both customers and the store owner.

For customers, the main need is a shopping experience that is simple, visually clear, and secure. Users need to be able to browse photography products easily, narrow results by category, view individual product details, and understand what they are purchasing before committing to an order. Fotolio addresses this by providing a clear gallery layout, category filtering, detailed product pages, pricing information, and a streamlined cart and checkout flow.

Customers also need confidence when purchasing online. The site supports this through secure Stripe payment processing, visible order confirmation, account registration and login functionality, and access to order history through the user profile area. Supporting pages such as contact, privacy policy, and refund information also help build trust and transparency.

For the store owner, the main need is to manage products efficiently and maintain an up-to-date online catalogue. Fotolio meets this need through Django’s admin functionality and product management features, allowing authorised users to add, edit, and remove products as needed. This supports the commercial purpose of the application while keeping the product catalogue accurate and maintainable.

---

## E-commerce Business Model

Fotolio follows a direct-to-consumer e-commerce model in which printed photography products are presented and sold through a dedicated online storefront. Customers can browse the catalogue, select the prints they wish to purchase, add them to the cart, and complete payment online through Stripe.

The business model is based on selling photography prints as individual retail products. Revenue is generated per order, with each completed checkout representing a direct sale to the customer. This makes the platform suitable for a photography brand, independent photographer, or print-focused online store that wants to sell curated visual work in a professional and scalable way.

The commercial value of the project lies in combining strong visual presentation with practical e-commerce functionality. Because photography is a product that depends heavily on presentation and trust, the platform is designed to support both. Customers are given a clear product browsing and checkout experience, while the store owner benefits from a manageable catalogue, secure payment processing, and an online sales channel that can be maintained and expanded over time.

---

## Agile Methodology

This project was developed using Agile principles to support structured planning, incremental progress, and clear task management throughout the development process. GitHub Issues and GitHub Projects were used to organise and track the work, allowing features to be planned, implemented, reviewed, and updated in a transparent way.

The project was divided into **Epics** and **User Stories** to break the application into manageable areas of development. Each User Story represented a specific feature, goal, or task, helping to maintain clarity during implementation and making progress easier to monitor throughout the project lifecycle.

To support prioritisation, the project used the **MoSCoW method**, where tasks were classified as **Must Have**, **Should Have**, **Could Have**, or **Won’t Have**. This helped focus development on the core features required to deliver a functional e-commerce application first, while also identifying secondary enhancements and future improvements.

The Agile workflow supported a practical and iterative development process. Features were planned in advance, implemented step by step, and then reviewed through testing, refinement, and documentation. This structure helped ensure that the final project remained aligned with its original goals while still allowing flexibility during development.

The GitHub Project Board was used as the central planning tool, with issues mapped to User Stories and grouped under relevant Epics. This provided a clear overview of the project structure and made it easier to track completed work, active tasks, and the overall development progress of the application.

---

## User Experience (UX)

### Strategy / Site Goals

The main strategic goal of Fotolio was to create a visually engaging and commercially relevant e-commerce application for selling printed photography. The project was designed to combine strong visual presentation with the practical functionality expected from a modern online store.

The core site goals were to:

- Provide a simple, enjoyable, and intuitive shopping experience
- Allow customers to browse, filter, and purchase photography prints with ease
- Support secure online payments and clear order tracking
- Provide store owners with practical tools for managing products and store content
- Maintain responsive and accessible design across desktop, tablet, and mobile devices

---

### Scope / User Stories

To support development, the project was organised into a series of Epics and related User Stories. This helped define the scope of the application clearly and ensured that each major area of functionality was planned with a user-focused purpose.

#### Epic 1: Project Setup, Agile & Deployment

**Goal:**  
Set up the project structure, repository, Agile board, and deployment workflow, while ensuring that sensitive configuration is handled securely through environment variables.

**User Stories:**
- As a developer, I want to set up the Django project with proper environment configuration so that I can start development securely.
- As a developer, I want to maintain a GitHub Project Board so that I can track the progress of all User Stories.
- As a developer, I want to deploy the app to Heroku so that it can be accessed online.

**MoSCoW Priority:** Must Have  
**Related Areas:** Environment Setup, GitHub, Heroku, Agile

---

#### Epic 2: User Accounts & Authentication

**Goal:**  
Allow visitors to register and existing users to log in securely, while also giving authenticated users access to profile-related features such as order history.

**User Stories:**
- As a visitor, I want to sign up with my email so that I can create an account.
- As a customer, I want to log in and out securely so that I can access my profile and orders.
- As a customer, I want to view my order history so that I can keep track of my purchased photographs.

**MoSCoW Priority:** Must Have  
**Related Areas:** Django Authentication, User Profiles, Security

---

#### Epic 3: Browsing & Products

**Goal:**  
Enable users to browse the photography catalogue, filter products by category, and view detailed product information before making a purchase decision.

**User Stories:**
- As a visitor, I want to view a gallery of printed photographs so that I can explore available artworks.
- As a customer, I want to filter photographs by category so that I can easily find the style I prefer.
- As a customer, I want to view details of each photograph, such as title, description, size, price, and preview, so that I can make an informed decision before buying.

**MoSCoW Priority:** Must Have  
**Related Areas:** Product Catalogue, Gallery, Filtering

---

#### Epic 4: Shopping Cart & Checkout

**Goal:**  
Provide customers with a clear and manageable cart and checkout process so they can review and complete their purchases smoothly.

**User Stories:**
- As a customer, I want to add a photograph print to my shopping cart so that I can purchase it later.
- As a customer, I want to update quantities or remove items from my cart so that I can manage my order.
- As a customer, I want to proceed to a secure checkout page so that I can finalise my purchase.

**MoSCoW Priority:** Must Have  
**Related Areas:** Cart, Checkout, Orders

---

#### Epic 5: Payments

**Goal:**  
Allow customers to complete payment securely through Stripe and receive confirmation that their order has been successfully placed.

**User Stories:**
- As a customer, I want to pay for my order using Stripe so that my payment is processed securely.
- As a customer, I want to receive confirmation after a successful payment so that I know my order was placed correctly.

**MoSCoW Priority:** Must Have  
**Related Areas:** Stripe, Secure Payments, Checkout

---

#### Epic 6: Admin & Store Management

**Goal:**  
Provide store management functionality that allows authorised users to add, edit, and remove products in order to maintain an accurate and current catalogue.

**User Stories:**
- As a store owner, I want to add new photograph products so that I can update my catalogue.
- As a store owner, I want to edit existing product details so that the information remains accurate.
- As a store owner, I want to delete old or discontinued products so that the store remains relevant and up to date.

**MoSCoW Priority:** Should Have  
**Related Areas:** Product Management, Admin Features

---

#### Epic 7: Customer Support & Information

**Goal:**  
Provide customers with key support and policy information that improves trust, transparency, and overall confidence in the shopping experience.

**User Stories:**
- As a customer, I want to see a contact section so that I can reach out with questions.
- As a customer, I want to read a return and refund policy so that I feel more confident purchasing prints online.
- As a customer, I want to see a privacy policy page so that I understand how my data is handled.

**MoSCoW Priority:** Should Have  
**Related Areas:** Customer Trust, Support, Policies

---

#### Epic 8: Testing & Documentation

**Goal:**  
Ensure that the application is fully tested and documented to meet both academic and professional project standards.

**User Stories:**
- As a developer, I want to write and run manual and automated tests so that I can confirm the application works correctly.
- As a developer, I want to document wireframes, the ERD, and the testing process so that the project clearly demonstrates its planning, structure, and validation.

**MoSCoW Priority:** Must Have  
**Related Areas:** Testing, Documentation, Project Validation

---

### Structure / Design Choices

Fotolio was structured as a multi-app Django project to separate core areas of functionality and keep the codebase organised and maintainable. This approach supports scalability, clearer responsibility across different parts of the application, and easier future development.

The main project structure was divided into focused applications such as product browsing, cart and checkout, user profiles, newsletter functionality, and static content pages. This separation reflects the main user journeys of the site and helps keep related models, views, templates, and tests grouped logically.

From a design perspective, the application was built to support a visually led e-commerce experience. Because photography products rely heavily on presentation, the layout was designed to prioritise imagery, clear calls to action, and straightforward navigation. The interface uses a dark, premium-inspired visual style combined with high-contrast content areas so that product images remain the main focus.

The navigation structure was kept intentionally simple to reduce friction in the buying journey. Users can move easily from browsing, to product detail, to cart, to checkout, while account-related actions such as sign in, profile access, and order history remain accessible without overwhelming the main shopping flow.

The overall design choices were made to balance aesthetics and usability. The site aims to feel polished and brand-led while still delivering the practical features expected from a commercial e-commerce platform, including trust-building pages, secure checkout, responsive design, and clear user feedback throughout the shopping process.

---

### Skeleton / Wireframes

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

### Surface

The visual design of Fotolio was developed to support a premium, image-led shopping experience.


#### Colour Scheme

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

#### Typography
- **Primary font:** *Inter* (400 / 500 / 700) for clean, modern legibility across devices.  
- **Headings:** 700; **UI labels / buttons:** 500; **body:** 400.  
- **Fallbacks:** `system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif`.  
- **Line height:** ~1.5 for body; headings tight at ~1.1–1.2.  
- **Accessibility:** Maintain contrast ratio ≥ 4.5:1 (ink on white, white on charcoal, accent-ink on neon green).

---

#### Icons
- **Set:** Bootstrap Icons.  
- **Usage:** navigation, social, feedback.  
- **A11y:** include `aria-label` or `title` for every icon link; avoid color-only meaning—pair with text where important.

---

#### Buttons
- **Primary CTA (accent):** background `#28E98C`, text `#031E11`, subtle shadow/hover lift.  
- **Secondary (neutral):** white background with light border; hover adds shadow.  
- **On dark header/footer:** keep buttons either **accent** or **outline/ghost** with white text.  
- **States:** `:hover` lift/shadow, `:focus-visible` ring using semi-transparent accent (`rgba(40,233,140,.45)`), disabled reduced opacity.

---

#### Feedback Colors
- **Success:** `#198754` — order placed, payment success, profile saved.  
- **Error/Danger:** `#DC3545` — payment failed, form errors, destructive actions.  
- **Info/Neutral (optional):** `#0D6EFD` — notices and non-critical hints.  
- Always accompany colored alerts with clear icons/text for accessibility.

---

## Features

### Existing Features

- **Responsive homepage and visual storefront**  
  The site presents photography prints in a visually led layout designed to work across desktop, tablet, and mobile devices.

- **Product browsing and gallery view**  
  Users can explore the available photography prints through a dedicated gallery and product listing experience.

- **Category filtering**  
  Products can be filtered by category, making it easier for users to narrow down the catalogue and find prints that match their interests.

- **Product detail pages**  
  Each product includes detailed information such as title, description, image, and price so that customers can make informed purchase decisions.

- **Search functionality**  
  Users can search the catalogue to find products more quickly.

- **Shopping cart management**  
  Customers can add products to the cart, update quantities, and remove items before checkout.

- **Secure checkout and payment processing**  
  The checkout flow is integrated with Stripe, allowing users to complete purchases securely using Stripe card payments.

- **Order confirmation**  
  After a successful payment, users receive confirmation that the order has been placed.

- **User registration and authentication**  
  Visitors can create an account, sign in, and sign out securely.

- **User profile and order history**  
  Registered users can access their profile information and review previous orders.

- **Admin product management**  
  Authorised users can add, edit, and delete products, allowing the store catalogue to be maintained efficiently.

- **Contact and information pages**  
  The site includes supporting pages such as contact, privacy policy, refund policy, and about content to improve trust and usability.

- **Newsletter signup**  
  Users can subscribe to the newsletter as part of the site’s marketing and customer engagement features.

- **Custom error pages**  
  Custom 404 and 500 pages are included to provide a more consistent user experience when errors occur.

- **SEO foundations**  
  The application includes page-specific metadata, sitemap.xml, robots.txt, canonical links, and a custom 404 page to support discoverability and search visibility.

### Future Features

Future improvements for Fotolio could include product variants such as multiple print sizes or framing options, wishlist functionality, discount and promotional code support, more advanced filtering and sorting options, enhanced customer account settings, and a stronger admin analytics dashboard for store management. These additions would further improve both the shopping experience and the commercial value of the platform.

---

## Technologies Used

### Languages
- HTML5
- CSS3
- JavaScript
- Python

### Frameworks, Libraries, and Packages
- Django
- Bootstrap 4
- Django Allauth
- Gunicorn
- psycopg2-binary
- Stripe
- Cloudinary
- django-cloudinary-storage
- WhiteNoise

### Database
- PostgreSQL for the production database
- SQLite for local development and testing where applicable

### Hosting and Deployment
- Heroku for application deployment and cloud hosting

### Tools and Services
- Git for version control
- GitHub for repository hosting and project management
- GitHub Projects for Agile planning
- Balsamiq for wireframes
- Google Fonts
- Bootstrap Icons
- Adobe Express / Adobe tools for mockups and presentation assets

---

## Database Schema

### Data Model Overview

Fotolio uses a relational database structure to support the main functionality of the application, including product browsing, user accounts, reviews, cart and checkout, order processing, and newsletter subscriptions. The database design was created to keep the data organised, scalable, and suitable for a full-stack e-commerce platform.

The main models work together to support both the customer journey and store management. Products are grouped into categories, users can create accounts and maintain profile information, authenticated users can leave reviews, and completed purchases are stored as orders with related order line items. Additional models support features such as newsletter subscriptions and other related site functionality where required.

This relational structure allows the application to manage linked data efficiently while keeping responsibilities clearly separated across the project. It also supports future growth by making it easier to extend the catalogue, user functionality, and store features over time.

### Entity Relationship Diagram

![Fotolio ERD](documentation/erd/fotolio-erd.png)

---

## Testing

Testing for Fotolio is documented in a dedicated testing file:

[View full testing documentation](TESTING.md)

The testing process for this project included:

- Manual testing of key user journeys and core e-commerce functionality
- Automated Django testing across the main applications
- Stripe test payment verification
- Python, HTML, CSS, and JavaScript validation
- Accessibility testing
- Responsiveness testing across different screen sizes
- Cross-browser testing
- Lighthouse performance, accessibility, best practices, and SEO checks
- Documentation of bugs found and the fixes applied

The full details, evidence, test results, and screenshots are provided in `TESTING.md`.

---

## SEO

Fotolio includes several core SEO features to improve search visibility and help the site present content clearly to both users and search engines.

The project uses page-specific meta descriptions across key pages such as the home page, about page, contact page, product listing page, and product detail pages. This helps provide more relevant search snippets and improves how each page is described in search results.

The application also uses clear page titles and a global canonical link strategy to reduce duplication issues and provide a consistent preferred URL structure across the site.

To support crawling and indexing, the project includes both a `robots.txt` file and a `sitemap.xml` file. These help search engines understand which areas of the site can be crawled and where the main site content is located.

A custom 404 page is also included, which improves user experience when a non-existent page is accessed and supports a more polished overall site structure.

These SEO foundations were implemented to align with the commercial purpose of the project and improve discoverability for users searching for printed photography and related visual products online.

---

## Marketing Strategy

Fotolio was designed not only as a functional e-commerce platform, but also as a brand-led online storefront for reaching customers interested in printed photography. The marketing strategy focuses on combining visual branding, social media presence, on-site email capture, and SEO foundations to improve audience reach and support long-term growth.

A key part of this strategy is social media visibility. As part of its marketing foundation, Fotolio has branded Facebook and Instagram pages that support the project’s visual identity and provide a basis for future audience engagement and promotion on platforms that are well suited to photography-based content.

The site also includes a newsletter signup feature, allowing visitors to subscribe for updates, offers, and future product releases. This supports direct communication with interested users and creates an owned marketing channel beyond third-party social platforms.

In addition, the project uses core SEO features such as meta descriptions, page titles, canonical links, `robots.txt`, and `sitemap.xml` to support discoverability through search engines. This helps users find the site organically when searching for photography prints and related visual products.

Together, these elements create a simple but relevant marketing foundation for a photography e-commerce brand: brand visibility through social media, direct audience retention through newsletter signup, and search visibility through SEO implementation.

---

## Deployment

### Local Development

To work on Fotolio locally, the repository can be cloned from GitHub and opened in a development environment such as VS Code.

1. Clone the repository:

        git clone https://github.com/ajoedv/fotolio.git

2. Move into the project directory:

        cd fotolio

3. Create and activate a virtual environment:

        python3 -m venv .venv
        source .venv/bin/activate

4. Install the project requirements:

        pip install -r requirements.txt

5. Create a `.env` file in the project root and add the required environment variables.

6. Apply migrations:

        python manage.py migrate

7. Create a superuser if needed:

        python manage.py createsuperuser

8. Run the development server:

        python manage.py runserver

The site will then be available locally through the Django development server.

### PostgreSQL Setup

Fotolio uses SQLite for local development by default and PostgreSQL in production.

In `settings.py`, the default local database is configured as SQLite:

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

When a `DATABASE_URL` environment variable is present, the project automatically switches to PostgreSQL using `dj-database-url`:

    if "DATABASE_URL" in os.environ:
        DATABASES["default"] = dj_database_url.config(
            conn_max_age=600,
            ssl_require=True,
        )

This setup keeps local development simple while using a production-ready PostgreSQL database on Heroku.

### Environment Variables

Sensitive values are not stored directly in the codebase. Instead, Fotolio uses environment variables for security and deployment flexibility.

Examples of environment variables used by the project include:

- `SECRET_KEY`
- `DEBUG`
- `DATABASE_URL`
- `STRIPE_PUBLIC_KEY`
- `STRIPE_SECRET_KEY`
- `STRIPE_CURRENCY`
- `CLOUDINARY_URL`

These values should be added either to a local `.env` file for development or to Heroku Config Vars for the deployed application.

### Heroku Deployment

Fotolio is deployed to Heroku as a cloud-hosted Django application.

The confirmed deployment setup for this project includes:

- **Heroku app name:** `fotolio-joe-p5`
- **Live site URL:** `https://fotolio-joe-p5-1bff429e735e.herokuapp.com/`
- **GitHub repository:** `https://github.com/ajoedv/fotolio`
- **GitHub integration:** Connected
- **Automatic deploys:** Enabled from the `main` branch
- **Direct Heroku deployment:** Also supported through `git push heroku main`
- **Heroku stack:** `heroku-24`
- **Database add-on:** Heroku Postgres
- **Dyno formation:** `web: 1`

The deployment setup also includes:

1. A valid `Procfile` for Gunicorn
2. A defined Python version in `.python-version`
3. Static file handling through WhiteNoise
4. Media storage through Cloudinary
5. A production PostgreSQL database
6. Environment variables configured through Heroku Config Vars
7. Database migrations applied to the production database

The project includes the following production deployment files:

`Procfile`

    web: gunicorn fotolio.wsgi

`.python-version`

    3.12


### Static Files and Media

Static files are served using WhiteNoise. In `settings.py`, the static configuration includes:

- `STATIC_URL`
- `STATICFILES_DIRS`
- `STATIC_ROOT`
- `STATICFILES_STORAGE`

This allows static assets such as CSS, JavaScript, fonts, and images to be collected and served correctly in production.

Uploaded media files are handled through Cloudinary using:

- `cloudinary`
- `django-cloudinary-storage`

In `settings.py`, media storage is configured with:

    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
    MEDIA_URL = "/media/"

This allows uploaded assets such as product images and user avatars to be stored through Cloudinary rather than the local filesystem.

### Migrations

After setting up the database, migrations must be applied so that the schema matches the Django models.

To apply migrations locally:

    python manage.py migrate

If new migrations are needed:

    python manage.py makemigrations
    python manage.py migrate

This step is also required after deployment when changes are made to the database schema.

---

## Credits

The Fotolio project was developed as a full-stack e-commerce application using the Code Institute Boutique Ado walkthrough project as a learning foundation for core commerce concepts such as product handling, cart logic, checkout flow, and Stripe integration. The final project was substantially expanded, redesigned, and customised to create an original photography print storefront with its own structure, styling, content, and supporting features.

The following resources, libraries, and tools were used during development:

- **Code Institute learning materials** for project structure, Django development workflow, and e-commerce concepts
- **Boutique Ado walkthrough project** as a reference point for core learning and implementation patterns
- **Django documentation** for framework guidance and best practices
- **Bootstrap documentation** for layout, components, and responsive design
- **Stripe documentation** for payment integration and testing
- **Cloudinary documentation** for media storage and delivery
- **Heroku documentation** for deployment and production hosting guidance
- **dbdiagram.io** for creating the ERD diagram
- **Balsamiq** for wireframe creation
- **Adobe Express / Adobe tools** for README mockups and presentation assets
- **Google Fonts** for typography
- **Bootstrap Icons** for interface icons

All additional design decisions, implementation work, testing, debugging, documentation, and project customisation were completed independently as part of the development of this project.

---

## Acknowledgements

I would like to acknowledge Code Institute for the course structure, learning materials, and guidance that supported the development of this project.

I would also like to acknowledge the Boutique Ado walkthrough project as an important learning reference for understanding the structure and workflow of a Django e-commerce application.

Additional acknowledgement goes to the official documentation and tools used throughout the project, including Django, Bootstrap, Stripe, Cloudinary, Heroku, dbdiagram.io, Balsamiq, and Adobe tools.

---

[Back to Top](#fotolio)
