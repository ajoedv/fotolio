document.addEventListener("DOMContentLoaded", () => {
    console.log("Fotolio JS initialized");

    // Hero background slider
    const heroBg = document.querySelector(".hero-bg");
    const dots = document.querySelectorAll(".hero-dot");

    if (heroBg && dots.length > 0) {
        const slides = [
            "/static/img/hero/hero-1.webp",
            "/static/img/hero/hero-2.webp",
            "/static/img/hero/hero-3.webp"
        ];

        let currentIndex = 0;
        let timerId = null;
        const intervalMs = 7000;

        function setSlide(index) {
            if (index < 0 || index >= slides.length) {
                return;
            }

            currentIndex = index;
            heroBg.style.backgroundImage = `url("${slides[index]}")`;

            dots.forEach((dot, i) => {
                dot.classList.toggle("active", i === index);
            });
        }

        function nextSlide() {
            const nextIndex = (currentIndex + 1) % slides.length;
            setSlide(nextIndex);
        }

        function resetTimer() {
            if (timerId) {
                clearInterval(timerId);
            }
            timerId = setInterval(nextSlide, intervalMs);
        }

        dots.forEach((dot, index) => {
            dot.addEventListener("click", () => {
                setSlide(index);
                resetTimer();
            });
        });

        setSlide(0);
        resetTimer();
    }

    // Navbar scroll behavior
    const header = document.querySelector(".site-header");
    const hasHero = document.querySelector(".hero-section");

    if (header) {
        function handleScroll() {
            if (!hasHero) {
                header.classList.add("scrolled");
                return;
            }

            if (window.scrollY > 40) {
                header.classList.add("scrolled");
            } else {
                header.classList.remove("scrolled");
            }
        }

        window.addEventListener("scroll", handleScroll);
        window.addEventListener("load", handleScroll);
        handleScroll();
    }

    // Product teaser slider (You may also like)
    const sliders = document.querySelectorAll(".product-related-slider");

    sliders.forEach((slider) => {
        const track = slider.querySelector(".product-related-track");
        const arrowPrev = slider.querySelector(".product-related-arrow-left");
        const arrowNext = slider.querySelector(".product-related-arrow-right");

        if (!track || !arrowPrev || !arrowNext) {
            return;
        }

        function getStep() {
            return track.clientWidth * 0.8;
        }

        arrowPrev.addEventListener("click", () => {
            track.scrollBy({
                left: -getStep(),
                behavior: "smooth",
            });
        });

        arrowNext.addEventListener("click", () => {
            track.scrollBy({
                left: getStep(),
                behavior: "smooth",
            });
        });

        let autoTimer = setInterval(() => {
            track.scrollBy({
                left: getStep(),
                behavior: "smooth",
            });
        }, 8000);

        slider.addEventListener("mouseenter", () => {
            clearInterval(autoTimer);
        });

        slider.addEventListener("mouseleave", () => {
            autoTimer = setInterval(() => {
                track.scrollBy({
                    left: getStep(),
                behavior: "smooth",
                });
            }, 8000);
        });
    });

    // Auto-dismiss alerts
    const alerts = document.querySelectorAll(".auto-dismiss-alert");

    alerts.forEach((alert) => {
        setTimeout(() => {
            $(alert).alert("close");
        }, 4000);
    });
});