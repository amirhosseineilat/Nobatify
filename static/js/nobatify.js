document.addEventListener("DOMContentLoaded", () => {
    const nav = document.getElementById("site-nav");
    const mobileButton = document.querySelector(".mobile-menu-btn");
    const mobileMenu = document.querySelector(".mobile-menu");

    const updateNav = () => {
        if (!nav) return;
        nav.classList.toggle("pt-2", window.scrollY > 20);
        nav.classList.toggle("pt-4", window.scrollY <= 20);
    };
    window.addEventListener("scroll", updateNav, { passive: true });
    updateNav();

    mobileButton?.addEventListener("click", () => {
        const open = mobileButton.getAttribute("aria-expanded") === "true";
        mobileButton.setAttribute("aria-expanded", String(!open));
        mobileMenu?.classList.toggle("hidden");
    });

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("is-visible");
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });

    document.querySelectorAll(".reveal-up, .reveal-scale, .reveal-left, .reveal-right").forEach((el) => observer.observe(el));

    document.querySelectorAll(".magnetic").forEach((button) => {
        button.addEventListener("mousemove", (event) => {
            const rect = button.getBoundingClientRect();
            const x = (event.clientX - rect.left - rect.width / 2) * 0.10;
            const y = (event.clientY - rect.top - rect.height / 2) * 0.10;
            button.style.transform = `translate(${x}px, ${y}px)`;
        });
        button.addEventListener("mouseleave", () => {
            button.style.transform = "";
        });
    });

    document.querySelectorAll(".btn").forEach((button) => {
        button.addEventListener("click", () => {
            button.classList.add("button-pop");
            window.setTimeout(() => button.classList.remove("button-pop"), 220);
        });
    });
});
